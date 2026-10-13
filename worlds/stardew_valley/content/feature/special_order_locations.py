def get_qi_gem_amount(item_name: str) -> int:
    amount = item_name.replace(" Qi Gems", "")
    if amount.isdigit():
        return int(amount)
    return 0
