# Mega Man X guía de instalación

## Software requerido

- [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases).
- [SNI](https://github.com/alttpo/sni/releases). Este viene proporcionado junto a la instalación de Archipelago.
- Software capaz de cargar y permitir jugar archivos ROM de SNES:
   - [snes9x-nwa](https://github.com/Skarsnik/snes9x-emunwa/releases)
   - [snes9x-rr](https://github.com/gocha/snes9x-rr/releases)
   - [BSNES-plus](https://github.com/black-sliver/bsnes-plus). **Nota:** No usen el `Reset` del emulador, causa 
   corrupción de RAM y puede mandar Checks de manera aleatoria.
- Una copia de tu Mega Man X US proveniente del cartucho original o de la Legacy Collection. La comunidad de 
Archipelago no puede proveer ni uno de estos.
   - SNES US MD5: `cfe8c11f0dce19e4fa5f3fd75775e47c`
   - Legacy Collection US MD5: `ff683b75e75e9b59f0c713c7512a016b`

## Software opcional
- [Tracker de mapa y niveles para Mega Man X Archipelago](https://github.com/BrianCumminger/megamanx-ap-poptracker/releases), 
para usar con [PopTracker](https://github.com/black-sliver/PopTracker/releases)
- [Scripts Lua que muestran información variada en el mismo emulador](https://github.com/Coltaho/emulator_lua_scripts), 
para [snes9x-rr](https://github.com/gocha/snes9x-rr/releases) y [BizHawk](https://tasvideos.org/BizHawk/ReleaseHistory)

### Métodos de jugar no soportados oficialmente
- [BizHawk](https://tasvideos.org/BizHawk/ReleaseHistory) tiene reportes de funcionar adecuadamente, pero no es un 
método de jugar que el desarollador utiliza. Procede bajo tu propio riesgo.
- RetroArch no tiene reportes de funcionar. Procede bajo tu propio riesgo.
- sd2snes/FX Pak no funcionan en esta implementación debido a limitantes de los componentes internos de dichos cartuchos.

## Procedimiento de instalación

1. Descarga e instala [Archipelago](<https://github.com/ArchipelagoMW/Archipelago/releases/latest>). **El instalador se 
encuentra en la sección de `Assets` después de la información de la versión.**
2. Asocia los archivos `.sfc` con el emulador deseado:
   1. Extrae el emulador y sus archivos en algún lugar de tu computadora que puedas recordar.
   2. Da clic derecho en un ROM y selecciona **Abrir con...**
   3. Activa la casilla enseguida de **Siempre usar esta aplicación para abrir archivos .sfc**
   4. Mueve el menú hasta encontrar al final de la lista la opción llamada **Buscar otra aplicación en el equipo**
   5. Busca el archivo ejecutable del emulador (`.exe`) y da click en **Abrir**. El archivo puede encontrarse en donde 
   extrajíste el emulador en el primer paso.

## Configura tu archivo YAML

### ¿Qué es un archivo YAML y por qué necesito uno?

Tu archivo YAML contiene un número de opciones que proveen al generador con información sobre como debe generar tu
juego. Cada jugador de un multiworld entregará su propio archivo YAML. Esto permite que cada jugador disfrute de una
experiencia personalizada a su manera, y que diferentes jugadores dentro del mismo multiworld pueden tener diferentes
opciones.

### ¿Dónde puedo obtener un archivo YAML?

Puedes generar un archivo YAML or descargar su plantilla en la [página de configuración de jugador de Mega Man X](/games/Mega%20Man%20X%20/player-options)

## Unirse a un juego MultiWorld

### Obtener tu parche de Mega Man X

Cuando te unes a un juego multiworld, se te pedirá que entregues tu archivo YAML a quien lo esté organizando.
Una vez que la generación acabe, el anfitrión te dará un enlace a tu archivo, o un .zip con los archivos de
todos. Tu archivo tiene una extensión `.apmmx`.

Haz doble clic en tu archivo `.apmmx` para que se ejecute el cliente y realice el parcheado del ROM.
Una vez acabe ese proceso (esto puede tardar un poco), el cliente y el emulador se abrirán automáticamente (si es que se
ha asociado la extensión al emulador tal como fue recomendado)

### Conectarse al multiserver

Cuando el cliente se ejecuta automaticamente, SNI también se debe ejecutar automaticamente en segundo plano. Si es la
primera vez que ejecutas el cliente, es posible que se te pida que permitas a la aplicación a través del Firewall de
Windows.

Para conectar el cliente con el servidor, simplemente pon `<dirección>:<puerto>` en la caja de texto superior y presiona
enter (si el servidor tiene contraseña, en la caja de texto inferior escribe `/connect <dirección>:<puerto> [contraseña]`)

Cada emulador tiene un procedimiento distinto para poder jugar, sigue el que se acomode a tus preferencias.

#### snes9x-nwa

1. Da click en el menú de Network y activa **Enable Emu Network Control**
2. Carga tu ROM parcheado si aún no ha sido cargado
3. El emulador debe de conectarse automáticamente mientras SNI está ejecutandose en segundo plano

#### snes9x-rr

1. Carga tu ROM parcheado si aún no ha sido cargado
2. Da click en el menú de File y coloca el cursor sobre **Lua Scripting**
3. Da click en **New Lua Script Window...**
4. En la ventana que aparece da click en **Browse..**
5. Selecciona el archivo conector incluido con el cliente
   - Busca en la carpeta de Archipelago el directorio de `/SNI/lua/`
6. Si llega a aparecer un error al cargar el script que diga que no cuentas con `socket.dll` o algo similar, ve a la
carpeta del lua que estás utilizando y copia el archivo `socket.dll` a la carpeta raíz de tu snes9x

#### BSNES-Plus

1. Carga tu ROM parcheado si aún no ha sido cargado
2. El emulador debe de conectarse automáticamente mientras SNI está ejecutándose en segundo plano

## Notas finales para jugar

Cuando el cliente muestra que el dispositivo de SNES y el Server están conectados, estas listo para comenzar a jugar.
Dentro del mismo cliente puedes encontrar diferentes comandos que puedes ejecutar. Para más información acerca de los 
comandos disponibles puedes escribir `/help` para comandos del cliente y `!help` para comandos del server.
