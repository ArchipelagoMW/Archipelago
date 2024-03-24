# Guide de configuration pour Pokémon Rouge et Bleu : Archipelago

## Important

Comme nous utilisons BizHawk, ce guide s'applique uniquement aux systèmes Windows et Linux.

## Logiciel requis

- BizHawk : [Version BizHawk de TASVideos](https://tasvideos.org/BizHawk/ReleaseHistory)
   - Les versions 2.3.1 et ultérieures sont prises en charge. La version 2.9.1 est recommandée.
   - Des instructions d'installation détaillées pour BizHawk peuvent être trouvées sur le lien ci-dessus.
   - Les utilisateurs Windows doivent d'abord exécuter le programme d'installation des prérequis, qui peut également être trouvé sur le lien ci-dessus.
- Le client Archipelago intégré, qui peut être installé [ici](https://github.com/ArchipelagoMW/Archipelago/releases)
   (sélectionnez `Pokemon Client` lors de l'installation).
- Fichiers ROM Pokémon Rouge et/ou Bleu. La communauté Archipelago ne peut pas les fournir.

## Logiciel en option

-[Pokémon Red and Blue Archipelago Map Tracker](https://github.com/j-imbo/pkmnrb_jim/releases/latest), à utiliser avec [PopTracker](https://github.com/black-sliver/PopTracker/releases)


## Configuration de BizHawk

Une fois BizHawk installé, ouvrez EmuHawk et modifiez les paramètres suivants :

- (≤ 2,8) Allez dans Config > Personnaliser. Passez à l'onglet Avancé, puis faites passer le Lua Core de "NLua+KopiLua" à "Lua+LuaInterface". 
Ensuite redémarrez EmuHawk. Ceci est nécessaire pour que le script Lua fonctionne correctement.
   **REMARQUE : Même si « Lua+LuaInterface » est déjà sélectionné, basculez entre les deux options et resélectionnez-la. Nouvelles installations**
   **des versions plus récentes d'EmuHawk ont tendance à afficher "Lua+LuaInterface" comme option sélectionnée par défaut mais se chargent toujours**
   ** "NLua+KopiLua" jusqu'à ce que cette étape soit terminée.**
- Sous Config > Personnaliser > Avancé, assurez-vous que la case AutoSaveRAM est cochée et cliquez sur le bouton 5s.
   Cela réduit la possibilité de perdre des données de sauvegarde en cas de panne de l'émulateur.
- Sous Config > Personnaliser, cochez la case "Exécuter en arrière-plan". Cela empêchera la déconnexion du client pendant EmuHawk s'exécute en arrière-plan.

Il est fortement recommandé d'associer des extensions de rom GB (\*.gb) à l'EmuHawk que nous venons d'installer.
Pour ce faire, nous devons simplement rechercher n'importe quelle rom Gameboy que nous possédons, faire un clic droit et sélectionner "Ouvrir avec...", déplier
la liste qui apparaît et sélectionnez l'option du bas "Rechercher une autre application", puis accédez au dossier BizHawk et sélectionnez EmuHawk.exe.

## Configurer votre fichier YAML

### Qu'est-ce qu'un fichier YAML et pourquoi en ai-je besoin ?

Votre fichier YAML contient un ensemble d'options de configuration qui fournissent au générateur des informations sur la manière dont il doit
générer votre jeu. Chaque joueur d'un multimonde fournira son propre fichier YAML. Cette configuration permet à chaque joueur de profiter
une expérience personnalisée à leur goût, et les différents joueurs du même multimonde peuvent tous avoir des options différentes.

### Où puis-je obtenir un fichier YAML ?

Vous pouvez générer un yaml ou télécharger un modèle en visitant la [Page des paramètres du joueur Pokémon Rouge et Bleu](/games/Pokemon%20Red%20and%20Blue/player-settings)

Il est important de noter que l'option `game_version` détermine le fichier ROM qui sera corrigé.
Le joueur et la personne qui génère (s'ils génèrent localement) auront besoin du fichier ROM correspondant.

Pour `trainer_name` et `rival_name`, les caractères réguliers suivants sont autorisés :

* `‘’“”·… ABCDEFGHIJKLMNOPQRSTUVWXYZ():;[]abcdefghijklmnopqrstuvwxyzé'-?!.♂$×/,♀0123456789`

Et les caractères spéciaux suivants (ceux-ci occupent chacun un caractère) :
* `<'d>`
* `<'l>`
* `<'t>`
* `<'v>`
* `<'r>`
* `<'m>`
* `<PK>`
* `<MN>`
* `<MALE>` alias pour `♂`
* `<FEMALE>` alias pour `♀`

## Rejoindre un jeu multimonde

### Obtenez votre fichier de patch Pokémon

Lorsque vous rejoignez un jeu multimonde, il vous sera demandé de fournir votre fichier YAML à celui qui l'héberge. Une fois cela fait,
l'hébergeur vous fournira soit un lien pour télécharger votre fichier de données, soit un fichier zip contenant les données de chacun
des dossiers. Votre fichier de données doit avoir une extension « .apred » ou « .apblue ».

Double-cliquez sur votre fichier de correctif pour démarrer votre client et démarrer le processus de correctif ROM. Une fois le processus terminé
(cela peut prendre un certain temps), le client et l'émulateur seront automatiquement démarrés (si vous avez associé l'extension à l'émulateur comme recommandé).

### Connectez-vous au multiserveur

Une fois le client et l'émulateur démarrés, vous devez les connecter. Accédez à votre dossier d'installation Archipelago,
puis vers `data/lua`, et faites glisser et déposez le script `connector_pkmn_rb.lua` sur la fenêtre principale d'EmuHawk. (Vous pourriez plutôt
ouvrez la console Lua manuellement, cliquez sur `Script` 〉 `Open Script` et accédez à `connector_pkmn_rb.lua` avec le fichier
cueilleur.)

Pour connecter le client au multiserveur, mettez simplement `<adresse>:<port>` dans le champ de texte en haut et appuyez sur Entrée (si le
le serveur utilise un mot de passe, tapez dans le champ de texte inférieur `/connect <adresse>:<port> [mot de passe]`)

Vous êtes maintenant prêt à commencer votre aventure à Kanto.

## Suivi automatique

Pokémon Rouge et Bleu dispose d'un tracker de carte entièrement fonctionnel qui prend en charge le suivi automatique.

1. Téléchargez [Pokémon Red and Blue Archipelago Map Tracker](https://github.com/j-imbo/pkmnrb_jim/releases/latest) et [PopTracker](https://github.com/black-sliver/PopTracker/releases).
2. Ouvrez PopTracker et chargez le pack Pokémon Rouge et Bleu.
3. Cliquez sur le symbole « AP » en haut.
4. Entrez l'adresse AP, le nom de l'emplacement et le mot de passe.

Le reste devrait se faire tout seul ! Les éléments et les ckecks seront marqués automatiquement et il connaît même vos paramètres. Il masquera les ckecks et ajustera la logique en conséquence.