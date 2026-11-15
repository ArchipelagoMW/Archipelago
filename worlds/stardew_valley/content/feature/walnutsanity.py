def get_walnut_amount(item_name: str) -> int:
    if item_name == "Golden Walnut":
        return 1
    if item_name == "3 Golden Walnuts":
        return 3
    if item_name == "5 Golden Walnuts":
        return 5
    return 0
