from ..data.match import Match

class Coliseum():
    MATCH_COUNT = 256
    DATA_START_ADDR = 0x1fb600

    def __init__(self, rom, args, enemies, items):
        self.rom = rom
        self.args = args
        self.enemies = enemies
        self.items = items

        self.read()

    def read(self):
        self.matches = []
        for match_index in range(self.MATCH_COUNT):
            match_data_start = self.DATA_START_ADDR + match_index * Match.DATA_SIZE
            match_data = self.rom.get_bytes(match_data_start, Match.DATA_SIZE)

            new_match = Match(match_data)
            self.matches.append(new_match)

    def shuffle_opponents(self):
        opponents = []
        for match in self.matches:
            opponents.append(match.opponent)
        import random
        random.shuffle(opponents)
        for match_index, match in enumerate(self.matches):
            match.opponent = opponents[match_index]

    def randomize_opponents(self, random_opponent_percent = None):
        import random

        for match in self.matches:
            match.opponent = self.enemies.get_random() if random_opponent_percent is not None and (random.random() < random_opponent_percent) else match.opponent

    def shuffle_rewards(self):
        rewards = []
        for match in self.matches:
            rewards.append(match.reward)

        import random
        random.shuffle(rewards)
        for match_index, match in enumerate(self.matches):
            match.reward = rewards[match_index]

    def randomize_rewards(self, random_reward_percent = None):
        import random

        for match in self.matches:
            match.reward = self.items.get_random() if random_reward_percent is not None and (random.random() < random_reward_percent) else match.reward
            while match.reward == 231: # no ArchplgoItems allowed
                match.reward = self.items.get_random()

    def remove_excluded_items(self):
        import random

        exclude = self.items.get_excluded()
        if self.args.coliseum_no_exp_eggs:
            exclude.append(self.items.get_id("Exp. Egg"))
        if self.args.coliseum_no_illuminas:
            exclude.append(self.items.get_id("Illumina"))

        possible_items = self.items.get_items(exclude)

        for match in self.matches:
            if match.reward in exclude:
                match.reward = random.choice(possible_items)

    def randomize_rewards_hidden(self):
        for match in self.matches:
            match.reward_hidden = 0

        import random
        number_visible = random.randint(self.args.coliseum_rewards_visible_random_min,
                                        self.args.coliseum_rewards_visible_random_max)
        number_hidden = self.items.ITEM_COUNT - number_visible - 1
        hidden_indices = random.sample(range(self.items.ITEM_COUNT - 1), number_hidden)
        for match_index in hidden_indices:
            self.matches[match_index].reward_hidden = 1

    def mod(self):
        if self.args.coliseum_opponents_random:
            self.randomize_opponents(self.args.coliseum_opponents_random / 100.0)
        elif self.args.coliseum_opponents_shuffle_random:
            self.shuffle_opponents()
            self.randomize_opponents(self.args.coliseum_opponents_shuffle_random / 100.0)

        if self.args.coliseum_rewards_random:
            self.randomize_rewards(self.args.coliseum_rewards_random / 100.0)
        elif self.args.coliseum_rewards_shuffle_random:
            self.shuffle_rewards()
            self.randomize_rewards(self.args.coliseum_rewards_shuffle_random / 100.0)

        self.remove_excluded_items()

        if self.args.coliseum_rewards_visible_random:
            self.randomize_rewards_hidden()

    def log(self):
        from ..log import section
        section("Coliseum", self.formatted_rows(), [])

    def print(self):
        rows = self.formatted_rows()
        for row in rows:
            print(row)

    def formatted_rows(self):
        row_width = 120
        col_width = row_width // 3

        rows = []
        for match_index, match in enumerate(self.matches):
            wager_name = self.items.get_name(match_index)
            opponent_name = self.enemies.get_name(match.opponent)
            reward_name = self.items.get_name(match.reward)
            reward_name += '*' if match.reward_hidden else ' '

            if match_index % 2:
                rows.append(f"{wager_name:-<{col_width}}{opponent_name:-^{col_width}}{reward_name:->{col_width}}")
            else:
                rows.append(f"{wager_name:<{col_width}}{opponent_name:^{col_width}}{reward_name:>{col_width}}")
        rows.append("")
        rows.append("* = Hidden Reward")
        return rows

    def write(self):
        if self.args.spoiler_log:
            self.log()

        for match_index, match in enumerate(self.matches):
            match_data = match.data()
            match_data_start = self.DATA_START_ADDR + match_index * Match.DATA_SIZE
            self.rom.set_bytes(match_data_start, match_data)
