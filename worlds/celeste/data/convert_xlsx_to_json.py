from pathlib import Path

import pandas as pd


def main():
    input_path = Path(__file__, "..", "items.xlsx")
    output_item_path = Path(__file__, "..", "items.json")
    output_region_path = Path(__file__, "..", "regions.json")

    df = pd.read_excel(input_path, sheet_name="items", na_filter=False)
    df.to_json(output_item_path, orient="records")

    df = pd.read_excel(input_path, sheet_name="regions", na_filter=False)
    df.to_json(output_region_path, orient="records")


if __name__ == "__main__":
    main()
