# *StarCraft 2*

## Quel est l'effet de la *randomization* sur ce jeu ?

### *Items* et *locations*

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

Dans la nomenclature d'Archipelago, il s'agit des *locations* où l'on peut trouver des *items*.
Pour chaque *location*, incluant le fait de terminer une mission, il y a des règles qui définissent les *items* 
nécessaires pour y accéder.
Ces règles ont été conçues en assumant que *StarCraft 2* est joué à la difficulté *Brutal*.
Étant donné que chaque *location* a ses propres règles, il est possible qu'un *item* nécessaire à la progression se 
trouve dans une mission dont vous ne pouvez pas atteindre toutes les *locations* ou que vous ne pouvez pas terminer. 
Cependant, il est toujours nécessaire de terminer une mission pour pouvoir accéder à de nouvelles missions.

Ces catégories, outre la première, peuvent être désactivées dans les options du jeu. 
Par exemple, vous pouvez désactiver le fait d'obtenir des *items*  lorsque des étapes importantes d'une mission sont 
accomplies.

Quand vous recevez un *item*, il devient immédiatement disponible, même pendant une mission, et vous serez avertis via 
la boîte de texte situé dans le coin en haut à droite de *StarCraft 2*.
L'acquisition d'un *item* est aussi indiquée dans le client d'Archipelago.

### *Mission order*

Les missions et l'ordre dans lequel elles doivent être complétées, dénoté *mission order*, peuvent également être 
*randomized*.
Les quatre campagnes de *StarCraft 2* peuvent être utilisées pour remplir le *mission order*.
Notez que les missions d'évolution de *Heart of the Swarm* ne sont pas incluses dans le *randomizer*.
Par défaut, le *mission order* suit la structure des campagnes sélectionnées, mais plusieurs autres options sont 
disponibles, comme *blitz*, *grid*, etc.

Les missions peuvent être lancées par le client *StarCraft 2 Archipelago*, via l'interface graphique de l'onglet 
*StarCraft 2 Launcher*.
Les segments qui se passent sur l'*Hyperion*, un Léviathan et la *Spear of Adun* ne sont pas inclus.
De plus, les points de progression, tels que les crédits ou la Solarite, ne sont pas utilisés dans *StarCraft 2 
Archipelago*.
Les missions accessibles ont leur nom en bleu, tandis que celles où toutes les *locations* ont été collectées 
apparaissent en blanc.
En plaçant votre souris sur une mission, les *locations* non collectées s’affichent, classées par catégorie.
Les missions qui ne sont pas accessibles ont leur nom en gris et leurs prérequis seront également affichés à cet endroit.


## Quel est le but de ce jeu quand il est *randomized*?

Le but est de réussir la mission finale du *mission order* (e.g. *blitz*, *grid*, etc.).
Le fichier de configuration yaml permet de spécifier le *mission order*, quelle combinaison des quatre campagnes de 
*StarCraft 2* peuvent être utilisée et comment les missions sont distribuées dans le *mission order*. 
Étant donné que les deux premières options déterminent le nombre de missions dans un monde de *StarCraft 2*, elles 
peuvent être utilisées pour moduler le temps nécessaire pour terminer le monde. 

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
    * Si la commande est lancée sans option, la liste des *factions* et des couleurs disponibles sera affichée.
* `/option [option_name] [option_value]` Permet de changer un option normalement définit dans le *yaml*. 
    * Si la commande est lancée sans option, la liste des options qui sont modifiables va être affichée.
    * Les options qui peuvent être changées avec cette commande incluent sauter les cinématiques  automatiquement, la 
présence de Kerrigan dans les missions, la disponibilité de la *Spear of Adun*, la quantité de ressources 
supplémentaires données au début des missions, la capacité de contrôler les alliées IA, etc.
* `/disable_mission_check` Désactive les requit pour lancer les missions.
Cette option a pour but de permettre de jouer en mode coopératif en permettant à un joueur de jouer à la prochaine 
mission de la chaîne qu'un autre joueur est en train d'entamer.
* `/set_path [path]` Permet de définir manuellement où *StarCraft 2* est installé ce qui est pertinent seulement si la 
détection automatique de cette dernière échoue.

Notez que le comportement de la commande `/received` a été modifié dans le client *StarCraft 2*.
Dans le client *Common* d'Archipelago, elle renvoie la liste des *items* reçus dans l'ordre inverse de leur réception.
Dans le client de *StarCraft 2*, la liste est divisée par races (i.e., *Any*, *Protoss*, *Terran*, et *Zerg*).
De plus, les améliorations sont regroupées sous leurs unités/bâtiments correspondants.
Un paramètre de filtrage peut aussi être fourni, e.g., `/received Thor`, pour limiter le nombre d'*items* affichés.
Tous les *items* dont le nom, la race ou le nom de groupe contient le paramètre fourni seront affichés.

## Particularités dans un multiworld

### *Collect on goal completion*

L'une des options par défaut des *multiworlds* est qu'une fois qu'un monde a atteint son objectif final, il collecte 
tous ses *items*, incluant ceux dans les autres mondes.
Si vous ne souhaitez pas que cela se produise, vous devez demander à la personne générant le *multiworld* de changer 
l'option *Collect Permission*.
Si la génération n'est pas effectuée via le site web, la personne qui effectue la génération doit modifier l'option 
`collect_mode` dans son fichier *host.yaml* avant la génération.
Si le *multiworld* a déjà été généré, l'hôte peut utiliser la commande `/option collect_mode [valeur]` pour modifier 
cette option.

## Problèmes connus

- *StarCraft 2 Archipelago* ne supporte pas le chargement d'une sauvegarde. 
Pour cette raison, il est recommandé de jouer à un niveau de difficulté inférieur à celui avec lequel vous êtes 
normalement à l'aise.
- *StarCraft 2 Archipelago* ne supporte pas le redémarrage d'une mission depuis le menu de *StarCraft 2*.
Pour redémarrer une mission, utilisez le client de *StarCraft 2 Archipelago*.
- Un rapport d'erreur est souvent généré lorsqu'une mission est fermée. 
Cela n'affecte pas le jeu et peut être ignoré.
- Actuellement, le client de *StarCraft 2* utilise la *location* associée à la victoire d'une mission pour déterminer 
si celle-ci a été complétée.
En conséquence, la fonctionnalité *collect* d'*Archipelago* peut rendre accessible des missions connectées à une 
mission que vous n'avez pas terminée.
