# Guide de customisation du son "OOF"

## À quoi sert cette fonctionnalité ?

Elle permet de modifier l'effet sonore quand Link prend des dégâts. Elle est habituellement utilisé en paire avec l'usage d'un sprite personnalisé. Cependant, il est possible d'utiliser cette fonctionnalité avec le sprite par défaut.

En raison de restrictions techniques dû à la limite de mémoire disponible, le son utilisé ne peut pas dépasser  **0,394 secondes**. Il est alors recommandé de choisir un son court comme un grognement ou un simple bruit afin qu'il soit reconnaissable.


Quelques exemples de ce qui est possible : https://www.youtube.com/watch?v=TYs322kHlc0

## Comment je crée mon propre son personnalisé ? 

1. Obtenez un fichier `.wav` avec les spécifications suivantes : PCM signé 16 bits à 12kHz et durée inférieure à 0,394 secondes. Vous pouvez faire cela en modifiant un échantillon existant avec un programme de modification sonore comme Audacity, ou en enregistrant votre propre son. Notez que les échantillons peuvent être réduits ou tronqués pour répondre aux exigences de la longueur, au détriment de la qualité sonore.

2. Utilisez la fonction `--encode` de l'outil snesbrr (https://github.com/boldowa/snesbrr) pour encoder le fichier `.wav` dans le bon format (.brr).

Le fichier .brr **ne peut pas** dépasser 2 673 octets. Tant que le fichier d'entrée répond aux spécifications ci-dessus, le fichier .brr doit avoir cette taille ou moins. Si le fichier est trop volumineux, retournez à l'étape 1 et raccourcissez l'échantillon. 

3. Lors de l'exécution de l'interface graphique de l'ajusteur, sélectionnez le fichier .brr que vous souhaitez utiliser après avoir cliqué l'option de menu  `"OOF" Sound`.

4. Vous pouvez également faire le patch via la ligne de commande: `python .\LttPAdjuster.py --baserom .\baserom.sfc --oof .\oof.brr .\romtobeadjusted.sfc`, qui remplace les noms de fichiers par les vôtres. 

## Puis-je utiliser plusieurs sons pour les sprites composites ?

Non, ce n'est techniquement pas réalisable. Vous ne pouvez utiliser qu'un seul son. 