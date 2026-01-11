from typing import List

from BaseClasses import ItemClassification
from worlds.dc1.Options import DarkCloudOptions
from worlds.dc1.Items import DarkCloudItem

ids = {
    "Progressive Parts HD": 971110500,
    "Progressive Parts AMR": 971110501,
    "Progressive Parts AML": 971110502,
    "Progressive Parts HGR": 971110503,
    "Progressive Parts HGL": 971110504,
    "Progressive Parts HGR2": 971110505,
    "Progressive Parts HGL2": 971110506,
    "Progressive Parts CT": 971110507,
    "Progressive Parts WT": 971110508,
    "Progressive Parts TIR": 971110509,
    "Progressive Parts TIL": 971110510,
    "Progressive Parts FTR": 971110511,
    "Progressive Parts FTL": 971110512,
    "Progressive Lookout": 971110513,
  }

# Head is required to fight Joe
head_ids = ["Progressive Parts HD", "Progressive Parts HD"]

aml_ids = ["Progressive Parts AML", "Progressive Parts AML", "Progressive Parts AML",
           "Progressive Parts AML", "Progressive Parts AML"]
amr_ids = ["Progressive Parts AMR", "Progressive Parts AMR", "Progressive Parts AMR",
           "Progressive Parts AMR", "Progressive Parts AMR"]
hgr_ids = ["Progressive Parts HGR", "Progressive Parts HGR", "Progressive Parts HGR", "Progressive Parts HGR"]
hgl_ids = ["Progressive Parts HGL", "Progressive Parts HGL", "Progressive Parts HGL", "Progressive Parts HGL"]
hg2_ids = ["Progressive Parts HGR2", "Progressive Parts HGL2"]
chest_ids = ["Progressive Parts CT","Progressive Parts CT"]
waist_ids = ["Progressive Parts WT", "Progressive Parts WT", "Progressive Parts WT"]
tir_ids = ["Progressive Parts TIR", "Progressive Parts TIR"]
til_ids = ["Progressive Parts TIL", "Progressive Parts TIL"]
ftr_ids = ["Progressive Parts FTR", "Progressive Parts FTR", "Progressive Parts FTR", "Progressive Parts FTR"]
ftl_ids = ["Progressive Parts FTL", "Progressive Parts FTL", "Progressive Parts FTL", "Progressive Parts FTL"]

# Excluding the lookout tower, only the first piece of any georama gives any MCs
mc_filler = ["Progressive Lookout", "Progressive Lookout", "Progressive Parts AMR", "Progressive Parts AML",
             "Progressive Parts HGR", "Progressive Parts HGL", "Progressive Parts HGR2", "Progressive Parts HGL2",
             "Progressive Parts TIR", "Progressive Parts TIL", "Progressive Parts FTR", "Progressive Parts FTL"]
mc_useful = ["Progressive Lookout", "Progressive Lookout", "Progressive Parts CT", "Progressive Parts WT"]

filler_ids = (aml_ids + amr_ids + hgr_ids + hgl_ids + hg2_ids + chest_ids + waist_ids +
              tir_ids + til_ids + ftr_ids + ftl_ids)

def create_factory_atla(options: DarkCloudOptions, player: int) -> List["DarkCloudItem"]:
  items = []

  factory_required = []
  factory_useful = []
  factory_filler = filler_ids.copy()

  if options.boss_goal == 5 or options.all_bosses:
    factory_required.extend(head_ids + ["Progressive Parts HD"])
  else:
    if options.miracle_sanity:
      factory_required.append("Progressive Parts HD")
    else:
      factory_useful.append("Progressive Parts HD")
    factory_filler.extend(head_ids)

  if options.miracle_sanity:
    factory_required.extend(mc_useful)
    factory_required.extend(mc_filler)
  else:
    factory_useful.extend(mc_useful)
    factory_filler.extend(mc_filler)

  for i in factory_required:
    items.append(DarkCloudItem(i, ItemClassification.progression, ids[i], player))

  for i in factory_useful:
    items.append(DarkCloudItem(i, ItemClassification.useful, ids[i], player))

  for i in factory_filler:
    items.append(DarkCloudItem(i, ItemClassification.filler, ids[i], player))

  # print(len(items))
  # print (items)
  return items

