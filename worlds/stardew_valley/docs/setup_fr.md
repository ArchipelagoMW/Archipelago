# Guide d'installation de Stardew Valley Randomizer

## Logiciels requis

- Stardew Valley sur PC (Recommandée: [Version Steam](https://store.steampowered.com/app/413150/Stardew_Valley/))
- SMAPI ([Chargeur de mods pour Stardew Valley](https://smapi.io/))
- [Version 5.x.x du mod StardewArchipelago](https://github.com/agilbert1412/StardewArchipelago/releases)
    - Il est important d'utiliser une version 5.x.x du mod pour jouer à des "seeds" qui y ont été générées. Les versions les plus récentes ne peuvent être utilisées qu'avec les versions les plus récentes du générateur de monde, qui ne sont pas encore supportées par archiepalgo.gg.

## Logiciels facultatifs
- Archipelago via la [page des versions Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases)
    - (Uniquement pour le textclient)
- Autres mods de Stardew Valley depuis [Nexus Mods](https://www.nexusmods.com/stardewvalley)
    - Il y a des [mods supportés](https://github.com/agilbert1412/StardewArchipelago/blob/5.x.x/Documentation/Supported%20Mods.md) que vous pouvez ajouter à votre dossier YAML pour les inclure avec la randomisation de Archipelago.

    - Il n'est cependant **pas** recommandé d'ajouter des mods non supportés, même s'il est possible de le faire. Les intéractions entre les mods peuvent être imprévisibles, et aucune assistance ne sera proposée si des problèmes surviennent.
    - Plus vous avez de mods non supportés, et plus ils sont lourds, plus vous avez de chance de causer des problèmes.

## Configurer votre dossier YAML

### Qu'est-ce qu'un dossier YAML et pourquoi il m'en faut un ?

Voir le guide pour configurer un YAML basique: [Guide basique de configuration d'un MultiWrold](/tutorial/Archipelago/setup/en)

### Où puis-je obtenir un dossier YAML ?

Vous pouvez customiser vos paramètres en visitant la [page de paramètres de joueur de Stardew Valley](/games/Stardew%20Valley/player-settings)

## Rejoindre une partie Multimondes

### Installation du mod

- Installez [SMAPI](https://smapi.io/) en suivant les instructions sur leur site internet.
- Téléchargez et extrayez le mod [StardewArchipelago](https://github.com/agilbert1412/StardewArchipelago/releases) dans votre dossier "Mods" de Stardew Valley.
- *FACULTATIF*: Si vous voulez lancer votre jeu depuis Steam, ajoutez ce qui suit dans vos options de lancement de Stardew Valley:
    - "[PATH TO STARDEW VALLEY]\Stardew Valley\StardewModdingAPI.exe" %command%
- Sinon, lancez simplement "StardewModdingAPI.exe" directement dans votre dossier d'installation.
- Stardew Valley devrait se lancer seul à côté d'une console qui vous permet de lire les informations de mods et d'intéragir avec certains d'entre eux.

### Se connecter au MultiServer

Lancez Stardew Valley avec SMAPI. Une fois que vous êtes sur l'écran d'accueil de Stardew Valley, créez une nouvelle ferme.

Sur la page de création d'un nouveau personnage, vous verrez trois nouveaux champs, utilisés pour lier votre nouveau personnage au multiworld d'Archipelago.

![image](https://i.imgur.com/b8KZy2F.png)

Vous pouvez customiser votre ferme et votre personnage autant que vous le souhaitez.

Le champ "Server" doit contenir l'adresse et le port, et le champ "Slot" doit contenir le nom que vous avez spécifié dans votre yaml.

`archipelago.gg:38281`

`StardewPlayer`

Le mot de passe est facultatif.

Votre partie se connectera automatiquement à Archipelago, et se reconnectera automatiquement en chargeant la partie, plus tard.

Vous n'aurez jamais besoin d'entrer ces informations de nouveau pour ce personnage, à moins que vous ne changiez l'adresse ip ou le port de la salle/page.
Si l'adresse ip ou le port de la salle/page change, vous pouvez suivre les instructions suivantes pour modifier les informations de connection de votre partie.
- Lancez la version modifiée de Stardew Valley
- En étant **sur le menu principal** du jeu, entrez la commande suivante **dans la console SMAPI**:
- `connect_override ip:port slot password`
- Exemple: `connect_override archipelago.gg:38281 StardewPlayer`
- Sauvegardez la partie. Les nouvelles informations de connexion seront utilisées, à la place des anciennes.
- Jouer un jour complet, dormez, et sauvegardez le jeu. Ces informations de connexions remplaceront les anciennes et deviendront permanentes.

### Intéragir avec le MultiWorld depuis le jeu

Lorsque vous vous connectez, vous devriez voir un message dans le clavardage vous informant de la commande `!!help`. Cette comande listera d'autres commandes de chat exclusives à Stardew Valley, que vous pouvez utiliser.

En outre, vous pouvez utiliser le chat du jeu pour communiquer à d'autres joueurs du MultiWorld, à condition qu'ils jouent à un jeu ayant la fontion "chat".

Enfin, vous pouvez également utiliser la commande `!help` depuis le chat du jeu, vous permettant de demander des indices sur certains objets, ou des endroits encore non trouvés.

Il est important de noter que le chat de Stardew Valley est assez limité dans ses capacités. Par exemple, il ne permet pas de remonter l'historique, et ainsi de voir ce qui est sorti de l'affichage. La console SMAPI, qui tourne en même temps que votre jeu aura le même historique, entier, et sera sans doute une meilleure option pour lire les ancien messages. 
Pour une meilleure expérience de chat, vous pouvez aussi utiliser le Client de Texte Archipelago (Archipelago Text Client) officiel; il ne vous permettra cependant pas de taper des commanddes exclusives à Stardew Valley.

### Jouer avec des mods supportés

Voir la [documentation des mods supportés](https://github.com/agilbert1412/StardewArchipelago/blob/5.x.x/Documentation/Supported%20Mods.md)

### Multijoueur

Le mode multijoueur de Stardew Valley n'est pas compatible avec Archipelago pour le moment. Il n'y aucun projet pour supporter cette fonctionnalité.
