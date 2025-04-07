from .base_logic import BaseLogicMixin, BaseLogic
from ..data.movies import movies_by_name, npc_snacks, Snack
from ..stardew_rule import StardewRule, Or


class MovieLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.movie = MovieLogic(*args, **kwargs)


class MovieLogic(BaseLogic):

    def can_watch_movie_with_loving_npc(self, movie_name: str) -> StardewRule:
        movie = movies_by_name[movie_name]
        return self.logic.relationship.can_meet_any(movie.loving_npcs)

    def can_watch_movie_with_loving_npc_and_snack(self, movie_name: str) -> StardewRule:
        movie = movies_by_name[movie_name]
        potential_partner_rules = []
        for npc in movie.loving_npcs:
            meet_rule = self.logic.relationship.can_meet(npc)
            snack_rule = self.can_buy_loved_snack(npc)
            potential_partner_rules.append(meet_rule & snack_rule)
        return Or(*potential_partner_rules)

    def can_buy_loved_snack(self, npc: str) -> StardewRule:
        snacks = npc_snacks[npc]
        snacks_rule = Or(*[self.can_buy_snack(snack) for snack in snacks])
        return snacks_rule

    def can_buy_snack(self, snack: Snack) -> StardewRule:
        return self.logic.received(snack.category)

    def can_buy_snack_for_someone_who_loves_it(self, snack: Snack) -> StardewRule:
        return self.logic.received(snack.category) & self.logic.relationship.can_meet_any(snack.loving_npcs)
