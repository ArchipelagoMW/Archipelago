import os
import json
import pkgutil
from .data.item_info import item_info

apworld_version = "v0.0.1"
base_id = 3000000

Scenario_Items = {
  # "Lakeside Gardens"
  0: item_info['Rides'] + item_info['Shops'],

  # "Dusty Ridge Ranch"
  1: item_info['Rides'] + item_info['Shops'],

  # "The Broken Atoll"
  2: item_info['Rides'] + item_info['Shops'],

  # "Magma Falls"
  3: item_info['Rides'] + item_info['Shops'],
}