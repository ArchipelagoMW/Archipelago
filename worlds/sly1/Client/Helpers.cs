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

namespace Sly1AP
{
    class Helpers
    {
        public static List<Location> GetLocations()
        {
            var json = OpenEmbeddedResource("Sly1AP.Resources.Locations.json");
            var list = JsonConvert.DeserializeObject<List<Location>>(json);
            return list;
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
    }
}
