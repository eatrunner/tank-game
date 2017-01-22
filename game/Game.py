from Tank import Tank
from random import randint
from Map import Map
from Bonus import Bonus
from WeaponBonus import WeaponBonus
from BonusSpawner import BonusSpawner


class Game(Map):
    CONTROL = ["left", "right", "up", "down"]
    BONUSES = ["weapon", "vest"]

    def __init__(self, mapId, mapSize):
        super(Game, self).__init__(mapId, mapSize)
        self.observers = []
        self.playerTank = Tank(0, self.playerPos, self)
        self.tanks.append(self.playerTank)
        self.avalMaps = []
        self.avalMaps.append(1)
        self.timeToNextBonus = 5
        self.currentBonusId = 0
        self.bonusSpawner = BonusSpawner(self, self.bonusSpawnTime)

    # Returns a list of available maps' id numbers
    def getAvalMaps(self):
        return self.avalMaps

    def getMap(self):
        return self.array

    # Returns the map size - all maps are square
    def getMapSize(self):
        return self.size

    # Notifies all obsevers about tank's position change
    def notifyTankPosition(self, tank):
        for observer in self.observers:
            observer.updateTankPosition(
                tank.id, tank.currPos, tank.faceDirection)

    def notifyBulletPosition(self, bullet):
        for observer in self.observers:
            observer.updateBulletPosition(
                bullet.id, bullet.currPos, bullet.direction)

    def notifyAddTank(self, tank):
        for observer in self.observers:
            observer.addTank(tank.id, tank.currPos, tank.faceDirection)

    def notifyRemoveTank(self, tank):
        for observer in self.observers:
            observer.removeTank(tank.id)

    def notifyAddBullet(self, bullet):
        for observer in self.observers:
            observer.addBullet(bullet.id, bullet.currPos, bullet.direction)

    def notifyRemoveBullet(self, bullet):
        for observer in self.observers:
            observer.removeBullet(bullet.id)

    def notifyAddBonus(self, bonus):
        for observer in self.observers:
            observer.addBonus(bonus.id, bonus.pos, bonus.name)

    def notifyRemoveBonus(self, bonus):
        for observer in self.observers:
            observer.removeBonus(bonus.id, bonus.x, bonus.y, bonus.name)

    def getTank(self, id):
        for tank in self.tanks:
            if tank.id == id:
                return tank
        return None

    # if possible moves a tank in a direction
    def moveTank(self, id, direction):
        for tank in self.tanks:
            if tank.id == id:
                if (tank.move(direction)):
                    self.notifyTankPosition(tank)

    def addTank(self, tank):
        self.tanks.append(tank)
        self.notifyAddTank(tank)

    def removeTank(self, tank):
        self.notifyRemoveTank(tank)
        self.tanks.remove(tank)

    def addBullet(self, bullet):
        self.bullets.append(bullet)
        self.notifyAddBullet(bullet)

    def removeBullet(self, bullet):
        self.notifyRemoveBullet(bullet)
        self.bullets.remove(bullet)
        tank = self.getTank(bullet.tankId)
        if(tank != None):
            tank.removeBullet(bullet)

    def createBonus(self, id, pos, name):
        [x, y] = pos
        bonus = WeaponBonus(id, x, y)
        self.bonuses.append(bonus)
        self.notifyAddBonus(bonus)

    def addBonus(self, bonus):
        self.bonuses.append(bonus)
        self.notifyAddBonus(bonus)

    def removeBonus(self, bonus):
        self.bonuses.remove(bonus)
        self.notifyRemoveBonus(bonus)

    def shoot(self, id):
        for tank in self.tanks:
            if tank.id == id:
                if (len(tank.bullets) < tank.maxBullets):
                    bullet = tank.createBullet()
                    self.addBullet(bullet)

    def getFreeCoords(self):
        while(True):
            x = randint(0, self.size - 1)
            y = randint(0, self.size - 1)
            if self.matrix[x][y] == 'E' and self.getTank([x, y]) == None and self.getBonus(x, y) == None:
                return [x, y]

    def addObserver(self, observer):
        self.observers.append(observer)
        for tank in self.tanks:
            observer.addTank(tank.id, tank.currPos, tank.faceDirection)
            if(tank.bullets != []):
                for bullet in tank.bullets:
                    observer.addBullet(
                        bullet.id, bullet.currPos, bullet.direction)
        observer.updateMap(self.array)
        observer.updateMapSize(self.size)

    def processGame(self):
        """if self.timeToNextBonus == 0:
            self.timeToNextBonus = 5
            self.createBonus(self.currentBonusId,
                             self.getFreeCoords(), "weapon")
            self.currentBonusId += 1
        else:
            self.timeToNextBonus = self.timeToNextBonus - 1
"""
        self.bonusSpawner.process()
        for tank in self.tanks:
            if (tank.bullets != []):
                bulletsToRemove = []
                for bullet in tank.bullets:
                    if(tank.moveBullet(bullet) == True):
                        self.notifyBulletPosition(bullet)
                    else:
                        bulletsToRemove.append(bullet)
                for bullet in bulletsToRemove:
                    self.removeBullet(bullet)
