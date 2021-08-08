# from https://github.com/DJuttmann/SM3E/blob/master/SM3E/Tools/Compression.cs
import utils.log

class Compressor:
    def __init__(self):
        self.log = utils.log.get('Compressor')

    def _concatBytes(self, b0, b1):
        return b0 + (b1 << 8)

    def _nextByte(self):
        return self.romFile.readByte()

    def decompress(self, romFile, address):
        self.romFile = romFile
        self.romFile.seek(address)

        startAddress = address
        curAddress = address
        output = []

        while curAddress < startAddress + 0x8000:
            curByte = self._nextByte()
            curAddress += 1

            # End of compressed data
            if curByte == 0xFF:
                return (curAddress - startAddress, output)

            command = curByte >> 5
            length = (curByte & 0b11111) + 1

            self.log.debug("@: {} curByte: {} cmd: {} len: {}".format(curAddress-startAddress-1, curByte, bin(command), length))

            while True:
                isLongLength = False

                if command == 0b000:
                    # Copy source bytes
                    for i in range(length):
                        output.append(self._nextByte())
                    curAddress += length
                    self.log.debug("Uncompressed: {}".format(output[-length:]))

                elif command == 0b001:
                    # Repeat one byte <length> times
                    copyByte = self._nextByte()
                    curAddress += 1
                    for i in range(length):
                        output.append(copyByte)
                    self.log.debug("Repeat: {}".format(output[-length:]))

                elif command == 0b010:
                    # Alternate between two bytes <length> times
                    copyByte1 = self._nextByte()
                    copyByte2 = self._nextByte()
                    curAddress += 2
                    for i in range(length):
                      output.append(copyByte1 if i % 2 == 0 else copyByte2)
                    self.log.debug("Word: {}".format(output[-length:]))

                elif command == 0b011:
                    # Sequence of increasing bytes
                    copyByte = self._nextByte()
                    curAddress += 1
                    for i in range(length):
                        output.append(copyByte)
                        copyByte += 1
                    self.log.debug("Increment: {}".format(output[-length:]))

                elif command == 0b100:
                    # Copy from output stream
                    outAddress = self._concatBytes(self._nextByte(), self._nextByte())
                    curAddress += 2
                    for i in range(length):
                        output.append(output[outAddress + i])
                    self.log.debug("Copy: {}".format(output[-length:]))

                elif command == 0b101:
                    # Copy from output stream, flip bits
                    outAddress = self._concatBytes(self._nextByte(), self._nextByte())
                    curAddress += 2
                    for i in range(length):
                        output.append(output[outAddress + i] ^ 0xFF)
                    self.log.debug("CopyXOR: {}".format(output[-length:]))

                elif command == 0b110:
                    # Copy from output stream, relative to current index
                    outAddress = len(output) - self._nextByte()
                    curAddress += 1
                    for i in range(length):
                        output.append(output[outAddress + i])
                    self.log.debug("RelativeCopy: {}".format(output[-length:]))

                elif command == 0b111:
                    # Long length (10 bits) command
                    command = (curByte >> 2) & 0b111;
                    length = ((curByte & 0b11) << 8) + self._nextByte() + 1;
                    curAddress += 1
                    self.log.debug("Long command")

                    if command == 0b111:
                        # Copy output relative to current index, flip bits
                        outAddress = len(output) - self._nextByte()
                        curAddress += 1
                        for i in range(length):
                            output.append(output[outAddress + i] ^ 0xFF)
                        self.log.debug("LongRelativeCopyXOR: {}".format(output[-length:]))
                    else:
                        isLongLength = True;

                if isLongLength == False:
                    break


    def compress(self, inputData):
        # compress the data in input array, return array of compressed bytes
        self.inputData = inputData
        self.output = []

        # brute force all the cases for every byte in the input.
        # For every inputData address, these arrays save the max number of bytes that can be
        # compressed with a single chunk, starting at that address.
        self._computeByteFill(inputData)
        self._computeWordFill(inputData)
        self._computeByteIncrement(inputData)
        self._computeCopy(inputData)

        i = 0
        while i < len(inputData):
            length = max(self.byteFillLengths[i],
                         self.wordFillLengths[i],
                         self.byteIncrementLengths[i],
                         self.copyLengths[i].length)

            self.log.debug("i:{} bf: {} wf: {} bi: {} c: {}".format(i, self.byteFillLengths[i], self.wordFillLengths[i], self.byteIncrementLengths[i], self.copyLengths[i].length))

            if length < 3:
                j = i
                while j < len(inputData) and length < 3:
                    length = max(self.byteFillLengths[j],
                                 self.wordFillLengths[j],
                                 self.byteIncrementLengths[j],
                                 self.copyLengths[j].length)
                    j += 1
                length = j - i if j == len(inputData) else j - i - 1
                self._writeUncompressed(inputData, i, length)

            elif length == self.byteFillLengths[i]:
                length = min(length, 1024)
                self._writeByteFill(inputData[i], length)

            elif length == self.wordFillLengths[i]:
                length = min(length, 1024)
                self._writeWordFill(inputData[i], inputData[i+1], length)

            elif length == self.byteIncrementLengths[i]:
                length = min(length, 1024)
                self._writeByteIncrement(inputData[i], length)

            elif length == self.copyLengths[i].length:
                length = min(length, 1024)
                if i - self.copyLengths[i].address < 0xFF:
                    self._writeNegativeCopy(i, i - self.copyLengths[i].address, length)
                else:
                    self._writeCopy(self.copyLengths[i].address, length)

            i += length

        # end of compressed data marker
        self.output.append(0xFF)

        if len(self.output) > len(inputData):
            print("WARNING !!! len compressed {} > original data {}".format(len(self.output), len(inputData)))
            print("original: {}".format(inputData))
            print("compressed: {}".format(self.output))

        return self.output[:]

    def _writeChunkHeader(self, type, length):
        length -= 1
        if length < 32:
            # regular command
            self.output.append(type << 5 | length)
            self.log.debug("_writeChunkHeader: cmd: {} len: {} value: {}".format(bin(type), length, type << 5 | length))
        else:
            # long command
            self.output.append(0b11100000 | type << 2 | length >> 8)
            self.output.append(length & 0xFF)
            self.log.debug("_writeChunkHeader: long cmd: {} len: {} value: {} {}".format(bin(type), length, 0b11100000 | type << 2 | length >> 8, length & 0xFF))

    def _writeUncompressed(self, inputData, index, length):
        self._writeChunkHeader(0b000, length)
        self.output += inputData[index:index+length]
        self.log.debug("_writeUncompressed: len: {} index: {} data: {}".format(length, index, inputData[index:index+length]))

    def _writeByteFill(self, byte, length):
        self._writeChunkHeader(0b001, length)
        self.output.append(byte)
        self.log.debug("_writeByteFill: len: {} byte: {}: {}".format(length, byte, [byte for i in range(length)]))

    def _writeWordFill(self, b0, b1, length):
        self._writeChunkHeader(0b010, length)
        self.output.append(b0)
        self.output.append(b1)
        self.log.debug("_writeWordFill: len: {} b0: {} b1: {}: {}".format(length, b0, b1, [b0 if i%2==0 else b1 for i in range(length)]))

    def _writeByteIncrement(self, byte, length):
        self._writeChunkHeader(0b011, length)
        self.output.append(byte)
        self.log.debug("_writeByteIncrement: len: {} byte: {}: {}".format(length, byte, [byte+i for i in range(length)]))

    def _writeCopy(self, address, length):
        self._writeChunkHeader(0b100, length)
        self.output.append(address & 0xFF)
        self.output.append(address >> 8)
        self.log.debug("_writeCopy: {}".format(self.output[-3:]))
        self.log.debug("_writeCopy: len: {} address: {}: {}".format(length, address, self.inputData[address:address+length]))

    def _writeNegativeCopy(self, i, address, length):
        self._writeChunkHeader(0b110, length)
        self.output.append(address)
        self.log.debug("_writeNegativeCopy: len: {} address: {}: {}".format(length, address, self.inputData[i-address:i-address+length]))

    def _computeByteFill(self, inputData):
        self.byteFillLengths = []
        carry = 0
        for i in range(len(inputData)):
            if carry == 0:
                value = inputData[i]
                # count how many repeating value we have
                while i + carry < len(inputData) and inputData[i + carry] == value:
                    carry += 1
            self.byteFillLengths.append(carry)
            carry -= 1

    def _computeWordFill(self, inputData):
        self.wordFillLengths = []
        carry = 1
        for i in range(len(inputData)-1):
            if carry == 1:
                value = (inputData[i], inputData[i+1])
                while i + carry < len(inputData) and inputData[i + carry] == value[carry & 1]:
                    carry += 1
            if carry < 4:
                # no compression when replacing [b0, b1, b0] with [cmd, b0, b1]
                self.wordFillLengths.append(2)
            else:
                self.wordFillLengths.append(carry)
            carry -= 1
        # missing last value
        self.wordFillLengths.append(carry)

    def _computeByteIncrement(self, inputData):
        self.byteIncrementLengths = []
        carry = 0
        for i in range(len(inputData)):
            if carry == 0:
                value = inputData[i]
                while i + carry < len(inputData) and inputData[i + carry] == value:
                    carry += 1
                    value += 1
            self.byteIncrementLengths.append(carry)
            carry -= 1

    class _Interval:
        def __init__(self, address, length):
            self.address = address
            self.length = length

        def __repr__(self):
            return "({},{})".format(self.address, self.length)

    def _computeCopy(self, inputData):
        self.copyLengths = []
        limit = 5

        # for each possible value store the positions of the value in the input data
        start = [[] for i in range(len(inputData))]
        for i in range(len(inputData)-1):
            start[inputData[i]].append(i)

        for i, value in enumerate(inputData, start=0):
            maxLength = 0
            maxAddress = -1
            for j, address in enumerate(start[inputData[i]], start=0):
                # for performance reasons limit the number of addresses
                if j >= limit:
                    break
                # only in previous addresses
                if address >= i:
                    break
                length = self._matchSubSequences(address, i, inputData)
                if length > maxLength:
                    maxLength = length
                    maxAddress = address
            self.copyLengths.append(Compressor._Interval(maxAddress, maxLength))

    # Find the max length of two matching sequences starting at a and b in Input array.
    # Make sure that 0 <= a < b, otherwise bad stuff will happen.
    def _matchSubSequences(self, a, b, inputData):
        if a >= b:
            return 0

        i = 0
        length = len(inputData)
        while b+i < length and inputData[a+i] == inputData[b+i]:
            i += 1
        #self.log.debug("_matchSubSequences a: {} b: {} i: {}".format(a,b,i))
        return i
