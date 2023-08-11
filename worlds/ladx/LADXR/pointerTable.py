import copy
import struct


class PointerTable:
    END_OF_DATA = (0xff, )

    """
        Class to manage a list of pointers to data objects
        Can rewrite the rom to modify the data objects and still keep the pointers intact.
    """
    def __init__(self, rom, info):
        assert "count" in info
        assert "pointers_bank" in info
        assert "pointers_addr" in info
        assert ("banks_bank" in info and "banks_addr" in info) or ("data_bank" in info)
        self.__info = info

        self.__data = []
        self.__alt_data = {}
        self.__banks = []
        self.__storage = []

        count = info["count"]
        addr = info["pointers_addr"]
        pointers_bank = rom.banks[info["pointers_bank"]]
        if "data_addr" in info:
            pointers_raw = []
            for n in range(count):
                pointers_raw.append(info["data_addr"] + 0x4000 + pointers_bank[addr + n] * info["data_size"])
        else:
            pointers_raw = struct.unpack("<" + "H" * count, pointers_bank[addr:addr+count*2])
        if "data_bank" in info:
            banks = [info["data_bank"]] * count
        else:
            addr = info["banks_addr"]
            banks = rom.banks[info["banks_bank"]][addr:addr+count]

        if "alt_pointers" in self.__info:
            for key, (bank, addr) in self.__info["alt_pointers"].items():
                pointer = struct.unpack("<H", rom.banks[bank][addr:addr+2])[0]
                assert 0x4000 <= pointer < 0x8000
                self.__alt_data[key] = self._readData(rom, self.__info["data_bank"], pointer & 0x3FFF)

        for n in range(count):
            bank = banks[n] & 0x3f
            pointer = pointers_raw[n]
            if 0x4000 <= pointer < 0x8000:
                pointer &= 0x3fff
                self.__data.append(self._readData(rom, bank, pointer))
            else:
                self.__data.append(pointer)
            self.__banks.append(bank)

        while self.__mergeStorage():
            pass
        self.__storage.sort(key=lambda n: n["start"])
        if "claim_storage_gaps" in info and info["claim_storage_gaps"]:
            self.__storage = [{"bank": self.__storage[0]["bank"], "start": self.__storage[0]["start"], "end": self.__storage[-1]["end"]}]
        if "expand_to_end_of_bank" in info and info["expand_to_end_of_bank"]:
            for st in self.__storage:
                if info["expand_to_end_of_bank"] == True or st["bank"] in info["expand_to_end_of_bank"]:
                    expand = True
                    for st2 in self.__storage:
                        if st["bank"] == st2["bank"] and st["end"] < st2["end"]:
                            expand = False
                    if expand:
                        st["end"] = 0x4000
        self.storage = self.__storage

        # for s in sorted(self.__storage, key=lambda s: (s["bank"], s["start"])):
        #     print(self.__class__.__name__, s)

    def __contains__(self, item):
        if isinstance(item, str):
            return item in self.__alt_data
        return 0 <= item < len(self.__data)

    def __setitem__(self, item, value):
        if isinstance(item, str):
            self.__alt_data[item] = value
        else:
            self.__data[item] = value

    def __getitem__(self, item):
        if isinstance(item, str):
            return self.__alt_data[item]
        return self.__data[item]

    def __len__(self):
        return len(self.__data)

    def store(self, rom):
        storage = copy.deepcopy(self.__storage)

        pointers_bank = self.__info["pointers_bank"]
        pointers_addr = self.__info["pointers_addr"]

        done = {}
        for st in storage:
            done[st["bank"]] = {}
        for key, (ptr_bank, ptr_addr) in self.__info.get("alt_pointers", {}).items():
            s = bytes(self.__alt_data[key])
            bank = self.__info["data_bank"]
            my_storage = None
            for st in storage:
                if st["end"] - st["start"] >= len(s) and st["bank"] == bank:
                    my_storage = st
                    break
            assert my_storage is not None, "Not enough room in storage... %s" % (storage)

            pointer = my_storage["start"]
            my_storage["start"] = pointer + len(s)
            rom.banks[bank][pointer:pointer + len(s)] = s

            rom.banks[ptr_bank][ptr_addr] = pointer & 0xFF
            rom.banks[ptr_bank][ptr_addr + 1] = (pointer >> 8) | 0x40

        for n, s in enumerate(self.__data):
            if isinstance(s, int):
                pointer = s
            else:
                s = bytes(s)
                bank = self.__banks[n]
                if s in done[bank]:
                    pointer = done[bank][s]
                    assert rom.banks[bank][pointer:pointer+len(s)] == s
                else:
                    my_storage = None
                    for st in storage:
                        if st["end"] - st["start"] >= len(s) and st["bank"] == bank:
                            my_storage = st
                            break
                    assert my_storage is not None, "Not enough room in storage... %d/%d %s id:%x(%d) bank:%d" % (n, len(self.__data), storage, n, n, bank)

                    pointer = my_storage["start"]
                    my_storage["start"] = pointer + len(s)
                    rom.banks[bank][pointer:pointer+len(s)] = s

                    if "data_size" not in self.__info:
                        # aggressive de-duplication.
                        for skip in range(len(s)):
                            done[bank][s[skip:]] = pointer + skip
                    done[bank][s] = pointer

            if "data_addr" in self.__info:
                offset = pointer - self.__info["data_addr"]
                if "data_size" in self.__info:
                    assert offset % self.__info["data_size"] == 0
                    offset //= self.__info["data_size"]
                rom.banks[pointers_bank][pointers_addr + n] = offset
            else:
                rom.banks[pointers_bank][pointers_addr+n*2] = pointer & 0xff
                rom.banks[pointers_bank][pointers_addr+n*2+1] = ((pointer >> 8) & 0xff) | 0x40

        space_left = sum(map(lambda n: n["end"] - n["start"], storage))
        # print(self.__class__.__name__, "Space left:", space_left)
        return storage

    def _readData(self, rom, bank_nr, pointer):
        bank = rom.banks[bank_nr]
        start = pointer
        if "data_size" in self.__info:
            pointer += self.__info["data_size"]
        else:
            while bank[pointer] not in self.END_OF_DATA:
                pointer += 1
            pointer += 1
        self._addStorage(bank_nr, start, pointer)
        return bank[start:pointer]

    def _addStorage(self, bank, start, end):
        for n, data in enumerate(self.__storage):
            if data["bank"] == bank:
                if data["start"] == end:
                    data["start"] = start
                    return
                if data["end"] == start:
                    data["end"] = end
                    return
                if data["start"] <= start and data["end"] >= end:
                    return
        self.__storage.append({"bank": bank, "start": start, "end": end})

    def __mergeStorage(self):
        for n in range(len(self.__storage)):
            n_end = self.__storage[n]["end"]
            n_start = self.__storage[n]["start"]
            for m in range(len(self.__storage)):
                if m == n or self.__storage[n]["bank"] != self.__storage[m]["bank"]:
                    continue
                m_end = self.__storage[m]["end"]
                m_start = self.__storage[m]["start"]
                if m_start - 1 <= n_end <= m_end:
                    self.__storage[n]["start"] = min(self.__storage[n]["start"], self.__storage[m]["start"])
                    self.__storage[n]["end"] = self.__storage[m]["end"]
                    self.__storage.pop(m)
                    return True
        return False

    def addStorage(self, extra_storage):
        for data in extra_storage:
            self._addStorage(data["bank"], data["start"], data["end"])
        while self.__mergeStorage():
            pass
        self.__storage.sort(key=lambda n: n["start"])

    def adjustDataStart(self, new_start):
        self.__info["data_addr"] = new_start