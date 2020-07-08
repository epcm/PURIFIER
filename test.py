import pgzrun

class HP(object):
    def __init__(self, full_HP, num):
        self.full_HP = full_HP
        self.current_HP = full_HP
        self.num = num  #命数
        self.count = 1  #复活次数

class monster(Actor):
    def __init__(self, image, full_HP):
        super().__init__(image)
        self.list = []
        self.monster_HP = HP(full_HP, 1)
        self.HP_bar = Rect[(0, 0), (28, 5)]
        self.currentHP_bar = Rect[(0, 0), (28*self.HP.current_HP/self.HP.full_HP, 5)]
        self.HP_bar.pos = self.x, self.y + 16
        self.currentHP_bar.pos = self.x, self.y + 16

red_dino = monster('red_dino', 10)
print(red_dino.image + 'din', red_dino.a)

def draw():
    red_dino.draw()


def update():
    red_dino.x += 1


pgzrun.go()