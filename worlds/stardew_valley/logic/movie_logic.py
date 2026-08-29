from .base_logic import BaseLogicMixin, BaseLogic
from ..data.movies import movies_by_name, npc_snacks, Snack, Movie, snacks_by_name
from ..stardew_rule import StardewRule, Or
from ..strings.villager_names import NPC


class MovieLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.movie = MovieLogic(*args, **kwargs)


class MovieLogic(BaseLogic):

    def can_watch_movie(self, movie: str | Movie) -> StardewRule:
        if isinstance(movie, str):
            movie = movies_by_name[movie]
        return self.logic.season.has(movie.season)

    def can_watch_movie_with_loving_npc(self, movie: str | Movie) -> StardewRule:
        if isinstance(movie, str):
            movie = movies_by_name[movie]
        return self.can_watch_movie(movie) & self.logic.relationship.can_meet_any(*movie.loving_npcs)

    def can_invite_to_movie(self, npcs: str | list[str]) -> StardewRule:
        if isinstance(npcs, str):
            npc = npcs
            if npc == NPC.leo:
                return self.logic.relationship.has_hearts(NPC.leo, 6)
            return self.logic.relationship.can_meet(npc)
        return self.logic.or_(*[self.can_invite_to_movie(npc) for npc in npcs])

    def can_watch_movie_with_loving_npc_and_snack(self, movie: str | Movie) -> StardewRule:
        if isinstance(movie, str):
            movie = movies_by_name[movie]
        potential_partner_rules = []
        for npc in movie.loving_npcs:
            meet_rule = self.can_invite_to_movie(npc)
            snack_rule = self.can_buy_loved_snack(npc)
            potential_partner_rules.append(meet_rule & snack_rule)
        return self.can_watch_movie(movie) & Or(*potential_partner_rules)

    def can_buy_loved_snack(self, npc: str) -> StardewRule:
        snacks = npc_snacks[npc]
        if not snacks:
            return self.logic.false_
        snacks_rule = Or(*[self.can_buy_snack(snack) for snack in snacks])
        return snacks_rule

    def can_buy_snack(self, snack: str | Snack) -> StardewRule:
        if isinstance(snack, str):
            snack = snacks_by_name[snack]
        return self.logic.received(snack.category)

    def can_buy_snack_for_someone_who_loves_it(self, snack: str | Snack) -> StardewRule:
        if isinstance(snack, str):
            snack = snacks_by_name[snack]
        return self.logic.received(snack.category) & self.can_invite_to_movie(snack.loving_npcs)
