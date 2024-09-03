using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Sly1AP.Models
{
    internal class ArchipelagoOptions
    {
        public int StartingEpisode { get; set; } = 1;
        public bool IncludeHourglasses { get; set; } = true;
        public bool AlwaysSpawnHourglasses { get; set; } = false;
    }
}
