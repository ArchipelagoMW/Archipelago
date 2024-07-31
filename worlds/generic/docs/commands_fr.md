# Commandes utiles

Les commandes sont divisées en deux types : les commandes client et les commandes serveur. Les commandes client sont des commandes qui sont exécutées par le client et qui n'affectent pas la session à distance de l'Archipelago.
Les commandes serveur sont des commandes exécutées par le serveur de l'Archipelago  et qui affectent la session distante de l'Archipelago .

Dans les clients qui ont leurs propres commandes, celles-ci sont généralement précédées d'une barre oblique : `/`. 

Les commandes du serveur sont toujours envoyées au serveur avec un point d'exclamation : `!`. <br/>

# Commandes du serveur

Les commandes du serveur peuvent être exécutées par n'importe quel client qui permet d'envoyer des messages textuels au serveur de l'Archipelago. Si votre client
client ne permet pas d'envoyer du chat, vous pouvez vous connecter à votre fenêtre de jeu avec le TextClient qui est fourni avec l'installation d'Archipelago.
Pour exécuter la commande, il suffit d'envoyer un message texte avec la commande,
including the exclamation point.

### Général
- `!help` Renvoie une liste des commandes disponibles.
- `!license` Renvoie les informations relatives à la licence du logiciel.
- `!options` Renvoie les options actuelles du serveur, y compris le mot de passe en clair.
- `!players` Renvoie des informations sur les joueurs connectés et non connectés.
- `!status` Renvoie des informations sur l'état de la connexion et le nombre de vérifications effectuées pour tous les joueurs de la salle en cours. <br /> ( En option, mentionnez un nom de joueur et obtenez des informations sur ce joueurs. Par exemple : !status DeathLink)


### Utilitaires
- `!countdown <nombre de secondes>` Démarre un compte à rebours en utilisant la valeur de secondes donnée. Utile pour synchroniser les démarrages.
  Le compte à rebours durera 10 secondes si vous tapez simplement `!countdown` sans argument.
- `!alias <alias>` Définit votre alias, ce qui vous permet d'utiliser des commandes avec l'alias plutôt qu'avec le nom que vous avez fourni.
- `!admin <commande>` Exécute une commande comme si vous l'aviez tapée dans la console du serveur. L'administration à distance doit être activée.

### Informations
- `!remaining` Liste les objets restants dans votre jeu, mais pas l'endroit où ils se trouvent ni leur destinataire.
- `!missing` Liste les emplacements qui vous manquent du point de vue du serveur.
- `!checked` Liste les emplacements qui ont été vérifiés du point de vue du serveur.

### Indices
- `!hint` Liste tous les indices concernant votre monde, les points dont vous disposez pour les indices et le coût d'un indice.
- `!hint <nom de l'objet>` Indique le monde du jeu et l'endroit où se trouve votre objet, en utilisant les points gagnés en complétant les emplacements.
- `!hint_location <emplacement>` Indique quel est l'objet qui se trouve dans un emplacement spécifique et utilise les points gagnés en validant les emplacements.

### Collecte/libération
- `!collect` Vous permet d'obtenir tous les objets restants pour votre monde en les collectant dans tous les jeux. Généralement utilisé après l'accomplissement de l'objectif.
- `!release` Libère tous les objets contenus dans votre monde vers d'autres mondes. Généralement, cette opération est effectuée automatiquement par le serveur, mais il est possible de la configurer pour autoriser ou exiger une utilisation manuelle.

### Cheats
- `!getitem <nom de l'objet>` Permet d'ajouter un objet au joueur actuellement connecté, si cette fonction est activée dans le serveur.


## Hôte uniquement (sur Archipelago.gg ou dans la console de votre serveur)

### Général
- `/help` Renvoie une liste des commandes disponibles.
- `/license` Renvoie les informations relatives à la licence du logiciel.
- `/options` Renvoie les options actuelles du serveur, y compris le mot de passe en clair.
- `/players` Renvoie des informations sur les joueurs connectés et non connectés.
- `/save` Sauvegarde l'état du multi-monde actuel. Notez que le serveur procède à des sauvegardes automatiques toutes les minutes.
- `/exit` Arrêt du serveur

### Utilitaires
- `/countdown <nombre de secondes>` Démarre un compte à rebours en utilisant la valeur de secondes donnée. Utile pour synchroniser les démarrages.
  Le compte à rebours durera 10 secondes si vous tapez simplement `/countdown` sans argument.
- `/option <nom de l'option> <valeur de l'option>` Définir une option du serveur. Pour obtenir une liste d'options, utilisez la commande `/options`.
- `/alias <nom du joueur> <nom d'alias>` Attribuez un alias à un joueur, ce qui vous permet de faire référence au joueur par l'alias dans les commandes. 

### Collecte/libération
- `/collect <nom du joueur>` Envoyer tous les objets restants dans le multi-monde appartenant au joueur. 
- `/release <nom du joueur>` Envoie tous les objets restants dans ce monde, quels que soient les paramètres et le statut de fin de partie.
- `/allow_release <nom du joueur>` Permet au joueur concerné d'utiliser la commande `!release`.
- `/forbid_release <nom du joueur>` Empêche le joueur concerné d'utiliser la commande `!release`.

### Cheats
- `/send <nom du joueur> <nom de l'objet>` Attribue au joueur l'objet spécifié.
- `/send_multiple <amount> <nom du joueur> <nom de l'objet>` Attribue au joueur la quantité indiquée de l'objet spécifié.
- `/send_location <nom du joueur> <nom de l'emplacement>` Distribue l'emplacement donné au joueur spécifié comme si le joueur l'avait validé.
- `/hint <nom du joueur> <nom de l'objet ou de l'emplacement>` Envoyer un indice pour l'objet ou l'emplacement spécifié pour le joueur spécifié.

<br/> <br/>

# Commandes locales

Il s'agit d'une liste de commandes client qui peuvent être disponibles par l'intermédiaire de votre client Archipelago. Vous pouvez exécuter ces commandes dans la fenêtre de votre client.

Les commandes suivantes sont disponibles dans les clients qui utilisent le CommonClient, par exemple : TextClient, SNIClient, etc.

- `/connect <adresse:port>` Se connecter au serveur multi-monde à l'adresse donnée.
- `/disconnect` Vous déconnecte de votre session actuelle.
- `/help` Retourne une liste des commandes disponibles.
- `/license` Affiche les informations relatives à la licence du logiciel.
- `/received` Affiche tous les objets que vous avez reçus de tous les joueurs, y compris vous-même.
- `/missing` Affiche tous les emplacements avec leur statut actuel (coché/manquant).
- `/items` Liste tous les noms d'objets pour la partie en cours.
- `/locations` Liste tous les noms de lieux de la partie en cours.
- `/ready` Envoie le statut prêt au serveur.
- Si vous tapez quelque chose qui ne commence pas par `/`, un message sera envoyé à tous les joueurs.

## SNIClient seulement

La commande suivante n'est disponible que si vous utilisez le SNIClient pour les jeux basés sur la SNES.

- `/snes` Tente de se connecter à votre appareil SNES via SNI.
- `/snes_close` Ferme la connexion SNES actuelle.
- `/slow_mode` Active ou désactive le mode lent, qui limite la vitesse à laquelle vous recevez des objets.
