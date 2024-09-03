using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Sly1AP.Models
{
    public class Moves
    {
        public uint SlyMoves { get; set; } = 0;
        public uint DiveAttack { get; set; } = 2;
        public uint Roll { get; set; } = 4;
        public uint Slow { get; set; } = 8;
        public uint Safety { get; set; } = 256;
        public uint Invisibility { get; set; } = 65536;
        public uint CoinMagnet { get; set; } = 32;
        public uint Mine { get; set; } = 64;
        public uint Fast { get; set; } = 128;
        public uint Decoy { get; set; } = 512;
        public uint Hacking { get; set; } = 2048;
        public uint RaleighBlueprint { get; set; } = 0x20000000;
        public uint MuggshotBlueprint { get; set; } = 0x40000000;
        public uint MzRubyBlueprint { get; set; } = 0x80000000;
        public uint PandaKingBlueprint { get; set; } = 0xD0000000;
    }
}
