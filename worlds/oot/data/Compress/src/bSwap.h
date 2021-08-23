#ifndef BSWAP_H
#define BSWAP_H

#include <stdint.h>

uint32_t bSwap32(uint32_t a)
{
    return( (a & 0x000000FF) << 24 |
            (a & 0x0000FF00) <<  8 |
            (a & 0x00FF0000) >>  8 |
            (a & 0xFF000000) >> 24 );
}

uint16_t bSwap16(uint16_t a)
{
    return( (a & 0x00FF) << 8 |
            (a & 0xFF00) >> 8 );
}

#endif
