import pgzrun

hero = Actor('prince')
animate(hero, duration = 1, angle = 10)

def draw():
    screen.clear()
    hero.draw()

pgzrun.go()