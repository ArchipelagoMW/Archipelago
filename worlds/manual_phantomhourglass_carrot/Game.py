from .Data import game_table

if 'creator' in game_table:
    game_table['player'] = game_table['creator']

game_name = "Manual_%s_%s" % (game_table["game"], game_table["player"])
filler_item_name = game_table["filler_item_name"] if "filler_item_name" in game_table else "Filler"
starting_items = game_table["starting_items"] if "starting_items" in game_table else None

if "starting_index" in game_table:
    try:
        starting_index = int(game_table["starting_index"])
    except ValueError:
        raise Exception("The value of data/game.json:'starting_index' should be an int")
else:
    starting_index = 1
