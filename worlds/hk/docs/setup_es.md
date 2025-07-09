# Hollow Knight Archipelago

## Software requerido
* Descarga y descomprime Lumafly Mod manager desde el [sitio web de Lumafly](https://themulhima.github.io/Lumafly/)
* Tener una copia legal de Hollow Knight.
    * Las versiones de Steam, GOG y Xbox Game Pass son compatibles
    * Las versiones de Windows, Mac y Linux (Incluyendo Steam Deck) son compatibles

## Instalación del mod de Archipelago con Lumafly
1. Ejecuta Lumafly y asegurate de localizar la carpeta de instalación de Hollow Knight
2. Instala el mod de Archipiélago haciendo click en cualquiera de los siguientes:
    * Haz clic en uno de los enlaces de abajo para permitir Lumafly para instalar los mods. Lumafly pedirá 
      confirmación.
        * [Archipiélago y dependencias solamente](https://themulhima.github.io/Lumafly/commands/download/?mods=Archipelago)
        * [Archipelago con rando essentials](https://themulhima.github.io/Lumafly/commands/download/?mods=Archipelago/Archipelago%20Map%20Mod/RecentItemsDisplay/DebugMod/RandoStats/Additional%20Timelines/CompassAlwaysOn/AdditionalMaps/)
          (incluye Archipelago Map Mod, RecentItemsDisplay, DebugMod, RandoStats, AdditionalTimelines, CompassAlwaysOn,
          y AdditionalMaps).
    * Haz clic en el botón "Instalar" situado junto a la entrada del mod "Archipiélago". Si lo deseas, instala también 
      "Archipelago Map Mod" para utilizarlo como rastreador en el juego.
      Si lo requieres (Y recomiendo hacerlo) busca e instala Archipelago Map Mod para usar un tracker in-game
3. Ejecuta el juego desde el apartado de inicio haciendo click en el botón Launch with Mods

## Que hago si Lumafly no encontro la ruta de instalación de mi juego?
1. Busca el directorio manualmente
    * En Xbox Game pass:
        1. Entra a la Xbox App y dirigete sobre el icono de Hollow Knight que esta a la izquierda.
        2. Haz click en los 3 puntitos y elige el apartado Administrar
        3. Dirigete al apartado Archivos Locales y haz click en Buscar
        4. Abre en Hollow Knight, luego Content y copia la ruta de archivos que esta en la barra de navegación.
    * En Steam:
        1. Si instalaste Hollow Knight en algún otro disco que no sea el predeterminado, ya sabrás donde se encuentra 
           el juego, ve a esa carpeta, abrela y copia la ruta de archivos que se encuentra en la barra de navegación.
            * En Windows, la ruta predeterminada suele ser:`C:\Program Files (x86)\Steam\steamapps\common\Hollow Knight`
            * En linux/Steam Deck suele ser: ~/.local/share/Steam/steamapps/common/Hollow Knight
            * En Mac suele ser: ~/Library/Application Support/Steam/steamapps/common/Hollow Knight/hollow_knight.app
2. Ejecuta Lumafly como administrador y, cuando te pregunte por la ruta de instalación, pega la ruta que copeaste 
   anteriormente.

## Configuración de tu fichero YAML
### ¿Qué es un YAML y por qué necesito uno?
Un archivo YAML es la forma en la que proporcionas tus opciones de jugador a Archipelago.
Mira la [guía básica de configuración multiworld](/tutorial/Archipelago/setup/en) aquí en la web de Archipelago para 
aprender más, (solo se encuentra en Inglés).

### ¿Dónde consigo un YAML?
Puedes usar la [página de opciones de juego para Hollow Knight](/games/Hollow%20Knight/player-options) aquí en la web 
de Archipelago para generar un YAML usando una interfaz gráfica.

## Unete a una partida de Archipelago en Hollow Knight
1. Inicia el juego con los mods necesarios indicados anteriormente.
2. Crea una **nueva partida.**
3. Elige el modo **Archipelago** en la selección de modos de partida.
4. Introduce la configuración correcta para tu servidor de Archipelago.
5. Pulsa **Iniciar** para iniciar la partida. El juego se quedará con la pantalla en negro unos segundos mientras 
   coloca todos los objetos.
6. El juego debera comenzar y ya estaras dentro del servidor.
    * Si estas esperando a que termine un contador/timer, procura presionar el boton Start cuando el contador/timer 
      termine.
    * Otra manera es pausar el juego y esperar a que el contador/timer termine cuando ingreses a la partida.

## Consejos y otros comandos
Mientras juegas en un multiworld, puedes interactuar con el servidor usando varios comandos listados en la 
[guía de comandos](/tutorial/Archipelago/commands/en). Puedes usar el Cliente de Texto Archipelago para hacer esto,
que está incluido en la última versión del [software de Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases/latest).