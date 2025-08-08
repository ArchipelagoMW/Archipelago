# Guía de instalación de Super Mario 64 EX MultiWorld

## Software necesario

- Una ROM de Super Mario 64 US o JP (Las versiones de Europa y Shindou no son compatibles)
- Cualquiera de las siguientes opciones
    - [SM64AP-Launcher](https://github.com/N00byKing/SM64AP-Launcher/releases) o
    - Clonar y compilar [sm64ex](https://github.com/N00byKing/sm64ex) manualmente
- Opcional, para enviar [comandos](/tutorial/Archipelago/commands/en) como `!hint`: el TextClient de [la versión más reciente de Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases)

NOTA: El launcher enlazado arriba es una versión especial diseñada para funcionar con la versión Archipelago de sm64ex.
Se pueden utilizar otras versiones basadas en el sm64-port con él, pero no se puede utilizar un launcher diferente con 
la versión Archipelago de sm64ex.

## Procedimientos de instalación e inicio del juego

### Instalación mediante SM64AP-Launcher

### Preparativos para Windows

Primero, instala [MSYS](https://www.msys2.org/) como se describe en la página. NO DEBE INSTALARSE EN UNA RUTA DE 
CARPETA CON ESPACIOS.
Se recomienda encarecidamente utilizar el directorio de instalación predeterminado.
Luego continúa con `Usando el Launcher`.

*Preparativos para Linux*

Necesitarás instalar algunas dependencias antes de usar el launcher.
El launcher necesita `qt6`, `patch` y `git`, y compilar el juego requiere `sdl2 glew cmake python make` (Si instalas 
`jsoncpp` también, se enlazará dinámicamente).
Luego continúa con `Usando el Launcher`.

*Usando el launcher*
1. Ve a la página vinculada a SM64AP-Launcher y selecciona la última versión lanzada.
2. Desliza hacia abajo, y descarga el archivo zip para tu sistema operativo.
3. Descomprime el archivo zip en una carpeta vacía.
4. Ejecuta el Launcher. En el primer inicio, haz click en el botón `Register SM64 Rom` para seleccionar tu ROM de SM64,
seguido de `Check Requirements`, que te guiará por el resto de pasos necesarios.
    - Windows: Si no ha utilizado el directorio de instalación por defecto para MSYS, cierre esta ventana, marque 
    `Show advanced options` y vuelva a abrirla utilizando `Re-check Requirements`. A continuación podrá establecer la 
    ruta manualmente.
5. Cuando termine, haz click en el botón `Compile default SM64AP build` para continuar.
    - Configuración avanzada:** Si quieres usar opciones adicionales de compilación como Mejor Cámara, Sin Distancia de
    Dibujo, etc. o aplicar parches del juego como 60FPS, Movimientos Mejorados, etc., usa la opción `Compile custom build`:
      - Ponle un nombre a tu build, por ejemplo «archipiélago» o el que quieras.
      - Pulsa el botón `Download Files`.
      - Establezce las banderas de configuración en `Make Flags`, por ejemplo `-j8 BETTERCAMERA=1 NODRAWINGDISTANCE=1` 
      para activar Better Camera y No Drawing Distance.
      - Haz click en `Apply Patches` para seleccionar los parches a aplicar. Algunos ejemplos de parches son:
        - 60FPS: Mejora la velocidad de fotogramas.
        - Extended Moveset: Proporciona nuevas habilidades a Mario. [Más detalles aquí](https://github.com/TheGag96/sm64-port).
        - Modo NonStop: Permite conseguir varias estrellas en un nivel sin salir de él.
      - Pulsa `Create Build`. Esto llevará varios minutos.
      - También puedes utilizar los campos `Repository` y `Branch` para compilar con diferentes repositorios o ramas si
      deseas compilar utilizando una versión fork o de desarrollo del SM64AP.
      - Para más detalles, consulte:
        - [Makeflags disponibles](https://github.com/sm64pc/sm64ex/wiki/Build-options)
        - [Parches de Juego Incluidos](https://github.com/N00byKing/sm64ex/blob/archipelago/enhancements/README.md)
6. Pulse `Download Files` para preparar la compilación, después `Create Build`.
7. Ahora se compilará SM64EX. Esto puede llevar un rato.

Cuando termine, la lista de compilación debería tener otra entrada con el nombre que le haya dado.

NOTA: Si no se inicia al pulsar `Play selected build`, vuelve a comprobar si ha escrito correctamente las opciones de 
lanzamiento (Descritas en `Unirse a un juego MultiWorld`)

### Compilación Manual (Linux/Windows)

*Preparacion en Windows*

Primero, instala [MSYS](https://www.msys2.org/) como se describe en la página. NO DEBE INSTALARSE EN UNA RUTA DE 
CARPETA CON ESPACIOS.

Después de iniciar msys2 utilizando un intérprete de comandos MinGW x64 (debería haber una en el menú de inicio), 
actualice introduciendo `pacman -Syuu` en el símbolo del sistema. A continuación, instala las dependencias relevantes 
introduciendo `pacman -S unzip mingw-w64-x86_64-gcc mingw-w64-x86_64-glew mingw-w64-x86_64-SDL2 git make python3 mingw-w64-x86_64-cmake`.

Continúe con `Compilando`.

*Preparativos para Linux*

Instala las dependencias relevantes `sdl2 glew cmake python make patch git`. SM64EX enlazará `jsoncpp` dinámicamente si
está instalado. Si no, compilará y enlazará estáticamente.

Continúe con `Compilando`.

*Compilando*

Consigue el código fuente clonando el repositorio correspondiente mediante `git clone --recursive https://github.com/N00byKing/sm64ex`.
Copia tu ROM legalmente volcada en la carpeta sm64ex (si no está seguro de dónde se encuentra la carpeta, haz una
búsqueda rápida en Windows de sm64ex). El nombre de la ROM debe ser `baserom.REGION.z64` donde `REGION` es `us` o `jp`
respectivamente.

Una vez realizados todos estos pasos preparatorios, escribe `cd sm64ex && make` en el símbolo del sistema y prepárate 
para esperar un poco. Si deseas acelerar la compilación, ingresa en el compilador cuántos núcleos de CPU debe utilizar 
usando el comando `cd sm64ex && make -jn` en su lugar, donde n es el número de núcleos que deseas usar.

Después de que la compilación haya tenido éxito, habrá un binario en la carpeta `sm64ex/build/REGION_pc/`.

### Unirse a una partida MultiWorld

Para unirse, configure las siguientes opciones de lanzamiento: `--sm64ap_name TuNombre --sm64ap_ip ServerIP:Port`.
Por ejemplo, si estás alojando una partida usando la página web, `TuNombre` será el nombre de la página de opciones, 
`ServerIP` es `archipelago.gg` y `Port` el puerto dado en la página de la sala Archipelago.
Opcionalmente, añade `--sm64ap_passwd «TuContraseña»` si la sala que estás utilizando requiere una contraseña.
Si tu nombre o contraseña tienen espacios, enciérrelos entre comillas: `"Tu Contraseña"` y `"Tu Nombre"`.
Como nota adicional puedes usar `--skip-intro` para saltar la cinemática del inicio del juego para directamente tener 
el control de Mario

Si la conexión falla (por ejemplo, al utilizar un nombre o una combinación IP/Puerto incorrectos), el juego te 
informará de ello.
Además, cada vez que el juego no esté conectado (por ejemplo cuando la conexión es inestable) intentará reconectarse y 
mostrará un texto de estado.

### Jugar sin conexión

Para jugar sin conexión, primero genera una semilla en la página de opciones del juego.
Crea una sala y descarga el archivo `.apsm64ex`, e inicia el juego con el argumento de arranque `--sm64ap_file "path/to/FileName"`.

### Opcional: Usar archivos por lotes para jugar partidas offline y MultiWorld

Como alternativa al ejecutar el juego con SM64AP-Launcher, también es posible lanzar la versión completa utilizando 
archivos por lotes de Windows. Esto tiene la ventaja añadida de agilizar el proceso de unión de modo que no es 
necesario editar manualmente la información de conexión para cada nueva partida. Sin embargo, necesitarás sentirte 
cómodo con la creación y el uso de archivos por lotes.

NOTA IMPORTANTE: El resto de esta sección utiliza código de copiar y pegar que asume que estás utilizando la versión 
Americana del juego. Si por el contrario utiliza la versión Japonesa, deberá editar el nombre del EXE cambiando 
"sm64.us.f3dex2e.exe" por "sm64.jp.f3dex2e.exe".

### Creación de un archivo offline.bat para lanzar archivos de parche offline

Abre el Bloc de notas (o el editor de texto de tu conveniencia). Pega el siguiente texto: `start sm64.us.f3dex2e.exe --sm64ap_file %1`

Ve a Archivo > Guardar como...

Ve a la carpeta que seleccionó para la compilación de SM64 cuando seguiste la guía de compilación de SM64AP-Launcher. 
Una vez allí, navega hasta `build` y luego hasta `us_pc`. Esta carpeta debería ser la misma en la que se encuentra `sm64.us.f3dex2e.exe`.

Escribe el nombre del archivo `"offline.bat"`. ¡LAS COMILLAS SON IMPORTANTES! De lo contrario, creará un archivo de 
texto ("offline.bat.txt"), que no funcionará como archivo por lotes.

Ahora deberías tener un archivo llamado `offline.bat` con el icono de un engranaje en la misma carpeta que tu 
`sm64.us.f3dex2e.exe`. Haz clic con el botón derecho en `offline.bat` y elige `Enviar a > Escritorio (Crear acceso directo)`.
- Si el icono de este archivo es un bloc de notas en lugar de un engranaje, es que lo has guardado como archivo .txt 
por accidente. Para solucionarlo, cambia la extensión del archivo a .bat.

A partir de ahora, siempre que inicies una partida para un jugador sin conexión, descarga el archivo de parche 
`.apsm64ex` del Generador y arrástralo y suéltalo en `offline.bat` para abrir la partida y empezar a jugar.

NOTA: Cuando juegues con archivos de parche offline, se creará un archivo `.save` en el mismo directorio que el archivo
de parche, que contendrá tus datos de guardado para esa semilla. No lo borres hasta que hayas terminado con esa semilla.

### Hacer un online.bat para lanzar partidas MultiWorld online

Estos pasos son muy similares. Crearás un archivo por lotes en la misma ubicación que antes. Sin embargo, el texto que 
pones en este archivo por lotes es diferente, y no arrastrarás archivos de parches en él.

Sigue los mismos pasos que antes para abrir el Bloc de notas (o el editor de texto de tu conveniencia) y pegar 
lo siguiente:

`set /p port="Introduce el número de puerto de la sala - "`

`set /p slot="Introduce tu nombre de jugador - "`

`start sm64.us.f3dex2e.exe --sm64ap_name «%slot%» --sm64ap_ip archipelago.gg:%port%`

Guarda este archivo como `"online.bat"` y, a continuación, crea un acceso directo siguiendo los mismos pasos que antes.

Para utilizar este archivo por lotes, haz doble clic en él. Se abrirá una ventana. Escribe el número de puerto de cinco
dígitos de la sala a la que deseas unirte y, a continuación, escribe tu nombre de jugador.
- El número de puerto aparece en la página de la sala. El anfitrión del juego debe compartir esta página con 
  todos los jugadores.
- El nombre del espacio es el que hayas escrito en el campo "Name" al crear un archivo de configuración. Todos los
  nombres de jugador son visibles en la página de la sala.

Una vez que proporciones estos dos datos, el juego se abrirá.
- Si el juego sólo dice `Connecting`, inténtalo de nuevo. Comprueba dos veces el número de puerto y el nombre de
jugador; incluso un solo error tipográfico hará que tu conexión falle.

## Solución de problemas de instalación

Inicia el juego desde la línea de comandos para ver mensajes útiles sobre SM64EX.

### El juego no se inicia después de compilar

Lo más probable es que hayas olvidado configurar las opciones de inicio. `--sm64ap_name TuNombre` y 
`--sm64ap_ip ServerIP:Port` son necesarios para el inicio para MultiWorlds, y
`--sm64ap_file FileName` es necesario para (offline) singleplayer.
Si tu Nombre o Contraseña tienen espacios, ponlos entre comillas.

### El juego se bloquea al entrar en el Castillo de Peach

Esto ocurre cuando al juego le faltan los datos relevantes del randomizador. Si estás intentando conectarte a un 
servidor, verifica que la información introducida es correcta, y para un archivo local asegúrate de que estás usando la
ruta completa al archivo en conjunción con su nombre.

## Solución de problemas del juego

### Problemas conocidos

Cuando se utiliza una Rom Americana, en los mensajes del juego faltan algunas letras: `J Q V X Z` y `?`.
La versión japonesa no debería tener problemas para mostrarlos.

### Toad no tiene un item para mi.

Esto ocurre en versiones anteriores cuando se carga un archivo existente que ya había recibido un elemento de ese Toad.
Para resolver esto, sal y comienza desde un archivo `NEW`. El servidor restaurará automáticamente tu progreso.
Alternativamente, actualizando tu compilación evitará este problema en el futuro.

### ¿Qué ocurre si pierdo la conexión?

SM64EX intenta reconectar unas cuantas veces, así que sé paciente.
Si el problema persiste después de uno o dos minutos, simplemente guarda y reinicia el juego.

### ¿Cómo actualizo el juego a una nueva versión?

Cuando uses el Launcher, sigue los pasos normales, pero cuando elijas el nombre de la carpeta, usa el mismo que antes.
El Launcher lo reconocerá y ofrecerá reemplazarlo.
Cuando compiles manualmente, simplemente introduce los cambios y ejecuta `make` de nuevo. A veces ayuda
ejecutar `make clean` antes.