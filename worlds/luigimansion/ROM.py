
# import

# Need to extract and modify jmp tables to assign items spawns
# For furnitureinfo items  (interactables & plants), specify entry number in itemappeartable to spawn object. Will need to expand item appear table
# the above does include some base checks
# For chest items, edit treasuretable with either money amounts or specific key/mario item/element in other slot, by room. Only one true chest per room
# Must expand iteminfotable for use with treasuretable. treasuretable references iteminfotable
# Portrait Ghosts, toads and Boos unsure
# Blue Ghost and Gold Mice also use iteminfortable. Must add "other" field to jmp iyapootable. (iyapoo are the money ghosts)
# need to add AP type checks to table somehow and trigger the item send
# Need way to unpack and then edit jump tables automatically.
# Need a way to add a custom item type that, when acquired, triggers the client to send an item
# Need to adjust location names and items names to match code in game.
# Need methods to give items to Luigi in game
# How are keys/items/money stored once received??? How do they get committed to memory?
