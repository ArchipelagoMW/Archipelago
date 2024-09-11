# Sonic Adventure 2: Battle Randomizer Guia de Setup

## Software Requerido

- Sonic Adventure 2: Battle de: [Página da Loja Steam de Sonic Adventure 2: Battle](https://store.steampowered.com/app/213610/Sonic_Adventure_2/)
	- A DLC "SONIC ADVENTURE 2: BATTLE" é requerida se você escolher adicionar as localizações do Chao Karate para o randomizer.
- SA Mod Manager de: [Página de Lançamentos do SA Mod Manager no GitHub](https://github.com/X-Hax/SA-Mod-Manager/releases)
- .NET Desktop Runtime 7.0 de: [Página de Download de .NET Desktop Runtime 7.0](https://dotnet.microsoft.com/pt-br/download/dotnet/thank-you/runtime-desktop-7.0.9-windows-x64-installer)
- Mod do Archipelago para Sonic Adventure 2: Battle
  de: [Página de Lançamentos do Mod Archipelago Randomizer para Sonic Adventure 2: Battle](https://github.com/PoryGone/SA2B_Archipelago/releases/)

## Software Opcional
- Rastreador Sonic Adventure 2 (Tracker)
	- PopTracker de: [Página de Lançamentos de PopTracker](https://github.com/black-sliver/PopTracker/releases/)
	- Sonic Adventure 2: Battle Archipelago PopTracker pack de: [Página de Lançamentos de SA2B AP Tracker](https://github.com/PoryGone/SA2B_AP_Tracker/releases/)
- Mods qualidade de vida
	- SA2 Volume Controls de: [Página de Mod de SA2 Volume Controls](https://gamebanana.com/mods/381193)
- Sonic Adventure DX de: [Página da Loja Steam de Sonic Adventure DX](https://store.steampowered.com/app/71250/Sonic_Adventure_DX/)
	- Para o funcionamento da opção `SADX Music` (Veja "Opções Adicionais" para instruções).

## Passo a Passo de Instalação (Windows)

1. Instale Sonic Adventure 2: Battle na Steam.

2. Abra o jogo sem mods pelo menos uma vez.

3. Instale SA Mod Manager de acordo com [suas instruções](https://github.com/X-Hax/SA-Mod-Manager/tree/master?tab=readme-ov-file).

4. Extraia o mod do Archipelago na pasta `/mods` na pasta em que você instalou Sonic Adventure 2: Battle, a fim que `/mods/SA2B_Archipelago` seja um endereço válido.

5. Na pasta SA2B_Archipelago, execute o script `CopyAPCppDLL.bat` (a janela vai rapidamente abrir e fechar sozinha).

6. Execute o `SAModManager.exe` e tenha certeza que o mod SA2B_Archipelago está listado e habilitado.

## Passo a Passo de Instalação (Linux e Steam Deck)

1. Instale Sonic Adventure 2: Battle na Steam.

2. Nas propriedades para Sonic Adventure 2 na Steam, force o uso de Proton Experimental como ferramenta de compatibilidade.

3. Abra o jogo sem mods pelo menos uma vez.

4. Crie uma pasta `/mods` e outra pasta `/SAManager` na pasta em que você instalou Sonic Adventure 2: Battle.

5. Instale SA Mod Manager como de acordo com [suas instruções](https://github.com/X-Hax/SA-Mod-Manager/tree/master?tab=readme-ov-file). Especificamente, extraia o arquivo SAModManager.exe para a pasta em que Sonic Adventure 2: Battle foi instalado. Para executar o programa, adicione `SAModManager.exe` como um jogo não Steam (No canto inferior esquerdo da biblioteca Steam). Nas propriedades para SA Mod Manager na Steam, habilite o uso de Proton como ferramenta de compatibilidade.

6. Execute SAModManager.exe na Steam. Isso deve produzir um popup de erro para uma dependência faltando (missing dependency), então feche o erro.

7. Instale protontricks, no Steam Deck isso pode ser feito via Discover store, em outros distros instruções podem variar, [veja a página do github de protontricks](https://github.com/Matoking/protontricks).

8. Instale o [.NET 7 Desktop Runtime for x64 Windows](https://dotnet.microsoft.com/pt-br/download/dotnet/thank-you/runtime-desktop-7.0.17-windows-x64-installer}. Se esse link não funcionar, o download pode ser encontrado [nesta página](https://dotnet.microsoft.com/pt-br/download/dotnet/7.0).

9. Clique com o botão direito no exe do .NET 7 Desktop Runtime, e assumindo que protontricks foi instalado corretamente, a opção para "Abrir com Protontricks Launcher" deve estar disponível. Clique nisso, e na janela popup que abrir, selecione SAModManager.exe. Siga os prompts após isso para instalar o .NET 7 Desktop Runtime para o SAModManager. Uma vez finalizado, você deve conseguir executar com sucesso o SAModManager na Steam.

10. Extraia o mod do Archipelago nessa pasta, a fim que `/mods/SA2B_Archipelago` seja um endereço válido.

11. Na pasta SA2B_Archipelago, copie o arquivo `APCpp.dll` e cole-o na pasta de instalação de Sonic Adventure 2 (onde o arquivo `sonic2app.exe` se localiza).

12. Execute `SAModManager.exe` na Steam e tenha certeza que o mod SA2B_Archipelago está listado e habilitado.

Nota: Tenha certeza de executar Sonic Adventure 2 diretamente da Steam no Linux, ao invés de executar usando o botão `Salvar & Jogar` do SA Mod Manager.

## Entrando em um jogo MultiWorld

1. Antes de abrir o jogo, execute o `SAModManager.exe`, selecione o mod SA2B_Archipelago, e aperte o botão `Configurar Mod`.

2. Para o campo `Server IP` em  `AP Settings`, coloque o endereço do servidor, como por exemplo archipelago.gg:38281, o host do servidor deve conseguir identificar isso.

3. Para o campo `PlayerName` em `AP Settings`, insira o "nome" que inseriu no yaml, ou no website config.

4. Para o campo `Password` em `AP Settings`, insira a senha do servidor se uma existir, caso o contrário deixe em branco.

5. Clique no botão `Salvar` e aperte `Salvar & Jogar` para abrir o jogo. No Linux, abra Sonic Adventure 2 diretamente da Steam ao invés de apertar `Salvar & Jogar`.

6. Crie um novo save para se conectar a um jogo MultiWorld. Uma mensagem dizendo "Connected to Archipelago" irá aparecer se você se conectar com sucesso. Se você fechar o jogo enquanto conectado, você pode se reconectar ao jogo MultiWorld selecionando o mesmo save slot.

## Opções Adicionais

Algumas opções adicionais relacionadas às mensagens do Archipelago dentro do jogo podem ser ajustadas no SAModManager se você selecionar `Configurar Mod` no mod SA2B_Archipelago. Essas opções estarão na aba `General Settings`.
	
- Message Display Count: Esse é o número máximo de mensagens do Archipelago que podem ser exibidas na tela a qualquer ponto.
- Message Display Duration: Isso dita por quanto tempo as mensagens do Archipelago são exibidas na tela (em segundos).
- Message Font Size: Isso é o tamanho da fonte usada para exibir as mensagens do Archipelago.

Se você deseja usar a opção `SADX Music` do Randomizer, você deve possuir uma cópia de `Sonic Adventure DX` na Steam e seguir os seguintes passos:

1. Ache a pasta no seu PC onde `Sonic Adventure DX` está instalado.

2. Abra a pasta `SoundData` na pasta de instalação de `Sonic Adventure DX`, e copie a pasta `bgm`.

3. Dentro da pasta do mod `SA2B_Archipelago`, cole a pasta `bgm` na pasta `ADX` que existe dentro da pasta `gd_PC`.

## Solução de problemas

- "The following mods didn't load correctly: SA2B_Archipelago: DLL error - The specified module could not be found."
	- Tenha certeza que `APCpp.dll` está na mesma pasta que `sonic2app.exe`. (Veja Passo a Passo de Instalação passo 6)
	
- "sonic2app.exe - Entry Point Not Found"
	- Tenha certeza que `APCpp.dll` está atualizado para a última versão. Siga Passo a Passo de Instalação passo 6 para atualizar o dll.

- Jogo rodando muito rápido (Que nem o Sonic).
	- Limite o framerate usando o mod manager:
		1. Execute `SAModManager.exe`.
		2. Selecione a aba `Definições do Jogo`, e então selecione a subaba `Correções`.
		3. Marque a caixinha do `Lock Framerate` (Limitar Framerate) na seção Correções.
		4. Aperte o botão `Salvar`.
	- Se estiver usando uma placa de vídeo da NVidia:
		1. Abra NVIDIA Control Panel.
		2. Selecione `Gerenciar as configurações em 3D` em `Configurações 3D` na esquerda.
		3. Selecione a aba `Configurações do programa` na janela principal.
		4. Clique o botão `Acrescentar` e selecione `sonic2app.exe` (ou procure a localização do exe), então clique `Adicionar Programa selecionado`.
		5. Abaixo de `Especificar as configurações deste programa:`, encontre a opção `Taxa Máxima de Quadros` e clique na coluna de configuração para essa opção.
		6. Escolha a opção `Ligado` e insira 60 como valor do FPS na caixa ao lado do slider (ou 59 se 60 crashar o jogo).

- Inputs de Controle não estão funcionando.
	1. Execute Launcher.exe na mesma pasta em que instalou Sonic Adventure 2: Battle.
	2. Selecione a aba `Player` e re-selecione o controle do método de input do player 1.
	3. Clique o botão `Save settings and launch SONIC ADVENTURE 2`. (Quaisquer configurações do mod manager irão aplicar mesmo se o jogo for iniciado dessa maneira ao invés de iniciado pelo mod manager)
	
-  O jogo crasha após logos.
	- Isso pode ser causado por uma alta taxa de atualização no monitor.
		- Mude a taxa de atualização no monitor para 60 Hz [Alterar a taxa de atualização no monitor no Windows] (https://support.microsoft.com/pt-br/windows/change-your-display-refresh-rate-in-windows-c8ea729e-0678-015c-c415-f806f04aae5a)
	- Isso pode ser consertado habilitando o modo de compatibilidade com Windows 7 no app do Sonic:
		1. Clique no botão direito do mouse no sonic2app.exe e selecione `Propriedades`.
		2. Selecione a aba `Compatibilidade`.
		3. Cheque a caixa `Executar este programa em modo de compatibilidade:` e selecione Windows 7 no drop-down abaixo.
		4. Clique no botão `Aplicar`.
		
- Sem opções de resolução no Launcher.exe.
	- No drop-down `Graphics device`, selecione o dispositivo e display em que você planeja rodar o jogo. O drop-down `Resolution` deve funcionar assim que o Graphics device for selecionado.
	
- Nenhuma música está tocando no jogo.
	- Se você habilitou a opção `SADX Music`, então provavelmente os arquivos de música não foram copiados apropriadamente na pasta do mod (Veja Opções Adicionais para instruções).
	
- A Missão 1 contém uma textura faltando na UI do Stage Select.
	- Provavelmente algum outro mod está tendo conflito e sobrescrevendo a textura. É recomendado ter o mod SA2B Archipelago carregado por último no mod manager.

## Proteção de Save File (Opção Avançada)

O mod contém uma proteção de save a qual associa o save file a uma seed específica do Archipelago. Por padrão, save files apenas podem conectar-se aos servidores de Archipelago que correspondem com sua seed. A proteção pode ser desabilitada no mod config.ini mudando a linha `IgnoreFileSafety` para `true`. Isso NÃO é recomendado para o usuário comum, já que isso permitirá que qualquer save file conecte-se e mande itens para o servidor do Archipelago.
