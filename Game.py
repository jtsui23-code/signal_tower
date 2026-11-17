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


        self.coins = 0
        self.health = health
        self.fps = fps

        self.running = True

        self.width = 1200
        self.height = 800
        self.background = (30, 30, 40)

        self.screen = pygame.display.set_mode((self.width, self.height))


        pygame.display.set_caption("Signal Tower")
        self.clock = pygame.time.Clock()

        self.spawnTimer = 0.0
        self.spawnInterval = 3

    def run(self):
        while self.running:

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit() 
                    sys.exit()

            self.screen.fill(self.background)
            dt = self.clock.tick(self.fps) / 1000

            self.update(dt)
            pygame.display.flip()
            


    def handleClick(self, pos):
        pass

    def update(self, dt):
        self.spawnEnemies(dt)
        self.enemies = [e for e in self.enemies if e.hp > 0]
        self.enemies = [e for e in self.enemies if e.distance < self.path.totalLength]
        self.render()
        for e in self.enemies:
            e.updateDistance(dt)

    def render(self):
        pygame.draw.lines(self.screen, (120, 120, 130), False, self.path.positions, 40)

        for e in self.enemies:
            x, y= self.path.calculatePosition(e.distance)

            if isinstance(e, SuperEnemy):
                # (screen, (r,g,b), (x,y,w,h))
                pygame.draw.ellipse(self.screen, (0,255,0), (x-10, y-25, 20, 50))

            elif isinstance(e, Enemy):
                # (screen, (r,g,b), (center, radius), width)
                pygame.draw.circle(self.screen, (255,0,0), (x, y), 20)

    def spawnEnemies(self, dt):
        self.spawnTimer -= dt
        if self.spawnTimer <= 0:

            enemy = Enemy(hp=3, speed=65.0) if random.random() < 0.75 else SuperEnemy(hp=6, speed=75.0, defense=3)
            self.enemies.append(enemy)
            self.spawnTimer = self.spawnInterval

game = Game(fps=60, health=30)
game.run()



    

