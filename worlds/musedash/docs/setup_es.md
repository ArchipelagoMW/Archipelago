# Guía de instalación para Muse Dash: Archipelago

## Enlaces rápidos
- [Página Principal](../../../../games/Muse%20Dash/info/en)
- [Página de Configuraciones](../../../../games/Muse%20Dash/player-settings)

## Software Requerido

- Windows 8 o más reciente.
- Muse Dash: [Disponible en Steam](https://store.steampowered.com/app/774171/Muse_Dash/)
  - \[Opcional\] [Muse Plus] DLC: [tambien disponible on Steam](https://store.steampowered.com/app/2593750/Muse_Dash__Muse_Plus/)
- Melon Loader: [GitHub](https://github.com/LavaGang/MelonLoader/releases/latest)
  - .Net Framework 4.8 podría ser necesario para el instalador: [Descarga](https://dotnet.microsoft.com/es-es/download/dotnet-framework/net48)
- Entorno de ejecución de escritorio de .NET 6.0.XX (si aún no está instalado): [Descarga](https://dotnet.microsoft.com/es-es/download/dotnet/6.0)
- Muse Dash Archipelago Mod: [GitHub](https://github.com/DeamonHunter/ArchipelagoMuseDash/releases/latest)

## Instalar el mod de Archipelago en Muse Dash

1. Descarga [MelonLoader.Installer.exe](https://github.com/LavaGang/MelonLoader/releases/latest) y ejecutalo.
2. Elije la pestaña "automated", haz clic en el botón "select" y busca tu `MuseDash.exe`. Luego haz clic en "install".
  - Puedes encontrar la carpeta en Steam buscando el juego en tu biblioteca, haciendo clic derecho sobre el y elegir *Administrar→Ver archivos locales*.
  - Si haces clic en la barra superior que te indica la carpeta en la que estas, te dará la dirección de ésta para que puedas copiarla. Al pegar esa dirección en la ventana que **MelonLoader** abre, irá automaticamente a esa carpeta.
3. Ejecuta el juego una vez, y espera hasta que aparezca la pantalla de inicio de Muse Dash antes de cerrarlo.
4. Descarga la última version de [Muse Dash Archipelago Mod](https://github.com/DeamonHunter/ArchipelagoMuseDash/releases/latest) y extraelo en la nueva carpeta creada llamada `/Mods/`, localizada en la carpeta de instalación de Muse Dash.
  - Todos los archivos deben ir directamente en la carpeta `/Mods/`, y NO en una subcarpeta dentro de la carpeta `/Mods/`

Si todo fue instalado correctamente, un botón aparecerá en la parte inferior derecha del juego una vez abierto, que te permitirá conectarte al servidor de Archipelago.

## Generar un juego MultiWorld
1. Entra a la página de [configuraciones de jugador](/games/Muse%20Dash/player-settings) y configura las opciones del juego a tu gusto.
2. Genera tu archivo YAML y úsalo para generar un juego nuevo en el radomizer
  - (Instrucciones sobre como generar un juego en Archipelago disponibles en la [guía web de Archipelago en Inglés](/tutorial/Archipelago/setup/en))

## Unirse a un juego MultiWorld

1. Ejecuta Muse Dash y pasa por la pantalla de introducción. Haz clic en el botón de la esquina inferior derecha.
2. Ingresa los detalles de la sesión de archipelago, como la dirección del servidor con el puerto (por ejemplo, archipelago.gg:38381), nombre de usuario y contraseña.
3. Si todo se ingresó correctamente, el pop-up debería desaparecer y se mostrará el menú principal habitual. Al ingresar a la selección de canciones, deberías ver una cantidad limitada de canciones.

## Solución de problemas

### No Support Module Loaded

Este error ocurre cuando Melon Loader no puede encontrar los archivos necesarios para ejecutar mods. Generalmente, hay dos razones principales de este error: una falla al generar los archivos cuando el juego se ejecutó por primera vez con Melon Loader, o un antivirus que elimina los archivos después de la generación.

Para solucionar este problema, primero debes eliminar Melon Loader de Muse Dash. Puedes hacer esto eliminando la carpeta Melon Loader dentro de la carpeta de Muse Dash. Luego, seguir los pasos de instalación nuevamente.

Si continúas teniendo problemas y estás utilizando un antivirus, es posible que tengas que desactivarlo temporalmente cuando se ejecute Muse Dash por primera vez, o excluir la carpeta Muse Dash de ser escaneada.
