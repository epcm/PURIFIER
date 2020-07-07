import pgzrun
import turtle
import random
import math

music.play('达拉崩吧')
# HP类，可用于王子及小怪
class HP(object):
    def __init__(self, FullHP, num):
        self.FullHP = FullHP
        self.CurrentHP = FullHP
        self.num = num  #命数
        self.count = 1  #复活次数

    #判断是否死亡并在可能的情形下复活
    def isdead(self):
        if self.CurrentHP > 0:
            return
        elif self.CurrentHP <= 0 and self.count < self.num:  #能复活
            self.CurrentHP = self.FullHP
            self.count += 1
            hero.pos = (0, 0)
            return
        else:
            return True

class monster(Actor):
    def __init__(self, image, HP):
        super().__init__(image)
        self.list = []
        self.HP = HP


red_dino = monster('red_dino', 10)
green_din = monster('green_din', 10)
red_din = monster('red_din', 10)


class weapon():
    def __init__(self, type, distance, damage):
        self.type = type # 1为近战武器，2为远程武器
        self.distance = distance
        self.damage = damage
        self.image_name = ''
    
    def attack(self, pos):
        # 近战武器
        if self.type == 1:
            #clock.schedule_interval(animate_chop, 1)
            #for mon in monsters:
            if hero.distance_to(monster) < self.distance:
                ang = hero.angle_to(monster)
                if ((step == 4 and -60 <ang < 60) or 
                (step == 5 and (120 <ang < 180 or -180< ang < -120)) or 
                (step == 6 and 30 <ang < 150) or 
                (step == 7 and -150 <ang < -30)):
                    global monster_HP, speed_x, speed_y
                    monster_HP.CurrentHP -= self.damage
                    if step == 4:
                        monster.x += standard_speed*10
                    elif step == 5:
                        monster.x -= standard_speed*10
                    elif step == 6:
                        monster.y -= standard_speed*10
                    elif step == 7:
                        monster.y += standard_speed*10
                    global beaten
                    animate_shake(monster)
                    beaten = True
        
        # 远程武器
        elif self.type == 2:
            b = bullet(self.distance, self.damage, hero.angle_to(pos))
            b.actor.pos = hero.pos
            bullets.append(b)

class bullet():
    def __init__(self,distance, damage, ang):
        self.damage = damage
        self.distance = distance
        self.actor = Actor('子弹特效1')
        self.actor.angle = ang
        self.speed_x = standard_speed ** 1.5 *math.cos(math.radians(ang))
        self.speed_y = -standard_speed ** 1.5 *math.sin(math.radians(ang))
        self.count_time = 0 #计时工具

def on_mouse_down(pos):
    current_weapon.attack(pos)

# 怪兽shake
def animate_shake(monster):
    animate(monster, duration = 0.1, angle = 30)
    clock.schedule(shake2, 0.1)
    clock.schedule(shake3, 0.3)
    clock.schedule(recover, 0.2)
    tone.play('A2', 0.1)
def shake2():
    animate(monster, duration = 0.2, angle = -30)
def shake3():
    animate(monster, duration = 0.1, angle = 0)

# 近战动画
image_count = 1
def animate_chop():
    global image_count
    if(step == 4):
        hero.image = "prince_right_斧子{}".format(image_count)
    image_count += 1
    if image_count > 3:
        clock.unschedule(animate_chop)
        image_count = 1 
    
# 怪兽在被击退后重获速度
def recover():
    global beaten
    beaten = False


bullets = []
weapons = [weapon(2, 300, 1), weapon(1, 300, 2)]
current_weapon = weapon(1, 300, 1)
current_weapon_id = 0


# 测试用怪兽血条
monster_HP = HP(500, 1)
beaten = False

isLoose = False
speed_x = 2
speed_y = 2
standard_speed = 2

background1 = Actor("bg1")  # 896, 448
background1.pos = 500, 300

hero = Actor("prince")
prince_HP = HP(10, 1)  #初始化王子HP

monsters = []
monster = Actor("red_din")
start = False
game = False

coins = 0

n = 3
box = Actor('box_close')
box1 = Actor('box_close')
box2 = Actor('box_close')
box3 = Actor('box_close')
send = Actor('传送门')
background1 = Actor('bg1')
send.pos = 700, 500

boxes = [box, box1, box2, box3]

for i in range(4):
    a = random.randint(100, 800)
    b = random.randint(150, 600)
    boxes[i].x = a
    boxes[i].y = b


WIDTH = background1.width + 100
HEIGHT = background1.height + 300
step = 99

monster.x = WIDTH / 2
monster.y = HEIGHT / 2


class Boxing:
    for i in range(4):
            boxes[i].open = False

def open_box():
    global check, coins
    j = check
    bit = random.randint(0, 30)
    if bit % 5 == 0:
        boxes[j].image = 'red_dino'
    elif bit % 5 == 1:
        boxes[j].image = 'green_din'
    elif bit % 5 == 2:
        boxes[j].image = 'red_din'
    elif bit % 5 == 3 or bit % 5 == 4:
        boxes[j].image = 'gloden2'
    boxes[j].open = True
    if boxes[j].image == 'gloden2':
        number = random.randint(20, 40)
        coins += number

def game_over():
    pass


# 画血条
def draw_hp_bar():
    global step
    if (prince_HP.isdead()):
        step = 3
    #screen.blit('hp_bar', (20, 20))
    HP_bar = Rect((20, 20), (200, 35))  #血槽
    CurrentHPBar = Rect(
        (183, 20), (165 *(prince_HP.CurrentHP / prince_HP.FullHP) , 13))  #当前血量
    #CurrentHPBar.right = 183+20
    screen.draw.rect(HP_bar, 'black')
    screen.draw.filled_rect(CurrentHPBar, 'black')
    #########
    MonsterBar = Rect((100, 300), (200, 35))
    MonsterCurrentBar = Rect(
        (100, 20), (200 * monster_HP.CurrentHP / monster_HP.FullHP, 33))
    screen.draw.filled_rect(MonsterCurrentBar, 'green')
    ##########

# 画金币
def draw_coins_bar():
    screen.blit('gloden', (20, 60))  #20,60
    screen.draw.text(str(coins), (125, 77), fontsize=50)  #125 77


### 上下左右行走模块函数 ###
def left_movement():
    hero.image = "prince_left"


def right_movement():
    hero.image = "prince_right"


def up_movement():
    hero.image = "prince_back"


def down_movement():
    hero.image = "prince"


####################


def draw():
    global step, isLoose, start, game
    screen.fill('white')
    if step != 1 and step != 2 and step != 3:
        screen.draw.text("Welcome to the Prince V.S. Monsters Game\n"
                         "  Press  Number  1  to  start  the  new  game\n"
                         "  Press  Number  2  to  continue  the  game\n"
                         "  Press  Number  3  to  exit  the  game", (200, 200), fontsize=50, color="orange")
        start = False
    else:
        start = True
        game = True
    if game:
        screen.clear()
        screen.fill('white')
        background1.draw()
        hero.draw()
        screen.draw.text("Press Number 3 to exit the game", (80, 0), fontsize=25, color='orange')
        monster.draw()
        send.draw()

        # elif step == 2:
        if step == 3:
            isLoose = True
            screen.clear()
            screen.fill('white')
            screen.draw.text("You have lose your game, please exit!", (200, 200), fontsize=50, color="orange")
            exit()
        ### 上下左右移动模块 ####
        if step == 4 or step == 5 or step == 6 or step == 7:
            background1.draw()
            monster.draw()
            for i in range(4):
                boxes[i].draw()
            send.draw()
            # 优先级最高
            hero.draw()
            # HP、金币状态绘制
            draw_hp_bar()
            draw_coins_bar()

            # 子弹绘制
            for i in bullets:
                i.actor.draw()

            if step == 4:
                clock.schedule(right_movement, 0.01)
            if step == 5:
                clock.schedule(left_movement, 0.01)
            if step == 6:
                clock.schedule(up_movement, 0.01)
            if step == 7:
                clock.schedule(down_movement, 0.01)
    #################################

def on_key_down(key):
    global step
    step = 0
    if key == keys.K_1:
        step = 1
    elif key == keys.K_2:
        step = 2
    elif key == keys.K_3:
        step = 3
        exit()

#### 切换武器
def on_key_up(key):
    global current_weapon_id, current_weapon
    if key == keys.Q:
        current_weapon_id = (1 + current_weapon_id) % 2
        current_weapon = weapons[current_weapon_id]
        print(current_weapon_id)

def update():
    global step, hero, speed_x, speed_y, game, check
    prince_HP.CurrentHP -= 0.5
    # 往右走
    if game:
        if keyboard.D:
            hero.x += 5
            if hero.x >= WIDTH:
                hero.x = WIDTH - 30
            step = 4
        elif keyboard.A:
            if hero.x < 0:
                hero.x = 0 + 30
            hero.x -= 5
            step = 5
        elif keyboard.W:
            if hero.y < 0:
                hero.y = 0 + 30
            hero.y -= 5
            step = 6
        elif keyboard.S:
            if hero.y >= HEIGHT:
                hero.y = HEIGHT - 30
            hero.y += 5
            step = 7
        #####子弹更新模块#####
        for i in bullets:
            i.actor.x += i.speed_x
            i.actor.y += i.speed_y
            i.count_time += 1
            if (i.count_time >= i.distance / standard_speed ** 1.5):
                bullets.remove(i)
            if monster.colliderect(i.actor):
                global monster_HP
                monster_HP.CurrentHP -= i.damage
                bullets.remove(i)
                tone.play('A1', 0.1)
                animate_shake(monster)
        if monster_HP.isdead():
            monster.x = -50
            monster.y = -50



        ##### 怪兽自己走模块 #####
        # monster.pos = random.randint(0, WIDTH), random.randint(0, HEIGHT)


        if hero.distance_to(monster) <= 5:
            prince_HP.CurrentHP -= 5



        # 靠近至一定距离时怪兽主动接近
        if not beaten:
            if monster.distance_to(hero) < 200:
                '''#if random.randint(1,6) == 1:
                speed_x = standard_speed**1.5 * math.cos(monster.angle_to(hero))
                speed_y = -standard_speed**1.5 * math.sin(monster.angle_to(hero))'''
                ## 注意以下模块中speed维持非负
                if monster.x > hero.x:
                    monster.x -= speed_x
                elif monster.x < hero.x:
                    monster.x += speed_x
                else:
                    speed_y = standard_speed ** 1.5
                speed_x = standard_speed

                if monster.y > hero.y:
                    monster.y -= speed_y
                elif monster.y < hero.y:
                    monster.y += speed_y
                else:
                    speed_x = standard_speed ** 1.5
                speed_y = standard_speed

            else:
                # 平均2s一次的随机转向
                if random.randint(1, 120) == 1:
                    # ang = random.randint(-180, 180)
                    ang = random.choice([0, 45, 90, 135, 180, 225, 270, 315])
                    speed_x = standard_speed ** 1.5 * math.cos(math.radians(ang))
                    speed_x = -standard_speed ** 1.5 * math.sin(math.radians(ang))
                monster.x += speed_x
                monster.y += speed_y

        if WIDTH <= monster.x or monster.x <= 0:
            speed_x *= -1
        if HEIGHT <= monster.y or monster.y <= 0:
            speed_y *= -1

        # 画箱子函数
        for j in range(0, 4):
            if hero.colliderect(boxes[j]) and boxes[j].open == False:
                check = j
                boxes[j].image = 'box_open'
                clock.schedule_unique(open_box, 0.1)
'''
#如果第一关没死光
second_mission = False
if second_mission and hero.pos = 700, 500:
    #如果没杀光，第三、四关都不可以
    background2 = Actor('ba2')
    background2.draw()
    thrid_mission, final_mission = False, False
    #杀光后就是通过
    third_mission = True
if third_mission and hero.pos = 700, 500:
    # 如果没死光,最后一关不可以
    background3 = Actor('ba3')
    background3.draw()
    final_mission = False
    #杀光后就进入Boss关卡
    final_mission = True
if final_mission and hero.pos = 700, 500:
    # 如果没死光
    background4 = Actor('ba4')
    background4.draw()
    # 死光后进入结束语
'''





pgzrun.go()
