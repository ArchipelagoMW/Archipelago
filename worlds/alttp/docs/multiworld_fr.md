# Guide d'installation du MultiWorld de A Link to the Past Randomizer

<div id="tutorial-video-container">
    <iframe width="560" height="315" src="https://www.youtube-nocookie.com/embed/mJKEHaiyR_Y" frameborder="0"
      allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen>
    </iframe>
</div>

## Logiciels requis

- [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases)
- [QUsb2Snes](https://github.com/Skarsnik/QUsb2snes/releases) (Inclus dans les utilitaires précédents)
- Une solution logicielle ou matérielle capable de charger et de lancer des fichiers ROM de SNES
    - Un émulateur capable d'éxécuter des scripts Lua
      ([snes9x rr](https://github.com/gocha/snes9x-rr/releases),
      [BizHawk](https://tasvideos.org/BizHawk))
    - Un SD2SNES, [FXPak Pro](https://krikzz.com/store/home/54-fxpak-pro.html), ou une autre solution matérielle
      compatible
- Le fichier ROM de la v1.0 japonaise, sûrement nommé `Zelda no Densetsu - Kamigami no Triforce (Japan).sfc`

## Procédure d'installation

### Installation sur Windows

1. Téléchargez et installez les utilitaires du MultiWorld à l'aide du lien au-dessus, faites attention à bien installer
   la version la plus récente.
   **Le fichier se situe dans la section "assets" en bas des informations de version**. Si vous voulez jouer des parties
   classiques de multiworld, téléchargez `Setup.BerserkerMultiWorld.exe`
    - Si vous voulez jouer à la version alternative avec le mélangeur de portes dans les donjons, vous téléchargez le
      fichier
      `Setup.BerserkerMultiWorld.Doors.exe`.
    - Durant le processus d'installation, il vous sera demandé de localiser votre ROM v1.0 japonaise. Si vous avez déjà
      installé le logiciel auparavant et qu'il s'agit simplement d'une mise à jour, la localisation de la ROM originale
      ne sera pas requise.
    - Il vous sera peut-être également demandé d'installer Microsoft Visual C++. Si vous le possédez déjà (possiblement
      parce qu'un jeu Steam l'a déjà installé), l'installateur ne reproposera pas de l'installer.

2. Si vous utilisez un émulateur, il est recommandé d'assigner votre émulateur capable d'éxécuter des scripts Lua comme
   programme par défaut pour ouvrir vos ROMs.
    1. Extrayez votre dossier d'émulateur sur votre Bureau, ou à un endroit dont vous vous souviendrez.
    2. Faites un clic droit sur un fichier ROM et sélectionnez **Ouvrir avec...**
    3. Cochez la case à côté de **Toujours utiliser cette application pour ouvrir les fichiers .sfc**
    4. Descendez jusqu'en bas de la liste et sélectionnez **Rechercher une autre application sur ce PC**
    5. Naviguez dans les dossiers jusqu'au fichier `.exe` de votre émulateur et choisissez **Ouvrir**. Ce fichier
       devrait se trouver dans le dossier que vous avez extrait à la première étape.

### Installation sur Mac

- Des volontaires sont recherchés pour remplir cette section ! Contactez **Farrak Kilhn** sur Discord si vous voulez
  aider.

## Configurer son fichier YAML

### Qu'est-ce qu'un fichier YAML et pourquoi en ai-je besoin ?

Votre fichier YAML contient un ensemble d'options de configuration qui fournissent au générateur des informations sur
comment il devrait générer votre seed. Chaque joueur d'un multiwolrd devra fournir son propre fichier YAML. Cela permet
à chaque joueur d'apprécier une expérience customisée selon ses goûts, et les différents joueurs d'un même multiworld
peuvent avoir différentes options.

### Où est-ce que j'obtiens un fichier YAML ?

La page [Génération de partie](/games/A%20Link%20to%20the%20Past/player-settings) vous permet de configurer vos
paramètres personnels et de les exporter vers un fichier YAML.

### Configuration avancée du fichier YAML

Une version plus avancée du fichier YAML peut être créée en utilisant la page
des [paramètres de pondération](/weighted-settings), qui vous permet de configurer jusqu'à trois préréglages. Cette page
a de nombreuses options qui sont essentiellement représentées avec des curseurs glissants. Cela vous permet de choisir
quelles sont les chances qu'une certaine option apparaisse par rapport aux autres disponibles dans une même catégorie.

Par exemple, imaginez que le générateur crée un seau étiqueté "Mélange des cartes", et qu'il place un morceau de papier
pour chaque sous-option. Imaginez également que la valeur pour "On" est 20 et la valeur pour "Off" est 40.

Dans cet exemple, il y a soixante morceaux de papier dans le seau : vingt pour "On" et quarante pour "Off". Quand le
générateur décide s'il doit oui ou non activer le mélange des cartes pour votre partie, , il tire aléatoirement un
papier dans le seau. Dans cet exemple, il y a de plus grandes chances d'avoir le mélange de cartes désactivé.

S'il y a une option dont vous ne voulez jamais, mettez simplement sa valeur à zéro. N'oubliez pas qu'il faut que pour
chaque paramètre il faut au moins une option qui soit paramétrée sur un nombre strictement positif.

### Vérifier son fichier YAML

Si vous voulez valider votre fichier YAML pour être sûr qu'il fonctionne, vous pouvez le vérifier sur la page du
[Validateur de YAML](/check).

## Générer une partie pour un joueur

1. Aller sur la page [Génération de partie](/games/A%20Link%20to%20the%20Past/player-settings), configurez vos options,
   et cliquez sur le bouton "Generate Game".
2. Il vous sera alors présenté une page d'informations sur la seed, où vous pourrez télécharger votre patch.
3. Double-cliquez sur le patch et l'émulateur devrait se lancer automatiquement avec la seed. Etant donné que le client
   n'est pas requis pour les parties à un joueur, vous pouvez le fermer ainsi que l'interface Web (WebUI).

## Rejoindre un MultiWorld

### Obtenir son patch et créer sa ROM

Quand vous rejoignez un multiworld, il vous sera demandé de fournir votre fichier YAML à celui qui héberge la partie ou
s'occupe de la génération. Une fois cela fait, l'hôte vous fournira soit un lien pour télécharger votre patch, soit un
fichier `.zip` contenant les patchs de tous les joueurs. Votre patch devrait avoir l'extension `.aplttp`.

Placez votre patch sur votre bureau ou dans un dossier simple d'accès, et double-cliquez dessus. Cela devrait lancer
automatiquement le client, et devrait créer la ROM dans le même dossier que votre patch.

### Se connecter au client

#### Avec un émulateur

Quand le client se lance automatiquement, QUsb2Snes devrait se lancer automatiquement également en arrière-plan. Si
c'est la première fois qu'il démarre, il vous sera peut-être demandé de l'autoriser à communiquer à travers le pare-feu
Windows.

##### snes9x-rr

1. Chargez votre ROM si ce n'est pas déjà fait.
2. Cliquez sur le menu "File" et survolez l'option **Lua Scripting**
3. Cliquez alors sur **New Lua Script Window...**
4. Dans la nouvelle fenêtre, sélectionnez **Browse...**
5. Dirigez vous vers le dossier où vous avez extrait snes9x-rr, allez dans le dossier `lua`, puis
   choisissez `multibridge.lua`
6. Remarquez qu'un nom vous a été assigné, et que l'interface Web affiche "SNES Device: Connected", avec ce même nom
   dans le coin en haut à gauche.

##### BizHawk

1. Assurez vous d'avoir le coeur BSNES chargé. Cela est possible en cliquant sur le menu "Tools" de BizHawk et suivant
   ces options de menu :
   `Config --> Cores --> SNES --> BSNES`  
   Une fois le coeur changé, vous devez redémarrer BizHawk.
2. Chargez votre ROM si ce n'est pas déjà fait.
3. Cliquez sur le menu "Tools" et cliquez sur **Lua Console**
4. Cliquez sur le bouton pour ouvrir un nouveau script Lua.
5. Dirigez vous vers le dossier d'installation des utilitaires du MultiWorld, puis dans les dossiers suivants :  
   `QUsb2Snes/Qusb2Snes/LuaBridge`
6. Sélectionnez `luabridge.lua` et cliquez sur "Open".
7. Remarquez qu'un nom vous a été assigné, et que l'interface Web affiche "SNES Device: Connected", avec ce même nom
   dans le coin en haut à gauche.

#### Avec une solution matérielle

Ce guide suppose que vous avez télchargé le bon micro-logiciel pour votre appareil. Si ce n'est pas déjà le cas, faites
le maintenant. Les utilisateurs de SD2SNES et de FXPak Pro peuvent télécharger le micro-logiciel approprié
[ici](https://github.com/RedGuyyyy/sd2snes/releases). Pour les autres solutions, de l'aide peut être trouvée
[sur cette page](http://usb2snes.com/#supported-platforms).

1. Fermez votre émulateur, qui s'est potentiellement lancé automatiquement.
2. Fermez QUsb2Snes, qui s'est lancé automatiquement avec le client.
3. Lancez la version appropriée de QUsb2Snes (v0.7.16).
4. Lancer votre console et chargez la ROM.
5. Remarquez que l'interface Web affiche "SNES Device: Connected", avec le nom de votre appareil.

### Se connecter au MultiServer

Le patch qui a lancé le client devrait vous avoir connecté automatiquement au MultiServer. Il y a cependant quelques cas
où cela peut ne pas se produire, notamment si le multiworld est hébergé sur ce site, mais a été généré ailleurs. Si
l'interface Web affiche "Server Status: Not Connected", demandez simplement à l'hôte l'adresse du serveur, et
copiez/collez la dans le champ "Server" puis appuyez sur Entrée.

Le client essaiera de vous reconnecter à la nouvelle adresse du serveur, et devrait mentionner "Server Status:
Connected". Si le client ne se connecte pas après quelques instants, il faudra peut-être rafraîchir la page de
l'interface Web.

### Jouer au jeu

Une fois que l'interface Web affiche que la SNES et le serveur sont connectés, vous êtes prêt à jouer. Félicitations
pour avoir rejoint un multiworld !

## Héberger un MultiWorld

La méthode recommandée pour héberger une partie est d'utiliser le service d'hébergement fourni par
[le site](https://berserkermulti.world/generate). Le processus est relativement simple :

1. Récupérez les fichiers YAML des joueurs.
2. Créez une archive zip contenant ces fichiers YAML.
3. Téléversez l'archive zip sur le lien ci-dessus.
4. Attendez un moment que les seed soient générées.
5. Lorsque les seeds sont générées, vous serez redirigé vers une page d'informations "Seed Info".
6. Cliquez sur "Create New Room". Cela vous amènera à la page du serveur. Fournissez le lien de cette page aux autres
   joueurs afin qu'ils puissent récupérer leurs patchs.  
   **Note:** Les patchs fournis sur cette page permettront aux joueurs de se connecteur automatiquement au serveur,
   tandis que ceux de la page "Seed Info" non.
7. Remarquez qu'un lien vers le traqueur du MultiWorld est en haut de la page de la salle. Vous devriez également
   fournir ce lien aux joueurs pour qu'ils puissent suivre la progression de la partie. N'importe quel personne voulant
   observer devrait avoir accès à ce lien.
8. Une fois que tous les joueurs ont rejoint, vous pouvez commencer à jouer.

## Auto-tracking

Si vous voulez utiliser l'auto-tracking, plusieurs logiciels offrent cette possibilité.  
Le logiciel recommandé pour l'auto-tracking actuellement est
[OpenTracker](https://github.com/trippsc2/OpenTracker/releases).

### Installation

1. Téléchargez le fichier d'installation approprié pour votre ordinateur (Les utilisateurs Windows voudront le
   fichier `.msi`).
2. Durant le processus d'installation, il vous sera peut-être demandé d'installer les outils "Microsoft Visual Studio
   Build Tools". Un lien est fourni durant l'installation d'OpenTracker, et celle des outils doit se faire manuellement.

### Activer l'auto-tracking

1. Une fois OpenTracker démarré, cliquez sur le menu "Tracking" en haut de la fenêtre, puis choisissez **
   AutoTracker...**
2. Appuyez sur le bouton **Get Devices**
3. Sélectionnez votre appareil SNES dans la liste déroulante.
4. Si vous voulez tracquer les petites clés ainsi que les objets des donjons, cochez la case **Race Illegal Tracking**
5. Cliquez sur le bouton **Start Autotracking**
6. Fermez la fenêtre "AutoTracker" maintenant, elle n'est plus nécessaire