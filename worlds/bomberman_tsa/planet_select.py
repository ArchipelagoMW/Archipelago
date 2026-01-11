def get_planet_selection(planets_have):
    
    def has_positive(lst):
        return any(x > 0 for x in lst)
        
    def contains_negative(lst):
        for num in lst:
            if num < 0:
                return True
        return False
        
    def get_lowest_negative(lst):
        negatives = [num for num in lst if num < 0]
        if negatives:
            return max(negatives)
        else:
            return None
    Planet_coords = {
        0x1C30010:  [194,395,0], # 0 Alcatraz
        0x1C30011:  [85,305,1], # 1 Aquanet
        0x1C30012:  [385,370,2], # 2 Horizon
        0x1C30013:  [125,165,3], # 3 Starlight
        0x1C30014:  [525,235,4], # 4 Neverland
        0x1C30015:  [260,120,5], # 5 Epikyur
        0x1C30016:  [480,135,6], # 6 Thantos
        0x1C30017:  [340,240,7], # 7 Noah
    }
    
    #planets_have = ["Alcatraz","Thantos","Starlight"]

    Stage_Sel = [
        0x00,0x00,0x00,0x78, 0x00,0x00,0x00,0xC0, 0xFF,0xFF,0xFF,0xFF, 0xFF,0xFF,0xFF,0xFF, 0xFF,0xFF,0xFF,0xFF, 0xFF,0xFF,0xFF,0xFF, 0x00,0x00,0x00,0x00, # 0
        0x00,0x00,0x00,0x20, 0x00,0x00,0x00,0xB0, 0xFF,0xFF,0xFF,0xFF, 0xFF,0xFF,0xFF,0xFF, 0xFF,0xFF,0xFF,0xFF, 0xFF,0xFF,0xFF,0xFF, 0x00,0x00,0x00,0x00, # 1
        0x00,0x00,0x00,0xD0, 0x00,0x00,0x00,0xC8, 0xFF,0xFF,0xFF,0xFF, 0xFF,0xFF,0xFF,0xFF, 0xFF,0xFF,0xFF,0xFF, 0xFF,0xFF,0xFF,0xFF, 0x00,0x00,0x00,0x00, # 2
        0x00,0x00,0x00,0x28, 0x00,0x00,0x00,0x40, 0xFF,0xFF,0xFF,0xFF, 0xFF,0xFF,0xFF,0xFF, 0xFF,0xFF,0xFF,0xFF, 0xFF,0xFF,0xFF,0xFF, 0x00,0x00,0x00,0x00, # 3
        0x00,0x00,0x00,0xF8, 0x00,0x00,0x00,0x70, 0xFF,0xFF,0xFF,0xFF, 0xFF,0xFF,0xFF,0xFF, 0xFF,0xFF,0xFF,0xFF, 0xFF,0xFF,0xFF,0xFF, 0x00,0x00,0x00,0x00, # 4
        0x00,0x00,0x00,0x70, 0x00,0x00,0x00,0x30, 0xFF,0xFF,0xFF,0xFF, 0xFF,0xFF,0xFF,0xFF, 0xFF,0xFF,0xFF,0xFF, 0xFF,0xFF,0xFF,0xFF, 0x00,0x00,0x00,0x00, # 5
        0x00,0x00,0x00,0xF8, 0x00,0x00,0x00,0x40, 0xFF,0xFF,0xFF,0xFF, 0xFF,0xFF,0xFF,0xFF, 0xFF,0xFF,0xFF,0xFF, 0xFF,0xFF,0xFF,0xFF, 0x00,0x00,0x00,0x00, # 6
        0x00,0x00,0x00,0xA8, 0x00,0x00,0x00,0x50, 0xFF,0xFF,0xFF,0xFF, 0xFF,0xFF,0xFF,0xFF, 0xFF,0xFF,0xFF,0xFF, 0xFF,0xFF,0xFF,0xFF, 0x00,0x00,0x00,0x00, # 7
    ]
    
    
    for planet in planets_have:
        src_x = Planet_coords[planet][0]
        src_y = Planet_coords[planet][1]
        src_idx = Planet_coords[planet][2]
        dist = []
        connections = []
        dist_x = []
        dist_y = []
        dist_id = []
        for planets_coord_name, coord_array in Planet_coords.items():
            if planets_coord_name in planets_have and (planets_coord_name != planet):
                dest_x = coord_array[0]
                dest_y = coord_array[1]
                dest_idx = coord_array[2]
                dif_x = src_x - dest_x
                dif_y = src_y - dest_y
                dist_x.append(dif_x)
                dist_y.append(dif_y)
                dist_id.append(dest_idx)
        
        min_u = 9
        min_d = 9
        min_l = 9
        min_r = 9

            
        if has_positive(dist_y):
            min_u= dist_y.index(min(y for y in dist_y if y > 0))
        if contains_negative(dist_y):
            min_d= dist_y.index(get_lowest_negative(dist_y))

        if has_positive(dist_x):
            min_l= dist_x.index(min(x for x in dist_x if x > 0))
        if contains_negative(dist_x):
            min_r = dist_x.index(get_lowest_negative(dist_x))
        #print(min_x,dist_id[min_x], min_y, dist_id[min_y])
        
        offset_base = (src_idx * 0x1C) + (0x08)
        for i in range(3):
            if min_u < 9:
                Stage_Sel[offset_base+(i+0x00)] = 0x00  # Up
            if min_d < 9:
                Stage_Sel[offset_base+(i+0x04)] = 0x00  # Down
            if min_l < 9:
                Stage_Sel[offset_base+(i+0x08)] = 0x00  # Left
            if min_r < 9:
                Stage_Sel[offset_base+(i+0x0C)] = 0x00  # Right
        
        if min_u < 9:
            Stage_Sel[offset_base+0x00+3] = dist_id[min_u]
        if min_d < 9:
            Stage_Sel[offset_base+0x04+3] = dist_id[min_d]
        if min_l < 9:
            Stage_Sel[offset_base+0x08+3] = dist_id[min_l]
        if min_r < 9:
            Stage_Sel[offset_base+0x0C+3] = dist_id[min_r]

    return bytes(Stage_Sel)
#print(list(map(hex, Stage_Sel)))

def highlight_planets(planets_have,stageflags,bossflags,select):
    result = {}
    Planet_items = [
        0x1C30010, # 0 Alcatraz
        0x1C30011, # 1 Aquanet
        0x1C30012, # 2 Horizon
        0x1C30013, # 3 Starlight
        0x1C30014, # 4 Neverland
        0x1C30015, # 5 Epikyur
        0x1C30016, # 6 Thantos
        0x1C30017, # 7 Noah
    ]
    planet_offsets = [
        0xB5694, # Alcatraz
        0xB56EC, # Aquanet
        0xB5744, # Horizon
        0xB579C, # Starlight
        0xB57F4, # Neverland
        0xB584C, # Epikyur
        0xB58A4, # Thantos
        0xB58FC, # Noah
        ]
    for idx in range(len(planet_offsets)):
        if idx == select:
            base_display = 0xFFFFFFFF
        elif Planet_items[idx] in planets_have:
            mask = 1 << idx
            stageclear = stageflags & mask
            bossclear = bossflags & mask
            base_display = 0x808080FF
            if bossclear:
                base_display | 0xE0000000
            if stageclear:
                base_display | 0x0000E000
            if bossclear and stageclear:
                base_display = 0xE0E0E0FF
        else:
            base_display = 0x40404040
        result[planet_offsets[idx]]  = base_display
    return result