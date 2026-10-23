# Guia para Ejecutar Archipelago desde Código Fuente en macOS
Archipelago no tiene una versión compilada en macOS. Aún así, se puede ejecutar desde código fuente en macOS. Esta guia espera que tengas algo de experiencia ejecutando software desde la terminal.
## Software Necesario
Aquí hay una lista del software a instalar y el código fuente para descargar.
1. Python 3.11.9 "universal2" o más reciente de la <a href="https://www.python.org/downloads/macos/">[página de descargas de Python para macOS](https://www.python.org/downloads/macos/).
**Python 3.14 no tiene soporte todavía.**
2. Xcode de la [App Store de macOS](https://apps.apple.com/us/app/xcode/id497799835).
3. El código fuente del [Github de Archipelago]("https://github.com/ArchipelagoMW/Archipelago/releases).
4. El asset con darwin en el nombre de la [página de Github de SNI](https://github.com/alttpo/sni/releases).
5. Si quieres generar seeds de los enemigos para ALTTP de manera local (no en la página web), quizá necesites el EnemizerCLI de su [página de Github](https://github.com/Ijwu/Enemizer/releases).
6. Un Emulador de tu elección para juegos que necesitan un emulador. Para juegos de SNES, yo recomiendo RetroArch, solo porque fue el más fácil de configurar en macOS. Puede descargarse en la [página de descargas de RetroArch](https://www.retroarch.com/?page=platforms).
## Extraer el Directorio de Archipelago
1. Doble click en el archivo .zip del código fuente de Archipelago para extraer los archivos en un directorio de Archipelago.
2. Mueve el directorio de Archipelago fuera del de descargas.
3. Abre el terminal y colócate en el directorio de Archipelago.
## Configurar un Ecosistema Virtual
Por lo general, es recomendable que uses un ecosistema virtual para ejecutar software basado en python para evitar contaminación que pueda romper software. Si Archipelago es lo único que usa python en tu ordenador, no es necesario usar un ecosistema virtual.
1. Abre el terminal y ve al directorio de Archipelago. También puedes hacerlo haciendo click derecho en la carpeta de Archipelago en Finder y seleccionando 'Nuevo terminal en carpeta'.
2. Ejecuta `python3 -m venv venv` para crear un ecosistema virtual. Ejecutar este comando creará un nuevo directorio en el camino especificado, así que asegúrate que ese camino está limpio para que se cree el nuevo directorio.
3. Ejecuta `source venv/bin/activate` para activar el ecosistema virtual.
4. Si quieres salir del ecosistema virtual, ejecuta `deactivate`.
## Crear la App
1. Ejecuta `python3 setup.py bdist_mac` para crear un Paquete de Aplicación. Este paso puede tomar un tiempo.
2. En Finder, ve al nuevo subdirectorio `build`, y copia la app de Archipelago que acabas de crear a tu directorio de Aplicaciones.
## Pasos para Ejecutar los Clientes
1. Ejecuta el Launcher de Archipelago.
2. Si tu juego no tiene un parche, clica en el cliente deseado de la columna de la derecha.
3. Si tu juego tiene un parche, clica en 'Open Patch' y ve a tu parche (la extensión del archivo será parecida a apsm, aplttp, apsmz3, etc.).
4. Si el proceso de parcheo necesita una rom, pero no puede encontrarla, te pedirá que le digas donde está tu rom obtenida legalmente.
5. Tu cliente debería de funcionar y tu rom debería estar creada (cuándo aplicable).
## Pasos Extra para Juegos de SNES
1. Si estás usando RetroArch, las instrucciones para poner a funcionar el emulador [están en la guía de configuración de a Link to the Past](/tutorial/A%20Link%20to%20the%20Past/multiworld/en), también funcionan en la versión de macOS de RetroArch.
2. Doble click en la descarga del tar.gz del SNI para extraer los archivos a un directorio de SNI. Sino tiene el nombre 'SNI' renómbralo para facilitar los siguientes pasos.
3. Mueve el directorio de SNI fuera de descargas, preferiblemente al directorio de Archipelago creado antes.
4. Si el directorio de SNI tiene el nombre correcto y se ha movido al directorio de Archipelago, debería ejecutarse automáticamente con el cliente SNI. Sino se ejecuta automáticamente, abre el directorio de SNI y ejecuta el archivo ejecutable de SNI manualmente.
5. Si estás usando EnemizerCLI, extrae el directorio descargado y renómbralo a EnemizerCLI.
6. Mueve el directorio EnemizerCLI al directorio de Archipelago para que Generate.py pueda usarlo.
7. Ahora que SNI, el cliente, y el emulador están funcionando, todo debería estar listo.