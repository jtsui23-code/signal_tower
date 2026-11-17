import math
import random


class Tower:
    def __init__(self, pos, range, fr, dmg, cooldown):
        self.position = pos
        self.range = range
        self.fireRate = fr
        self.dmg = dmg
        self.cooldown = cooldown

    def updateCooldown(self, dt):
        self.cooldown -= dt
        if self.cooldown <= 0:
            self.cooldown = self.fireRate
            return True
        return False

    def fire(self, enemies, path):

        # Looks at all enemies if they are in range the enemy takes damage
        for e in enemies:
            x,y = path.calculatePosition(e.distance)
            if math.dist((x,y), (self.position[0], self.position[1])) <= self.range:
                e.takeDMG(self.dmg)

class SuperTower(Tower):
    def __init__(self, pos, range, fr, dmg, cooldown, crit):
        super().__init__(pos, range, fr, dmg, cooldown)

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





