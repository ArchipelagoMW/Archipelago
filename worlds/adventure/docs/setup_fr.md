# Guide d'installation pour Aventure : Archipelago

## Important

Comme nous utilisons Bizhawk, ce guide ne s'applique qu'aux systèmes Windows et Linux.

## Logiciel requis

- Bizhawk : [Bizhawk sort de TASVideos](https://tasvideos.org/BizHawk/ReleaseHistory)
   - Les versions 2.3.1 et ultérieures sont prises en charge. La version 2.7 est recommandée pour la stabilité.
   - Des instructions d'installation détaillées pour Bizhawk peuvent être trouvées sur le lien ci-dessus.
   - Les utilisateurs Windows doivent d'abord exécuter le programme d'installation prereq, qui peut également être trouvé sur le lien ci-dessus.
- Le client Archipelago intégré, qui peut être installé [ici](https://github.com/ArchipelagoMW/Archipelago/releases)
   (sélectionnez `Adventure Client` lors de l'installation).
- Un fichier ROM Adventure NTSC. La communauté Archipelago ne peut pas les fournir.

## Configuration de Bizhawk

Une fois Bizhawk installé, ouvrez Bizhawk et modifiez les paramètres suivants :

- Allez dans Config > Personnaliser. Basculez vers l'onglet Avancé, puis basculez le Lua Core de "NLua+KopiLua" vers
   "Interface Lua+Lua". Redémarrez ensuite Bizhawk. Ceci est nécessaire pour que le script Lua fonctionne correctement.
   **REMARQUE : Même si "Lua+LuaInterface" est déjà sélectionné, basculez entre les deux options et resélectionnez-le. Nouvelles installations**
   **des versions plus récentes de Bizhawk ont tendance à afficher "Lua+LuaInterface" comme option sélectionnée par défaut mais se chargent toujours**
   **"NLua+KopiLua" jusqu'à ce que cette étape soit terminée.**
- Sous Config > Personnaliser, cochez la case "Exécuter en arrière-plan". Cela empêchera la déconnexion du client pendant
BizHawk s'exécute en arrière-plan.

- Il est recommandé de fournir un chemin vers BizHawk dans votre host.yaml pour Adventure afin que le client puisse le démarrer automatiquement
- En même temps, vous pouvez définir une option pour charger automatiquement le script connector_adventure.lua lors du lancement de BizHawk
d'AdventureClient.
Exemple d'installation Windows par défaut :
```rom_args: "--lua=C:/ProgramData/Archipelago/data/lua/connector_adventure.lua"```

## Configuration de votre fichier YAML

### Qu'est-ce qu'un fichier YAML et pourquoi en ai-je besoin ?

Votre fichier YAML contient un ensemble d'options de configuration qui fournissent au générateur des informations sur la façon dont il doit
générer votre jeu. Chaque joueur d'un multimonde fournira son propre fichier YAML. Cette configuration permet à chaque joueur de profiter
une expérience personnalisée à leur goût, et différents joueurs dans le même multimonde peuvent tous avoir des options différentes.

### Où puis-je obtenir un fichier YAML ?

Vous pouvez générer un yaml ou télécharger un modèle en visitant la [page des paramètres d'aventure](/games/Adventure/player-settings)

### Quels sont les paramètres recommandés pour s'initier à la rando ?
Régler la difficulty_switch_a et réduire la vitesse des dragons rend les dragons plus faciles à éviter. Ajouter Calice à
local_items garantit que vous visiterez au moins un des châteaux intéressants, car il ne peut être placé que dans un château ou
la salle des crédits.

## Rejoindre une partie MultiWorld

### Obtenez votre fichier de correctif Adventure

Lorsque vous rejoignez un jeu multimonde, il vous sera demandé de fournir votre fichier YAML à l'hébergeur. Une fois cela fait,
l'hébergeur vous fournira soit un lien pour télécharger votre fichier de données, soit un fichier zip contenant les données de chacun
des dossiers. Votre fichier de données doit avoir une extension `.apadvn`.

Faites glisser votre fichier de correctif vers AdventureClient.exe pour démarrer votre client et démarrer le processus de correctif ROM. Une fois le processus
est terminé (cela peut prendre un certain temps), le client et l'émulateur seront démarrés automatiquement (si vous configurez l'émulateur
chemin recommandé).

### Connectez-vous au multiserveur

Une fois le client et l'émulateur démarrés, vous devez les connecter. Dans l'émulateur, cliquez sur "Outils"
menu et sélectionnez "Console Lua". Cliquez sur le bouton du dossier ou appuyez sur Ctrl+O pour ouvrir un script Lua.

Accédez à votre dossier d'installation Archipelago et ouvrez `data/lua/connector_adventure.lua`, si ce n'est pas le cas
configuré pour le faire automatiquement.

Pour connecter le client au multiserveur, mettez simplement `<adresse>:<port>` dans le champ de texte en haut et appuyez sur Entrée (si le
le serveur utilise un mot de passe, saisissez dans le champ de texte inférieur `/connect <adresse> :<port> [mot de passe]`)

Appuyez sur Réinitialiser et commencez à jouer