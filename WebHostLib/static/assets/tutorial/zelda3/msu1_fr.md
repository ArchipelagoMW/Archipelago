# Guide d'installation de MSU-1

## Qu'est-ce que MSU-1 ?

MSU-1 permet l'utilisation de musiques en jeu personnalisées. Cela fonctionne sur une console originale, sur SuperNT, et
sur certains émulateurs. Ce guide explique comment trouver des packs de musiques personnalisées, couremment appelées
packs MSU, et comment les configurer pour les utiliser sur console, sur SuperNT et sur l'émulateur snes9x.

## Où trouver des packs MSU

Les packs MSU sont constamment en développement. Vous pouvez trouver une liste de packs complétés, ainsi que des packs
en développement sur
[cette feuille de calcul Google](https://docs.google.com/spreadsheets/d/1XRkR4Xy6S24UzYkYBAOv-VYWPKZIoUKgX04RbjF128Q).

## A quoi ressemble un pack MSU

Les packs MSU contiennent beaucoup de fichiers, la plupart étant des fichiers musicaux qui seront utilisés en cours de
jeu. Ces fichiers doivent être nommés de façon similaire, avec un nombre derrière le tiret, puis l'extension `.pcm`. Le
nom de chaque fichier n'importe pas, du moment qu'ils suivent tous le même motif. Le nom le plus populaire que vous
verrez est
`alttp_msu-X.pcm`, où X est remplacé par un nombre.

Il existe un autre type de fichier que vous devriez trouver dans le dossier d'un pack MSU. Ce fichier indique au
matériel ou à l'émulateur que MSU doit être activé pour ce jeu. Ce fichier doit être nommé de façon similaires aux
autres dans le dossier, mais il aura une extension `.msu` et pèsera 0 KB.

Voici un exemple de ce à quoi ressemble le dossier d'un pack MSU :

```
Liste des fichiers dans le dossier d'un pack MSU :
alttp_msu.msu
alttp_msu-1.pcm
alttp_msu-2.pcm
...
alttp_msu-34.pcm
```

## Comment utiliser un pack MSU

Dans tous les cas, vosu devez renommer votre fichier ROM pour qu'il corresponde au même motif que les autres fichiers
dans le dossier du pack MSU, ensuite vous placez votre fichier ROM dans ce dossier.

Le contenu du dossier ressemblera alors à ceci :

```
Liste des fichiers dans le dossier d'un pack MSU :
alttp_msu.msu
alttp_msu.sfc    <-- Ajoutez votre fichier ROM
alttp_msu-1.pcm
alttp_msu-2.pcm
...
alttp_msu-34.pcm
```

### Avec snes9x

1. Chargez le fichier ROM depuis snes9x.

### Avec un SD2SNES / FXPak sur une console originale

1. Mettez le dossier du pack MSU avec la ROM sur votre SD2SNES / FXPak.
2. Naviguez vers ce dossier et chargez votre ROM.

### Avec un SD2SNES / FXPak sur SuperNT

1. Mettez le dossier du pack MSU avec la ROM sur votre SD2SNES / FXPak.
2. Allumez votre SuperNT et naviguez vers le menu `Settings` (paramètres).
3. Entrez dans les paramètres `Audio`.
4. Cochez la case marquée `Cartridge Audio Enable` (activer l'audio de cartouche).
5. Retournez dans le menu précédent.
6. Choisissez `Save/Clear Settings` (sauvegarder/effacer les paramètres).
7. Choisissez `Save Settings` (sauvegarder les paramètres).
8. Choisissez `Run Cartridge` (lancer une cartouche) depuis le menu principal.
9. Naviguez vers le dossier du pack MSU et chargez votre ROM.

## Avertissement pour les streamers

Beaucoup de packs MSU utilisent des musiques copyrightées ce qui n'est pas permis sur des plateformes comme Twitch et
YouTube. Si vous choisissez de streamer des musiques copyrightées, votre VOD sera peut-être rendue muette. Dans le pire
des cas, vous pourriez recevoir une plainte DMCA pour faire retirer la vidéo. Faites attention à streamer uniquement des
musiques pour lesquelles vous avez le droit.