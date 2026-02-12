This is just a huge todo file

there are also todos dropped around the code base

if anyone decides to pick one up please tell me

if you pick one up and then decide to do something else, add research notes here

# boot-strap logic
- this is needed to ensure recipes are possible and speed up best logic
- should be able to be implemented as separate logic mode but would ignore most recursion
- probably going to be a modified dykstra with multi start and 2 found modes
- 2 found modes being automated and manual
- if manual node finds another manual node look if it's a positive loop if it is, make it automated
- this would only find minimum recipe loops and method to hint? (can LP be applied here?)

# add `pulp` library to internal apworld
- `pulp` is the python library used for linear programming (LP)
- this would remove the requirement for precalculating
- caching on the system ontop of packs would need to be implemented

# rocket silo products
- needs to be added to extractor
- silo is its own prototype https://lua-api.factorio.com/latest/prototypes/RocketSiloPrototype.html
- silo-parts are `hidden` but I think they are required by all rocket silos (if they exist silo-parts do)
- number of silo-parts in silo prototype
- products are defined in launch items with `rocket_launch_products`
- `send_to_orbit_mode` on item might define automatability
- remove force space-science-pack

# Irregular tree shape
- pull request by CosmicWolf
- small improvements from the pull request to base needs to be added

# boiler recipes
- needs to be added to extractor

# reactor recipes
- needs to be added to extractor
- energy being burn time?

# spoilage recipes
- needs to be added to extractor
- energy being spoil time (this might be too high and might need a modifier?)

# fluid temperature
- needs to be added to extractor
- how minimum (and maximum?) defined in recipes
- is temperature just multiple different "items"

# energy sources and uses
- `void` is no energy source needed
- can custom be defined?

# infinite research
- already (mostly) extracted (extract max level instead?)
- how options?