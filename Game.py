# Jack Tsui
# OOP Program 4
# Project Description: Tower Defense Game with GUI. Place down towers to defend against enemies. 

import pygame
from Enemy import Enemy, SuperEnemy
from Path import Path
import sys
import random

pygame.init()

class Game:

    def __init__(self, fps=60, health=30):
        self.enemies = []
        self.towers = []

        # Spots next to the path where towers can be built, each kept 80+ pixels from the path
        self.buildPads = [
            (150, 70),
            (150, 250),
            (180, 450),
            (420, 400),
            (550, 420),
            (480, 700),
            (800, 150),
            (800, 400),
            (1080, 450),
            (1080, 560),
        ]

        # Set points for the path the enemies will travel
        self.path = Path([
            (0, 150),
            (300, 150),
            (300, 600),
            (650, 600),
            (650, 250),
            (950, 250),
            (950, 650),
            (1200, 650),
        ])

        # Currency to buy more towers
        self.coins = 0
        self.health = health
        self.fps = fps

        self.running = True

        self.width = 1200
        self.height = 800
        self.background = (30, 30, 40)

        # Setting screen display
        self.screen = pygame.display.set_mode((self.width, self.height))


        pygame.display.set_caption("Signal Tower")
        self.clock = pygame.time.Clock()

        # Setting timmers for when to spawn enemies
        self.spawnTimer = 0.0
        self.spawnInterval = 3

    def run(self):
        while self.running:

            # Checks for events
            for e in pygame.event.get():

                # Will end game if user presses x button on top right
                if e.type == pygame.QUIT:
                    pygame.quit() 
                    sys.exit()

            # Rendering background
            self.screen.fill(self.background)
            dt = self.clock.tick(self.fps) / 1000

            # Updates the game
            self.update(dt)

            # Updates the screen state otherwise the screen would have bleed effect when rendering
            pygame.display.flip()
            


    def handleClick(self, pos):
        pass

    def update(self, dt):

        # Spawns enemies
        self.spawnEnemies(dt)

        # Add coins +1 for every defeated enemy
        self.coin += sum(1 for e in self.enemies if e.hp <= 0)

        # Lose health for every enemy that passes -2 for super enemies -1 for standard enemies
        for e in self.enemies:
            if isinstance(e, SuperEnemy) and e.distance >= self.path.totalLength:
                self.health -= 2
            elif isinstance(e, Enemy) and e.distance >= self.path.totalLength:
                self.health -= 1


        # If enemy doesn't have health or reached end of the path despawn them
        self.enemies = [e for e in self.enemies if e.hp > 0]
        self.enemies = [e for e in self.enemies if e.distance < self.path.totalLength]

        self.towerFire(dt)
        # Renders assests on the screen
        self.render()

        # Updates the position of the enemies
        for e in self.enemies:
            e.updateDistance(dt)

    def render(self):

        # Draws path using a line from Pygame
        pygame.draw.lines(self.screen, (120, 120, 130), False, self.path.positions, 40)

        # Renders enemies if the enemy is Super Enemy draw green ellipse if normal enemy draw red circle
        for e in self.enemies:
            x, y= self.path.calculatePosition(e.distance)

            if isinstance(e, SuperEnemy):
                # (screen, (r,g,b), (x,y,w,h))
                pygame.draw.ellipse(self.screen, (0,255,0), (x-10, y-25, 20, 50))

            elif isinstance(e, Enemy):
                # (screen, (r,g,b), (center, radius), width)
                pygame.draw.circle(self.screen, (255,0,0), (x, y), 20)
        for t in self.towers:
            x, y = t.position[0], t.position[1]



    def spawnEnemies(self, dt):

        # Sets cooldown for when to spawn enemies
        self.spawnTimer -= dt
        if self.spawnTimer <= 0:

            enemy = Enemy(hp=3, speed=65.0) if random.random() < 0.75 else SuperEnemy(hp=6, speed=75.0, defense=3)
            self.enemies.append(enemy)
            self.spawnTimer = self.spawnInterval

    def towerFire(self, dt):

        # Set logic for tower firing at enemy checks for if the tower out of cooldown then fire to 
        # save on computation
        for t in self.towers:
            v = t.updateCooldown(dt)
            if v:
                t.fire(self.enemies, self.path)
            

# Creates instance of Game Class and runs the game loop
game = Game(fps=60, health=30)
game.run()



    

