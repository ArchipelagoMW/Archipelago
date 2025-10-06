# The Wind Waker

## Où est la page d'options ?

La [page d'option pour ce jeu](../player-options) contient toutes les options que vous avez besoin de configurer et 
exporter afin d'obtenir un fichier de configuration.

## Que fait la randomisation à ce jeu ?

Les objets sont mélangés entre les différentes localisations du jeu, donc chaque expérience est unique. 
Les localisations randomisés incluent les coffres, les objets reçu des PNJ, ainsi que les trésors submergés sous l'eau.
Le randomiseur inclue également des qualités de vie tel qu'un monde entièrement ouvert, 
des cinématiques retirées ainsi qu'une vitesse de navigation améliorée, et plus.

## Quelles localisations sont mélangés ?

Seulement les localisations mises en logiques dans les paramètres du monde seront randomisés.
Les localisations restantes dans le jeu auront un rubis jaune.
Celles-ci incluant un message indiquant que la localisation n'est pas randomisé.

## Quel est l'objectif de The Wind Waker ?

Atteindre et battre Ganondorf en haut de la tour de Ganon. 
Pour cela, vous aurez besoin des huit morceaux de la Triforce du Courage, l'Excalibur entièrerement ranimée (sauf si ce
sont des épées optionnelles ou en mode sans épée), les flèches de lumières, ainsi que tous les objets nécessaires pour
atteindre Ganondorf.

## A quoi ressemble un objet venant d'un autre monde dans TWW ?

Les objets appartenant aux autres mondes qui ne sont pas TWW sont représentés 
par la Lettre de Père (la lettre que Médolie vous donne pour la donner à Komali),
un objet inutilisé dans le randomiseur.

## Que se passe-t-il quand un joueur reçoit un objet ?

Quand le joueur reçoit n'importe quel objet, il sera automatiquement ajouté à l'inventaire de Link.
Link **ne tiendra pas** l'objet au dessus de sa tête comme dans d'autres randomizer de Zelda.

## J'ai besoin d'aide ! Que dois-je faire ?

Référez vous à la [FAQ](https://lagolunatic.github.io/wwrando/faq/) premièrement. Ensuite, 
essayez les étapes de résolutions de problèmes dans le [guide de mise en place](/tutorial/The%20Wind%20Waker/setup/en).
Si vous êtes encore bloqué, s'il vous plait poser votre question dans le salon textuel Wind Waker 
dans le serveur discord d'Archipelago.

## J'ai ouvert mon jeu dans Dolphin, mais je n'ai aucun de mes items de démarrage !

Vous devez vous connecter à la salle du multiworld pour recevoir vos objets. Cela inclut votre inventaire de départ.

## Problèmes Connus

- Les rubis randomisés freestanding, butins, et appâts seront aussi données au joueur qui récupère l'objet.
  L'objet sera bien envoyé mais le joueur qui le collecte recevra une copie supplémentaire.
- Les objets que tiens Link au dessus de sa tête **ne sont pas** randomisés, 
  comme les rubis allant des trésors venant des cercles lumineux
  jusqu'aux récompenses venant des mini-jeux, ne fonctionneront pas.
- Un objet qui reçoit des messages pour des objets progressifs reçu à des localisations
  qui s'envoient plus tôt que prévu seront incorrect. Cela n'affecte pas le gameplay.
- Le compteur de quart de cœur dans les messages lorsqu'on reçoit un objet seront faux d'un.
  Cela n'affecte pas le gameplay.
- Il a été signalé que l'itemlink peut être buggé. 
  Ça ne casse en rien le jeu, mais soyez en conscient.

N'hésitez pas à signaler n'importe quel autre problème ou suggestion d'amélioration dans le salon textuel Wind Waker
dans le serveur discord d'Archipelago !

## Astuces et conseils

### Où sont les secrets de donjons trouvés à trouver dans les donjons ?

[Ce document](https://docs.google.com/document/d/1LrjGr6W9970XEA-pzl8OhwnqMqTbQaxCX--M-kdsLos/edit?usp=sharing)
contient des images montrant les différents secrets des donjons.

### Que font exactement les options obscures et de précisions des options de difficultés ?

Les options `logic_obscurity` et `logic_precision` modifient la logique du randomizer
pour mettre différentes astuces et techniques en logique.
[Ce document](https://docs.google.com/spreadsheets/d/14ToE1SvNr9yRRqU4GK2qxIsuDUs9Edegik3wUbLtzH8/edit?usp=sharing)
liste parfaitement les changements qui sont fait. Les options sont progressives donc par exemple,
la difficulté obscure dur inclue les astuces normales et durs. 
Certains changements ont besoin de la combinaison des deux options.
Par exemple, pour mettre les canons qui détruisent la porte de la Forteresse Maudite pour vous en logique,
les paramètres obscure et précision doivent tout les deux être mis au moins à normal.

### Quels sont les différents préréglages d'options ?

Quelques préréglages (presets) sont disponibles sur la [page d'options](../player-options) pour votre confort.

- **Tournoi Saison 8**: Ce sont (aussi proche que possible) les paramètres utilisés dans le [Tournoi
  Saison 8](https://docs.google.com/document/d/1b8F5DL3P5fgsQC_URiwhpMfqTpsGh2M-KmtTdXVigh4) du serveur WWR Racing.
  Ce préréglage contient 4 boss requis (avec le Roi Cuirassé garanti d'être requis),
  entrée des donjons randomisées, difficulté obscure dur, et une variété de checks dans l'overworld,
  même si la liste d'options progressive peut sembler intimidante.
  Ce préréglage exclut également plusieurs localisations et vous fait commencez avec plusieurs objets.
- **Miniblins 2025**: Ce sont (aussi proche que possible) les paramètres utilisés dans la
  [Saison 2025 de Miniblins](https://docs.google.com/document/d/19vT68eU6PepD2BD2ZjR9ikElfqs8pXfqQucZ-TcscV8)
  du serveur WWR Racing. Ce préréglage est bien si vous êtes nouveau à The Wind Waker ! 
  Il n'y a pas beaucoup de localisation dans ce monde, et tu as seulement besoin de compléter deux donjons.
  Tu commences aussi avec plusieurs objets utiles comme la double magie, 
  une amélioration de capacité pour votre arc et vos bombes ainsi que six coeurs.
- **Mixed Pools**: Ce sont (aussi proche que possible) les paramètres utilisés dans le
  [Tournoi Mixed Pools Co-op](https://docs.google.com/document/d/1YGPTtEgP978TIi0PUAD792OtZbE2jBQpI8XCAy63qpg) 
  du serveur WWR Racing. 
  Ce préréglage contient toutes les entrées randomisés et inclue la plupart des localisations
  derrière une entrée randomisé. Il y a aussi plusieurs locations de l'overworld,
  étant donnée que ces paramètres sont censés être joué dans une équipe de deux joueurs.
  Ce préréglage a aussi six boss requis, mais vu que les pools d'entrées sont randomisés, 
  les boss peuvent être trouvés n'importe où ! Regarder votre carte de l'océan pour
  déterminer quels îles les boss sont.

## Fonctionnalités planifiées

- Type des coffres Dynamique assorties au contenu en fonction des options activés
- Implémentation des indices venant du randomiseur de base (options de placement des indices et des types d'indices)
- Intégration avec le système d'indice d'Archipelago (ex: indices des enchères)
- Support de l'EnergyLink
- Logique de la voile rapide en tant qu'option
- Continuer la correction de bug

## Crédits

Ce randomiseur ne pouvait pas être possible sans l'aide de :

- BigSharkZ: (Dessinateur de l'îcone)
- Celeste (Maëlle): (correction de logique et de fautes d'orthographe, programmation additionnelle)
- Chavu: (document sur les difficultés de logique)
- CrainWWR: (multiworld et assitance sur la mémoire de Dolphin, programmation additionnelle)
- Cyb3R: (référence pour `TWWClient`)
- DeamonHunter: (programmation additionnelle)
- Dev5ter: (Implémentation initiale de l'AP de TWW)
- Gamma / SageOfMirrors: (programmation additionnelle)
- LagoLunatic: (randomiseur de base, assistance additionelle)
- Lunix: (Support Linux, programmation additionnelle)
- mobby45 (Traduction du guide français)
- Mysteryem: (Support du tracker, programmation additionnelle)
- Necrofitz: (documentation additionelle)
- Ouro: (Support du tracker)
- tal (matzahTalSoup): (guide pour les dungeon secrets)
- Tubamann: (programmation additionnelle)

Le logo archipelago © 2022 par Krista Corkos et Christopher Wilson, sous licence
[CC BY-NC 4.0](http://creativecommons.org/licenses/by-nc/4.0/).
