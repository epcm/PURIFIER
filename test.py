import pgzrun
import csv
import random

standard_speed = 2

a = Actor('red_dino')
a.pos = 100, 100
b = Actor('green_dino')
b.pos = 50, 100
animate(a, pos = (50, 100))

def draw():
    a.draw()
    b.draw()
    if a.collidepoint(b):
        print(1)

pgzrun.go()