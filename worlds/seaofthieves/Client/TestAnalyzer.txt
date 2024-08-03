
import argparse
import os
import time

import SOTDataAnalyzer
import UserInformation
from worlds.seaofthieves.Locations.LocationCollection import LocationDetailsCollection, LocDetails
import typing
import pickle
#
# parser = argparse.ArgumentParser()
# parser.add_argument('--ship', dest='ship', type=str, help='Player ship name')
# parser.add_argument('--mscookie', dest='msCookie', type=str,
#                     help='Microsoft login cookie given to www.seaofthieves.com', nargs='+')
# parser.add_argument('--options', dest='options', type=str,
#                     help='Microsoft login cookie given to www.seaofthieves.com', nargs='+')
# args = parser.parse_args()
# real_cookie = ""
# if args.msCookie is not None:
#     filepath = args.msCookie[0]
#     while not os.path.exists(filepath):
#         filepath = input('File not found. Enter an absolute Filepath to a text file containing your mscookie : ')
#     file = open(filepath, "r")
#     real_cookie = str(file.read())
#     file.close()
#
# if args.options is not None:
#     filepath = args.options[0]
#     while not os.path.exists(filepath):
#         filepath = input('File not found. Enter an absolute Filepath to a text file containing your options.yaml : ')
#     file = open(filepath, "rb")
#     options = pickle.load(file)
#     file.close()
#
# crds = UserInformation.SotLoginCredentials(real_cookie)
# analyzer_dets = UserInformation.SotAnalyzerDetails(args.ship,None)
# userInfo: UserInformation.UserInformation = UserInformation.UserInformation(crds, analyzer_dets, "fake", "fake", options)
# analyzer: SOTDataAnalyzer.SOTDataAnalyzer = SOTDataAnalyzer.SOTDataAnalyzer(userInfo, 1)
#
# locationCollection = LocationDetailsCollection()
# locationCollection.applyOptions(options)
# locationCollection.addAll()
# locs: typing.List[LocDetails] = locationCollection.findDetailsCheckable(set(), True)
#
# #id to locDet
# mappings = {}
# for loc in locs:
#     analyzer.allowTrackingOfLocation(loc)
#     mappings[loc.id] = loc
#     print("tracking: " + loc.name)


# while True:
#     analyzer.update()
#     completedChecks: typing.Dict[int, bool] = analyzer.getAllCompletedChecks()
#     for k in completedChecks.keys():
#         if completedChecks[k]:
#             print("Completed -> " + str(mappings[k].name))
#             analyzer.stopTracking(k)
#
#     time.sleep(1)

