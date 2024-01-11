# Guide d'installation d'Archipelago

Ce guide a pour but de fournir une vue d'ensemble de la procédure à suivre pour :
- installer, configurer et exécuter le logiciel Multi-World Archipelago
- Générer et héberger des Multi-World
- Se connecter à un Multi-World une fois que l'hébergement a commencé.

Il s'agit d'une présentation générale. Pour des étapes plus spécifiques, se référer au [guide d'installation](/tutorial) du jeu concerné.

Certaines étapes supposent également l'utilisation de Windows, et peuvent donc varier en fonction de votre système d'exploitation.

## Installation du logiciel Archipelago

La version officielle la plus récente d'Archipelago se trouve sur la page GitHub Releases :
[Archipelago Releases Page] (https://github.com/ArchipelagoMW/Archipelago/releases).

Exécutez le fichier exe, et après avoir accepté la licence d'utilisation, il vous sera demandé quels composants vous souhaitez installer.

Les composant d'Archipelago sont automatiquement installés avec certains programmes. Il s'agit d'un lanceur, d'un générateur, d'un serveur et de quelques clients.

- Le lanceur vous permet d'accéder rapidement aux différents composants et programmes d'Archipelago. Il se trouve sous le nom 
  `ArchipelagoLauncher` et se trouve dans le répertoire principal de votre installation d'Archipelago.

- Le générateur vous permet de générer des jeux Multi-World sur votre ordinateur. Veuillez vous référer à la section "Générer un jeu" de ce guide pour plus d'informations sur la création d'un jeu Multi-World.

- Le serveur vous permet d'héberger le Multi-World sur votre machine. L'hébergement sur votre machine nécessite la redirection du port
sur lequel vous hébergez. Le port par défaut d'Archipelago est `38281`. Si vous n'êtes pas sûr de savoir comment faire, il y a beaucoup d'autres guides sur Internet qui vous aideront.

- Les clients sont utilisés pour connecter votre jeu au Multi-World. Certains jeux utilisent un client qui est installé automatiquement lors de l'installation d'Archipelago. Vous pouvez accéder à ces clients via le lanceur ou en naviguant dans l'interface d'Archipelago.

## Générer un jeu

### Qu'est-ce qu'un YAML ?

YAML est le format de fichier utilisé par Archipelego pour configurer le monde d'un joueur. Il vous permet d'indiquer 
le jeu auquel vous allez jouer ainsi que les paramètres que vous souhaitez pour ce jeu.

YAML est un format très similaire à JSON, mais il est conçu pour être plus lisible par l'homme. Si vous n'êtes pas sûr
de la validité  de votre fichier YAML, vous pouvez le vérifier en le téléchargeant sur la page de vérification du site web
d'Archipelago :
[Page de validation YAML](/check)

### Création d'un YAML

Les fichiers YAML peuvent être générés sur le site web d'Archipelago en visitant la [page des jeux](/games) et en cliquant 
sur le lien "Settings Pages" sous le jeu concerné. En cliquant sur "Export Settings" dans la page des paramètres d'un jeu, 
vous téléchargerez le fichier YAML sur votre système.

Alternativement, vous pouvez lancer `ArchipelagoLauncher.exe` et cliquer sur `Generate Template Settings` pour créer 
un ensemble de modèles YAML pour chaque jeu dans votre installation d'Archipel (y compris pour APWorlds).
Ceux-ci seront placés dans votre dossier `Players/Templates`.

Dans un monde multiple, il doit y avoir un YAML par monde. Un nombre illimité de joueurs peut jouer sur chaque monde 
en utilisant soit le système de coopération. Chaque monde occupera un emplacement dans le MultiWorld et aura un 
nom d'emplacement. Si le jeu concerné l'exige, des fichiers pour l'associer à ce multi-monde.

Si plusieurs personnes prévoient de jouer dans un monde en coopération, elles n'auront besoin que d'un seul YAML
pour leur monde coopératif. Si chaque joueur prévoit de jouer son propre jeu, ils auront chacun besoin d'un YAML.

### Générer un jeu à un seul joueur

#### Sur le site

La façon la plus simple de commencer à jouer à un jeu généré par Archipelago, après avoir suivi la configuration de base 
du guide d'installation du jeu, est de trouver le jeu sur la [Liste des jeux d'Archipelago](/games), de cliquer sur `Page de Paramètres`, 
de régler les paramètres pour la façon dont vous voulez jouer, et de cliquer sur `Générer un jeu` en bas de la page. Cela créera une page 
pour la seed, à partir de laquelle vous pourrez créer une salle, puis vous [connecter] (#connecting-to-an-archipelago-server).

Si vous avez téléchargé les paramètres ou créé un fichier de paramètres manuellement, ce fichier peut être téléchargé 
sur la [page de génération](/generate) où vous pourrez également définir des paramètres spécifiques d'host.

#### Sur votre installation locale

Pour générer un jeu sur votre machine locale, assurez-vous que le logiciel Archipelago est installé. Naviguez jusqu'à votre installation Archipelago
(généralement C:\ProgramData\Archipelago), et placez le fichier de configuration que vous avez créé ou téléchargé depuis le site Web dans le dossier `Players`.

Exécutez `ArchipelagoGenerate.exe`, ou cliquez sur `Generate` dans le lanceur, et il vous indiquera si la génération a réussi ou non.
Si elle a réussi, il y aura un fichier zip dans le dossier `output`. (généralement nommé quelque chose comme `AP_XXXXX.zip`). 
Ce fichier contiendra toutes les informations relatives à la session, y compris le journal des spoilers, s'il a été généré.

Veuillez noter que certains jeux exigent que vous possédiez leurs fichiers ROM pour les générer, car ils sont nécessaires pour générer les fichiers patchs correspondants.
Lorsque vous générez un jeu ROM pour la première fois, il vous sera demandé de localiser son fichier ROM de base.
Cette étape ne doit être effectuée qu'une seule fois.

### Générer un jeu multi-joueur

Archipelago est une architecture multi-jeux et multi-world, si bien que n'importe quel nombre de joueurs et n'importe quel nombre de jeux peuvent être utilisés pour générer un jeu multi-jeux.
Il convient de remarquer que le site web a pour le moment un nombre maximum de joueur de 30. Si vous souhaitez générer une partie
plus grande, cela doit être fait sur une installation locale. En général, il est préférable de générer une partie localement afin de libérer 
les ressources du serveur et ensuite d'héberger le jeu multi-world sur le site web.

#### Rassembler tous les YAML des joueurs

Tous les joueurs qui souhaitent jouer dans le multi-monde généré doivent avoir un fichier YAML qui contient les paramètres avec lesquels ils souhaitent jouer.
Une personne doit rassembler tous les fichiers de tous les participants qui participent au Multi-world généré.
Il est possible qu'un même joueur ait plusieurs jeux, ou même plusieurs parties d'un même jeu, mais chaque YAML doit avoir un nom de joueur unique.

#### Sur le site

Rassemblez tous les fichiers YAML des joueurs en un seul endroit, puis accédez à [Generate Page](/generate). Sélectionnez les paramètres de l'hôte
que vous souhaitez, cliquez sur `Upload File(s)`, et sélectionnez tous les fichiers YAML des joueurs. Le site accepte également les archives `zip` contenant des fichiers YAML.

Après un certain temps, vous serez redirigé vers une page d'information sur les seeds qui affichera la seed générée, l'heure à laquelle elle a été créée, le nombre de joueurs, le spoiler (si un spoiler a été créé) et toutes les salles créées à partir de cette seed.

#### Sur votre installation locale

Il est possible de générer le multi-world localement, en utilisant une installation locale d'Archipelago. Pour ce faire, il faut entrer dans le dossier d'installation de
Archipelago (généralement C:\ProgramData\Archipelago) et en plaçant chaque fichier YAML dans le dossier `Players`.
Si ce dossier n'existe pas, il doit être créé manuellement. Les fichiers ne doivent pas être compressés.

Après avoir rempli le dossier `Players`, exécutez `ArchipelagoGenerate.exe` ou cliquez sur `Generate` dans le lanceur. 
La sortie de la génération est placée dans le dossier `output` (généralement nommé quelque chose comme `AP_XXXXX.zip`).

Veuillez noter que si un joueur de la partie que vous souhaitez générer joue à un jeu qui nécessite un fichier ROM pour être généré, vous aurez besoin des fichiers ROM correspondants.

##### Modification des paramètres de l'hôte local pour la génération

Parfois, il y a plusieurs paramètres que vous pouvez vouloir modifier avant de lancer une seed, comme l'activation du mode race,
la release automatique, le support plando, ou la définition d'un mot de passe.

Tous ces paramètres, ainsi que d'autres options, peuvent être changés en modifiant le fichier `host.yaml` dans le dossier d'installation d'Archipelago
Vous pouvez accéder rapidement à ce fichier en cliquant sur "Open host.yaml" dans le lanceur.
Les paramètres choisis ici sont intégrés dans le fichier `.archipelago` qui est édité avec les autres fichiers après la génération. 
Si vous lancez localement, assurez-vous que ce fichier est édité à votre convenance **avant** de lancer la seed.
Ce fichier est écrasé lors de l'exécution du logiciel d'installation d'Archipelago. 
Si vous avez modifié des paramètres dans ce fichier et que vous souhaitez les conserver, vous pouvez renommer le fichier en `options.yaml`. 

## Hébergement d'un serveur Archipelago 

Lorsqu'une graine Multiworld est générée, les données Multidata seront générées sous la forme d'un `.archipelago`.
Si le jeu a été généré localement,un dossier compressé se trouvera dans `/output` et contiendra le fichier `.archipelago`, 
le spoiler log, et tous les fichiers pertinents pour les jeux générés.


### Hébergement sur le site web

Une fois qu'une page seed a été créée sur le site web, cliquer sur `Create Room` créera une nouvelle instance de serveur, 
et une page qui peut être liée aux autres joueurs, afin qu'ils puissent tous voir les informations de connexion, 
obtenir leurs fichiers de données, et se connecter au multiworld. Cliquez simplement sur l'url dans la barre de titre, 
copiez le lien et envoyez-le à vos amis. La room s'arrêtera après 2 heures d'inactivité, sauvegardant ainsi la progression 
du multiworld et la qualité de ses services. En retournant sur la page de la salle, le serveur de salle relancé et le multiworld 
peut continuer à être joué. Si le lien vers la salle est perdu, le créateur de la salle peut le retrouver sur la [User Content Page](/user-content).
La personne qui a créé la salle devient le "propriétaire" de la salle et, à ce titre, a accès à la console du serveur. 
L'effacement des cookies supprime l'accès à cette console, et il n'y a aucun moyen de le récupérer.
Si un mot de passe de serveur a été défini lors de la création du jeu Multiworld, il est possible d'obtenir les privilèges d'administrateur du serveur 
en entrant `!admin <password>` à partir de `ArchipelagoTextClient.exe`.

#### La page de la salle 

![Capture d'écran de la page de la chambre](/static/generated/docs/Archipelago/example_room.png)
1. Nom du serveur/de l'hôte
2. Port
3. Nom du joueur
4. Lien de téléchargement des fichiers de données
5. Lien vers la page de suivi de ce joueur

#### À partir d'un jeu généré sur le site web 

Après avoir généré un jeu sur le site web, vous serez redirigé vers la page d'accueil. Pour commencer à jouer, cliquez sur `Create Room`.
pour créer une nouvelle salle et un nouveau serveur pour votre jeu.

#### A partir d'un jeu généré localement 

Après avoir généré un jeu, un dossier compressé sera créé dans le dossier `/output`. Allez sur la page [Archipelago Host Game Page](/uploads).
(/uploads), cliquez sur `Upload File`, naviguez jusqu'à votre installation d'Archipelago, et sélectionnez le dossier généré.
Cela créera une nouvelle page de seed en utilisant les informations de ce dossier.

### Hébergement sur une machine locale 

Le fichier `.archipelago` peut être extrait du fichier compressé. Un double-clic sur le fichier ouvrira alors
`ArchipelagoServer.exe` afin d'héberger le Multiworld sur la machine locale. Il est également possible d'exécuter
`ArchipelagoServer.exe` en sélectionnant le fichier `.archipelago`  généré pour commencer l'hébergement.

## Connexion à un serveur d'Archipelago

La méthode de connexion varie en fonction du jeu, il faut donc suivre le guide d'installation de ce jeu,
mais tous les jeux utiliseront les mêmes informations générales de connexion indiquées ici.

### Connection Info

Pour se connecter du jeu sur le serveur, les informations de connexion sont nécessaires pour tous les clients du jeu. 
Les jeux qui utilisent des fichiers de données contiennent généralement les informations de connexion dans ces fichiers, 
lorsqu'ils sont hébergés sur le site web d'Archipelago. Si les informations doivent être saisies manuellement, elles sont
généralement composées de quatre sections différentes.

* `Server`, `Server Name` ou `Host Name` sont tous utilisés indifféremment comme le domaine ou l'adresse IP du serveur.
Si le jeu est hébergé sur le site principal d'Archipel, ce sera `archipelago.gg`. Si le jeu est hébergé sur votre propre machine locale, 
`localhost` fonctionnera. Si le jeu est hébergé sur l'ordinateur d'une autre personne, vous devez entrer l'adresse IP publique de cette personne.
* `Port` est le port du domaine ou de l'adresse IP sur lequel le jeu est hébergé. Sur les pages des Room du site, 
il s'agit de `archipelago.gg:<port>`. La plupart des clients acceptent que cette information soit saisie directement telle quelle.
Si l'information doit être saisie séparément, le port est la séquence de chiffres après le `:`, et le `:` n'a pas besoin d'être saisi.
Si un jeu est hébergé à partir de `ArchipelagoServer.exe`, le port sera par défaut `38281`, mais il peut être modifié dans le fichier `host.exe`. 
* `Slot Name` est le nom du joueur auquel vous vous connectez. C'est le même nom que celui qui a été défini
lors de la création de votre [fichier YAML](#création-dun-yaml).Si le jeu est hébergé sur le site web, ce nom est également affiché sur la
page de la salle.Le nom est sensible à la casse.
* `Password` est le mot de passe défini par l'hôte pour rejoindre le multiworld. Par défaut, ce champ est vide et n'est presque 
jamais requis, mais un mot de passe peut être défini lors de la génération du jeu. En général, laissez ce champ vide lorsqu'il 
existe, à moins que vous ne sachiez qu'un mot de passe a été défini, et ce qu'est ce mot de passe.