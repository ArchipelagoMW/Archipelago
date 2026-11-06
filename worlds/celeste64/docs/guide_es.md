# Celeste 64 Guía de Instalación

## Programas Necesarios
- Compilación de Celeste 64 para Archípelago de la: [Repositorio de GitHub de Celeste 64 para Archipelago](https://github.com/PoryGoneDev/Celeste64/releases/)

## Programas Opcionales
- Tracker de Celeste 64
	- PopTracker desde el: [Repositorio de GitHub de PopTracker](https://github.com/black-sliver/PopTracker/releases/)
	- Paquete de Celeste 64 para Archipelago PopTracker desde el: [Repositorio de GitHub de Celeste 64 AP Tracker](https://github.com/PoryGone/Celeste-64-AP-Tracker/releases/)

## Pasos para la instalación (Windows)

1. Descarga el repositorio puesto arriba y extrae sus archivos.

## Pasos para la instalación (Linux y Steam Deck)

1. Descarga el repositorio puesto arriba y extrae sus archivos.

2. Agrega el archivo Celeste64.exe a Steam como un Juego Externo. En las propiedades del juego en Steam, configúralo para que utilice Proton como herramienta de compatibilidad. Inicia el juego a través de Steam para ejecutarlo.

## Unirte a una partida MultiWorld

1. Antes de iniciar el juego, edita el archivo `AP.json` en la raíz de la instalación de Celeste 64.

2. En el campo `Url`, ingresa la dirección del servidor, por ejemplo: `archipelago.gg:38281`. El administrador de la partida debería indicar esta información.

3. En el campo `SlotName` escribe el nombre (campo "name") que pusiste en tu archivo YAML o en tu configuración Web

4. En el campo `Password` escribe la contraseña del servidor si es que la partida tiene una; si no es así, deja el campo en blanco ""

5. Guarda el archivo `AP.json`, y ejecuta el archivo `Celeste64.exe`. Si puedes pasar de la pnatalla del título, significa que te has conectado sin problemas.

Ejemplo de un archivo `AP.json` con info de una partida:

```
{
	"Url": "archipelago.gg:12345",
	"SlotName": "Maddy",
	"Password": ""
}
```
