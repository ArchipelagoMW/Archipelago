# Copied from the SOTN APWorld under MIT license. Credit goes to fdelduque

import os

ecc_f_lut = bytearray(256)
ecc_b_lut = bytearray(256)
edc_lut = [0] * 256
SYNCHEADER = bytes([0,255,255,255,255,255,255,255,255,255,255,0])
SECTOR_SIZE = 2352

# Initialize ECC and EDC lookup tables
for i in range(256):
    j = (i << 1) ^ (0x11D if i & 0x80 else 0)
    ecc_f_lut[i] = j
    ecc_b_lut[i ^ j] = i
    edc = i

    for j in range(8):
        edc = (edc >> 1) ^ (0xD8018001 if edc & 1 else 0)
    
    edc_lut[i] = edc


def all_zero(data):
    return all(v == 0 for v in data)

def compute_edc_block(sector):
    edc = 0
    for b in sector:
        edc = (edc >> 8) ^ edc_lut[(edc ^ b) & 0xFF]
    
    return edc

def compute_ecc_block(sector, major_count, minor_count, major_mult, minor_inc):
    size = major_count * minor_count
    block = bytearray(major_count * 2)
    
    for major in range(major_count):
        index = (major >> 1) * major_mult + (major & 1)
        ecc_a = 0
        ecc_b = 0

        for _ in range(minor_count):
            temp = sector[index]
            index += minor_inc
            if index >= size:
                index -= size
            
            ecc_a ^= temp
            ecc_b ^= temp
            ecc_a = ecc_f_lut[ecc_a]
        
        ecc_a = ecc_b_lut[ecc_f_lut[ecc_a] ^ ecc_b]
        block[major] = ecc_a
        block[major + major_count] = ecc_a ^ ecc_b
    
    return block

def generate_ecc(sector, zeroaddress):
    if zeroaddress:
        address = sector[12:12+4]
        sector[12:12+4] = [0] * 4

    # Generate P code
    p_code = compute_ecc_block(sector[0xC:], 86, 24,  2, 86)
    sector[0x81C:0x81C+len(p_code)] = p_code

    # Generate Q code
    q_code = compute_ecc_block(sector[0xC:], 52, 43, 86, 88)
    sector[0x8C8:0x8C8+len(q_code)] = q_code

    if zeroaddress:
        sector[12:12+4] = address

def verify_edc(sector):
    mode = sector[0x0F]
    if mode == 0:
        return all_zero(sector[0x10:0x10+0x920])
    elif mode == 1:
        ref = int.from_bytes(sector[0x810:0x810+4], byteorder='little')
        edc = compute_edc_block(sector[:0x810])
        return edc == ref
    elif mode == 2:
        form = sector[0x12] & 0x20
        if not form:
            edc = compute_edc_block(sector[0x10:0x10+0x808])
            ref = int.from_bytes(sector[0x818:0x818+4], byteorder='little')
            return edc == ref
        else:
            ref = int.from_bytes(sector[0x92C:0x92C+4], byteorder='little')
            if ref == 0:
                return True
            edc = compute_edc_block(sector[0x10:0x10+0x91C])
            return edc == ref

class RecalcStats:
    recalc_sectors: int = 0
    edc_blocks_computed: int = 0
    ecc_blocks_generated: int = 0

    def total_sectors(self):
        return self.recalc_sectors
            
class FullRecalcStats(RecalcStats):
    pass

class DiffRecalcStats(RecalcStats):
    identical_sectors: int = 0

    def total_sectors(self):
        return self.identical_sectors + self.recalc_sectors

class ValidateStats:
    ok_sectors: int = 0
    bad_sectors: int = 0
    missing_sync_headers: int = 0

    def total_sectors(self):
        return self.ok_sectors + self.bad_sectors
    
class ErrorRecalculator:
    calculate_form_2_edc: bool

    def __init__(self, calculate_form_2_edc = False):
        """
        :param bool calculate_form_2_edc: Specify whether Mode 2 Form 2 sectors should have their edc calculated or zeroed
        """
        self.calculate_form_2_edc = calculate_form_2_edc

    def ecc_edc_generate(self, sector, stats: RecalcStats):
        sector[0:len(SYNCHEADER)] = SYNCHEADER
        mode = sector[0x0F]
        if mode == 0:
            sector[0x10:0x10+0x920] = [0] * 0x920
        elif mode == 1:
            edc = compute_edc_block(sector[:0x810])
            sector[0x810:0x810+4] = edc.to_bytes(4, byteorder='little')
            sector[0x814:0x814+8] = [0] * 8
            generate_ecc(sector, False)
            
            stats.edc_blocks_computed += 1
            stats.ecc_blocks_generated += 1
        elif mode == 2:
            form = sector[0x12] & 0x20
            if not form:
                # Form 1
                edc = compute_edc_block(sector[0x10:0x10+0x808])
                sector[0x818:0x818+4] = edc.to_bytes(4, byteorder='little')
                generate_ecc(sector, True)
                
                stats.edc_blocks_computed += 1
                stats.ecc_blocks_generated += 1
            else:
                # Form 2
                if self.calculate_form_2_edc:
                    edc = compute_edc_block(sector[0x10:0x10+0x91C])
                    stats.edc_blocks_computed += 1
                else:
                    edc = 0
                
                sector[0x92C:0x92C+4] = edc.to_bytes(4, byteorder='little')
                # Form 2 doesn't generate ecc

                 
    
    def _diff_recalc(self, target_file: os.PathLike, base_file: os.PathLike):
        '''
        Do a smart ECC/EDC recalc based on a diff with a base file

        This function compares the new file with a base file. It skips over every sector that has not changed from the
        base file, and recalculated ECC/EDC only for sectors with changed data.

        It is meant to be an optimization that avoids work over a full recalc. It incurs a penalty in having to compare
        byte-for-byte between 2 files before recalculating ECC/EDC for a sector, but can save a lot of time if the 2 files
        are similar, for exemple if the target file is a patched version of base_file.
        
        It is assumed that the ECC/EDC blocks in the base file are already valid.
        '''
        stats = DiffRecalcStats()    
        target_file_size = os.path.getsize(target_file)
        base_file_size = os.path.getsize(base_file)

        if target_file_size != base_file_size:
            raise "File sizes of base and target files do not match"
        
        if target_file_size % SECTOR_SIZE != 0:
            raise f"Files are not in {SECTOR_SIZE} bytes sectors"

        sector_count = int(target_file_size / SECTOR_SIZE)
        with open(target_file, 'r+b') as ftarget:
            with open(base_file, 'r+b') as fbase:
                for sector_no in range(16, sector_count):
                    start = sector_no*SECTOR_SIZE
                    ftarget.seek(start, os.SEEK_SET)
                    fbase.seek(start, os.SEEK_SET)

                    target_sector = ftarget.read(SECTOR_SIZE)
                    base_sector = fbase.read(SECTOR_SIZE)

                    if base_sector == target_sector:
                        stats.identical_sectors += 1
                    else:
                        sector = bytearray(target_sector)
                        self.ecc_edc_generate(sector, stats)
                        ftarget.seek(start, os.SEEK_SET)
                        ftarget.write(sector)
                        stats.recalc_sectors += 1
        
        return stats
                

    def _full_recalc(self, file: os.PathLike):
        '''
        Recalculate EDC/ECC for all sectors in a file
        '''
        stats = FullRecalcStats()    
        file_size = os.path.getsize(file)

        if file_size % SECTOR_SIZE != 0:
            raise f"File is not in {SECTOR_SIZE} bytes sectors"

        sector_count = int(file_size / SECTOR_SIZE)
        with open(file_size, 'r+b') as f:
            for sector_no in range(16, sector_count):
                start = sector_no*SECTOR_SIZE
                f.seek(start, os.SEEK_SET)

                sector = bytearray(f.read(SECTOR_SIZE))
                self.ecc_edc_generate(sector, stats)
                f.seek(start, os.SEEK_SET)
                f.write(sector)
                stats.recalc_sectors += 1
        
        return stats

    def recalc(self, target_file: os.PathLike, base_file: os.PathLike = None) -> DiffRecalcStats | FullRecalcStats:
        if not base_file:
            return self._full_recalc(target_file)
        else:
            return self._diff_recalc(target_file, base_file)
            
    def validate(self, target_file: os.PathLike) -> ValidateStats:
        with open(target_file, "rb") as f:
            fd = bytearray(f.read())
            sector_count = len(fd) / 2352
            stats = ValidateStats()
            
            for sector_no in range(16, int(sector_count)):
                start = sector_no * 2352
                sector = fd[start:start+2352]
                
                if not sector[0:len(SYNCHEADER)] == SYNCHEADER:
                    stats.missing_sync_headers += 1
                
                if verify_edc(sector):
                    stats.ok_sectors += 1
                else:
                    stats.bad_sectors += 1

            return stats
