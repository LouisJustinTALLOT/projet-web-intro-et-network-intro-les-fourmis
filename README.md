# Ce que nous avons fait

### Monstres et trésors

Nous avons ajouté un certain nombre de monstres (Dark Vador, Gollum, le Joker et Voldemord, en rouge) et de trésors
apparents sur la carte (en jaune). Les joueurs sont tous en vert.

Les joueurs peuvent attaquer ces monstres en appuyant sur la barre espace s'ils sont proches d'eux. Mais attention,
les monstres peuvent également attaquer les joueurs ! Les points de vie des monstres sont variables, ils ne sont pas
tous faciles à battre !

Un compteur sous la carte indique les points de vie restants de chaque joueur. Il y a aussi une ligne avec la quantité
d'argent gagnée, et un score (calculé avec les gains d'argent, les intéractions avec les monstres et les morts).

### Multi-joueur

Nous avons ajouté un mode multijoueur. Pour y accéder, on peut ouvrir plusieurs onglets sur le même navigateur, ou
jouer sur le même réseau local (host=0.0.0.0).

Les joueurs peuvent s'attaquer entre eux, et voir les autres informations de chaque joueur. Des flèches permettent de
savoir quel joueur nous sommes actuellement en train de jouer.

Nous avons ajouté un petit bandeau avec la dernière action pour pouvoir suivre les aventures des autres joueurs
(par exemple : "le joueur 2 a attaqué Voldemord").

Attention, il ne faut pas actualiser la page pendant la partie !

### Interface

Nous avons amélioré l'interface. Le code couleur se rapproche d'un Rogue-Pacman !

### Système de niveaux

Nous avons ajouté un système de niveaux. Pour accéder au niveau supérieur, il faut se placer sur la case grisée.
Le niveau actuel est marché en haut à gauche.

Le système de niveau marche en mode joueur unique. En mode multijoueur, le système est pratiquement fonctionnel.

# Rogue nethack with Flask

Programme Python servant de base à l'évaluation par projet du cours Programme coopérants et Web Intro.

## Execution du programme 

Dans le dossier racine du dépôt, il suffit de lancer 

```bash 
python app.py 
```

Et ensuite dans le navigateur allez à l'url `localhost:5001` vous verrez alors apparaitre la page suivante : 

![](media/demo.png)


Vous pouvez alors déplacer le personnage (symbolisé par un `@`) à l'aide des boutons de navigations ou des fleches de votre clavier. 

## Description du code 

Le code est assez sommaire.

Dans `game_backend` vous trouverez la gestion du jeux. En l'état il y a surtout la génération de la map et la gestion du personnage pour qu'il ne puisse pas traverser les murs. 

Dans `app.py` vous avez le serveur Flask qui s'occupe de faire l'interaction entre le client (la page html) et le backend de jeux. 

Dans templates vous avez la page html et dans `static/js` les quelques fonctions javascript nécessaire à l'interaction (les déplacements du personnage). 

## Travail à faire 

Pour rappel le travail attendu est d'enrichir ce squelette de code de la manière suivante (trié par ordre croissant d'importance) : 

1. Ajout de monstres/trésors/équipements apparents et/ou cachés sur la map 
2. Ajout d'un mode multi-joueur (possibilité pour les joueurs de s'attaquer entre eux) 
3. Amélioration de l'interface côté joueur (j'ai fait un html pas très beau à vous de faire mieux) 
4. Système de niveau (pour le mode joueur unique) 
5. Possibilité de sauvergarder sa partie et de revenir plus tard (pour le mode joueur unique)  

Pour la notation, histoire qu'il n'y ait pas de surprise, voici les règles : 
* Si le point (1) est traité => 10/20 
* Si les points (1) + (2) sont traités => 13/20 
* Si les points (1) + (2) + (3) sont traités => 15/20 
* Si les points (1) + (2) + (3) + (4) sont traités => 18/20 
* Si les points (1) + (2) + (3) + (4) + (5) sont traités => 20/20

La date de rendu, qui est fixée dans le github classroom, est le **03/05/2021 à 12h00**. 
