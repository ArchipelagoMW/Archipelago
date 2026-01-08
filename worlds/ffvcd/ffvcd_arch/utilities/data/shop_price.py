resell_dict = {
    "HALF": "0",
    "5": "4",
    "1": "8"
    }
NUM_SHOP_PRICES = 768

class ShopPrice:
    def __init__(self, index, collectible_manager, data_manager):
        self.idx = index
        self.generate_from_data(data_manager.files['shopprices'])
        '''
        self.address
        self.shop_type (00 for magic, 03 for item, 07 for crystal/ability)
        self.id (hex byte)
        self.content_name (reward name)
        self.price (two hexbytes concatenated)
        self.resell_byte (first byte of price)
        self.price_byte (second byte of price)
        self.int_price (human readable price)
        self.resell (HALF, 5 or 1)
        '''
        self.resell = str(self.resell)
        self.collectible = collectible_manager.get_by_name(self.content_name)

    @property
    def asar_output(self):
        return f"org ${self.address}\ndb ${self.resell_byte}, ${self.price_byte}"

    @property
    def short_output(self):
        if self.shop_type == '03':
            resell = self.resell
        else:
            resell = "NOSELL"
        return f"{self.content_name} costs {self.int_price} and resells for {resell}"

    def generate_from_data(self, data):
        
        if self.idx in data.keys():
            s = data[self.idx]
            for k, v in s.items():
                setattr(self,k,v)
        else:
            print("No match on index found for Shop prices %s" % self.idx)



class ShopPriceManager:
    def __init__(self, collectible_manager, data_manager):
        self.shopprices = [ShopPrice(x, collectible_manager, data_manager) for x in range(1, NUM_SHOP_PRICES)]

    def get_patch(self):
        output = ';===========\n'
        output = output + ';shop prices\n'
        output = output + ';===========\n'
        for i in self.shopprices:
            output = output + i.asar_output + '\n'
        
        return output

    def get_spoiler(self):
        output = '-----SHOP PRICES-----\n'
        for i in self.shopprices:
            output = output + i.short_output + '\n'
        output = output + '-----***********-----'

        return output