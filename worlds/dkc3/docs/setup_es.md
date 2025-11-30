# Guiá de configuración del randomizer de Donkey Kong Country 3

## Software requerido

- [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases).


- Hardware o software capaz de cargar y ejecutar Roms de SNES.
    - Un emulador capaz de conectarse a SNI, como por ejemplo:
        - snes9x-rr desde: [snes9x rr](https://github.com/gocha/snes9x-rr/releases),
        - BizHawk desde: [TASVideos](https://tasvideos.org/BizHawk),
        - RetroArch 1.10.3 o mas reciente: [RetroArch Website](https://retroarch.com?page=platforms). O,
    - Un SD2SNES, FXPak Pro ([FXPak Pro Store Page](https://krikzz.com/store/home/54-fxpak-pro.html)), u otro
      hardware compatible.
- Una copia legal de Donkey Kong Country 3, nombrada regularmente como 
`Donkey Kong Country 3 - Dixie Kong's Double Trouble! (USA) (En,Fr).sfc`.

## Software Opcional
- Tracker para Donkey Kong Country 3
	- PopTracker desde: [PopTracker Releases Page](https://github.com/black-sliver/PopTracker/releases/),
	- Donkey Kong Country 3 Archipelago PopTracker pack desde: [DKC3 AP Tracker Releases Page](https://github.com/PoryGone/DKC3_AP_Tracker/releases/)

## Procedimientos de instalación

### Configuración para Windows

1. Descarga e instala [Archipelago](<https://github.com/ArchipelagoMW/Archipelago/releases/latest>). **El archivo de 
   instalación se encuentra en la sección de recursos, en la parte inferior de los cambios de la versión.**
2. La primera vez que hagas una generación o parche del juego, aparecerá una ventana solicitándote donde están 
   ubicados los archivos base del juego (ROM).
   Este archivo es tu copia de Donkey Kong Counry 3. Una vez que lo selecciones, ya no se te preguntará por él en el 
   futuro.
3. Si estás usando un emulador, necesitarás asignarlo como el LUA predeterminado para abrir ese tipo de archivos.
    1. Extrae tu emulador en una carpeta en tu escritorio o cualquier otro lugar que recuerdes.
    2. Haz clic derecho en cualquier Rom de SNES y selecciona **Abrir con...**
    3. Marca la casilla **Usar siempre esta aplicación para abrir archivos .sfc**.
    4. Baja hasta el final de la lista y da clic en el texto en gris que dice: **Buscar otra aplicación en este PC**.
    5. Navega hasta la carpeta donde se encuentra el emulador que usarás, da click en el archivo `.exe` y luego en 
    **Abrir**. Este archivo ejecutable debe de encontrarse en la carpeta que obtuviste en el paso uno.

## Crea un archivo de configuración (.yaml)

### ¿Qué es un archivo de configuración, y por qué necesito uno?

Consulte la guía sobre cómo configurar un YAML básico en la guía de configuración de 
Archipelago: [Guía básica de configuración para Multiworld](/tutorial/Archipelago/setup/en)

### ¿Dónde consigo el archivo de configuración para este juego?

El archivo de configuración se encuentra en la página web de archipelago. En esta página se te permitirá configurar 
los ajustes de tu partida de la manera que tú prefieras y podrás exportar dichos ajustes desde la misma página. 
La página de configuración es la siguiente: [Página de opciones del jugador para Donkey Kong Country 3](/games/Donkey%20Kong%20Country%203/player-options)

### Verifica tu archivo de configuración (.yaml)

Si deseas verificar que tu archivo funcionara o está estructurado correctamente, puedes usar cualquier página para 
verificar archivos YAML. Puedes usar esta por ejemplo: [Página para validación de YAML](/check)

## Generar una partida de un solo jugador

1. Navega a la página de configuración de Donkey Kong Country 3, configura tus opciones y preferencias, y, por último, 
   haz clic en el botón "Generate Game".
    - Página de configuración: [Página de opciones del jugador para Donkey Kong Country 3](/games/Donkey%20Kong%20Country%203/player-options)
2. Se te mostrará una página titulada "Seed Info".
3. Haz clic en el texto "Create New Room".
4. Se te mostrará otra página titulada ¨Server Page¨, donde podrás descargar tu archivo/parche del juego.
5. Haz doble clic en tu archivo/parche, y el cliente de archipelago con la estancia de Donkey Kong Country 3 se abrirá 
   de manera automática. Se te pedirá que abras tu ROM de Donkey Kong Country 3 y el emulador se abrirá de manera 
   automática.

## Unirse a una partida Multiworld

### Obtén tu archivo/parche y crea tu ROM

Cuando te unas a un juego multiworld, se te pedirá que proporciones tu archivo de configuración al anfitrión (YAML). 
Una vez hecho esto, el anfitrión te proporcionará un enlace para descargar tu archivo de parche o un archivo ZIP que 
contiene los archivos de parche de todos los jugadores. Tu archivo de parche debe tener la extensión ".apdkc3".⁣

Coloca el archivo/parche en tu escritorio o en algún lugar de tu preferencia, luego haz doble clic en él. Esto deberá 
abrir de manera automática el launcher del cliente de archipelago. Se te pedirá que elijas tu ROM y se creará la ROM 
con el parche en la misma carpeta donde se encuentra el archivo/parche que se te otorgó al inicio.

### Conectarse al cliente

#### Con un emulador

Cuando el launcher del cliente se abra de manera automática, y el emulador se abra junto a este. Se ejecutará en 
simultáneo una instancia SNI de fondo. Si es tu primera vez ejecutando el parche, se te podría preguntar que permitas 
la comunicación del programa en el Firewall de Windows.

##### snes9x-rr

1. Carga tu ROM parchada si el emulador no se ejecutó.
2. Haz clic en ¨File¨ en el menú superior y luego clic en **Lua Scripting**
3. Haz clic en **New Lua Script Window...**
4. En la ventana que se abrirá, haz clic en **Browse...**
5. Selecciona el archivo `Connector.lua`, que se incluye al instalar archipelago launcher:
    - Busca en la carpeta de instalación de Archipelago, normalmente se encuentra en la ruta; `/SNI/lua/Connector.lua`
6. Si al cargar el script aparece un error que indica que `falta socket.dll` o algo similar, ve a la carpeta del lua 
   que estás utilizando en el explorador de archivos y copia el archivo `socket.dll` en la carpeta base de la instalación 
   de tu emulador snes9x.

##### BizHawk

1. Asegúrate de que tienes configurado el núcleo BSNES como predeterminado. Esto se puede hacer en el menú principal, 
en los apartados:
    - Si tienes la versión 2.8 o inferior: `Config` 〉 `Cores` 〉 `SNES` 〉 `BSNES`
    - Si tienes la versión 2.9 o superior: `Config` 〉 `Preferred Cores` 〉 `SNES` 〉 `BSNESv115+`
2. Carga tu ROM con parche si aún no lo has hecho o si el emulador no la abrió de manera automática.
   Si cambiaste el núcleo preferido después de cargar la ROM, no olvides recargar el emulador. 
   (Puedes usar las teclas CTRL + R)
3. Arrastra y suelta el archivo `Connector.lua` que se incluye al instalar archipelago launcher:
    - Busca en la carpeta de instalación de Archipelago, normalmente se encuentra en la ruta; `/SNI/lua/Connector.lua`.
      - Puedes abrir la consola Lua de manera manual, si así lo deseas, haz clic en `Script 〉 Open Script`, 
       luego dirígete a la ruta donde se encuentre el `Connector.lua` y selecciónalo.

##### RetroArch 1.10.3 or newer

Solo tendrás que realizar estos pasos una vez. Nota, RetroArch 1.9.x ya no funcionará, ya que es una versión más vieja 
que la versión 1.10.3.

1. Dirígete al menú principal de RetroArch.
2. Dirígete al apartado "Settings" --> "User Interface". Y asegúrate de que el apartado "Show Advanced Settings" esté 
   encendido.
3. Dirígete al apartado "Settings" --> "Network". Asegúrate de que el apartado "Network Commands" esté encendido. 
   (Se encuentra debajo de Solicitar dispositivo 16). Deje el puerto de comando de red predeterminado en 55355. \
   ![Screenshot of Network Commands setting](../../generic/docs/retroarch-network-commands-en.png)
4. Dirígete al menú principal --> "Online Updater" --> "Core Downloader". Baja un poco en el apartado y selecciona 
   "Nintendo - SNES /SFC (bsnes-mercury Performace)".

Cuando cargues la ROM parchada, asegúrate de que tengas elegido el núcleo **bsnes-mercury**. Estos son los únicos 
núcleos que permiten herramientas externas para poder leer los datos de las ROM.

#### Con Hardware

Esta guía asume que cuentas con el firmware correcto para tu dispositivo. Si no lo tienes aún, por favor, hazlo ahora. 
Los usuarios de SD2SNES y FXPak Pro deben de descargar el Firmware apropiado en la página de SD2SNES en el apartado de 
lanzamientos: [Pagina de lanzamientos de SD2SNES](https://github.com/RedGuyyyy/sd2snes/releases)

Otro tipo de hardware podría contar con información útil en 
la página de usb2snes: [Página de plataformas compatibles de usb2snes](http://usb2snes.com/#supported-platforms)

1. Cuando apliques el parche a tu ROM, cierra el emulador que se abrirá de manera automática. 
2. Enciende tu dispositivo SNES y ejecuta la ROM parchada.

### Conéctate al servidor de Archipelago

El archivo/parche deberá de abrir de manera automática el cliente de archipelago, y este, en consecuencia, se 
conectará al servidor AP. Aun así, existen casos en donde esto no pasa, incluido el caso donde la partida/servidor se 
hostea en la página web, pero la semilla se generó en otra parte. Si la ventana del cliente muestra el texto 
"Server Status: Not Connected", pídele al host de la partida que te comparta la dirección IP y el puerto de la partida 
(Debe verse algo como: archipelago.gg:12345), copia la IP y pégala en el recuadro de texto que aparece en la consola 
y presiona Enter.

El cliente intentará conectarse al servidor con esa nueva dirección IP y puerto, y en unos momentos lanzará un nuevo 
texto; "Server Status: Connected", lo cual indicará que ya estás dentro de la partida del servidor.

### Empezar a jugar

Cuando el cliente indique que tanto el dispositivo SNES como el Servidor están conectados, puedes comenzar a jugar. 
¡Felicidades, te has unido de manera exitosa a una partida multiworld!

## Alojar una partida multiworld

La forma recomendada de alojar un juego es utilizar nuestro servicio de alojamiento. 
El proceso es relativamente sencillo:

1. Recopila los archivos de configuración de tus jugadores.
2. Crea un archivo zip que contenga los archivos de configuración de tus jugadores.
3. Sube ese archivo ZIP a la página para generar partidas que se encuentra arriba.
    - Página para generar partidas: [Página WebHost de generación de semillas](/generate)
4. Espera un momento mientras la semilla se genera.
5. Cuando se genere la semilla, se te redirigirá a la página "Seed Info".
6. Haz clic en "Create New Room". Esto te enviará a la página del servidor. Proporciona el enlace a esta página a tus 
   jugadores para que puedan descargar sus archivos de parche desde allí.
7. Ten en cuenta que hay un enlace a "MultiWorld Tracker" en la parte superior de la página de la sala. 
   El tracker muestra el progreso de todos los jugadores en el juego. 
   También se puede proporcionar el enlace a esta página a cualquier espectador.
8. Una vez que todos los jugadores se hayan unido, pueden comenzar a jugar.
