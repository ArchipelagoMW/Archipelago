from typing import List, Tuple

from kvui import GameManager

from kivy.lang import Builder

from kivy.uix.layout import Layout
from kivy.uix.widget import Widget

# Debugging
# from kivy.core.window import Window
# from kivy.modules import inspector

from ..client import KeymastersKeepContext

from .client_gui_layouts import KeymastersKeepTabLayout, ShopsTabLayout, TrialsTabLayout, TrialsCompletedTabLayout

from ..world import KeymastersKeepWorld


unicode_font_name: str = KeymastersKeepWorld.settings.client_unicode_font_name or "Roboto"
unicode_font_size: int = KeymastersKeepWorld.settings.client_unicode_font_size or 15

Builder.load_string(
    f"""
<TrialLabel>
    font_name: '{unicode_font_name}'
    font_size: '{unicode_font_size}dp'
    markup: True
    """
)


class KeymastersKeepManager(GameManager):
    ctx: KeymastersKeepContext

    logging_pairs: List[Tuple[str, str]] = [("Client", "Archipelago")]
    base_title: str = "Archipelago Keymaster's Keep Client"

    keymasters_keep_tab_layout: KeymastersKeepTabLayout
    trials_tab_layout: TrialsTabLayout
    trials_completed_tab_layout: TrialsCompletedTabLayout
    shops_tab_layout: ShopsTabLayout

    keymasters_keep_tab: Widget
    available_trials_tab: Widget
    completed_trials_tab: Widget
    shops_tab: Widget

    def build(self) -> Layout:
        container: Layout = super().build()

        self.keymasters_keep_tab_layout = KeymastersKeepTabLayout(self.ctx)
        self.keymasters_keep_tab = self.add_client_tab("Keymaster's Keep", self.keymasters_keep_tab_layout)

        self.trials_tab_layout = TrialsTabLayout(self.ctx)
        self.available_trials_tab = self.add_client_tab("Available Trials", self.trials_tab_layout)

        self.trials_completed_tab_layout = TrialsCompletedTabLayout(self.ctx)
        self.completed_trials_tab = self.add_client_tab("Completed Trials", self.trials_completed_tab_layout)

        self.shops_tab_layout = ShopsTabLayout(self.ctx)
        self.shops_tab = self.add_client_tab("Shops", self.shops_tab_layout)

        # Debugging
        # inspector.create_inspector(Window, container)

        return container

    def update_tabs(self) -> None:
        self.keymasters_keep_tab_layout.update()
        self.trials_tab_layout.update()
        self.trials_completed_tab_layout.update()
        self.shops_tab_layout.update()
