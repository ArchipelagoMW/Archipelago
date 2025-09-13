# Choo-Choo Charles

## Où est la page d'options ?
La [page d'options du joueur pour ce jeu](../player-options) contient toutes les options pour configurer et exporter un fichier de configuration yaml.

## Qu'est ce que la randomisation fait au jeu ?
Tous les débrits ou n'importe quel objet ramassable au sol (excepté les Caisses à Butin) et objets reçus par les missions de PNJs sont considérés comme emplacements à vérifier.

## Quel est le but de Choo-Choo Charles lorsqu'il est randomisé ?
Vaincre le train démoniaque de l'Enfer nommé "Charles".

## Comment le jeu est-il géré en mode Nightmare ?
À sa mort, le joueur doit relancer une toute nouvelle partie, lui donnant la possisilité de rester en mode Nightmare ou de poursuivre la partie en mode Normal s'il considère la partie trop difficile.
Dans ce cas, tous les objets collectés seront redistribués dans l'inventaire et les états des missions seront conservés.
Le Deathlink n'est pas implémenté pour l'instant. Lorsque cette option sera disponible, un choix sera fourni pour :
* Désactiver le Deathlink
* Activer le Deathlink modéré avec réapparition au Train du Joueur lorsqu'un évènement Deathlink est reçu
* Activer le Deathlink strict avec suppression de la sauvegarde lorsqu'un évènement Deathlink est reçu

## À quoi ressemble un objet d'un autre monde dans Choo-Choo Charles ?
Les apparances des objets sont conservés.
Tout indice qui ne peut pas être représenté normalement dans le jeu est remplacé par l'Easter Egg "DeadDuck" miniaturisé qui peut être vu en dehors des limites murales physiques du jeu original.

## Comment le joueur est-il informé par une transmission d'objet et des indices ?
Un message apparaît en jeu pour informer quel objet est envoyé ou reçu, incluant de quel monde et de quel joueur vient l'objet.
La même méthode est utilisée pour les indices.

## Est-il possible d'utiliser les indices dans le jeu ?
Non, ceci est un travail en cours.
Les options suivantes seront possibles une fois les implémentations disponibles :

À n'importe quel moment, le joueur peu appuyer sur l'une des touches suivantes pour afficher la console dans le jeu :
* "~" (qwerty)
* "²" (azerty)
* "F10"
Puis, un indice peut être révélé en tapant "/hint [player] <item>"
