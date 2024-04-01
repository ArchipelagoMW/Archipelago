# Guide des Triggers d'Archipelago

Ce guide détaille l'utilisation du système de déclenchement YAML d'Archipelago. Il s'adresse à un utilisateur
avancé ayant une connaissance approfondie des options YAML d'Archipelago ainsi qu'une expérience dans l'édition
de fichiers YAML. Ce guide devrait prendre environ 5 minutes à lire.

## Qu'est-ce que des Triggers?

Les triggers vous permettent de personnaliser les paramètres de votre jeu en vous permettant de définir
une ou plusieurs options qui ne surviennent que dans des conditions spécifiques. Il s'agit essentiellement
de déclarations "if, then" pour les options de votre jeu. Un bon exemple de ce que vous pouvez
faire avec les triggers est le [mode mercenaire personnalisé YAML](https://github.com/alwaysintreble/Archipelago-yaml-dump/blob/main/Snippets/Mercenary%20Mode%20Snippet.yaml)
qui a été créé entièrement à l'aide de triggers et de plando.

Pour plus d'informations sur plando, vous pouvez consulter le [guide général sur plando](/tutorial/Archipelago/plando/fr)
ou le [guide plando A Link to the Past](/tutorial/A%20Link%20to%20the%20Past/plando/en).

## # Utilisation des Triggers

Les triggers peuvent être définis soit à la racine (root) soit dans les sections du jeu. En général,
le meilleur endroit pour le faire est à la fin du fichier YAML pour une organisation claire.

Chaque trigger se compose de quatre parties :
- `option_category` spécifie la section dans laquelle l'option du trigger est définie.
    - Exemple : `A Link to the Past`
    - Il s'agit de la catégorie dans laquelle l'option est située. Si l'option que vous utilisez
	  comme trigger est à la racine, vous utiliseriez `null`. Sinon, il s'agit du jeu pour lequel
	  vous voulez que ce trigger d'option s'active.
- `option_name` spécifie le nom de l'option du trigger.
    - Exemple : `shop_item_slots`
    - Cela peut être n'importe quelle option de n'importe quelle catégorie définie dans le fichier
	  YAML, à la racine ou dans une section de jeu.
- `option_result` spécifie la valeur de l'option qui active ce trigger.
    - Exemple : `15`
    - Chaque trigger doit être utilisé pour exactement un résultat d'option.
	  Si vous souhaitez que la même chose se produise avec plusieurs résultats,
	  vous aurez besoin de plusieurs triggers pour cela.
- `options` est l'endroit où vous définissez ce qui se passera lorsque le trigger s'active.
  Cela peut être aussi simple que de s'assurer qu'une autre option est également sélectionnée ou
  de placer un objet à un endroit spécifique. Il est possible d'avoir plusieurs actions dans cette section.
    - Exemple :
  ```yaml
  A Link to the Past:
    start_inventory: 
      Rupees (300): 2
  ```
  
Le format général est le suivant :

  ```yaml
  category:
    option to change:
      desired result
  ```

### Exemples
Les exemples ci-dessus, une fois regroupés, ressembleront à ceci :

  ```yaml
  triggers:
    - option_category: A Link to the Past
      option_name: shop_item_slots
      option_result: 15
      options:
        A Link to the Past:
          start_inventory:
            Rupees(300): 2
  ```

Dans cet exemple, si le générateur tombe sur 15 pour les emplacements d'objets dans les boutiques
de votre jeu, vous recevrez 600 rubis au début. Les triggers peuvent également être utilisés pour
modifier d'autres options.

Par exemple :

  ```yaml
  triggers:
    - option_category: Timespinner
      option_name: SpecificKeycards
      option_result: true
      options:
        Timespinner:
          Inverted: true
  ```

Dans cet exemple, si votre monde obtient la valeur "true" pour SpecificKeycards, alors votre jeu
commencera également en mode inversé.

Il est également possible d'utiliser des valeurs imaginaires dans les options pour déclencher
des paramètres spécifiques. Vous pouvez utiliser ces valeurs fictives dans vos options principales
ou pour déclencher à partir d'un autre trigger. Actuellement, c'est la seule façon de déclencher
sur "setting 1 ET setting 2".

Par exemple :

  ```yaml
  triggers:
    - option_category: Secret of Evermore
      option_name: doggomizer
      option_result: pupdunk
      options:
        Secret of Evermore:
          difficulty:
            normal: 50
            pupdunk_hard: 25
            pupdunk_mystery: 25
          exp_modifier:
            150: 50
            200: 50
    - option_category: Secret of Evermore
      option_name: difficulty
      option_result: pupdunk_hard
      options:
        Secret of Evermore:
          fix_wings_glitch: false
          difficulty: hard
    - option_category: Secret of Evermore
      option_name: difficulty
      option_result: pupdunk_mystery
      options:
        Secret of Evermore:
          fix_wings_glitch: false
          difficulty: mystery
  ```

Dans cet exemple (Merci à @Black-Sliver), si l'option `pupdunk` est tirée, alors les valeurs
de difficulté seront à nouveau tirées en utilisant les nouvelles options `normal`, `pupdunk_hard`,
et `pupdunk_mystery`, et le modificateur d'expérience sera à nouveau tiré avec de nouveaux poids
pour 150 et 200. Cela permet d'avoir deux autres triggers qui ne seront utilisés que pour les
nouvelles options `pupdunk_hard` et `pupdunk_mystery`, de sorte qu'ils ne seront déclenchés que
sur "pupdunk ET hard/mystery".

Par exemple :

```yaml
Super Metroid:
  start_location: 
    landing_site: 50
    aqueduct: 50
  start_hints:
    - Morph Ball
triggers:
  - option_category: Super Metroid
    option_name: start_location
    option_result: aqueduct
    options:
      Super Metroid:
        +start_hints:
          - Gravity Suit
```
Dans cet exemple, si l'option `start_location` est `landing_site`, seul un indice de départ pour Morph Ball sera créé.
Si `aqueduct` est obtenu, un indice de départ pour Gravity Suit sera également créé en même temps que l'indice pour Morph Ball.

Notez que pour les listes, les éléments peuvent uniquement être ajoutés, et non supprimés ou remplacés. 
Pour les dicts, la définition d'une valeur pour une clé présente remplacera cette valeur dans le dict. 