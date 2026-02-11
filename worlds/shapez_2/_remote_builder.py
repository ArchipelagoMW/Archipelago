
if __name__ == "__main__":
    from data.items import all_standard_items

    with open("docs/remote_items.md", "wt") as file:
        file.write("# List of all items and their remote names in shapez 2\n\n" +
                   "| Item name".ljust(41) + "| Remote name".ljust(41) + "|\n"
                   "|" + "-" * 40 + "|" + "-" * 40 + "|\n")
        for _map in all_standard_items.maps:
            for name, data in _map.items():
                file.write(f"| {name:39}| {data.remote_id:39}|\n")
