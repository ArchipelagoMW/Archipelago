# DishonoredClient.py
import os
import sys

# Fix pour les imports Archipelago
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import asyncio
from CommonClient import CommonContext, server_loop, gui_enabled
from client_memory import MemoryHandler
from client_locations import GAME_CHECKS

class DishonoredContext(CommonContext):
    game = "Dishonored"
    items_handling = 0b111

    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.memory = MemoryHandler("Dishonored.exe")


async def game_watcher(ctx: DishonoredContext):
    """Boucle principale qui vérifie la mémoire et communique avec AP."""
    print("[LOG] Surveillance de la mémoire démarrée.")

    while not ctx.exit_event.is_set():
        # 1. Gestion de la reconnexion au jeu
        if not ctx.memory.is_connected():
            if ctx.memory.connect():
                print("[PYMEM] Connecté à Dishonored.exe !")
            else:
                await asyncio.sleep(2.0)
                continue

        # 2. Parcours des checks
        locations_to_send = []

        for check in GAME_CHECKS:
            # On ignore les checks déjà validés sur le serveur
            if check.id in ctx.checked_locations:
                continue

            try:
                # Lecture via notre module mémoire
                value = ctx.memory.read_pointer_chain(check.static_offset, check.offsets)

                # Validation
                if check.condition(value):
                    print(f"[CHECK] {check.name} validé ! (Valeur: {value})")
                    locations_to_send.append(check.id)

            except Exception:
                # Gestion des erreurs de lecture lors des écrans de chargement
                pass

        # 3. Envoi au serveur AP
        if locations_to_send:
            await ctx.send_msgs([{"cmd": "LocationChecks", "locations": locations_to_send}])

        await asyncio.sleep(0.5)


async def main():
    ctx = DishonoredContext("localhost:38281", "")
    ctx.server_task = asyncio.create_task(server_loop(ctx))
    asyncio.create_task(game_watcher(ctx))
    
    if gui_enabled:
        ctx.run_gui()
    
    await ctx.exit_event.wait()

if __name__ == "__main__":
    asyncio.run(main())