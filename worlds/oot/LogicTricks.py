known_logic_tricks = {
    # General tricks

    'Pass Through Visible One-Way Collisions': {
        'name'    : 'logic_visible_collisions',
        'tags'    : ("Entrance", "Kakariko Village",),
        'tooltip' : '''\
                    Allows climbing through the platform to reach 
                    Impa's House Back as adult with no items and 
                    going through the Kakariko Village Gate as child
                    when coming from the Mountain Trail side.
                    '''},
    'Hidden Grottos without Stone of Agony': {
        'name'    : 'logic_grottos_without_agony',
        'tags'    : ("General", "Entrance",),
        'tooltip' : '''\
                    Allows entering hidden grottos without the
                    Stone of Agony.
                    '''},
    'Fewer Tunic Requirements': {
        'name'    : 'logic_fewer_tunic_requirements',
        'tags'    : ("General", "Fire Temple", "Water Temple", "Gerudo Training Ground", "Zora's Fountain", "Death Mountain Crater", "MQ",),
        'tooltip' : '''\
                    Allows the following possible without Tunics:
                    - Enter Water Temple. The area below the center
                    pillar still requires Zora Tunic. Applies to
                    MQ also.
                    - Enter Fire Temple. Only the first floor is
                    accessible, and not Volvagia. Applies to
                    MQ also.
                    - Zora's Fountain Bottom Freestanding PoH.
                    Might not have enough health to resurface.
                    - Gerudo Training Ground Underwater
                    Silver Rupee Chest. May need to make multiple
                    trips. Applies to MQ also.
                    '''},
    'Beehives with Bombchus' : {
        'name'    : 'logic_beehives_bombchus',
        'tags'    : ("Beehives",),
        'tooltip' : '''\
                    Puts breaking beehives with bombchus into logic.
                    Using bombs is already expected on beehives that
                    that are low enough that a bomb throw will reach.
                    '''},
    'Hammer Rusted Switches Through Walls': {
        'name'    : 'logic_rusted_switches',
        'tags'    : ("Fire Temple", "Ganon's Castle", "MQ",),
        'tooltip' : '''\
                    Applies to:
                    - Fire Temple Highest Goron Chest.
                    - MQ Fire Temple Lizalfos Maze.
                    - MQ Spirit Trial.
                    '''},

    # Overworld tricks

    'Adult Kokiri Forest GS with Hover Boots': {
        'name'    : 'logic_adult_kokiri_gs',
        'tags'    : ("Kokiri Forest", "Skulltulas",),
        'tooltip' : '''\
                    Can be obtained without Hookshot by using the Hover
                    Boots off of one of the roots.
                    '''},
    'Jump onto the Lost Woods Bridge as Adult with Nothing': {
        'name'    : 'logic_lost_woods_bridge',
        'tags'    : ("the Lost Woods", "Entrance",),
        'tooltip' : '''\
                    With very precise movement it's possible for
                    adult to jump onto the bridge without needing
                    Longshot, Hover Boots, or Bean.
                    '''},
    'Backflip over Mido as Adult': {
        'name'    : 'logic_mido_backflip',
        'tags'    : ("the Lost Woods",),
        'tooltip' : '''\
                    With a specific position and angle, you can
                    backflip over Mido.
                    '''},
    'Lost Woods Adult GS without Bean': {
        'name'    : 'logic_lost_woods_gs_bean',
        'tags'    : ("the Lost Woods", "Skulltulas",),
        'tooltip' : '''\
                    You can collect the token with a precise
                    Hookshot use, as long as you can kill the
                    Skulltula somehow first. It can be killed
                    using Longshot, Bow, Bombchus or Din's Fire.
                    '''},
    'Hyrule Castle Storms Grotto GS with Just Boomerang': {
        'name'    : 'logic_castle_storms_gs',
        'tags'    : ("Hyrule Castle", "Skulltulas",),
        'tooltip' : '''\
                    With precise throws, the Boomerang alone can
                    kill the Skulltula and collect the token,
                    without first needing to blow up the wall.
                    '''},
    'Man on Roof without Hookshot': {
        'name'    : 'logic_man_on_roof',
        'tags'    : ("Kakariko Village",),
        'tooltip' : '''\
                    Can be reached by side-hopping off
                    the watchtower as either age, or by
                    jumping onto the potion shop's roof
                    from the ledge as adult.
                    '''},
    'Kakariko Tower GS with Jump Slash': {
        'name'    : 'logic_kakariko_tower_gs',
        'tags'    : ("Kakariko Village", "Skulltulas",),
        'tooltip' : '''\
                    Climb the tower as high as you can without
                    touching the Gold Skulltula, then let go and
                    jump slash immediately. By jump-slashing from
                    as low on the ladder as possible to still
                    hit the Skulltula, this trick can be done
                    without taking fall damage.
                    '''},
    'Windmill PoH as Adult with Nothing': {
        'name'    : 'logic_windmill_poh',
        'tags'    : ("Kakariko Village",),
        'tooltip' : '''\
                    Can jump up to the spinning platform from
                    below as adult.
                    '''},
    'Kakariko Rooftop GS with Hover Boots': {
        'name'    : 'logic_kakariko_rooftop_gs',
        'tags'    : ("Kakariko Village", "Skulltulas",),
        'tooltip' : '''\
                    Take the Hover Boots from the entrance to Impa's
                    House over to the rooftop of Skulltula House. From
                    there, a precise Hover Boots backwalk with backflip
                    can be used to get onto a hill above the side of
                    the village. And then from there you can Hover onto
                    Impa's rooftop to kill the Skulltula and backflip
                    into the token.
                    '''},
    'Graveyard Freestanding PoH with Boomerang': {
        'name'    : 'logic_graveyard_poh',
        'tags'    : ("the Graveyard",),
        'tooltip' : '''\
                    Using a precise moving setup you can obtain
                    the Piece of Heart by having the Boomerang
                    interact with it along the return path.
                    '''},
    'Second Dampe Race as Child': {
        'name'    : 'logic_child_dampe_race_poh',
        'tags'    : ("the Graveyard", "Entrance",),
        'tooltip' : '''\
                    It is possible to complete the second dampe
                    race as child in under a minute, but it is
                    a strict time limit.
                    '''},
    'Shadow Temple Entry with Fire Arrows': {
        'name'    : 'logic_shadow_fire_arrow_entry',
        'tags'    : ("Shadow Temple",),
        'tooltip' : '''\
                    It is possible to light all of the torches to
                    open the Shadow Temple entrance with just Fire
                    Arrows, but you must be very quick, precise,
                    and strategic with how you take your shots.
                    '''},
    'Death Mountain Trail Soil GS without Destroying Boulder': {
        'name'    : 'logic_dmt_soil_gs',
        'tags'    : ("Death Mountain Trail", "Skulltulas",),
        'tooltip' : '''\
                    Bugs will go into the soft soil even while the boulder is
                    still blocking the entrance.
                    Then, using a precise moving setup you can kill the Gold
                    Skulltula and obtain the token by having the Boomerang
                    interact with it along the return path.
                    '''},
    'Death Mountain Trail Chest with Strength': {
        'name'    : 'logic_dmt_bombable',
        'tags'    : ("Death Mountain Trail",),
        'tooltip' : '''\
                    Child Link can blow up the wall using a nearby bomb
                    flower. You must backwalk with the flower and then
                    quickly throw it toward the wall.
                    '''},
    'Death Mountain Trail Lower Red Rock GS with Hookshot': {
        'name'    : 'logic_trail_gs_lower_hookshot',
        'tags'    : ("Death Mountain Trail", "Skulltulas",),
        'tooltip' : '''\
                    After killing the Skulltula, the token can be fished
                    out of the rock without needing to destroy it, by
                    using the Hookshot in the correct way.
                    '''},
    'Death Mountain Trail Lower Red Rock GS with Hover Boots': {
        'name'    : 'logic_trail_gs_lower_hovers',
        'tags'    : ("Death Mountain Trail", "Skulltulas",),
        'tooltip' : '''\
                    After killing the Skulltula, the token can be
                    collected without needing to destroy the rock by
                    backflipping down onto it with the Hover Boots.
                    First use the Hover Boots to stand on a nearby
                    fence, and go for the Skulltula Token from there.
                    '''},
    'Death Mountain Trail Lower Red Rock GS with Magic Bean': {
        'name'    : 'logic_trail_gs_lower_bean',
        'tags'    : ("Death Mountain Trail", "Skulltulas",),
        'tooltip' : '''\
                    After killing the Skulltula, the token can be
                    collected without needing to destroy the rock by
                    jumping down onto it from the bean plant,
                    midflight, with precise timing and positioning.
                    '''},
    'Death Mountain Trail Climb with Hover Boots': {
        'name'    : 'logic_dmt_climb_hovers',
        'tags'    : ("Death Mountain Trail",),
        'tooltip' : '''\
                    It is possible to use the Hover Boots to bypass
                    needing to destroy the boulders blocking the path
                    to the top of Death Mountain.
                    '''},
    'Death Mountain Trail Upper Red Rock GS without Hammer': {
        'name'    : 'logic_trail_gs_upper',
        'tags'    : ("Death Mountain Trail", "Skulltulas",),
        'tooltip' : '''\
                    After killing the Skulltula, the token can be collected
                    by backflipping into the rock at the correct angle.
                    '''},
    'Deliver Eye Drops with Bolero of Fire': {
        'name'    : 'logic_biggoron_bolero',
        'tags'    : ("Death Mountain Trail",),
        'tooltip' : '''\
                    Playing a warp song normally causes a trade item to
                    spoil immediately, however, it is possible use Bolero
                    to reach Biggoron and still deliver the Eye Drops
                    before they spoil. If you do not wear the Goron Tunic,
                    the heat timer inside the crater will override the trade
                    item's timer. When you exit to Death Mountain Trail you
                    will have one second to show the Eye Drops before they
                    expire. You can get extra time to show the Eye Drops if
                    you warp immediately upon receiving them. If you don't
                    have many hearts, you may have to reset the heat timer
                    by quickly dipping in and out of Darunia's chamber or
                    quickly equipping and unequipping the Goron Tunic.
                    This trick does not apply if "Randomize Warp Song
                    Destinations" is enabled, or if the settings are such
                    that trade items do not need to be delivered within a
                    time limit.
                    '''},                    
    'Goron City Spinning Pot PoH with Bombchu': {
        'name'    : 'logic_goron_city_pot',
        'tags'    : ("Goron City",),
        'tooltip' : '''\
                    A Bombchu can be used to stop the spinning
                    pot, but it can be quite finicky to get it
                    to work.
                    '''},
    'Goron City Spinning Pot PoH with Strength': {
        'name'    : 'logic_goron_city_pot_with_strength',
        'tags'    : ("Goron City",),
        'tooltip' : '''\
                    Allows for stopping the Goron City Spinning
                    Pot using a bomb flower alone, requiring 
                    strength in lieu of inventory explosives.
                    '''},
    'Rolling Goron (Hot Rodder Goron) as Child with Strength': {
        'name'    : 'logic_child_rolling_with_strength',
        'tags'    : ("Goron City",),
        'tooltip' : '''\
                    Use the bombflower on the stairs or near Medigoron.
                    Timing is tight, especially without backwalking.
                    '''},
    "Stop Link the Goron with Din's Fire": {
        'name'    : 'logic_link_goron_dins',
        'tags'    : ("Goron City",),
        'tooltip' : '''\
                    The timing is quite awkward.
                    '''},
    'Goron City Maze Left Chest with Hover Boots': {
        'name'    : 'logic_goron_city_leftmost',
        'tags'    : ("Goron City",),
        'tooltip' : '''\
                    A precise backwalk starting from on top of the
                    crate and ending with a precisely-timed backflip
                    can reach this chest without needing either
                    the Hammer or Silver Gauntlets.
                    '''},
    'Goron City Grotto with Hookshot While Taking Damage': {
        'name'    : 'logic_goron_grotto',
        'tags'    : ("Goron City",),
        'tooltip' : '''\
                    It is possible to reach the Goron City Grotto by
                    quickly using the Hookshot while in the midst of
                    taking damage from the lava floor. This trick will
                    not be expected on OHKO or quadruple damage.
                    '''},
    "Crater's Bean PoH with Hover Boots": {
        'name'    : 'logic_crater_bean_poh_with_hovers',
        'tags'    : ("Death Mountain Crater",),
        'tooltip' : '''\
                    Hover from the base of the bridge
                    near Goron City and walk up the
                    very steep slope.
                    '''},
    'Death Mountain Crater Jump to Bolero': {
        'name'    : 'logic_crater_bolero_jump',
        'tags'    : ("Death Mountain Crater",),
        'tooltip' : '''\
                    Using a shield to drop a pot while you have
                    the perfect speed and position, the pot can
                    push you that little extra distance you
                    need to jump across the gap in the bridge.
                    '''},
    'Death Mountain Crater Upper to Lower with Hammer': {
        'name'    : 'logic_crater_boulder_jumpslash',
        'tags'    : ("Death Mountain Crater",),
        'tooltip' : '''\
                    With the Hammer, you can jump slash the rock twice
                    in the same jump in order to destroy it before you
                    fall into the lava.
                    '''},
    'Death Mountain Crater Upper to Lower Boulder Skip': {
        'name'    : 'logic_crater_boulder_skip',
        'tags'    : ("Death Mountain Crater",),
        'tooltip' : '''\
                    With careful positioning, you can jump to the ledge
                    where the boulder is, then use repeated ledge grabs
                    to shimmy to a climbable ledge. This trick supersedes
                    "Death Mountain Crater Upper to Lower with Hammer".
                    '''},
    "Zora's River Lower Freestanding PoH as Adult with Nothing": {
        'name'    : 'logic_zora_river_lower',
        'tags'    : ("Zora's River",),
        'tooltip' : '''\
                    Adult can reach this PoH with a precise jump,
                    no Hover Boots required.
                    '''},
    "Zora's River Upper Freestanding PoH as Adult with Nothing": {
        'name'    : 'logic_zora_river_upper',
        'tags'    : ("Zora's River",),
        'tooltip' : '''\
                    Adult can reach this PoH with a precise jump,
                    no Hover Boots required.
                    '''},
    "Zora's Domain Entry with Cucco": {
        'name'    : 'logic_zora_with_cucco',
        'tags'    : ("Zora's River",),
        'tooltip' : '''\
                    Can fly behind the waterfall with
                    a cucco as child.
                    '''},
    "Zora's Domain Entry with Hover Boots": {
        'name'    : 'logic_zora_with_hovers',
        'tags'    : ("Zora's River",),
        'tooltip' : '''\
                    Can hover behind the waterfall as adult.
                    '''},
    "Zora's River Rupees with Jump Dive": {
        'name'    : 'logic_zora_river_rupees',
        'tags'    : ("Zora's River", "Freestandings",),
        'tooltip' : '''\
                    You can jump down onto them from
                    above to skip needing Iron Boots.
                    '''},
    'Skip King Zora as Adult with Nothing': {
        'name'    : 'logic_king_zora_skip',
        'tags'    : ("Zora's Domain",),
        'tooltip' : '''\
                    With a precise jump as adult, it is possible to
                    get on the fence next to King Zora from the front
                    to access Zora's Fountain.
                    '''},
    "Zora's Domain GS with No Additional Items": {
        'name'    : 'logic_domain_gs',
        'tags'    : ("Zora's Domain", "Skulltulas",),
        'tooltip' : '''\
                    A precise jump slash can kill the Skulltula and
                    recoil back onto the top of the frozen waterfall.
                    To kill it, the logic normally guarantees one of
                    Hookshot, Bow, or Magic.
                    '''},                    
    'Lake Hylia Lab Wall GS with Jump Slash': {
        'name'    : 'logic_lab_wall_gs',
        'tags'    : ("Lake Hylia", "Skulltulas",),
        'tooltip' : '''\
                    The jump slash to actually collect the
                    token is somewhat precise.
                    '''},
    'Lake Hylia Lab Dive without Gold Scale': {
        'name'    : 'logic_lab_diving',
        'tags'    : ("Lake Hylia",),
        'tooltip' : '''\
                    Remove the Iron Boots in the midst of
                    Hookshotting the underwater crate.
                    '''},
    'Water Temple Entry without Iron Boots using Hookshot': {
        'name'    : 'logic_water_hookshot_entry',
        'tags'    : ("Lake Hylia",),
        'tooltip' : '''\
                    When entering Water Temple using Gold Scale instead
                    of Iron Boots, the Longshot is usually used to be
                    able to hit the switch and open the gate. But, by
                    standing in a particular spot, the switch can be hit
                    with only the reach of the Hookshot.
                    '''},
    'Gerudo Valley Crate PoH as Adult with Hover Boots': {
        'name'    : 'logic_valley_crate_hovers',
        'tags'    : ("Gerudo Valley",),
        'tooltip' : '''\
                    From the far side of Gerudo Valley, a precise
                    Hover Boots movement and jump-slash recoil can
                    allow adult to reach the ledge with the crate
                    PoH without needing Longshot. You will take 
                    fall damage.
                    '''},
    '''Thieves' Hideout "Kitchen" with No Additional Items''': {
        'name'    : 'logic_gerudo_kitchen',
        'tags'    : ("Thieves' Hideout", "Gerudo's Fortress",),
        'tooltip' : '''\
                    Allows passing through the kitchen by avoiding being
                    seen by the guards. The logic normally guarantees
                    Bow or Hookshot to stun them from a distance, or
                    Hover Boots to cross the room without needing to
                    deal with the guards.
                    '''},
    "Gerudo's Fortress Ledge Jumps": {
        'name'    : 'logic_gf_jump',
        'tags'    : ("Gerudo's Fortress",),
        'tooltip' : '''\
                    Adult can jump onto the top roof of the fortress
                    without going through the interior of the hideout.
                    '''},
    'Wasteland Crossing without Hover Boots or Longshot': {
        'name'    : 'logic_wasteland_crossing',
        'tags'    : ("Haunted Wasteland",),
        'tooltip' : '''\
                    You can beat the quicksand by backwalking across it
                    in a specific way.
                    Note that jumping to the carpet merchant as child
                    typically requires a fairly precise jump slash.
                    '''},
    'Lensless Wasteland': {
        'name'    : 'logic_lens_wasteland',
        'tags'    : ("Lens of Truth", "Haunted Wasteland",),
        'tooltip' : '''\
                    By memorizing the path, you can travel through the
                    Wasteland without using the Lens of Truth to see
                    the Poe.
                    The equivalent trick for going in reverse through
                    the Wasteland is "Reverse Wasteland".
                    '''},
    'Reverse Wasteland': {
        'name'    : 'logic_reverse_wasteland',
        'tags'    : ("Haunted Wasteland",),
        'tooltip' : '''\
                    By memorizing the path, you can travel through the
                    Wasteland in reverse.
                    Note that jumping to the carpet merchant as child
                    typically requires a fairly precise jump slash.
                    The equivalent trick for going forward through the
                    Wasteland is "Lensless Wasteland".
                    To cross the river of sand with no additional items,
                    be sure to also enable "Wasteland Crossing without
                    Hover Boots or Longshot".
                    Unless all overworld entrances are randomized, child
                    Link will not be expected to do anything at Gerudo's
                    Fortress.
                    '''},
    'Colossus Hill GS with Hookshot': {
        'name'    : 'logic_colossus_gs',
        'tags'    : ("Desert Colossus", "Skulltulas",),
        'tooltip' : '''\
                    Somewhat precise. If you kill enough Leevers
                    you can get enough of a break to take some time
                    to aim more carefully.
                    '''},

    # Dungeons

    'Deku Tree Basement Vines GS with Jump Slash': {
        'name'    : 'logic_deku_basement_gs',
        'tags'    : ("Deku Tree", "Skulltulas",),
        'tooltip' : '''\
                    Can be defeated by doing a precise jump slash.
                    '''},
    'Deku Tree Basement without Slingshot': {
        'name'    : 'logic_deku_b1_skip',
        'tags'    : ("Deku Tree", "MQ",),
        'tooltip' : '''\
                    A precise jump can be used to skip
                    needing to use the Slingshot to go
                    around B1 of the Deku Tree. If used
                    with the "Closed Forest" setting, a
                    Slingshot will not be guaranteed to
                    exist somewhere inside the Forest.
                    This trick applies to both Vanilla
                    and Master Quest.
                    '''},
    'Deku Tree Basement Web to Gohma with Bow': {
        'name'    : 'logic_deku_b1_webs_with_bow',
        'tags'    : ("Deku Tree", "Entrance",),
        'tooltip' : '''\
                    All spider web walls in the Deku Tree basement can be burnt
                    as adult with just a bow by shooting through torches. This
                    trick only applies to the circular web leading to Gohma;
                    the two vertical webs are always in logic.

                    Backflip onto the chest near the torch at the bottom of
                    the vine wall. With precise positioning you can shoot
                    through the torch to the right edge of the circular web.

                    This allows completion of adult Deku Tree with no fire source.
                    '''},
    'Deku Tree MQ Compass Room GS Boulders with Just Hammer': {
        'name'    : 'logic_deku_mq_compass_gs',
        'tags'    : ("Deku Tree", "Skulltulas", "MQ",),
        'tooltip' : '''\
                    Climb to the top of the vines, then let go
                    and jump slash immediately to destroy the
                    boulders using the Hammer, without needing
                    to spawn a Song of Time block.
                    '''},
    'Deku Tree MQ Roll Under the Spiked Log': {
        'name'    : 'logic_deku_mq_log',
        'tags'    : ("Deku Tree", "MQ",),
        'tooltip' : '''\
                    You can get past the spiked log by rolling
                    to briefly shrink your hitbox. As adult,
                    the timing is a bit more precise.
                    '''},
    "Dodongo's Cavern Scarecrow GS with Armos Statue": {
        'name'    : 'logic_dc_scarecrow_gs',
        'tags'    : ("Dodongo's Cavern", "Skulltulas",),
        'tooltip' : '''\
                    You can jump off an Armos Statue to reach the
                    alcove with the Gold Skulltula. It takes quite
                    a long time to pull the statue the entire way.
                    The jump to the alcove can be a bit picky when
                    done as child.
                    '''},
    "Dodongo's Cavern Vines GS from Below with Longshot": {
        'name'    : 'logic_dc_vines_gs',
        'tags'    : ("Dodongo's Cavern", "Skulltulas",),
        'tooltip' : '''\
                    The vines upon which this Skulltula rests are one-
                    sided collision. You can use the Longshot to get it
                    from below, by shooting it through the vines,
                    bypassing the need to lower the staircase.
                    '''},
    "Dodongo's Cavern Staircase with Bow": {
        'name'    : 'logic_dc_staircase',
        'tags'    : ("Dodongo's Cavern",),
        'tooltip' : '''\
                    The Bow can be used to knock down the stairs
                    with two well-timed shots.
                    '''},
    "Dodongo's Cavern Child Slingshot Skips": {
        'name'    : 'logic_dc_slingshot_skip',
        'tags'    : ("Dodongo's Cavern",),
        'tooltip' : '''\
                    With precise platforming, child can cross the
                    platforms while the flame circles are there.
                    When enabling this trick, it's recommended that
                    you also enable the Adult variant: "Dodongo's
                    Cavern Spike Trap Room Jump without Hover Boots".
                    '''},
    "Dodongo's Cavern Two Scrub Room with Strength": {
        'name'    : 'logic_dc_scrub_room',
        'tags'    : ("Dodongo's Cavern",),
        'tooltip' : '''\
                    With help from a conveniently-positioned block,
                    Adult can quickly carry a bomb flower over to
                    destroy the mud wall blocking the room with two
                    Deku Scrubs.
                    '''},
    "Dodongo's Cavern Spike Trap Room Jump without Hover Boots": {
        'name'    : 'logic_dc_jump',
        'tags'    : ("Dodongo's Cavern", "MQ",),
        'tooltip' : '''\
                    The jump is adult Link only. Applies to both Vanilla and MQ.
                    '''},
    "Dodongo's Cavern Smash the Boss Lobby Floor": {
        'name'    : 'logic_dc_hammer_floor',
        'tags'    : ("Dodongo's Cavern", "Entrance", "MQ",),
        'tooltip' : '''\
                    The bombable floor before King Dodongo can be destroyed
                    with Hammer if hit in the very center. This is only
                    relevant with Shuffle Boss Entrances or if Dodongo's Cavern
                    is MQ and either variant of "Dodongo's Cavern MQ Light the
                    Eyes with Strength" is on.
                    '''},
    "Dodongo's Cavern MQ Early Bomb Bag Area as Child": {
        'name'    : 'logic_dc_mq_child_bombs',
        'tags'    : ("Dodongo's Cavern", "MQ",),
        'tooltip' : '''\
                    With a precise jump slash from above, you
                    can reach the Bomb Bag area as only child
                    without needing a Slingshot. You will
                    take fall damage.
                    '''},
    "Dodongo's Cavern MQ Light the Eyes with Strength as Child": {
        'name'    : 'logic_dc_mq_eyes_child',
        'tags'    : ("Dodongo's Cavern", "MQ",),
        'tooltip' : '''\
                    If you move very quickly, it is possible to use
                    the bomb flower at the top of the room to light
                    the eyes. To perform this trick as child is
                    significantly more difficult than adult. The
                    player is also expected to complete the DC back
                    area without explosives, including getting past
                    the Armos wall to the switch for the boss door.
                    '''},
    "Dodongo's Cavern MQ Light the Eyes with Strength as Adult": {
        'name'    : 'logic_dc_mq_eyes_adult',
        'tags'    : ("Dodongo's Cavern", "MQ",),
        'tooltip' : '''\
                    If you move very quickly, it is possible to use
                    the bomb flower at the top of the room to light
                    the eyes.
                    '''},
    'Jabu Underwater Alcove as Adult with Jump Dive': {
        'name'    : 'logic_jabu_alcove_jump_dive',
        'tags'    : ("Jabu Jabu's Belly", "Entrance", "MQ",),
        'tooltip' : '''\
                    Standing above the underwater tunnel leading to the scrub,
                    jump down and swim through the tunnel. This allows adult to
                    access the alcove with no Scale or Iron Boots. In vanilla Jabu,
                    this alcove has a business scrub. In MQ Jabu, it has the compass
                    chest and a door switch for the main floor.
                    '''},
    'Jabu Near Boss Room with Hover Boots': {
        'name'    : 'logic_jabu_boss_hover',
        'tags'    : ("Jabu Jabu's Belly", "Skulltulas", "Entrance",),
        'tooltip' : '''\
                    A box for the blue switch can be carried over
                    by backwalking with one while the elevator is
                    at its peak. Alternatively, you can skip
                    transporting a box by quickly rolling from the
                    switch and opening the door before it closes.
                    However, the timing for this is very tight.
                    '''},
    'Jabu Near Boss Ceiling Switch/GS without Boomerang or Explosives': {
        'name'    : 'logic_jabu_near_boss_ranged',
        'tags'    : ("Jabu Jabu's Belly", "Skulltulas", "Entrance", "MQ",),
        'tooltip' : '''\
                    Vanilla Jabu: From near the entrance into the room, you can
                    hit the switch that opens the door to the boss room using a
                    precisely-aimed use of the Slingshot, Bow, or Longshot. As well,
                    if you climb to the top of the vines you can stand on the right
                    edge of the platform and shoot around the glass. From this
                    distance, even the Hookshot can reach the switch. This trick is
                    only relevant if "Shuffle Boss Entrances" is enabled.

                    MQ Jabu: A Gold Skulltula Token can be collected with the
                    Hookshot or Longshot using the same methods as hitting the switch
                    in vanilla. This trick is usually only relevant if Jabu dungeon
                    shortcuts are enabled.
                    '''},                    
    'Jabu Near Boss Ceiling Switch with Explosives': {
        'name'    : 'logic_jabu_near_boss_explosives',
        'tags'    : ("Jabu Jabu's Belly", "Entrance",),
        'tooltip' : '''\
                    You can hit the switch that opens the door to the boss
                    room using a precisely-aimed Bombchu. Also, using the
                    Hover Boots, adult can throw a Bomb at the switch. This
                    trick is only relevant if "Shuffle Boss Entrances" is
                    enabled.
                    '''},
    'Jabu MQ without Lens of Truth': {
        'name'    : 'logic_lens_jabu_mq',
        'tags'    : ("Lens of Truth", "Jabu Jabu's Belly", "MQ",),
        'tooltip' : '''\
                    Removes the requirements for the Lens of Truth
                    in Jabu MQ.
                    '''},                                      
    'Jabu MQ Compass Chest with Boomerang': {
        'name'    : 'logic_jabu_mq_rang_jump',
        'tags'    : ("Jabu Jabu's Belly", "MQ",),
        'tooltip' : '''\
                    Boomerang can reach the cow switch to spawn the chest by
                    targeting the cow, jumping off of the ledge where the
                    chest spawns, and throwing the Boomerang in midair. This
                    is only relevant with Jabu Jabu's Belly dungeon shortcuts
                    enabled.
                    '''},
    'Jabu MQ Song of Time Block GS with Boomerang': {
        'name'    : 'logic_jabu_mq_sot_gs',
        'tags'    : ("Jabu Jabu's Belly", "Skulltulas", "MQ",),
        'tooltip' : '''\
                    Allow the Boomerang to return to you through
                    the Song of Time block to grab the token.
                    '''},
    'Bottom of the Well without Lens of Truth': {
        'name'    : 'logic_lens_botw',
        'tags'    : ("Lens of Truth", "Bottom of the Well",),
        'tooltip' : '''\
                    Removes the requirements for the Lens of Truth
                    in Bottom of the Well.
                    '''},
    'Child Dead Hand without Kokiri Sword': {
        'name'    : 'logic_child_deadhand',
        'tags'    : ("Bottom of the Well",),
        'tooltip' : '''\
                    Requires 9 sticks or 5 jump slashes.
                    '''},   
    'Bottom of the Well Map Chest with Strength & Sticks': {
        'name'    : 'logic_botw_basement',
        'tags'    : ("Bottom of the Well",),
        'tooltip' : '''\
                    The chest in the basement can be reached with
                    strength by doing a jump slash with a lit
                    stick to access the bomb flowers.
                    '''},
    'Bottom of the Well MQ Jump Over the Pits': {
        'name'    : 'logic_botw_mq_pits',
        'tags'    : ("Bottom of the Well", "MQ",),
        'tooltip' : '''\
                    While the pits in Bottom of the Well don't allow you to
                    jump just by running straight at them, you can still get
                    over them by side-hopping or backflipping across. With
                    explosives, this allows you to access the central areas
                    without Zelda's Lullaby. With Zelda's Lullaby, it allows
                    you to access the west inner room without explosives.
                    '''},
    'Bottom of the Well MQ Dead Hand Freestanding Key with Boomerang': {
        'name'    : 'logic_botw_mq_dead_hand_key',
        'tags'    : ("Bottom of the Well", "MQ",),
        'tooltip' : '''\
                    Boomerang can fish the item out of the rubble without
                    needing explosives to blow it up.
                    '''},
    'Forest Temple First Room GS with Difficult-to-Use Weapons': {
        'name'    : 'logic_forest_first_gs',
        'tags'    : ("Forest Temple", "Entrance", "Skulltulas",),
        'tooltip' : '''\
                    Allows killing this Skulltula with Sword or Sticks by
                    jump slashing it as you let go from the vines. You can
                    avoid taking fall damage by recoiling onto the tree.
                    Also allows killing it as Child with a Bomb throw. It's
                    much more difficult to use a Bomb as child due to
                    Child Link's shorter height.
                    '''},
    'Forest Temple East Courtyard GS with Boomerang': {
        'name'    : 'logic_forest_outdoor_east_gs',
        'tags'    : ("Forest Temple", "Entrance", "Skulltulas",),
        'tooltip' : '''\
                    Precise Boomerang throws can allow child to
                    kill the Skulltula and collect the token.
                    '''},                                      
    'Forest Temple East Courtyard Vines with Hookshot': {
        'name'    : 'logic_forest_vines',
        'tags'    : ("Forest Temple", "MQ",),
        'tooltip' : '''\
                    The vines in Forest Temple leading to where the well
                    drain switch is in the standard form can be barely
                    reached with just the Hookshot. Applies to MQ also.
                    '''},
    'Forest Temple NE Outdoors Ledge with Hover Boots': {
        'name'    : 'logic_forest_outdoors_ledge',
        'tags'    : ("Forest Temple", "Entrance", "MQ",),
        'tooltip' : '''\
                    With precise Hover Boots movement you can fall down
                    to this ledge from upper balconies. If done precisely
                    enough, it is not necessary to take fall damage.
                    In MQ, this skips a Longshot requirement.
                    In Vanilla, this can skip a Hookshot requirement in
                    entrance randomizer.
                    '''},
    'Forest Temple East Courtyard Door Frame with Hover Boots': {
        'name'    : 'logic_forest_door_frame',
        'tags'    : ("Forest Temple", "MQ",),
        'tooltip' : '''\
                    A precise Hover Boots movement from the upper
                    balconies in this courtyard can be used to get on
                    top of the door frame. Applies to both Vanilla and
                    Master Quest. In Vanilla, from on top the door
                    frame you can summon Pierre, allowing you to access
                    the falling ceiling room early. In Master Quest,
                    this allows you to obtain the GS on the door frame
                    as adult without Hookshot or Song of Time.
                    '''},                    
    'Forest Temple Outside Backdoor with Jump Slash': {
        'name'    : 'logic_forest_outside_backdoor',
        'tags'    : ("Forest Temple", "MQ",),
        'tooltip' : '''\
                    A jump slash recoil can be used to reach the
                    ledge in the block puzzle room that leads to
                    the west courtyard. This skips a potential
                    Hover Boots requirement in vanilla, and it
                    can sometimes apply in MQ as well. This trick
                    can be performed as both ages.
                    '''},
    'Swim Through Forest Temple MQ Well with Hookshot': {
        'name'    : 'logic_forest_well_swim',
        'tags'    : ("Forest Temple", "MQ",),
        'tooltip' : '''\
                    Shoot the vines in the well as low and as far to
                    the right as possible, and then immediately swim
                    under the ceiling to the right. This can only be
                    required if Forest Temple is in its Master Quest
                    form.
                    '''},
    'Skip Forest Temple MQ Block Puzzle with Bombchu': {
        'name'    : 'logic_forest_mq_block_puzzle',
        'tags'    : ("Forest Temple", "MQ",),
        'tooltip' : '''\
                    Send the Bombchu straight up the center of the
                    wall directly to the left upon entering the room.
                    '''},                    
    'Forest Temple MQ Twisted Hallway Switch with Jump Slash': {
        'name'    : 'logic_forest_mq_hallway_switch_jumpslash',
        'tags'    : ("Forest Temple", "MQ",),
        'tooltip' : '''\
                    The switch to twist the hallway can be hit with
                    a jump slash through the glass block. To get in
                    front of the switch, either use the Hover Boots
                    or hit the shortcut switch at the top of the
                    room and jump from the glass blocks that spawn.
                    Sticks can be used as child, but the Kokiri
                    Sword is too short to reach through the glass.
                    '''},
    #'Forest Temple MQ Twisted Hallway Switch with Hookshot': {
    #    'name'    : 'logic_forest_mq_hallway_switch_hookshot',
    #    'tags'    : ("Forest Temple", "MQ",),
    #    'tooltip' : '''\
    #                There's a very small gap between the glass block
    #                and the wall. Through that gap you can hookshot
    #                the target on the ceiling.
    #                '''},
    'Forest Temple MQ Twisted Hallway Switch with Boomerang': {
        'name'    : 'logic_forest_mq_hallway_switch_boomerang',
        'tags'    : ("Forest Temple", "Entrance", "MQ",),
        'tooltip' : '''\
                    The Boomerang can return to Link through walls,
                    allowing child to hit the hallway switch. This
                    can be used to allow adult to pass through later,
                    or in conjuction with "Forest Temple Outside
                    Backdoor with Jump Slash".
                    '''},
    'Fire Temple Boss Door without Hover Boots or Pillar': {
        'name'    : 'logic_fire_boss_door_jump',
        'tags'    : ("Fire Temple", "MQ",),
        'tooltip' : '''\
                    The Fire Temple Boss Door can be reached with a precise
                    jump. You must be touching the side wall of the room so
                    that Link will grab the ledge from farther away than
                    is normally possible.
                    '''},
    'Fire Temple Song of Time Room GS without Song of Time': {
        'name'    : 'logic_fire_song_of_time',
        'tags'    : ("Fire Temple", "Skulltulas",),
        'tooltip' : '''\
                    A precise jump can be used to reach this room.
                    '''},
    'Fire Temple Climb without Strength': {
        'name'    : 'logic_fire_strength',
        'tags'    : ("Fire Temple",),
        'tooltip' : '''\
                    A precise jump can be used to skip
                    pushing the block.
                    '''},
    "Fire Temple East Tower without Scarecrow's Song": {
        'name'    : 'logic_fire_scarecrow',
        'tags'    : ("Fire Temple",),
        'tooltip' : '''\
                    Also known as "Pixelshot".
                    The Longshot can reach the target on the elevator
                    itself, allowing you to skip needing to spawn the
                    scarecrow.
                    '''},
    'Fire Temple Flame Wall Maze Skip': {
        'name'    : 'logic_fire_flame_maze',
        'tags'    : ("Fire Temple",),
        'tooltip' : '''\
                    If you move quickly you can sneak past the edge of
                    a flame wall before it can rise up to block you.
                    To do it without taking damage is more precise.
                    Allows you to progress without needing either a
                    Small Key or Hover Boots.
                    '''},
    'Fire Temple MQ Chest Near Boss without Breaking Crate': {
        'name'    : 'logic_fire_mq_near_boss',
        'tags'    : ("Fire Temple", "MQ",),
        'tooltip' : '''\
                    The hitbox for the torch extends a bit outside of the crate.
                    Shoot a flaming arrow at the side of the crate to light the
                    torch without needing to get over there and break the crate.
                    '''},
    'Fire Temple MQ Big Lava Room Blocked Door without Hookshot': {
        'name'    : 'logic_fire_mq_blocked_chest',
        'tags'    : ("Fire Temple", "MQ",),
        'tooltip' : '''\
                    There is a gap between the hitboxes of the flame
                    wall in the big lava room. If you know where this
                    gap is located, you can jump through it and skip
                    needing to use the Hookshot. To do this without
                    taking damage is more precise.
                    '''},
    'Fire Temple MQ Boss Key Chest without Bow': {
        'name'    : 'logic_fire_mq_bk_chest',
        'tags'    : ("Fire Temple", "MQ",),
        'tooltip' : '''\
                    It is possible to light both of the timed torches
                    to unbar the door to the boss key chest's room
                    with just Din's Fire if you move very quickly
                    between the two torches. It is also possible to
                    unbar the door with just Din's by abusing an
                    oversight in the way the game counts how many
                    torches have been lit.
                    '''},
    'Fire Temple MQ Climb without Fire Source': {
        'name'    : 'logic_fire_mq_climb',
        'tags'    : ("Fire Temple", "MQ",),
        'tooltip' : '''\
                    You can use the Hover Boots to hover around to
                    the climbable wall, skipping the need to use a
                    fire source and spawn a Hookshot target.
                    '''},
    'Fire Temple MQ Lizalfos Maze Side Room without Box': {
        'name'    : 'logic_fire_mq_maze_side_room',
        'tags'    : ("Fire Temple", "MQ",),
        'tooltip' : '''\
                    You can walk from the blue switch to the door and
                    quickly open the door before the bars reclose. This
                    skips needing to reach the upper sections of the
                    maze to get a box to place on the switch.
                    '''},
    'Fire Temple MQ Lower to Upper Lizalfos Maze with Hover Boots': {
        'name'    : 'logic_fire_mq_maze_hovers',
        'tags'    : ("Fire Temple", "MQ",),
        'tooltip' : '''\
                    Use the Hover Boots off of a crate to
                    climb to the upper maze without needing
                    to spawn and use the Hookshot targets.
                    '''},
    'Fire Temple MQ Lower to Upper Lizalfos Maze with Precise Jump': {
        'name'    : 'logic_fire_mq_maze_jump',
        'tags'    : ("Fire Temple", "MQ",),
        'tooltip' : '''\
                    A precise jump off of a crate can be used to
                    climb to the upper maze without needing to spawn
                    and use the Hookshot targets. This trick
                    supersedes both "Fire Temple MQ Lower to Upper
                    Lizalfos Maze with Hover Boots" and "Fire Temple
                    MQ Lizalfos Maze Side Room without Box".
                    '''},
    'Fire Temple MQ Above Flame Wall Maze GS from Below with Longshot': {
        'name'    : 'logic_fire_mq_above_maze_gs',
        'tags'    : ("Fire Temple", "Skulltulas", "MQ",),
        'tooltip' : '''\
                    The floor of the room that contains this Skulltula
                    is only solid from above. From the maze below, the
                    Longshot can be shot through the ceiling to obtain 
                    the token with two fewer small keys than normal.
                    '''},                    
    'Fire Temple MQ Flame Wall Maze Skip': {
        'name'    : 'logic_fire_mq_flame_maze',
        'tags'    : ("Fire Temple", "Skulltulas", "MQ",),
        'tooltip' : '''\
                    If you move quickly you can sneak past the edge of
                    a flame wall before it can rise up to block you.
                    To do it without taking damage is more precise.
                    Allows you to reach the side room GS without needing
                    Song of Time or Hover Boots. If either of "Fire Temple
                    MQ Lower to Upper Lizalfos Maze with Hover Boots" or
                    "with Precise Jump" are enabled, this also allows you
                    to progress deeper into the dungeon without Hookshot.
                    '''},
    'Water Temple Torch Longshot': {
        'name'    : 'logic_water_temple_torch_longshot',
        'tags'    : ("Water Temple",),
        'tooltip' : '''\
                    Stand on the eastern side of the central pillar and longshot
                    the torches on the bottom level. Swim through the corridor
                    and float up to the top level. This allows access to this
                    area and lower water levels without Iron Boots.
                    The majority of the tricks that allow you to skip Iron Boots
                    in the Water Temple are not going to be relevant unless this
                    trick is first enabled.
                    '''},
    'Water Temple Cracked Wall with Hover Boots': {
        'name'    : 'logic_water_cracked_wall_hovers',
        'tags'    : ("Water Temple",),
        'tooltip' : '''\
                    With a midair side-hop while wearing the Hover
                    Boots, you can reach the cracked wall without
                    needing to raise the water up to the middle level.
                    '''},
    'Water Temple Cracked Wall with No Additional Items': {
        'name'    : 'logic_water_cracked_wall_nothing',
        'tags'    : ("Water Temple",),
        'tooltip' : '''\
                    A precise jump slash (among other methods) will
                    get you to the cracked wall without needing the
                    Hover Boots or to raise the water to the middle
                    level. This trick supersedes "Water Temple
                    Cracked Wall with Hover Boots".
                    '''},
    'Water Temple Boss Key Region with Hover Boots': {
        'name'    : 'logic_water_boss_key_region',
        'tags'    : ("Water Temple",),
        'tooltip' : '''\
                    With precise Hover Boots movement it is possible
                    to reach the boss key chest's region without
                    needing the Longshot. It is not necessary to take
                    damage from the spikes. The Gold Skulltula Token
                    in the following room can also be obtained with
                    just the Hover Boots.
                    '''},
    'Water Temple North Basement Ledge with Precise Jump': {
        'name'    : 'logic_water_north_basement_ledge_jump',
        'tags'    : ("Water Temple", "MQ",),
        'tooltip' : '''\
                    In the northern basement there's a ledge from where, in
                    vanilla Water Temple, boulders roll out into the room.
                    Normally to jump directly to this ledge logically
                    requires the Hover Boots, but with precise jump, it can
                    be done without them. This trick applies to both
                    Vanilla and Master Quest.
                    '''},
    'Water Temple Boss Key Jump Dive': {
        'name'    : 'logic_water_bk_jump_dive',
        'tags'    : ("Water Temple",),
        'tooltip' : '''\
                    Stand on the very edge of the raised corridor leading from the
                    push block room to the rolling boulder corridor. Face the
                    gold skulltula on the waterfall and jump over the boulder
                    corridor floor into the pool of water, swimming right once
                    underwater. This allows access to the boss key room without
                    Iron boots.
                    '''},
    "Water Temple Central Pillar GS with Farore's Wind": {
        'name'    : 'logic_water_central_gs_fw',
        'tags'    : ("Water Temple", "Skulltulas",),
        'tooltip' : '''\
                    If you set Farore's Wind inside the central pillar
                    and then return to that warp point after raising
                    the water to the highest level, you can obtain this
                    Skulltula Token with Hookshot or Boomerang.
                    '''},
    'Water Temple Central Pillar GS with Iron Boots': {
        'name'    : 'logic_water_central_gs_irons',
        'tags'    : ("Water Temple", "Skulltulas",),
        'tooltip' : '''\
                    After opening the middle water level door into the
                    central pillar, the door will stay unbarred so long
                    as you do not leave the room -- even if you were to
                    raise the water up to the highest level. With the
                    Iron Boots to go through the door after the water has
                    been raised, you can obtain the Skulltula Token with
                    the Hookshot.
                    '''},                    
    'Water Temple Central Bow Target without Longshot or Hover Boots': {
        'name'    : 'logic_water_central_bow',
        'tags'    : ("Water Temple",),
        'tooltip' : '''\
                    A very precise Bow shot can hit the eye
                    switch from the floor above. Then, you
                    can jump down into the hallway and make
                    through it before the gate closes.
                    It can also be done as child, using the
                    Slingshot instead of the Bow.
                    '''},
    'Water Temple Falling Platform Room GS with Hookshot': {
        'name'    : 'logic_water_falling_platform_gs_hookshot',
        'tags'    : ("Water Temple", "Skulltulas",),
        'tooltip' : '''\
                    If you stand on the very edge of the platform, this
                    Gold Skulltula can be obtained with only the Hookshot.
                    '''},
    'Water Temple Falling Platform Room GS with Boomerang': {
        'name'    : 'logic_water_falling_platform_gs_boomerang',
        'tags'    : ("Water Temple", "Skulltulas", "Entrance",),
        'tooltip' : '''\
                    If you stand on the very edge of the platform, this
                    Gold Skulltula can be obtained with only the Boomerang.
                    '''},
    'Water Temple River GS without Iron Boots': {
        'name'    : 'logic_water_river_gs',
        'tags'    : ("Water Temple", "Skulltulas",),
        'tooltip' : '''\
                    Standing on the exposed ground toward the end of
                    the river, a precise Longshot use can obtain the
                    token. The Longshot cannot normally reach far
                    enough to kill the Skulltula, however. You'll
                    first have to find some other way of killing it.
                    '''},
    'Water Temple Dragon Statue Jump Dive': {
        'name'    : 'logic_water_dragon_jump_dive',
        'tags'    : ("Water Temple", "MQ",),
        'tooltip' : '''\
                    If you come into the dragon statue room from the
                    serpent river, you can jump down from above and get
                    into the tunnel without needing either Iron Boots
                    or a Scale. This trick applies to both Vanilla and
                    Master Quest. In Vanilla, you must shoot the switch
                    from above with the Bow, and then quickly get
                    through the tunnel before the gate closes.
                    '''},
    'Water Temple Dragon Statue Switch from Above the Water as Adult': {
        'name'    : 'logic_water_dragon_adult',
        'tags'    : ("Water Temple",),
        'tooltip' : '''\
                    Normally you need both Hookshot and Iron Boots to hit the
                    switch and swim through the tunnel to get to the chest. But
                    by hitting the switch from dry land, using one of Bombchus,
                    Hookshot, or Bow, it is possible to skip one or both of
                    those requirements. After the gate has been opened, besides 
                    just using the Iron Boots, a well-timed dive with at least
                    the Silver Scale could be used to swim through the tunnel. If
                    coming from the serpent river, a jump dive can also be used
                    to get into the tunnel.
                    '''},
    'Water Temple Dragon Statue Switch from Above the Water as Child': {
        'name'    : 'logic_water_dragon_child',
        'tags'    : ("Water Temple", "Entrance",),
        'tooltip' : '''\
                    It is possible for child to hit the switch from dry land
                    using one of Bombchus, Slingshot or Boomerang. Then, to
                    get to the chest, child can dive through the tunnel using
                    at least the Silver Scale. The timing and positioning of
                    this dive needs to be perfect to actually make it under the
                    gate, and it all needs to be done very quickly to be able to
                    get through before the gate closes. Be sure to enable "Water
                    Temple Dragon Statue Switch from Above the Water as Adult"
                    for adult's variant of this trick.
                    '''},
    'Water Temple MQ Central Pillar with Fire Arrows': {
        'name'    : 'logic_water_mq_central_pillar',
        'tags'    : ("Water Temple", "MQ",),
        'tooltip' : '''\
                    Slanted torches have misleading hitboxes. Whenever
                    you see a slanted torch jutting out of the wall,
                    you can expect most or all of its hitbox is actually
                    on the other side that wall. This can make slanted
                    torches very finicky to light when using arrows. The
                    torches in the central pillar of MQ Water Temple are
                    a particularly egregious example. Logic normally
                    expects Din's Fire and Song of Time.
                    '''},
    'Water Temple MQ North Basement GS without Small Key': {
        'name'    : 'logic_water_mq_locked_gs',
        'tags'    : ("Water Temple", "Skulltulas", "MQ",),
        'tooltip' : '''\
                    There is an invisible Hookshot target that can be used
                    to get over the gate that blocks you from going to this
                    Skulltula early, skipping a small key as well as
                    needing Hovers or Scarecrow to reach the locked door.
                    '''},
    'Shadow Temple Stationary Objects without Lens of Truth': {
        'name'    : 'logic_lens_shadow',
        'tags'    : ("Lens of Truth", "Shadow Temple",),
        'tooltip' : '''\
                    Removes the requirements for the Lens of Truth
                    in Shadow Temple for most areas in the dungeon
                    except for crossing the moving platform in the huge
                    pit room and for fighting Bongo Bongo.
                    '''},
    'Shadow Temple Invisible Moving Platform without Lens of Truth': {
        'name'    : 'logic_lens_shadow_platform',
        'tags'    : ("Lens of Truth", "Shadow Temple",),
        'tooltip' : '''\
                    Removes the requirements for the Lens of Truth
                    in Shadow Temple to cross the invisible moving
                    platform in the huge pit room in either direction.
                    '''},
    'Shadow Temple Bongo Bongo without Lens of Truth': {
        'name'    : 'logic_lens_bongo',
        'tags'    : ("Shadow Temple", "Entrance", "MQ",),
        'tooltip' : '''\
                    Bongo Bongo can be defeated without the use of
                    Lens of Truth, as the hands give a pretty good
                    idea of where the eye is.
                    '''},
    'Shadow Temple Stone Umbrella Skip': {
        'name'    : 'logic_shadow_umbrella',
        'tags'    : ("Shadow Temple", "MQ",),
        'tooltip' : '''\
                    A very precise Hover Boots movement
                    from off of the lower chest can get you
                    on top of the crushing spikes without
                    needing to pull the block. Applies to
                    both Vanilla and Master Quest.
                    '''},
    'Shadow Temple Falling Spikes GS with Hover Boots': {
        'name'    : 'logic_shadow_umbrella_gs',
        'tags'    : ("Shadow Temple", "Skulltulas", "MQ",),
        'tooltip' : '''\
                    After killing the Skulltula, a very precise Hover Boots
                    movement from off of the lower chest can get you on top
                    of the crushing spikes without needing to pull the block.
                    From there, another very precise Hover Boots movement can
                    be used to obtain the token without needing the Hookshot.
                    Applies to both Vanilla and Master Quest. For obtaining
                    the chests in this room with just Hover Boots, be sure to
                    enable "Shadow Temple Stone Umbrella Skip".
                    '''},                    
    'Shadow Temple Freestanding Key with Bombchu': {
        'name'    : 'logic_shadow_freestanding_key',
        'tags'    : ("Shadow Temple",),
        'tooltip' : '''\
                    Release the Bombchu with good timing so that
                    it explodes near the bottom of the pot.
                    '''},
    'Shadow Temple River Statue with Bombchu': {
        'name'    : 'logic_shadow_statue',
        'tags'    : ("Shadow Temple", "MQ",),
        'tooltip' : '''\
                    By sending a Bombchu around the edge of the
                    gorge, you can knock down the statue without
                    needing a Bow.
                    Applies in both vanilla and MQ Shadow.
                    '''},
    'Shadow Temple Bongo Bongo without projectiles': {
        'name'    : 'logic_shadow_bongo',
        'tags'    : ("Shadow Temple", "Entrance",),
        'tooltip' : '''\
                    Using precise sword slashes, Bongo Bongo can be
                    defeated without using projectiles. This is
                    only relevant in conjunction with Shadow Temple
                    dungeon shortcuts or shuffled boss entrances.
                    '''},
    'Shadow Temple MQ Stationary Objects without Lens of Truth': {
        'name'    : 'logic_lens_shadow_mq',
        'tags'    : ("Lens of Truth", "Shadow Temple", "MQ",),
        'tooltip' : '''\
                    Removes the requirements for the Lens of Truth
                    in Shadow Temple MQ for most areas in the dungeon.
                    See "Shadow Temple MQ Invisible Moving Platform
                    without Lens of Truth", "Shadow Temple MQ Invisible
                    Blades Silver Rupees without Lens of Truth",
                    "Shadow Temple MQ 2nd Dead Hand without Lens of Truth",
                    and "Shadow Temple Bongo Bongo without Lens of Truth"
                    for exceptions.
                    '''},
    'Shadow Temple MQ Invisible Blades Silver Rupees without Lens of Truth': {
        'name'    : 'logic_lens_shadow_mq_invisible_blades',
        'tags'    : ("Lens of Truth", "Shadow Temple", "MQ",),
        'tooltip' : '''\
                    Removes the requirement for the Lens of Truth or
                    Nayru's Love in Shadow Temple MQ for the Invisible
                    Blades room silver rupee collection.
                    '''},                    
    'Shadow Temple MQ Invisible Moving Platform without Lens of Truth': {
        'name'    : 'logic_lens_shadow_mq_platform',
        'tags'    : ("Lens of Truth", "Shadow Temple", "MQ",),
        'tooltip' : '''\
                    Removes the requirements for the Lens of Truth
                    in Shadow Temple MQ to cross the invisible moving
                    platform in the huge pit room in either direction.
                    '''},
    'Shadow Temple MQ 2nd Dead Hand without Lens of Truth': {
        'name'    : 'logic_lens_shadow_mq_dead_hand',
        'tags'    : ("Lens of Truth", "Shadow Temple", "MQ",),
        'tooltip' : '''\
                    Dead Hand spawns in a random spot within the room.
                    Having Lens removes the hassle of having to comb
                    the room looking for his spawn location.
                    '''},
    'Shadow Temple MQ Truth Spinner Gap with Longshot': {
        'name'    : 'logic_shadow_mq_gap',
        'tags'    : ("Shadow Temple", "MQ",),
        'tooltip' : '''\
                    You can Longshot a torch and jump-slash recoil onto
                    the tongue. It works best if you Longshot the right
                    torch from the left side of the room.
                    '''},
    'Shadow Temple MQ Invisible Blades without Song of Time': {
        'name'    : 'logic_shadow_mq_invisible_blades',
        'tags'    : ("Shadow Temple", "MQ",),
        'tooltip' : '''\
                    The Like Like can be used to boost you into the
                    silver rupee or recovery hearts that normally
                    require Song of Time. This cannot be performed
                    on OHKO since the Like Like does not boost you
                    high enough if you die.
                    '''},
    'Shadow Temple MQ Lower Huge Pit without Fire Source': {
        'name'    : 'logic_shadow_mq_huge_pit',
        'tags'    : ("Shadow Temple", "MQ",),
        'tooltip' : '''\
                    Normally a frozen eye switch spawns some platforms
                    that you can use to climb down, but there's actually
                    a small piece of ground that you can stand on that
                    you can just jump down to.
                    '''},
    'Shadow Temple MQ Windy Walkway Reverse without Hover Boots': {
        'name'    : 'logic_shadow_mq_windy_walkway',
        'tags'    : ("Shadow Temple", "MQ",),
        'tooltip' : '''\
                    With shadow dungeon shortcuts enabled, it is possible
                    to jump from the alcove in the windy hallway to the
                    middle platform. There are two methods: wait out the fan
                    opposite the door and hold forward, or jump to the right
                    to be pushed by the fan there towards the platform ledge.
                    Note that jumps of this distance are inconsistent, but
                    still possible.
                    '''},
    'Spirit Temple without Lens of Truth': {
        'name'    : 'logic_lens_spirit',
        'tags'    : ("Lens of Truth", "Spirit Temple",),
        'tooltip' : '''\
                    Removes the requirements for the Lens of Truth
                    in Spirit Temple.
                    '''},
    'Spirit Temple Child Side Bridge with Bombchu': {
        'name'    : 'logic_spirit_child_bombchu',
        'tags'    : ("Spirit Temple",),
        'tooltip' : '''\
                    A carefully-timed Bombchu can hit the switch.
                    '''},
    'Spirit Temple Main Room GS with Boomerang': {
        'name'    : 'logic_spirit_lobby_gs',
        'tags'    : ("Spirit Temple", "Skulltulas",),
        'tooltip' : '''\
                    Standing on the highest part of the arm of the statue, a
                    precise Boomerang throw can kill and obtain this Gold
                    Skulltula. You must throw the Boomerang slightly off to
                    the side so that it curves into the Skulltula, as aiming
                    directly at it will clank off of the wall in front.
                    '''},                    
    'Spirit Temple Lower Adult Switch with Bombs': {
        'name'    : 'logic_spirit_lower_adult_switch',
        'tags'    : ("Spirit Temple",),
        'tooltip' : '''\
                    A bomb can be used to hit the switch on the ceiling,
                    but it must be thrown from a particular distance
                    away and with precise timing.
                    '''},
    'Spirit Temple Main Room Jump from Hands to Upper Ledges': {
        'name'    : 'logic_spirit_lobby_jump',
        'tags'    : ("Spirit Temple", "Skulltulas", "MQ",),
        'tooltip' : '''\
                    A precise jump to obtain the following as adult
                    without needing one of Hover Boots, or Hookshot
                    (in vanilla) or Song of Time (in MQ):
                    - Spirit Temple Statue Room Northeast Chest
                    - Spirit Temple GS Lobby
                    - Spirit Temple MQ Central Chamber Top Left Pot 1
                    - Spirit Temple MQ Central Chamber Top Left Pot 2
                    '''},
    'Spirit Temple Main Room Hookshot to Boss Platform': {
        'name'    : 'logic_spirit_platform_hookshot',
        'tags'    : ("Spirit Temple",),
        'tooltip' : '''\
                    Precise hookshot aiming at the platform chains can be
                    used to reach the boss platform from the middle landings.
                    Using a jump slash immediately after reaching a chain
                    makes aiming more lenient. Relevant only when Spirit
                    Temple boss shortcuts are on.
                    '''},
    'Spirit Temple Map Chest with Bow': {
        'name'    : 'logic_spirit_map_chest',
        'tags'    : ("Spirit Temple",),
        'tooltip' : '''\
                    To get a line of sight from the upper torch to
                    the map chest torches, you must pull an Armos
                    statue all the way up the stairs.
                    '''},
    'Spirit Temple Sun Block Room Chest with Bow': {
        'name'    : 'logic_spirit_sun_chest',
        'tags'    : ("Spirit Temple",),
        'tooltip' : '''\
                    Using the blocks in the room as platforms you can
                    get lines of sight to all three torches. The timer
                    on the torches is quite short so you must move
                    quickly in order to light all three.
                    '''},
    'Spirit Temple Shifting Wall with No Additional Items': {
        'name'    : 'logic_spirit_wall',
        'tags'    : ("Spirit Temple",),
        'tooltip' : '''\
                    Logic normally guarantees a way of dealing with both
                    the Beamos and the Walltula before climbing the wall.
                    '''},
    'Spirit Temple MQ without Lens of Truth': {
        'name'    : 'logic_lens_spirit_mq',
        'tags'    : ("Lens of Truth", "Spirit Temple", "MQ",),
        'tooltip' : '''\
                    Removes the requirements for the Lens of Truth
                    in Spirit Temple MQ.
                    '''},
    'Spirit Temple MQ Sun Block Room as Child without Song of Time': {
        'name'    : 'logic_spirit_mq_sun_block_sot',
        'tags'    : ("Spirit Temple", "MQ",),
        'tooltip' : '''\
                    While adult can easily jump directly to the switch that
                    unbars the door to the sun block room, child Link cannot
                    make the jump without spawning a Song of Time block to
                    jump from. You can skip this by throwing the crate down
                    onto the switch from above, which does unbar the door,
                    however the crate immediately breaks, so you must move
                    quickly to get through the door before it closes back up.
                    '''},
    'Spirit Temple MQ Sun Block Room GS with Boomerang': {
        'name'    : 'logic_spirit_mq_sun_block_gs',
        'tags'    : ("Spirit Temple", "Skulltulas", "MQ",),
        'tooltip' : '''\
                    Throw the Boomerang in such a way that it
                    curves through the side of the glass block
                    to hit the Gold Skulltula.
                    '''},                    
    'Spirit Temple MQ Lower Adult without Fire Arrows': {
        'name'    : 'logic_spirit_mq_lower_adult',
        'tags'    : ("Spirit Temple", "MQ",),
        'tooltip' : '''\
                    By standing in a precise position it is possible to
                    "ight two of the torches with a single use of D"n's
                    Fire. This saves enough time to be able to light all
                    "hree torches with only Di"'s.
                    '''},
    'Spirit Temple MQ Frozen Eye Switch without Fire': {
        'name'    : 'logic_spirit_mq_frozen_eye',
        'tags'    : ("Spirit Temple", "MQ",),
        'tooltip' : '''\
                    You can melt the ice by shooting an arrow through a
                    torch. The only way to find a line of sight for this
                    shot is to first spawn a Song of Time block, and then
                    stand on the very edge of it.
                    '''},
    'Ice Cavern Block Room GS with Hover Boots': {
        'name'    : 'logic_ice_block_gs',
        'tags'    : ("Ice Cavern", "Skulltulas",),
        'tooltip' : '''\
                    The Hover Boots can be used to get in front of the
                    Skulltula to kill it with a jump slash. Then, the
                    Hover Boots can again be used to obtain the Token,
                    all without Hookshot or Boomerang.
                    '''},
    'Ice Cavern MQ Red Ice GS without Song of Time': {
        'name'    : 'logic_ice_mq_red_ice_gs',
        'tags'    : ("Ice Cavern", "Skulltulas", "MQ",),
        'tooltip' : '''\
                    If you side-hop into the perfect position, you
                    can briefly stand on the platform with the red
                    ice just long enough to dump some blue fire.
                    '''},
    'Ice Cavern MQ Scarecrow GS with No Additional Items': {
        'name'    : 'logic_ice_mq_scarecrow',
        'tags'    : ("Ice Cavern", "Skulltulas", "MQ",),
        'tooltip' : '''\
                    A precise jump can be used to reach this alcove.
                    '''},
    'Gerudo Training Ground without Lens of Truth': {
        'name'    : 'logic_lens_gtg',
        'tags'    : ("Lens of Truth", "Gerudo Training Ground",),
        'tooltip' : '''\
                    Removes the requirements for the Lens of Truth
                    in Gerudo Training Ground.
                    '''},
    'Gerudo Training Ground Left Side Silver Rupees without Hookshot': {
        'name'    : 'logic_gtg_without_hookshot',
        'tags'    : ("Gerudo Training Ground",),
        'tooltip' : '''\
                    After collecting the rest of the silver rupees in the room,
                    you can reach the final silver rupee on the ceiling by being
                    pulled up into it after getting grabbed by the Wallmaster.
                    Then, you must also reach the exit of the room without the
                    use of the Hookshot. If you move quickly you can sneak past
                    the edge of a flame wall before it can rise up to block you.
                    To do so without taking damage is more precise.
                    '''},
    'Reach Gerudo Training Ground Fake Wall Ledge with Hover Boots': {
        'name'    : 'logic_gtg_fake_wall',
        'tags'    : ("Gerudo Training Ground", "MQ",),
        'tooltip' : '''\
                    A precise Hover Boots use from the top of the chest can allow
                    you to grab the ledge without needing the usual requirements.
                    In Master Quest, this always skips a Song of Time requirement.
                    In Vanilla, this skips a Hookshot requirement, but is only
                    relevant if "Gerudo Training Ground Left Side Silver Rupees
                    without Hookshot" is enabled.
                    '''},
    'Gerudo Training Ground MQ without Lens of Truth': {
        'name'    : 'logic_lens_gtg_mq',
        'tags'    : ("Lens of Truth", "Gerudo Training Ground", "MQ",),
        'tooltip' : '''\
                    Removes the requirements for the Lens of Truth
                    in Gerudo Training Ground MQ.
                    '''},
    'Gerudo Training Ground MQ Left Side Silver Rupees with Hookshot': {
        'name'    : 'logic_gtg_mq_with_hookshot',
        'tags'    : ("Gerudo Training Ground", "MQ",),
        'tooltip' : '''\
                    The highest silver rupee can be obtained by
                    hookshotting the target and then immediately jump
                    slashing toward the rupee.
                    '''},
    'Gerudo Training Ground MQ Left Side Silver Rupees without Hookshot': {
        'name'    : 'logic_gtg_mq_without_hookshot',
        'tags'    : ("Gerudo Training Ground", "MQ",),
        'tooltip' : '''\
                    After collecting the rest of the silver rupees in the room,
                    you can reach the final silver rupee on the ceiling by being
                    pulled up into it after getting grabbed by the Wallmaster.
                    The Wallmaster will not track you to directly underneath the
                    rupee. You should take the last step to be under the rupee
                    after the Wallmaster has begun its attempt to grab you.
                    Also included with this trick is that fact that the switch
                    that unbars the door to the final chest of GTG can be hit
                    without a projectile, using a precise jump slash.
                    This trick supersedes "Gerudo Training Ground MQ Left Side
                    Silver Rupees with Hookshot".
                    '''},       
    "Ganon's Castle without Lens of Truth": {
        'name'    : 'logic_lens_castle',
        'tags'    : ("Lens of Truth", "Ganon's Castle",),
        'tooltip' : '''\
                    Removes the requirements for the Lens of Truth
                    in Ganon's Castle.
                    '''},
    'Spirit Trial without Hookshot': {
        'name'    : 'logic_spirit_trial_hookshot',
        'tags'    : ("Ganon's Castle",),
        'tooltip' : '''\
                    A precise jump off of an Armos can
                    collect the highest rupee.
                    '''},
    "Ganon's Castle MQ without Lens of Truth": {
        'name'    : 'logic_lens_castle_mq',
        'tags'    : ("Lens of Truth", "Ganon's Castle", "MQ",),
        'tooltip' : '''\
                    Removes the requirements for the Lens of Truth
                    in Ganon's Castle MQ.
                    '''},
    'Fire Trial MQ with Hookshot': {
        'name'    : 'logic_fire_trial_mq',
        'tags'    : ("Ganon's Castle", "MQ",),
        'tooltip' : '''\
                    It's possible to hook the target at the end of
                    fire trial with just Hookshot, but it requires
                    precise aim and perfect positioning. The main
                    difficulty comes from getting on the very corner
                    of the obelisk without falling into the lava.
                    '''},
    'Shadow Trial MQ Torch with Bow': {
        'name'    : 'logic_shadow_trial_mq',
        'tags'    : ("Ganon's Castle", "MQ",),
        'tooltip' : '''\
                    You can light the torch in this room without a fire
                    source by shooting an arrow through the lit torch
                    at the beginning of the room. Because the room is
                    so dark and the unlit torch is so far away, it can
                    be difficult to aim the shot correctly.
                    '''},
    'Light Trial MQ without Hookshot': {
        'name'    : 'logic_light_trial_mq',
        'tags'    : ("Ganon's Castle", "MQ",),
        'tooltip' : '''\
                    If you move quickly you can sneak past the edge of
                    a flame wall before it can rise up to block you.
                    In this case to do it without taking damage is
                    especially precise.
                    '''},
}

normalized_name_tricks = {trick.casefold(): info for (trick, info) in known_logic_tricks.items()}