# Hades Setup Guide

## Required Software

Instala el juego en steam o EGS y luego los siguientes mods:

- [ModImporter](https://github.com/SGG-Modding/ModImporter/releases/tag/1.5.2)
- [ModUtils v 2.10.1](https://github.com/SGG-Modding/ModUtil/releases/tag/2.10.1)
- [StyxScribe sin REPL](https://github.com/NaixGames/StyxScribeWithoutREPL).
- [Polycosmos](https://github.com/Naix99/Polycosmos/tree/main/Polycosmos)

Pon hades.apworld en un tu carpeta de custom_worlds (en tu carpeta de instalacion de archipelago).

## Configurando tu YAML

### Que es un YAML y por que necesito uno?

Un archivo YAML contiene un conjunto de opciones de configuración que proporcionan al generador información sobre cómo se debería
generar tu juego. Cada jugador de un multimundo proporcionará su propio archivo YAML. Esta configuración permite que cada jugador disfrute
una experiencia personalizada a su gusto, y diferentes jugadores en el mismo multimundo pueden tener diferentes opciones.

### Donde saco un YAML?

Puedes personalizar tu configuración usando el archivo .yaml en la carpeta Hades World. El repositorio también tiene 3 diferentes
plantillas con diferentes dificultades en mente. Recomendamos comenzar con la dificultad Fácil.

### Conectandose al Server

Para iniciar el juego y jugar en el multiworld, debes abrir ArchipelagoLauncher.exe. Debería haber una opción
para HadesCliente. Esto abre una ventana para buscar la ruta de instalación de Hades (la ruta de Steam estándar es
C:\Archivos de programa\Steam\steamapps\common\Hades).
Una vez seleccionada la carpeta, el juego debería abrir Hades y el cliente Archipelago.

Utilice la ventana Cliente para conectarse al servidor Archipelago antes de elegir su archivo guardado. Si esto se hace correctamente deberías
poder iniciar el juego y obtener una ubicación en la primera sala, que imprimirá un mensaje en tu consola. Si la conexión
no se realiza correctamente, recibirá un mensaje de error en la primera sala. Sale, vuelve a conectarte y intenta denuevo.