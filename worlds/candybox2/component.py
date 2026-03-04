import re
import webbrowser

from worlds.LauncherComponents import Component, Type, components


def open_page(url):
    # Extract slot, pass, host, and port from the URL
    # URL format: archipelago://slot:pass@host:port
    match = re.match(r"archipelago://([^:]+):([^@]+)@([^:]+):(\d+)", url)
    if not match:
        raise ValueError("Invalid URL format")

    slot, password, host, port = match.groups()
    if password == "None":
        webbrowser.open(f"https://candybox2-ap.vicr123.com/latest?hostport={host}:{port}&name={slot}")
    else:
        webbrowser.open(
            f"https://candybox2-ap.vicr123.com/latest?hostport={host}:{port}&name={slot}&password={password}"
        )


def setup_candy_box_2_component():
    components.append(
        Component("Candy Box 2", func=open_page, component_type=Type.HIDDEN, supports_uri=True, game_name="Candy Box 2")
    )
