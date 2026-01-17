
import io
import json
import math
import pkgutil
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, Triangle
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.image import Image, CoreImage
from kivy.uix.widget import Widget
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout

from NetUtils import NetworkItem
from kvui import HoverBehavior
from worlds.tboir.client import IsaacContext

class TrackerLayout(Widget):
    ctx: IsaacContext
            
    def load_image(self, filename):
        image_file_data = pkgutil.get_data(__name__, filename)
        if not image_file_data:
            raise FileNotFoundError(f"{__name__=} {filename=}")
        data = io.BytesIO(image_file_data)
        return Image(
            texture=CoreImage(data, ext="png").texture,
            fit_mode="contain"
        )

    def _force_tooltip(self, window, x, y, *args):
        self._update_tooltip(None, (x, Window.height-y))

    def _update_tooltip(self, window, pos):
        if not self.get_root_window():
            return  # Abort if not displayed
        for widget, tooltip in self.tooltips:
            if widget.collide_point(*widget.to_widget(*pos)):
                if self.active_tooltip != tooltip:
                    if self.active_tooltip:
                        self.remove_widget(self.active_tooltip)
                    self.add_widget(tooltip)
                    self.active_tooltip = tooltip
                    tooltip_pos = (widget.x + widget.tooltip_anchor, widget.y + widget.height / 2 - tooltip.height / 2)
                    x, y = self.to_widget(*widget.to_window(*tooltip_pos))
                    tooltip.pos = (min(max(0, x), self.width-tooltip.width), min(max(0, y), self.height-tooltip.height))
                    tooltip._update_pos()
                return
        if self.active_tooltip:
            self.remove_widget(self.active_tooltip)
            self.active_tooltip = None


    def on_connect(self, ctx):

        self.active_tooltip = None
        self.tooltips = []

        self.data = json.loads(pkgutil.get_data(__name__, "data.json").decode())
        self.bind(size=self._update_overlay, pos=self._update_overlay)
        Window.bind(mouse_pos=self._update_tooltip)
        Window.bind(on_mouse_down=self._force_tooltip)

        self.img = self.load_image('tracker/images/tracker.png')
        self.add_widget(self.img)
        self._update_overlay()

        self.items = {}
        self.unlocks = {}
        self.regions = {}
        self.tooltips = []
        self.locations = {}
        self.goals = {}
        self.ctx = ctx

        for locid in self.ctx.server_locations:
            location_name = self.ctx.location_names.lookup_in_slot(locid, self.ctx.slot)
            region_name = ""
            icon_name = ""
            if " - " in location_name:
                region_name = location_name.split(' - ')[0]
                icon_name = location_name.split(' - ')[1]
            elif " Reward " in location_name:
                region_name = location_name.split(' Reward ')[0]
                icon_name = "Reward"
            if "Item #" in location_name:
                icon_name = "ap_icon"
            if region_name not in self.regions:
                x = 0
                y = 0
                if region_name in self.data["regions"].keys():
                    x = self.data["regions"][region_name]["tracker_location"]["x"]
                    y = self.data["regions"][region_name]["tracker_location"]["y"]
                if region_name in self.data["boss_rewards"].keys():
                    x = self.data["boss_rewards"][region_name]["tracker_location"]["x"]
                    y = self.data["boss_rewards"][region_name]["tracker_location"]["y"]
                region = Region(ox=x, oy=y, osize=30)
                region.tooltip_anchor = 30
                self.img.add_widget(region)
                self.img.bind(size=region._update_graphics, pos=region._update_graphics)
                region._update_graphics()
                self.regions[region_name] = region
                tooltip = TrackerTooltip(padding=(8, 4), size_hint=(None, None), orientation="vertical")
                self.tooltips.append((region, tooltip))
                region.tooltip = tooltip

            region = self.regions[region_name]
            rule = None
            if icon_name in self.data["rooms"]:
                if "requires" in self.data["rooms"][icon_name]:
                    rule = self.data["rooms"][icon_name]["requires"]
            location_box = Location(location_name, rule, self, region, height=26, size_hint=(1, None), spacing=5)
            icon = self.load_image(f'tracker/images/{icon_name}.png')
            icon.size = (24, 24)
            icon.texture.min_filter = 'nearest'
            icon.texture.mag_filter = 'nearest'
            icon.size_hint=(None, None)
            location_box.add_widget(icon)
            label = Label(text=f"[color=ff0000]{location_name}[/color]", valign="center", size_hint=(None, 1), markup = True)
            label.texture_update() 
            label.size = label.texture_size
            location_box.add_widget(label)
            location_box.label = label
            location_box.width = icon.width + 5 + label.width
            region.locations.append(location_box)
            region.tooltip.add_widget(location_box)
            region.tooltip._recalc_size()
            self.locations[locid] = location_box

        self.run_info = InfoView(ox=0, oy=0, osize=400)
        self.img.add_widget(self.run_info)
        self.img.bind(size=self.run_info._update_graphics, pos=self.run_info._update_graphics)

        self.box_layout = BoxLayout(size_hint=(1, None), orientation='vertical', spacing=5, padding=8)
        self.run_info.add_widget(self.box_layout)

        self.goals_label = Label(text="Goals", height=26, size_hint=(1, None), halign="left")
        self.goals_label.texture_update() 
        self.goals_label.size = self.goals_label.texture_size
        self.box_layout.add_widget(self.goals_label)

        self.goals_box = StackLayout(size_hint=(1, None), spacing=4)
        self.box_layout.add_widget(self.goals_box)

        for goal in self.ctx.options["goals"]:
            goal_box = Goal(size=(48,48), size_hint=(None, None))
            icon = self.load_image(f'tracker/images/{goal} Goal.png')
            icon.size = (48, 48)
            icon.texture.min_filter = 'nearest'
            icon.texture.mag_filter = 'nearest'
            icon.size_hint=(None, None)
            icon.color = (0, 0, 0, 1)
            goal_box.add_widget(icon)
            self.goals[goal] = goal_box
            self.goals_box.add_widget(goal_box)
            goal_box.tooltip_anchor = 53
            tooltip = TrackerTooltip(padding=(8, 4), size_hint=(None, None))
            tooltip_label = Label(text=goal, size_hint=(None, None))
            tooltip_label.texture_update() 
            tooltip_label.size = tooltip_label.texture_size
            tooltip.add_widget(tooltip_label)
            tooltip._recalc_size()
            tooltip._update_pos()
            self.tooltips.append((goal_box, tooltip))
        self.goals_box.do_layout()

        self.unlocks_label = Label(text="Unlocks", height=26, size_hint=(1, None), halign="left")
        self.unlocks_label.texture_update() 
        self.unlocks_label.size = self.unlocks_label.texture_size
        self.box_layout.add_widget(self.unlocks_label)

        self.unlocks_box = StackLayout(size_hint=(1, None), spacing=4)
        self.box_layout.add_widget(self.unlocks_box)

        for unlock in self.data["unlocks"].keys():
            unlock_box = Unlock(size=(32,28), size_hint=(None, None))
            icon = self.load_image(f'tracker/images/{unlock}.png')
            icon.size = (32, 28)
            icon.texture.min_filter = 'nearest'
            icon.texture.mag_filter = 'nearest'
            icon.size_hint=(None, None)
            icon.color = (0, 0, 0, 1)
            unlock_box.add_widget(icon)
            self.unlocks[unlock] = unlock_box
            self.unlocks_box.add_widget(unlock_box)
            unlock_box.tooltip_anchor = 37
            tooltip = TrackerTooltip(padding=(8, 4), size_hint=(None, None))
            tooltip_label = Label(text=unlock, size_hint=(None, None))
            tooltip_label.texture_update() 
            tooltip_label.size = tooltip_label.texture_size
            tooltip.add_widget(tooltip_label)
            tooltip._recalc_size()
            tooltip._update_pos()
            self.tooltips.append((unlock_box, tooltip))
        self.unlocks_box.do_layout()

        self.items_label = Label(text="Items", height=26, size_hint=(1, None), halign="left")
        self.items_label.texture_update() 
        self.items_label.size = self.items_label.texture_size
        self.box_layout.add_widget(self.items_label)

        self.items_box = BoxLayout(size_hint=(1, None))
        self.box_layout.add_widget(self.items_box)

        consumables_layout = BoxLayout(size_hint=(1, None), height=0, orientation='vertical')
        self.items_box.add_widget(consumables_layout)
        items_layout = BoxLayout(size_hint=(1, None), height=0, orientation='vertical')
        self.items_box.add_widget(items_layout)
        items_layout_2 = BoxLayout(size_hint=(1, None), height=0, orientation='vertical')
        self.items_box.add_widget(items_layout_2)

        for item in self.data["items"]:
            if item.endswith('Trap'):
                continue
            item_box = BoxLayout(height=26, size_hint=(1, None), spacing=5)
            icon = self.load_image(f'tracker/images/{item}.png')
            icon.size = (24, 24)
            icon.texture.min_filter = 'nearest'
            icon.texture.mag_filter = 'nearest'
            icon.size_hint=(None, None)
            item_box.add_widget(icon)
            self.items[item] = Label(text="0 (0)", valign="center", size_hint=(None, 1), markup = True)
            self.items[item].texture_update() 
            self.items[item].size = self.items[item].texture_size
            item_box.add_widget(self.items[item])
            item_box.tooltip_anchor = icon.width + item_box.spacing * 2 + self.items[item].width
            item_box.icon = icon
            tooltip = TrackerTooltip(padding=(8, 4), size_hint=(None, None))
            tooltip_label = Label(text=item, size_hint=(None, None))
            tooltip_label.texture_update() 
            tooltip_label.size = tooltip_label.texture_size
            tooltip.add_widget(tooltip_label)
            tooltip._recalc_size()
            tooltip._update_pos()
            self.tooltips.append((item_box, tooltip))
            if item.startswith('Random'):
                consumables_layout.add_widget(item_box)
                consumables_layout.height += 26
            else:
                if len(items_layout.children) < 6:
                    items_layout.add_widget(item_box)
                    items_layout.height += 26
                else:
                    items_layout_2.add_widget(item_box)
                    items_layout_2.height += 26
        items_layout.add_widget(Widget(height=(consumables_layout.height - items_layout.height)))
        items_layout.height = consumables_layout.height
        items_layout_2.add_widget(Widget(height=(consumables_layout.height - items_layout_2.height)))
        items_layout_2.height = consumables_layout.height
        self.items_box.height = consumables_layout.height

        self.run_info._update_graphics()

        self.update_reachability("Menu", True)
        for region in self.regions.values():
            region._update_color()

    def on_item_update(self, items):
        refresh = False
        for item in items:
            name = self.ctx.item_names.lookup_in_slot(item.item, self.ctx.slot)
            if name.endswith('Unlock'):
                area = name.replace(' Unlock', '')
                if area in self.unlocks:
                    self.unlocks[area]._check()
                    refresh = True
        if refresh:
            self.update_reachability("Menu", True)
            for region in self.regions.values():
                region._update_color()
                

    def on_location_update(self, checked_locations):
        for locid in checked_locations:
            self.locations[locid].checked = True
            self.locations[locid].region._update_color()

    def on_goals_update(self, goals):
        for goal, completed in goals.items():
            if completed:
                self.goals[goal]._complete()

    def on_runinfo_update(self, run_info):
        items = {}
        if isinstance(run_info["discarded_items"], dict):
            for item, amount in run_info["discarded_items"].items():
                total = f"{item}"
                tbd = f"{item}_tbd"
                received = f"{item}_received"
                if total in items:
                    items[total] += amount
                else:
                    items[total] = amount
                if tbd not in items:
                    items[tbd] = 0
                if received not in items:
                    items[received] = 0
        if isinstance(run_info["to_be_distributed"], list):
            for floor in run_info["to_be_distributed"]:
                if isinstance(floor, dict):
                    for item, amount in floor.items():
                        total = f"{item}"
                        tbd = f"{item}_tbd"
                        received = f"{item}_received"
                        if total in items:
                            items[total] += amount
                        else:
                            items[total] = amount
                        if tbd in items:
                            items[tbd] += amount
                        else:
                            items[tbd] = amount
                        if received not in items:
                            items[received] = 0
        if isinstance(run_info["received_items"], dict):
            for item, amount in run_info["received_items"].items():
                total = f"{item}"
                tbd = f"{item}_tbd"
                received = f"{item}_received"
                if total in items:
                    items[total] += amount
                else:
                    items[total] = amount
                if tbd not in items:
                    items[tbd] = 0
                if received in items:
                    items[received] += amount
                else:
                    items[received] = amount

        for item, amount in items.items():
            if "_" in item:
                continue
            total = f"{item}"
            tbd = f"{item}_tbd"
            received = f"{item}_received"
            if items[tbd] > 0:
                self.items[item].text = f"{items[received]}[color=ffffff88]+{items[tbd]}[/color] ({items[total]})"
            else:
                self.items[item].text = f"{items[received]} ({items[total]})"
            self.items[item].texture_update() 
            self.items[item].size = self.items[item].texture_size
            item_box = self.items[item].parent
            item_box.tooltip_anchor = item_box.icon.width + item_box.spacing * 2 + self.items[item].width

    def _update_overlay(self, *args):
        if not self.img.texture:
            return

        self.img.width = self.width
        self.img.height = self.width * (self.img.texture.height / self.img.texture.width)
        if self.img.height > self.height:
            self.img.height = self.height
            self.img.width = self.height * (self.img.texture.width / self.img.texture.height)
            self.img.y = 0
            self.img.x = (self.width-self.img.width)/2
        else:
            self.img.x = 0
            self.img.y = (self.height-self.img.height)/2

    def evaluate_rule(self, rule):
        if not rule:
            return True
        if "has" in rule:
            return self.unlocks[rule["has"]].unlocked
        if "or" in rule:
            return any(self.evaluate_rule(x) for x in rule["or"])
        if "and" in rule:
            return all(self.evaluate_rule(x) for x in rule["and"])
        
    def update_reachability(self, region, prev_reachable):
        j_region = self.data["regions"][region]
        if region in self.regions:
            rule = None
            if "requires" in j_region:
                rule = j_region["requires"]
            prev_reachable = self.regions[region].reachable or (prev_reachable and self.evaluate_rule(rule))
            self.regions[region].reachable = prev_reachable
        if "connects_to" in j_region:
            for connecting_region in j_region["connects_to"]:
                if connecting_region in self.regions:
                    self.update_reachability(connecting_region, prev_reachable)
        if "boss" in j_region:
            boss_region = j_region["boss"]
            if boss_region in self.regions:
                self.regions[boss_region].reachable = self.regions[boss_region].reachable or prev_reachable


class Unlock(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.unlocked = False

    def _check(self, *args):
        self.children[0].color = (1, 1, 1, 1)
        self.unlocked = True

class Goal(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.completed = False

    def _complete(self, *args):
        self.children[0].color = (1, 1, 1, 1)
        self.completed = True

class TrackerTooltip(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(0.2, 0.2, 0.2, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)

    def _recalc_size(self, *args):
        padding_left, padding_top, padding_right, padding_bottom = self.padding
        w = padding_left + padding_right
        h = padding_top + padding_bottom + self.spacing * (len(self.children) - 1)
        for c in self.children:
            w = max(w, padding_left + padding_right + c.width)
            h += c.height
        self.size = (w, h)
        self.rect.size = self.size

    def _update_pos(self, *args):
        self.rect.pos = self.pos

class InfoView(ScrollView):
    def __init__(self, ox, oy, osize, **kwargs):
        super().__init__(**kwargs)
        self.ox = ox
        self.oy = oy
        self.osize = osize

        with self.canvas.before:
            Color(0, 0, 0, 0.85)
            self.rect = Rectangle(size=self.size, pos=self.pos)

    def _update_graphics(self, *args):
        scale = self.parent.width / self.parent.texture.width
        self.pos = (self.parent.x + self.ox * scale, self.parent.y + self.oy * scale)
        self.size = (self.osize * scale, self.osize * scale)

        self.rect.size = self.size
        self.rect.pos = self.pos

        tracker = self.parent.parent

        total_unlocks = len(self.parent.parent.data["unlocks"].keys())
        unlocks_per_row = max(math.floor((self.width - 12) / 36), 1)
        unlock_rows = math.ceil(total_unlocks / unlocks_per_row)
        tracker.unlocks_box.height = unlock_rows * 32

        total_goals = len(self.parent.parent.ctx.options["goals"])
        goals_per_row = max(math.floor((self.width - 12) / 52), 1)
        goal_rows = math.ceil(total_goals / goals_per_row)
        tracker.goals_box.height = goal_rows * 52

        tracker.box_layout.height = tracker.goals_label.height + tracker.goals_box.height + tracker.unlocks_label.height + tracker.unlocks_box.height + tracker.items_label.height + tracker.items_box.height + 35

class Location(BoxLayout):
    tracker: TrackerLayout

    def __init__(self, name, rule, tracker, region, **kwargs):
        super().__init__(**kwargs)
        self.rule = rule
        self.tracker = tracker
        self.checked = False
        self.region = region
        self.name = name

    def reachable(self):
        return self.region.reachable and self.tracker.evaluate_rule(self.rule)

    def _update_color(self):
        if self.checked:
            self.label.text = f"[color=888888]{self.name}[/color]"
        elif self.region.reachable and self.reachable():
            self.label.text = f"[color=00ff00]{self.name}[/color]"
        else:
            self.label.text = f"[color=ff0000]{self.name}[/color]"
        self.label.texture_update() 
        self.label.size = self.label.texture_size
        self.region.tooltip._recalc_size()

class Region(Widget):
    def __init__(self, ox, oy, osize, **kwargs):
        super().__init__(**kwargs)
        self.ox = ox
        self.oy = oy
        self.osize = osize

        self.reachable = False
        self.locations = []

        with self.canvas:
            Color(0, 0, 0)
            self.outer_rect = Rectangle(size=self.size, pos=self.pos)
            self.left_tri = Color(0, 1, 0)
            self.inner_rect = Rectangle(size=(self.width-4, self.height-4), pos=(self.x+2, self.y+2))
            self.right_tri = Color(1, 0, 0)
            x, y = self.inner_rect.pos
            width, height = self.inner_rect.size
            self.inner_triangle = Triangle(points=(x, y, x + width, y, x + width, y + height))

    def _update_graphics(self, *args):
        scale = self.parent.width / self.parent.texture.width
        self.pos = (self.parent.x + (self.ox - self.osize / 2) * scale, self.parent.y + self.parent.height - (self.oy + self.osize / 2) * scale)
        self.size = (self.osize * scale, self.osize * scale)

        self.tooltip_anchor = 30 * scale
        
        self.outer_rect.size=self.size
        self.outer_rect.pos=self.pos
        self.inner_rect.size=(self.width-4, self.height-4)
        self.inner_rect.pos=(self.x+2, self.y+2)
        x, y = self.inner_rect.pos
        width, height = self.inner_rect.size
        self.inner_triangle.points=(x, y, x + width, y, x + width, y + height)

    def _update_color(self, *args):
        all_green = True
        all_red = True
        all_gray = True
        one_green = False
        one_red = False
        one_gray = False

        for location in self.locations:
            location._update_color()
            if location.checked:
                one_gray = True
                all_green = False
                all_red = False
            else:
                all_gray = False
            if not location.checked and location.reachable():
                one_green = True
                all_gray = False
                all_red = False
            if not location.checked and not location.reachable():
                one_red = True
                all_green = False
                all_gray = False

        if all_red:
            self.left_tri.rgb = (1, 0, 0)
            self.right_tri.rgb = (1, 0, 0)
        elif all_gray:
            self.left_tri.rgb = (0.3, 0.3, 0.3)
            self.right_tri.rgb = (0.3, 0.3, 0.3)
        elif all_green:
            self.left_tri.rgb = (0, 1, 0)
            self.right_tri.rgb = (0, 1, 0)
        elif one_red and one_green:
            self.left_tri.rgb = (0, 1, 0)
            self.right_tri.rgb = (1, 0, 0)
        elif one_green and one_gray and not one_red:
            self.left_tri.rgb = (0, 1, 0)
            self.right_tri.rgb = (0, 1, 0)
        elif one_gray and one_red and not one_green:
            self.left_tri.rgb = (0.3, 0.3, 0.3)
            self.right_tri.rgb = (1, 0, 0)