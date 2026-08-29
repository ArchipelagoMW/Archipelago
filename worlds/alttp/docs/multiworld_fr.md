# Guide d'installation du MultiWorld de A Link to the Past Randomizer

## Logiciels requis

- [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases).
- [SNI](https://github.com/alttpo/sni/releases). Inclus avec l'installation d'Archipelago ci-dessus.
   - SNI n'est pas compatible avec (Q)Usb2Snes.
- Une solution logicielle ou matérielle capable de charger et de lancer des fichiers ROM de SNES
    - Un émulateur capable de se connecter à SNI
      [snes9x-nwa](https://github.com/Skarsnik/snes9x-emunwa/releases), ([snes9x rr](https://github.com/gocha/snes9x-rr/releases),
      [BSNES-plus](https://github.com/black-sliver/bsnes-plus),
      [BizHawk](https://tasvideos.org/BizHawk), ou
      [RetroArch](https://retroarch.com?page=platforms) 1.10.1 ou plus récent). Ou,
    - Un SD2SNES, [FXPak Pro](https://krikzz.com/store/home/54-fxpak-pro.html), ou une autre solution matérielle compatible. **À noter:
    les SNES minis ne sont pas encore supportés par SNI. Certains utilisateurs rapportent avoir du succès avec QUsb2Snes pour ce système,
    mais ce n'est pas supporté.**
- Le fichier ROM de la v1.0 japonaise, habituellement nommé `Zelda no Densetsu - Kamigami no Triforce (Japan).sfc`

## Procédure d'installation

1. Téléchargez et installez [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases). **L'installateur se situe dans la section "assets" en bas des informations de version**.
   
2. Si c'est la première fois que vous faites une génération locale ou un patch, il vous sera demandé votre fichier ROM de base. Il s'agit de votre fichier ROM Link to the Past japonais. Cet étape n'a besoin d'être faite qu'une seule fois.

3. Si vous utilisez un émulateur, il est recommandé d'assigner votre émulateur capable d'éxécuter des scripts Lua comme
   programme par défaut pour ouvrir vos ROMs.
    1. Extrayez votre dossier d'émulateur sur votre Bureau, ou à un endroit dont vous vous souviendrez.
    2. Faites un clic droit sur un fichier ROM et sélectionnez **Ouvrir avec...**
    3. Cochez la case à côté de **Toujours utiliser cette application pour ouvrir les fichiers .sfc**
    4. Descendez jusqu'en bas de la liste et sélectionnez **Rechercher une autre application sur ce PC**
    5. Naviguez dans les dossiers jusqu'au fichier `.exe` de votre émulateur et choisissez **Ouvrir**. Ce fichier
       devrait se trouver dans le dossier que vous avez extrait à la première étape.

### Obtenir son patch et créer sa ROM

Quand vous rejoignez un multiworld, il vous sera demandé de fournir votre fichier YAML à celui qui héberge la partie ou
s'occupe de la génération. Une fois cela fait, l'hôte vous fournira soit un lien pour télécharger votre patch, soit un
fichier `.zip` contenant les patchs de tous les joueurs. Votre patch devrait avoir l'extension `.aplttp`.

Placez votre patch sur votre bureau ou dans un dossier simple d'accès, et double-cliquez dessus. Cela devrait lancer
automatiquement le client, et devrait créer la ROM dans le même dossier que votre patch.

### Se connecter au client

#### Avec un émulateur

Quand le client se lance automatiquement, SNI devrait se lancer automatiquement également en arrière-plan. Si
c'est la première fois qu'il démarre, il vous sera peut-être demandé de l'autoriser à communiquer à travers le pare-feu
Windows.

#### snes9x-nwa

1. Cliquez sur 'Network Menu' et cochez **Enable Emu Network Control**
2. Chargez votre ROM si ce n'est pas déjà fait.

##### snes9x-rr

1. Chargez votre ROM si ce n'est pas déjà fait.
2. Cliquez sur le menu "File" et survolez l'option **Lua Scripting**
3. Cliquez alors sur **New Lua Script Window...**
4. Dans la nouvelle fenêtre, sélectionnez **Browse...**
5. Sélectionnez le fichier lua connecteur inclus avec votre client
    - Recherchez `/SNI/lua/` dans votre fichier Archipelago. 
6. Si vous avez une erreur en chargeant le script indiquant `socket.dll missing` ou similaire, naviguez vers le fichier du
lua que vous utilisez dans votre explorateur de fichiers et copiez le `socket.dll` à la base de votre installation snes9x.

#### BSNES-Plus

1. Chargez votre ROM si ce n'est pas déjà fait.
2. L'émulateur devrait automatiquement se connecter lorsque SNI se lancera.

##### BizHawk

1. Assurez vous d'avoir le cœur BSNES chargé. Cela est possible en cliquant sur le menu "Tools" de BizHawk et suivant
   ces options de menu :
    - (≤ 2.8) `Config` 〉 `Cores` 〉 `SNES` 〉 `BSNES`
    - (≥ 2.9) `Config` 〉 `Preferred Cores` 〉 `SNES` 〉 `BSNESv115+`  
   Une fois le cœur changé, rechargez le avec Ctrl+R (par défaut).
2. Chargez votre ROM si ce n'est pas déjà fait.
3. Glissez et déposez le fichier `Connector.lua` que vous avez téléchargé ci-dessus sur la fenêtre principale EmuHawk.
    - Recherchez `/SNI/lua/` dans votre fichier Archipelago. 
    - Vous pouvez aussi ouvrir la console Lua manuellement, cliquez sur `Script` 〉 `Open Script`, et naviguez sur `Connecteur.lua`
      avec le sélecteur de fichiers.

##### RetroArch 1.10.1 ou plus récent

Vous n'avez qu'à faire ces étapes qu'une fois.

1. Entrez dans le menu principal RetroArch
2. Allez dans Réglages --> Interface utilisateur. Mettez "Afficher les réglages avancés" sur ON.
3. Allez dans Réglages --> Réseau. Mettez "Commandes Réseau" sur ON. (trouvé sous Request Device 16.) Laissez le 
   Port des commandes réseau à 555355. \
   ![Screenshot of Network Commands setting](../../generic/docs/retroarch-network-commands-fr.png)
4. Allez dans Menu Principal --> Mise à jour en ligne --> Téléchargement de cœurs. Descendez jusqu'a"Nintendo - SNES / SFC (bsnes-mercury Performance)" et 
   sélectionnez le.

Quand vous chargez une ROM, veillez a sélectionner un cœur **bsnes-mercury**. Ce sont les seuls cœurs qui autorisent les outils externs à lire les données d'une ROM.

#### Avec une solution matérielle

Ce guide suppose que vous avez télchargé le bon micro-logiciel pour votre appareil. Si ce n'est pas déjà le cas, faites
le maintenant. Les utilisateurs de SD2SNES et de FXPak Pro peuvent télécharger le micro-logiciel approprié
[ici](https://github.com/RedGuyyyy/sd2snes/releases). Pour les autres solutions, de l'aide peut être trouvée
[sur cette page](http://usb2snes.com/#supported-platforms).

1. Fermez votre émulateur, qui s'est potentiellement lancé automatiquement.
2. Lancez votre console et chargez la ROM.

### Se connecter au MultiServer

Le patch qui a lancé le client devrait vous avoir connecté automatiquement au MultiServer. Il y a cependant quelques cas
où cela peut ne pas se produire, notamment si le multiworld est hébergé sur ce site, mais a été généré ailleurs. Si
l'interface Web affiche "Server Status: Not Connected", demandez simplement à l'hôte l'adresse du serveur, et
copiez/collez la dans le champ "Server" puis appuyez sur Entrée.

Le client essaiera de vous reconnecter à la nouvelle adresse du serveur, et devrait mentionner "Server Status:
Connected". Si le client ne se connecte pas après quelques instants, il faudra peut-être rafraîchir la page de
l'interface Web.

### Jouer au jeu

Une fois que l'interface Web affiche que la SNES et le serveur sont connectés, vous êtes prêt à jouer. Félicitations,
vous venez de rejoindre un multiworld ! Vous pouvez exécuter différentes commandes dans votre client. Pour plus d'informations
sur ces commandes, vous pouvez utiliser `/help` pour les commandes locales et `!help` pour les commandes serveur.
