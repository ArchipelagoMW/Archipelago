# MSU-1 Guía de instalación

## Que es MSU-1?

MSU-1 permite el uso de música personalizada durante el juego. Funciona en hardware original, la SuperNT, y algunos
emuladores. Esta guiá explicará como encontrar los packs de música personalizada, comúnmente llamados pack MSU, y como
configurarlos para su uso en hardware original, la SuperNT, and el emulador snes9x.

## Donde encontrar packs MSU

Los packs MSU están constantemente en desarrollo. Puedes encontrar una lista de pack completos, al igual que packs en
desarrollo en
[esta hoja de calculo Google](https://docs.google.com/spreadsheets/d/1XRkR4Xy6S24UzYkYBAOv-VYWPKZIoUKgX04RbjF128Q).

## Que pinta debe tener un pack MSU

Los packs MSU contienen muchos ficheros, la mayoria de los cuales son los archivos de música que se usaran durante el
juego. Estos ficheros deben tener un nombre similar, con un guión seguido por un número al final, y tienen
extensión`.pcm`. No importa como se llame cada archivo de música, siempre y cuando todos sigan el mismo patrón. El
nombre más popular es
`alttp_msu-X.pcm`, donde X es un número.

Hay otro tipo de fichero que deberias encontrar en el directorio de un pack MSU. Este archivo indica al hardware o
emulador que MSU debe ser activado para este juego. El fichero tiene un nombre similar al resto, pero tiene como
extensión `.msu` y su tamaño es 0 KB.

Un pequeño ejemplo de los contenidos de un directorio que contiene un pack MSU:

```
Lista de ficheros dentro de un directorio de pack MSU:
alttp_msu.msu
alttp_msu-1.pcm
alttp_msu-2.pcm
...
alttp_msu-34.pcm
```

## Como usar un pack MSU

En todos los casos, debes renombrar tu fichero de ROM para que coincida con el resto de nombres de fichero del
directorio, y copiar/pegar tu fichero rom dentro de dicho directorio.

Esto hara que los contenidos del directorio sean los siguientes:

```
Lista de ficheros dentro del directorio de pack MSU:
alttp_msu.msu
alttp_msu.sfc    <-- Tu fichero rom añadido
alttp_msu-1.pcm
alttp_msu-2.pcm
...
alttp_msu-34.pcm
```

### Con snes9x

1. Carga el fichero de rom en snes9x.

### Con SD2SNES / FXPak en hardware original

1. Carga tu directorio de pack MSU en tu SD2SNES / FXPak.
2. Navega hasta el directorio de pack MSU y carga la ROM

### Con SD2SNES / FXPak en SuperNT

1. Carga tu directorio de pack MSU en tu SD2SNES / FXPak.
2. Enciende tu SuperNT y navega al menú `Settings`.
3. Entra en la opcion `Audio`.
4. Activa la caja `Cartridge Audio Enable.`
5. Navega al menú anterior
6. Elije `Save/Clear Settings`.
7. Elije `Save Settings`.
8. Elije `Run Cartridge` en el menú principal.
9. Navega hasta el directorio de pack MSU y carga la ROM

## Aviso a streamers

Muchos packs MSU usan música con derechos de autor la cual no esta permitido su uso en plataformas como Twitch o
YouTube. Si elijes hacer stream de dicha música, tu VOD puede ser silenciado. En el peor caso, puedes recibir una orden
de eliminación DMCA. Por favor, tened cuidado y solo streamear música para la cual tengas los derechos para hacerlo.

##### Packs MSU seguros para Stream

A continuación enumeramos los packs MSU que, packs which, por lo que sabemos, son seguros para vuestras retransmisiones.
Se iran añadiendo mas conforme vayamos enterandonos. Si sabes alguno que podamos haber olvidado, por favor haznoslo
saber!

- Musica del juego original
- [Smooth McGroove](https://drive.google.com/open?id=1JDa1jCKg5hG0Km6xNpmIgf4kDMOxVp3n)

