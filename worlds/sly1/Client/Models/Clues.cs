using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Archipelago.Core.Util;

namespace Sly1AP.Models
{
    internal class Clues
    {
        public static int StealthyApproachBottles { get; set; } = 0;
        public static int StealthyApproachMax { get; set; } = 20;
        public static int IntoTheMachineBottles { get; set; } = 0;
        public static int IntoTheMachineMax { get; set; } = 30;
        public static int HighClassHeistBottles { get; set; } = 0;
        public static int HighClassHeistMax { get; set; } = 30;
        public static int FireDownBelowBottles { get; set; } = 0;
        public static int FireDownBelowMax { get; set; } = 30;
        public static int CunningDisguiseBottles { get; set; } = 0;
        public static int CunningDisguiseMax { get; set; } = 30;
        public static int GunboatGraveyardBottles { get; set; } = 0;
        public static int GunboatGraveyardMax { get; set; } = 20;
        public static int RockyStartBottles { get; set; } = 0;
        public static int RockyStartMax { get; set; } = 40;
        public static int BoneyardCasinoBottles { get; set; } = 0;
        public static int BoneyardCasinoMax { get; set; } = 40;
        public static int StraightToTheTopBottles { get; set; } = 0;
        public static int StraightToTheTopMax { get; set; } = 40;
        public static int TwoToTangoBottles { get; set; } = 0;
        public static int TwoToTangoMax { get; set; } = 30;
        public static int BackAlleyHeistBottles { get; set; } = 0;
        public static int BackAlleyHeistMax { get; set; } = 30;
        public static int DreadSwampPathBottles { get; set; } = 0;
        public static int DreadSwampPathMax { get; set; } = 20;
        public static int LairOfTheBeastBottles { get; set; } = 0;
        public static int LairOfTheBeastMax { get; set; } = 30;
        public static int GraveUndertakingBottles { get; set; } = 0;
        public static int GraveUndertakingMax { get; set; } = 40;
        public static int DescentIntoDangerBottles { get; set; } = 0;
        public static int DescentIntoDangerMax { get; set; } = 40;
        public static int PerilousAscentBottles { get; set; } = 0;
        public static int PerilousAscentMax { get; set; } = 30;
        public static int FlamingTempleBottles { get; set; } = 0;
        public static int FlamingTempleMax { get; set; } = 25;
        public static int UnseenFoeBottles { get; set; } = 0;
        public static int UnseenFoeMax { get; set; } = 30;
        public static int DuelByTheDragonBottles { get; set; } = 0;
        public static int DuelByTheDragonMax { get; set; } = 40;
        public static void UpdateBottles(long Id, int Bundles)
        {
            //Increment the count. Then, multiply it by the bundle size. If it exceeds the maximum for the level, reduce it to max. Then write it to the memory address.
            if (Id == 10020030)
            {
                Helpers.StealthyApproachItems++;
                StealthyApproachBottles = Helpers.StealthyApproachItems * Bundles;
                if (StealthyApproachBottles > StealthyApproachMax)
                {
                    StealthyApproachBottles = StealthyApproachMax;
                }
            }
            if (Id == 10020031)
            {
                Helpers.IntoTheMachineItems++;
                IntoTheMachineBottles = Helpers.IntoTheMachineItems * Bundles;
                if (IntoTheMachineBottles > IntoTheMachineMax)
                {
                    IntoTheMachineBottles = IntoTheMachineMax;
                }
            }
            if (Id == 10020032)
            {
                Helpers.HighClassHeistItems++;
                HighClassHeistBottles = Helpers.HighClassHeistItems * Bundles;
                if (HighClassHeistBottles > HighClassHeistMax)
                {
                    HighClassHeistBottles = HighClassHeistMax;
                }
            }
            if (Id == 10020033)
            {
                Helpers.FireDownBelowItems++;
                FireDownBelowBottles = Helpers.FireDownBelowItems * Bundles;
                if (FireDownBelowBottles > FireDownBelowMax)
                {
                    FireDownBelowBottles = FireDownBelowMax;
                }
            }
            if (Id == 10020034)
            {
                Helpers.CunningDisguiseItems++;
                CunningDisguiseBottles = Helpers.CunningDisguiseItems * Bundles;
                if (CunningDisguiseBottles > CunningDisguiseMax)
                {
                    CunningDisguiseBottles = CunningDisguiseMax;
                }
            }
            if (Id == 10020035)
            {
                Helpers.GunboatGraveyardItems++;
                GunboatGraveyardBottles = Helpers.GunboatGraveyardItems * Bundles;
                if (GunboatGraveyardBottles > GunboatGraveyardMax)
                {
                    GunboatGraveyardBottles = GunboatGraveyardMax;
                }
            }
            if (Id == 10020036)
            {
                Helpers.RockyStartItems++;
                RockyStartBottles = Helpers.RockyStartItems * Bundles;
                if (RockyStartBottles > RockyStartMax)
                {
                    RockyStartBottles = RockyStartMax;
                }
            }
            if (Id == 10020037)
            {
                Helpers.BoneyardCasinoItems++;
                BoneyardCasinoBottles = Helpers.BoneyardCasinoItems * Bundles;
                if (BoneyardCasinoBottles > BoneyardCasinoMax)
                {
                    BoneyardCasinoBottles = BoneyardCasinoMax;
                }
            }
            if (Id == 10020038)
            {
                Helpers.StraightToTheTopItems++;
                StraightToTheTopBottles = Helpers.StraightToTheTopItems * Bundles;
                if (StraightToTheTopBottles > StraightToTheTopMax)
                {
                    StraightToTheTopBottles = StraightToTheTopMax;
                }
            }
            if (Id == 10020039)
            {
                Helpers.TwoToTangoItems++;
                TwoToTangoBottles = Helpers.TwoToTangoItems * Bundles;
                if (TwoToTangoBottles > TwoToTangoMax)
                {
                    TwoToTangoBottles = TwoToTangoMax;
                }
            }
            if (Id == 10020040)
            {
                Helpers.BackAlleyHeistItems++;
                BackAlleyHeistBottles = Helpers.BackAlleyHeistItems * Bundles;
                if (BackAlleyHeistBottles > BackAlleyHeistMax)
                {
                    BackAlleyHeistBottles = BackAlleyHeistMax;
                }
            }
            if (Id == 10020041)
            {
                Helpers.DreadSwampPathItems++;
                DreadSwampPathBottles = Helpers.DreadSwampPathItems * Bundles;
                if (DreadSwampPathBottles > DreadSwampPathMax)
                {
                    DreadSwampPathBottles = DreadSwampPathMax;
                }
            }
            if (Id == 10020042)
            {
                Helpers.LairOfTheBeastItems++;
                LairOfTheBeastBottles = Helpers.LairOfTheBeastItems * Bundles;
                if (LairOfTheBeastBottles > LairOfTheBeastMax)
                {
                    LairOfTheBeastBottles = LairOfTheBeastMax;
                }
            }
            if (Id == 10020043)
            {
                Helpers.GraveUndertakingItems++;
                GraveUndertakingBottles = Helpers.GraveUndertakingItems * Bundles;
                if (GraveUndertakingBottles > GraveUndertakingMax)
                {
                    GraveUndertakingBottles = GraveUndertakingMax;
                }
            }
            if (Id == 10020044)
            {
                Helpers.DescentIntoDangerItems++;
                DescentIntoDangerBottles = Helpers.DescentIntoDangerItems * Bundles;
                if (DescentIntoDangerBottles > DescentIntoDangerMax)
                {
                    DescentIntoDangerBottles = DescentIntoDangerMax;
                }
            }
            if (Id == 10020045)
            {
                Helpers.PerilousAscentItems++;
                PerilousAscentBottles = Helpers.PerilousAscentItems * Bundles;
                if (PerilousAscentBottles > PerilousAscentMax)
                {
                    PerilousAscentBottles = PerilousAscentMax;
                }
            }
            if (Id == 10020046)
            {
                Helpers.FlamingTempleItems++;
                FlamingTempleBottles = Helpers.FlamingTempleItems * Bundles;
                if (FlamingTempleBottles > FlamingTempleMax)
                {
                    FlamingTempleBottles = FlamingTempleMax;
                }
            }
            if (Id == 10020047)
            {
                Helpers.UnseenFoeItems++;
                UnseenFoeBottles = Helpers.UnseenFoeItems * Bundles;
                if (UnseenFoeBottles > UnseenFoeMax)
                {
                    UnseenFoeBottles = UnseenFoeMax;
                }
            }
            if (Id == 10020048)
            {
                Helpers.DuelByTheDragonItems++;
                DuelByTheDragonBottles = Helpers.DuelByTheDragonItems * Bundles;
                if (DuelByTheDragonBottles > DuelByTheDragonMax)
                {
                    DuelByTheDragonBottles = DuelByTheDragonMax;
                }
            }
            var UpdatedLevels = Helpers.GetUpdatedLevels();
            foreach (var Level in UpdatedLevels)
            {
                var WriteMax = Level.ItemBottles * Bundles;
                if (WriteMax > Level.MaxBottles)
                {
                    WriteMax = Level.MaxBottles;
                }
                if (Level.LevelType == "Level")
                {
                    var NameLocation = Memory.ReadUInt(Level.NamePointer) + 0x20000000;
                    Memory.WriteString(NameLocation, Level.Name + " (" + WriteMax + "/" + Level.MaxBottles + ") ");
                }
            }
        }
        public static async void BottleSync()
        {
            Memory.Write(0x2027C6E0, StealthyApproachBottles);
            Memory.Write(0x2027C848, IntoTheMachineBottles);
            Memory.Write(0x2027C7D0, HighClassHeistBottles);
            Memory.Write(0x2027C938, FireDownBelowBottles);
            Memory.Write(0x2027C8C0, CunningDisguiseBottles);
            Memory.Write(0x2027CA28, GunboatGraveyardBottles);
            Memory.Write(0x2027CB2C, RockyStartBottles);
            Memory.Write(0x2027CC1C, BoneyardCasinoBottles);
            Memory.Write(0x2027CDFC, StraightToTheTopBottles);
            Memory.Write(0x2027CD84, TwoToTangoBottles);
            Memory.Write(0x2027CE74, BackAlleyHeistBottles);
            Memory.Write(0x2027CF78, DreadSwampPathBottles);
            Memory.Write(0x2027D068, LairOfTheBeastBottles);
            Memory.Write(0x2027D0E0, GraveUndertakingBottles);
            Memory.Write(0x2027D1D0, DescentIntoDangerBottles);
            Memory.Write(0x2027D3C4, PerilousAscentBottles);
            Memory.Write(0x2027D4B4, FlamingTempleBottles);
            Memory.Write(0x2027D52C, UnseenFoeBottles);
            Memory.Write(0x2027D694, DuelByTheDragonBottles);
            await Task.Delay(100);
        }
    }
}
