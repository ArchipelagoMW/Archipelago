from gclib.gcm import GCM
from gclib.rarc import RARC
from gclib.yaz0_yay0 import Yay0

def update_game_usa(given_gcm: GCM) -> GCM:
    obake_copy = __get_arc(given_gcm, "files/model/obake01.szp")
    game_usa_edit = __get_arc(given_gcm, "files/Game/game_usa.szp")

    # Delete unused skybox
    vrbox_data = next(sub_file for sub_file in next(game_usa_nodes for game_usa_nodes in game_usa_edit.nodes if
        game_usa_nodes.name == "iwamoto").files if sub_file.name == "vrbox")
    game_usa_edit.delete_directory(vrbox_data)

    # Delete unused window
    unused_window = next(sub_file for sub_file in (next(sub_folder for sub_folder in next(game_usa_nodes for
        game_usa_nodes in game_usa_edit.nodes if game_usa_nodes.name == "kawano").files if
        sub_folder.name == "dmman").node.files) if sub_file.name == "m_window3.bti")
    game_usa_edit.delete_file(unused_window)

    # Delete unused image file
    unused_image = next(sub_file for sub_file in (next(sub_folder for sub_folder in next(game_usa_nodes for
        game_usa_nodes in game_usa_edit.nodes if game_usa_nodes.name == "kawano").files if
        sub_folder.name == "base").node.files) if sub_file.name == "cgbk_v.tim")
    game_usa_edit.delete_file(unused_image)

    # Delete unused param files
    unused_params = list(sub_file for sub_file in (next(sub_folder for sub_folder in next(game_usa_nodes for
        game_usa_nodes in game_usa_edit.nodes if game_usa_nodes.name == "param").files if
        sub_folder.name == "ctp").node.files) if sub_file.name.startswith("iyapoo2") and sub_file.name
        not in ["iyapoo2.prm", 'iyapoo20.prm'])
    for prm_file in unused_params:
        game_usa_edit.delete_file(prm_file)

    # Delete second unused image file
    unused_second_image = next(sub_folder for sub_folder in next(game_usa_nodes for
        game_usa_nodes in game_usa_edit.nodes if game_usa_nodes.name == "kt_static").files if
        sub_folder.name == "test.bti")
    game_usa_edit.delete_file(unused_second_image)

    # Delete second unused image file
    unused_model = next(sub_folder for sub_folder in next(game_usa_nodes for game_usa_nodes in game_usa_edit.nodes if
        game_usa_nodes.name == "model").files if sub_folder.name == "takara1.arc")
    game_usa_edit.delete_file(unused_model)

    game_usa_edit.add_new_file("obake01.arc", obake_copy.data, next((game_usa_nodes for
         game_usa_nodes in game_usa_edit.nodes if game_usa_nodes.name == "model")))

    given_gcm.delete_file(given_gcm.files_by_path["files/Game/game_usa.szp"])
    given_gcm.add_new_file("files/Game/game_usa.szp", game_usa_edit)
    game_usa_edit.save_changes()
    given_gcm.changed_files["files/Game/game_usa.szp"] = Yay0.compress(game_usa_edit.data)
    return given_gcm

def __get_arc(gcm, arc_path) -> RARC:
    arc_path = arc_path.replace("\\", "/")
    data = gcm.read_file_data(arc_path)
    arc = RARC(data)  # Automatically decompresses Yay0
    arc.read()
    return arc