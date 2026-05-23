from typing import TYPE_CHECKING

from . import menu, r100, r122, r101, r102, r103, r104, rf01, rf02, rf03, rf04, rf07, rf08, r108, r109, r107, r10e, \
    r110, rf06, r105, rf09, rf0a, r201,r205, r200, r206

if TYPE_CHECKING:
    from .. import OkamiWorld

okami_exits = {
    **menu.exits,
    **r100.exits,
    **r101.exits,
    **r102.exits,
    **r103.exits,
    **r104.exits,
    **r105.exits,
    **r107.exits,
    **r108.exits,
    **r109.exits,
    **r10e.exits,
    **r110.exits,
    **r122.exits,
    **r200.exits,
    **r201.exits,
    **r205.exits,
    **r206.exits,
    **rf01.exits,
    **rf02.exits,
    **rf03.exits,
    **rf04.exits,
    **rf06.exits,
    **rf07.exits,
    **rf08.exits,
    **rf09.exits,
    **rf0a.exits,
}

okami_locations = {
    **r100.locations,
    **r101.locations,
    **r102.locations,
    **r103.locations,
    **r104.locations,
    **r105.locations,
    **r107.locations,
    **r108.locations,
    **r109.locations,
    **r10e.locations,
    **r110.locations,
    **r122.locations,
    **r200.locations,
    **r201.locations,
    **r205.locations,
    **r206.locations,
    **rf01.locations,
    **rf02.locations,
    **rf03.locations,
    **rf04.locations,
    **rf06.locations,
    **rf07.locations,
    **rf08.locations,
    **rf09.locations,
    **rf0a.locations,
}

okami_events = {
    **r100.events,
    **r101.events,
    **r102.events,
    **r103.events,
    **r104.events,
    **r105.events,
    **r107.events,
    **r108.events,
    **r109.events,
    **r10e.events,
    **r110.events,
    **r122.events,
    **r200.events,
    **r201.events,
    **r205.events,
    **r206.events,
    **rf01.events,
    **rf02.events,
    **rf03.events,
    **rf04.events,
    **rf06.events,
    **rf07.events,
    **rf08.events,
    **rf09.events,
    **rf0a.events,
}

# Shop locations are separate because they're conditionally created based on RandomizeShops
okami_shop_locations = {
    **getattr(r102, 'shop_locations', {}),
    **getattr(r105, 'shop_locations', {}),
    **getattr(r108, 'shop_locations', {}),
    **getattr(r109, 'shop_locations', {}),
    **getattr(r110, 'shop_locations', {}),
    **getattr(r201, 'shop_locations', {}),
    **getattr(rf02, 'shop_locations', {}),
    **getattr(rf04, 'shop_locations', {}),
    **getattr(rf08, 'shop_locations', {}),
    **getattr(rf0a, 'shop_locations', {}),
}

okami_warps = {
    **r102.warps,
    **r105.warps,
    **r108.warps,
    **r109.warps,
    **rf02.warps,
    **rf04.warps,
    **rf08.warps,
    **rf0a.warps,
}
