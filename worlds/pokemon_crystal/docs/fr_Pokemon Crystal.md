# Pokémon Cristal

## Que fait la randomization dans ce jeu ?

Quelques changements ont été faits au jeu de base pour ce randomizer :

- Le combat de dresseurs sur la Route 30 se termine dès la fin de la visite chez M. Pokémon, évitant de revenir
  voir le Professeur Orme
- Le directeur est toujours dans l'entrepôt du souterrain, même quand la Tour Radio n'est pas occuppée
- La porte dans le sous-sol du Centre Commercial de Doublonville s'ouvre avec la Carte Magnétique dans le Sac
- Les checks basés sur le temps, tels que la Fratrie des Sept et l'homme du toit du Manoir Céladon sont toujours
  disponibles
    - Les objets cachés sous Vanessa (Frieda) et Homer (Wesley) ont été bougés d'une case sur le côté pour rester
      accessibles
- Le Bateau entre Oliville et Carmin sur Mer est toujours présent dans des parties non-Johto-seulement,
  même avant d'accéder au Panthéon, et peut être monté à bord avec le Passe Bateau
- Ondine est toujours dans l'Arène d'Azuria
- Un rebord sur la Route 45 a été bougé pour que tous les objets et dresseurs puissent être accédés en 2 passages
- Pour les options qui le permettent, les badges de Kanto correspondent aux CS suivantes :
    - CS01 Coupe - Badge Cascade
    - CS02 Vol - Badge Foudre
    - CS03 Surf - Badge Âme
    - CS04 Force - Badge Prisme
    - CS05 Flash - Badge Roche
    - CS06 Siphon - Badge Volcan
    - CS07 Cascade - Badge Terre
- La CT02 et la CT08 seront toujours respectivement Coup d'Boule et Éclate-Roc, et sont toujours réutilisables
- Les évolutions par échange ont été changées pour les rendre possible dans une partie solo :
    - Les évolutions par échange normales se font maintenant au niveau 37
    - Les évolutions par échange et objet tenu se font quand leur objet d'évolution est utilisé sur le Pokémon, comme
      avec une pierre d'évolution
- Évoli évolue en Mentali et Noctali respectivement avec la Pierre Soleil et la Pierre Lune
- Les évolutions par bonheur sont logiquement liées à l'accès au Souterrain de Doublonville ou Bourg Palette.
  Le cadet des frères coiffeurs et Nina maximiseront le bonheur d'un Pokémon et sont toujours disponibles
- Zarbi n'apparaît à l'état sauvage qu'après avoir résolu un puzzle des Ruines d'Alpha. Avant ça, toute rencontre
  qui aurait été contre un Zarbi jouera son cri à la place
- Le RDC de la Tour Ferraille est accessible une fois que le Glas Transparent est acquis.
- Les étages supérieurs de la Tour Ferraille sont accessibles une fois que la condition ci-dessus est satisfaite,
  et que l'Arcenci'Aile est acquise. Les deux objets sont dans le Multiworld.
- Eusine donnera une Lettre Évoli en lui parlant au RDC de la Tour Ferraille après avoir vu Suicune
  à tous ses emplacements dans le monde, qui sont visitables dans n'importe quel ordre.
- Aux Ruines d'Alpha, la chambre à objets de Ho-Oh est accessible en possédant l'Arcenci'Aile
- L'événement de Celebi peut être activé en donnant la GS Ball à Fargas après avoir terminé le Puits Ramoloss
  et avoir battu le rival à Écorcia
- L'événement qui donne habituellement la GS Ball dans le Centre Pokémon de Doublonville s'active après
  être devenu Maître
- L'homme qui donne une récompense pour avoir tous les badges à Carmin sur Mer ne vérifie que les 8 badges de Kanto
- Une boutique a été ajoutée au premier étage de chaque Centre Pokémon. Il est possible de personnaliser
  ce que cette boutique vend avec l'option `build_a_mart`, mais elle vendra toujours des Poké Balls
  et des Cordes Sortie
- Un PNJ permettant de combattre des Pokémon sauvages aléatoires a été ajouté au premier étage de chaque Centre
  Pokémon, ce combat donne de l'argent et de l'exp, mais ne donne pas d'entrées du Pokédex, et le Pokémon n'est
  pas capturable

## Quels objets et emplacements se font randomizer ?

Par défaut, les objets situés par terre et les objets donnés par les PNJ sont randomizés.
Les badges peuvent être vanilla, mélangés entre eux ou randomizés. Le Pokématos et ses coupons peuvent être
vanilla ou randomizés.
Si le mode Johto Seulement est activé, les objets de Kanto ne seront pas randomizés et Kanto sera inaccessible.
Le Passe Bateau donné par Orme après avoir vaincu le Conseil 4 sera aussi remplacé par l'Aile Argentée.

Il y a des options pour ajouter plus d'objets dans le pool d'objets :

- Randomizer les Objets Cachés : Ajoute les objets cachés au pool
- Randomizer les Arbres à Baie : Ajoute les objets des arbres à baie au pool
- Trainersanity : Ajoute une récompense pour avoir vaincu des dresseurs au pool
- Dexsanity : L'entrée Pokédex d'un Pokémon peut détenir un check, et est liée à des Pokémon spécifiques.
- Dexcountsanity : Un certain nombre d'entrées Pokédex détiennent des checks.
  Ce n'est pas lié à des Pokémon spécifiques mais à un total.
- Shopsanity : Inclut les objets des boutiques dans le pool
- Grasssanity : Couper chaque tuile d'herbe est un check
- Concours de Capture d'Insecte : Ajoute les récompenses du concours de capture d'insecte au pool
- Randomizer les Requêtes de Pokémon : Ajoute les récompenses du grand-père de Léo et du Magicarpe au Lac Colère
  au pool
- Randomizer les Appels Téléphoniques : Ajoute les objets des appels de dresseurs au pool

## Quels autres changements ont été faits au jeu ?

De nombreux changements de qualité de vie ont été implémentés :

- Une nouvelle vitesse de texte, Instantanée, a été ajoutée au menu d'options du jeu.
- Les boutons A et/ou B peuvent être utilisés comme boutons turbo dans les dialogues
- L'option des Animations de Combat est plus granulaire. Le choix le plus rapide, *Speedy*, enlève quasiment toutes
  les animations
- B peut être maintenu pour courir. Une option de course automatique existe. Si elle est activée, B empêchera de
  courir.
- De nombreuses autres options ont été ajoutées pour drastiquement accélérer le gameplay, y compris : Les cannes
  à pêches peuvent toujours fonctionner, les Pokémon non-capturés peuvent avoir plus de chances d'apparaître, les
  dresseurs peuvent être aveugles, etc.
- Le lag dans les menus a été enlevé
- La Bicyclette peut être utilisée en intérieur
- La Corde Sortie peut être utilisée dans plus d'intérieurs, comme les Arènes
- Si un repousse se dissippe et qu'il en reste dans le Sac, le jeu donne le choix d'en utiliser un autre
- Les taux de croissance des Pokémon sont normalisés (Moyen-Rapide pour les Pokémon non-Légendaires, Lent pour les
  Pokémon Légendaires)
- Le système de mot de passe pour l'horloge a été enlevé, et l'horloge peut être réinitialisée en faisant
  Bas + Select + B sur l'écran titre
- Une option a été ajoutée au jeu pour ne pas requérir d'apprendre de Capacités à effet hors-combat.
  Pour garder Vol, Flash, et d'autres capacités accessibles, un menu additionnel est disponible
  en appuyant sur Select dans le Menu Start.
- Tous les événements statiques peuvent réapparaître en parlant à la personne du Bloc Temporel au premier étage
  de n'importe quel Centre Pokémon
- Il est possible de se téléporter à la ville de départ en séléctionnant "*Go Home*" dans le menu principal
  avant de charger la partie

## À quoi ressemble un objet d'un autre monde dans Pokémon Cristal ?

Les objets d'autres mondes indiqueront les noms de l'objet et du joueur destinataire une fois collectés. À cause de
limitations avec le texte du jeu, ces noms sont tronqués à 16 caractères, et les caractères spéciaux non
présents dans la police du jeu sont replacés par des points d'interrogation.

## Quand le joueur reçoit un objet, que se passe-t-il ?

Un son jouera quand un objet est reçu si l'option *Item Receive Sound* (Son de Réception d'Objet) est activée.
Des sons différents joueront pour distinguer les objets de progression et les pièges.

## Puis-je jouer hors-ligne ?

Oui, ce jeu n'a pas besoin d'être connecté au client pour des graines solo. Une connexion est uniquement requise
pour envoyer et recevoir des objets. Ceci ne s'applique pas lorsque l'option `remote_items` est active.
