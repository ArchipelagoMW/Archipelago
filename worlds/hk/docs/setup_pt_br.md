# Guia de configuração para Hollow Knight no Archipelago

## Programas obrigatórios
* Baixe e extraia o Lumafly Mod Manager (gerenciador de mods Lumafly) do [Site Lumafly](https://themulhima.github.io/Lumafly/).
* Uma cópia legal de Hollow Knight.
    * Versões Steam, Gog, e Xbox Game Pass do jogo são suportadas.
    * Windows, Mac, e Linux (incluindo Steam Deck) são suportados.

## Instalando o mod Archipelago Mod usando Lumafly
1. Abra o Lumafly e confirme que ele localizou sua pasta de instalação do Hollow Knight.
2. Clique em "Install (instalar)" perto da opção "Archipelago" mod.
    * Se quiser, instale também o "Archipelago Map Mod (mod do mapa do archipelago)" para usá-lo como rastreador dentro do jogo.
3. Abra o jogo, tudo preparado!

### O que fazer se o Lumafly falha em encontrar a sua pasta de instalação
1. Encontre a pasta manualmente.
    * Xbox Game Pass:
        1. Entre no seu aplicativo Xbox e mova seu mouse em cima de "Hollow Knight" na sua barra da esquerda. 
        2. Clique nos 3 pontos depois clique gerenciar.
        3. Vá nos arquivos e selecione procurar. 
        4. Clique em "Hollow Knight", depois em "Content (Conteúdo)", depois clique na barra com o endereço e a copie.
    * Steam:
        1. Você provavelmente colocou sua biblioteca Steam num local não padrão. Se esse for o caso você provavelmente sabe onde está.
           Encontre sua biblioteca Steam, depois encontre a pasta do Hollow Knight e copie seu endereço.
            * Windows - `C:\Program Files (x86)\Steam\steamapps\common\Hollow Knight`
            * Linux/Steam Deck - `~/.local/share/Steam/steamapps/common/Hollow Knight`
            * Mac - `~/Library/Application Support/Steam/steamapps/common/Hollow Knight/hollow_knight.app`
2. Rode o Lumafly como administrador e, quando ele perguntar pelo endereço do arquivo, cole o endereço do arquivo que você copiou.

## Configurando seu arquivo YAML
### O que é um YAML e por que eu preciso de um?
Um arquivo YAML é a forma que você informa suas configurações do jogador para o Archipelago.
Olhe o [guia de configuração básica de um multiworld](/tutorial/Archipelago/setup/en) aqui no site do Archipelago para aprender mais.

### Onde eu consigo o YAML?
Você pode usar a [página de configurações do jogador para Hollow Knight](/games/Hollow%20Knight/player-options) aqui no site do Archipelago 
para gerar o YAML usando a interface gráfica.

### Entrando numa partida de Archipelago no Hollow Knight
1. Começe o jogo depois de instalar todos os mods necessários.
2. Crie um **novo jogo salvo.**
3. Selecione o modo de jogo **Archipelago** do menu de seleção.
4. Coloque as configurações corretas do seu servidor Archipelago.
5. Aperte em **Começar**. O jogo vai travar por uns segundos enquanto ele coloca todos itens.
6. O jogo vai te colocar imediatamente numa partida randomizada. 
    * Se você está esperando uma contagem então espere ele cair antes de apertar começar.
    * Ou clique em começar e pause o jogo enquanto estiver nele.

## Dicas e outros comandos
Enquanto jogar um multiworld, você pode interagir com o servidor usando vários comandos listados no
[Guia de comandos](/tutorial/Archipelago/commands/en). Você pode usar o cliente de texto do Archipelago para isso,
que está incluido na ultima versão do [Archipelago software](https://github.com/ArchipelagoMW/Archipelago/releases/latest).
