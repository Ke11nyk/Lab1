# Lab1

Platformer Game (Python + Tkinter)

This repository contains the source code for a 2D platformer game built using Python and the Tkinter library. The game includes essential platformer mechanics such as:

   * Character movement and jumping
   * Collision detection with platforms
   * Movement of platforms
   * Menu and statistics of game

This project is ideal for those who want to learn the basics of game development in Python using Tkinter for the graphical interface.

📌 How to Run:

Install Python (version 3.8 or later).
Clone the repository:
```bash
git clone <repo-url>
cd platformer-game
```

Run the main script:
```bash
python main.py
```


**Disclaimer**

Errors are possible in the calculations :)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
10 classes: Game, Button, RestartButton, ExitButton, Coords, Sprite, PlatformSprite, MovingPlatformSprite, StickFigureSprite, DoorSprite

46 fields: Game: 10, Button: 5, Coords: 4, Sprite: 3, PlatformSprite: 2, MovingPlatformSprite: 5, StickFigureSprite: 13, DoorSprite: 4

26 methods(with getters): Game: 3, Button: 2, RestartButton: 2, ExitButton: 2, Coords: 1, Sprite: 3, PlatformSprite: 1, MovingPlatformSprite: 3, StickFigureSprite: 15, DoorSprite: 3 + def main

2 inheritance hierarchies: Button(RestartButton, ExitButton), Sprite(PlatformSprite(MovingPlatformSprite), StickFigureSprite, DoorSprite)

3 cases of polymorphism: move, coords, click_button
