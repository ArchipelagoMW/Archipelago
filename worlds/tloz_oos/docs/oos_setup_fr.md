# Guide d'installation de The Legend of Zelda : Oracle of Seasons

## Logiciels requis

- [Oracle of Seasons .apworld](https://github.com/Dinopony/ArchipelagoOoS/releases/latest)
- Bizhawk 2.9.1 (x64)](https://tasvideos.org/BizHawk/ReleaseHistory)
- Votre ROM Oracle of Seasons US obtenue légalement

## Instructions d'installation

1. Mettez votre **ROM US d'Oracle of Seasons** dans le dossier où Archipelago est installé (nommée "Legend of Zelda, The - Oracle of Seasons (USA).gbc")
2. Téléchargez le  **fichier .apworld pour Oracle of Seasons** et double-cliquez dessus afin de l'installer dans le répertoire "custom_worlds/" de votre installation Archipelago 
3. Générez une seed en utilisant vos fichiers d'options au format .yaml (voir ci-dessous si vous ne savez pas comment obtenir le fichier modèle)
4. Téléchargez le fichier de patch au format .apoos qui a été généré en même temps que la seed par le serveur. Celui-ci vous permettra de générer votre ROM modifiée.
5. Ouvrez ce fichier avec l'Archipelago Launcher
6. Si tout s'est bien passé, la ROM patchée a été générée dans le même répertoire que le fichier .apoos, et Bizhawk ainsi que le client se sont automatiquement lancés
7. Connectez-vous au serveur Archipelago de votre choix, et vous pouvez commencer à jouer!

## Créer un fichier d'options (.yaml)

Pour obtenir le fichier YAML modèle:
1. Installez le fichier .apworld comme indiqué ci-dessus
2. Si l'Archipelago Launcher était déjà lancé, fermez-le 
3. Lancez l'Archipelago launcher
4. Cliquez sur "Generate Template Settings"
5. Cela devrait ouvrir un répertoire de fichier avec les fichiers modèles, prenez le fichier `The Legend of Zelda - Oracle of Seasons.yaml`

## Gérer les options cosmétiques (sprite, palette...)

Dans le fichier de configuration "host.yaml" qui se trouve dans votre répertoire d'installation d'Archipelago,
vous pouvez régler des options cométiques pour le jeu.
Sous la catégorie "tloz_oos_options", vous trouverez les options suivantes:
- "**character_sprite**", qui sert à changer le sprite de votre personnage
- "**character_palette**", qui sert à changer la couleur de votre personnage
- "**heart_beep_interval**", qui sert à changer l'intervalle de bip du son lorsque vous êtes bas en coeurs

La plupart des ces réglages parlent d'eux-même, sauf les sprites qui méritent quelques informations supplémentaires.
Les sprites sont des fichiers avec l'extension ".bin" extension qui doivent être placés dans le sous-répertoire "data/sprites/oos_ooa/" de votre installation Archipelago.
Vous devez télécharger les fichiers de sprites que vous souhaitez utiliser depuis [ce repository](https://github.com/Dinopony/oracles-sprites/), et les placer ensuite dans le dossier mentionné ci-dessus.
Cela signifie que si vous placez un fichier "goron.bin" dans ce dossier, vous pouvez ensuite mettre "goron" comme valeur pour l'option "character_sprite" dans le fichier host.yaml avant de générer votre ROM.
Une fois cela réglé, toutes les ROMs seront patchées en utilisant ces paramètres cosmétiques.
