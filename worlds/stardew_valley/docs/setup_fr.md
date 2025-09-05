# Guide de configuration du Randomizer Stardew Valley

## Logiciels nécessaires

- Stardew Valley 1.6 sur PC (Recommandé: [Steam](https://store.steampowered.com/app/413150/Stardew_Valley/))
- SMAPI ([Mod loader pour Stardew Valley](https://www.nexusmods.com/stardewvalley/mods/2400?tab=files))
- [StardewArchipelago Version 6.x.x](https://github.com/agilbert1412/StardewArchipelago/releases)
  - Il est important d'utiliser une release en 6.x.x pour jouer sur des seeds générées ici. Les versions ultérieures peuvent uniquement être utilisées pour des release ultérieures du générateur de mondes, qui ne sont pas encore hébergées sur archipelago.gg

## Logiciels optionnels

- Launcher Archipelago à partir de la [page des versions d'Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases)
  - (Uniquement pour le client textuel)
- Autres [mods supportés](https://github.com/agilbert1412/StardewArchipelago/blob/6.x.x/Documentation/Supported%20Mods.md) que vous pouvez ajouter au yaml pour les inclure dans la randomization d'Archipelago

  - Il n'est **pas** recommandé de modder Stardew Valley avec des mods non supportés, même s'il est possible de le faire.
    Les interactions entre mods peuvent être imprévisibles, et aucune aide ne sera fournie pour les bugs qui y sont liés.
  - Plus vous avez de mods non supportés, et plus ils sont gros, plus vous avez de chances de casser des choses.

## Configuration du fichier YAML

### Qu'est qu'un fichier YAML et pourquoi en ai-je besoin ?

Voir le guide pour paramètrer un fichier YAML dans le guide de configuration d'Archipelago (en anglais): [Guide de configuration d'un MultiWorld basique](/tutorial/Archipelago/setup/en)

### Où puis-je récupèrer un fichier YAML

Vous pouvez personnaliser vos options en visitant la [Page d'options de joueur pour Stardew Valley](/games/Stardew%20Valley/player-options)

## Rejoindre une partie en MultiWorld

### Installation du mod

- Installer [SMAPI](https://www.nexusmods.com/stardewvalley/mods/2400?tab=files) en suivant les instructions sur la page du mod.
- Télécharger et extraire le mod [StardewArchipelago](https://github.com/agilbert1412/StardewArchipelago/releases) dans le dossier "Mods" de Stardew Valley.
- *Optionnel*: Si vous voulez lancer le jeu depuis Steam, ajouter l'option de lancement suivante à Stardew Valley : `"[PATH TO STARDEW VALLEY]\Stardew Valley\StardewModdingAPI.exe" %command%`
- Sinon, exécutez juste "StardewModdingAPI.exe" dans le dossier d'installation de Stardew Valley.
- Stardew Valley devrait se lancer avec une console qui liste les informations des mods installés, et intéragit avec certains d'entre eux.

### Se connecter au MultiServer

Lancer Stardew Valley avec SMAPI. Une fois que vous avez atteint l'écran titre du jeu, créez une nouvelle ferme.

Dans la fenêtre de création de personnage, vous verrez 3 nouveaux champs, qui permettent de relier votre personnage à un MultiWorld Archipelago.

![image](https://i.imgur.com/b8KZy2F.png)

Vous pouvez personnaliser votre personnage comme vous le souhaitez.

Le champ "Server" nécessite l'adresse **et** le port, et le "Slotname" est le nom que vous avez spécifié dans votre YAML.

`archipelago.gg:12345`

`StardewPlayer`

Le mot de passe est optionnel.

Votre jeu se connectera automatiquement à Archipelago, et se reconnectera automatiquement également quand vous chargerez votre sauvegarde, plus tard.

Vous n'aurez plus besoin d'entrer ces informations à nouveau pour ce personnage, à moins que votre session ne change d'ip ou de port.
Si l'ip ou le port de la session **change**, vous pouvez suivre ces instructions pour modifier les informations de connexion liées à votre sauvegarde :

- Lancer Stardew Valley moddé
- Dans le **menu principal** du jeu, entrer la commande suivante **dans la console de SMAPI** :
- `connect_override ip:port slot password`
- Par exemple : `connect_override archipelago.gg:54321 StardewPlayer`
- Chargez votre partie. Les nouvelles informations de connexion seront utilisées à la place de celles enregistrées initialement.
- Jouez une journée, dormez et sauvegarder la partie. Les nouvelles informations de connexion iront écraser les précédentes, et deviendront permanentes.

### Intéragir avec le MultiWorld depuis le jeu

Quand vous vous connectez, vous devriez voir un message dans le chat vous informant de l'existence de la commande `!!help`. Cette commande liste les autres commandes exclusives à Stardew Valley que vous pouvez utiliser.

De plus, vous pouvez utiliser le chat en jeu pour parler aux autres joueurs du MultiWorld, pour peu qu'ils aient un jeu qui supporte le chat.

Enfin, vous pouvez également utiliser les commandes Archipelago (`!help` pour les lister) depuis le chat du jeu, permettant de demander des indices (via la commande `!hint`) sur certains objets.

Il est important de préciser que le chat de Stardew Valley est assez limité. Par exemple, il ne permet pas de remonter l'historique de conversation. La console SMAPI qui tourne à côté aura quant à elle l'historique complet et sera plus pratique pour consulter des messages moins récents.
Pour une meilleure expérience avec le chat, vous pouvez aussi utiliser le client textuel d'Archipelago, bien qu'il ne permettra pas de lancer les commandes exclusives à Stardew Valley.

### Jouer avec des mods supportés

Voir la [documentation des mods supportés](https://github.com/agilbert1412/StardewArchipelago/blob/6.x.x/Documentation/Supported%20Mods.md) (en Anglais).

### Multijoueur

Vous ne pouvez pas jouer à Stardew Valley en mode multijoueur pour le moment. Il n'y a aucun plan d'action pour ajouter cette fonctionalité à court terme.