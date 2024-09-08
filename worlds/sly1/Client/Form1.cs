using Archipelago.Core.Util;
using Archipelago.PCSX2;
using Archipelago.Core.Models;
using Newtonsoft.Json;
using System.Media;
using System.Reflection;
using System.Text;
using System.Windows.Forms;
using static System.Windows.Forms.AxHost;
using static System.Windows.Forms.Design.AxImporter;
using Archipelago.Core;
using Sly1AP.Models;

namespace Sly1AP
{
    public partial class Form1 : Form
    {
        public static string GameVersion { get; set; } = "0";
        public static bool IsConnected { get; set; } = false;
        public static GameState CurrentGameState = new GameState();
        public static ArchipelagoClient? Client { get; set; }
        public static Moves slyMoves = new Moves();
        public static SlyKeys keys = new SlyKeys();
        public static int GameCompletion { get; set; } = 0;
        public Form1()
        {
            InitializeComponent();
            Encoding.RegisterProvider(CodePagesEncodingProvider.Instance);
            ThreadPool.SetMinThreads(500, 500);
            Console.WriteLine($"Sly 1 Archipelago Randomizer");
        }
        public async Task Loop()
        {
            // Console.SetBufferSize(Console.BufferWidth, 32766);

            while (true)
            {
                UpdateValues();
                if (Memory.ReadInt(0x2027DC18) == 2721)
                {
                    Memory.Write(0x2027D7AC, 1);
                }
                if (Memory.ReadByte(0x202623C0) == 0)
                {
                    Thread.Sleep(1000);
                    if (Memory.ReadByte(0x202623C0) == 0)
                    {
                        WriteLine("Lost connection to PCSX2.");
                        return;
                    }
                }
                if (!Client.IsConnected)
                {
                    return;
                }
                await Task.Delay(1000);
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
            Memory.Write(0x2027DC18, 0);

            WriteLine($"Connecting to Archipelago.");
            Client = new ArchipelagoClient(client);
            Client.Connected += OnConnected;
            Client.Disconnected += OnDisconnected;
            await Client.Connect(hostTextbox.Text, "Sly Cooper and the Thievius Raccoonus");
            var locations = Helpers.GetLocations();
            await Client.Login(slotTextbox.Text, passwordTextbox.Text);
            Client.PopulateLocations(locations);
            //On startup, set all values to 0. That way, the game won't overwrite Archipelago's values with the loaded game's values.
            UpdateStart();
            CutsceneSkip();
            ConfigureOptions(Client.Options);
            var SentLocations = Client.GameState.CompletedLocations;
            var ItemsReceived = Client.GameState.ReceivedItems;
            var NewItems = new List<Item>(ItemsReceived);
            var NewLocations = new List<Location>(SentLocations);
            foreach (var item in NewItems)
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
            WriteLine($"Receiving offline items.");
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
                if (StartingEpisode == "All" & Memory.ReadInt(0x2027C67C) == 0 & Memory.ReadInt(0x2027CAC8) == 0 & Memory.ReadInt(0x2027CF14) == 0 & Memory.ReadInt(0x2027D360) == 0)
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
            GetValues();
        }
        public void WriteLine(string output)
        {
            Invoke(() =>
            {
                outputTextbox.Text += output;
                outputTextbox.Text += System.Environment.NewLine;

                System.Diagnostics.Debug.WriteLine(output + System.Environment.NewLine);
            });
        }
        private void OnConnected(object? sender, EventArgs args)
        {
            WriteLine("Connected to Archipelago");
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
            Memory.Write(0x2027C3C0, 1);
            Memory.Write(0x2027C424, 1);
            Memory.Write(0x2027C960, 1);
            Memory.Write(0x2027D9A0, 1);
            Memory.Write(0x2027D9A4, 1);
            Memory.Write(0x2027CD3C, 1);
            Memory.Write(0x2027D678, 1);
        }
    }
}