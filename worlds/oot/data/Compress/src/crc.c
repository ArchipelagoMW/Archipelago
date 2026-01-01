/* snesrc - SNES Recompiler
 *
 * Copyright notice for this file:
 *  Copyright (C) 2005 Parasyte
 *
 * Based on uCON64's N64 checksum algorithm by Andreas Sterbenz
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
 */


#include <stdio.h>
#include <stdlib.h>

#define ROL(i, b) (((i) << (b)) | ((i) >> (32 - (b))))
#define BYTES2LONG(b) ( (b)[0] << 24 | \
                        (b)[1] << 16 | \
                        (b)[2] <<  8 | \
                        (b)[3] )

#define N64_HEADER_SIZE  0x40
#define N64_BC_SIZE      (0x1000 - N64_HEADER_SIZE)

#define N64_CRC1         0x10
#define N64_CRC2         0x14

#define CHECKSUM_START   0x00001000
#define CHECKSUM_LENGTH  0x00100000
#define CHECKSUM_CIC6102 0xF8CA4DDC
#define CHECKSUM_CIC6103 0xA3886759
#define CHECKSUM_CIC6105 0xDF26F436
#define CHECKSUM_CIC6106 0x1FEA617A


unsigned int crc_table[256];

void gen_table() 
{
    uint32_t crc, poly;
    int32_t  i, j;
    
    poly = 0xEDB88320;
    for (i = 0; i < 256; i++) {
        crc = i;
        for (j = 8; j > 0; j--) {
            if (crc & 1) crc = (crc >> 1) ^ poly;
            else crc >>= 1;
        }
        crc_table[i] = crc;
    }
}

unsigned int crc32(unsigned char *data, int len) 
{
    uint32_t crc, i;

    crc = ~0;
    for (i = 0; i < len; i++)
        crc = (crc >> 8) ^ crc_table[(crc ^ data[i]) & 0xFF];

    return ~crc;
}


int N64GetCIC(unsigned char *data) 
{
    switch (crc32(&data[N64_HEADER_SIZE], N64_BC_SIZE)) {
        case 0x6170A4A1: return 6101;
        case 0x90BB6CB5: return 6102;
        case 0x0B050EE0: return 6103;
        case 0x98BC2C86: return 6105;
        case 0xACC8580A: return 6106;
    }

    return 0;
}

int N64CalcCRC(unsigned int *crc, unsigned char *data) 
{
    int32_t bootcode, i;
    uint32_t seed, r, d;
    uint32_t t1, t2, t3;
    uint32_t t4, t5, t6;

    switch ((bootcode = N64GetCIC(data))) {
        case 6101:
        case 6102:
            seed = CHECKSUM_CIC6102;
            break;
        case 6103:
            seed = CHECKSUM_CIC6103;
            break;
        case 6105:
            seed = CHECKSUM_CIC6105;
            break;
        case 6106:
            seed = CHECKSUM_CIC6106;
            break;
        default:
            return 0;
    }

    t1 = t2 = t3 = t4 = t5 = t6 = seed;

    i = CHECKSUM_START;
    while (i < (CHECKSUM_START + CHECKSUM_LENGTH)) {
        d = BYTES2LONG(&data[i]);
        if ((t6 + d) < t6) t4++;
        t6 += d;
        t3 ^= d;
        r = ROL(d, (d & 0x1F));
        t5 += r;
        if (t2 > d) t2 ^= r;
        else t2 ^= t6 ^ d;

        if (bootcode == 6105) t1 += BYTES2LONG(&data[N64_HEADER_SIZE + 0x0710 + (i & 0xFF)]) ^ d;
        else t1 += t5 ^ d;

        i += 4;
    }
    if (bootcode == 6103) {
        crc[0] = (t6 ^ t4) + t3;
        crc[1] = (t5 ^ t2) + t1;
    }
    else if (bootcode == 6106) {
        crc[0] = (t6 * t4) + t3;
        crc[1] = (t5 * t2) + t1;
    }
    else {
        crc[0] = t6 ^ t4 ^ t3;
        crc[1] = t5 ^ t2 ^ t1;
    }

    return 1;
}

void fix_crc (uint8_t* buffer)
{
    uint8_t CRC1[4];
    uint8_t CRC2[4];
    uint32_t crc[2];
    uint32_t i;
    
    gen_table();

    /* If the CRC calc was successful, do stuff */
    if(N64CalcCRC(crc, buffer))
    {
        for(i = 0; i < 4; i++)
        {
            CRC1[i] = (crc[0] >> (24-8*i))&0xFF;
            CRC2[i] = (crc[1] >> (24-8*i))&0xFF;
        }
        
        /* If the CRC1 changed, update it */
        if(crc[0] != BYTES2LONG(&buffer[N64_CRC1]))
            memcpy(buffer + N64_CRC1, CRC1, 4);
        
        /* If the CRC2 changed, update it */
        if (crc[1] != BYTES2LONG(&buffer[N64_CRC2]))
            memcpy(buffer + N64_CRC2, CRC2, 4);
    }
}
