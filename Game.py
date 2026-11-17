import pygame
from Enemy import Enemy, SuperEnemy
from Path import Path
import sys

pygame.init()

class Game:

    def __init__(self, dt=60, health=30):
        self.enemies = []
        self.towers = []
        self.buildPads = []
        self.path = Path 


        self.coins = 0
        self.health = health
        self.dt = dt

        self.running = True
        self.width = 800
        self.height = 600
        self.background = (30, 30, 40)
        self.screen = pygame.display.set_mode((self.width, self.height))


        pygame.display.get_caption("Signal Tower")
        self.clock = pygame.time.Clock()



    def run(self):
        while self.running:

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit() 
                    sys.exit()

            self.screen.fill(self.background)
            
            pygame.display.flip()
            self.clock.tick(self.dt)

    def handleClick(self, pos):
        pass

    def update(self):
        pass

    def render():
        pass
    def spawnEnemies():
        pass



    

