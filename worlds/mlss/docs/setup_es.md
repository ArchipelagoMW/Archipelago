# Guía de instalación de Mario & Luigi: Superstar Saga Archipelago

## Importante

Como estamos usando Bizhawk, esta guía sólo es aplicable a sistemas Windows y Linux.

## Software necesario

- Bizhawk: [Lanzamientos Bizhawk por TASVideos](https://tasvideos.org/BizHawk/ReleaseHistory)
  - Se recomienda la versión 2.9.1.
  - Las instrucciones detalladas de instalación de Bizhawk se pueden encontrar en el enlace anterior.
  - Los usuarios de Windows deben ejecutar primero el instalador de requisitos previos, que también se puede encontrar en el enlace anterior.
- El cliente Bizhawk integrado, que puede instalarse [aquí](https://github.com/ArchipelagoMW/Archipelago/releases)
- Una copia americana de Mario & Luigi: Superstar Saga

## Software opcional

- [Poptracker](https://github.com/black-sliver/PopTracker/releases)
  - [MLSS Autotracker](https://github.com/seto10987/MLSS-PopTracker/releases)

## Configuración de su archivo YAML

### ¿Qué es un archivo YAML y por qué necesito uno?

Tu archivo YAML contiene un conjunto de opciones de configuración que proporcionan al generador información sobre cómo debe generar tu juego. Cada jugador de un multiworld proporcionará su propio archivo YAML. Esta configuración permite a cada jugador disfrutar
de una experiencia personalizada a su gusto, y distintos jugadores de un mismo multiworld pueden tener opciones diferentes.

### ¿Dónde consigo un archivo YAML?

Puedes personalizar tus opciones visitando 
[Mario & Luigi Superstar Saga Options Page](/games/Mario%20&%20Luigi%20Superstar%20Saga/player-options)

## Unirse a una partida MultiWorld

### Obtén tu archivo para parchear el juego de GBA

Cuando te unas a una partida multiworld, se te pedirá que proporciones tu archivo YAML a quien sea el anfitrión. Una vez hecho esto, el anfitrión te proporcionará o bien un enlace para descargar tu archivo parche, o bien un archivo zip que contiene los archivos de datos de todos. Tu archivo de datos debe tener la extensión `.apmlss`.

Haz doble clic en su archivo `.apmlss` para iniciar el cliente se aplique el parche automaticamente al ROM. Una vez finalizado el proceso, el cliente y el emulador se iniciarán automáticamente (si has asociado la extensión al emulador como se recomienda).

### Conectarse al Multiservidor

Una vez iniciados tanto el cliente como el emulador, debes conectarlos. Dentro del emulador haz clic en el menú "Herramientas" y selecciona "Consola Lua". Haz clic en el botón de carpeta o pulsa Ctrl+O para abrir un script Lua.

Navega a tu carpeta de instalación de Archipelago y abre `data/lua/connector_bizhawk_generic.lua`.

Para conectar el cliente al multiservidor simplemente pon `<dirección>:<puerto>` en el campo de texto de la parte superior y pulsa enter (si el servidor usa contraseña, escribe en el campo de texto inferior `/connect <dirección>:<puerto> [contraseña]`)