#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include "crc.c"
#include "bSwap.h"

#define UINTSIZE 0x01000000
#define COMPSIZE 0x02000000
#define DCMPSIZE 0x04000000

/* Structs */
typedef struct
{
    uint32_t startV;   /* Start Virtual Address  */
    uint32_t endV;     /* End Virtual Address    */
    uint32_t startP;   /* Start Physical Address */
    uint32_t endP;     /* End Phycical Address   */
}
table_t;

/* Functions */
void decompress(uint8_t*, uint8_t*, int32_t);
table_t getTabEnt(uint32_t);
void setTabEnt(uint32_t, table_t);
void loadROM(char*);
int32_t findTable();

/* Globals */
uint8_t* inROM;
uint8_t* outROM;
uint32_t* inTable;
uint32_t* outTable;

int main(int argc, char** argv)
{
    FILE* outFile;
    int32_t tabStart, tabSize, tabCount;
    int32_t size, i;
    table_t tab, tempTab;
    char* name;

    /* Check arguments */
    if(argc < 2 || argc > 3)
    {
        fprintf(stderr, "Usage: %s [Input ROM] <Output ROM>\n", argv[0]);
        exit(1);
    }

    /* If no output file was specified, make one */
    /* Add "-decomp.z64" to the end of the input file */
    if(argc != 3)
    {
        size = strlen(argv[1]);
        name = malloc(size + 7);
        strcpy(name, argv[1]);
        for(i = size; i >= 0; i--)
        {
            if(name[i] == '.')
            {
                name[i] = '\0';
                break;
            }
        }
        strcat(name, "-decomp.z64");
    }
    
    else
        name = argv[2];

    inROM = malloc(DCMPSIZE);
    outROM = malloc(DCMPSIZE);

    /* Load the ROM into inROM and outROM */
    loadROM(argv[1]);

    /* Find table offsets */
    tabStart = findTable();
    inTable = (uint32_t*)(inROM + tabStart);
    outTable = (uint32_t*)(outROM + tabStart);
    tab = getTabEnt(2);
    tabSize = tab.endV - tab.startV;
    tabCount = tabSize / 16;

    /* Set everything past the table in outROM to 0 */
    memset((uint8_t*)(outROM) + tab.endV, 0, DCMPSIZE - tab.endV);

    for(i = 3; i < tabCount; i++)
    {
        tempTab = getTabEnt(i);
        size = tempTab.endV - tempTab.startV;

        /* dmaTable will have 0xFFFFFFFF if file doesn't exist */
        if(tempTab.startP >= DCMPSIZE || tempTab.endP == 0xFFFFFFFF)
            continue;

        /* Copy if not compressed, decompress otherwise */
        if(tempTab.endP == 0x00000000)
            memcpy((void*)outROM + tempTab.startV, (void*)inROM + tempTab.startP, size);
        else
            decompress((void*)inROM + tempTab.startP, (void*)outROM + tempTab.startV, size);

        /* Clean up outROM's table */
        tempTab.startP = tempTab.startV;
        tempTab.endP = 0x00000000;
        setTabEnt(i, tempTab);
    }

    /* Fix the CRC */ 
    fix_crc(outROM);
    
    /* Write the new ROM */
    outFile = fopen(name, "wb");
    fwrite(outROM, sizeof(uint32_t), UINTSIZE, outFile);
    fclose(outFile);
    free(outROM);
    free(inROM);

    if(argc != 3)
        free(name);

    return(0);
}

int32_t findTable()
{
    int32_t i, temp;
    uint32_t* tempROM;

    tempROM = (uint32_t*)inROM;

    /* Start at the end of the makerom (0x10600000) */
    /* Look for dma entry for the makeom */
    /* Should work for all Zelda64 titles */
    for(i = 1048; i+4 < UINTSIZE; i += 4)
    {
        if(tempROM[i] == 0x00000000)
            if(tempROM[i+1] == 0x60100000)
                return(i * 4);
    }

    fprintf(stderr, "Error: Couldn't find table\n");
    exit(1);
}

void loadROM(char* name)
{
    uint32_t size, i;
    uint16_t* tempROM;
    FILE* romFile;
    
    /* Open file, make sure it exists */
    romFile = fopen(name, "rb");
    if(romFile == NULL)
    {
        perror(name);
        exit(1);
    }
    /* Find size of file */
    fseek(romFile, 0, SEEK_END);
    size = ftell(romFile);
    fseek(romFile, 0, SEEK_SET);

    /* If it's not the right size, exit */
    if(size != COMPSIZE)
    {
        fprintf(stderr, "Error, %s is not the correct size", name);
        exit(1);
    }

    /* Read to inROM, close romFile, and copy to outROM */
    fread(inROM, sizeof(char), size, romFile);
    tempROM = (uint16_t*)inROM;
    fclose(romFile);

    /* bSwap16 if needed */
    if (inROM[0] == 0x37)
        for (i = 0; i < UINTSIZE; i++)
            tempROM[i] = bSwap16(tempROM[i]);

    memcpy(outROM, inROM, size);
}

table_t getTabEnt(uint32_t i)
{
    table_t tab;

    /* First 32 bytes are VROM start address, next 32 are VROM end address */
    /* Next 32 bytes are Physical start address, last 32 are Physical end address */
    tab.startV = bSwap32(inTable[i*4]    );
    tab.endV   = bSwap32(inTable[(i*4)+1]);
    tab.startP = bSwap32(inTable[(i*4)+2]);
    tab.endP   = bSwap32(inTable[(i*4)+3]);

    return(tab);
}

void setTabEnt(uint32_t i, table_t tab)
{
    /* First 32 bytes are VROM start address, next 32 are VROM end address */
    /* Next 32 bytes are Physical start address, last 32 are Physical end address */
    outTable[i*4]     = bSwap32(tab.startV);
    outTable[(i*4)+1] = bSwap32(tab.endV);
    outTable[(i*4)+2] = bSwap32(tab.startP);
    outTable[(i*4)+3] = bSwap32(tab.endP);
}

void decompress(uint8_t* source, uint8_t* decomp, int32_t decompSize)
{
    uint32_t srcPlace = 0, dstPlace = 0;
    uint32_t i, dist, copyPlace, numBytes;
    uint8_t codeByte, byte1, byte2;
    uint8_t bitCount = 0;

    source += 0x10;
    while(dstPlace < decompSize)
    {
        /* If there are no more bits to test, get a new byte */
        if(!bitCount)
        {
            codeByte = source[srcPlace++];
            bitCount = 8;
        }

        /* If bit 7 is a 1, just copy 1 byte from source to destination */
        /* Else do some decoding */
        if(codeByte & 0x80)
        {
            decomp[dstPlace++] = source[srcPlace++];
        }
        else
        {
            /* Get 2 bytes from source */
            byte1 = source[srcPlace++];
            byte2 = source[srcPlace++];

            /* Calculate distance to move in destination */
            /* And the number of bytes to copy */
            dist = ((byte1 & 0xF) << 8) | byte2;
            copyPlace = dstPlace - (dist + 1);
            numBytes = byte1 >> 4;

            /* Do more calculations on the number of bytes to copy */
            if(!numBytes)
                numBytes = source[srcPlace++] + 0x12;
            else
                numBytes += 2;

            /* Copy data from a previous point in destination */
            /* to current point in destination */
            for(i = 0; i < numBytes; i++)
                decomp[dstPlace++] = decomp[copyPlace++];
        }

        /* Set up for the next read cycle */
        codeByte = codeByte << 1;
        bitCount--;
    }
}
