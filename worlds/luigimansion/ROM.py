
# import

# Need to extract and modify jmp tables to assign items spawns
# For furnitureinfo items  (interactables & plants), specify entry number in itemappeartable to spawn object. Will need to expand item appear table
# the above does include some base checks
# For chest items, edit treasuretable with either money amounts or specific key/mario item/element in other slot, by room. Only one true chest per room
# Must expand iteminfotable for use with treasuretable. treasuretable references iteminfotable
# Portrait Ghosts, toads and Boos unsure
# Blue Ghost and Gold Mice also use iteminfortable. Must add "other" field to jmp table
# need to add AP type checks to table somehow and trigger the item send
#
#
