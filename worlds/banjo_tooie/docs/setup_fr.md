
# GUIDE D'INSTALLATION POUR LE RANDOMISEUR ARCHIPELAGO DE BANJO-TOOIE

## Important

Puisque nous utilisons BizHawk, le randomiseur est seulement supporté sur Windows et Linux.
Le randomiseur supporte l'Everdrive 3.0 et X7.

## Logiciels et fichiers requis

-   Emulation sur PC:
    -   BizHawk:  [Les versions de BizHawk (TASVideos)](https://tasvideos.org/BizHawk/ReleaseHistory)
        -   La version <b>2.9.1</b> est présentement supportée, ne le sera plus bientôt.
        -   La version <b>2.10</b> et les versions plus récentes sont supportées.
        -   Les instructions d'installation de BizHawk sont incluses dans le lien.
        -   Sur Windows, il faut installer les pré-requis avant d'installer BizHawk. Vous pouvez les trouver dans le lien.
-   Everdrive:
    - Installer le pilote USB sur le PC, pour la connexion à l'Everdrive
        - Windows: https://ftdichip.com/wp-content/uploads/2021/08/CDM212364_Setup.zip
        - Linux: https://ftdichip.com/wp-content/uploads/2022/07/libftd2xx-x86_64-1.4.27.tgz
    - Pour l'Everdrive 3.0, le système d'exploitation doit être 3.06 pour fonctionner
    - Le Nintendo 64 Expansion Pak est requis
    -   Télécharger la version la plus récente du connecteur pour Everdrive: https://github.com/jjjj12212/AP_Banjo-Tooie/releases
-   Une ROM de la version Nord-Américaine de Banjo-Tooie.

## Jouer sur BizHawk
### Configuration de BizHawk

Une fois que BizHawk a été installé, lancer EmuHawk et changer les options suivantes:
-   Sous Config -> Customize, activer "Run in background" et "Accept background input". Cela va vous permettre de jouer, même si une autre fenêtre est selectionnée.
-   Sous Config > Hotkeys, plusieurs raccourcis clavier sont liés à des touches de clavier fréquemment utilisées. Il est recommender d'en désactiver la majorité, qui peut être fait rapidement avec `Esc`.
-   Si vous jouer avec une manette, quand vous choisissez vos contrôles, désactiver "P1 A Up", "P1 A Down", "P1 A Left", and "P1 A Right", et plutôt utiliser les options de l'onglet `Analog` pour configurer les contrôles du joystick
-   Sous N64, activer `Use Expansion Slot`. Cet option est seulement accessible après avoir chargé une ROM.
-   Sous Config -> Speed/Skip, activer "Audio Throttle". Ceci corrige les bugs sonores pendant le jeu.

Il est fortement recommendé d'associer les fichiers de ROM N64 (*.n64, *.z64) avec BizHawk, pour un démarrage plus rapide. Pour se faire, faire un clic droit sur un fichier de ROM N64, cliquer sur "Ouvrir avec...", "Plus d'applications" et "Rechercher plus d'applications sur ce PC". Avec l'explorateur de fichiers, sélectionner EmuHawk.exe dans le dossier BizHawk.

Si vous rencontrez des problèmes de performance, vous pouvez essayer ceci:
- Sous N64 -> Plugins, régler `Active video Plugin` à Rice.
Ceci causera des bugs d'affichage mineurs pendant le jeu, mais ne devrait pas causer des impacts majeurs

### Démarrage - BizHawk

- Lancer le Archipelago Launcher et sélectionner le client de Banjo-Tooie, dans la colonne de droite
- Si c'est la première fois que vous ouvrez le client de Banjo-Tooie (ou si vous changez de version), il va vous demander la ROM de Banjo-Tooie. La ROM sera ensuite patchée, et le client vous indiquera où trouver la ROM à utiliser.
- Connecter le client de Banjo-Tooie au serveur, en saisissant l'adresse du serveur et le port dans le champs en haut du client.
- Ouvrir BizHawk, et lancer la ROM patchée.
- Dans BizHawk, cliquer sur Tools, suivi de Lua Console. De là, vous pouvez glisser-déposer banjo_tooie_connector.lua (situé dans le dossier data/lua du dossier d'Archipelago) dans la fenêtre de la Lua console.

## Jouer sur Everdrive
- Lancer le Archipelago Launcher et sélectionner le client de Banjo-Tooie, dans la colonne de droite
- Si c'est la première fois que vous ouvrez le client de Banjo-Tooie, ou si vous changez de version:
  - Le client de Banjo-Tooie va vous demander la ROM de Banjo-Tooie. La ROM sera ensuite patchée, et le client vous indiquera où trouver la ROM à utiliser.
  - Copier la ROM patch sur la carte SD utilisée pour l'Everdrive
- Brancher un câble USB entre l'Everdrive et l'ordinateur
- Lancer banjo_tooie_everdrive_connector.exe sur l'ordinateur
  - Note 1: cette étape doit être faite avant de connecter le client Banjo-Tooie au serveur
  - Note 2: Si vous utilisez Linux, utilisez plutôt Banjo_Tooie_everdrive_connector_linux.exe
- Lancer la ROM sur l'Everdrive
- Connecter le client de Banjo-Tooie au serveur, en saisissant l'sdresse du serveur et le port dans le champs en haut du client.
