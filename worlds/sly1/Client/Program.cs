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
        public static async Task Main()
        {
            Console.SetBufferSize(Console.BufferWidth, 32766);
            Encoding.RegisterProvider(CodePagesEncodingProvider.Instance);

            Console.WriteLine("Sly 1 Archipelago Randomizer");

            await Initialise();

            Console.WriteLine("Beginning main loop.");
            while (true)
            {
                Thread.Sleep(1);
            }
        }

        private static async Task Initialise()
        {
            Console.WriteLine("Enter Address:");
            string Address = Console.ReadLine();
            Console.WriteLine("Enter Slot Name:");
            string SlotName = Console.ReadLine();
            Console.WriteLine("Enter Password:");
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

            Console.WriteLine($"Connecting to Archipelago.");
            ArchipelagoClient Client = new(client);
            await Client.Connect(address, "Sly Cooper and the Thievius Raccoonus");
            var locations = Helpers.GetLocations();
            Client.PopulateLocations(locations);
            await Client.Login(playerName, password);
            //ConfigureOptions(Client.Options);
            Client.ItemReceived += (e, args) =>
            {
                Console.WriteLine($"Received: + {JsonConvert.SerializeObject(args.Item)}");
            };
            return true;
        }
        public static async void ConfigureOptions(Dictionary<string, object> options)
        {
            var Options = new ArchipelagoOptions();
            if (options == null)
            {
                Console.WriteLine("Options dictionary is null.");
                return;
            }
        }
    }
}

