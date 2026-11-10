# Guida al Setup di Muse Dash per Archipelago

## Links
- [Pagina Principale](../../../../games/Muse%20Dash/info/en)
- [Opzioni](../../../../games/Muse%20Dash/player-options)

## Software Richiesto

- Windows 8 o più recente.
- Muse Dash: [Disponibile su Steam](https://store.steampowered.com/app/774171/Muse_Dash/)
  - \[Facoltativo\] DLC [Muse Plus]: [Disponibile su Steam](https://store.steampowered.com/app/2593750/Muse_Dash_Muse_Plus/)
- Melon Loader: [GitHub](https://github.com/LavaGang/MelonLoader/releases/latest)
  - L'installer potrebbe richiedere .Net Framework 4.8: [Download](https://dotnet.microsoft.com/it-it/download/dotnet-framework/net48)
- .NET Desktop Runtime 6.0.XX (Se non installato in precedenza): [Download](https://dotnet.microsoft.com/it-it/download/dotnet/6.0)
- Muse Dash Archipelago Mod: [GitHub](https://github.com/DeamonHunter/ArchipelagoMuseDash/releases/latest)

## Installare la mod di Archipelago per Muse Dash

1. Scarica [MelonLoader.Installer.exe](https://github.com/LavaGang/MelonLoader/releases/latest) ed eseguilo.
2. Seleziona la scheda "automated", premi select e naviga fino a `MuseDash.exe`.
  - Puoi trovare la cartella tramite steam premendo tasto destro sul gioco nella tua libreria e scegliendo *Gestisci→Sfoglia i file locali*
  - Se clicki sulla barra nella parte superiore della finestra, che ti dice la cartella attuale, questa ti darà un percorso che potrai copiare. 
    Se copi questo percorso nella finestra creata da **MelonLoader** il programma navigherà automaticamente fino a quella cartella.
3. Seleziona v0.7.0. e premi "install".
4. Esegui il gioco una volta e aspetta fino alla comparsa del menù iniziale di Muse Dash prima di chiuderlo.
5. Scarica l'ultima versione della [Muse Dash Archipelago Mod](https://github.com/DeamonHunter/ArchipelagoMuseDash/releases/latest)
   ed estraila nella cartella `/Mods/` appena creata nella cartella di installazione di Muse Dash.
  - Tutti i file devono essere nella cartella `/Mods/` e non in una cartella al suo interno.

Se hai installato tutto correttamente, dovrebbe apparire un bottone in basso a destra che ti permetterà di effettuare il login ad un server di Archipelago.

## Generare una Sessione MultiWorld
1. Visita la pagina [Player Options](/games/Muse%20Dash/player-options) e configura a tuo piacimento le opzioni specifiche per il gioco.
2. Esporta il tuo file yaml e usalo per generare una nuova sessione randomizzata
  - (Per istruizioni su come generare una nuova sessione di Archipelago, fai riferimento alla [Archipelago Web Guide](/tutorial/Archipelago/setup/en))

## Entrare in una Sessione MultiWorld

1. Esegui Muse Dash e supera la schermata iniziale. Premi il bottone in basso a destra.
2. Inserisci i dettagli della sessione di Archipelago, come l'indirizzo del server con la sua porta (per esempio, archipelago.gg:38381), nome utente e password.
3. Se tutto è stato inserito correttamente, la finestra dovrebbe scomparire e dovrebbe apparire il menù principale. 
   Una volta entrato nella schermata di selezione canzoni dovrebbe esserne disponibile un numero ridotto.

## Risoluzione Problemi

### No Support Module Loaded

Questo errore avviene quando Melon Loader non è in grado di trovare i file necessari per eseguire le mod. Generalmente ci sono due cause principali per questo errore:
un errore nella generazione dei file quando il gioco è stato avviato con Melon Loader per la prima volta o la rimozione di file dopo la generazione da parte di un antivirus.

Per risolvere questo problema devi per prima cosa rimuovere Melon Loader da Muse Dash.
Puoi fare ciò eliminando la cartella di Melon Loader all'interno della cartella di Muse Dash, dopodichè puoi seguire nuovamente i passaggi per l'installazione.

Se continui ad avere lo stesso problema e stai usando un antivirus, prova a disattivarlo temporaneamente quando esegui Muse Dash per la prima volta
o aggiungi la cartella di Muse Dash alla whitelist.
