import pgzrun
import csv
import random

standard_speed = 2

# HP类，可用于王子及小怪
class HP(object):
    def __init__(self, full_HP, num):
        self.full_HP = full_HP
        self.current_HP = full_HP
        self.num = num  #命数
        self.count = 1  #复活次数 + 1

    #判断是否死亡并在可能的情形下复活
    def isdead(self):
        if self.current_HP > 0:
            return
        elif self.current_HP <= 0 and self.count < self.num:  #能复活
            self.current_HP = self.full_HP
            self.count += 1
            hero.pos = (0, 0)
            return
        else:
            return True

class Monster(Actor):
    def __init__(self, name, full_HP, attack_distance,attack_damage,clash_damage,speed_rate,bullet_image,bullet_speed_rate,autochase_distance):
        super().__init__(name)
        self.list = []
        self.HP = HP(full_HP, 1)
        self.HP_bar = Rect((0, 0), (28, 5))
        self.currentHP_bar = Rect((0, 0), (28, 5))
        self.speed_x = random.choice([1, -1]) * standard_speed
        self.speed_y = random.choice([1, -1]) * standard_speed
        self.attack_distance = attack_distance
        self.attack_damage = attack_damage
        self.beaten = False
        self.attack_image = bullet_image
        self.clash_damage = clash_damage
        self.autochase_distance = autochase_distance

f = open('Monsters.csv', encoding = 'utf-8-sig')
rd = csv.reader(f)
row = next(rd)

for row in rd:
    if row[0] == 'red_dino':
        red_dino = Monster(*row)
    
print(red_dino.autochase_distance)
f.close()


'''def draw():
    red_dino.draw()


def update():
    red_dino.x += 1


pgzrun.go()'''