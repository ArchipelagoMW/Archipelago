# Guide d'installation pour le randomiseur Archipelago de Banjo-Tooie

## Important

Puisque nous utilisons BizHawk, le randomiseur est seulement supporté sur Windows et Linux.
Le randomiseur supporte l'Everdrive 3.0 et X7.

## Logiciels et fichiers requis

-   Emulation sur PC:
    -   BizHawk:  [Les versions de BizHawk (TASVideos)](https://tasvideos.org/BizHawk/ReleaseHistory)
        -   La version `2.10` et les versions plus récentes sont supportées.
        -   Les instructions d'installation de BizHawk sont incluses dans le lien.
        -   Sur Windows, il faut installer les pré-requis avant d'installer BizHawk. Vous pouvez les trouver dans le lien.
-   Everdrive:
    - Installez le pilote USB sur le PC, pour la connexion à l'Everdrive
        - Windows: https://ftdichip.com/wp-content/uploads/2021/08/CDM212364_Setup.zip
        - Linux: https://ftdichip.com/wp-content/uploads/2022/07/libftd2xx-x86_64-1.4.27.tgz
    - Pour l'Everdrive 3.0, le système d'exploitation doit être 3.06 pour fonctionner
    - Le Nintendo 64 Expansion Pak est requis
    -   Téléchargez la version la plus récente du connecteur pour Everdrive: https://github.com/jjjj12212/AP_Banjo-Tooie/releases
-   Une ROM de la version Nord-Américaine de Banjo-Tooie.

## Jouer sur BizHawk
### Configuration de BizHawk

Une fois que BizHawk a été installé, lancez EmuHawk et changez les options suivantes:
-   Sous Config -> Customize, activez "Run in background" et "Accept background input". Cela vous permettra de jouer même si une autre fenêtre est selectionnée.
-   Sous Config > Hotkeys, plusieurs raccourcis clavier sont liés à des touches de clavier fréquemment utilisées. Il est recommandé d'en désactiver la majorité, ce qui est faisable rapidement avec la touche `Esc`.
-   Si vous jouez avec une manette, quand vous choisissez vos contrôles, désactivez "P1 A Up", "P1 A Down", "P1 A Left", and "P1 A Right", et utilisez plutôt les options de l'onglet `Analog` pour configurer les contrôles du joystick.
-   Sous N64, activez `Use Expansion Slot`. Cette option est seulement accessible après avoir chargé une ROM.
-   Sous Config -> Speed/Skip, activez "Audio Throttle". Ceci corrige les bugs sonores pendant le jeu.

Il est fortement recommandé d'associer les fichiers de ROM N64 (*.n64, *.z64) avec BizHawk, pour un démarrage plus rapide. Pour ce faire, faites un clic droit sur un fichier de ROM N64, cliquez sur "Ouvrir avec...", "Plus d'applications" et "Rechercher plus d'applications sur ce PC". Avec l'explorateur de fichiers, sélectionnez EmuHawk.exe dans le dossier BizHawk.

Si vous rencontrez des problèmes de performance, vous pouvez essayer ceci:
- Sous N64 -> Plugins, régler `Active video Plugin` à Rice.
Ceci causera des bugs d'affichage mineurs pendant le jeu, mais ne devrait pas avoir d'impact majeur.

### Démarrage - BizHawk

- Lancez l'Archipelago Launcher et sélectionnez le client de Banjo-Tooie, dans la colonne de droite.
- Si c'est la première fois que vous ouvrez le client de Banjo-Tooie (ou si vous changez de version), il va vous demander la ROM de Banjo-Tooie. La ROM sera ensuite patchée, et le client vous indiquera où trouver la ROM à utiliser.
- Connectez le client de Banjo-Tooie au serveur, en saisissant l'adresse du serveur et le port dans le champ en haut du client.
- Ouvrez BizHawk, et lancez la ROM patchée.
- Dans BizHawk, cliquez sur Tools, suivi de Lua Console. De là, vous pouvez glisser-déposer banjo_tooie_connector.lua (situé dans le dossier data/lua du dossier d'Archipelago) dans la fenêtre de la Lua console.

## Jouer sur Everdrive
- Lancez l'Archipelago Launcher et sélectionnez le client de Banjo-Tooie, dans la colonne de droite.
- Si c'est la première fois que vous ouvrez le client de Banjo-Tooie, ou si vous changez de version:
  - Le client de Banjo-Tooie va vous demander la ROM de Banjo-Tooie. La ROM sera ensuite patchée, et le client vous indiquera où trouver la ROM à utiliser.
  - Copiez la ROM patch sur la carte SD utilisée pour l'Everdrive
- Branchez un câble USB entre l'Everdrive et l'ordinateur
- Lancez banjo_tooie_everdrive_connector.exe sur l'ordinateur
  - Note 1: cette étape doit être faite avant de connecter le client Banjo-Tooie au serveur
  - Note 2: Si vous utilisez Linux, utilisez plutôt Banjo_Tooie_everdrive_connector_linux.exe
- Lancer la ROM sur l'Everdrive
- Connectez le client de Banjo-Tooie au serveur, en saisissant l'adresse du serveur et le port dans le champ en haut du client.
