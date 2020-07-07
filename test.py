import pgzrun

class monster(Actor):
    def __init__(self, HP):
        super().__init__('red_din')
        self.HP = HP

red_dino = monster(HP = 10)
print(red_dino.image - 'din')

def draw():
    red_dino.draw()

def update():
    red_dino.x += 1


pgzrun.go()