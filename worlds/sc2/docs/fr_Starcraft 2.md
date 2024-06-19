# *StarCraft 2*

## Quel est l'effet de la *randomization* sur ce jeu ?

Les éléments qui suivent sont les *items* qui sont *randomized* et qui doivent être débloqués pour être utilisés dans 
le jeu:
1. La capacité de produire des unités, excepté les drones/probes/scv.
2. Des améliorations spécifiques à certaines unités incluant quelques combinaisons qui ne sont pas disponibles dans les 
campagnes génériques, comme le fait d'avoir les deux types d'évolution en même temps pour une unité *Zerg* et toutes 
les améliorations de la *Spear of Adun* simultanément pour les *Protoss*.
3. L'accès aux améliorations génériques des unités, e.g. les améliorations d'attaque et d'armure.
4. D'autres améliorations diverses telles que les améliorations de laboratoire et les mercenaires pour les *Terran*, 
les niveaux et les améliorations de Kerrigan pour les *Zerg*, et les améliorations de la *Spear of Adun* pour les 
*Protoss*.
5. Avoir des *minerals*, du *vespene gas*, et du *supply* au début de chaque mission.

Les *items* sont trouvés en accomplissant du progrès dans les catégories suivantes:
* Terminer des missions
* Réussir des objectifs supplémentaires (e.g., récolter le matériel pour les recherches dans *Wings of Liberty*)
* Atteindre des étapes importantes dans la mission, e.g. réussir des sous-objectifs
* Réussir des défis basés sur les succès du jeu de base, e.g. éliminer tous les *Zerg* dans la mission 
*Devil's Playground*

Ces catégories, outre la première, peuvent être désactivées dans les options du jeu. 
Par exemple, vous pouvez désactiver le fait d'obtenir des *items*  lorsque des étapes importantes d'une mission sont 
accomplies.

Quand vous recevez un *item*, il devient immédiatement disponible, même pendant une mission, et vous serez avertis via 
la boîte de texte situé dans le coin en haut à droite de *StarCraft 2*.
L'acquisition d'un *item* est aussi indiquée dans le client d'Archipelago.

Les missions peuvent être lancées par le client *StarCraft 2 Archipelago*, via l'interface graphique de l'onglet 
*StarCraft 2 Launcher*.
Les segments qui se passent sur l'*Hyperion*, un Léviathan et la *Spear of Adun* ne sont pas inclus.
De plus, les points de progression tels que les crédits ou la Solarite ne sont pas utilisés dans *StarCraft 2 
Archipelago*.

## Quel est le but de ce jeu quand il est *randomized*?

Le but est de réussir la mission finale dans la disposition des missions (e.g. *blitz*, *grid*, etc.).
Les choix faits dans le fichier *yaml* définissent la disposition des missions et comment elles sont mélangées.

## Quelles sont les modifications non aléatoires comparativement à la version de base de *StarCraft 2*

1. Certaines des missions ont plus de *vespene geysers* pour permettre l'utilisation d'une plus grande variété d'unités.
2. Plusieurs unités et améliorations ont été ajoutées sous la forme d*items*.
Ils proviennent de la version *co-op*, *melee*, des autres campagnes, d'expansions ultérieures, de *Brood War*, ou de 
l'imagination des développeurs de *StarCraft 2 Archipelago*.
3. Les structures de production, e.g. *Factory*, *Starport*, *Robotics Facility*, and *Stargate*, n'ont plus 
d'exigences technologiques.
4. Les missions avec la race *Zerg* ont été modifiées pour que les joueurs débuttent avec un *Lair* lorsqu'elles 
commençaient avec une *Hatchery*. 
5. Les désavantages des améliorations ont été enlevés, e.g. *automated refinery* qui coûte plus cher ou les *tech 
reactors* qui prennent plus de temps à construire. 
6. La collision des unités dans les couloirs de la mission *Enemy Within* a été ajustée pour permettre des unités 
plus larges de les traverser sans être coincés dans des endroits étranges. 
7. Plusieurs *bugs* du jeu original ont été corrigés.

## Quels sont les *items* qui peuvent être dans le monde d'un autre joueur? 

Par défaut, tous les *items* de *StarCraft 2 Archipelago* (voir la section précédente) peuvent être dans le monde d'un 
autre joueur.
Consulter [*Advanced YAML Guide*](/tutorial/Archipelago/advanced_settings/en) pour savoir comment 
changer ça.

## Commandes du client qui sont uniques à ce jeu

Les commandes qui suivent sont seulement disponibles uniquement pour le client de *StarCraft 2 Archipelago*.
Vous pouvez les afficher en utilisant la commande `/help` dans le client de *StarCraft 2 Archipelago*.
Toutes ces commandes affectent seulement le client où elles sont utilisées.

* `/download_data` Télécharge les versions les plus récentes des fichiers pour jouer à *StarCraft 2 Archipelago*.
Les fichiers existants vont être écrasés.
* `/difficulty [difficulty]` Remplace la difficulté choisie pour le monde. 
    * Les options sont *casual*, *normal*, *hard*, et *brutal*.
* `/game_speed [game_speed]` Remplace la vitesse du jeu pour le monde.  
    * Les options sont *default*, *slower*, *slow*, *normal*, *fast*, and *faster*.
* `/color [faction] [color]` Remplace la couleur d'une des *factions* qui est jouable. 
    * Les options de *faction*: raynor, kerrigan, primal, protoss, nova.
    * Les options de couleur: *white*, *red*, *blue*, *teal*, *purple*, *yellow*, *orange*, *green*, *lightpink*, 
*violet*, *lightgrey*, *darkgreen*, *brown*, *lightgreen*, *darkgrey*, *pink*, *rainbow*, *random*, *default*.
* `/option [option_name] [option_value]` Permet de changer un option normalement définit dans le *yaml*. 
    * Si la commande est lancée sans option, la liste des options qui sont modifiables va être affichée.
    * Les options qui peuvent être changées avec cette commande incluent sauter les cinématiques  automatiquement, la 
présence de Kerrigan dans les missions, la disponibilité de la *Spear of Adun*, la quantité de ressources 
supplémentaires données au début des missions, la capacité de contrôler les alliées IA, etc.
* `/disable_mission_check` Désactive les requit pour lancer les missions.
Cette option a pour but de permettre de jouer en mode coopératif en permettant à un joueur de jouer à la prochaine 
mission de la chaîne qu'un autre joueur est en train d'entamer.
* `/play [mission_id]` Lance la mission correspondant à l'identifiant donné.
* `/available` Affiche les missions qui sont présentement accessibles.
* `/unfinished` Affiche les missions qui sont présentement accessibles et dont certains des objectifs permettant 
l'accès à un *item* n'ont pas été accomplis.
* `/set_path [path]` Permet de définir manuellement où *StarCraft 2* est installé ce qui est pertinent seulement si la 
détection automatique de cette dernière échoue.
