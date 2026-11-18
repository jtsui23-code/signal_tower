import math
import random


class Tower:

    # Making the cost of all standard towers universal. This will make it easy to select between Standard and Super 
    # Towers when placing them in the game class without having to create an object. The game class can just 
    # access the cost of the tower using Tower.cost versus making a Tower and then checking its cost.
    cost = 3

    def __init__(self, pos, range, fr, dmg):
        self.position = pos
        self.range = range
        self.fireRate = fr
        self.dmg = dmg
        self.cooldown = 0

    # Handles cooldown of how fast the tower can fire.
    def updateCooldown(self, dt):
        self.cooldown -= dt
        if self.cooldown <= 0:
            self.cooldown = self.fireRate
            return True
        return False

    # Handles the logic for how towers target enemies and makes enemies take damage.
    def fire(self, enemies, path):

        # Looks at all enemies if they are in range the enemy takes damage
        for e in enemies:
            x,y = path.calculatePosition(e.distance)
            if math.dist((x,y), (self.position[0], self.position[1])) <= self.range:

                # Since Python passes list by object refernce calling the enemies's takeDMG method in here
                # will change the enemies in the Game script.
                e.takeDMG(self.dmg)

class SuperTower(Tower):
    cost = 5

    def __init__(self, pos, range, fr, dmg, crit):
        super().__init__(pos, range, fr, dmg)

        # Critical Hit is when a tower attacks for more than normal base damage based off set
        # critical hit rate percentage making Super Towers do more damage.
        self.crit = dmg * crit
        self.critRate = 0.25

    def fire(self, enemies, path):
        # Looks at all enemies if they are in range the enemy takes damage
        for e in enemies:
            x,y = path.calculatePosition(e.distance)
            if math.dist((x,y), (self.position[0], self.position[1])) <= self.range:

                # Added critical hits based off of crit multplier and crit rate
                dmg = self.crit if random.random() < self.critRate else self.dmg
                e.takeDMG(dmg)





