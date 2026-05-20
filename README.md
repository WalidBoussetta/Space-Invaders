#  Space Invaders - Python Pygame

Un jeu inspiré du célèbre **Space Invaders**, développé en **Python** avec la bibliothèque **Pygame**.  
Le joueur contrôle un vaisseau spatial capable de tirer sur des vagues d’ennemis tout en évitant leur progression.

---

##  Description

Ce projet consiste à créer un mini jeu arcade 2D avec :

- Déplacement du joueur
- Tir de projectiles
- Ennemis animés
- Système de score
- Gestion des niveaux
- Effets d’explosion avec particules
- Fond spatial animé

Le jeu utilise les fonctionnalités de **Pygame** pour gérer les graphismes, les événements clavier, les animations et les collisions.

---

##  Réalisé par

- Walid Boussetta

---

##  Fonctionnalités

###  Gameplay

- Déplacement gauche/droite du vaisseau
- Tir avec la touche `SPACE`
- Ennemis qui se déplacent en groupe
- Passage automatique au niveau suivant
- Système de vies et score
- Animation d’explosions
- Fond étoilé animé

---

##  Concepts utilisés

- Programmation orientée jeu
- Gestion des événements clavier
- Détection de collisions
- Animation 2D
- Gestion des particules
- Boucle de jeu (`game loop`)
- Gestion des niveaux et difficulté progressive

---

##  Architecture générale

Le jeu fonctionne avec une boucle principale :

1. Lecture des événements clavier
2. Déplacement du joueur
3. Création et déplacement des projectiles
4. Déplacement des ennemis
5. Détection des collisions
6. Mise à jour des particules
7. Affichage graphique avec Pygame

---

##  Structure du projet

```bash
space-invaders/
│
├── main.py
├── assets/
├── README.md
└── requirements.txt
