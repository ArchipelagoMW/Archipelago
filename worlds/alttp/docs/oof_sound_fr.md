# Guide de customisation du son "OOF"

## À quoi sert cette fonctionnalité ?

Cela remplace l'effet sonore quand Link prend des dégâts. Le cas d'utilisation prévu pour cela est celui des sprites personnalisés, mais vous pouvez utiliser avec n'importe quel sprite, celui par défaut inclus. 

En raison de restrictions techniques résultant d'une limite de mémoire disponible, il y a une limite quand à la durée du son. Utilisant la méthode actuelle, la limite est de  **0,394 secondes**. Cela signifie que beaucoup d'idées ne fonctionneront pas, et tout dialogue intelligible ou tout autre chose qu'un grognement ou un simple bruit sera trop long.

Quelques exemples de ce qui est possible : https://www.youtube.com/watch?v=TYs322kHlc0

## Comment je crée mon propre son personnalisé ? 

1. Obtenir un fichier .wav avec les spécifications suivantes : PCM signé 16 bits à 12kHz, pas plus de 0,394 secondes. Vous pouvez faire ça en éditant un échantillon existant avec un programme comme Audacity ou en enregistrant votre propre son. Notez que les échantillons peuvent être réduits ou tronqués pour répondre aux exigences de la longueur, au détriment de la qualité sonore.
2. Utiliser la fonction `--encode` de l'outil snesbrr (https://github.com/boldowa/snesbrr) pour encoder le fichier .wav dans le bon format (.brr).
Le fichier .brr **ne peut pas** dépasser 2 673 octets. Tant que le fichier d'entrée répond aux spécifications ci-dessus, le fichier .brr doit avoir cette taille ou moins. Si le fichier est trop large, retourner à l'étape 1 et raccourcir l'échantillon. 
3. Lors de l'exécution de l'interface graphique de l'ajusteur, sélectionner simplement le fichier .brr que vous souhaitez utiliser après avoir cliqué l'option de menu `"OOF" Sound`.
4. Vous pouvez également faire le patch via la ligne de commande: `python .\LttPAdjuster.py --baserom .\baserom.sfc --oof .\oof.brr .\romtobeadjusted.sfc`, qui remplace les noms de fichiers par les vôtres. 

## Puis-je utiliser plusieurs sons pour les sprites composites ?

Non, ce n'est techniquement pas réalisable. Vous ne pouvez utiliser qu'un seul son. 