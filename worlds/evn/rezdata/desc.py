
from typing import Dict, TypedDict

desc_columns = {
    "resource_type": "Resource Type",
    "id": "ID",
    "name": "Name",
    "text": "Text",
    "graphics": "Graphics",
    "movie_file": "Movie File",
    "flags": "Flags",
    "end_of_resource": "End-of-resource"
}

class DescDict(TypedDict, total=False): 
    resource_type: str
    id: int
    name: str
    text: str
    graphics: int
    movie_file: str
    flags: int
    end_of_resource: str

desc_table: Dict[int, DescDict] = {
    3000: {
        "resource_type": "desc",
        "id": "3000",
        "name": "Light Blaster",
        "text": "The various versions of the Pyrogenesis Compound Blaster have been the standard defense armament for Federation ships for the past 300 years.  Utilizing a magnetic containment bottle to collect photon packets before release, the Compound Blaster is capable of generating a kinetic impulse disproportionately large for a weapon of its meager power requirements.  The version designed for small ships, the Light Compound Blaster is easily held by the smallest of fighters.",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3001: {
        "resource_type": "desc",
        "id": "3001",
        "name": "Medium Blaster",
        "text": "Pyrogenesis' midrange product is the unimaginatively named Medium Blaster.  This variant is normally carried by capital ships only; the weight alone makes it difficult for anything smaller to mount it.  While it's slower and more bulky than its lesser sibling, the Medium Blaster is much more powerful.  The lack of a turret mechanism does drop the weight some.\\n\\nRequires: Heavy Weapons License{b424 \\q\\nYou stare at this item, and the others around it, for several long, sad moments, knowing that you may never be able to buy any of them ever again.\\q \\q \\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3002: {
        "resource_type": "desc",
        "id": "3002",
        "name": "LB Turret",
        "text": "The famous Light Blaster, but on a turret which Pyrogenesis copied from its younger rival Rauther.  The turret mechanism is very light and agile, making this an ideal anti-fighter weapon.  Again, this weapon is not able to be mounted on fighters, although independent traders may attempt to mount one on a largish freighter.",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3003: {
        "resource_type": "desc",
        "id": "3003",
        "name": "MB Turret",
        "text": "The Medium Blaster really comes into its own when it becomes turreted.  Combined with sophisticated Glenn:Cyber targeting scopes, these weapons score easy hits on all but the smallest space vessels.  The Medium Blaster Turret does tend to lag a little on the faster capital ships.  The IDA Frigate mounts two of these batteries as standard.\\n\\nRequires: Heavy Weapons License{b424 \\q\\nYou stare at this item, and the others around it, for several long, sad moments, knowing that you may never be able to buy any of them ever again.\\q \\q\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3004: {
        "resource_type": "desc",
        "id": "3004",
        "name": "HB Turret",
        "text": "So big and slow that only a turret mechanism allows it to hit anything at all, the Heavy Blaster Turret is the grand-daddy of the Pyrogenesis line of directed energy firepower.  Mounted as standard on the E-60 Carrier, the pride of the Federation fleet, the Heavy Blaster chews through shields and armor alike.  The short range and slow speed of the enormous packets limit the effectiveness of this weapon at anything other than boarding range.\\n\\nRequires: Heavy Weapons {P30\\qLicense\\q \\qLicense, REQUIRES YOU TO REGISTER EV NOVA\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3005: {
        "resource_type": "desc",
        "id": "3005",
        "name": "QLB Turret",
        "text": "Comprised of quadruple Pyrogenesis Blaster Lasers on the most technically advanced turret they offer, the Quad Light Blaster system comes with a guarantee that it will dispose of your hostile fighter problems once and for all.  Shipboard gunners salivate at the thought of being permanently assigned to one of these beauties.  While the QLB System is heavy, as a point defence weapon system it automatically tracks, without any input from the bridge, incoming missiles and enemy fighter squadrons and pours a truly prodigious amount of fire into them, creating havoc.\\n\\nRequires: Heavy Weapons License, Protective Technologies {P30\\qLicense\\q \\qLicense, REQUIRES YOU TO REGISTER EV NOVA\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3006: {
        "resource_type": "desc",
        "id": "3006",
        "name": "IRM Launcher",
        "text": "Kayel Solutions (KLSol) have won 'Best of Show' 26 years running for their clever adaptation of the Infrared Missile launcher.  Based on the launcher mounted by the F-29 Anaconda and the E-41 Destroyer, the KLSol version is a tightly integrated set of standardized components that can easily swap between a hundred different classes of ship with only a minor, dealer serviceable tweak of the software.  The KLSol IR Missile Launcher does produce a fair amount of heat for such a small unit, but it's easily compensated for.\\n\\nRequires: Missile Weapons License{b424 \\q\\nYou stare at this item, and the others around it, for several long, sad moments, knowing that you may never be able to buy any of them ever again.\\q \\q\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3007: {
        "resource_type": "desc",
        "id": "3007",
        "name": "IR Missile",
        "text": "The Infrared Missile uses the simplest of tracking systems to deliver its small payload.  It's not much to look at, but it's cheap and promiscuously available.  The weapon itself can be loaded into a number of aftermarket launchers, including several highly illegal handheld ones used by Rebellion Vacuum Soldiers.\\n\\nRequires: Missile Weapons License{b424 \\q\\nYou stare at this item, and the others around it, for several long, sad moments, knowing that you may never be able to buy any of them ever again.\\q \\q\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3008: {
        "resource_type": "desc",
        "id": "3008",
        "name": "RM Launcher",
        "text": "GLiMMER, a band of propellerheads turned pro, created the first modern radar guided missile and launcher system way back in 2045 AD.  This design, produced under license by KLSol, is practically identical to that original design, albeit with KLSol's usual software driver genius.  You can mount this unit in any spacefaring vessel with enough expansion space to hold it.  There have even been some reports that it has been successfully incorporated into Auroran vessels!\\n\\nRequires: Missile Weapons License{b424 \\q\\nYou stare at this item, and the others around it, for several long, sad moments, knowing that you may never be able to buy any of them ever again.\\q \\q\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3009: {
        "resource_type": "desc",
        "id": "3009",
        "name": "Radar Missile",
        "text": "Radar as a concept and as a useable weapons guidance system has been around since the middle of the twentieth century AD.  As humanity reached for the stars they brought their technology with them, and radar, which is not reliant on a medium for effectiveness, quickly became a necessary tool for guiding missiles.  This modern radar guided missile is a cheap GLiMMER knock-off.\\n\\nRequires: Missile Weapons License{b424 \\q\\nYou stare at this item, and the others around it, for several long, sad moments, knowing that you may never be able to buy any of them ever again.\\q \\q\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3010: {
        "resource_type": "desc",
        "id": "3010",
        "name": "GM launch",
        "text": "Gravimetric missiles require a very stable and well shielded position from which to get their bearings on a target.  The GLi-tech corporation ( which was formerly known as GLiMMER, before a 120 NC name change for legal purposes) makes and sells the only non-military implementation of the gravimetric missile system.  The monopoly market share that GLi-tech enjoys does not bode well for the price.\\n\\nRequires: Missile Weapons {P30\\qLicense\\q \\qLicense, REQUIRES YOU TO REGISTER EV NOVA\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3011: {
        "resource_type": "desc",
        "id": "3011",
        "name": "Grav missile",
        "text": "Gravimetric missiles lock onto the mass signature of a target.  They cannot be jammed by any known means, and they carry the biggest payload of any missile on the open market.  They are also far and away the most expensive.  For those willing to pay the price, the Gravimetric missile will almost never miss its target, and will destroy smaller ships with one hit.\\n\\nRequires: Missile Weapons {P30\\qLicense\\q \\qLicense, REQUIRES YOU TO REGISTER EV NOVA\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3012: {
        "resource_type": "desc",
        "id": "3012",
        "name": "EW launcher",
        "text": "The launcher for the new Etheric Wake missile is a streamlined unit perhaps as long as three fully grown men.  It contains ultra high-tech cybernetic connectors for the next generation of onboard ship computers, and damping field generators for the positron warhead that the evil-looking missile carries.  Cooling vents longer than baseball bats hiss and squeal as the EW missiles load into place inside it.\\n\\nRequires: Missile Weapons License",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3013: {
        "resource_type": "desc",
        "id": "3013",
        "name": "EW Missile",
        "text": "Because of the unique graviton emissions of the Wraith, a new targetable fire-and-forget weapon had to be devised to combat them.  The Etheric Wake missile uses a little-known principle of subspace disturbance to track Wraith through their flight path by detecting their wash in space-time.  Since the Wraith and the Polaris both use Etheric Wave hyperdrives (although the Wraith version is much more sophisticated), it has been theorized that this weapon will work well versus Polaris jamming.\\n\\nRequires: Missile Weapons License",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3014: {
        "resource_type": "desc",
        "id": "3014",
        "name": "Raven Pod",
        "text": "An underslung rack for the self-loading Raven Rockets.  No guidance system is present; this is simply a holder for the rocket packs.",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3015: {
        "resource_type": "desc",
        "id": "3015",
        "name": "Raven Rocket",
        "text": "Raven Rockets are the simplest chemical explosive projectile you can get.  They are fast, but they have small payloads and are unguided.  Raven Rockets can be devastating when multiple launch systems are installed, and because they have no active targeting systems most 'Point Defense' systems cannot target them.",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3016: {
        "resource_type": "desc",
        "id": "3016",
        "name": "Raven Turret",
        "text": "The Raven Rocket turret mounts two unguided pods on a swivel base.  It comes with a fairly basic tie-in to your vessel's sensors which allows it to track targets.  You'll still need to maneuver fairly well to get the rockets to hit small targets, but these pods allow slower ships to use the Raven.",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3017: {
        "resource_type": "desc",
        "id": "3017",
        "name": "Stellar Grenade Launcher",
        "text": "This weapon is a small airlock mounted in the underside of a ship.  Simply place a grenade in the receptacle provided and then pull the lever.  The airlock will cycle, and then a mechanical arm-launch system will fling the projectile backwards.  The simplicity of the launcher is reflected by its bargain-basement price.",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3018: {
        "resource_type": "desc",
        "id": "3018",
        "name": "Stellar Grenade",
        "text": "The Stellar Grenade is a device designed to throw pursuing ships off your tail.  Dropping a few of these little gems out the hatch will keep adversaries off your tail, or make them regret it if they follow you.  Bigger targets will be slowed a little.",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3019: {
        "resource_type": "desc",
        "id": "3019",
        "name": "Polaron Cannon",
        "text": "Polarons are the new kid on the block in Direct Energy Weapon (DEW) systems.  Polarons pack a punch with little generation loss, although they are hard to control out of the barrel.  In some ways this cannon is rather like a Tesla coil in space, as it arcs rather than fires.  You will need to be close to other ships to use this weapon effectively.  The Polaron generation technology is very new, so it's also very expensive.\\n\\nRequires: Exotic Ships & Weapons License",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3020: {
        "resource_type": "desc",
        "id": "3020",
        "name": "Ion Particle Cannon",
        "text": "The Rauther Power Industries Ion Particle Cannon is amongst the most powerful directed energy weapons in the known galaxy.  Mounted on a 360\u00a1/270\u00a1 firing platform, the weapons accuracy is unmatched, delivering incredibly destructive pulses of stripped helium nuclei, and its rotating phase excels in damaging shields and armor. The only major drawbacks of the Ion Cannon are its heavy power requirement and large mass.\\n\\nRequires: Exotic Ships & Weapons {P30\\qLicense\\q \\qLicense, REQUIRES YOU TO REGISTER EV NOVA\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3021: {
        "resource_type": "desc",
        "id": "3021",
        "name": "FPC",
        "text": "The Fusion Pulse Cannon, like most Aurora technology, is both crude and brutal.  However, the weapon's stocky build and inefficient containment fields still provide a highly effective energy packet.  Perhaps the most interesting feature of the weapon is the fact that the fusion pulses leave the barrel of the weapon while still at meta-reactive temperatures.  It is for this reason that the FPC should not be fired at close range.",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3022: {
        "resource_type": "desc",
        "id": "3022",
        "name": "FPC Turret",
        "text": "As the FPC is cheap and easy to build, the Auroran houses have opted to mount a turreted version of the cannon on almost all ships.  It's rare that you'll find even a freighter without the weapon, in either its forward-firing or its turreted versions.  The turret adds some tracking to the otherwise slow FPC blasts, but the overall design is very effective.  Just ask the Federation military commanders who have lost armadas to this chunky gun.",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3023: {
        "resource_type": "desc",
        "id": "3023",
        "name": "Wraith Cannon",
        "text": "Wraithii are tiny capsules of polarons contained in a mar-graviton field.  A Wraith Cannon fires these capsules via simple biomechanics, and the capsules burst on impact, releasing a powerful kinetic force.  These guns are mounted as standard on the Dragon, and can be retrofitted to most ships on the market.  The Nil'kemorya keep a careful eye on these weapons, however, and only the most favored of outsiders are ever allowed to buy them.",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3024: {
        "resource_type": "desc",
        "id": "3024",
        "name": "Wraithii",
        "text": "The polarons for Wraithii are harvested by deep-space mining scoops run by the Tre'pira.  These polarons are then shipped to P'aedt facilities for encapsulation in the mar-graviton field that will hold them until they impact at a speed of greater than 20 kilometers an hour.  Needless to say, the final packets are handled with kid gloves.  It is a testament to the Tre'pira and the P'aedt that no accidents with Wraithii have ever occurred.",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3025: {
        "resource_type": "desc",
        "id": "3025",
        "name": "Capacitor Pulse Laser",
        "text": "Perhaps the only weapon to require a ship to be built around it, the Capacitor Pulse Laser stores the energy created in Polaris fusion reactors to be discharged in a single beam lasting only a few short seconds.  For that short time, armor and shields may as well be wisps of smoke for all the good they will do against the fury of the most violent energy discharge mankind has yet created.  Arachnids and Scarabs are both built around CPL systems{P30\\q.\\q \\q.\\n\\nREQUIRES YOU TO REGISTER EV NOVA\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3026: {
        "resource_type": "desc",
        "id": "3026",
        "name": "BioRelay Laser",
        "text": "The BioRelay is a thin laser beam weapon mounted in the framework of Striker and Manta vessels.  The BioRelay is a series of cellular storage capacitors that discharge linearly to provide a steady power curve for the beam.  As such, the heat generated from the laser body is minimal, which keeps the size down for the Manta and Striker, and yet packs a punch compared to packeted weapons such as the Federation blasters{P30\\q.\\q \\q.\\n\\nREQUIRES YOU TO REGISTER EV NOVA\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3027: {
        "resource_type": "desc",
        "id": "3027",
        "name": "Polaron Torpedo Tube",
        "text": "This launcher ties into a ship's main computer core (or neural network, in the case of Polaris ships).  It tracks a target ship, and then calculates the complex field generation parameters for the Polaron Flux Coils in the tube.  By varying the quantity, spin and charge of the newly generated polarons, the tube can give the polaron 'virtual structure' a good bead on a target before the preprogrammed field generator in the heart of the energy burst takes over{P30\\q.\\q \\q.\\n\\nREQUIRES YOU TO REGISTER EV NOVA\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3028: {
        "resource_type": "desc",
        "id": "3028",
        "name": "Polaron Torpedo",
        "text": "Having no mass, the Polaron Torpedo is a masterpiece of non-corporeal engineering.  The charge and spin of the huge polaron virtual structure is set by the launcher at firing time.  The chaos mathematics of the field interaction is calculated by the neural net of the Polaris vessel, which makes sure that the field will collapse in such a way that it will steer toward the target from the tube.  A tiny field generator hovering in the middle of the torpedo modifies the field strengths to correct for mid-flight target variations, and provides the only part of the weapon system that has any mass whatsoever{P30\\q.\\q \\q.\\n\\nREQUIRES YOU TO REGISTER EV NOVA\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3029: {
        "resource_type": "desc",
        "id": "3029",
        "name": "Viper bay",
        "text": "A few days is all it takes to convert sections of your ship into a launchbay for Viper fighters.  The conversion comes complete with everything you'll need to refuel, re-arm and service a maximum force of four Vipers.\\n\\nRequires: Fighter Bay {P30\\qLicense\\q \\qLicense, REQUIRES YOU TO REGISTER EV NOVA\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3030: {
        "resource_type": "desc",
        "id": "3030",
        "name": "Viper",
        "text": "With the rapid development of space flight, it was inevitable that sports (particularly racing) would come to fruition sooner rather than later.  Power Sled racing stood up to the challenge.  A few intrepid hot-rodders noticed that one particular sled, the Viper, took very well to a bit of extra weight in the form of armor and armament.  With a little engine tweaking, these modified Vipers, designated F-23, were selected by the Federation as the mainstay of their fighter wings.\\n\\nRequires: Fighter Bay {P30\\qLicense\\q \\qLicense, REQUIRES YOU TO REGISTER EV NOVA\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3031: {
        "resource_type": "desc",
        "id": "3031",
        "name": "Anaconda Bay",
        "text": "Anacondas can provide long-range intercept capability for a vessel.  This bay allows you to outfit a maximum of two of them.\\n\\nRequires: Fighter Bay {P30\\qLicense\\q \\qLicense, REQUIRES YOU TO REGISTER EV NOVA\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3032: {
        "resource_type": "desc",
        "id": "3032",
        "name": "Anaconda",
        "text": "The main problem with the Viper as a fighter craft is a complete lack of any form of explosive projectile.  A new variant that has the 'long distance kill' capacity, based on the Viper chassis, has been the Federation's choice of Space Superiority Fighter ever since.  Although this ship, named the Anaconda, suffers from a slightly slower acceleration and top speed than the Viper, its ability to destroy enemy fighters before that fighter can get within gun range more than compensates.\\n\\nRequires: Fighter Bay {P30\\qLicense\\q \\qLicense, REQUIRES YOU TO REGISTER EV NOVA\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3033: {
        "resource_type": "desc",
        "id": "3033",
        "name": "Firebird Bay",
        "text": "The Auroran shipwrights can install the electromag catapults for Firebird launching quite quickly.  The conversion also includes the appropriate Firebird housing facilities, allowing for a maximum of six of them{P30\\q.\\q \\q.\\n\\nREQUIRES YOU TO REGISTER EV NOVA\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3034: {
        "resource_type": "desc",
        "id": "3034",
        "name": "Firebird",
        "text": "Firebirds are the main Auroran fighter.  Their engines are simple, to say the least.  Their task is to protect the Phoenix from attack by smaller fighters such as the Viper, while the Phoenix take on the heavier ships.  The Firebird is slower than the Viper, but not by enough to give the Viper a decisive edge.  Battles between the two often come down to individual skill.  Many a Federation/Auroran border skirmish has come to a halt while the two sides watch a Firebird/Viper dogfight between renowned pilots{P30\\q.\\q \\q.\\n\\nREQUIRES YOU TO REGISTER EV NOVA\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3035: {
        "resource_type": "desc",
        "id": "3035",
        "name": "Phoenix Bay",
        "text": "Phoenix bays are noisy, smelly and generally fairly grimy.  If you can put up with this, you'll have some serious mobile firepower at your disposal, as the bay is capable of housing up to three of these vicious little fighters{P30\\q.\\q \\q.\\n\\nREQUIRES YOU TO REGISTER EV NOVA\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3036: {
        "resource_type": "desc",
        "id": "3036",
        "name": "Phoenix",
        "text": "The Phoenix is yet another example of the Auroran will to survive.  The Phoenix is slow and turns badly.  One would think that it would be target practice for enemy pilots.  It is, but it has one redeeming feature: it has almost as good armor plating as a Thunderhead.  They plough through fire corridors with impunity, and attack in groups to maximize firepower.  The Phoenix can wear a missile from an Anaconda, but a Viper will stay on its tail and pound it mercilessly.  Suffice to say that Phoenix pilots suffer the greatest rate of attrition of any group in the Auroran armed forces{P30\\q.\\q \\q.\\n\\nREQUIRES YOU TO REGISTER EV NOVA\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3037: {
        "resource_type": "desc",
        "id": "3037",
        "name": "Thunderhead Bay",
        "text": "The schematics of this Thunderhead bay look impressive, but you're a bit unsure as to how you'll fit it to your current vessel, although adding the capability to launch as many as three Thunderheads from your ship could never hurt.\\n\\nRequires: Fighter Bay {P30\\qLicense\\q \\qLicense, REQUIRES YOU TO REGISTER EV NOVA\\q}{b424 \\q\\nYou stare at this item, and the others around it, for several long, sad moments, knowing that you may never be able to buy any of them ever again.\\q \\q\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3038: {
        "resource_type": "desc",
        "id": "3038",
        "name": "Thunderhead",
        "text": "The Thunderhead is so named for its main weapon, the Thunderhead Lance.  The Lance is a solid beam of coherent laser light.  In some ways, the Thunderhead has the worst reputation of any fighting vessel in the Galaxy, not because of turn ratings or levels of firepower, but because this assault fighter is the weapon of choice of pirates, privateers and corsairs throughout known space.  It has enough armor to allow it to go up against large ships, and enough speed to allow it to catch most craft that try to flee.\\n\\nRequires: Fighter Bay {P30\\qLicense\\q \\qLicense, REQUIRES YOU TO REGISTER EV NOVA\\q}{b424 \\q\\nYou stare at this item, and the others around it, for several long, sad moments, knowing that you may never be able to buy any of them ever again.\\q \\q\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3039: {
        "resource_type": "desc",
        "id": "3039",
        "name": "Manta Bay",
        "text": "Mantas require food and water, as well as sunlight.  This bay provides for up to six of them with all of that, plus the required power taps for recharging all their BioRelay lasers{P30\\q.\\q \\q.\\n\\nREQUIRES YOU TO REGISTER EV NOVA\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3040: {
        "resource_type": "desc",
        "id": "3040",
        "name": "Manta",
        "text": "A pilot in the Nil'kemorya comes of age at 16.  It is then that he meets the Manta that will be his fighter and personal transport for as long as he lives, no matter how far he advances in rank.  Grown from a DNA sample taken from the pilot when he was initiated into the Nil'kemorya, the Manta will bond with him in a very personal way.  These fighters are not only swift and powerful, they are also the most 'alive' of the Polaris ships, having approximately the same level of sentience as smart dogs.  It incorporates a potent bio-organic laser into its nose as its only weapon{P30\\q.\\q \\q.\\n\\nREQUIRES YOU TO REGISTER EV NOVA\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3041: {
        "resource_type": "desc",
        "id": "3041",
        "name": "Hail Chaingun",
        "text": "\\qIf it ain't broke, don't fix it,\\q is the old maxim, and the Hail Chaingun holds true to this time-honored principle.  A simple caseless round is loaded into one of the two gatling breaches, and liquid propellant is injected behind the shell.  The Hail has a cyclic rate of 3000 RPM, and has enough ammo on board for an extended firefight{b424 \\q.\\n\\nYou stare at this item, and the others around it, for several long, sad moments, knowing that you may never be able to buy any of them ever again.\\q \\q.\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3042: {
        "resource_type": "desc",
        "id": "3042",
        "name": "Chaingun Ammunition",
        "text": "Simple caseless rounds have been around for longer than most historians can remember, and the production of them is so old-tech as to be almost a backyard occurrence throughout most of Known Space.  The Aurorans in particular produce enormous amounts of it in order to fuel their almost constant war efforts (whether it be against the Federation or amongst themselves){b424 \\q.\\n\\nYou stare at this item, and the others around it, for several long, sad moments, knowing that you may never be able to buy any of them ever again.\\q \\q.\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3043: {
        "resource_type": "desc",
        "id": "3043",
        "name": "Railgun (100mm)",
        "text": "Railguns are simple enough in concept; get a pellet made from a highly conductive, but dense metal (something cheap, like copper or gold), and place it between two rails (one a cathode, the other an anode).  Charge the rails with a homopolar generator, and there you have it: one super-high-speed metal pellet.  First developed by Sir Marcus Oliphant as a scientific instrument in the twentieth century AD, the railgun is now standard armament on all Auroran capital ships.  This version fires 100mm pellets.",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3044: {
        "resource_type": "desc",
        "id": "3044",
        "name": "Railgun (150mm)",
        "text": "A slightly larger version of the 100mm railgun, this weapon requires a much larger generator, and a power supply to match.  The 150mm pellets are made from a copper/cadmium mix, and are drop-forged with care by Auroran weaponsmiths{P30\\q.\\q \\q.\\n\\nREQUIRES YOU TO REGISTER EV NOVA\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3045: {
        "resource_type": "desc",
        "id": "3045",
        "name": "Railgun (200mm)",
        "text": "The mother of all railguns.  Firing a 200mm copper/cadmium pellet, this railgun looks like nothing less than a deck gun from an ancient Earth ocean-going warship.  The electrode rails get so scored during battle that they must be replaced at every landfall.  Luckily the rails are very cheap and easy to manufacture.  Some have even been constructed of old armor plates in times of emergency{P30\\q.\\q \\q.\\n\\nREQUIRES YOU TO REGISTER EV NOVA\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3046: {
        "resource_type": "desc",
        "id": "3046",
        "name": "Turreted Railgun (100mm)",
        "text": "While railguns are normally fixed-position weapons, something turreted was required for the immense Auroran Carrier.  Thus the evergreen 100mm railgun was mounted on a Storm Chaingun swivel mount.  The combo has proved quite successful, with several other fighting ships being retrofitted with similar guns{P30\\q.\\q \\q.\\n\\nREQUIRES YOU TO REGISTER EV NOVA\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3047: {
        "resource_type": "desc",
        "id": "3047",
        "name": "EMP Torpedo Tube",
        "text": "EMP weapons have not changed much since the first days of nuclear power.  This tube fires torpedos carrying an EMP weapon with a yield of a gigaton or more of TNT.  EMP weapons, as with all nuclear-type weapons, are generally the province of pirates and military dictators, as their use has been severely limited by all civilized people{P30\\q.\\q \\q.\\n\\nREQUIRES YOU TO REGISTER EV NOVA\\q}{b424 \\q\\n\\nYou stare at this item, and the others around it, for several long, sad moments, knowing that you may never be able to buy any of them ever again.\\q \\q\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3048: {
        "resource_type": "desc",
        "id": "3048",
        "name": "EMP Torpedo",
        "text": "The EMP Torpedo was constructed from stolen Federation technology.  It is an awesome weapon, with only two real uses: mass destruction and ionization.  The Pirate Carrier carries four EMP torps as a blockade running tool; simply fire the weapon at the opposing line, and wait for them to scatter like sheep.  Not to be detonated at close range{P30\\q.\\q \\q.\\n\\nREQUIRES YOU TO REGISTER EV NOVA\\q}{b424 \\q\\n\\nYou stare at this item, and the others around it, for several long, sad moments, knowing that you may never be able to buy any of them ever again.\\q \\q\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3049: {
        "resource_type": "desc",
        "id": "3049",
        "name": "Fusion Reactor",
        "text": "While the basic design of the Fusion Reactor has remained unchanged for nearly three centuries, it still enjoys widespread use in the ships run by all castes (except those of the Nil'kemorya) as it more than fills their energy requirements.  When asked if Polaris freighters and pleasure craft will ever require greater power sources, members of the Ver'ash shrug their shoulders and answer that if that day ever comes, there are already more advanced energy reactors being used in warrior vessels which could be relatively easily converted for non-military applications{P30\\q.\\q \\q.\\n\\nREQUIRES YOU TO REGISTER EV NOVA\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3050: {
        "resource_type": "desc",
        "id": "3050",
        "name": "Thorium Reactor",
        "text": "Until recently, the mighty Federation Carrier had one significant weakness: its reactor was not powerful enough for these enormous ships to operate for very long in sustained battle operations.  With the advent of the Thorium Reactor, Federation Carriers can now spend much longer out on patrol without having to come in for a refit{P30\\q.\\q \\q.\\n\\nREQUIRES YOU TO REGISTER EV NOVA\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3051: {
        "resource_type": "desc",
        "id": "3051",
        "name": "Fission Reactor",
        "text": "This reactor is the mainstay of the Federation fleet, and can easily handle the energy requirements of most vessels, although it struggles a little with the energy needs of the enormous Federation Carrier.  However, for all but the largest of capital ships, the fission reactor is more than sufficient for any energy output{P30\\q.\\q \\q.\\n\\nREQUIRES YOU TO REGISTER EV NOVA\\q}{b424 \\q\\n\\nYou stare at this item, and the others around it, for several long, sad moments, knowing that you may never be able to buy any of them ever again.\\q \\q\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3052: {
        "resource_type": "desc",
        "id": "3052",
        "name": "Carbon Fiber",
        "text": "The invention of the carbon fiber technology has been lost in the turbulent eleven century history of mankind's adventures into space.  Easy to produce and very inexpensive, carbon fiber shielding has been added to ships for nearly as long as humanity has been in space, or so historians say.  At the end of the day, adding carbon fiber composites to your ship gives you a decent increase to your armor without draining your coffers or using up enormous amounts of your free space.\\n\\nRequires: Protective Technologies License{b424 \\q\\nYou stare at this item, and the others around it, for several long, sad moments, knowing that you may never be able to buy any of them ever again.\\q \\q\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3053: {
        "resource_type": "desc",
        "id": "3053",
        "name": "Matrix Steel",
        "text": "Throughout the Empire, armor has been piled onto warships in an effort to make up for shortcomings in Auroran particle shielding.  The slabs of matrix steel Auroran pilots and warriors add to their ships is indicative of this mindset; heavy but very strong, these enormous chunks of metal afford excellent protection against whatever unfriendly fire may come your way.",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3054: {
        "resource_type": "desc",
        "id": "3054",
        "name": "Titanium Lattice",
        "text": "Until very recently, Federation scientists, while having a vastly superior knowledge of particle shielding, were lagging their Auroran counterparts in armor technology.  With the recent invention of a commercially viable process to create a lattice of titanium and a few other minor ingredients, it is hoped that before long the vessels of the Federation Navy will begin to not only exhibit superior shielding when compared to their Auroran foes, but also superior armor.\\n\\nRequires: Protective Technologies {P30\\qLicense\\q \\qLicense, REQUIRES YOU TO REGISTER EV NOVA\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3055: {
        "resource_type": "desc",
        "id": "3055",
        "name": "Spun Diamond",
        "text": "Nearly a century ago, P'aedt scientists working with Ver'ash engineers stumbled across a biological process that could be adapted to allow their ships to literally extrude carbon atoms around themselves, forming a diamond shell.  Since then, Polaris shielding technology has been greatly enhanced, but many of the Nil'kemorya in particular still ask their Ver'ash cousins to modify their ships to also gain this armor advantage{P30\\q.\\q \\q.\\n\\nREQUIRES YOU TO REGISTER EV NOVA\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3056: {
        "resource_type": "desc",
        "id": "3056",
        "name": "Gravimetric Sensors",
        "text": "This software package will increase your onboard computer's ability to differentiate between the size of the sensor returns off any ships in your local area.  After installation, you should be able to detect the approximate mass of any ship within range of your ship's scanners, allowing you to differentiate between large and small ships on your radar display.",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3057: {
        "resource_type": "desc",
        "id": "3057",
        "name": "IFF Decoder",
        "text": "This simple modification to a ship's standard sensor system software will allow it to differentiate between the weapons states of ships within your scanning range.  Ships which have their weapons powered up and their sensors locked on you will show up as hostile (red), ships that come from recognized friendly governments will show up as friendly (green), unless they are acting in a hostile manner towards you, and all other ships will show up as neutral (blue).",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3058: {
        "resource_type": "desc",
        "id": "3058",
        "name": "Auto-recharger",
        "text": "This handy piece of software automatically contacts spaceport computers via your comm system whenever you land and arranges for them to recharge your ship, saving you the worry. Of course, the cost remains the same regardless of whether you have the Auto-recharger or not.",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3059: {
        "resource_type": "desc",
        "id": "3059",
        "name": "Auto-eject",
        "text": "Without this piece of equipment, the chances of you surviving an encounter with overwhelming forces is greatly decreased.  Essentially, the auto-eject is very simple: when it detects your armor state fall to zero it launches your eject mechanism without waiting for any input from the pilot.  With a nearly 100% success rate, this piece of hardware is something of a must for anybody foolhardy enough to brave the spaceways in this day and age.",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3060: {
        "resource_type": "desc",
        "id": "3060",
        "name": "Escape Pod",
        "text": "By the time you factor in the costs of training, qualified pilots are, almost without fail, far more valuable than the ships they fly.  So most governments and major organizations fit this device to their vessels to protect their investment.  Though fairly expensive, a fair number of independent pilots who, quite understandably, highly value their own lives, also use escape pods.  Unfortunately, no insurance company worth its salt would ever offer ship destruction insurance.  Let's face it, with the current unstable climate, travelling the space-lanes is hardly the safest way to make a living...",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3061: {
        "resource_type": "desc",
        "id": "3061",
        "name": "Cargo Expansion",
        "text": "This simple upgrade takes up 15 tons of your free mass and gives you 10 tons more cargo space.  Common throughout nearly all the known galaxy, the Cargo Expansion upgrade is used by freighter captains everywhere to increase their hold size.  As an unfortunate side-effect of the process it also decreases the space available for weapons, so think twice before purchasing if you are going to be operating in dangerous areas.",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3062: {
        "resource_type": "desc",
        "id": "3062",
        "name": "Mass Expansion",
        "text": "A large number of starship captains, from the earliest pioneers over a millennia ago to those travelling the enormous voids between the stars today, will attest to the value of this simple upgrade.  If you are prepared to give up 15 tons of cargo space, it will give you 10 more tons of free mass, allowing you that much more room for weapons for personal protection.  In a dangerous galaxy, it would pay to seriously consider this module.",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3063: {
        "resource_type": "desc",
        "id": "3063",
        "name": "Cargo Retool",
        "text": "The cargo retool is similar to the cargo expansion in that it exchanges free mass for cargo space, but instead of adding a module to do it the refitters retool a portion of your weapon space and turn it into cargo space.  It gives a better return on your space (12 tons of free mass turns into 10 tons of cargo space), but, unlike the cargo expansion, it is not a reversible procedure.  That space will remain cargo space forever.",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3064: {
        "resource_type": "desc",
        "id": "3064",
        "name": "Mass Retool",
        "text": "The mass retool does the exact opposite of the cargo retool; it exchanges cargo space for free mass.  Like the cargo retool, it gives a better return on your space than the mass expansion equivalent (12 tons of cargo space turns into 10 tons of free mass), but it too is a non-reversible procedure.",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3065: {
        "resource_type": "desc",
        "id": "3065",
        "name": "Shield Recharger",
        "text": "Federation particle shielding technology has always been vastly ahead of anything the Auroran Empire has ever had, and the shield recharger is a prime example of this.  All ships with particle shielding can gradually recharge any lost shield power, but the shield recharger has a separate power source specifically attuned to your shield frequencies, allowing raw power to be pumped into your shields and causing them to recharge faster.\\n\\nRequires: Protective Technologies {P30\\qLicense\\q \\qLicense, REQUIRES YOU TO REGISTER EV NOVA\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3066: {
        "resource_type": "desc",
        "id": "3066",
        "name": "Organic Shield",
        "text": "\\qWe strive always to ensure that we achieve the balance of a true warrior,\\q explains a gray-cloaked Nil'kemorya warrior.  \\qAnd our ships, when we fly into battle with them, must become extensions of ourselves, and must therefore be balanced also.  If we wield great weapons of destruction, they must also have excellent protection, as they will become a target by the enemy.  The organic shield increases the restorative power of our shields, allowing us to maintain our balance.{P30\\q\\\\\\q\\q \\q\\\\\\q\\n\\nREQUIRES YOU TO REGISTER EV NOVA\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3067: {
        "resource_type": "desc",
        "id": "3067",
        "name": "Shield Buffer",
        "text": "At the end of the day, the greater your shields, the longer you will survive.  Most Federation starship captains, if they can get their hands on the necessary funding, will leap at the chance to get ahold of one of these Sigma Shipyards S-72 Shield Buffers.  In simple terms, the S-72 detects the outer layer of your particle shielding and adds another layer on top of that.\\n\\nRequires: Protective Technologies {P30\\qLicense\\q \\qLicense, REQUIRES YOU TO REGISTER EV NOVA\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3068: {
        "resource_type": "desc",
        "id": "3068",
        "name": "Shield Organelles",
        "text": "As with all Polaris ships, everything is now bioengineered, including the organs that produce the particle shielding.  However, like everything else they do, the Ver'ash have the capability of growing new organs to either 'heal' existing damage on ships or to 'add' a new organ to a ship, enhancing its capabilities.  If more shielding is wanted, then they can cause your ship to grow more shield organelles to accommodate you{P30\\q.\\q \\q.\\n\\nREQUIRES YOU TO REGISTER EV NOVA\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3069: {
        "resource_type": "desc",
        "id": "3069",
        "name": "Afterburner",
        "text": "The ability to dump raw power into your propulsion system to temporarily increase your acceleration and top speed has been around since we were trapped within Earth's biosphere, and has followed us out into space.  The afterburner chews power at a prodigious rate, but losing a little power is better than getting caught in the middle of a fleet battle{P30\\q.\\q \\q.\\n\\nREQUIRES YOU TO REGISTER EV NOVA\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3070: {
        "resource_type": "desc",
        "id": "3070",
        "name": "Port & Polish",
        "text": "A Port & Polish is just that, a cleanup of your ship and its drive systems, allowing for more efficient engine usage.  Anybody seeking to get that little bit of extra acceleration out of their ship could use one of these little tune-ups{P30\\q.\\q \\q.\\n\\nREQUIRES YOU TO REGISTER EV NOVA\\q}{b424 \\q\\n\\nYou stare at this item, and the others around it, for several long, sad moments, knowing that you may never be able to buy any of them ever again.\\q \\q\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3071: {
        "resource_type": "desc",
        "id": "3071",
        "name": "Overdrive",
        "text": "This is the engine modification inspired by the inbred mechanical genius 'Skinny'.  Without getting too technical, it dramatically increases the speed and acceleration of your ship, and as everyone knows, the faster your ship, the harder you are to catch.  Anybody who lives close to the legal edge needs more speed.  Merchants need it to try and keep away from the pirates, the pirates need it to keep ahead of the merchants and to keep away from the authorities, and the authorities could use it to catch the pirates.  If you need to get out to hyperspace range in a hurry, then this is the upgrade for you{P30\\q.\\q \\q.\\n\\nREQUIRES YOU TO REGISTER EV NOVA\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3072: {
        "resource_type": "desc",
        "id": "3072",
        "name": "Vectored Thrust",
        "text": "This is another Owen Greylock special.  He came up with the idea when he saw ancient drawings of aerial fighter-craft that had small panels on either side of their exhaust pipes to direct the thrust in one direction or another and enhance maneuverability.  It took him ten years to perfect, but now the Greylock system is used by nearly all pirates throughout the Known Galaxy, and more than a few merchants and free-lance starship captains have also chosen to add this upgrade to their ships{P30\\q.\\q \\q.\\n\\nREQUIRES YOU TO REGISTER EV NOVA\\q}{b424 \\q\\n\\nYou stare at this item, and the others around it, for several long, sad moments, knowing that you may never be able to buy any of them ever again.\\q \\q\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3073: {
        "resource_type": "desc",
        "id": "3073",
        "name": "Alluvial Damper",
        "text": "When he joined the Rebellion, Mr. Donald Chick and his engineers took with them many of Sigma Shipyards experimental designs, and one of them that has come into fruition was the alluvial damper.  Strictly speaking, it is more of a psychological damper: it lessens the EM field strengths created by a hyperspace field, but only within the living compartments of a starship.  The end result is that humans can therefore endure the more powerful hyperspace fields without mental breakdown, and so starships can travel faster between systems{P30\\q.\\q \\q.\\n\\nREQUIRES YOU TO REGISTER EV NOVA\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3074: {
        "resource_type": "desc",
        "id": "3074",
        "name": "Horizontal Booster",
        "text": "Donald Chick's expertise does not just stop at starship design and engineering; it also extends to hyperspatial navigational computational modules.  When you link this module into your navi-computer, it will be able to calculate hyperspatial trajectories much earlier than normal, as it includes an incredibly advanced gravitational compensation algorithm which allows you to enter hyperspace from much closer to the system center.  Many Rebel starship captains will attest to its effectiveness{P30\\q.\\q \\q.\\n\\nREQUIRES YOU TO REGISTER EV NOVA\\q}{b424 \\q\\n\\nYou stare at this item, and the others around it, for several long, sad moments, knowing that you may never be able to buy any of them ever again.\\q \\q\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3075: {
        "resource_type": "desc",
        "id": "3075",
        "name": "Sensor Boost",
        "text": "Throughout the galaxy there are navigational hazards that affect your sensors, and the only problem with increasing power to your sensors is that any more power would start creating EM fields which would render your sensors useless.  Federation scientists on Menin recently found a new, commercially viable, way of increasing the shielding on the solid state electronics which then allows for more powerful sensors that do not interfere with their own operation.",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3076: {
        "resource_type": "desc",
        "id": "3076",
        "name": "Map",
        "text": "This map will automatically update your ship's computer with information about the location and contents of the systems surrounding this one.",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3077: {
        "resource_type": "desc",
        "id": "3077",
        "name": "T5 Strength",
        "text": "While your skills are still rudimentary, and you are far from powerful, you still have some capability to defend yourself",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3078: {
        "resource_type": "desc",
        "id": "3078",
        "name": "T4 Strength",
        "text": "Your telepathic capabilities afford you some increased protection against possible hazards.",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3079: {
        "resource_type": "desc",
        "id": "3079",
        "name": "T3 Strength",
        "text": "With your power growing and your skills increasing, you telepathic capabilities afford you a fair amount of protection against the many and various hazards of the modern universe.",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3080: {
        "resource_type": "desc",
        "id": "3080",
        "name": "Cargo Retool",
        "text": "The cargo retool is similar to the cargo expansion in that it exchanges free mass for cargo space, but instead of adding a module to do it the refitters retool a portion of your weapon space and turn it into cargo space.  It gives a better return on your space (12 tons of free mass turns into 10 tons of cargo space), but, unlike the cargo expansion, it is not a reversible procedure.  That space will remain cargo space forever.",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3081: {
        "resource_type": "desc",
        "id": "3081",
        "name": "T2 Strength",
        "text": "Your skill and power would be the envy of most Vell-os galaxy wide.  It affords you excellent protection against the hazards of the universe.",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3082: {
        "resource_type": "desc",
        "id": "3082",
        "name": "Mass Retool",
        "text": "The mass retool does the exact opposite of the cargo retool; it exchanges cargo space for free mass.  Like the cargo retool, it gives a better return on your space than the mass expansion equivalent (12 tons of cargo space turns into 10 tons of free mass), but it too is a non-reversible procedure.",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3083: {
        "resource_type": "desc",
        "id": "3083",
        "name": "Fed Cloaking Device",
        "text": "As a result of a lab accident when trying to study a captured Polaris biological ship, Federation scientists were able to create a sub-space bubble.  Later, with further research, they were able to figure out how to wrap one around a ship.  The result is that most modern sensors are completely incapable of detecting the ship as it is now 'cloaked' in the background fabric of the universe.",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3084: {
        "resource_type": "desc",
        "id": "3084",
        "name": "Sensor Boost",
        "text": "Throughout the galaxy there are navigational hazards that affect your sensors, and over the last four centuries the Ver'ash and the P'aedt have been working on ways and means to overcome these problems.  The latest version can cut through even the most horrendous interference, making even the most treacherous parts of the galaxy navigable{b424 \\q.\\n\\nYou stare at this item, and the others around it, for several long, sad moments, knowing that you may never be able to buy any of them ever again.\\q \\q.\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3085: {
        "resource_type": "desc",
        "id": "3085",
        "name": "Sensor Boost",
        "text": "Throughout the galaxy there are navigational hazards that affect your sensors, and even though the Empire's scientists are not as capable as those of the Federation, they are more than capable of reverse engineering anything they find on a captured Federation vessel.  The Auroran sensor boosts are not quite as effective as those of the Federation, but only because the manufacturing processes are not of the same meticulous standard.  You will find, however, that the Auroran sensor boost is a very cheap buy{b424 \\q.\\n\\nYou stare at this item, and the others around it, for several long, sad moments, knowing that you may never be able to buy any of them ever again.\\q \\q.\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3086: {
        "resource_type": "desc",
        "id": "3086",
        "name": "Sensor Boost",
        "text": "When Owen Greylock tinkers with a design, you can be assured that he will improve it somehow, and this sensor boost is no exception.  While the cost is enormous, the only place that you can get a better sensor array is from the Polaris, and they tend to keep their technology to themselves.  If you want the next best thing, then this is it{b424 \\q.\\n\\nYou stare at this item, and the others around it, for several long, sad moments, knowing that you may never be able to buy any of them ever again.\\q \\q.\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3087: {
        "resource_type": "desc",
        "id": "3087",
        "name": "Storm Chaingun",
        "text": "The Storm is a sacred weather pattern in Auroran culture.  Symbolizing the power and fury of the hordes of Auroran warriors, many warriors have a thundercloud as a death tattoo, indicating that they will die in the fury of a mass offensive.  The Storm Chaingun reflects the Auroran philosophy of overwhelming the enemy with numbers; the Storm is effectively four Hails on a turret, and, as a point defence weapon system, is used to destroy incoming fighters and missiles with often devastating effect, and without requiring any command input from the bridge{P30\\q.\\q \\q.\\n\\nREQUIRES YOU TO REGISTER EV NOVA\\q}{b424 \\q\\n\\nYou stare at this item, and the others around it, for several long, sad moments, knowing that you may never be able to buy any of them ever again.\\q \\q\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3088: {
        "resource_type": "desc",
        "id": "3088",
        "name": "Fusion Pulse Turret",
        "text": "When the Heraan family were constructing the first Abomination gunboats, they discovered quite quickly that standard Fusion Pulse Cannons mounted on Abominations were unable to hit fast moving targets, due to the poor turning speed of the craft.  So was born the Fusion Pulse Turret (and later the battery version).",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3089: {
        "resource_type": "desc",
        "id": "3089",
        "name": "Thunderhead Lance",
        "text": "Thunderheads are built around this stocky beam unit.  The Lance is a simple laser; nothing more, nothing less.  It is a very highly charged weapon, but it is effective only at short range.  As the best way to use a Lance is to almost ram the ship in question, it is a favored weapon of the Wild Geese, who consider it a divine gift.\\n\\nRequires: Heavy Weapons {P30\\qLicense\\q \\qLicense, REQUIRES YOU TO REGISTER EV NOVA\\q}{b424 \\q\\n\\nYou stare at this item, and the others around it, for several long, sad moments, knowing that you may never be able to buy any of them ever again.\\q \\q\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3090: {
        "resource_type": "desc",
        "id": "3090",
        "name": "Pirate Viper Bay",
        "text": "Pirates know about violence, and the threat of violence.  They also know about hounding individual ships in packs.  However, they also value speed, and the Pirate Viper Bay launches them far faster than any other type of bay outside of Polaris Space, allowing them to swarm over their foes with frightening rapidity.  So despite only being able to house a maximum of four Pirate Vipers, many pirates vessels have at least one.  With one of these bays on board, you'll have a fast pack at your disposal at all times{P30\\q.\\q \\q.\\n\\nREQUIRES YOU TO REGISTER EV NOVA\\q}{b424 \\q\\n\\nYou stare at this item, and the others around it, for several long, sad moments, knowing that you may never be able to buy any of them ever again.\\q \\q\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3091: {
        "resource_type": "desc",
        "id": "3091",
        "name": "Pirate Viper",
        "text": "As soon as Comara released the Viper frame on the general market, a few shiploads of frames were bought up by notorious pirate shipwright Olaf Greyshoulders.  He and his crew have totally refitted the shell, and the familiar shape of its advanced armor plating hides a wealth of minor and major improvements to the basic idea.  But, as with all Greyshoulders upgrades, there is a hefty price to pay for the improved model.  It's up to you to decide whether it's worth it{P30\\q.\\q \\q.\\n\\nREQUIRES YOU TO REGISTER EV NOVA\\q}{b424 \\q\\n\\nYou stare at this item, and the others around it, for several long, sad moments, knowing that you may never be able to buy any of them ever again.\\q \\q\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3092: {
        "resource_type": "desc",
        "id": "3092",
        "name": "Turreted BioRelay Laser",
        "text": "The TBRL is a special variant of the Polaris BioRelay Laser.  It is mounted on the Polaris Dragon as a primary weapon.  This weapon is used rather than the more powerful pulse laser, so as to limit the potential damage were a Dragon to fall into unfriendly hands; a good scientist can unravel much from a working sample of an enemy weapon{P30\\q.\\q \\q.\\n\\nREQUIRES YOU TO REGISTER EV NOVA\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3093: {
        "resource_type": "desc",
        "id": "3093",
        "name": "Flower Of Spring",
        "text": "The Vell-os name their weapons after the telepathic weaves used to turn their telepathic abilities into physical energy.  Thus this weapon is called the Flower Of Spring because the weave works from the ground up and includes patterns much like that of a flower.",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3094: {
        "resource_type": "desc",
        "id": "3094",
        "name": "Summer Bloom",
        "text": "The Summer Bloom is the magenta beam that is incorporated into the form of the Arrow.  A T2 Vell-os can maintain power to this weapon almost indefinitely, and the stopping power of a Bloom is stunning for such a small beam.",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3095: {
        "resource_type": "desc",
        "id": "3095",
        "name": "Autumn Petal",
        "text": "This instrument of destruction is an integral part of the makeup of a Vell-os Javelin.  The color of early autumn kirastei petals on Vell-os worlds, the Autumn Petal has an excellent sustained fire rate, and long range.  Only T1's have been known to be able to create the weave required for this weapon.",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3096: {
        "resource_type": "desc",
        "id": "3096",
        "name": "Winter Tempest",
        "text": "Winter Tempest is a name spoken in dark corners by the Vell-os people.  The storm-colored arc of light has only once been used in anger.  Even then it took a T1 working at focusing the power of twenty T2's to get it to work.  It has been theorized by Vell-os scientists that a T0 would have the potential to create this beam by himself.",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3097: {
        "resource_type": "desc",
        "id": "3097",
        "name": "Create Dart",
        "text": "As your telepathic power swells, you learn a great deal more about how to project your consciousness out upon the universe.  Now, if you choose to prepare yourself correctly by selecting this ability, you can project small parts of your mind into Dart-like receptacles which will act as you command them.",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3098: {
        "resource_type": "desc",
        "id": "3098",
        "name": "Dart",
        "text": "As part of gaining the ability to project small parts of your consciousness out onto the universe, you must prepare yourself for it by deliberately setting apart portions of your telepathic energy by selecting this option.",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3099: {
        "resource_type": "desc",
        "id": "3099",
        "name": "Marine Platoon",
        "text": "The leader of these hard-looking men tells you that he is capable of increasing your chances of capturing any vessel enormously.\\n\\n\\qAnd we don't need continuous cash flow,\\q he explains in his deep voice as his men watch on with casual alertness.  \\qWe have all the equipment we need, and we take small amounts of profit by foraging on every ship we board.{P30\\q\\\\\\q\\q \\q\\\\\\q\\n\\nREQUIRES YOU TO REGISTER EV NOVA\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3100: {
        "resource_type": "desc",
        "id": "3100",
        "name": "Solar Panel",
        "text": "Most experienced traders will recommend that you buy at least one of these Sigma N41 Solar Panels.  They work by converting the energy of nearby stars, via super-efficient photo-voltaic cells, into electrical energy to continually build up charge in the superconductor loops which store the energy for later use.  The energy thus stored can the be called upon to slowly build up the reserves in your energy cells.  Comes in handy when you find yourself out of energy in an uninhabited system with no help in sight.",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3101: {
        "resource_type": "desc",
        "id": "3101",
        "name": "Nanites",
        "text": "Krypt has no weapons; why should she have?  As far as she is concerned, she is the only life-form in the universe.  Krypt is, however, very curious.  She will send out colonies of nanites from her roving spheres to explore strange asteroids and other phenomena.  These colonies will latch on to material in space, and start exploring the composition.  This has a devastating effect on ships.",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3102: {
        "resource_type": "desc",
        "id": "3102",
        "name": "Solar Lance",
        "text": "The Solar Lance is the defensive mechanism of the Hyperioids.  A Hyperioid can generate a significant charge by rotating its pods around its body at a high rate of speed.  The Solar Lance uses this charge to propel photons out of the Hyperioid's feeding orifice.  The resulting beam weapon is very dangerous; contact should be avoided at all costs.",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3103: {
        "resource_type": "desc",
        "id": "3103",
        "name": "WGB (A)",
        "text": "The Wraith have evolved a focused graviton beam as a territorial display, and as a weapon in mating rituals.  As the Wraith evolved into an intelligent species, their beams became defensive weapons as well.  The highly focused gravitons cause severe damage to unshielded vessels.  Armor plates of lesser ships have been known to simply shear off under the force.",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3104: {
        "resource_type": "desc",
        "id": "3104",
        "name": "WGB (Y)",
        "text": "Despite not being as powerful as that of an adult Wraith, the graviton beam produced by young Wraith is still a formidable weapon.  It gives pause to smaller ships, and can inflict serious damage on larger ships if unchecked.",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3105: {
        "resource_type": "desc",
        "id": "3105",
        "name": "WGB (C)",
        "text": "The children of the Wraith use their underdeveloped beams to divert the courses of small meteors in games of skill and dexterity.  They're not much good for anything else.",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3106: {
        "resource_type": "desc",
        "id": "3106",
        "name": "Rebel Cloaking Device - legal",
        "text": "With the help of Polaris scientists and engineers, the Rebels were able to build cloaking devices that fold the fabric of space around a ship, leaving it undetectable by any current sensor array.  More than a few undercover Rebel ships have been fitted with this upgrade as an insurance policy against Bureau discovery.",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3107: {
        "resource_type": "desc",
        "id": "3107",
        "name": "Matter/Anti-Matter Reactor",
        "text": "Humanity has been trying to figure out ways of controlling a matter/anti-matter reaction so as to gain access to an enormous, virtually undepletable energy source for nearly two millennia.  When P'Ardandt discovered that particular high energy frequency EM fields could be used to 'resonate' with varying sized particles of matter and anti-matter, the matter/anti-matter reactor became a reality, ensuring near-limitless power to any machine connected to it{P30\\q.\\q \\q.\\n\\nREQUIRES YOU TO REGISTER EV NOVA\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3108: {
        "resource_type": "desc",
        "id": "3108",
        "name": "Fuel Transfer",
        "text": "No desc req'd",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3109: {
        "resource_type": "desc",
        "id": "3109",
        "name": "Map",
        "text": "No desc req'd",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3110: {
        "resource_type": "desc",
        "id": "3110",
        "name": "Civilian IR Jammer",
        "text": "Just traveling the space lanes can be dangerous, what with the pirates as well as the Aurorans and the Federation fighting.  So it never hurts to have a little insurance against some of their long range attacks to give you some time to get away.  This simple system merely fires a low-power laser into the IR sensor of the incoming missile, hopefully burning it out.  The technology is still a little bit hit-and-miss, but it sure beats nothing.\\n\\nRequires: Protective Technologies License{b424 \\q\\nYou stare at this item, and the others around it, for several long, sad moments, knowing that you may never be able to buy any of them ever again.\\q \\q\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3111: {
        "resource_type": "desc",
        "id": "3111",
        "name": "Civilian Radar Jammer",
        "text": "Like the IR Jammer, this system is a cheap, low power rip-off of the military models.  It works by flooding the space directly surrounding your ship with incoherent signals.  Unfortunately, due to the low power of this model (which has more to do with legal restrictions than any engineering faults), many missiles still manage to get through.\\n\\nRequires: Protective Technologies License{b424 \\q\\nYou stare at this item, and the others around it, for several long, sad moments, knowing that you may never be able to buy any of them ever again.\\q \\q\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3112: {
        "resource_type": "desc",
        "id": "3112",
        "name": "Military IR Jammer",
        "text": "This system is the top of the line in IR missile protection.  It sends out a short laser burst at the incoming missile, disabling its sensor 'eye' and causing it to wander off target.  Recent developments in this technology have improved its reliability, and very few missiles make it through its 'screen'.\\n\\nRequires: Protective Technologies {P30\\qLicense\\q \\qLicense, REQUIRES YOU TO REGISTER EV NOVA\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3113: {
        "resource_type": "desc",
        "id": "3113",
        "name": "Military Radar Jammer",
        "text": "This is a much higher power version of the Civilian Radar Jammer.  It creates a lot more sensor interference and so is correspondingly much better at confusing the incoming missiles.  This system has recently been tested against the Aurorans radar missiles and has shown itself to be enormously effective, but it has not yet been issued to all Federation capital ships.\\n\\nRequires: Protective Technologies {P30\\qLicense\\q \\qLicense, REQUIRES YOU TO REGISTER EV NOVA\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3114: {
        "resource_type": "desc",
        "id": "3114",
        "name": "Auroran IR Jammer",
        "text": "During their interminable wars, the first missile to be used successfully by the Aurorans was the IR missile. For a while they were produced in huge quantities, but now, due to the effectiveness of this system, they are all but extinct within the Auroran Empire.  Even the Federation has copied its design of firing a laser at the sensor 'eye' of the incoming missile for their systems as it is so effective{P30\\q.\\q \\q.\\n\\nREQUIRES YOU TO REGISTER EV NOVA\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3115: {
        "resource_type": "desc",
        "id": "3115",
        "name": "Auroran Radar Jammer",
        "text": "Only recently have the Aurorans managed to develop the technology to have any effect against radar guided missiles.  They were able to salvage an old Federation radar counter-measures package and deconstruct it.  The capabilities of the resulting system are still years behind those of the Federation, but it is better than nothing{P30\\q.\\q \\q.\\n\\nREQUIRES YOU TO REGISTER EV NOVA\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3116: {
        "resource_type": "desc",
        "id": "3116",
        "name": "Polaris Jammer",
        "text": "Although very few non-military Polaris ships venture out of Polaris space, for the sake of safety, a counter-measures system to foil the most common types of missile tracking (infra-red and radar) is available to all Polaris ships{P30\\q.\\q \\q.\\n\\nREQUIRES YOU TO REGISTER EV NOVA\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3117: {
        "resource_type": "desc",
        "id": "3117",
        "name": "Nil'kemorya Jammer",
        "text": "Unlike their civilian counterparts, the ships of the Nil'kemorya are forced to deal with hostile forces quite often.  To help them deal with the problem, P'aedt scientists and Ver'ash engineers have come up with this system that detects the electron movements common to most guidance systems and then shorts them out by creating an electromagnetic field in the surrounding space that is directly inverse to the fields of the incoming missiles{P30\\q.\\q \\q.\\n\\nREQUIRES YOU TO REGISTER EV NOVA\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3118: {
        "resource_type": "desc",
        "id": "3118",
        "name": "Rebel IR Jammer",
        "text": "Stolen from the Federation military by General Cade 'Sundown' Smart, this system has been tinkered with by Donald Chick and his staff of engineers, and while they have made a few minor improvements, the end result is barely different from the original Federation designs in effectiveness{P30\\q.\\q \\q.\\n\\nREQUIRES YOU TO REGISTER EV NOVA\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3119: {
        "resource_type": "desc",
        "id": "3119",
        "name": "Rebel Radar Jammer",
        "text": "Unlike their Federation counterparts, the Rebels have rushed this piece of equipment into production to make it standard throughout their fleet.  Already all the capital ships carry them, and it will not be long before the heavy interceptors get them also.  Of course, the Rebel fleet is much smaller than that of the Federation, so it is a lot easier to get all the new technology out to its ships{P30\\q.\\q \\q.\\n\\nREQUIRES YOU TO REGISTER EV NOVA\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3120: {
        "resource_type": "desc",
        "id": "3120",
        "name": "Pirate Jammer",
        "text": "This is another Olaf Greyshoulders special.  He took the recent Federation improvements in radar countermeasures and combined them with their already excellent infra-red systems.  The end result is a little bulkier, but performs both jobs admirably.  'Free traders' from all over are buying it, and Olaf is making a quiet killing{P30\\q.\\q \\q.\\n\\nREQUIRES YOU TO REGISTER EV NOVA\\q}{b424 \\q\\n\\nYou stare at this item, and the others around it, for several long, sad moments, knowing that you may never be able to buy any of them ever again.\\q \\q\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3121: {
        "resource_type": "desc",
        "id": "3121",
        "name": "Distract Sensors",
        "text": "As your abilities grow, you are soon able to discern the workings of guided missiles from background space.  It is a simple matter of twisting the surrounding space to confuse them.",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3122: {
        "resource_type": "desc",
        "id": "3122",
        "name": "Rebel Radar Jammer",
        "text": "Unlike their Federation counterparts, the Rebels have rushed this piece of equipment into production to make it standard throughout their fleet.  Already all the capital ships carry them, and it will not be long before the heavy interceptors get them also.  Of course, the Rebel fleet is much smaller than that of the Federation, so it is a lot easier to get all the new technology out to its ships{P30\\q.\\q \\q.\\n\\nREQUIRES YOU TO REGISTER EV NOVA\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3123: {
        "resource_type": "desc",
        "id": "3123",
        "name": "Vell-os Area Map",
        "text": "With your telepathic senses, you can reach out and observe the physical nature of the universe around.  The further out you get, the harder it is to make out distinctive features, but it does allow you a greater understanding of the local area of the universe than any human map.",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3124: {
        "resource_type": "desc",
        "id": "3124",
        "name": "Physical Sense",
        "text": "No desc req'd",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3125: {
        "resource_type": "desc",
        "id": "3125",
        "name": "Hostility Sense",
        "text": "No desc req'd",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3126: {
        "resource_type": "desc",
        "id": "3126",
        "name": "Wraith Cannon",
        "text": "Wraithii are tiny capsules of polarons contained in a mar-graviton field.  A Wraith Cannon fires these capsules via simple biomechanics, and the capsules burst on impact, releasing a powerful kinetic force.  These guns are mounted as standard on the Dragon, a Polaris vessel, but can be retrofitted to most ships on the market.  Ever since this technology was stolen from the Polaris in a daring raid, Federation scientists, while capable of duplicating the technology, have been having problems understanding it...",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3127: {
        "resource_type": "desc",
        "id": "3127",
        "name": "Wraithii",
        "text": "The polarons for Wraithii are harvested by deep-space mining scoops manned usually by hard-core prospectors.  These polarons are then shipped to military installations for encapsulation in the mar-graviton field (a type of field that Federation scientists are still struggling to understand) that will hold them until they impact at a speed of greater than 20 kilometers an hour.  Needless to say, the final packets are handled with kid gloves.  It is a testament to the safety protocols put in place by the Bureau that only a few minor accidents have ever occurred since they stole the plans for this weapon from the Polaris...",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3128: {
        "resource_type": "desc",
        "id": "3128",
        "name": "Battery Pack",
        "text": "Most traders who have been working in space for more than a few years have at least one of these fitted onto their vessels.  In over a thousand years this simple design of several interlocking superconductor rings has remained virtually unchanged and has provided extra energy storage for countless numbers of ships, giving them that extra jump that everyone so often needs.",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3129: {
        "resource_type": "desc",
        "id": "3129",
        "name": "Heavy Weapons License",
        "text": "Heavy Weapons License:\\n\\nThe Holder of this License is able to purchase the following items classed as 'Heavy Weapons' by the Federation Security Council: Medium Blaster, Medium Blaster Turret, Heavy Blaster Turret (subject to military approval), Quad Light Blaster Turret (also requires 'Protective Technologies License' and subject to military approval), Thunderhead Lance.",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3130: {
        "resource_type": "desc",
        "id": "3130",
        "name": "Missile Weapons License",
        "text": "Missile Weapons License:\\n\\nThe Holder of this License is able to purchase the following items classed as 'Missile Weapons' by the Federation Security Council: IR Missile Launcher, IR Missile, Radar Missile Launcher, Radar Missile, Gravimetric Missile Launcher (subject to military approval), Gravimetric Missile (subject to military approval).",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3131: {
        "resource_type": "desc",
        "id": "3131",
        "name": "Fighter Bay License",
        "text": "Fighter Bay License:\\n\\nThe Holder of this License is able to purchase the following items classed as 'Fighter Bays' or as 'Carried Fighters' by the Federation Security Council: Thunderhead Bay, Thunderhead, Viper Bay (subject to military approval), Viper (subject to military approval), Anaconda Bay (subject to military approval), Anaconda (subject to military approval).",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3132: {
        "resource_type": "desc",
        "id": "3132",
        "name": "Protective Technologies License",
        "text": "Protective Technologies License:\\n\\nThe Holder of this License is able to purchase the following items classed as 'Protective Technologies' by the Federation Security Council: Quad Light Blaster Turret (also requires 'Heavy Weapons License' and subject to military approval), Carbon Fiber, Titanium Lattice (subject to military approval), Shield Recharger (subject to military approval), Shield Buffer (subject to military approval), Civilian IR Jammer, Civilian Radar Jammer, Military IR Jammer (subject to military approval), Military Radar Jammer (subject to military approval).",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3133: {
        "resource_type": "desc",
        "id": "3133",
        "name": "Thorium Reactor - Ionization",
        "text": "This is what happens when you own a dodgy Thorium Reactor from \\qJoe's Magic Thorium Reactor Saleyard(tm)\\q.  Having forked over your hard earned, you'll be willing to bet you'll find yourself getting kicked royally in the bum as your cheapo Thorium Reactor blows.  You will probably be able to limp into port, so long as no pirates notice that you have little chance of evading them.  Of course, if you want to sell it before this happens, be our guest.",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3134: {
        "resource_type": "desc",
        "id": "3134",
        "name": "Ion Dissipator",
        "text": "This outfit, stolen from Rauther when the engineer Tomak Gemmell defected to the Rebellion, is actually a series of radiative surfaces that radiate the energy buildup that causes ionization out into the surrounding space, allowing ships to function more fully under an ionizing attack.",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3135: {
        "resource_type": "desc",
        "id": "3135",
        "name": "Capital Ships License",
        "text": "Capital Ships License:\\n\\nThe Holder of this License is able to purchase the following ships classed as 'Capital Ships' by the Federation Security Council: Leviathan, Pegasus, Starliner, IDA Frigate (also requires 'Capital Warships License'), Federation Destroyer (also requires 'Capital Warships License' and subject to military approval), Federation Carrier (also requires 'Capital Warships License' and subject to military approval){P30\\q.\\q \\q.\\n\\nREQUIRES YOU TO REGISTER EV NOVA\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3136: {
        "resource_type": "desc",
        "id": "3136",
        "name": "Capital Warships License",
        "text": "Capital Warships License:\\n\\nThe Holder of this License is able to purchase the following ships classed as 'Capital Warships' by the Federation Security Council: IDA Frigate, Federation Patrol Boat (subject to military approval), Federation Destroyer (also requires 'Capital Ships License' and subject to military approval), Federation Carrier (also requires 'Capital Ships License' and subject to military approval){P30\\q.\\q \\q.\\n\\nREQUIRES YOU TO REGISTER EV NOVA\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3137: {
        "resource_type": "desc",
        "id": "3137",
        "name": "Exotic Ships & Weapons License",
        "text": "Exotic Ships & Weapons License:\\n\\nThe Holder of this License is able to purchase those ships and items classed as 'Exotic Ships' or as 'Exotic Weapons' and all items of any other classification as classified by the Federation Security Council{P30\\q.\\q \\q.\\n\\nREQUIRES YOU TO REGISTER EV NOVA\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3138: {
        "resource_type": "desc",
        "id": "3138",
        "name": "Wraith Cloaking Device",
        "text": "The Wraith have an instinctual ability to cloak.  Much in the same way a human will put on a coat for certain situations, a Wraith will be able to cloak.  It is a fairly big mystery how this occurs, but needless to say at one moment the Wraith will be there and the next it won't.",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3139: {
        "resource_type": "desc",
        "id": "3139",
        "name": "Wraith Fast Jump",
        "text": "Living totally in the cold void of deep space has led to some amazing adaptations for the Wraith.  The same evolutionary forces that led to opposable thumbs for humans has also led to unbelievable advantages for the wraith in their natural environment.  While a human can run, jump and chew gum at the same time, a wraith may choose to jump at any time without slowing down to stop.",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3140: {
        "resource_type": "desc",
        "id": "3140",
        "name": "Cloaking Organ - Pol v1.0",
        "text": "The Ver'ash, working with the P'aedt on data recovered from encounters with the Wraith, have managed to duplicate their 'cloaking' capabilities.  There is still an energy signature that can be easily be read by most sensor systems, but any ship with the Cloaking Organ is invisible to the naked eye and is extremely difficult to target.",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3141: {
        "resource_type": "desc",
        "id": "3141",
        "name": "Cloaking Organ - Pol v1.0",
        "text": "With a great deal of research and exhaustive trials, the Ver'ash, working with the P'aedt, have improved upon their original Cloaking Organ.  No longer does the organ leave behind a noticeable energy signature, making the cloaked ship almost impossible to detect.",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3142: {
        "resource_type": "desc",
        "id": "3142",
        "name": "Asteroid Mining Laser",
        "text": "When mankind first began exploring space, one of the many things they were looking for was new sources of raw materials, and the asteroids of many systems proved to hold a relative bonanza of near-pure metals and minerals.  The Pyrogenesis Asteroid Mining Laser is the tool of choice to break up passing asteroids and to get at the contained metals.  Over the past millennia, the basic design has changed only minimally, but it still remains popular with asteroid prospectors the galaxy over.",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3143: {
        "resource_type": "desc",
        "id": "3143",
        "name": "Asteroid Scoop",
        "text": "For the would-be asteroid prospector, this is the second piece of necessary equipment.  Blowing up asteroids, while being fun, is only half the job; a prospector needs to be able to scoop up the resulting debris.  The Asteroid Scoop is simply that, a small ram-scoop that picks up any useful products released in the break-up of an asteroid.",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3144: {
        "resource_type": "desc",
        "id": "3144",
        "name": "Dr. Ralph's Exploration Map",
        "text": "No desc req'd",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3145: {
        "resource_type": "desc",
        "id": "3145",
        "name": "Tunnelling Organ",
        "text": "By observing the Wraith, the P'aedt learned that instead of projecting hyperspace around them and then moving, they tunnelled directly into hyperspace, allowing them to hyperjump without stopping.  Now, with the experimental Tunnelling Organ, the Polaris are seeking to emulate this capability.",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3146: {
        "resource_type": "desc",
        "id": "3146",
        "name": "Tunnelling Organ",
        "text": "By observing the Wraith, the P'aedt learned that instead of projecting hyperspace around them and then moving, they tunnelled directly into hyperspace, allowing them to hyperjump without stopping.  Now, with the Tunnelling Organ, they have managed to emulate this remarkable capability.",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3147: {
        "resource_type": "desc",
        "id": "3147",
        "name": "Multi-Jump Organ",
        "text": "The Ver'ash and the P'aedt, working together on Ver'a Se, have grown an organ that combines the tunnelling capabilities of the Wraith with more traditional hyperspace manipulation techniques. It enables a ship to change direction in hyperspace, allowing for multiple jumps to be performed as if performing a single jump.\\n\\nAs yet, only a maximum of ten jumps are possible due to organ fatigue, but it is a major leap forward for Polaris hyperspatial technology.",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3148: {
        "resource_type": "desc",
        "id": "3148",
        "name": "Polaron Multi-Torpedo Tube",
        "text": "Like the simpler Polaron Torpedo Tube, this launcher ties into a ship's main computer core (or neural network, in the case of Polaris ships).  It tracks nearby hostile ships, and then calculates the complex field generation parameters for the Polaron Flux Coils in the tube.  By varying the quantity, spin and charge of the newly generated polarons, the tube can give the polaron 'virtual structure' allowing it to replicate itself into five separate copies that begin tracking the local hostile ships{P30\\q.\\q \\q.\\n\\nREQUIRES YOU TO REGISTER EV NOVA\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3149: {
        "resource_type": "desc",
        "id": "3149",
        "name": "Polaron Multi-Torpedo",
        "text": "The Polaron Multi-Torpedo takes non-corporeal engineering to the extreme.  The charge and spin of the huge polaron virtual structure is set by the launcher at firing time, much like the simpler Polaron Torpedoes.  However, in the case of the Multi-Torpedo, the chaos mathematics of the field interaction allows the neural net of the Polaris vessel to create virtual sub-structures that get activated shortly after launch, creating five simple Torpedoes all capable of attacking different targets{P30\\q.\\q \\q.\\n\\nREQUIRES YOU TO REGISTER EV NOVA\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3150: {
        "resource_type": "desc",
        "id": "3150",
        "name": "Wraith Cannon",
        "text": "Wraithii are tiny capsules of polarons contained in a mar-graviton field.  A Wraith Cannon fires these capsules via simple biomechanics, and the capsules burst on impact, releasing a powerful kinetic force.  These guns are mounted as standard on the Dragon, and can be retrofitted to most ships on the market.  And now that they have been modified to allow them to shoot while the parent ship is cloaked, they are even more effective.  The Nil'kemorya keep a careful eye on these weapons, however, and only the most favored of outsiders are ever allowed to buy them.",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3151: {
        "resource_type": "desc",
        "id": "3151",
        "name": "Wraithii",
        "text": "The polarons for Wraithii are harvested by deep-space mining scoops run by the Tre'pira.  These polarons are then shipped to P'aedt facilities for encapsulation in the mar-graviton field that will hold them until they impact at a speed of greater than 20 kilometers an hour.  Needless to say, the final packets are handled with kid gloves.  It is a testament to the Tre'pira and the P'aedt that no accidents with Wraithii have ever occurred.",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3152: {
        "resource_type": "desc",
        "id": "3152",
        "name": "Polaron Torpedo Tube",
        "text": "This launcher ties into a ship's main computer core (or neural network, in the case of Polaris ships).  It tracks a target ship, and then calculates the complex field generation parameters for the Polaron Flux Coils in the tube.  By varying the quantity, spin and charge of the newly generated polarons, the tube can give the polaron 'virtual structure' a good bead on a target before the preprogrammed field generator in the heart of the energy burst takes over.  And with a few relatively minor adjustments, it is now possible to use this weapon while the parent ship is cloaked{P30\\q.\\q \\q.\\n\\nREQUIRES YOU TO REGISTER EV NOVA\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3153: {
        "resource_type": "desc",
        "id": "3153",
        "name": "Polaron Torpedo",
        "text": "Having no mass, the Polaron Torpedo is a masterpiece of non-corporeal engineering.  The charge and spin of the huge polaron virtual structure is set by the launcher at firing time.  The chaos mathematics of the field interaction is calculated by the neural net of the Polaris vessel, which makes sure that the field will collapse in such a way that it will steer toward the target from the tube.  A tiny field generator hovering in the middle of the torpedo modifies the field strengths to correct for mid-flight target variations{P30\\q.\\q \\q.\\n\\nREQUIRES YOU TO REGISTER EV NOVA\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3154: {
        "resource_type": "desc",
        "id": "3154",
        "name": "Polaron Multi-Torpedo Tube",
        "text": "Like the simpler Polaron Torpedo Tube, this launcher ties into a ship's main computer core (or neural network, in the case of Polaris ships).  It tracks nearby hostile ships, and then calculates the complex field generation parameters for the Polaron Flux Coils in the tube.  By varying the quantity, spin and charge of the newly generated polarons, the tube can give the polaron 'virtual structure' allowing it to replicate itself into five separate copies that begin tracking the local hostile ships.  And, again like the simpler version, the Multi-Torpedo Tube is also now capable of being fired while cloaked{P30\\q.\\q \\q.\\n\\nREQUIRES YOU TO REGISTER EV NOVA\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3155: {
        "resource_type": "desc",
        "id": "3155",
        "name": "Polaron Multi-Torpedo",
        "text": "The Polaron Multi-Torpedo takes non-corporeal engineering to the extreme.  The charge and spin of the huge polaron virtual structure is set by the launcher at firing time, much like the simpler Polaron Torpedoes.  However, in the case of the Multi-Torpedo, the chaos mathematics of the field interaction allows the neural net of the Polaris vessel to create virtual sub-structures that get activated shortly after launch, creating five simple Torpedoes all capable of attacking different targets{P30\\q.\\q \\q.\\n\\nREQUIRES YOU TO REGISTER EV NOVA\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3156: {
        "resource_type": "desc",
        "id": "3156",
        "name": "Pirate Thunderhead Bay",
        "text": "The schematics for this Pirate Thunderhead bay look both impressive and practical, but you're a bit unsure as to how you'll fit it to your current vessel, although having the ability to launch three Pirate Thunderheads at your foes could never hurt{P30\\q.\\q \\q.\\n\\nREQUIRES YOU TO REGISTER EV NOVA\\q}{b424 \\q\\n\\nYou stare at this item, and the others around it, for several long, sad moments, knowing that you may never be able to buy any of them ever again.\\q \\q\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3157: {
        "resource_type": "desc",
        "id": "3157",
        "name": "Pirate Thunderhead",
        "text": "The Pirate Thunderhead, like its civilian cousin, is so named for its main weapon, the Thunderhead Lance.  Upgraded beyond even the deadly capabilities of the basic Thunderhead, this pirate version has enough armor to allow it to go up against even the largest ships, and enough speed to allow it to stay with most craft that try to flee{P30\\q.\\q \\q.\\n\\nREQUIRES YOU TO REGISTER EV NOVA\\q}{b424 \\q\\n\\nYou stare at this item, and the others around it, for several long, sad moments, knowing that you may never be able to buy any of them ever again.\\q \\q\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3158: {
        "resource_type": "desc",
        "id": "3158",
        "name": "Firebird Bay",
        "text": "The Auroran shipwrights can install the electromag catapults for Firebird launching quite quickly.  The conversion also includes the appropriate Firebird housing facilities, allowing for a maximum of six of them{P30\\q.\\q \\q.\\n\\nREQUIRES YOU TO REGISTER EV NOVA\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3159: {
        "resource_type": "desc",
        "id": "3159",
        "name": "Firebird",
        "text": "Firebirds are the main Auroran fighter.  Their engines are simple, to say the least.  Their task is to protect the Phoenix from attack by smaller fighters such as the Viper, while the Phoenix take on the heavier ships.  The Firebird is slower than the Viper, but not by enough to give the Viper a decisive edge.  Battles between the two often come down to individual skill.  Many a Federation/Auroran border skirmish has come to a halt while the two sides watch a Firebird/Viper dogfight between renowned pilots{P30\\q.\\q \\q.\\n\\nREQUIRES YOU TO REGISTER EV NOVA\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3160: {
        "resource_type": "desc",
        "id": "3160",
        "name": "Firebird Bay",
        "text": "The Auroran shipwrights can install the electromag catapults for Firebird launching quite quickly.  The conversion also includes the appropriate Firebird housing facilities, allowing for a maximum of six of them{P30\\q.\\q \\q.\\n\\nREQUIRES YOU TO REGISTER EV NOVA\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3161: {
        "resource_type": "desc",
        "id": "3161",
        "name": "Firebird",
        "text": "Firebirds are the main Auroran fighter.  Their engines are simple, to say the least.  Their task is to protect the Phoenix from attack by smaller fighters such as the Viper, while the Phoenix take on the heavier ships.  The Firebird is slower than the Viper, but not by enough to give the Viper a decisive edge.  Battles between the two often come down to individual skill.  Many a Federation/Auroran border skirmish has come to a halt while the two sides watch a Firebird/Viper dogfight between renowned pilots{P30\\q.\\q \\q.\\n\\nREQUIRES YOU TO REGISTER EV NOVA\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3162: {
        "resource_type": "desc",
        "id": "3162",
        "name": "Phoenix Bay",
        "text": "Phoenix bays are noisy, smelly and generally fairly grimy.  If you can put up with this, you'll have some serious mobile firepower at your disposal, as the bay is capable of housing up to three of these vicious little fighters{P30\\q.\\q \\q.\\n\\nREQUIRES YOU TO REGISTER EV NOVA\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3163: {
        "resource_type": "desc",
        "id": "3163",
        "name": "Phoenix",
        "text": "The Phoenix is yet another example of the Auroran will to survive.  The Phoenix is slow and turns badly.  One would think that it would be target practice for enemy pilots.  It is, but it has one redeeming feature: it has almost as good armor plating as a Thunderhead.  They plough through fire corridors with impunity, and attack in groups to maximize firepower.  The Phoenix can wear a missile from an Anaconda, but a Viper will stay on its tail and pound it mercilessly.  Suffice to say that Phoenix pilots suffer the greatest rate of attrition of any group in the Auroran armed forces{P30\\q.\\q \\q.\\n\\nREQUIRES YOU TO REGISTER EV NOVA\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3164: {
        "resource_type": "desc",
        "id": "3164",
        "name": "Phoenix Bay",
        "text": "Phoenix bays are noisy, smelly and generally fairly grimy.  If you can put up with this, you'll have some serious mobile firepower at your disposal, as the bay is capable of housing up to three of these vicious little fighters{P30\\q.\\q \\q.\\n\\nREQUIRES YOU TO REGISTER EV NOVA\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3165: {
        "resource_type": "desc",
        "id": "3165",
        "name": "Phoenix",
        "text": "The Phoenix is yet another example of the Auroran will to survive.  The Phoenix is slow and turns badly.  One would think that it would be target practice for enemy pilots.  It is, but it has one redeeming feature: it has almost as good armor plating as a Thunderhead.  They plough through fire corridors with impunity, and attack in groups to maximize firepower.  The Phoenix can wear a missile from an Anaconda, but a Viper will stay on its tail and pound it mercilessly.  Suffice to say that Phoenix pilots suffer the greatest rate of attrition of any group in the Auroran armed forces{P30\\q.\\q \\q.\\n\\nREQUIRES YOU TO REGISTER EV NOVA\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3166: {
        "resource_type": "desc",
        "id": "3166",
        "name": "Pirate Viper Bay",
        "text": "Pirates know about violence, and the threat of violence.  They also know about hounding individual ships in packs.  However, they also value speed, and the Pirate Viper Bay launches them far faster than any other type of bay outside of Polaris Space, allowing them to swarm over their foes with frightening rapidity.  So despite only being able to house a maximum of two Pirate Vipers, many pirates vessels have at least one.  With one of these bays on board, you'll have a fast pack at your disposal at all times{P30\\q.\\q \\q.\\n\\nREQUIRES YOU TO REGISTER EV NOVA\\q}{b424 \\q\\n\\nYou stare at this item, and the others around it, for several long, sad moments, knowing that you may never be able to buy any of them ever again.\\q \\q\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3167: {
        "resource_type": "desc",
        "id": "3167",
        "name": "Pirate Viper",
        "text": "As soon as Comara released the Viper frame on the general market, a few shiploads of frames were bought up by notorious pirate shipwright Olaf Greyshoulders.  He and his crew have totally refitted the shell, and the familiar shape of its advanced armor plating hides a wealth of minor and major improvements to the basic idea.  But, as with all Greyshoulders upgrades, there is a hefty price to pay for the improved model.  It's up to you to decide whether it's worth it{P30\\q.\\q \\q.\\n\\nREQUIRES YOU TO REGISTER EV NOVA\\q}{b424 \\q\\n\\nYou stare at this item, and the others around it, for several long, sad moments, knowing that you may never be able to buy any of them ever again.\\q \\q\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3168: {
        "resource_type": "desc",
        "id": "3168",
        "name": "Pirate Viper Bay",
        "text": "Pirates know about violence, and the threat of violence.  They also know about hounding individual ships in packs.  However, they also value speed, and the Pirate Viper Bay launches them far faster than any other type of bay outside of Polaris Space, allowing them to swarm over their foes with frightening rapidity.  So despite only being able to house a maximum of two Pirate Vipers, many pirates vessels have at least one.  With one of these bays on board, you'll have a fast pack at your disposal at all times{P30\\q.\\q \\q.\\n\\nREQUIRES YOU TO REGISTER EV NOVA\\q}{b424 \\q\\n\\nYou stare at this item, and the others around it, for several long, sad moments, knowing that you may never be able to buy any of them ever again.\\q \\q\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3169: {
        "resource_type": "desc",
        "id": "3169",
        "name": "Pirate Viper",
        "text": "As soon as Comara released the Viper frame on the general market, a few shiploads of frames were bought up by notorious pirate shipwright Olaf Greyshoulders.  He and his crew have totally refitted the shell, and the familiar shape of its advanced armor plating hides a wealth of minor and major improvements to the basic idea.  But, as with all Greyshoulders upgrades, there is a hefty price to pay for the improved model.  It's up to you to decide whether it's worth it{P30\\q.\\q \\q.\\n\\nREQUIRES YOU TO REGISTER EV NOVA\\q}{b424 \\q\\n\\nYou stare at this item, and the others around it, for several long, sad moments, knowing that you may never be able to buy any of them ever again.\\q \\q\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3170: {
        "resource_type": "desc",
        "id": "3170",
        "name": "Rebel Viper Bay",
        "text": "Mr. Donald Chick and his engineers have spent years trying to adapt the enormous fighter bays so that they can be fitted into the relatively small ships that the Rebels have managed to get their hands on.  With it, you will be able to hold and launch up to four of the upgraded Rebel Vipers.  As far as adaptive engineering solutions go, this one certainly stands up well...",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3171: {
        "resource_type": "desc",
        "id": "3171",
        "name": "Rebel Viper",
        "text": "When General (ret) Cade 'Sundown' Smart defected to the Rebellion, he brought with him plans for all Federation vessels, and also intelligence on many ships used by other governments.  With this in hand, Donald Chick and his engineers set to work building and upgrading existing ships.  The resulting variant of the Viper is virtually unmatched anywhere in space.",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3172: {
        "resource_type": "desc",
        "id": "3172",
        "name": "Rebel Viper Bay",
        "text": "Mr. Donald Chick and his engineers have spent years trying to adapt the enormous fighter bays so that they can be fitted into the relatively small ships that the Rebels have managed to get their hands on.  With it, you will be able to hold and launch up to four of the upgraded Rebel Vipers.  As far as adaptive engineering solutions go, this one certainly stands up well...",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3173: {
        "resource_type": "desc",
        "id": "3173",
        "name": "Rebel Viper",
        "text": "When General (ret) Cade 'Sundown' Smart defected to the Rebellion, he brought with him plans for all Federation vessels, and also intelligence on many ships used by other governments.  With this in hand, Donald Chick and his engineers set to work building and upgrading existing ships.  The resulting variant of the Viper is virtually unmatched anywhere in space.",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3174: {
        "resource_type": "desc",
        "id": "3174",
        "name": "Rebel Viper Bay",
        "text": "Mr. Donald Chick and his engineers have spent years trying to adapt the enormous fighter bays so that they can be fitted into the relatively small ships that the Rebels have managed to get their hands on.  With it, you will be able to hold and launch up to four of the upgraded Rebel Vipers.  As far as adaptive engineering solutions go, this one certainly stands up well...",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3175: {
        "resource_type": "desc",
        "id": "3175",
        "name": "Rebel Viper",
        "text": "When General (ret) Cade 'Sundown' Smart defected to the Rebellion, he brought with him plans for all Federation vessels, and also intelligence on many ships used by other governments.  With this in hand, Donald Chick and his engineers set to work building and upgrading existing ships.  The resulting variant of the Viper is virtually unmatched anywhere in space.",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3176: {
        "resource_type": "desc",
        "id": "3176",
        "name": "Rebel Viper Bay",
        "text": "Mr. Donald Chick and his engineers have spent years trying to adapt the enormous fighter bays so that they can be fitted into the relatively small ships that the Rebels have managed to get their hands on.  With it, you will be able to hold and launch up to four of the upgraded Rebel Vipers.  As far as adaptive engineering solutions go, this one certainly stands up well...",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3177: {
        "resource_type": "desc",
        "id": "3177",
        "name": "Rebel Viper",
        "text": "When General (ret) Cade 'Sundown' Smart defected to the Rebellion, he brought with him plans for all Federation vessels, and also intelligence on many ships used by other governments.  With this in hand, Donald Chick and his engineers set to work building and upgrading existing ships.  The resulting variant of the Viper is virtually unmatched anywhere in space.",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3178: {
        "resource_type": "desc",
        "id": "3178",
        "name": "Viper bay",
        "text": "A few days is all it takes to convert sections of your ship into a launchbay for Viper fighters.  The conversion comes complete with everything you'll need to refuel, re-arm and service a maximum force of four Vipers.\\n\\nRequires: Fighter Bay {P30\\qLicense\\q \\qLicense, REQUIRES YOU TO REGISTER EV NOVA\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3179: {
        "resource_type": "desc",
        "id": "3179",
        "name": "Viper",
        "text": "With the rapid development of space flight, it was inevitable that sports (particularly racing) would come to fruition sooner rather than later.  Power Sled racing stood up to the challenge.  A few intrepid hot-rodders noticed that one particular sled, the Viper, took very well to a bit of extra weight in the form of armor and armament.  With a little engine tweaking, these modified Vipers, designated F-23, were selected by the Federation as the mainstay of their fighter wings.\\n\\nRequires: Fighter Bay {P30\\qLicense\\q \\qLicense, REQUIRES YOU TO REGISTER EV NOVA\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3180: {
        "resource_type": "desc",
        "id": "3180",
        "name": "Viper bay",
        "text": "A few days is all it takes to convert sections of your ship into a launchbay for Viper fighters.  The conversion comes complete with everything you'll need to refuel, re-arm and service a maximum force of four Vipers.\\n\\nRequires: Fighter Bay {P30\\qLicense\\q \\qLicense, REQUIRES YOU TO REGISTER EV NOVA\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3181: {
        "resource_type": "desc",
        "id": "3181",
        "name": "Viper",
        "text": "With the rapid development of space flight, it was inevitable that sports (particularly racing) would come to fruition sooner rather than later.  Power Sled racing stood up to the challenge.  A few intrepid hot-rodders noticed that one particular sled, the Viper, took very well to a bit of extra weight in the form of armor and armament.  With a little engine tweaking, these modified Vipers, designated F-23, were selected by the Federation as the mainstay of their fighter wings.\\n\\nRequires: Fighter Bay {P30\\qLicense\\q \\qLicense, REQUIRES YOU TO REGISTER EV NOVA\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3182: {
        "resource_type": "desc",
        "id": "3182",
        "name": "Anaconda Bay",
        "text": "Anacondas can provide long-range intercept capability for a vessel.  This bay allows you to outfit a maximum of two of them.\\n\\nRequires: Fighter Bay {P30\\qLicense\\q \\qLicense, REQUIRES YOU TO REGISTER EV NOVA\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3183: {
        "resource_type": "desc",
        "id": "3183",
        "name": "Anaconda",
        "text": "The main problem with the Viper as a fighter craft is a complete lack of any form of explosive projectile.  A new variant that has the 'long distance kill' capacity, based on the Viper chassis, has been the Federation's choice of Space Superiority Fighter ever since.  Although this ship, named the Anaconda, suffers from a slightly slower acceleration and top speed than the Viper, its ability to destroy enemy fighters before that fighter can get within gun range more than compensates.\\n\\nRequires: Fighter Bay {P30\\qLicense\\q \\qLicense, REQUIRES YOU TO REGISTER EV NOVA\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3184: {
        "resource_type": "desc",
        "id": "3184",
        "name": "Anaconda Bay",
        "text": "Anacondas can provide long-range intercept capability for a vessel.  This bay allows you to outfit a maximum of two of them.\\n\\nRequires: Fighter Bay {P30\\qLicense\\q \\qLicense, REQUIRES YOU TO REGISTER EV NOVA\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3185: {
        "resource_type": "desc",
        "id": "3185",
        "name": "Anaconda",
        "text": "The main problem with the Viper as a fighter craft is a complete lack of any form of explosive projectile.  A new variant that has the 'long distance kill' capacity, based on the Viper chassis, has been the Federation's choice of Space Superiority Fighter ever since.  Although this ship, named the Anaconda, suffers from a slightly slower acceleration and top speed than the Viper, its ability to destroy enemy fighters before that fighter can get within gun range more than compensates.\\n\\nRequires: Fighter Bay {P30\\qLicense\\q \\qLicense, REQUIRES YOU TO REGISTER EV NOVA\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3186: {
        "resource_type": "desc",
        "id": "3186",
        "name": "Chrome Valk Upgrade",
        "text": "Sigma Shipyard engineers recently came up with a relatively simple process for upgrading the standard Starbridge into the far more capable Starbridge C, most commonly known as the Chrome Valkyrie for reasons known only to its original designers.  The process takes barely 24 hours and at the end of it the new ship is ready for action.  The only drawback is that the process will strip all of your outfits from your old model and only leaves the 'standard' fittings for the Starbridge C type{P30\\q.\\q \\q.\\n\\nREQUIRES YOU TO REGISTER EV NOVA\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3187: {
        "resource_type": "desc",
        "id": "3187",
        "name": "Rebel Starbridge Upgrade",
        "text": "Before he defected, Mr. Donald Chick and his engineers were working on processes of updating older versions of spare vessels to later models.  Since then he has perfected the techniques required, and here is the resulting process to upgrade a standard Starbridge to the slightly more capable Rebellion standard type.  It takes just short of 24 hours and strips all excess outfits, leaving only those outfits defined as standard for the Rebel version.  However it is cheap, and relatively simple{P30\\q.\\q \\q.\\n\\nREQUIRES YOU TO REGISTER EV NOVA\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3188: {
        "resource_type": "desc",
        "id": "3188",
        "name": "Rebel Valkyrie Upgrade",
        "text": "Before he defected, Mr. Donald Chick and his engineers were working on processes of updating older versions of spare vessels to later models.  Since then he has perfected the techniques required, and here is the resulting process to upgrade a standard Valkyrie to the slightly more capable Rebellion standard type.  It takes just short of 24 hours and strips all excess outfits, leaving only those outfits defined as standard for the Rebel version.  However it is cheap, and relatively simple{P30\\q.\\q \\q.\\n\\nREQUIRES YOU TO REGISTER EV NOVA\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3189: {
        "resource_type": "desc",
        "id": "3189",
        "name": "Pirate Starbridge Upgrade",
        "text": "In a direct rip-off of the Sigma Shipyards upgrading process (which was probably taken from the upgrading process used by engineers working for the Rebellion), underhanded outfitters can now upgrade your standard Starbridge to the base level Pirate type.  Like the Sigma Shipyards process, all existing outfits are stripped from your vessel, leaving only those outfits deemed to be standard according to the new vessel type{P30\\q.\\q \\q.\\n\\nREQUIRES YOU TO REGISTER EV NOVA\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3190: {
        "resource_type": "desc",
        "id": "3190",
        "name": "Pirate Valkyrie Upgrade",
        "text": "With only a few relatively minor modifications, many shady outfitters have been able to take the Sigma Shipyards Starbridge upgrading process and use it to upgrade standard Valkyries to the much more feared pirate type.  Like all processes of this type, all existing outfits are stripped from your vessel, leaving only those outfits deemed to be standard according to the parameters of the new model{P30\\q.\\q \\q.\\n\\nREQUIRES YOU TO REGISTER EV NOVA\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3191: {
        "resource_type": "desc",
        "id": "3191",
        "name": "Drop Bear Repellant",
        "text": "You are a little dubious as to the veracity of the claims of this shifty, grinning merchant trying to sell you bottles of Auroran Drop Bear repellant.  But you cannot help feeling that anything that helps protect you from the well-documented deadly Drop Bear attacks will stand you in good stead.\\n\\nStill, it is strange that just about everyone who walks past you starts grinning and shaking their heads as you consider buying from the smiling merchant...",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3192: {
        "resource_type": "desc",
        "id": "3192",
        "name": "Medium Blaster",
        "text": "Pyrogenesis' midrange product is the unimaginatively named Medium Blaster.  This variant is normally carried by capital ships only; the weight alone makes it difficult for anything smaller to mount it.  While it's slower and more bulky than its lesser sibling, the Medium Blaster is much more powerful.  The lack of a turret mechanism does drop the weight some.  And you can buy it here without a license, but you had better be wary of Federation scans..{b424 \\q.\\n\\nYou stare at this item, and the others around it, for several long, sad moments, knowing that you may never be able to buy any of them ever again.\\q \\q.\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3193: {
        "resource_type": "desc",
        "id": "3193",
        "name": "MB Turret",
        "text": "The Medium Blaster really comes into its own when it becomes turreted.  Combined with sophisticated Glenn:Cyber targeting scopes, these weapons score easy hits on all but the smallest space vessels.  The Medium Blaster Turret does tend to lag a little on the faster capital ships.  The IDA Frigate mounted two of these batteries as standard.  And you can buy it here without a license, but you had better be wary of Federation scans..{b424 \\q.\\n\\nYou stare at this item, and the others around it, for several long, sad moments, knowing that you may never be able to buy any of them ever again.\\q \\q.\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3194: {
        "resource_type": "desc",
        "id": "3194",
        "name": "HB Turret",
        "text": "So big and slow that only a turret mechanism allows it to hit anything at all, the Heavy Blaster Turret is the grand-daddy of the Pyrogenesis line of directed energy firepower.  Mounted as standard on the E-60 Carrier, the pride of the Federation fleet, the Heavy Blaster chews through shields and armor alike.  The short range and slow speed of the enormous packets limit the effectiveness of this weapon at anything other than boarding range.  And you can buy it here without a license, but you had better be wary of Federation scans...",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3195: {
        "resource_type": "desc",
        "id": "3195",
        "name": "QLB Turret",
        "text": "Comprised of quadruple Pyrogenesis Light Blasters on the most technically advanced turret they offer, the Quad Light Blaster system comes with a guarantee that it will dispose of your hostile fighter problems once and for all.  Shipboard gunners salivate at the thought of being permanently assigned to one of these beauties.  While the QLB System is heavy, it pours a truly prodigious amount of fire into enemy fighter squadrons, and creates havoc in the ranks of even the most disciplined fighter wings.  And you can buy it here without a license, but you had better be wary of Federation scans...",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3196: {
        "resource_type": "desc",
        "id": "3196",
        "name": "IRM Launcher",
        "text": "Kayel Solutions (KLSol) have won 'Best of Show' 26 years running for their clever adaptation of the Infrared Missile launcher.  Based on the launcher mounted by the F-29 Anaconda and the E-41 Destroyer, the KLSol version is a tightly integrated set of standardized components that can easily swap between a hundred different classes of ship with only a minor, dealer serviceable tweak of the software.  The KLSol IR Missile Launcher does produce a fair amount of heat for such a small unit, but it's easily compensated for.  And you can buy it here without a license, but you had better be wary of Federation scans..{b424 \\q.\\n\\nYou stare at this item, and the others around it, for several long, sad moments, knowing that you may never be able to buy any of them ever again.\\q \\q.\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3197: {
        "resource_type": "desc",
        "id": "3197",
        "name": "IR Missile",
        "text": "The Infrared Missile uses the simplest of tracking systems to deliver its small payload.  It's not much to look at, but it's cheap and promiscuously available.  The weapon itself can be loaded into a number of aftermarket launchers, including several highly illegal handheld ones used by Rebellion Vacuum Soldiers.  And you can buy it here without a license, but you had better be wary of Federation scans..{b424 \\q.\\n\\nYou stare at this item, and the others around it, for several long, sad moments, knowing that you may never be able to buy any of them ever again.\\q \\q.\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3198: {
        "resource_type": "desc",
        "id": "3198",
        "name": "RM Launcher",
        "text": "GLiMMER, a band of propellerheads turned pro, created the first modern radar guided missile and launcher system way back in 2045 AD.  This design, produced under license by KLSol, is practically identical to that original design, albeit with KLSol's usual software driver genius.  You can mount this unit in any spacefaring vessel with enough expansion space to hold it.  There have even been some reports that it has been successfully incorporated into Auroran vessels!  And you can buy it here without a license, but you had better be wary of Federation scans..{b424 \\q.\\n\\nYou stare at this item, and the others around it, for several long, sad moments, knowing that you may never be able to buy any of them ever again.\\q \\q.\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3199: {
        "resource_type": "desc",
        "id": "3199",
        "name": "Radar Missile",
        "text": "Radar as a concept and as a useable weapons guidance system has been around since the middle of the twentieth century AD.  As humanity reached for the stars they brought their technology with them, and radar, which is not reliant on a medium for effectiveness, quickly became a necessary tool for guiding missiles.  This modern radar guided missile is a cheap GLiMMER knock-off.  And you can buy it here without a license, but you had better be wary of Federation scans..{b424 \\q.\\n\\nYou stare at this item, and the others around it, for several long, sad moments, knowing that you may never be able to buy any of them ever again.\\q \\q.\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3200: {
        "resource_type": "desc",
        "id": "3200",
        "name": "Disabling FPC Turret",
        "text": "As the FPC is cheap and easy to build the Auroran houses have opted to mount a turreted version of the cannon on almost all ships.  This particular version has been designed to specifically disable yet not destroy any targeted ships.  Auroran warriors use this weapon as their weapon of choice in their many and varied duels, and some even mount it as their standard battle weapon, claiming that they only wish to defeat their opponents, not destroy them.",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3201: {
        "resource_type": "desc",
        "id": "3201",
        "name": "Disabling RM Launcher",
        "text": "Many Auroran warriors have taken the basic GLiMMER radar missile launchers and modified them to launch the modified disable-only radar missiles they use in their many space-based duels.  The only main difference is a slightly wider bore so that the extra sensors required to sense ship activity can fit.",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3202: {
        "resource_type": "desc",
        "id": "3202",
        "name": "Disabling Radar Missile",
        "text": "To allow them to conduct space-based, yet non-lethal duels, the Aurorans have been forced to add some fairly sophisticated sensory equipment to their radar missiles.  The result is a missile with a slightly greater diameter than the basic radar missile design that allows warriors to fight to the utmost of their ability without fear of utterly destroying their opponents.",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3203: {
        "resource_type": "desc",
        "id": "3203",
        "name": "User Modified Ion Particle Cannon",
        "text": "The Rauther Power Industries Ion Particle Cannon is amongst the most powerful directed energy weapons in the known galaxy.  Mounted on a 360\u00a1/270\u00a1 firing platform, the weapons' accuracy is unmatched, delivering incredibly destructive pulses of charged helium nuclei. This particular version looks like it's a few decades old, and has been tinkered with and repaired by a number of different owners.  A few backyard tinkerers, and even one major weapon corporations seem interested in buying it, but only so they can pull it apart and have a look at what's been done to it.",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3204: {
        "resource_type": "desc",
        "id": "3204",
        "name": "Ion Particle Cannon",
        "text": "The Rauther Power Industries Ion Particle Cannon is amongst the most powerful directed energy weapons in the known galaxy.  Mounted on a 360\u00a1/270\u00a1 firing platform, the weapons accuracy is unmatched, delivering incredibly destructive pulses of charged helium nuclei. The weapon's rotating phase excels in damaging shields and armor. The weapon's only major drawbacks are its heavy power requirement and large mass.  And you can buy it here without a license, but you had better be wary of Federation scans..{b424 \\q.\\n\\nYou stare at this item, and the others around it, for several long, sad moments, knowing that you may never be able to buy any of them ever again.\\q \\q.\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3205: {
        "resource_type": "desc",
        "id": "3205",
        "name": "Sigma Engine Tune-up",
        "text": "If you are prepared to pay the exorbitant price, the Sigma Shipyards engineers will go over the engines of your ship with a fine-tooth comb, bringing out every possible bit of performance from your engine.  They will personalize every aspect of your engine to take advantage of every ounce of power, and make it as efficient as possible.  The end result is an engine that will accelerate faster, have a higher top speed, allow for slightly better maneuverability and will be more energy-efficient when hyperspacin{P30\\qg.\\q \\qg.\\n\\nREQUIRES YOU TO REGISTER EV NOVA\\q}{b424 \\q\\n\\nYou stare at this item, and the others around it, for several long, sad moments, knowing that you may never be able to buy any of them ever again.\\q \\q\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3206: {
        "resource_type": "desc",
        "id": "3206",
        "name": "Sigma Electrical Rewiring",
        "text": "The electrical wiring of ships created on a production line is never very efficient, as manufacturers are more interested in cutting costs than creating a perfect electrical system.  However, if you are prepared to pay the price, the Sigma engineers will rip out all the electrics of your ship and recraft them with far more attention to detail.  The resulting system should slightly increase the capabilities of your sensors, and give a boost to both your shielding capacity and your recharge rat{P30\\qe.\\q \\qe.\\n\\nREQUIRES YOU TO REGISTER EV NOVA\\q}{b424 \\q\\n\\nYou stare at this item, and the others around it, for several long, sad moments, knowing that you may never be able to buy any of them ever again.\\q \\q\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3207: {
        "resource_type": "desc",
        "id": "3207",
        "name": "Sigma Mount Reinforcement",
        "text": "The limits of guns and turrets on most vessels are decided by safety engineers, but with a little bit of reinforcement, it becomes possible to increase those limits.  The cost may be prohibitive, but for the ship captain who wants that much more firepower, the Sigma engineers will guarantee that by the time they are finished you should be able to fit four more guns and two more turrets to your vesse{P30\\ql.\\q \\ql.\\n\\nREQUIRES YOU TO REGISTER EV NOVA\\q}{b424 \\q\\n\\nYou stare at this item, and the others around it, for several long, sad moments, knowing that you may never be able to buy any of them ever again.\\q \\q\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3208: {
        "resource_type": "desc",
        "id": "3208",
        "name": "T1 Strength",
        "text": "Your power and skill match that of any Vell-os that has ever lived.  There is very little in the universe that can harm you now.",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3209: {
        "resource_type": "desc",
        "id": "3209",
        "name": "T0 Strength",
        "text": "Mighty beyond the understanding of even the Vell-os of old, your telepathic capabilities afford you protection against all but the most destructive of forces in the universe, and even they are often survivable.",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3211: {
        "resource_type": "desc",
        "id": "3211",
        "name": "Krypt Mind Attack",
        "text": "MY BRAIN HURTS!  This is a stupid d\u00ebsc to have to write.  Who bloody knows?  You can make people hurt with your brain! ",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3212: {
        "resource_type": "desc",
        "id": "3212",
        "name": "Sigma Mass Expansion",
        "text": "If you have a large enough ship, with lots of cargo space that you would like to swap out for a bit more weapons room, the Sigma Shipyards engineers can mount the required structural beams inside your ship and cut the necessary weapons ports in your hull.  They don't recommend this procedure more than once, as it could start to destabilise your vessel, and once done, it is virtually impossible to undo, as they have to dramatically change the overall integrity of your hull.  However, for a cost of 120 tons of cargo space, you can gain a total of 100 tons of room for any weapon emplacements you like{P30\\q.\\q \\q.\\n\\nREQUIRES YOU TO REGISTER EV NOVA\\q}{b424 \\q\\n\\nYou stare at this item, and the others around it, for several long, sad moments, knowing that you may never be able to buy any of them ever again.\\q \\q\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3213: {
        "resource_type": "desc",
        "id": "3213",
        "name": "Sigma Mass Addition",
        "text": "The Sigma Shipyards engineers are capable of adding numerous small 'weapons pods' to the outside of your hull without seriously unbalancing your vessel.  The result is a mere 5 extra tons of weapons space, but it is 5 tons gained without the loss of any cargo space and, as any pilot can tell you, that extra 5 tons can make all the difference{P30\\q.\\q \\q.\\n\\nREQUIRES YOU TO REGISTER EV NOVA\\q}{b424 \\q\\n\\nYou stare at this item, and the others around it, for several long, sad moments, knowing that you may never be able to buy any of them ever again.\\q \\q\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3214: {
        "resource_type": "desc",
        "id": "3214",
        "name": "Area Map - Vell-os",
        "text": "Placeholder text to prevent error from appearing on start-up. This description is never seen by the player.",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3217: {
        "resource_type": "desc",
        "id": "3217",
        "name": "Wraith Cannon",
        "text": "Wraithii are tiny capsules of polarons contained in a mar-graviton field.  A Wraith Cannon fires these capsules via simple biomechanics, and the capsules burst on impact, releasing a powerful kinetic force.  These guns are mounted as standard on the Dragon, and can be retrofitted to most ships on the market.  Only in recent times have the Polaris even allowed this item, which they consider to be low-tech, to be used by the Rebellion, and even then there were stringent controls placed upon them.",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3218: {
        "resource_type": "desc",
        "id": "3218",
        "name": "Wraithii",
        "text": "The polarons for Wraithii are harvested by deep-space mining scoops run by the Polaris worker caste.  These polarons are then shipped to P'aedt facilities for encapsulation in the mar-graviton field that will hold them until they impact at a speed of greater than 20 kilometers an hour.  Needless to say, the final packets are handled with kid gloves.  It is a testament to the capabilities of the Polaris that no accidents have ever occurred since they began shipping these weapons to the Rebellion.",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3219: {
        "resource_type": "desc",
        "id": "3219",
        "name": "Rebel Cloaking Device - illegal",
        "text": "Rebel Scientists, working in conjunction with Polaris Ver'ash, have devised a cloaking device for rebel ships.  Highly illegal, it is advised to not allow the customs inspector a good look at it.  You will be able to cloak in space, thus becoming all but invisible to your foes.",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3220: {
        "resource_type": "desc",
        "id": "3220",
        "name": "Bureau Bomb Outfit Called Desc",
        "text": "With a sudden whump, you realize that nobody escapes the Bureau that easily.  As the expanding gases engulf your body you wish you had never gotten yourself involved with the Bureau in the first place...",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3230: {
        "resource_type": "desc",
        "id": "3230",
        "name": "Thorium Reactor",
        "text": "After much argument you discover that the main saving of mass and energy in this poorer cousin of the Thorium reactors in Federation Carriers and the new models of Starbridge is in its radiation shielding and reaction-containing walls.  While it should work, if things go wrong, it may result in a rather large expanding ball of gas that you will end up being a part of{b424 \\q.\\n\\nYou stare at this item, and the others around it, for several long, sad moments, knowing that you may never be able to buy any of them ever again.\\q \\q.\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3231: {
        "resource_type": "desc",
        "id": "3231",
        "name": "Fission Reactor",
        "text": "If pure safety is one of your major concerns when it comes to power systems, then you had better skip this item.  However, if you want a quick power boost but do not have the cash or the clearance to buy the more expensive commercial items then this might be the answer.  Still, you have more than a few doubts that it performs as well as the backyard tinkerer who built it says it should..{b424 \\q.\\n\\nYou stare at this item, and the others around it, for several long, sad moments, knowing that you may never be able to buy any of them ever again.\\q \\q.\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3232: {
        "resource_type": "desc",
        "id": "3232",
        "name": "Carbon Fiber",
        "text": "The introduction of controlled impurities has made a relatively inexpensive process almost dirt cheap.\\n\\n\\qIt will degrade over time, {G\\qmate\\q \\qma'am\\q},\\q says the podgy grease-covered tinkerer, \\qSo you will have to regularly replace it.  Once every six months or so should be fine, but if you let it go too long, you will end up with a very expensive paint job, and no protection whatsoever.{b424 \\q\\\\\\q\\n\\nYou stare at this item, and the others around it, for several long, sad moments, knowing that you may never be able to buy any of them ever again.\\q \\q\\\\\\q\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3233: {
        "resource_type": "desc",
        "id": "3233",
        "name": "Military IR Jammer",
        "text": "This stolen version of the IR Jammer used by the Federation Navy was salvaged from a destroyed Federation Destroyer and then patched up. Highly illegal (and probably a little less capable than it was before its former housing was destroyed), but very inexpensive, it is still going to be far more capable than anything you can buy in the normal civilian market{b424 \\q.\\n\\nYou stare at this item, and the others around it, for several long, sad moments, knowing that you may never be able to buy any of them ever again.\\q \\q.\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3234: {
        "resource_type": "desc",
        "id": "3234",
        "name": "Military Radar Jammer",
        "text": "This is actually a real Federation Navy Radar Jammer, salvaged from debris after a space battle and restored to nearly its former condition.  However, it is highly illegal, but it is far better at confusing incoming missiles than the civilian version available nearly everywhere{b424 \\q.\\n\\nYou stare at this item, and the others around it, for several long, sad moments, knowing that you may never be able to buy any of them ever again.\\q \\q.\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3235: {
        "resource_type": "desc",
        "id": "3235",
        "name": "Exotic Ships & Weapons License",
        "text": "The 'Exotic Ships & Weapons License' is the most expensive and the most sought-after license, as it gives you access to all of the outfits classified by the Federation Navy as requiring a license.  The small hunched man before you grumpily informs you that his work will fool even the most capable sensor sweep by Federation interceptors{b424 \\q.\\n\\nYou stare at this item, and the others around it, for several long, sad moments, knowing that you may never be able to buy any of them ever again.\\q \\q.\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3236: {
        "resource_type": "desc",
        "id": "3236",
        "name": "Exotic Ships & Weapons License",
        "text": "The 'Exotic Ships & Weapons License' is the most expensive and the most sought-after license, as it gives you access to all of the outfits classified by the Federation Navy as requiring a license.  The small hunched man before you grumpily informs you that his work will fool even the most capable sensor sweep by Federation interceptors{b424 \\q.\\n\\nYou stare at this item, and the others around it, for several long, sad moments, knowing that you may never be able to buy any of them ever again.\\q \\q.\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3246: {
        "resource_type": "desc",
        "id": "3246",
        "name": "Thorium Reactor - bomb",
        "text": "Warning klaxons sound as the safeguards on your Thorium Reactor begin to catastrophically fail.  As explosions engulf your ship, you curse yourself for buying a cheap knock-off instead of the real thing...",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3247: {
        "resource_type": "desc",
        "id": "3247",
        "name": "Fission Reactor - disabled",
        "text": "All good things must come to an end, and unfortunately for this fission reactor, the end has come.  Pure and simple, you need to sell it for whatever you can get (telling the new owner it is shagged or not) and get a new power source.",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3248: {
        "resource_type": "desc",
        "id": "3248",
        "name": "Carbon Fiber - disabled",
        "text": "\\qIt looks like this is just starting to go,\\q says the podgy grease-covered tinkerer, \\qA nip and tuck here and there and it could be as good as new.\\q",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3249: {
        "resource_type": "desc",
        "id": "3249",
        "name": "Carbon Fiber - disabled",
        "text": "\\qIt looks like this is well on the way out,\\q says the podgy grease-covered tinkerer, \\qIf you want to return it to full effectiveness, you will need to replace most of it.\\q",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3250: {
        "resource_type": "desc",
        "id": "3250",
        "name": "Carbon Fiber - degraded",
        "text": "\\qIt looks like this is shot to pieces,\\q says the podgy grease-covered tinkerer, \\qThis is going to require a complete replace, I'm afraid.\\q",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3305: {
        "resource_type": "desc",
        "id": "3305",
        "name": "Map",
        "text": "This map will automatically update your ship's computer with information about the location and contents of the systems surrounding this one.",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3306: {
        "resource_type": "desc",
        "id": "3306",
        "name": "Map",
        "text": "This map will automatically update your ship's computer with information about the location and contents of the systems surrounding this one.",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3307: {
        "resource_type": "desc",
        "id": "3307",
        "name": "Hellhound Missile Launcher",
        "text": "In recent times the Federation has been trying to come up with something new between the radar missile and the nuclear torpedo.  The end result has been this beauty.  Hellhound missiles scare every ship captain who is unfortunate enough to be anywhere near the business end of this devastating weapon.  This launcher gives you the capability to hurl these hellish thunderbolts at your enemies, something they will never forget.\\n\\nRequires: Missile Weapons {P30\\qLicense\\q \\qLicense, REQUIRES YOU TO REGISTER EV NOVA\\q}{b424 \\q\\nYou stare at this item, and the others around it, for several long, sad moments, knowing that you may never be able to buy any of them ever again.\\q \\q\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3308: {
        "resource_type": "desc",
        "id": "3308",
        "name": "Hellhound Missile",
        "text": "Without a doubt, this is one of the most devastating missiles out there.  Although technically radar-guided, it will burn through most forms of radar jamming, making it nearly impossible to shake, and it lasts just a little too long before detonating.  With an excellent turn rate and a hefty payload, the hellhound missile is an excellent addition to any arsenal.\\n\\nRequires: Missile Weapons {P30\\qLicense\\q \\qLicense, REQUIRES YOU TO REGISTER EV NOVA\\q}{b424 \\q\\nYou stare at this item, and the others around it, for several long, sad moments, knowing that you may never be able to buy any of them ever again.\\q \\q\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3309: {
        "resource_type": "desc",
        "id": "3309",
        "name": "Armor Repair Droids",
        "text": "These little droids, an invention by the redoubtable Dr. Sutherland, repair your armor while you are in flight.  Not very pretty, but extremely effective, these little critters will make you the envy of every trader captain out there...",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3310: {
        "resource_type": "desc",
        "id": "3310",
        "name": "Light Cannon",
        "text": "When they were developing the Lightning Heavy Fighter, Rauther discovered that the traditional Light Blaster just didn't suit the ship's basic load-out.  So they went away and tinkered with the design somewhat, and they came up with a weapon they called the Light Cannon.  It isn't quite as powerful as the Light Blaster, but it fires faster, its shots reach a little further, and it takes up a little less space as well.  Every Lightning to roll off their production line has three of them.  Not all pilots like them, because they are twice as expensive as the ubiquitous Blaster, but most agree they are a somewhat better product...",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3311: {
        "resource_type": "desc",
        "id": "3311",
        "name": "Exotic Ships & Weapons License",
        "text": "The 'Exotic Ships & Weapons License' is the most expensive and the most sought after license, as it gives you access to all of the outfits classified by the Federation Navy as requiring a license.  The small hunched man before you grumpily informs you that his work will fool even the most capable sensor sweep by Federation interceptors{b424 \\q.\\n\\nYou stare at this item, and the others around it, for several long, sad moments, knowing that you may never be able to buy any of them ever again.\\q \\q.\\q}",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3312: {
        "resource_type": "desc",
        "id": "3312",
        "name": "TripHammer",
        "text": "The Auroran Thunderforge is the pinnacle of current Auroran science.  It combines many diverse elements with a distinctive Auroran flavour, and nothing typifies this more than the Triphammer.  Thanks largely to Vell-os intervention, the Triphammer combines Vell-os energy principals with typical Auroran brutish  technology.  The cannon fires a cadmium telluride pellet which vaporizes during its flight.  The particles left in its wake create a conduit for the real action to follow.  The particle trail is a perfect channel to conduct an obscene amount of metaphasic energy, which arcs into the target with predictably devastating results.  The Thunderforge itself was built as a suitable weapons platform for these mighty guns, and would be immeasurably weakened by their removal; they form an integral part of the ship's structure.",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3313: {
        "resource_type": "desc",
        "id": "3313",
        "name": "Transmission Jammer",
        "text": "Heraan scientists quickly utilized technology stolen from the Federation during the Battle of Lesten and created the Transmission Jammer.  It jams the signals being sent out so that reinforcement fleets will not receive notice to make their move.  The military applications of this technology are immense, and especially for those involved in operations deep within enemy territory.",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3314: {
        "resource_type": "desc",
        "id": "3314",
        "name": "IFF Projector - Federation",
        "text": "This outfit, based on technology stolen during the Battle of Lesten, will manipulate your IFF system to project a signal friendly to Federation forces, so that they will treat you as friendly unless directly attacked.",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3315: {
        "resource_type": "desc",
        "id": "3315",
        "name": "IFF Projector - Moash",
        "text": "This outfit, based on technology stolen during the Battle of Lesten, will manipulate your IFF system to project a signal friendly to Moashi forces, so that they will treat you as friendly unless directly attacked.",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    }
}