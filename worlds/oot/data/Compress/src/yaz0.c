#include <stdlib.h>
#include <stdint.h>
#include <string.h>

uint32_t RabinKarp(uint8_t*, int, int, uint32_t*);
uint32_t findBest(uint8_t*, int, int, uint32_t*, uint32_t*, uint32_t*, uint8_t*);
int      yaz0_internal(uint8_t*, int, uint8_t*);
void     yaz0_encode(uint8_t*, int, uint8_t*, int*);

uint32_t RabinKarp(uint8_t* src, int srcSize, int srcPos, uint32_t* matchPos)
{
    int startPos, smp, i;
    uint32_t hash, curHash, curSize;
    uint32_t bestSize, bestPos;

    smp = srcSize - srcPos;
    startPos = srcPos - 0x1000;
    bestPos = bestSize = 0;

    /* If available size is too small, return */
    if(smp < 3)
        return(0);

    /* If available size is too big, reduce it */
    if(smp > 0x111)
        smp = 0x111;

    /* If start position is negative, make it 0 */
    if(startPos < 0)
        startPos = 0;

    /* Generate "hash" by converting to an int */
    hash = bSwap32(*(int*)(src + srcPos));
    hash = hash >> 8;
    curHash = bSwap32(*(int*)(src + startPos));
    curHash = curHash >> 8;

    /* Search through data */
    for(i = startPos; i < srcPos; i++)
    {
        /* If 3 bytes match, check for more */
        if(curHash == hash)
        {
            for(curSize = 3; curSize < smp; curSize++)
                if(src[i + curSize] != src[srcPos + curSize])
                    break;

            /* Uodate best if needed */
            if(curSize > bestSize)
            {
                bestSize = curSize;
                bestPos = i;
                if(bestSize == 0x111)
                    break;
            }
        }

        /* Scoot over 1 byte */
        curHash = (curHash << 8 | src[i + 3]) & 0x00FFFFFF;
    }
    
    /* Set match position, return the size of the match */
    *matchPos = bestPos;
    return(bestSize);
}

uint32_t findBest(uint8_t* src, int srcSize, int srcPos, uint32_t* matchPos, uint32_t* pMatch, uint32_t* pSize, uint8_t* pFlag)
{
    int rv;

    /* Check to see if this location was found by a look-ahead */
    if(*pFlag == 1)
    {
        *pFlag = 0;
        return(*pSize);
    }

    /* Find best match */
    *pFlag = 0;
    rv = RabinKarp(src, srcSize, srcPos, matchPos);

    /* Look-ahead */
    if(rv >= 3)
    {
        /* Find best match if current one were to be a 1 byte copy */
        *pSize = RabinKarp(src, srcSize, srcPos+1, pMatch);
        if(*pSize >= rv+2)
        {
            rv = *pFlag = 1;
            *matchPos = *pMatch;
        }
    }

    return(rv);
}

int yaz0_internal(uint8_t* src, int srcSize, uint8_t* dst)
{
    int dstPos, srcPos, codeBytePos;
    uint32_t numBytes, matchPos, dist, pMatch, pSize;
    uint8_t codeByte, bitmask, pFlag;

    srcPos = codeBytePos = 0;
    dstPos = codeBytePos + 1;
    bitmask = 0x80;
    codeByte = pFlag = 0;

    /* Go through all of src */
    while(srcPos < srcSize)
    {
        /* Try to find matching bytes for compressing */
        numBytes = findBest(src, srcSize, srcPos, &matchPos, &pMatch, &pSize, &pFlag);

        /* Single byte copy */
        if(numBytes < 3)
        {
            dst[dstPos++] = src[srcPos++];
            codeByte |= bitmask; 
        }

        /* Three byte encoding */
        else if (numBytes > 0x11)
        {
            dist = srcPos - matchPos - 1;

            /* Copy over 0R RR */
            dst[dstPos++] = dist >> 8;
            dst[dstPos++] = dist & 0xFF;

            /* Reduce N if needed, copy over NN */
            if(numBytes > 0x111)
                numBytes = 0x111;
            dst[dstPos++] = (numBytes - 0x12) & 0xFF;

            srcPos += numBytes;
        }

        /* Two byte encoding */
        else
        {
            dist = srcPos - matchPos - 1;
            
            /* Copy over NR RR */
            dst[dstPos++] = ((numBytes - 2) << 4) | (dist >> 8);
            dst[dstPos++] = dist & 0xFF;
            
            srcPos += numBytes;
        }

        /* Move bitmask to next byte */
        bitmask = bitmask >> 1;

        /* If all 8 bytes were used, write and move to the next one */
        if(bitmask == 0)
        {
            dst[codeBytePos] = codeByte;
            codeBytePos = dstPos;
            if(srcPos < srcSize)
                dstPos++;
            codeByte = 0;
            bitmask = 0x80;
        }
    }

    /* Copy over last byte if it hasn't already */
    if(bitmask != 0)
        dst[codeBytePos] = codeByte;

    /* Return size of dst */
    return(dstPos);
}

void yaz0_encode(uint8_t* src, int srcSize, uint8_t* dst, int* dstSize)
{
    int temp;

    /* Write Yaz0 header */
    temp = bSwap32(srcSize);
    memcpy(dst, "Yaz0", 4);
    memcpy(dst + 4, &temp, 4);

    /* Encode, adjust dstSize */
    temp = yaz0_internal(src, srcSize, dst + 16);
    *dstSize = (temp + 31) & -16;
    return;
}
