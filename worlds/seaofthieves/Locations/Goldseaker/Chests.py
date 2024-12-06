from ..LocationsBase import LocationsBase


class SettingsChest:

    def __init__(self, gh_count=10, ma_count=10, oos_count=10, rb_count=2, af_count=5):
        self.gh_count = gh_count
        self.ma_count = ma_count
        self.oos_count = oos_count
        self.rb_count = rb_count
        self.af_count = af_count


class Chests(LocationsBase):
    L_UN_SELL_CHEST = "Sell (GH)"
    L_UN_SELL_SKULL = "Sell (OoS)"
    L_UN_SELL_MERCH = "Sell (MA)"
    L_UN_SELL_AF = "Sell (AF)"
    L_UN_SELL_RB = "Sell (RB)"

    def __init__(self, settings: SettingsChest):
        super().__init__()

        # This is a big work in progress. The idea is that we can allow the player to get a check when they sell a generic chest
        # This needs to be tested, but before we can, we need to fix the item requirements to be something tangible and event based

        '''
        self.x = [0, 1, 1]
        reg = RegionNameCollection()
        reg.addFromList([Regions.R_DOMAIN_GH, Regions.R_DOMAIN_GH_ASHEN])
        lgc = ItemReqEvalOr([])
        web = WebItemJsonIdentifier(0, 2, 0)
        wlc = WebLocationCollection([WebLocation(web, reg, lgc)])

        for i in range(1, settings.gh_count+1):
            cnt = i*5
            self.locations.append(LocDetails(self.L_UN_SELL_CHEST + " " + str(cnt), copy.deepcopy(wlc)))
            itm_detail = copy.deepcopy(Items.upgrade_cnt_gh)
            itm_detail.req_qty = cnt
            lgc = ItemReqEvalOr([itm_detail])
            wlc = WebLocationCollection([WebLocation(web, reg, lgc)])



        reg = RegionNameCollection()
        reg.addFromList([Regions.R_DOMAIN_OOS, Regions.R_DOMAIN_OOS_ASHEN])
        lgc = ItemReqEvalOr([])
        web = WebItemJsonIdentifier(0, 4, 0)
        wlc = WebLocationCollection([WebLocation(web, reg, lgc)])
        for i in range(1, settings.oos_count+1):
            cnt = i * 5
            self.locations.append(LocDetails(self.L_UN_SELL_SKULL + " " + str(i), copy.deepcopy(wlc)))
            itm_detail = copy.deepcopy(Items.upgrade_cnt_gh)
            itm_detail.req_qty = cnt
            lgc = ItemReqEvalOr([itm_detail])
            wlc = WebLocationCollection([WebLocation(web, reg, lgc)])

        reg = RegionNameCollection()
        reg.addFromList([Regions.R_DOMAIN_MA, Regions.R_DOMAIN_MA_ASHEN])
        lgc = ItemReqEvalOr([])
        web = WebItemJsonIdentifier(0, 3, 0)
        wlc = WebLocationCollection([WebLocation(web, reg, lgc)])
        for i in range(1, settings.ma_count+1):
            cnt = i * 5
            self.locations.append(LocDetails(self.L_UN_SELL_MERCH + " " + str(i), copy.deepcopy(wlc)))
            itm_detail = copy.deepcopy(Items.upgrade_cnt_ma)
            itm_detail.req_qty = cnt
            lgc = ItemReqEvalOr([itm_detail])
            wlc = WebLocationCollection([WebLocation(web, reg, lgc)])

        reg = RegionNameCollection()
        reg.addFromList([Regions.R_DOMAIN_AF, Regions.R_DOMAIN_AF_ASHEN])
        lgc = ItemReqEvalOr([Items.emissary_af])
        web = WebItemJsonIdentifier(0, 5, 0)
        wlc = WebLocationCollection([WebLocation(web, reg, lgc)])
        for i in range(1, settings.af_count+1):
            cnt = i
            self.locations.append(LocDetails(self.L_UN_SELL_AF + " " + str(cnt), copy.deepcopy(wlc)))
            itm_detail = copy.deepcopy(Items.emissary_af)
            itm_detail.req_qty = cnt
            lgc = ItemReqEvalOr([itm_detail])
            wlc = WebLocationCollection([WebLocation(web, reg, lgc)])

        reg = RegionNameCollection()
        reg.addFromList([Regions.R_DOMAIN_RB, Regions.R_DOMAIN_RB_ASHEN])
        lgc = ItemReqEvalOr([Items.emissary_rb])
        web = WebItemJsonIdentifier(0, 6, 0)
        wlc = WebLocationCollection([WebLocation(web, reg, lgc)])
        for i in range(1, settings.rb_count+1):
            cnt = i
            self.locations.append(LocDetails(self.L_UN_SELL_RB + " " + str(cnt), copy.deepcopy(wlc)))
            itm_detail = copy.deepcopy(Items.emissary_rb)
            itm_detail.req_qty = cnt
            lgc = ItemReqEvalOr([itm_detail])
            wlc = WebLocationCollection([WebLocation(web, reg, lgc)])

        '''
