const data = require("./data/extracted_data.json")

// console.log(Object.entries(data.maps).reduce((acc, map, i) => {
//   if (map[1].land_encounters !== undefined)
//     map[1].land_encounters.slots.forEach((slot) => acc.add(slot + (i * 1000)))
//   if (map[1].water_encounters !== undefined)
//     map[1].water_encounters.slots.forEach((slot) => acc.add(slot + (i * 1000)))
//   if (map[1].fishing_encounters !== undefined)
//     map[1].fishing_encounters.slots.forEach((slot) => acc.add(slot + (i * 1000)))

//   // if (map[1].water_encounters !== undefined && map[1].fishing_encounters === undefined) {
//   //   console.log(map[0])
//   //   console.log(map[1])
//   // }
//   // if (map[1].fishing_encounters !== undefined && map[1].water_encounters === undefined) {
//   //   console.log(map[0])
//   //   console.log(map[1])
//   // }

//   return acc
// }, new Set()))

const region = require("./data/regions/routes.json")
console.log(JSON.stringify(Object.entries(region).reduce((acc, [regionName, regionData]) => {
  return {
    ...acc,
    [regionName]: {
      parent_map: regionData.parent_map,
      has_grass: false,
      has_water: false,
      has_fishing: false,
      ...regionData
    }
  }
}, {})))
