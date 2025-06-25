import io
from pathlib import Path
from .common import parse_string


item_dt_headers = [
    "item_id",
    "item_type",
    "item_restriction",
    "item_icon",
    "item_subtype",
    "item_eff_1",
    "item_eff_2",
    "item_eff_3",
    "item_target_type",
    "item_rng",
    "item_aoe_size",
    "item_str",
    "item_def",
    "item_ats",
    "item_adf",
    "item_agi",
    "item_dex",
    "item_spd",
    "item_mov",
    "item_limit",
    "item_price",
]


def parse_item_table(dt_path: Path, text_path: Path):
    items = list()
    items_text = list()
    with open(dt_path, "rb") as item_dt_file:
        idx_end = int.from_bytes(item_dt_file.read(2), "little")
        item_idxes = list()
        item_dt_file.seek(0)

        while item_dt_file.tell() != idx_end:
            item_idxes.append(int.from_bytes(item_dt_file.read(2), "little"))

        for idx in item_idxes:
            item_dt_file.seek(idx)

            item = dict()

            item["item_id"] = int.from_bytes(item_dt_file.read(2), "little")
            item["item_type"] = int.from_bytes(item_dt_file.read(1), "little")
            item["item_restriction"] = int.from_bytes(item_dt_file.read(1), "little")
            item["item_icon"] = int.from_bytes(item_dt_file.read(1), "little")
            item["item_subtype"] = int.from_bytes(item_dt_file.read(1), "little")
            item["item_eff_1"] = int.from_bytes(item_dt_file.read(1), "little")
            item["item_eff_2"] = int.from_bytes(item_dt_file.read(1), "little")
            item["item_eff_3"] = int.from_bytes(item_dt_file.read(1), "little")
            item["item_target_type"] = int.from_bytes(item_dt_file.read(1), "little")

            item["item_rng"] = int.from_bytes(item_dt_file.read(2), "little", signed=True)
            item["item_aoe_size"] = int.from_bytes(item_dt_file.read(2), "little", signed=True)
            item["item_str"] = int.from_bytes(item_dt_file.read(2), "little", signed=True)
            item["item_def"] = int.from_bytes(item_dt_file.read(2), "little", signed=True)
            item["item_ats"] = int.from_bytes(item_dt_file.read(2), "little", signed=True)
            item["item_adf"] = int.from_bytes(item_dt_file.read(2), "little", signed=True)
            item["item_agi"] = int.from_bytes(item_dt_file.read(2), "little", signed=True)
            item["item_dex"] = int.from_bytes(item_dt_file.read(2), "little", signed=True)
            item["item_mov"] = int.from_bytes(item_dt_file.read(2), "little", signed=True)
            item["item_spd"] = int.from_bytes(item_dt_file.read(2), "little", signed=True)

            item["item_limit"] = int.from_bytes(item_dt_file.read(2), "little")
            item["item_price"] = int.from_bytes(item_dt_file.read(4), "little")

            items.append(item)

    with open(text_path, "rb") as ittxt_file:
        idx_end = int.from_bytes(ittxt_file.read(2), "little")
        item_idxes = list()
        ittxt_file.seek(0)

        while ittxt_file.tell() != idx_end:
            item_idxes.append(int.from_bytes(ittxt_file.read(2), "little"))

        for idx in item_idxes:
            ittxt_file.seek(idx)
            item_text = dict()
            item_text["item_id"] = int.from_bytes(ittxt_file.read(2), "little")
            ittxt_file.read(2)

            name_idx = int.from_bytes(ittxt_file.read(2), "little")
            desc_idx = int.from_bytes(ittxt_file.read(2), "little")

            ittxt_file.seek(name_idx)
            item_text["item_name"] = parse_string(ittxt_file)

            ittxt_file.seek(desc_idx)
            item_text["item_desc"] = parse_string(ittxt_file)

            items_text.append(item_text)

    return items, items_text


def write_item_table(output_path: Path, item_table: list):
    item_count = len(item_table)

    item_header_length = 2 * item_count

    item_header_stream = io.BytesIO()
    item_data_stream = io.BytesIO()

    for item in item_table:
        item_header_stream.write(int.to_bytes(item_header_length + item_data_stream.tell(), 2, "little"))

        item_data_stream.write(int.to_bytes(item["item_id"], 2, "little"))
        item_data_stream.write(int.to_bytes(item["item_type"], 1, "little"))
        item_data_stream.write(int.to_bytes(item["item_restriction"], 1, "little"))
        item_data_stream.write(int.to_bytes(item["item_icon"], 1, "little"))
        item_data_stream.write(int.to_bytes(item["item_subtype"], 1, "little"))
        item_data_stream.write(int.to_bytes(item["item_eff_1"], 1, "little"))
        item_data_stream.write(int.to_bytes(item["item_eff_2"], 1, "little"))
        item_data_stream.write(int.to_bytes(item["item_eff_3"], 1, "little"))
        item_data_stream.write(int.to_bytes(item["item_target_type"], 1, "little"))

        item_data_stream.write(int.to_bytes(item["item_rng"], 2, "little", signed=True))
        item_data_stream.write(int.to_bytes(item["item_aoe_size"], 2, "little", signed=True))
        item_data_stream.write(int.to_bytes(item["item_str"], 2, "little", signed=True))
        item_data_stream.write(int.to_bytes(item["item_def"], 2, "little", signed=True))
        item_data_stream.write(int.to_bytes(item["item_ats"], 2, "little", signed=True))
        item_data_stream.write(int.to_bytes(item["item_adf"], 2, "little", signed=True))
        item_data_stream.write(int.to_bytes(item["item_agi"], 2, "little", signed=True))
        item_data_stream.write(int.to_bytes(item["item_dex"], 2, "little", signed=True))
        item_data_stream.write(int.to_bytes(item["item_mov"], 2, "little", signed=True))
        item_data_stream.write(int.to_bytes(item["item_spd"], 2, "little", signed=True))

        item_data_stream.write(int.to_bytes(item["item_limit"], 2, "little"))
        item_data_stream.write(int.to_bytes(item["item_price"], 4, "little"))

    with open(output_path, "wb") as item_table_file:
        item_header_stream.seek(0)
        item_data_stream.seek(0)

        item_table_file.write(item_header_stream.read())
        item_table_file.write(item_data_stream.read())


def write_item_text_table(output_path: Path, item_text_table: list):
    item_count = len(item_text_table)

    item_header_length = 2 * item_count

    item_header_stream = io.BytesIO()
    item_data_stream = io.BytesIO()

    for item in item_text_table:
        item_header_stream.write(int.to_bytes(item_header_length + item_data_stream.tell(), 2, "little"))

        item_data_stream.write(int.to_bytes(item["item_id"], 2, "little"))
        item_data_stream.write(b"\0\0")

        item_text_stream = io.BytesIO()

        item_data_stream.write(int.to_bytes(item_header_length + item_data_stream.tell() + 4, 2, "little"))
        item_text_stream.write(item["item_name"].encode("shift-jis"))
        item_text_stream.write(b"\0")

        item_data_stream.write(int.to_bytes(item_header_length + item_data_stream.tell() + 2 + item_text_stream.tell(), 2, "little"))
        item_text_stream.write(item["item_desc"].encode("shift-jis"))
        item_text_stream.write(b"\0")

        item_text_stream.seek(0)
        item_data_stream.write(item_text_stream.read())

    with open(output_path, "wb") as item_text_file:
        item_header_stream.seek(0)
        item_data_stream.seek(0)

        item_text_file.write(item_header_stream.read())
        item_text_file.write(item_data_stream.read())


def create_non_local_item(item_id: int, item_name: str):
    item = dict()
    item_text = dict()
    item["item_id"] = item_id
    item["item_icon"] = 16
    item["item_limit"] = 1
    item_text["item_id"] = item_id
    item_text["item_name"] = item_name
    item_text["item_desc"] = ""

    for header in item_dt_headers:
        if header not in item:
            item[header] = 0

    return item, item_text
