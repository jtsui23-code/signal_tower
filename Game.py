# Jack Tsui
# OOP Program 4
# Project Description: Tower Defense Game with GUI. Place down towers to defend against enemies. 

import pygame
from Enemy import Enemy, SuperEnemy
from Tower import Tower, SuperTower
from Path import Path
import sys
import random
import math

pygame.init()

class Game:

    def __init__(self, fps=60, health=30):
        self.reset(fps=fps, health=health)

    def run(self):
        while self.running:

            # Checks for events
            for e in pygame.event.get():

                # Will end game if user presses x button on top right
                if e.type == pygame.QUIT:
                    pygame.quit() 
                    sys.exit()

                elif e.type == pygame.MOUSEBUTTONDOWN:
                    self.handleClick(e.pos)


                # Lets you toggle between different towers you want to place based off clicking 1 or 2
                elif e.type == pygame.KEYDOWN and self.state == "playing":

                    if e.key == pygame.K_1:
                        self.selectTower = Tower

                    elif e.key == pygame.K_2:
                        self.selectTower = SuperTower

                elif e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN and self.state != "playing":
                    self.reset(fps=60, health=30)
                    self.state = "playing"

            # Rendering background
            self.screen.fill(self.background)
            dt = self.clock.tick(self.fps) / 1000

            # If in playing mode, update the game
            if self.state == "playing":
                self.update(dt)

                # If lost all health set to gameover mode
                if self.health <= 0:
                    self.state = "gameover"
            else:
                self.renderMenu()
           

            # Updates the screen state otherwise the screen would have bleed effect when rendering
            pygame.display.flip()
            
    def renderMenu(self):
        lines = []

        # You can only enter renderMenu either in title or game over state
        # Displayed text on the screen will vary
        if self.state == "title":
            lines = ["Signal Tower", "Build towers on the pads to stop enemies reaching the end.",
                 "[1] Basic tower   [2] Super tower   Click a pad to build", "Press Enter to start"]
            
        else:
            lines = ["Game Over, Press Enter to play again"]
        
        for i, text in enumerate(lines):
            # First element is title of the screen so gets larger font size
            font = self.titleFont if i == 0 else self.font

            # Renders text on the screen render(text, 
            # antialias which is True for 24-bit RGB/alpha surface false 8-bit surface, 
            # color RGB)

            surface = font.render(text, True, (230, 230, 240))
            self.screen.blit(surface, surface.get_rect(center=(self.width // 2, 250 + i * 70)))

    def handleClick(self, pos):

        # Checks if the user clicked on a build pad
        for pad in self.buildPads:
            if math.dist(pos, pad) <= 20:

                # Check if there is already a tower at the build pad if so don't build there
                if any(t.position == pad for t in self.towers):
                    return

                # Checks if have enough coins to buy tower                        
                if self.coins < self.selectTower.cost:
                    return

                # Spends coins on tower
                self.coins -= self.selectTower.cost

                # Places a Tower down based off of the selected tower type. 
                if self.selectTower is Tower:
                    self.towers.append(Tower(pos=pad, range=130, fr=0.4, dmg=0.5))

                elif self.selectTower is SuperTower:
                    self.towers.append(SuperTower(pos=pad, range=150, fr=1.2, dmg=2, crit=2))


    def update(self, dt):

        # Spawns enemies
        self.spawnEnemies(dt)

        # Ramps up difficulty of the game every 20 seconds by spawning in more enemies
        self.difficultTimer += dt
        if self.difficultTimer >= 7:
            self.difficultTimer = 0

            # Decreases the enemy spawning interval until reach 0.75 interval otherwise enemies would swarm screen.
            self.spawnInterval = max(0.2, self.spawnInterval - 0.25)
            self.speedMultiplier = min(8.5, self.speedMultiplier + 0.5)

        # Add coins +1 for every defeated enemy
        self.coins += sum(1 for e in self.enemies if e.hp <= 0)

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

        # Empty pads as outlines so players can see where to build.
        for x, y in self.buildPads:
            pygame.draw.rect(self.screen, (90, 90, 100), (x - 20, y - 20, 40, 40), 2)

        # Renders the towers
        for t in self.towers:
            color = (180, 120, 255) if isinstance(t, SuperTower) else (80, 200, 170)
            pygame.draw.circle(self.screen, color, t.position, 16)

            # Thin ring shows how far the tower can reach.
            pygame.draw.circle(self.screen, color, t.position, t.range, 1)

        name = "Super Tower" if self.selectTower is SuperTower else "Basic Tower"
        hud = f"Health: {self.health}   Coins: {self.coins}   Selected: {name} ({self.selectTower.cost} Cost)   [1] Basic Tower  [2] Super Tower"
        self.screen.blit(self.font.render(hud, True, (230, 230, 240)), (10, 10))
        



    def spawnEnemies(self, dt):

        # Sets cooldown for when to spawn enemies
        self.spawnTimer -= dt
        if self.spawnTimer <= 0:

            # Increase the speed of the enemies over time.
            enemy = Enemy(hp=4, speed=65.0* self.speedMultiplier) if random.random() < 0.75 else SuperEnemy(hp=7, speed=75.0* self.speedMultiplier, defense=3)
            self.enemies.append(enemy)
            self.spawnTimer = self.spawnInterval

    def towerFire(self, dt):

        # Set logic for tower firing at enemy checks for if the tower out of cooldown then fire to 
        # save on computation
        for t in self.towers:
            v = t.updateCooldown(dt)
            if v:
                t.fire(self.enemies, self.path)

    def reset(self, fps, health):
        self.enemies = []
        self.towers = []
        self.selectTower = Tower
        self.state = "title"

        # Spots next to the path where towers can be built, each kept 80+ pixels from the path
        self.buildPads = [
            (150, 90),
            (150, 210),
            (240, 380),
            (360, 300),
            (360, 540),
            (475, 660),
            (590, 420),
            (710, 450),
            (800, 190),
            (890, 310),
            (1010, 450),
            (1075, 590),
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
        self.coins = 3
        self.health = health
        self.fps = fps

        # Used to increase difficult by spawning in more enemies
        self.difficultTimer = 0.0
        self.speedMultiplier = 1.0

        self.running = True

        self.width = 1200
        self.height = 800
        self.background = (30, 30, 40)

        # Setting screen display
        self.screen = pygame.display.set_mode((self.width, self.height))

        # Fonts for the game.
        self.font = pygame.font.SysFont(None, 32)
        self.titleFont = pygame.font.SysFont(None, 80)


        pygame.display.set_caption("Signal Tower")
        self.clock = pygame.time.Clock()

        # Setting timmers for when to spawn enemies
        self.spawnTimer = 0.0
        self.spawnInterval = 3
            

# Creates instance of Game Class and runs the game loop
game = Game(fps=60, health=30)
game.run()



    

