import typing


class RegionNameCollection:

    def __int__(self):
        self.regions = {}

    def add(self, name: str):
        self.regions = {}
        self.regions[name] = True

    def addFromList(self, details):
        self.regions = {}
        for i in range(len(details)):
            self.regions[details[i].name] = True

    # def contains(self, name: Name):
    #     return name in self.regions
    #
    # def getAllRegionStrings(self) -> typing.List[str]:
    #     ret: typing.List[str] = []
    #     for key in self.regions.keys():
    #         ret.append(key)
    #     return ret

    def getFirst(self) -> str:

        # TODO make this function return the set and have logic pick one?
        for k in self.regions.keys():
            return k
