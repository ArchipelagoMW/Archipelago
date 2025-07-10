# Guía de instalación para A Link to the Past Randomizer Multiworld

## Software requerido

- [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases).
- [SNI](https://github.com/alttpo/sni/releases). Esto está incluido automáticamente en la instalación de Archipelago.
- SNI no es compatible con (Q)Usb2Snes.
- Hardware o software capaz de cargar y ejecutar archivos de ROM de SNES, por ejemplo:
    - Un emulador capaz de conectarse a SNI
      ([snes9x-nwa](https://github.com/Skarsnik/snes9x-emunwa/releases), [snes9x-rr](https://github.com/gocha/snes9x-rr/releases),
       [BSNES-plus](https://github.com/black-sliver/bsnes-plus),
       [BizHawk](https://tasvideos.org/BizHawk), o
       [RetroArch](https://retroarch.com?page=platforms) 1.10.1 o más nuevo).
    - Un SD2SNES, [FXPak Pro](https://krikzz.com/store/home/54-fxpak-pro.html), u otro hardware compatible. **nota:
Las SNES minis modificadas no tienen soporte de SNI. Algunos usuarios dicen haber tenido éxito con Qusb2Snes para esta consola,
pero no tiene soporte.**
- Tu archivo ROM japones v1.0, probablemente se llame `Zelda no Densetsu - Kamigami no Triforce (Japan).sfc`

## Procedimiento de instalación

1. Descarga e instala [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases/latest).
   **El archivo del instalador se encuentra en la sección de assets al final de la información de version**.
2. La primera vez que realices una generación local o parchees tu juego, se te pedirá que ubiques tu archivo ROM base.
   Este es tu archivo ROM de Link to the Past japonés. Esto sólo debe hacerse una vez.
   
4. Si estás usando un emulador, deberías de asignar tu emulador con compatibilidad con Lua como el programa por defecto para abrir archivos 
   ROM.
    1. Extrae la carpeta de tu emulador al Escritorio, o algún otro sitio que vayas a recordar.
    2. Haz click derecho en un archivo ROM y selecciona **Abrir con...**
    3. Marca la casilla junto a **Usar siempre este programa para abrir archivos .sfc**
    4. Baja al final de la lista y haz click en el texto gris **Buscar otro programa en este PC**
    5. Busca el archivo `.exe` de tu emulador y haz click en **Abrir**. Este archivo debería de encontrarse dentro de la carpeta que
      extrajiste en el paso uno. 

### Obtener el fichero de parche y crea tu ROM

Cuando te unas a una partida multiworld, se te pedirá enviarle tu archivo de configuración a quien quiera que esté creando. Una vez eso
este hecho, el creador te devolverá un enlace para descargar el parche o un fichero zip conteniendo todos los ficheros
de parche de la partida. Tu fichero de parche debe de tener la extensión `.aplttp`.

Pon tu fichero de parche en el escritorio o en algún sitio conveniente, y hazle doble click. Esto debería ejecutar
automáticamente el cliente, y además creará la rom en el mismo directorio donde este el fichero de parche.

### Conectar al cliente

#### Con emulador

Cuando el cliente se lance automáticamente, SNI debería de ejecutarse en segundo plano. Si es la 
primera vez que se ejecuta, tal vez se te pida permitir que se comunique a través del firewall de Windows

#### snes9x-nwa

1. Haz click en el menu Network y marca 'Enable Emu Network Control
2. Carga tu archivo ROM si no lo habías hecho antes

##### snes9x-rr

1. Carga tu fichero ROM, si no lo has hecho ya
2. Abre el menu "File" y situa el raton en **Lua Scripting**
3. Haz click en **New Lua Script Window...**
4. En la nueva ventana, haz click en **Browse...**
5. Selecciona el archivo lua conector incluido con tu cliente
      - Busca en la carpeta de Archipelago `/SNI/lua/`.
6. Si ves un error mientras carga el script que dice `socket.dll missing` o algo similar, ve a la carpeta de
el lua que estas usando en tu gestor de archivos y copia el `socket.dll` a la raíz de tu instalación de snes9x.

##### BNES-Plus

1. Cargue su archivo ROM si aún no se ha cargado.
2. El emulador debería conectarse automáticamente mientras SNI se está ejecutando.

##### BizHawk

1. Asegurate que se ha cargado el núcleo BSNES. Se hace en la barra de menú principal, bajo:
    - (≤ 2.8) `Config` 〉 `Cores` 〉 `SNES` 〉 `BSNES`
    - (≥ 2.9) `Config` 〉 `Preferred Cores` 〉 `SNES` 〉 `BSNESv115+`
2. Carga tu fichero de ROM, si no lo has hecho ya.
   Si has cambiado tu preferencia de núcleo tras haber cargado la ROM, no te olvides de volverlo a cargar (atajo por defecto: Ctrl+R).
3. Arrastra el archivo `Connector.lua` que has descargado a la ventana principal de EmuHawk.
   - Busca en la carpeta de Archipelago `/SNI/lua/`.
   - También podrías abrir la consola de Lua manualmente, hacer click en `Script` 〉 `Open Script`, e ir a `Connector.lua`
      con el selector de archivos.

##### RetroArch 1.10.1 o más nuevo

Sólo hay que seguir estos pasos una vez.

1. Comienza en la pantalla del menú principal de RetroArch.
2. Ve a Ajustes --> Interfaz de usario. Configura "Mostrar ajustes avanzados" en ON.
3. Ve a Ajustes --> Red. Pon "Comandos de red" en ON. (Se encuentra bajo Request Device 16.) Deja en 55355 el valor por defecto,
 el Puerto de comandos de red.

![Captura de pantalla del ajuste Comandos de red](/static/generated/docs/A%20Link%20to%20the%20Past/retroarch-network-commands-en.png)
4. Ve a Menú principal --> Actualizador en línea --> Descargador de núcleos. Desplázate y selecciona "Nintendo - SNES /
   SFC (bsnes-mercury Performance)".

Cuando cargas un ROM, asegúrate de seleccionar un núcleo **bsnes-mercury**. Estos son los únicos núcleos que permiten
que herramientas externas lean datos del ROM.

#### Con Hardware

Esta guía asume que ya has descargado el firmware correcto para tu dispositivo. Si no lo has hecho ya, por favor hazlo ahora. Los
usuarios de SD2SNES y FXPak Pro pueden descargar el firmware apropiado
[aqui](https://github.com/RedGuyyyy/sd2snes/releases). Puede que los usuarios de otros dispositivos encuentren informacion útil
[en esta página](http://usb2snes.com/#supported-platforms).

1. Cierra tu emulador, el cual debe haberse autoejecutado.
2. Enciende tu dispositivo y carga la ROM.

### Conecta al Servidor Archipelago

El fichero de parche que ha lanzado el cliente debería de haberte conectado automaticamente al MultiServer. Sin embargo hay algunas
razones por las que puede que esto no suceda, como que la partida este hospedada en la página web pero generada en otra parte. Si la
ventana del cliente muestra "Server Status: Not Connected", simplemente preguntale al creador de la partida la dirección
del servidor, cópiala en el campo "Server" y presiona Enter.

El cliente intentará conectarse a esta nueva dirección, y debería mostrar "Server Status: Connected" momentáneamente.

### Jugar al juego

Cuando el cliente muestre tanto el dispositivo SNES como el servidor como conectados, estas listo para empezar a jugar. Felicidades por
haberte unido a una partida multiworld con exito! Puedes ejecutar varios comandos en tu cliente. Para mas informacion
acerca de estos comando puedes usar `/help` para comandos locales del cliente y `!help` para comandos de servidor.
