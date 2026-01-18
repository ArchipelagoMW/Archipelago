"""
Command tool for dev interaction.
"""
import asyncio
import os
import sys

AP_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.dirname(AP_DIR))

from worlds.tits_the_3rd.client.memory_io import TitsThe3rdMemoryIO

async def main():
    print("Command tool started. Type 'help' for commands or 'exit' to quit.")
    print("Enter commands:")

    exit_event = asyncio.Event()
    memory_io = TitsThe3rdMemoryIO(exit_event)
    await memory_io.connect()
    
    while True:
        try:
            command = input("> ").strip()

            if command.lower() == "help":
                print("Available commands:")
                print("  connect              - Reconnect to the game")
                print("  item <id> [amount]   - Give an item (amount defaults to 1)")
                print("  craft <char_id> <id> - Give a craft to a character")
                print("  flag <id> <0|1>      - Set a flag value")
                print("  exit                 - Exit the tool")

            elif command.lower() == "connect":
                memory_io = TitsThe3rdMemoryIO(exit_event)
                await memory_io.connect()

            elif command.lower().startswith("craft"):
                _, character_id, craft_id = command.split(" ")
                memory_io.give_craft(int(character_id), int(craft_id))

            elif command.lower().startswith("item"):
                parts = command.split(" ")
                item_id = int(parts[1])
                amount = int(parts[2]) if len(parts) > 2 else 1
                memory_io.give_item(item_id, amount)

            elif command.lower().startswith("flag"):
                _, flag_id, value = command.split(" ")
                memory_io.write_flag(int(flag_id), bool(int(value)))

            elif command.lower() == "exit":
                print("Exiting...")
                exit_event.set()
                break
            elif not command:
                continue
            else:
                print(f"Received command: {command}")
                # Add command handling logic here

        except KeyboardInterrupt:
            exit_event.set()
            print("\nReceived keyboard interrupt, exiting...")
            break
        except Exception as e:
            exit_event.set()
            print(f"Error processing command: {e}")

if __name__ == "__main__":
    asyncio.run(main())
