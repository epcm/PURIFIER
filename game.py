import pgzrun
import csv
import random
import time
#import numpy as math
import math
import easygui as g
import sys

TITLE = "The Game of Purifier"
FM = open('Monsters.csv', encoding = 'utf-8-sig')
FW = open('Weapons.csv', encoding = 'utf-8-sig')
FG = open('GlobalConst.csv', encoding = 'utf-8-sig')
#music.play('达拉崩吧')
pos = [(1000, 400), (1000, 400), (1000, 300), (1500, 600)]
surface = Actor('purifier1')


###############类class######################

# HP类，可用于王子及小怪
class HP(object):
    def __init__(self, full_HP, num):
        self.full_HP = full_HP
        self.current_HP = full_HP
        self.num = num  # 命数
        self.count = 1  # 复活次数 + 1

    # 判断是否死亡并在可能的情形下复活
    def isdead(self):
        if self.current_HP > 0:
            return
        elif self.current_HP <= 0 and self.count < self.num:  # 能复活
            self.current_HP = self.full_HP
            self.count += 1
            hero.bottomleft = (0, HEIGHT)
            return
        else:
            return True
        

class Monster(Actor):
    # 参数传入亦可改写为args，更简洁美观，不过可读性下降
    def __init__(self, image, full_HP, attack_distance,attack_damage,clash_damage,speed_rate,
                bullet_image,bullet_speed_rate,autochase_distance):
        super().__init__(image)
        self.list = []
        self.HP = HP(float(full_HP), 1) # 血量类
        self.HP_bar = Rect((0, 0), (28, 5)) # 满血条
        self.currentHP_bar = Rect((0, 0), (28, 5)) # 血条
        self.speed_rate = float(speed_rate) # 移动速度
        self.speed_x = random.choice([1, -1]) * STANDARD_SPEED * self.speed_rate
        self.speed_y = random.choice([1, -1]) * STANDARD_SPEED * self.speed_rate # 速度
        self.attack_distance = float(attack_distance) # 攻击距离
        self.attack_damage = float(attack_damage) # 攻击伤害
        self.beaten = False # 击退状态
        self.bullet_image = bullet_image # 攻击图像
        self.clash_damage = float(clash_damage) # 接触伤害
        self.autochase_distance = float(autochase_distance) # 自动追逐距离
        self.bullet_speed_rate = float(bullet_speed_rate) # 发射攻击速度
        self.mode = 1

    # 怪兽在被击退后重获速度
    def recover(self):
        self.beaten = False
    
    def attack(self):
        b = Bullet(self.bullet_image,self.attack_distance, self.attack_damage, 
                    self.bullet_speed_rate,self.angle_to(hero))
        b.pos = self.pos
        monster_bullets.append(b)
        
    # 每次uodate时更新怪兽的状态
    def move(self):
        self.HP_bar.topleft = self.x - 11, self.y - 18
        self.currentHP_bar.width = 28 * self.HP.current_HP / self.HP.full_HP
        self.currentHP_bar.topleft = self.x - 11, self.y - 18
        # 靠近至一定距离时怪兽主动接近
        if not self.beaten:
            if self.distance_to(hero) < self.autochase_distance:
                chase(self, hero)         
            else:
                #平均2s一次的随机转向
                if random.randint(1, 120) == 1:
                    #ang = random.randint(-180, 180)
                    ang = random.randint(0, 360)#choice([0, 45, 90, 135, 180, 225, 270, 315])
                    self.speed_x = STANDARD_SPEED ** 1.5 * math.cos(math.radians(ang)) * self.speed_rate
                    self.speed_x = -STANDARD_SPEED ** 1.5 * math.sin(math.radians(ang)) * self.speed_rate
                self.x += self.speed_x
                self.y += self.speed_y

        if WIDTH <= self.x or self.x <= 0:
            self.speed_x *= -1
        if HEIGHT <= self.y or self.y <= 0:
            self.speed_y *= -1

    # 怪兽shake
    def animate_shake(self):
        animate(self, duration = 0.1, angle = 30)
        clock.schedule(self.shake2, 0.1)
        clock.schedule(self.shake3, 0.3)
        clock.schedule(self.recover, 0.2)
        tone.play('A2', 0.1)
    def shake2(self):
        animate(self, duration = 0.2, angle = -30)
    def shake3(self):
        animate(self, duration = 0.1, angle = 0)

    # 从迟缓状态恢复
    def reset_speed_rate(self):
        self.speed_rate /= 0.8

class Boss(Actor):
    def __init__(self):
        super().__init__('boss')
        self.image = 'boss'
        self.midtop = 983.5, 164
        self.pos1 = (WIDTH - 395, 265)
        self.pos2 = (WIDTH - 401, 389) 
        self.HP = HP(200, 1)
        self.timer = 0
        self.magic = Actor('magic')
        self.magic_on = False


    # 冲撞
    def attack1(self):
        self.ahead()
        clock.schedule(self.back, 0.8)
    def ahead(self):
        clock.schedule_interval(self.foreward, 1/100)
    def back(self):
        self.image = 'boss_right'
        clock.schedule_interval(self.backward, 1/100)
        clock.schedule(self.stop, 0.8)
    def foreward(self):
        self.x -= 15
    def backward(self):
        self.x += 30
    def stop(self):
        clock.unschedule(self.backward)
        clock.unschedule(self.foreward)
        self.image = 'boss'

    
    # 散射
    def attack2(self):
        for i in range(3):
            b = Bullet('fireball1', 500, 2, 3, 150 + 30 * i)
            b1 = Bullet('fireball1', 500, 2, 3, 150 + 30 * i)
            b.pos = self.pos1
            b1.pos = self.pos2
            monster_bullets.append(b)
            monster_bullets.append(b1)

    # magic
    def attack3(self):
        self.magic_on = True
        clock.schedule(self.remove_magic, 1)
        clock.schedule(self.set_bullet, 0.5)
        self.magic.center = hero.pos
    def remove_magic(self):
        self.magic_on = False
    def set_bullet(self):
        for i in range(10):
            b = Bullet('fireball', 100, 1, 2, -135)
            x = random.random()*244 + self.magic.center[0] - 122 + 100
            y = random.random()*154 + self.magic.center[1] - 77 - 100
            b.pos = x, y
            monster_bullets.append(b)


    def call(self):
        x = random.randint(100, 800)
        y = random.randint(150, 430)
        type = random.randint(1, 5)
        boxes.append(Box(type, (x, y))) 


class Weapon(Actor):
    def __init__(self, image,type,distance,damage,price,MP_consuming,bullet_image,speed_rate,Note):
        super().__init__(image)
        self.type = int(type) # 1为近战武器，2为远程武器
        self.distance = float(distance) # 攻击距离
        self.damage = float(damage) # 伤害
        self.price = float(price) # 价格
        self.MP_consuming = float(MP_consuming) # MP消耗
        self.bullet_image = bullet_image # 子弹图像
        self.speed_rate = float(speed_rate) # 子弹速度
        self.Note = Note # 武器信息
    
    def attack(self, pos):
        global current_MP, animate_image_count, no_boss
        if self.MP_consuming > current_MP:
            return
        current_MP -= self.MP_consuming
        # 近战武器
        if self.type == 1:
            if step in [4, 5]:
                animate_image_count = 1
                clock.schedule_interval(animate_chop, 0.05)
            for monster in monsters:
                if hero.distance_to(monster) < self.distance:
                    ang = hero.angle_to(monster)
                    if ((step == 4 and -60 <ang < 60) or 
                    (step == 5 and (120 <ang < 180 or -180< ang < -120)) or 
                    (step == 6 and 30 <ang < 150) or 
                    (step == 7 and -150 <ang < -30)):
                        monster.HP.current_HP -= self.damage
                        if step == 4:
                            monster.x += STANDARD_SPEED*10
                        elif step == 5:
                            monster.x -= STANDARD_SPEED*10
                        elif step == 6:
                            monster.y -= STANDARD_SPEED*10
                        elif step == 7:
                            monster.y += STANDARD_SPEED*10
                        monster.HP.current_HP -= self.damage
                        if monster.HP.isdead():
                            monsters.remove(monster)
                        monster.animate_shake()
                        monster.beaten = True
                if LEVEL == 4 and hero.distance_to(boss) < self.distance:
                    boss.HP.current_HP -= self.damage
                if boss.HP.isdead():
                    no_boss = True
                    clock.unschedule(boss_attack) 
                    
        
        # 远程武器
        elif self.type == 2:
            b = Bullet(self.bullet_image, self.distance, self.damage, self.speed_rate,hero.angle_to(pos))
            b.pos = hero.pos
            bullets.append(b)
            if self is qiang1:
                b1 = Bullet(self.bullet_image, self.distance, self.damage, self.speed_rate,hero.angle_to(pos) + 20)
                b2 = Bullet(self.bullet_image, self.distance, self.damage, self.speed_rate,hero.angle_to(pos) - 20)
                b1.pos = hero.pos
                b2.pos = hero.pos
                bullets.append(b1)
                bullets.append(b2)
            elif self is changmao1:
                b.trace = True
                mindis = 10000
                for monster in monsters:
                    dis = monster.distance_to(hero)
                    if  dis < mindis:
                        mindis = dis
                        b.target = monster

class Bullet(Actor):
    def __init__(self, image, distance, damage, speed_rate, ang):
        super().__init__(image)
        self.damage = damage
        self.distance = distance
        self.angle = ang
        self.speed_x = STANDARD_SPEED ** 1.5 *math.cos(math.radians(ang)) * speed_rate
        self.speed_y = -STANDARD_SPEED ** 1.5 *math.sin(math.radians(ang)) * speed_rate
        self.count_time = 0 #计时工具
        self.target = None # 长矛1的跟踪对象
        self.speed_rate = speed_rate
        self.trace = False

class Box(Actor):

    def __init__(self, type, pos):
        super().__init__('box_close')
        self.type = type
        self.pos = pos
        self.open = False

    def open_box(self):
        global  coins
        self.image = 'box_open'
        self.open = True
        if self.type == 1:
            mon = Monster(*ls_monster[1])
            mon.pos = self.pos
            monsters.append(mon)
        elif self.type == 2:
            mon = Monster(*ls_monster[2])
            mon.pos = self.pos
            monsters.append(mon)
        elif self.type == 3:
            mon = Monster(*ls_monster[3])
            mon.pos = self.pos
            monsters.append(mon)
        elif self.type == 4 or type == 5:
            self.image = 'golden_coin'
            number = random.randint(20, 40)
            coins += number
        elif self.type == 6:
            mon = Monster(*ls_monster[4])
        clock.schedule(self.remove_self, 1)

    def remove_self(self):
        boxes.remove(self)
    


##################全局变量global##########################
FGreader = csv.DictReader(FG)
dic = next(FGreader)
ls_monster = list(csv.reader(FM))
ls = list(csv.reader(FW))

# 武器模块
# 参数依次为 image, type, distance, damage, price, MP_consuming
fuzi = Weapon(*ls[1])
gong1 = Weapon(*ls[2])
gong2 = Weapon(*ls[3]) # 半透明代表未拥有
jian1= Weapon(*ls[4])
jian2 = Weapon(*ls[5])
qiang1 = Weapon(*ls[6])
qiang2 = Weapon(*ls[7])
changmao1 = Weapon(*ls[8])
changmao2 = Weapon(*ls[9])
fuzi.pos = (370,240)
gong1.pos = (405,240)
gong2.pos = (445,240)
jian1.pos = (480,240)
jian2.pos = (520,240)
qiang1.pos = (560,240)
qiang2.pos = (590,240)
changmao1.pos = (630,240)
changmao2.pos = (370,280)

# 双方在空中的子弹
bullets = []
monster_bullets = []

# 参战武器槽与参战武器控制
weapon_bar = Actor('weapon_bar')
weapon_bar.pos = 320, 40
weapons_on_bar = [fuzi, gong1]
current_weapon_id = 0
current_weapon = weapons_on_bar[current_weapon_id]

# 背包
bag = Actor('背包')
bag.pos = 500,300
bag_weapons = [fuzi, gong1] # 已经拥有的武器
bag_open = False

# 武器
weapons = [fuzi, gong1, gong2, jian1, jian2, qiang1, qiang2, changmao1, changmao2]

# 金币，商店页面控制
coins = int(dic['coins'])
step_store = 0
step_store1 = 0

#武器商店模块
store_button = Actor("store_button")
store_inner = Actor("store")
Pur_button = Actor("purchase")

# 标准速度
STANDARD_SPEED = float(dic['STANDARD_SPEED'])

# 地图与背景
background1 = Actor("bg1")  # 896, 448
background1.topleft = 0, 0#background1.pos = 500, 300
WIDTH = background1.width #+ 100
HEIGHT = background1.height #+ 300

# 在场角色
hero = Actor("prince")
hero.bottomleft = 0, HEIGHT
hero_HP = HP(float(dic['HP']), int(dic['LIFE']))  #初始化王子HP
full_MP = float(dic['MP'])
HERO_SPEED = float(dic['HERO_SPEED'])
HERO_SPEED_DICT = {4:(HERO_SPEED, 0), 5:(-HERO_SPEED, 0), 6:(0, -HERO_SPEED), 7:(0, HERO_SPEED)}
current_MP = full_MP
MP_RECOVERY_SPEED = float(dic['MP_RECOVERY_SPEED']) #每次刷新的MP恢复量
monsters = []
send = Actor('传送门')
boss = Boss()

# 游戏控制
isLoose = False
game = False
step = 99
Total = 3
LEVEL = 4
no_boss = True

# 箱子部分
n = int(dic['BOX_NUM_LEVEL1'])
boxes = []
#background1 = Actor('bg1')
#send.bottomright = 1200, 450#send.pos = 700, 500

################各类函数##############################
# 追逐函数
def chase(a, b):
    if b != None:
        rand_ang = random.randint(-20, 20)
        a.speed_x = STANDARD_SPEED **1.5 * math.cos(math.radians(a.angle_to(b)+rand_ang)) * a.speed_rate
        a.speed_y = -STANDARD_SPEED**1.5 * math.sin(math.radians(a.angle_to(b)+rand_ang)) * a.speed_rate
    a.x += a.speed_x
    a.y += a.speed_y   

# 近战动画
animate_image_count = ''
def animate_chop():
    global animate_image_count
    animate_image_count += 1
    if animate_image_count > 3:
        clock.unschedule(animate_chop)
        animate_image_count = ''

# 画血条和蓝条
def draw_status_bar():
    global step
    if (hero_HP.isdead()):
        step = 2
    currentHP_bar = Rect(
        (27, 26), (235 * hero_HP.current_HP / hero_HP.full_HP, 13))  #当前血量
    screen.blit('status_bar', (20, 20))
    screen.draw.filled_rect(currentHP_bar, 'red')

    currentMP_bar = Rect(
        (27, 54), (235 * current_MP / full_MP, 13))  #当前血量
    screen.blit('status_bar', (20, 48))
    screen.draw.filled_rect(currentMP_bar, 'blue')

# 画金币
def draw_coins_bar():
    screen.blit('golden_coin', (20, 80))  #20,60
    screen.draw.text(str(coins), (125, 97), fontsize=50, color = 'gold')  #125 77


### 上下左右行走模块函数 ###
def left_movement():
    hero.image = f"prince_left_{current_weapon.image}{animate_image_count}"


def right_movement():
    hero.image = f"prince_right_{current_weapon.image}{animate_image_count}"


def up_movement():
    hero.image = "prince_back"


def down_movement():
    hero.image = f"prince_{current_weapon.image}"

# 商店的购买判断
def purchase_judge(n):
    global coins, step_store1, step_store, current_weapon_id
    if coins < weapons[step_store - 2].price:
        step_store1 = 20
        clock.schedule(reset_step_store1, 2)
    else:
        key = weapons[step_store - 2]
        key.image = f'{key.image[:-6]}'#将半透明图像替换为不透明图像
        coins = coins - weapons[step_store - 2].price
        bag_weapons.append(key)
        weapons_on_bar[current_weapon_id] = key
        current_weapon_id = (current_weapon_id+1)%2
        current_weapon = weapons_on_bar[current_weapon_id]
        step_store = 1

# 用于clock.schedule调用，清除金钱不够的信息
def reset_step_store1():
    global step_store1
    step_store1 = 0
# boss攻击
def boss_attack():
    seed = random.randint(1, 7)
    if seed == 1:
        boss.attack1()
    elif seed in [2, 3]:
        boss.attack2()
    elif seed in [4, 5]:
        boss.attack3()
    elif seed in [6, 7]:
        boss.call()

# 构造关卡函数
def construct_level():
    global n
    if LEVEL == 1:
        send.pos = pos[0][0], pos[0][1]
        background1.image = 'bg1'
        n = int(dic['BOX_NUM_LEVEL1'])
        for i in range(n):
            x = random.randint(100, 800)
            y = random.randint(150, 430)
            type = random.randint(1, 5)
            boxes.append(Box(type, (x, y))) 

    elif LEVEL == 2:
        send.pos = pos[1][0], pos[1][1]
        background1.image = 'bg2'
        n = int(dic['BOX_NUM_LEVEL2'])
        for i in range(n):
            x = random.randint(100, 800)
            y = random.randint(150, 430)
            type = random.randint(1, 5)
            boxes.append(Box(type, (x, y))) 

    elif LEVEL == 3:
        send.pos = pos[2][0], pos[2][1]
        background1.image = 'bg3'
        for i in range(n):
            x = random.randint(100, 800)
            y = random.randint(150, 430)
            type = random.randint(1, 5)
            boxes.append(Box(type, (x, y))) 

    elif LEVEL == 4:
        send.pos = pos[3][0], pos[3][1]
        background1.image = 'final'
        background1.topleft = 0, 0
        global no_boss
        no_boss = False
        clock.schedule_interval(boss_attack, 2)

    elif LEVEL == 5:  
        endgamemode()
construct_level()

############按键与鼠标#########################

def on_mouse_down(pos, button):
    global coins
    global step_store, bag_open, current_weapon, current_weapon_id, weapons_on_bar
    if button == mouse.RIGHT:
        if step_store in range(2, 11):
            step_store = 1 #返回商店初始界面
        else:
            step_store = 12 #退出商店
            current_weapon_id = 0
        if bag_open:
            bag_open = False
            current_weapon_id = 0
    else:
        if weapon_bar.collidepoint(pos):
            bag_open = True
        if store_button.collidepoint(pos):
            step_store = 1
        else:
            if not step_store in range(1, 11) and not bag_open:# 即未在商店和背包
                current_weapon.attack(pos)
            else:
                global weapons
                count = 2 #标识第几个武器
                for i in weapons:
                    if i.collidepoint(pos):
                        if i in bag_weapons:
                            weapons_on_bar[current_weapon_id] = i
                            current_weapon_id = (current_weapon_id+1)%2
                            current_weapon = weapons_on_bar[current_weapon_id]
                        else:
                            step_store = count
                    count += 1
                if Pur_button.collidepoint(pos) and not bag_open:
                    purchase_judge(step_store)

def on_key_down(key):
    global step
    step = 0
    if key == keys.K_1:
        step = 1
        #gamemode()
    elif key == keys.K_2:
        FM.close()
        FW.close()
        FG.close()
        exit()

#### 切换武器
def on_key_up(key):
    global current_weapon_id, current_weapon
    if key == keys.Q:
        current_weapon_id = (1 + current_weapon_id) % 2
        current_weapon = weapons_on_bar[current_weapon_id]

########################draw函数###########################


def draw():
    global step, isLoose, game, WIDTH, HEIGHT, LEVEL
    screen.fill('white')
    if step != 1 and step != 2:
        WIDTH = surface.width
        HEIGHT = surface.height
        surface.draw()
        screen.draw.text(" Welcome to the Game of Purifier\n\n"
                         " Press Number 1 to start the new game\n\n"
                         " Press Number 2 to exit the game\n\n", (350, 500), fontsize=60, color="darkgoldenrod")
    else:
        game = True
    if game:
        WIDTH = background1.width
        HEIGHT = background1.height
        screen.clear()
        screen.fill('white')
        background1.draw()
        hero.draw()
        screen.draw.text("Press Number 2 to exit the game", (800, 20), fontsize=25, color='orange')
        for monster in monsters:
            monster.draw()
            screen.draw.filled_rect(monster.HP_bar, 'gray')
            screen.draw.filled_rect(monster.currentHP_bar, 'black')


        if step == 2:
            isLoose = True
            screen.clear()
            screen.fill('white')
            screen.draw.text("You have lost your game, please exit!", (300, 300), fontsize=50, color="orange")
            FM.close()
            FW.close()
            FG.close()
            clock.schedule(exit, 3)

        ### 上下左右移动模块 ####
        if step == 4 or step == 5 or step == 6 or step == 7:

            background1.draw()

            for monster in monsters:
                monster.draw()
                screen.draw.filled_rect(monster.HP_bar, 'gray')
                screen.draw.filled_rect(monster.currentHP_bar, 'red')


            hero.draw()

            if step == 4:
                clock.schedule(right_movement, 0.01)
            if step == 5:
                clock.schedule(left_movement, 0.01)
            if step == 6:
                clock.schedule(up_movement, 0.01)
            if step == 7:
                clock.schedule(down_movement, 0.01)


    # 游戏进行中
    if step in range(0, 8): 
        if len(boxes) == 0 and len(monsters) == 0 and no_boss:
            send.draw()
            if hero.colliderect(send):
                LEVEL += 1
                construct_level()
        for box in boxes:
            box.draw()

        #HP、金币状态绘制
        draw_status_bar()
        draw_coins_bar()

        # 商店图标
        store_button.draw()

        if LEVEL == 4 and not no_boss:
            boss.draw()
            boss_currentHP_bar = Rect(
                (787, 26), (235 * boss.HP.current_HP / boss.HP.full_HP, 13))  #当前血量
            screen.blit('status_bar', (780, 20))
            screen.draw.filled_rect(boss_currentHP_bar, 'green')
            if boss.magic_on:
                boss.magic.draw()
        
        hero.draw()

        # 子弹绘制
        for i in bullets:
            i.draw()
        for i in monster_bullets:
            i.draw()

        #武器槽绘制
        weapon_bar.draw()
        screen.blit(weapons_on_bar[0].image, (285, 26))
        screen.blit(weapons_on_bar[1].image, (323, 26))
        frame1 = Rect((285, 24), (34, 34))
        frame2 = Rect((323, 24), (34, 34))
        if current_weapon_id == 0:
            screen.draw.rect(frame1, 'red')
        else:
            screen.draw.rect(frame2, 'red')
    

    # 背包绘制
    if bag_open:
        bag.draw()
        bag.pos = (500,300)
        for w in weapons:
            w.draw()

    #商店图标绘制
    store_button.pos= WIDTH-50, 50#(WIDTH-50,HEIGHT-50)
    if step_store == 1:
        store_inner.draw()
        store_inner.pos = (500,300)
        for w in weapons:
            w.draw()
        fuzi.pos = (370,240)
        gong1.pos = (405,240)
        gong2.pos = (445,240)
        jian1.pos = (480,240)
        jian2.pos = (520,240)
        qiang1.pos = (560,240)
        qiang2.pos = (590,240)
        changmao1.pos = (630,240)
        changmao2.pos = (370,280)
    #购买点击图标
    x0,y0 = 400,150
    x1,y1 = 400,200
    x2,y2 = 500,300

    if step_store in range(2,11) and not bag_open:
        Pur_button.draw()
        Pur_button.pos = (x2,y2)
        screen.draw.text("Price: %d "%weapons[step_store-2].price,(x1,y1),fontsize=50,color = "gold")
        screen.draw.text(weapons[step_store-2].Note,(x0, y0),fontsize=50,color = "gold")

    if step_store1 == 20:
        screen.draw.text("Your coins are not ENOUGH!",(300,400),fontsize=50,color = "red")

    ####################update函数#################################

def update():
    global step, hero, game, current_MP, current_weapon, boxes, no_boss
    if game:
        if keyboard.D:
            hero.x += HERO_SPEED
            if hero.x >= WIDTH:
                hero.x = WIDTH - 30
            step = 4
        elif keyboard.A:
            if hero.x < 0:
                hero.x = 0 + 30
            hero.x -= HERO_SPEED
            step = 5
        elif keyboard.W:
            if hero.y < 0:
                hero.y = 0 + 30
            hero.y -= HERO_SPEED
            step = 6
        elif keyboard.S:
            if hero.y >= HEIGHT:
                hero.y = HEIGHT - 30
            hero.y += HERO_SPEED
            step = 7

        current_weapon = weapons_on_bar[current_weapon_id]
        if current_MP < full_MP:
            current_MP += MP_RECOVERY_SPEED
        if LEVEL == 4 and not no_boss:
            # 自动追踪弹
            if hero.distance_to(boss.center) < 400 and boss.timer == 0:
                b = Bullet('fireball', 450, 0.5, 1, 180)
                tls = [boss.pos1, boss.pos2]
                b.pos = random.choice(tls)
                b.trace = True
                monster_bullets.append(b)
            boss.timer = (boss.timer + 1) % 30

        #####子弹更新模块#####
        for i in bullets:
            if i.trace:
                chase(i, i.target)
            else:
                i.x += i.speed_x
                i.y += i.speed_y
            i.count_time += 1
            if(i.count_time >= i.distance/STANDARD_SPEED**1.5):
                bullets.remove(i)
            for monster in monsters:
                if monster.colliderect(i):
                    monster.HP.current_HP -= i.damage
                    if i.image == '箭_ice':
                        clock.schedule(monster.reset_speed_rate, 3)
                        monster.speed_rate *= 0.8
                    if i.image != '长矛2_bullet':
                        bullets.remove(i)
                    tone.play('A1', 0.1)
                    monster.animate_shake()
                if monster.HP.isdead():
                    monsters.remove(monster)
            if LEVEL == 4:
                if boss.colliderect(i):
                    boss.HP.current_HP -= i.damage
                    bullets.remove(i)
                if boss.HP.isdead():
                    no_boss = True
                    clock.unschedule(boss_attack)     
            '''
            elif i.special == 2:
                ang = math.arctan(math.sin(811-i.x)) + 180
                i.speed_x = STANDARD_SPEED **1.5 * math.cos(math.radians(ang) * i.speed_rate
                i.speed_y = -STANDARD_SPEED**1.5 * math.sin(math.radians(ang) * i.speed_rate
            '''        
        for i in monster_bullets:
            if i.trace == 1:
                chase(i, hero)

            else:            
                i.x += i.speed_x
                i.y += i.speed_y
            i.count_time += 1
            if(i.count_time >= i.distance/STANDARD_SPEED**1.5):
                monster_bullets.remove(i)
            if hero.colliderect(i):
                hero_HP.current_HP -= i.damage
                monster_bullets.remove(i)
        
        for monster in monsters:
            # 在一定距离内怪兽使用火球术 ~
            if monster.distance_to(hero) < 200 and random.randint(1, 120) == 1:
                monster.attack()
            # 怪兽的状态更新
            monster.move()

        # 画箱子
        for box in boxes:
            if hero.colliderect(box) and box.open == False:
                box.open_box()


    #### 碰撞伤害 ######
    for monster in monsters:
        if hero.colliderect(monster):
            #tone.play('G2', 0.1)
            hero_HP.current_HP -= monster.clash_damage
    if not no_boss and hero.colliderect(boss):
            #tone.play('G2', 0.1)
            hero_HP.current_HP -= 0.1



######游戏开始对白界面##########
def gamemode():
    global step, game
    while not game:
        # 有两个参数，第一个是文字，第二个是标题
        g.msgbox('公元前2020年，王国遭遇了一场前所未有的新型瘟疫。\n'
                 '越来越多的人染上瘟疫，一时间，民不聊生。\n'
                 '一个自称神奇博士的人找到他，声称这场瘟疫是远方山洞的一条恶龙所为，而恶龙身上的鳞片则是瘟疫的解药。\n'
                 '为了解救人民，王浩然带上最好的武器，踏上了征程。', '前情概要', ok_button='继续')

        # 选择
        # 想要导入图片, 我先看看什么办法，现在无法导入gif图片，有解决办法告诉你
        g.msgbox(msg='你是王浩然，一名b大学生，最近正为了暑校typhon课程的大作业忙得昏头昏脑。\n'
                     '这天，一名自称来自公元前2020年的神奇博士找到了你！', title='身份介绍', image='images\prince.png', ok_button='听他说')
        g.msgbox(msg='   王浩然！\n'
                     '只有你才能突破封印，进入恶龙的洞穴，拿到解药，解救大家啊！', title='神奇博士', image='images\professor.png', ok_button=('继续听他啰嗦'))
        g.msgbox(msg='拜托。我只是个学生。\n'
                     '还有，虽然我很中二，但是不二。别拿这么假的骗术糊弄我！！！', title='王浩然', image='images\prince.png', ok_button='转身离去')
        g.msgbox(msg='你身上流淌着勇者的血脉，应当肩负起拯救人民的重任。\n'
                     '哎，你别走啊。我费了老大劲穿越回来找你的！', title='神奇博士', image='images\professor.png', ok_button='一把拉住王浩然')
        g.msgbox(msg='什么勇者的血脉……\n'
                     '还穿越？你小说看多了吧！', title='王浩然', image='images\prince.png', ok_button='挣脱着想要离开')
        g.msgbox(msg='你知道你的父亲叫什么吗？', title='神奇博士', image='images\professor.png', ok_button='生气的甩开王浩然')
        g.msgbox(msg='真是越说越离谱了，没什么事我去敲代码了。\n'
                     '虽然你是个骗子，不过挺有趣的。赶紧去大医院看看脑子哈！', title='王浩然', image='images\prince.png', ok_button='同情地拍了拍神奇博士')
        g.msgbox(msg='你的父亲俗名叫王建国，\n'
                     '其实他还有另一个名字，达拉崩吧斑得贝迪卜多比鲁翁，\n'
                     '……\n'
                     '他斩杀了恶龙，成功地救出了公主，也就是你的母亲。\n'
                     '你的母亲叫米娅莫拉苏娜丹妮谢莉红。', title='神奇博士', image='images\professor.png', ok_button='一脸自信地点点头')
        g.msgbox(msg='………………', title='', image='images\prince.png', ok_button='一脸茫然')
        g.msgbox(msg='你跟我来！', title='', image='images\professor.png', ok_button='拉着王浩然向有名湖旁的小树林走去')

        # 选择
        if g.ccbox('请做出决定', '', choices=('跟他去一探究竟', '不去不去，他是个大骗子')):
            return
        # 退出程序
        else:
            sys.exit(0)


###########################################

################结束游戏对白################
def endgamemode():
    global End, step
    if End:
        g.msgbox('恭喜您，打败恶龙昆图库塔卡提考特苏瓦西拉松\n'
                 '的儿子\n'
                 '尼普坤图库塔卡提考特苏瓦西拉松，\n'
                 '赢得了解药！！！', '', image='images\medicine.png', ok_button='带解药回城')
        g.msgbox(msg='你带着解药回到了蒙达鲁克硫斯伯古比奇巴勒城。\n'
                     '见到了达拉崩吧斑得贝迪卜多比鲁翁和米娅莫拉苏娜丹妮谢莉红', title='', image='images\dog.png', ok_button='上前')
        g.msgbox(msg='欸？您好！\n'
                     '达拉崩吧斑得贝迪卜多比鲁翁陛下，米娅莫拉苏娜丹妮谢莉红王后\n'
                     '解药也拿到了，我怎么回去啊？', title='王浩然', image='images\prince.png', ok_button='单膝跪地')
        g.msgbox(msg='孩子，\n'
                     '妈妈好想你啊！', title='米娅莫拉苏娜丹妮谢莉红王后', image='images\couple.png', ok_button='抱住王浩然痛哭')
        g.msgbox(msg='孩子，\n'
                     '谢谢你为我们的王国找回解药。\n', title='达拉崩吧斑得贝迪卜多比鲁翁', image='images\couple.png', ok_button='拍拍王浩然的肩膀')
        g.msgbox(msg='那\n'
                     '我怎么回去啊？\n'
                     '我作业还没写完呢！', title='王浩然', image='images\prince.png', ok_button='焦急')
        g.msgbox(msg='这个嘛，神奇博士会带你回去的！\n'
                     '我知道，你们的那个世界也在经历着一场瘟疫。\n'
                     '我希望，你能明白，现实的世界就和这场梦一样，\n'
                     '只要你们勇敢地与病毒战斗，只要你们齐心协力，胜利终将到来！', title='达拉崩吧斑得贝迪卜多比鲁翁', image='images\couple.png',
                 ok_button='微笑着点点头')
        g.buttonbox(msg='你认为你是在做梦吗？\n', title='王浩然', choices=('相信自己就是在做梦', '不可能，这一定是真实的'))
        g.msgbox(msg='王浩然！！！\n'
                     '你在干嘛啊？\n'
                     '代码写完了吗？\n'
                     'ddl就要到了！！！', title='暑校python微信群', ok_button='原来你就是在做梦')
        g.msgbox(msg='2020年7月13日0：01', title='时间', ok_button='大作业还没交呢！！！')

        # 选择
        if g.ccbox('请做出选择', '', choices=('不管了，再来一局', '退出游戏，滚去学习')):

            #####有bug
            step = 1  # 进入游戏界面
        # 退出程序
        else:
            sys.exit(0)


pgzrun.go()
