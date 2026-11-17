class Enemy:
    def __init__(self, hp, speed):
        self.hp = hp
        self.speed = speed
        self.distance = 0.0

    def updateDistance(self, dt):
        self.distance += dt * self.speed

    def takeDMG(self, dmg):
        self.hp -= dmg

class SuperEnemy(Enemy):
    def __init__(self, hp, speed, defense):
        super().__init__(hp, speed)
        self.defense = defense

    def takeDMG(self, dmg):
        super().takeDMG(max(1, dmg-self.defense))



if __name__ == "__main__":

    e = Enemy(hp=3, speed=60.0)
    e.updateDistance(0.5)
    assert e.distance == 30.0

    # Armor of 3 against a 10 damage hit should take 7 off, never heal.
    s = SuperEnemy(hp=20, speed=40.0, defense=3)
    s.takeDMG(10)
    assert s.hp == 13

    # Weak hits still do 1 so armor can't make it unkillable.
    s.takeDMG(1)
    assert s.hp == 12
    print("Enemy checks passed.")