using Archipelago.Core.Util;
using Archipelago.Core.Models;
using Archipelago.Core.GameClients;
using Newtonsoft.Json;
using System.Media;
using System.Reflection;
using System.Text;
using System.Windows.Forms;
using static System.Windows.Forms.AxHost;
using static System.Windows.Forms.Design.AxImporter;
using Archipelago.Core;
using Sly1AP.Models;
using System.Windows;
using System.Timers;
using System.Security.Policy;
using System.Text.Json;
using System;
using System.Linq;

namespace Sly1AP
{
    public partial class Form1 : Form
    {
        public static string GameVersion { get; set; } = "0";
        public static bool IsConnected { get; set; } = false;
        public static GameState CurrentGameState = new GameState();
        public static ArchipelagoClient Client { get; set; }
        public static Moves slyMoves = new Moves();
        public static SlyKeys keys = new SlyKeys();
        public static int GameCompletion { get; set; } = 0;
        public static Random rnd = new Random();
        public static int ClueBundles { get; set; } = 0;
        public Form1()
        {
            InitializeComponent();
            Encoding.RegisterProvider(CodePagesEncodingProvider.Instance);
            ThreadPool.SetMinThreads(500, 500);
        }
        public async Task Loop()
        {
            // Console.SetBufferSize(Console.BufferWidth, 32766);

            while (true)
            {
                UpdateValues();
                CutsceneSkip();
                UpdateBosses();
                if (ClueBundles > 0)
                {
                    Clues.BottleSync();
                }
                if (Memory.ReadByte(0x202623C0) == 0)
                {
                    Thread.Sleep(1000);
                    if (Memory.ReadByte(0x202623C0) == 0)
                    {
                        WriteLine("Lost connection to PCSX2. Are you using 1.6.0?");
                        return;
                    }
                }
                if (!Client.IsConnected)
                {
                    return;
                }
                await Task.Delay(100);
            }
        }

        public async Task<bool> ConnectAsync()
        {
            if (Client != null)
            {
                Client.Connected -= OnConnected;
                Client.Disconnected -= OnDisconnected;
            }
            PCSX2Client client = new PCSX2Client();
            var pcsx2Connected = client.Connect();
            if (!pcsx2Connected)
            {
                WriteLine("Failed to connect to PCSX2.");
                return false;
            }
            WriteLine($"Connected to PCSX2.");

            //Set the game completion flag to 0, so boss locations won't be sent unintentionally.
            //Memory.Write(0x2027DC18, 0);

            WriteLine($"Connecting to Archipelago.");
            Client = new ArchipelagoClient(client);
            Client.Connected += OnConnected;
            Client.Disconnected += OnDisconnected;
            Client.ItemReceived += (e, args) =>
            {
                WriteLine($"Received: {JsonConvert.SerializeObject(args.Item.Name)}");
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
                if (args.Item.Id >= 10020026 & args.Item.Id <= 10020029)
                {
                    UpdateTraps(args.Item.Id);
                }
                if (args.Item.Id == 10020025)
                {
                    Client.SendGoalCompletion();
                }
                if (args.Item.Id >= 10020030 & args.Item.Id <= 10020048)
                {
                    Clues.UpdateBottles(args.Item.Id, ClueBundles);
                }
            };
            await Client.Connect(hostTextbox.Text, "Sly Cooper and the Thievius Raccoonus");
            var locations = Helpers.GetLocations();
            await Client.Login(slotTextbox.Text, passwordTextbox.Text);
            var PlayerName = slotTextbox.Text;
            await Client.PopulateLocations(locations);
            if (Memory.ReadInt(0x2027DBF8) == 0 & Memory.ReadInt(0x2027DBFC) != 4)
            {
                WriteLine("Load a save file, start a new game, or finish the prologue.");
                while (Memory.ReadInt(0x2027DBF8) == 0 & Memory.ReadInt(0x2027DBFC) != 4)
                {
                    CutsceneSkip();
                    await Task.Delay(1000);
                }
            }
            //On startup, set all values to 0. That way, the game won't overwrite Archipelago's values with the loaded game's values.
            UpdateStart();
            ConfigureOptions(Client.Options);
            var SentLocations = Client.GameState.CompletedLocations;
            var ItemsReceived = Client.GameState.ReceivedItems;
            var NewItems = new List<Item>(ItemsReceived);
            var NewLocations = new List<Location>(SentLocations);
            foreach (var item in NewItems)
            {
                for (int i = 0; i < item.Quantity; i++)
                {
                    if (item.Id >= 10020001 & item.Id <= 10020014)
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
                    if (item.Id >= 10020030 & item.Id <= 10020048)
                    {
                        Clues.UpdateBottles(item.Id, ClueBundles);
                    }
                }
            }
            foreach (var loc in NewLocations)
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
            Client.MessageReceived += (e, args) =>
            {
                string ClientMessage = args.Message?.ToString();
                if (ClientMessage != null & ClientMessage.Contains(PlayerName))
                {
                    WriteLine($"{args.Message}");
                }
            };
            await Loop();
            return true;
        }

        private void Client_Disconnected(object? sender, ConnectionChangedEventArgs e)
        {
            throw new NotImplementedException();
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
                string? StartingEpisode = Convert.ToString(options["StartingEpisode"]);
                if (StartingEpisode == "Tide of Terror" & Memory.ReadInt(0x2027C67C) == 0)
                {
                    keys.RaleighStart = 1;
                    Memory.Write(0x2027C67C, keys.RaleighStart);
                }
                if (StartingEpisode == "Sunset Snake Eyes" & Memory.ReadInt(0x2027CAC8) == 0)
                {
                    keys.MuggshotStart = 1;
                    Memory.Write(0x2027CAC8, keys.MuggshotStart);
                }
                if (StartingEpisode == "Vicious Voodoo" & Memory.ReadInt(0x2027CF14) == 0)
                {
                    keys.MzRubyStart = 1;
                    Memory.Write(0x2027CF14, keys.MzRubyStart);
                }
                if (StartingEpisode == "Fire in the Sky" & Memory.ReadInt(0x2027D360) == 0)
                {
                    keys.PandaKingStart = 1;
                    Memory.Write(0x2027D360, keys.PandaKingStart);
                }
                if (StartingEpisode == "All" & Memory.ReadInt(0x2027C67C) == 0 & Memory.ReadInt(0x2027CAC8) == 0 
                    & Memory.ReadInt(0x2027CF14) == 0 & Memory.ReadInt(0x2027D360) == 0)
                {
                    keys.RaleighStart = 1;
                    keys.MuggshotStart = 1;
                    keys.MzRubyStart = 1;
                    keys.PandaKingStart = 1;
                    Memory.Write(0x2027C67C, keys.RaleighStart);
                    Memory.Write(0x2027CAC8, keys.MuggshotStart);
                    Memory.Write(0x2027CF14, keys.MzRubyStart);
                    Memory.Write(0x2027D360, keys.PandaKingStart);
                }
            }
            if (options.ContainsKey("CluesanityBundleSize"))
            {
                var clueBundleSizeElement = (JsonElement)options["CluesanityBundleSize"];
                ClueBundles = clueBundleSizeElement.GetUInt16();
            }
        }
        //This probably looks like gore to actual programmers, but it works.
        public static void UpdateMoves(long id)
        {
            //var addresses = new Addresses();
            //Progressive Moves
            if (id == 10020001)
            {
                slyMoves.SlyMoves += slyMoves.DiveAttack;
                slyMoves.DiveAttack += 14;
            }
            if (id == 10020002)
            {
                slyMoves.SlyMoves += slyMoves.Roll;
                slyMoves.Roll += 1016;
            }
            if (id == 10020003)
            {
                slyMoves.SlyMoves += slyMoves.Slow;
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
                slyMoves.Safety += 16128;
                slyMoves.SafetyCount += 1;
            }
            if (id == 10020010)
            {
                slyMoves.SlyMoves += slyMoves.Invisibility;
                slyMoves.Invisibility = 8192;
            }
            //Regular Moves
            if (id == 10020004)
            {
                slyMoves.SlyMoves += slyMoves.CoinMagnet;
            }
            if (id == 10020005)
            {
                slyMoves.SlyMoves += slyMoves.Mine;
            }
            if (id == 10020006)
            {
                slyMoves.SlyMoves += slyMoves.Fast;
            }
            if (id == 10020008)
            {
                slyMoves.SlyMoves += slyMoves.Decoy;
            }
            if (id == 10020009)
            {
                slyMoves.SlyMoves += slyMoves.Hacking;
            }
            //Blueprints
            if (id == 10020011)
            {
                slyMoves.SlyMoves += slyMoves.RaleighBlueprint;
            }
            if (id == 10020012)
            {
                slyMoves.SlyMoves += slyMoves.MuggshotBlueprint;
            }
            if (id == 10020013)
            {
                slyMoves.SlyMoves += slyMoves.MzRubyBlueprint;
            }
            if (id == 10020014)
            {
                slyMoves.SlyMoves += slyMoves.PandaKingBlueprint;
            }
            return;
        }
        public static void UpdateKeys(long id)
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
        public static void UpdateLevels(long id)
        {
            //Levels
            if (id == 10020021 & Memory.ReadInt(0x2027C67C) == 0)
            {
                keys.RaleighStart = 1;
                Memory.Write(0x2027C67C, keys.RaleighStart);
            }
            if (id == 10020022 & Memory.ReadInt(0x2027CAC8) == 0)
            {
                keys.MuggshotStart = 1;
                Memory.Write(0x2027CAC8, keys.MuggshotStart);
            }
            if (id == 10020023 & Memory.ReadInt(0x2027CF14) == 0)
            {
                keys.MzRubyStart = 1;
                Memory.Write(0x2027CF14, keys.MzRubyStart);
            }
            if (id == 10020024 & Memory.ReadInt(0x2027D360) == 0)
            {
                keys.PandaKingStart = 1;
                Memory.Write(0x2027D360, keys.PandaKingStart);
            }
            return;
        }
        public static void UpdateJunk(long id)
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
        public static async void UpdateTraps(long id)
        {
            var TrapTimer = new System.Timers.Timer(10000);
            TrapTimer.AutoReset = false;
            //Traps
            uint SlyControl = 0x20262C68;
            if (Memory.ReadByte(SlyControl) != 7)
            {
                while (Memory.ReadByte(SlyControl) != 7)
                {
                   await Task.Delay(1000);
                }
            }
            if (id == 10020026)
            {
                TrapTimer.Start();
                if (TrapTimer.Interval != 0) // Check if the trap timer is not 0
                {
                   Memory.Write(0x20274AD0, 1060655596);
                }
                TrapTimer.Elapsed += (sender, e) =>
                {
                    Memory.Write(0x20274AD0, 0);
                    Memory.Write(0x20274AD2, -49280);
                    TrapTimer.Stop();
                    TrapTimer.Dispose();
                };
            }
            if (id == 10020027)
            {
                TrapTimer.Start();
                int random = rnd.Next(1, 3);
                if (TrapTimer.Interval != 0)
                {
                    if (random == 1)
                    {
                        Memory.Write(0x20261850, 1056964608);
                    }
                    if (random == 2)
                    {
                        Memory.Write(0x20261850, 1069547520);
                    }
                }
                TrapTimer.Elapsed += (sender, e) =>
                {
                    Memory.Write(0x20261850, 1065353216);
                    //Memory.Write(0x20261852, -128);
                    TrapTimer.Stop();
                    TrapTimer.Dispose();
                };
            }
            if (id == 10020028)
            {
                TrapTimer.Start();
                uint TrueMoves = 0;
                int TrueSelect = 0;
                if (slyMoves.SlyMoves != 4)
                {
                    TrueMoves = slyMoves.SlyMoves;
                }

                //Get the current position of Sly's data in code.
                uint SlyPos = (Memory.ReadUInt(0x20262E10) + 536870912) + 8736;
                uint BodyPos = SlyPos + 8;
                uint CanePos = SlyPos + 28;
                //Reset Sly's current action to 0.
                Memory.Write(SlyPos, 0);
                Memory.Write(BodyPos, 0);
                Memory.Write(CanePos, 0);

                if (slyMoves.SafetyCount == 1)
                {
                    slyMoves.SlyMoves = 260;
                }
                if (slyMoves.SafetyCount == 2)
                {
                    slyMoves.SlyMoves = 16644;
                }
                else
                {
                    slyMoves.SlyMoves = 4;
                }

                while (TrapTimer.Enabled == true)
                {
                    Memory.Write(0x20274F74, 1);
                    Memory.Write(0x20262D18, 16);
                    Memory.Write(0x20262D22, 0xFF);
                    Memory.Write(0x20262D1A, 16);
                    await Task.Delay(1);
                };
                TrapTimer.Elapsed += (sender, e) =>
                {
                    Memory.Write(0x20262D18, 0);
                    Memory.Write(0x20262D22, 0);
                    Memory.Write(0x20262D1A, 0);
                    Memory.Write(0x20262D1C, 0);
                };
                TrapTimer.Stop();
                TrapTimer.Dispose();
                slyMoves.SlyMoves = TrueMoves;
                Memory.Write(0x20274F74, TrueSelect);
                return;
            }
            if (id == 10020029)
            {
                int random = rnd.Next(Helpers.bentley.Length);
                string SoundFile = Helpers.bentley[random];
                var stream = Assembly.GetExecutingAssembly().GetManifestResourceStream(SoundFile);
                SoundPlayer player = new SoundPlayer(stream);
                player.Play();
            }
        }
        public static void UpdateValues()
        {
            Memory.Write(0x2027DC10, slyMoves.SlyMoves);
            Memory.Write(0x2027CAB4, keys.RaleighKeys);
            Memory.Write(0x2027CF00, keys.MuggshotKeys);
            Memory.Write(0x2027D34C, keys.MzRubyKeys);
            Memory.Write(0x2027D798, keys.PandaKingKeys);
            //Make all maps selectable.
            if (Memory.ReadInt(0x2027CAC4) == 0)
            {
                Memory.Write(0x2027CAC4, keys.Map);
            }
            if (Memory.ReadInt(0x2027CF10) == 0)
            {
                Memory.Write(0x2027CF10, keys.Map);
            }
            if (Memory.ReadInt(0x2027D35C) == 0)
            {
                Memory.Write(0x2027D35C, keys.Map);
            }
            if (Memory.ReadInt(0x2027D7A8) == 0)
            {
                Memory.Write(0x2027D7A8, keys.Map);
            }
            return;
        }
        public static void GetValues()
        {
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
            slyMoves.SlyMoves = 0;
            slyMoves.Roll = 4;
            slyMoves.DiveAttack = 2;
            slyMoves.Slow = 8;
            slyMoves.Safety = 256;
            slyMoves.Invisibility = 65536;
            slyMoves.SafetyCount = 0;
            Memory.Write(0x2027CAB4, 0);
            Memory.Write(0x2027CF00, 0);
            Memory.Write(0x2027D34C, 0);
            Memory.Write(0x2027D798, 0);
            GetValues();
        }
        public void WriteLine(string output)
        {
            Invoke(() =>
            {
                outputTextbox.Text += output;
                outputTextbox.Text += System.Environment.NewLine;
                outputTextbox.SelectionStart = outputTextbox.Text.Length;
                outputTextbox.ScrollToCaret();

                System.Diagnostics.Debug.WriteLine(output + System.Environment.NewLine);
            });
        }
        private void OnConnected(object? sender, EventArgs args)
        {
            WriteLine("Connected to Archipelago.");
            WriteLine($"Playing {Client?.CurrentSession.ConnectionInfo.Game} as {Client?.CurrentSession.Players.GetPlayerName(Client.CurrentSession.ConnectionInfo.Slot)}");
            Invoke(() =>
            {
                connectBtn.Text = "Disconnect";
            });
        }
        private void OnDisconnected(object? sender, EventArgs args)
        {
            WriteLine($"Disconnected from Archipelago.");
            Invoke(() =>
            {
                connectBtn.Text = "Connect";
            });
        }
        private bool ValidateSettings()
        {
            var valid = !string.IsNullOrWhiteSpace(hostTextbox.Text) && !string.IsNullOrWhiteSpace(slotTextbox.Text);
            return valid;
        }
        private async void connectBtn_Click(object sender, EventArgs e)
        {
            if (!(Client?.IsConnected ?? false))
            {
                var valid = ValidateSettings();
                if (!valid)
                {
                    WriteLine("Invalid settings, please check your input and try again.");
                    return;
                }
                await ConnectAsync().ConfigureAwait(false);
            }
            else
            {
                WriteLine("Disconnecting...");
                Client.Disconnect();
            }
        }
        private void CutsceneSkip()
        {
            //Dialogue Skipper
            uint Cutscene = Memory.ReadUInt(0x2027051C) + 0x20000000;
            uint Playing = Cutscene + 744;
            int SlyControl = Memory.ReadInt(0x20262C68);
            if (Memory.ReadUInt(Cutscene) != 0 & SlyControl != 7)
            {
                Memory.Write(Playing, 0);
            }

            //Bentley Skipper
            if (Memory.ReadInt(0x20270458) == 2)
            {
                Memory.Write(0x20270458, 0);
            }

            //FMV Skipper
            if (Memory.ReadInt(0x20269A18) > 20)
            {
                Memory.Write(0x20269A60, 0);
            }
        }
        private void UpdateBosses()
        {
            if ((Memory.ReadBit(0x2027DC18, 5)) & (Memory.ReadBit(0x2027DC18, 7)) & (Memory.ReadBit(0x2027DC19, 1)) & (Memory.ReadBit(0x2027DC19, 3)))
            {
                Memory.Write(0x2027D7A8, 53);
            }
            else if (Memory.ReadByte(0x2027D7A8) >= 21)
            {
                Memory.Write(0x2027D7A8, 21);
            }
        }
    }
}