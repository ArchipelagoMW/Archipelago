# Guide de configuration du randomiseur Minecraft

## Logiciel requis

- Minecraft Java Edition à partir de
   la [page de la boutique Minecraft Java Edition](https://www.minecraft.net/en-us/store/minecraft-java-edition)
- Archipelago depuis la [page des versions d'Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases)
     - (sélectionnez `Minecraft Client` lors de l'installation.)

## Configuration de votre fichier YAML

### Qu'est-ce qu'un fichier YAML et pourquoi en ai-je besoin ?

Voir le guide sur la configuration d'un YAML de base lors de la configuration d'Archipelago
guide : [Guide de configuration de base de Multiworld](/tutorial/Archipelago/setup/en)

### Où puis-je obtenir un fichier YAML ?

Vous pouvez personnaliser vos paramètres Minecraft en allant sur la [page des paramètres de joueur](/games/Minecraft/player-options)

## Rejoindre une partie MultiWorld

### Obtenez votre fichier de données Minecraft

**Un seul fichier yaml doit être soumis par monde minecraft, quel que soit le nombre de joueurs qui y jouent.**

Lorsque vous rejoignez un jeu multimonde, il vous sera demandé de fournir votre fichier YAML à l'hébergeur. Une fois cela fait,
l'hébergeur vous fournira soit un lien pour télécharger votre fichier de données, soit un fichier zip contenant les données de chacun
des dossiers. Votre fichier de données doit avoir une extension `.apmc`.

Double-cliquez sur votre fichier `.apmc` pour que le client Minecraft lance automatiquement le serveur forge installé. Assurez-vous de
laissez cette fenêtre ouverte car il s'agit de votre console serveur.

### Connectez-vous au multiserveur

Ouvrez Minecraft, accédez à "Multijoueur> Connexion directe" et rejoignez l'adresse du serveur "localhost".

Si vous utilisez le site Web pour héberger le jeu, il devrait se connecter automatiquement au serveur AP sans avoir besoin de `/connect`

sinon, une fois que vous êtes dans le jeu, tapez `/connect <AP-Address> (Port) (Password)` où `<AP-Address>` est l'adresse du
Serveur Archipelago. `(Port)` n'est requis que si le serveur Archipelago n'utilise pas le port par défaut 38281. Notez qu'il n'y a pas de deux-points entre `<AP-Address>` et `(Port)` mais un espace.
`(Mot de passe)` n'est requis que si le serveur Archipelago que vous utilisez a un mot de passe défini.

### Jouer le jeu

Lorsque la console vous indique que vous avez rejoint la salle, vous êtes prêt. Félicitations pour avoir rejoint avec succès un
jeu multimonde ! À ce stade, tous les joueurs minecraft supplémentaires peuvent se connecter à votre serveur forge. Pour commencer le jeu une fois
que tout le monde est prêt utilisez la commande `/start`.

## Installation non Windows

Le client Minecraft installera forge et le mod pour d'autres systèmes d'exploitation, mais Java doit être fourni par l'
utilisateur. Rendez-vous sur [minecraft_versions.json sur le MC AP GitHub](https://raw.githubusercontent.com/KonoTyran/Minecraft_AP_Randomizer/master/versions/minecraft_versions.json)
pour voir quelle version de Java est requise. Les nouvelles installations utiliseront par défaut la version "release" la plus élevée.
- Installez le JDK Amazon Corretto correspondant
     - voir les [Liens d'installation manuelle du logiciel](#manual-installation-software-links)
     - ou gestionnaire de paquets fourni par votre OS/distribution
- Ouvrez votre `host.yaml` et ajoutez le chemin vers votre Java sous la clé `minecraft_options`
     - ` java : "chemin/vers/java-xx-amazon-corretto/bin/java"`
- Exécutez le client Minecraft et sélectionnez votre fichier .apmc

## Installation manuelle complète

Il est fortement recommandé d'utiliser le programme d'installation d'Archipelago pour gérer l'installation du serveur forge pour vous.
Le support ne sera pas fourni pour ceux qui souhaitent installer manuellement forge. Pour ceux d'entre vous qui savent comment faire et qui souhaitent le faire,
les liens suivants sont les versions des logiciels que nous utilisons.

### Liens d'installation manuelle du logiciel

- [Page de téléchargement de Minecraft Forge] (https://files.minecraftforge.net/net/minecraftforge/forge/)
- [Page des versions du mod Minecraft Archipelago Randomizer] (https://github.com/KonoTyran/Minecraft_AP_Randomizer/releases)
     - **NE PAS INSTALLER CECI SUR VOTRE CLIENT**
- [Amazon Corretto](https://docs.aws.amazon.com/corretto/)
     - choisissez la version correspondante et sélectionnez "Téléchargements" sur la gauche
