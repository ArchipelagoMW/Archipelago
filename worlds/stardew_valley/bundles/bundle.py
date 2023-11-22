from typing import List

from worlds.stardew_valley.bundles.bundle_item import BundleItem


class Bundle:
    room: str
    name: str
    items: List[BundleItem]
    number_required: int

    def __init__(self, key: str, value: str):
        key_parts = key.split("/")
        self.room = key_parts[0]
        self.sprite = key_parts[1]

        value_parts = value.split("/")
        self.original_name = value_parts[0]
        self.name = value_parts[0]
        self.rewards = self.parse_stardew_objects(value_parts[1])
        self.requirements = self.parse_stardew_bundle_items(value_parts[2])
        self.color = value_parts[3]
        if len(value_parts) > 4:
            self.number_required = int(value_parts[4])
        else:
            self.number_required = len(self.requirements)

    def __repr__(self):
        return f"{self.original_name} -> {repr(self.requirements)}"

    def get_name_with_bundle(self) -> str:
        return f"{self.original_name} Bundle"

    def to_pair(self) -> (str, str):
        key = f"{self.room}/{self.sprite}"
        str_rewards = ""
        for reward in self.rewards:
            str_rewards += f" {reward}"
        str_rewards = str_rewards.strip()
        str_requirements = ""
        for requirement in self.requirements:
            str_requirements += f" {requirement.item.item_id} {requirement.amount} {requirement.quality}"
        str_requirements = str_requirements.strip()
        value = f"{self.name}/{str_rewards}/{str_requirements}/{self.color}/{self.number_required}"
        return key, value

    def remove_rewards(self):
        self.rewards = []

    def change_number_required(self, difference: int):
        self.number_required = min(len(self.requirements), max(1, self.number_required + difference))
        if len(self.requirements) == 1 and self.requirements[0].item.item_id == -1:
            one_fifth = self.requirements[0].amount / 5
            new_amount = int(self.requirements[0].amount + (difference * one_fifth))
            self.requirements[0] = BundleItem.money_bundle(new_amount)
            thousand_amount = int(new_amount / 1000)
            dollar_amount = str(new_amount % 1000)
            while len(dollar_amount) < 3:
                dollar_amount = f"0{dollar_amount}"
            self.name = f"{thousand_amount},{dollar_amount}g"

    def randomize_requirements(self, random: Random,
                               potential_requirements: Union[List[BundleItem], List[List[BundleItem]]]):
        if not potential_requirements:
            return

        number_to_generate = len(self.requirements)
        self.requirements.clear()
        if number_to_generate > len(potential_requirements):
            choices: Union[BundleItem, List[BundleItem]] = random.choices(potential_requirements, k=number_to_generate)
        else:
            choices: Union[BundleItem, List[BundleItem]] = random.sample(potential_requirements, number_to_generate)
        for choice in choices:
            if isinstance(choice, BundleItem):
                self.requirements.append(choice)
            else:
                self.requirements.append(random.choice(choice))

    def assign_requirements(self, new_requirements: List[BundleItem]) -> List[BundleItem]:
        number_to_generate = len(self.requirements)
        self.requirements.clear()
        for requirement in new_requirements:
            self.requirements.append(requirement)
            if len(self.requirements) >= number_to_generate:
                return new_requirements[number_to_generate:]

    @staticmethod
    def parse_stardew_objects(string_objects: str) -> List[str]:
        objects = []
        if len(string_objects) < 5:
            return objects
        rewards_parts = string_objects.split(" ")
        for index in range(0, len(rewards_parts), 3):
            objects.append(f"{rewards_parts[index]} {rewards_parts[index + 1]} {rewards_parts[index + 2]}")
        return objects

    @staticmethod
    def parse_stardew_bundle_items(string_objects: str) -> List[BundleItem]:
        bundle_items = []
        parts = string_objects.split(" ")
        for index in range(0, len(parts), 3):
            item_id = int(parts[index])
            bundle_item = BundleItem(all_bundle_items_by_id[item_id].item,
                                     int(parts[index + 1]),
                                     int(parts[index + 2]))
            bundle_items.append(bundle_item)
        return bundle_items

    # Shuffling the Vault doesn't really work with the stardew system in place
    # shuffle_vault_amongst_themselves(random, bundles)