using System.Text.Json.Serialization;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Archipelago.Core.Models;
using Newtonsoft.Json;
using System.Reflection;
using System.IO;
using Archipelago.Core.Util;
using Sly1AP.Models;
using Archipelago.Core;

namespace Sly1AP
{
    class Helpers
    {
        public static int StealthyApproachItems { get; set; }
        public static int IntoTheMachineItems { get; set; }
        public static int HighClassHeistItems { get; set; }
        public static int FireDownBelowItems { get; set; }
        public static int CunningDisguiseItems { get; set; }
        public static int GunboatGraveyardItems { get; set; }
        public static int RockyStartItems { get; set; }
        public static int BoneyardCasinoItems { get; set; }
        public static int BackAlleyHeistItems { get; set; }
        public static int StraightToTheTopItems { get; set; }
        public static int TwoToTangoItems { get; set; }
        public static int DreadSwampPathItems { get; set; }
        public static int LairOfTheBeastItems { get; set; }
        public static int GraveUndertakingItems { get; set; }
        public static int DescentIntoDangerItems { get; set; }
        public static int PerilousAscentItems { get; set; }
        public static int FlamingTempleItems { get; set; }
        public static int UnseenFoeItems { get; set; }
        public static int DuelByTheDragonItems { get; set; }
        public static List<Location> GetLocations()
        {
            var json = OpenEmbeddedResource("Sly1AP.Resources.Locations.json");
            var list = JsonConvert.DeserializeObject<List<Location>>(json);
            return list;
        }

        public class Level
        {
            public string Name { get; set; }
            public string LevelType { get; set; }
            public ulong Address { get; set; }
            public int BottleId { get; set; }
            public int ItemBottles { get; set; }
            public int MaxBottles { get; set; }
            public ulong NamePointer { get; set; }

            public Level(string name, string levelType, ulong address, int bottleId, int itemBottles, int maxBottles, ulong namePointer)
            {
                Name = name;
                LevelType = levelType;
                Address = address;
                BottleId = bottleId;
                ItemBottles = itemBottles;
                MaxBottles = maxBottles;
                NamePointer = namePointer;
            }
        }


        public static List<Level> Levels = new()
            {
                new Level("Stealthy Approach", "Level", 0x2027C67C, 10020400, StealthyApproachItems, Clues.StealthyApproachMax, 0x20247B98),
                new Level("Into the Machine", "Level", 0x2027C7E4, 10020420, IntoTheMachineItems, Clues.IntoTheMachineMax, 0x20247C1C),
                new Level("High Class Heist", "Level", 0x2027C76C, 10020450, HighClassHeistItems, Clues.HighClassHeistMax, 0x20247BF0),
                new Level("Fire Down Below", "Level", 0x2027C8D4, 10020480, FireDownBelowItems, Clues.FireDownBelowMax, 0x20247C74),
                new Level("Cunning Disguise", "Level", 0x2027C85C, 10020510, CunningDisguiseItems, Clues.CunningDisguiseMax, 0x20247C48),
                new Level("Gunboat Graveyard", "Level", 0x2027C9C4, 10020540, GunboatGraveyardItems, Clues.GunboatGraveyardMax, 0x20247CCC),
                new Level("Rocky Start", "Level", 0x2027CAC8, 10020560, RockyStartItems, Clues.RockyStartMax, 0x20247D24),
                new Level("Boneyard Casino", "Level", 0x2027CBB8, 10020600, BoneyardCasinoItems, Clues.BoneyardCasinoMax, 0x20247D7C),
                new Level("Back Alley Heist", "Level", 0x2027CE10, 10020710, BackAlleyHeistItems, Clues.BackAlleyHeistMax, 0x20247E58),
                new Level("Straight to the Top", "Level", 0x2027CD98, 10020640, StraightToTheTopItems, Clues.StraightToTheTopMax, 0x20247E2C),
                new Level("Two to Tango", "Level", 0x2027CD20, 10020680, TwoToTangoItems, Clues.TwoToTangoMax, 0x20247E00),
                new Level("Dread Swamp Path", "Level", 0x2027CF14, 10020740, DreadSwampPathItems, Clues.DreadSwampPathMax, 0x20247EB0),
                new Level("Lair of the Beast", "Level", 0x2027D004, 10020760, LairOfTheBeastItems, Clues.LairOfTheBeastMax, 0x20247F08),
                new Level("Grave Undertaking", "Level", 0x2027D07C, 10020790, GraveUndertakingItems, Clues.GraveUndertakingMax, 0x20247F34),
                new Level("Descent into Danger", "Level", 0x2027D16C, 10020830, DescentIntoDangerItems, Clues.DescentIntoDangerMax, 0x20247F8C),
                new Level("Perilous Ascent", "Level", 0x2027D360, 10020870, PerilousAscentItems, Clues.PerilousAscentMax, 0x2024803C),
                new Level("Flaming Temple of Flame", "Level", 0x2027D450, 10020930, FlamingTempleItems, Clues.FlamingTempleMax, 0x20248094),
                new Level("Unseen Foe", "Level", 0x2027D4C8, 10020900, UnseenFoeItems, Clues.UnseenFoeMax, 0x202480C0),
                new Level("Duel by the Dragon", "Level", 0x2027D630, 10020955, DuelByTheDragonItems, Clues.DuelByTheDragonMax, 0x20248144),
                new Level("Tide of Terror", "Hub", 0x2027C67C, 0, 0, 0, 0x20274434),
                new Level("Sunset Snake Eyes", "Hub", 0x2027CAC8, 0, 0, 0, 0x20274438),
                new Level("Vicious Voodoo", "Hub", 0x2027CF14, 0, 0, 0, 0x2027443C),
                new Level("Fire in the Sky", "Hub", 0x2027D360, 0, 0, 0, 0x20274440)
            };

        public static List<Level> GetUpdatedLevels()
        {
            var updatedLevels = new List<Level>
            {
                new Level("Stealthy Approach", "Level", 0x2027C67C, 10020400, StealthyApproachItems, Clues.StealthyApproachMax, 0x20247B98),
                new Level("Into the Machine", "Level", 0x2027C7E4, 10020420, IntoTheMachineItems, Clues.IntoTheMachineMax, 0x20247C1C),
                new Level("High Class Heist", "Level", 0x2027C76C, 10020450, HighClassHeistItems, Clues.HighClassHeistMax, 0x20247BF0),
                new Level("Fire Down Below", "Level", 0x2027C8D4, 10020480, FireDownBelowItems, Clues.FireDownBelowMax, 0x20247C74),
                new Level("Cunning Disguise", "Level", 0x2027C85C, 10020510, CunningDisguiseItems, Clues.CunningDisguiseMax, 0x20247C48),
                new Level("Gunboat Graveyard", "Level", 0x2027C9C4, 10020540, GunboatGraveyardItems, Clues.GunboatGraveyardMax, 0x20247CCC),
                new Level("Rocky Start", "Level", 0x2027CAC8, 10020560, RockyStartItems, Clues.RockyStartMax, 0x20247D24),
                new Level("Boneyard Casino", "Level", 0x2027CBB8, 10020600, BoneyardCasinoItems, Clues.BoneyardCasinoMax, 0x20247D7C),
                new Level("Back Alley Heist", "Level", 0x2027CE10, 10020710, BackAlleyHeistItems, Clues.BackAlleyHeistMax, 0x20247E58),
                new Level("Straight to the Top", "Level", 0x2027CD98, 10020640, StraightToTheTopItems, Clues.StraightToTheTopMax, 0x20247E2C),
                new Level("Two to Tango", "Level", 0x2027CD20, 10020680, TwoToTangoItems, Clues.TwoToTangoMax, 0x20247E00),
                new Level("Dread Swamp Path", "Level", 0x2027CF14, 10020740, DreadSwampPathItems, Clues.DreadSwampPathMax, 0x20247EB0),
                new Level("Lair of the Beast", "Level", 0x2027D004, 10020760, LairOfTheBeastItems, Clues.LairOfTheBeastMax, 0x20247F08),
                new Level("Grave Undertaking", "Level", 0x2027D07C, 10020790, GraveUndertakingItems, Clues.GraveUndertakingMax, 0x20247F34),
                new Level("Descent into Danger", "Level", 0x2027D16C, 10020830, DescentIntoDangerItems, Clues.DescentIntoDangerMax, 0x20247F8C),
                new Level("Perilous Ascent", "Level", 0x2027D360, 10020870, PerilousAscentItems, Clues.PerilousAscentMax, 0x2024803C),
                new Level("Flaming Temple of Flame", "Level", 0x2027D450, 10020930, FlamingTempleItems, Clues.FlamingTempleMax, 0x20248094),
                new Level("Unseen Foe", "Level", 0x2027D4C8, 10020900, UnseenFoeItems, Clues.UnseenFoeMax, 0x202480C0),
                new Level("Duel by the Dragon", "Level", 0x2027D630, 10020955, DuelByTheDragonItems, Clues.DuelByTheDragonMax, 0x20248144),
                new Level("Tide of Terror", "Hub", 0x2027C67C, 0, 0, 0, 0x20274434),
                new Level("Sunset Snake Eyes", "Hub", 0x2027CAC8, 0, 0, 0, 0x20274438),
                new Level("Vicious Voodoo", "Hub", 0x2027CF14, 0, 0, 0, 0x2027443C),
                new Level("Fire in the Sky", "Hub", 0x2027D360, 0, 0, 0, 0x20274440)
            };
            return updatedLevels;
        }

        public static string OpenEmbeddedResource(string resourceName)
        {
            var assembly = Assembly.GetExecutingAssembly();
            using (Stream stream = assembly.GetManifestResourceStream(resourceName))
            using (StreamReader reader = new StreamReader(stream))
            {
                string jsonFile = reader.ReadToEnd();
                return jsonFile;
            }
        }

        public static string[] bentley = { "Sly1AP.Bentley.Bentley1.wav", "Sly1AP.Bentley.Bentley2.wav", "Sly1AP.Bentley.Bentley3.wav", "Sly1AP.Bentley.Bentley4.wav",
                                               "Sly1AP.Bentley.Bentley5.wav", "Sly1AP.Bentley.Bentley6.wav", "Sly1AP.Bentley.Bentley7.wav", "Sly1AP.Bentley.Bentley8.wav",
                                               "Sly1AP.Bentley.Bentley9.wav", "Sly1AP.Bentley.Bentley10.wav", "Sly1AP.Bentley.Bentley11.wav", "Sly1AP.Bentley.Bentley12.wav",
                                               "Sly1AP.Bentley.Bentley13.wav", "Sly1AP.Bentley.Bentley14.wav", "Sly1AP.Bentley.Bentley15.wav"};
        //public List<string> BentleyLines = new List<string>(bentley);

        public static void SendBottles(List<Level> Levels, ArchipelagoClient Client)
        {
            ulong CurrentLevel = Memory.ReadUInt(0x202623C8) + 0x20000000;
            Level LevelObj = Levels.FirstOrDefault(x => x.Address == CurrentLevel);
            CurrentLevel += 0x68;
            if ((Memory.ReadByte(0x202623C4) == 0 || Memory.ReadByte(0x26202023C4) == 5) || LevelObj == null)
            {
                return;
            }
            int CurrentBit = 0;
            int TotalBottles = 0;
            for (int i = 0; i < LevelObj.MaxBottles; i++)
            {
                if (Memory.ReadBit(CurrentLevel, CurrentBit))
                {
                    TotalBottles++;
                    {
                        Location BottleLoc = new Location
                        {
                            Name = LevelObj.Name + " Bottle #" + TotalBottles,
                            Id = LevelObj.BottleId + TotalBottles - 1,
                        };
                        if (BottleLoc.Id < LevelObj.BottleId)
                        {
                            return;
                        }
                        if (!Client.GameState.CompletedLocations.Any(l => l.Id == BottleLoc.Id))
                        {
                            Client.SendLocation(BottleLoc);
                        }
                    }
                }
                CurrentBit++;
                if (CurrentBit == 8)
                {
                    CurrentBit = 0;
                    CurrentLevel++;
                }
            }
        }
    }
}
