# The Minish Cap

## Où se trouve la page des options ?
 
Il s'agit actuellement d'un monde personnalisé, il n'y a donc pas encore de page d'options. Pour
créer vos options, vous devrez télécharger l'un des fichiers YAML de démarrage sur la page des versions GitHub. Vous pouvez également créer le fichier YAML par défaut en suivant le guide Archipelago `&template` :

Comment générer un modèle YAML :  Pour les apworld vérifié, votre dossier \Players\Templates contient déjà des modèles YAML par défaut. Pour les apworlds personnalisés, installez d'abord l'apworld en double-cliquant dessus, puis ouvrez ArchipelagoLauncher.exe pour lancer le Launcher, et cliquez sur Generate Template Options pour créer des modèles YAML pour tous les apworlds de votre dossier \custom_worlds ainsi que de votre dossier \lib\worlds.  Après avoir cliqué sur ce bouton, une fenêtre de l'Explorateur de fichiers s'ouvrira (sous Windows) pointant directement vers votre dossier \Players\Templates, avec tous les nouveaux fichiers de modèles. Utilisez-les pour créer des options de joueur pour tous les mondes apworlds que vous avez installés, qu'ils soient vérifié ou personnalisés.

## Quel est l'effet de la randomisation sur ce jeu ?

Ce randomiseur ne gère que la randomisation des objets. Les objets d'inventaire, les objets de quête, les éléments, les morceaux de cœur et les conteneurs,
les Parchemins et les Rubis peuvent tous être randomisés.

Les kinstones et les fusions ne sont pas *encore* incluses. Le jeu agira comme si toutes les fusions avaient déjà eu lieu et aucune kinstone ne dropera de l'herbe ou des ennemis.

## Quels sont les items et les emplacements aléatoires ?

Emplacements:
- Big/Small Chests
- Heart Pieces/Containers
- Shops
- Dojo Items
- Dig Spots
- Rupees

Items:
- All inventory items
- Quest Items
- Heart Pieces/Containers
- Dungeon Keys, Maps & Compasses
- Elements
- Scrolls
- Rupees
- Refills (hearts, bombs & arrows)

## Quels sont les autres changements apportés au jeu ?

Le jeu a été modifié pour ouvrir le monde beaucoup plus que dans le jeu vanille. Vous commencerez avec Ezlo et toutes les scènes d'ouverture ainsi que de nombreux autres événements de l'histoire seront passés.
Hyrule Town a également été modifiée pour rendre presque tous les endroits accessibles à tout moment.

Il y a également une petite poignée de changements de qualité de vie qui ont été apportés pour plus de commodité. Voici quelques-unes des plus importantes :
- La possibilité de faire un quickwarp dans le menu de sauvegarde (sauvegarder, quitter et charger en une seule option).
- Affichage de la quantité de clés petit/grand donjon, de la boussole et de la carte en survolant la région d'un donjon particulier sur la carte du monde.
- enregistrement de diverses statistiques, telles que la date d'acquisition d'objets spécifiques, à afficher dans les crédits.
- L'attribution progressive de plusieurs objets.
- Et bien sûr, supprimer autant de dialogues d'Ezlo que possible. Sérieusement, qui a pensé qu'un chapeau parlant était une bonne idée ?

  
## À quoi ressemblent les objets d'un autre monde dans The Minish Cap ?

Les objets provenant d'autres mondes que le vôtre s'afficheront sous la forme d'une icône d'horloge, mais il s'agit d'un sprite temporaire jusqu'à ce qu'un sprite d'objet ap
soit créé. Les types d'objets suivants apparaîtront dans des couleurs différentes :
- Progression: Vert
- Useful: Bleu
- Normal/Filler : Rouge
- Trap: Une apparence aléatoire de Vert/Bleu/Rouge

## Lorsque le joueur reçoit un objet, que se passe-t-il ?

La plupart des objets déclencheront la courte scène « Obtenir l'objet » dans laquelle Link brandit l'objet. D'autres, comme les bouteilles, les roupies, les objets de donjon ne déclencheront pas la scène.
Ils seront simplement placés directement dans votre menu d'inventaire,
visible sur l'un des trois écrans de pause.

## Puis-je jouer hors ligne ?

Oui, le client et le connector ne sont nécessaires que pour envoyer et recevoir des objets.
Si vous jouez en solo, vous n'avez pas besoin de jouer en ligne, sauf si vous voulez bénéficier du reste des fonctionnalités d'Archipelago (comme les hint et l'auto-tracking).
Si vous jouez à un jeu multi-monde, le client synchronisera votre jeu avec le serveur la prochaine fois que vous vous connecterez.
