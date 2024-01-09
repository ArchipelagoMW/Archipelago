# Links Awakening DX Multiworld Setup Guide

## Required Software

- [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases). 
- Logiciel capable de charger et de lire les fichiers ROM de la GBC
    - [RetroArch](https://retroarch.com?page=platforms) 1.10.3 ou plus récent.
    - [BizHawk](https://tasvideos.org/BizHawk) 2.8 ou plus récent.
- Votre fichier ROM américain 1.0, probablement nommé `Legend of Zelda, The - Link's Awakening DX (USA, Europe) (SGB Enhanced).gbc`

## Procédures d'installation

1. Téléchargez et installez [Archipelago] (<https://github.com/ArchipelagoMW/Archipelago/releases/latest>). **Le fichier d'installation se trouve dans la section "assets", au bas de la page d'information sur la version**.
2. La première fois que vous faites une génération locale ou que vous patchez votre jeu, il vous sera demandé de localiser votre fichier ROM de base.
   Il s'agit du fichier ROM de Links Awakening DX. Cela ne doit être fait qu'une seule fois.

3. Vous devriez assigner votre émulateur comme programme par défaut pour lancer les fichiers ROM. par défaut.

    1. Extrayez le dossier de votre émulateur sur votre bureau, ou dans un endroit dont vous vous souviendrez.
    2. Faites un clic droit sur un fichier ROM et sélectionnez **Ouvrir avec...**
    3. Cochez la case à côté de **Toujours utiliser cette application pour ouvrir les fichiers .gbc**
    4. Faites défiler la liste jusqu'en bas et cliquez sur le texte gris **Rechercher une autre application sur ce PC**
    5. Recherchez le fichier `.exe` de votre émulateur et cliquez sur **Ouvrir**. Ce fichier devrait se trouver dans le dossier que vous avez extrait à l'étape 1.

## Créer un fichier de configuration (.yaml)

### Qu'est-ce qu'un fichier de configuration et pourquoi en ai-je besoin ?

Votre fichier de configuration contient un ensemble de paramètres de configuration qui fournissent au générateur des informations sur la façon dont il doit générer votre jeu.
Chaque joueur d'un multi-monde fournira son propre fichier de configuration. Cette configuration permet à chaque joueur
de profiter d'une expérience personnalisée selon ses goûts, et les différents joueurs d'un même multi-monde peuvent tous avoir des options différentes.

### Où puis-je obtenir un fichier de configuration ?

La page [Player Settings](/games/Links%20Awakening%20DX/player-settings) du site web vous permet de configurer vos paramètres personnels et d'exporter le fichier.

### Verifying your config file

Vérification du fichier de configuration

Si vous souhaitez valider votre fichier de configuration pour vous assurer qu'il fonctionne, vous pouvez le faire sur la page[YAML Validateur](/check).

## Génération d'un jeu à un seul joueur

1. Accédez à la page [Paramètres du joueur] (/games/Links%20Awakening%20DX/player-settings), configurez vos paramètres, et cliquez sur le bouton "Generate Game".
2. Une page "Seed Info" s'affiche.
3. Cliquez sur le lien "Create New Room".
4. Une page serveur s'affiche, à partir de laquelle vous pouvez télécharger votre fichier patch.
5. Double-cliquez sur votre fichier patch, et Links Awakening DX se lancera automatiquement, et créera votre ROM à partir du fichier patch.
6. Comme il s'agit d'un jeu solo, vous n'aurez plus besoin du client, alors n'hésitez pas à le fermer.

## Rejoindre une partie multi-monde

### Obtenir votre fichier patch et créer votre ROM

Lorsque vous rejoignez une partie multi-monde, il vous sera demandé de fournir votre fichier de configuration à l'hôte. Une fois que c'est fait, l'hôte vous fournira soit un lien pour télécharger votre fichier patch, soit un fichier zip contenant les fichiers patch de tout le monde. Votre fichier patch doit avoir une extension `.apladx`.

Placez votre fichier patch sur votre bureau ou dans un endroit pratique, et double-cliquez dessus. Cela devrait lancer automatiquement le client et créera votre ROM au même endroit que votre fichier patch.

### Se connecter au client

#### RetroArch 1.10.3 ou plus récent

Vous ne devez effectuer ces étapes qu'une seule fois. Note : RetroArch 1.9.x ne fonctionnera pas car il est plus ancien que 1.10.3.

1. Entrez dans le menu principal de RetroArch.
2. Allez dans Réglages --> Interface utilisateur. Mettez "Afficher les réglages avancés" sur Activé.
3. Allez dans Réglages --> Réseau. Réglez "Commandes réseau" sur Activé. (Il se trouve sous Request Device 16.) 
Laissez le port de commande réseau par défaut à 55355.
![Capture d'écran du réglage des commandes réseau](/static/generated/docs/A%20Link%20to%20the%20Past/retroarch-network-commands-en.png)
4. Allez dans le menu principal --> Mise à jour en ligne --> Téléchargement des coeurs. Faites défiler vers le bas et sélectionnez "Nintendo - Gameboy / Color (SameBoy)".

#### BizHawk 2.8 ou plus récent (les versions plus anciennes ne sont pas testées)

1. Chargez la ROM.
2. Naviguez vers le dossier dans lequel Archipelago est installé, puis `data/lua`, et glissez-déposez `connector_ladx_bizhawk.lua` sur la fenêtre principale d'EmuHawk.
    - Vous pouvez aussi ouvrir la console Lua manuellement, cliquer sur `Script` 〉 `Ouvrir Script`, et naviguer vers
      `connector_ladx_bizhawk.lua` avec le sélecteur de fichiers.
3. Garder la console Lua ouverte pendant le jeu (la réduire n'est pas un problème !).

### Connexion au serveur Archipelago

Le fichier patch qui a lancé votre client devrait vous avoir automatiquement connecté au serveur AP. Il y a quelques
raisons pour lesquelles ce n'est pas le cas, notamment si le jeu est hébergé sur le site web mais a été généré ailleurs. Si la fenêtre
client affiche "Statut du serveur : Non connecté", il suffit de demander à l'hôte l'adresse du serveur et de la copier/coller dans le champ de saisie "Serveur".
dans le champ de saisie "Serveur", puis appuyez sur la touche "Entrée".

Le client tentera de se reconnecter à la nouvelle adresse du serveur et affichera momentanément "État du serveur : Connecté".

### Jouer le jeu

Lorsque le client indique que Retroarch et le serveur sont connectés, vous pouvez commencer à jouer. Félicitations pour avoir
avoir réussi à rejoindre une partie multi-monde ! Vous pouvez exécuter diverses commandes dans votre client.
Pour plus d'informations concernant les commandes, vous pouvez utiliser `/help` pour les commandes du client local et `!help` pour les commandes du serveur.