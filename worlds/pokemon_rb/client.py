from NetUtils import ClientStatus
from worlds._bizhawk.client import BizHawkClient
from worlds._bizhawk import read


class PokemonRBClient(BizHawkClient):
    system = "GB"
    game = "Pokemon Red and Blue"

    async def validate_rom(self, ctx):
        game_name = await read(ctx, [(0x134, 8, "ROM")])
        game_name = game_name[0].decode("ascii")
        if game_name == "POKEMON ":
            ctx.game = self.game
            ctx.items_handling = 0b001
            return True
        return False

    async def set_auth(self, ctx):
        player_name = await read(ctx, [(0xFFF0, 0x10, "ROM")])
        seed_name = await read(ctx, [(0xFFDB, 21, "ROM")])
        ctx.auth = player_name

    async def game_watcher(self, ctx):
        pass
