# Custom blueprint shapes guide for shapez 2

## How does this work?

The `blueprint_shapes` option normally gives you a choice between different sets of blueprint shapes taken from the 
vanilla scenarios (or completely random shapes). However, you can also provide a list of custom shapes to be used for 
gaining blueprint points.

## How do I use it?

Instead of just writing a single option name like `regular` or `randomized`, you need to provide list **as a choice**.
"As a choice" means that you'll need to pack it into a list or as a weighted choice, see the examples down below for 
how to do it. The value has to be a list of shape codes surrounded by quotation marks (`"` or `'`). It needs to contain 
at least 1 and up to 5 shapes.

## Examples on how using this option could look like

```
shapez 2:
  ...
  blueprint_shapes:
    # The extra "- " is required in order to not break weighting
    # That however makes picking out a random list possible (if multiple are provided)
    - ["CuCuCuCu", "P-P-P-P-:RgRbRgRb", "Cr------:Cg------"]
```

```
shapez 2:
  ...
  blueprint_shapes:
    # Here is an example of providing multiple lists and even regular choices
    - ["CuCuCuCu", "P-P-P-P-:RgRbRgRb", "Cr------:Cg------"]
    - ["SrCmSrCm", "crcrcrcr:P-P-P-P-:RgRbRgRb"]
    - insane
```

```
...
shapez 2:
  ...
  blueprint_shapes:
    # Alternative way with different weights
    randomized: 25
    ["CuCuCuCu", "P-P-P-P-:RgRbRgRb", "Cr------:Cg------"]: 75
```