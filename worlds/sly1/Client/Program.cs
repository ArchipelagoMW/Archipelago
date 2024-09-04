// See https://aka.ms/new-console-template for more information
using Archipelago.PCSX2;
using Archipelago.Core.Models;
using Sly1AP.Models;
using Archipelago.Core.Util;
using Newtonsoft.Json;
using System;
using System.Collections;
using System.ComponentModel;
using System.Diagnostics;
using System.Reflection.PortableExecutable;
using System.Runtime.CompilerServices;
using System.Text;
using Archipelago.Core;
using System.IO.Pipes;
using System.Security.Cryptography.X509Certificates;

namespace Sly1AP
{
    public static class Program
    {
        public static string GameVersion { get; set; } = "0";
        public static bool IsConnected { get; set; } = false;
        public static ArchipelagoClient Client { get; set; }
        public static GameState CurrentGameState = new GameState();
        public static Moves slyMoves = new Moves();
        public static Keys keys = new Keys();
        public static int GameCompletion { get; set; } = 0;
        public static async Task Main()
        {
            // Console.SetBufferSize(Console.BufferWidth, 32766);
            Encoding.RegisterProvider(CodePagesEncodingProvider.Instance);

            Console.WriteLine("Sly 1 Archipelago Randomizer");

            await Initialise();

            Console.WriteLine("Beginning main loop.");
            while (true)
            {
                if (!IsConnected)
                {
                    Console.WriteLine("Not connected to Archipelago. Press any key to exit.");
                    Console.ReadKey();
                    return;
                };
                UpdateValues();
                if (Memory.ReadInt(0x2027DC18) == 2721)
                {
                    Memory.Write(0x2027D7AC, 1);
                }
                Thread.Sleep(1);
            }
        }

        private static async Task Initialise()
        {
            Console.Write("Enter Address: ");
            string Address = Console.ReadLine();
            Console.Write("Enter Slot Name: ");
            string SlotName = Console.ReadLine();
            Console.Write("Enter Password: ");
            string Password = Console.ReadLine();
            IsConnected = await ConnectAsync(Address, SlotName, Password);
        }

        static async Task<bool> ConnectAsync(string address, string playerName, string password)
        {
            PCSX2Client client = new PCSX2Client();
            var pcsx2Connected = client.Connect();
            if (!pcsx2Connected)
            {
                Console.WriteLine("Failed to connect to PCSX2.");
                return false;
            }
            Console.WriteLine($"Connected to PCSX2.");

            //Set the game completion flag to 0, so boss locations won't be sent unintentionally.
            Memory.Write(0x2027DC18, 0);

            Console.WriteLine($"Connecting to Archipelago.");
            ArchipelagoClient Client = new(client);
            await Client.Connect(address, "Sly Cooper and the Thievius Raccoonus");
            var locations = Helpers.GetLocations();
            Client.PopulateLocations(locations);
            await Client.Login(playerName, password);
            //On startup, set all values to 0. That way, the game won't overwrite Archipelago's values with the loaded game's values.
            ConfigureOptions(Client.Options);
            UpdateStart();
            var SentLocations = Client.GameState.CompletedLocations;
            var ReceivedItems = Client.GameState.ReceivedItems;
            foreach (var item in ReceivedItems)
            {
                if (item.Id >= 10020001 & item.Id <= 100200014)
                {
                    UpdateMoves(item.Id);
                }
                if (item.Id >= 10020015 & item.Id <= 10020018)
                {
                    UpdateKeys(item.Id);
                }
                if (item.Id >= 10020021 & item.Id <= 10020024)
                {
                    UpdateLevels(item.Id);
                }
                if (item.Id >= 10020019 & item.Id <= 10020020)
                {
                    UpdateJunk(item.Id);
                }
            }
            foreach (var loc in SentLocations)
            {
                if (loc.Name == "Paris Files")
                {
                    GameCompletion += 1;
                }
                if (loc.Name == "Eye of the Storm")
                {
                    GameCompletion += 32;
                }
                if (loc.Name == "Last Call")
                {
                    GameCompletion += 128;
                }
                if (loc.Name == "Deadly Dance")
                {
                    GameCompletion += 512;
                }
                if (loc.Name == "Flame-Fu!")
                {
                    GameCompletion += 2048;
                }

            }
            Client.ItemReceived += (e, args) =>
            {
                Console.WriteLine($"Received: " + args.Item.Name);
                if (args.Item.Id >= 10020001 & args.Item.Id <= 100200014)
                {
                    UpdateMoves(args.Item.Id);
                }
                if (args.Item.Id >= 10020015 & args.Item.Id <= 10020018)
                {
                    UpdateKeys(args.Item.Id);
                }
                if (args.Item.Id >= 10020021 & args.Item.Id <= 10020024)
                {
                    UpdateLevels(args.Item.Id);
                }
                if (args.Item.Id >= 10020019 & args.Item.Id <= 10020020)
                {
                    UpdateJunk(args.Item.Id);
                }
            };
            return true;
        }
        public static void ConfigureOptions(Dictionary<string, object> options)
        {
            var Options = new ArchipelagoOptions();
            if (options == null)
            {
                Console.WriteLine("Options dictionary is null.");
                return;
            }
            if (options.ContainsKey("StartingEpisode"))
            {
                string StartingEpisode = Convert.ToString(options["StartingEpisode"]);
                if (StartingEpisode == "Tide Of Terror")
                {
                    keys.RaleighStart = 1;
                    Memory.Write(0x2027C67C, keys.RaleighStart);
                }
                if (StartingEpisode == "Sunset Snake Eyes")
                {
                    keys.MuggshotStart = 1;
                    Memory.Write(0x2027CAC8, keys.MuggshotStart);
                }
                if (StartingEpisode == "Vicious Voodoo")
                {
                    keys.MzRubyStart = 1;
                    Memory.Write(0x2027CF14, keys.MzRubyStart);
                }
                if (StartingEpisode == "Fire In The Sky")
                {
                    keys.PandaKingStart = 1;
                    Memory.Write(0x2027D360, keys.PandaKingStart);
                }
            }
        }
        //This probably looks like gore to actual programmers, but it works.
        public static void UpdateMoves(int id)
        {
            //var addresses = new Addresses();
            //Progressive Moves
            if (id == 10020001)
            {
                slyMoves.SlyMoves += slyMoves.DiveAttack;
                Memory.Write(0x2027DC10, slyMoves.SlyMoves);
                slyMoves.DiveAttack += 14;
            }
            if (id == 10020002)
            {
                slyMoves.SlyMoves += slyMoves.Roll;
                Memory.Write(0x2027DC10, slyMoves.SlyMoves);
                slyMoves.Roll += 1016;
            }
            if (id == 10020003)
            {
                slyMoves.SlyMoves += slyMoves.Slow;
                Memory.Write(0x2027DC10, slyMoves.SlyMoves);
                if (slyMoves.Slow == 8)
                {
                    slyMoves.Slow += 4080;
                }
                else
                {
                    slyMoves.Slow += 28688;
                }
            }
            if (id == 10020007)
            {
                slyMoves.SlyMoves += slyMoves.Safety;
                Memory.Write(0x2027DC10, slyMoves.SlyMoves);
                slyMoves.Safety += 16128;
            }
            if (id == 10020010)
            {
                slyMoves.SlyMoves += slyMoves.Invisibility;
                Memory.Write(0x2027DC10, slyMoves.SlyMoves);
                slyMoves.Invisibility = 8192;
            }
            //Regular Moves
            if (id == 10020004)
            {
                slyMoves.SlyMoves += slyMoves.CoinMagnet;
                Memory.Write(0x2027DC10, slyMoves.SlyMoves);
            }
            if (id == 10020005)
            {
                slyMoves.SlyMoves += slyMoves.Mine;
                Memory.Write(0x2027DC10, slyMoves.SlyMoves);
            }
            if (id == 10020006)
            {
                slyMoves.SlyMoves += slyMoves.Fast;
                Memory.Write(0x2027DC10, slyMoves.SlyMoves);
            }
            if (id == 10020008)
            {
                slyMoves.SlyMoves += slyMoves.Decoy;
                Memory.Write(0x2027DC10, slyMoves.SlyMoves);
            }
            if (id == 10020009)
            {
                slyMoves.SlyMoves += slyMoves.Hacking;
                Memory.Write(0x2027DC10, slyMoves.SlyMoves);
            }
            //Blueprints
            if (id == 10020011)
            {
                slyMoves.SlyMoves += slyMoves.RaleighBlueprint;
                Memory.Write(0x2027DC10, slyMoves.SlyMoves);
            }
            if (id == 10020012)
            {
                slyMoves.SlyMoves += slyMoves.MuggshotBlueprint;
                Memory.Write(0x2027DC10, slyMoves.SlyMoves);
            }
            if (id == 10020013)
            {
                slyMoves.SlyMoves += (slyMoves.MzRubyBlueprint);
                Memory.Write(0x2027DC10, slyMoves.SlyMoves);
            }
            if (id == 10020014)
            {
                slyMoves.SlyMoves += (slyMoves.PandaKingBlueprint);
                Memory.Write(0x2027DC10, slyMoves.SlyMoves);
            }
            return;
        }
        public static void UpdateKeys(int id)
        {
            //Keys
            if (id == 10020015)
            {
                keys.RaleighKeys += 1;
                Memory.Write(0x2027CAB4, keys.RaleighKeys);
            }
            if (id == 10020016)
            {
                keys.MuggshotKeys += 1;
                Memory.Write(0x2027CF00, keys.MuggshotKeys);
            }
            if (id == 10020017)
            {
                keys.MzRubyKeys += 1;
                Memory.Write(0x2027D34C, keys.MzRubyKeys);
            }
            if (id == 10020018)
            {
                keys.PandaKingKeys += 1;
                Memory.Write(0x2027D798, keys.PandaKingKeys);
            }
            return;
        }
        public static void UpdateLevels(int id)
        {
            //Levels
            if (id == 10020021)
            {
                keys.RaleighStart = 1;
                Memory.Write(0x2027C67C, keys.RaleighStart);
            }
            if (id == 10020022)
            {
                keys.MuggshotStart = 1;
                Memory.Write(0x2027CAC8, keys.MuggshotStart);
            }
            if (id == 10020023)
            {
                keys.MzRubyStart = 1;
                Memory.Write(0x2027CF14, keys.MzRubyStart);
            }
            if (id == 10020024)
            {
                keys.PandaKingStart = 1;
                Memory.Write(0x2027D360, keys.PandaKingStart);
            }
            return;
        }
        public static void UpdateJunk(int id)
        {
            //Junk
            //Don't continuously update these or else they'll never go down!
            if (id == 10020020)
            {
                var Lives = Memory.ReadInt(0x2027DC00);
                Lives += 1;
                Memory.Write(0x2027DC00, Lives);
            }
            if (id == 10020019)
            {
                var Charms = Memory.ReadInt(0x2027DC04);
                if (Charms < 2)
                {
                    Charms += 1;
                    Memory.Write(0x2027DC04, Charms);
                }
                else
                {
                    var Lives = Memory.ReadInt(0x2027DC00);
                    Lives += 1;
                    Memory.Write(0x2027DC00, Lives);
                }
            }
            return;
        }
        public static void UpdateValues()
        {
            Memory.Write(0x2027DC10, slyMoves.SlyMoves);
            Memory.Write(0x2027CAB4, keys.RaleighKeys);
            Memory.Write(0x2027CF00, keys.MuggshotKeys);
            Memory.Write(0x2027D34C, keys.MzRubyKeys);
            Memory.Write(0x2027D798, keys.PandaKingKeys);
            //Make all maps selectable from the start.
            Memory.Write(0x2027CAC4, keys.Map);
            Memory.Write(0x2027CF10, keys.Map);
            Memory.Write(0x2027D35C, keys.Map);
            Memory.Write(0x2027D7A8, keys.Map);
            return;
        }
        public static void GetValues()
        {
            slyMoves.SlyMoves = Memory.ReadUInt(0x2027DC10);
            keys.RaleighKeys = Memory.ReadInt(0x2027CAB4);
            keys.MuggshotKeys = Memory.ReadInt(0x2027CF00);
            keys.MzRubyKeys = Memory.ReadInt(0x2027D34C);
            keys.PandaKingKeys = Memory.ReadInt(0x2027D798);
            keys.RaleighStart = Memory.ReadInt(0x2027C67C);
            keys.MuggshotStart = Memory.ReadInt(0x2027CAC8);
            keys.MzRubyStart = Memory.ReadInt(0x2027CF14);
            keys.PandaKingStart = Memory.ReadInt(0x2027D360);
        }
        public static void UpdateStart()
        {
            Memory.Write(0x2027DC10, 0);
            Memory.Write(0x2027CAB4, 0);
            Memory.Write(0x2027CF00, 0);
            Memory.Write(0x2027D34C, 0);
            Memory.Write(0x2027D798, 0);
            Memory.Write(0x2027C67C, 0);
            Memory.Write(0x2027CAC8, 0);
            Memory.Write(0x2027CF14, 0);
            Memory.Write(0x2027D360, 0);
            GetValues();
        }
    }
}

