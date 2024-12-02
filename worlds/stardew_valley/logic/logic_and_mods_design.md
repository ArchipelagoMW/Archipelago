# Logic mixin

Mixins are used to split the logic building methods in multiple classes, so it's more scoped and easier to extend specific methods.

One single instance of Logic is necessary so mods can change the logics. This means that, when calling itself, a `Logic` class has to call its instance in
the `logic`, because it might have been overriden.

```python
class TimeLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.time = TimeLogic(*args, **kwargs)


class TimeLogic(BaseLogic[Union[TimeLogicMixin, ReceivedLogicMixin]]):

    def has_lived_months(self, number: int) -> StardewRule:
        return self.logic.received(Event.month_end, number)

    def has_year_two(self) -> StardewRule:
        return self.logic.time.has_lived_months(4)

    def has_year_three(self) -> StardewRule:
        return self.logic.time.has_lived_months(8)
```

Creating the rules for actual items has to be outside the `logic` instance. Once the vanilla logic builder is created, mods will be able to replace the logic
implementations by their own modified version. For instance, the `combat` logic can be replaced by the magic mod to extends its methods to add spells in the
combat logic.

## Logic class created on the fly (idea)

The logic class could be created dynamically, based on the `LogicMixin` provided by the content packs. This would allow replacing completely mixins, instead of
overriding their logic afterward. Might be too complicated for no real gain tho...

# Content pack (idea)

Instead of using modules to hold the data, and have each mod adding their data to existing content, each mod data should be in a `ContentPack`. Vanilla, Ginger
Island, or anything that could be disabled would be in a content pack as well.

Eventually, Vanilla content could even be disabled (a split would be required for items that are necessary to all content packs) to have a Ginger Island only
play through created without the heavy vanilla logic computation.

## Unpacking

Steps to unpack content follows the same steps has the world initialisation. Content pack however need to be unpacked in a specific order, based on their
dependencies. Vanilla would always be first, then anything that depends only on Vanilla, etc.

1. In `generate_early`, content packs are selected. The logic builders are created and content packs are unpacked so all their content is in the proper
   item/npc/weapon lists.
    - `ContentPack` instances are shared across players. However, some mods need to modify content of other packs. In that case, an instance of the content is
      created specifically for that player (For instance, SVE changes the Wizard). This probably does not happen enough to require sharing those instances. If
      necessary, a FlyWeight design pattern could be used.
2. In `create_regions`, AP regions and entrances are unpacked, and randomized if needed.
3. In `create_items`, AP items are unpacked, and randomized.
4. In `set_rules`, the rules are applied to the AP entrances and locations. Each content pack have to apply the proper rules for their entrances and locations.
    - (idea) To begin this step, sphere 0 could be simplified instantly as sphere 0 regions and items are already known.
5. Nothing to do in `generate_basic`.

## Item Sources

Instead of containing rules directly, items would contain sources that would then be transformed into rules. Using a single dispatch mechanism, the sources will
be associated to their actual logic.

This system is extensible and easily maintainable in the ways that it decouple the rule and the actual items. Any "type" of item could be used with any "type"
of source (Monster drop and fish can have foraging sources).

- Mods requiring special rules can remove sources from vanilla content or wrap them to add their own logic (Magic add sources for some items), or change the
  rules for monster drop sources.
- (idea) A certain difficulty level (or maybe tags) could be added to the source, to enable or disable them given settings chosen by the player. Someone with a
  high grinding tolerance can enable "hard" or "grindy" sources. Some source that are pushed back in further spheres can be replaced by less forgiving sources
  if easy logic is disabled. For instance, anything that requires money could be accessible as soon as you can sell something to someone (even wood).

Items are classified by their source. An item with a fishing or a crab pot source is considered a fish, an item dropping from a monster is a monster drop. An
item with a foraging source is a forageable. Items can fit in multiple categories. 
