# *Starcraft 2*

## Quel est l'effet de la randomisation sur ce jeu ?

Les éléments qui suivent sont les *items* qui sont randomizés et qui doivent être débloqués pour être utilisé:
1. La capacité de produire des unités, outre les drones/probes/scv.
2. Des améliorations spécifique à certains unités incluant quelques combinaisons qui ne sont pas disponible dans les campagnes génériques, comme le fait d'avoir les deux types d'évolution en même temps pour une unité *Zerg* et toutes les améliorations de la Lance d'Adun simultanément pour les *Protoss*.
3. L'accès aux améliorations génériques des unités, e.g. les améliorations d'attaque et d'armure.
4. D'autres améliorations diverses tel que les améliration de laboratoire et les mercenaires pour les *Terran*, les niveaux et les améliorations de Kerrigan pour les *Zerg*, et les amélirations de la Lance d'Adun pour les *Protoss*.
5. Small boosts to your starting mineral, vespene gas, and supply totals on each mission.

Les *items* sont trouvés en accomplissant du progrès dans les catégories suivantes:
* Completing missions
* Completing bonus objectives (like by gathering lab research material in Wings of Liberty)
* Reaching milestones in the mission, such as completing part of a main objective
* Completing challenges based on achievements in the base game, such as clearing all Zerg on Devil's Playground

Except for mission completion, these categories can be disabled in the game's settings. For instance, you can disable getting items for reaching required milestones.

Quand vous recevez un *item*, il devient imédiatement disponible, même pendant une mission, et vous serez avertis via la boîte de texte situé dans le coin haut-droit de *StarCraft 2*.
L'acquisition d'un *item* est aussi indiqué dans le client d'Archipelago.

Les missions peuvent être lancées par le client *StarCraft 2 Archipelago*, via l'interface graphique de l'onglet *StarCraft 2 Launcher*.
Missions are launched through the Starcraft 2 Archipelago client, through the Starcraft 2 Launcher tab. 
Les segments qui se passe sur l'Hyperrion, le Léviathan et la Lance d'Adun ne sont pas inclus.
De plus, les points de progression tel que les crédits ou la Solarite ne sont pas utilisés dans *StarCraft 2 Archipelago*.

## Quel est le but de ce jeu quand il est randomisé?

Le but est de réussir la mission finale dans le dsa(missison order).
dsa couleur de celle-ci
Les choix fait dans le fichier *yaml* définissent le dsa(mission oder) et comment les missions sont disposés.

## What non-randomized changes are there from vanilla Starcraft 2?

1. Some missions have more vespene geysers available to allow a wider variety of units.
2. Many new units and upgrades have been added as items, coming from co-op, melee, later campaigns, later expansions, brood war, and original ideas.
3. Higher-tech production structures, including Factories, Starports, Robotics Facilities, and Stargates, no longer have tech requirements.
4. Zerg missions have been adjusted to give the player a starting Lair where they would only have Hatcheries.
5. Upgrades with a downside have had the downside removed, such as automated refineries costing more or tech reactors taking longer to build.
6. Unit collision within the vents in Enemy Within has been adjusted to allow larger units to travel through them without getting stuck in odd places.
7. Several vanilla bugs have been fixed.

## Which of my items can be in another player's world?

By default, any of StarCraft 2's items (specified above) can be in another player's world. See the
[Advanced YAML Guide](https://archipelago.gg/tutorial/Archipelago/advanced_settings/en)
for more information on how to change this.

## Unique Local Commands

The following commands are only available when using the Starcraft 2 Client to play with Archipelago. You can list them any time in the client with `/help`.

* `/download_data` Download the most recent release of the necessary files for playing SC2 with Archipelago. Will overwrite existing files
* `/difficulty [difficulty]` Overrides the difficulty set for the world.
    * Options: casual, normal, hard, brutal
* `/game_speed [game_speed]` Overrides the game speed for the world
    * Options: default, slower, slow, normal, fast, faster
* `/color [faction] [color]` Changes your color for one of your playable factions.
    * Faction options: raynor, kerrigan, primal, protoss, nova
    * Color options: white, red, blue, teal, purple, yellow, orange, green, lightpink, violet, lightgrey, darkgreen, brown, lightgreen, darkgrey, pink, rainbow, random, default
* `/option [option_name] [option_value]` Sets an option normally controlled by your yaml after generation.
    * Run without arguments to list all options.
    * Options pertain to automatic cutscene skipping, Kerrigan presence, Spear of Adun presence, starting resource amounts, controlling AI allies, etc.
* `/disable_mission_check` Disables the check to see if a mission is available to play. Meant for co-op runs where one player can play the next mission in a chain the other player is doing.
* `/play [mission_id]` Starts a Starcraft 2 mission based off of the mission_id provided
* `/available` Get what missions are currently available to play
* `/unfinished` Get what missions are currently available to play and have not had all locations checked
* `/set_path [path]` Manually set the SC2 install directory (if the automatic detection fails)
