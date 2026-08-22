# Guía de configuración para Wind Waker Archipelago 

¡Bienvenido a The Wind Waker Archipelago! Esta Guía te ayudará a configurar el randomizer y jugar tu primer
multimundo. Si vas a jugar The Wind Waker, debes seguir unos pasos sencillos para empezar.

## Requisitos

Necesitarás los siguientes componentes para poder jugar The Wind Waker:
* Instalar [Dolphin Emulator](https://dolphin-emu.org/download/). **Recomendamos usar la versión más reciente.**
    * Los usuarios de Linux pueden usar el paquete flatpak 
    [disponible en Flathub](https://flathub.org/apps/org.DolphinEmu.dolphin-emu).
* La versión más reciente de [TWW AP Randomizer Build](https://github.com/tanjo3/wwrando/releases?q=tag%3Aap_2).
    * Tenga en cuenta que este build es **diferente** del usado por el randomizador independiente. Este build es
      específico para Archipelago.
* Un ISO de The Wind Waker (versión de Norte América), probablemente llamado
  "Legend of Zelda, The - The Wind Waker (USA).iso".

Opcionalmente, también puedes descargar:
* [Wind Waker Tracker](https://github.com/Mysteryem/ww-poptracker/releases/latest)
  * Requiere [PopTracker](https://github.com/black-sliver/PopTracker/releases)
* [Modelos de jugador personalizables para Wind Waker](https://github.com/Sage-of-Mirrors/Custom-Wind-Waker-Player-Models)

## Configurando el YAML

Todos aquellos que vayan a jugar a The Wind Waker deben darle al host de la sala un archivo YAML el cual contiene
la configuración para su mundo. Visita la
[página de opciones para The Wind Waker](/games/The%20Wind%20Waker/player-options) para generar un YAML con las
opciones deseadas. Solamente las localizaciones con la categoría de "Progression Locations" van a ser randomizadas
en tu mundo. Una vez que estés feliz con tu configuración, provee al host de la sala tu archivo YAML y procede
con el siguiente paso.

## Conectándose a una sala

El host del multimundo te proveerá de un enlace para descargar tu archivo APTWW o un archivo zip que contiene los
archivos de todos. El archivo APTWW debería llamarse `P#_<name>_XXXXX.aptww`, donde `#` es tu ID de jugador,
`<name>` es tu nombre de jugador, y `XXXXX` es el ID de la sala. El host también debería proveerte con el nombre
de la sala y número de puerto.

Una vez que estés listo, sigue estos pasos para conectarte a la sala:
1. Ejecuta el TWW AP Randomizer Build. Si esta es la primera vez que abres el randomizer, vas a tener que
   especificar la ruta del ISO The Wind Waker y la carpeta donde se guardará el ISO randomizado. Estos se van a
   guardar para la próxima vez que abras el programa. 
2. Modifica cualquier ajuste estético y opciones de personalización del jugador según lo desees.
3. Para el archivo APTWW, busque y localice la ruta de tu archivo APTWW.
4. Abajo a la derecha haga clic en `Randomize`. Esto randomizará el ISO y lo pondrá en la carpeta que se
   especificó antes (en el paso 1). El archivo se llamará `TWW AP_YYYYY_P# (<name>).iso`, donde `YYYYY` es el
   nombre de la semilla, `#` es tu ID de jugador, y `<name>` es tu nombre (ranura) de jugador. Verifica que los
   valores sean correctos para el multimundo.
5. Abre Dolphin y úsalo para abrir el ISO randomizado.
6. Ejecuta `ArchipelagoLauncher.exe` (sin `.exe` en Linux) y elige `The Wind Waker Client`, el cual abrirá un
   cliente de texto. Si Dolphin no está abierto o aún tienes que crear una nueva partida, se te notificará que
   lo hagas.
    * Una vez que hayas abierto el ISO en Dolphin, el cliente deberá decir "Dolphin connected successfully.".
7. Conéctate a la sala ingresando el nombre del servidor y el número de puerto en la parte de arriba y presionando
   `Connect`. Para salas que sean alojadas en la página web, este sería `archipelago.gg:<port>`, donde `<port>`
   es el número de puerto. Si el juego está siendo alojado con el `ArchipelagoServer.exe` (sin `.exe` en Linux),
   el número de puerto será el default `38281` pero puede ser cambiado en el `host.yaml`.
8. Si has abierto el ISO correspondiente al multimundo al que te has conectado, se debería autenticar
   automáticamente a tu nombre de slot al empezar una nueva partida.

## Solución de problemas

* Asegúrate de que estés usando la misma versión de Archipelago en la que el multimundo se generó.
* Asegúrate de que `tww.apworld` no esté en tu carpeta de `custom_worlds` en la ruta de instalación de
  Archipelago.
* Asegúrate de que el build del randomizer y la versión de Archipelago que se esté usando sea la misma. El build
  debería proveerte un mensaje de error indicándote la versión correcta. También puedes ver las notas de release
  de TWW AP build [aquí](https://github.com/tanjo3/wwrando/releases?q=tag%3Aap_2) para verificar que versiones de
  Archipelago son compatibles con cada build.
* No ejecutes el Archipelago Launcher o Dolphin como administrador en Windows.
* Si tienes problemas con la autenticación, asegúrate que el ISO randomizado esté abierto en Dolphin y corresponda
  al multimundo al que te intentas conectar.
* Asegúrate de que no tengas los trucos (cheats) o códigos habilitados. Algunos trucos (cheats) pueden interferir
  con la emulación de manera inesperada y causar que sea más difícil solucionar otros problemas.
* Asegúrate de que `Emular caché de escritura diferida (lento)` en Dolphin (en `Opciones` > `Configuración` >
  `Avanzado`) esté **deshabilitado**.
* Si el cliente no se puede conectar a Dolphin, asegúrate que Dolphin esté en el mismo disco que Archipelago.
  Tenerlo en un disco externo ha sido reportado por causar problemas de conexión.
* Asegúrate que `Región de respaldo` en Dolphin (en `Opciones` > `Configuración` > `General`) esté puesto en
  `NTSC-U`.
* Si estás ejecutando un GC boot menu personalizado, necesitarás omitirlo en `Opciones` > `Configuración` >
  `GameCube` y activando `Omitir menú principal`.