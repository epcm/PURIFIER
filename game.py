import pgzrun
import csv
import random
# import numpy as math
import math
import easygui as g
import sys

TITLE = "The Game of Purifier"
FM = open('Monsters.csv', encoding='utf-8-sig')
FW = open('Weapons.csv', encoding='utf-8-sig')
FG = open('GlobalConst.csv', encoding='utf-8-sig')
# music.play('达拉崩吧')
pos = [(1000, 400), (1000, 300), (1000, 400), (1500, 600)]
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
            hero.pos = (100, 300)
            return
        else:
            return True


class Monster(Actor):
    # 参数传入亦可改写为args，更简洁美观，不过可读性下降
    def __init__(self, image, full_HP, attack_distance, attack_damage, clash_damage, speed_rate, bullet_image,
                 bullet_speed_rate, autochase_distance):
        super().__init__(image)
        self.list = []
        self.HP = HP(float(full_HP), 1)  # 血量类
        self.HP_bar = Rect((0, 0), (28, 5))  # 满血条
        self.currentHP_bar = Rect((0, 0), (28, 5))  # 血条
        self.speed_rate = float(speed_rate)  # 移动速度
        self.speed_x = random.choice([1, -1]) * STANDARD_SPEED * self.speed_rate
        self.speed_y = random.choice([1, -1]) * STANDARD_SPEED * self.speed_rate  # 速度
        self.attack_distance = float(attack_distance)  # 攻击距离
        self.attack_damage = float(attack_damage)  # 攻击伤害
        self.beaten = False  # 击退状态
        self.bullet_image = bullet_image  # 攻击图像
        self.clash_damage = float(clash_damage)  # 接触伤害
        self.autochase_distance = float(autochase_distance)  # 自动追逐距离
        self.bullet_speed_rate = float(bullet_speed_rate)  # 发射攻击速度

    # 怪兽在被击退后重获速度
    def recover(self):
        self.beaten = False

    def attack(self):
        b = Bullet(self.bullet_image, self.attack_distance, self.attack_damage, self.bullet_speed_rate,
                   self.angle_to(hero))
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

                self.speed_x = STANDARD_SPEED ** 1.5 * math.cos(math.radians(self.angle_to(hero))) * self.speed_rate
                self.speed_y = -STANDARD_SPEED ** 1.5 * math.sin(math.radians(self.angle_to(hero))) * self.speed_rate
                self.x += self.speed_x
                self.y += self.speed_y
                '''## 注意以下模块中speed维持非负
                if self.x > hero.x:
                    self.x -= self.speed_x
                elif self.x < hero.x:
                    self.x += self.speed_x
                else:
                    self.speed_y = STANDARD_SPEED ** 1.5 * self.speed_rate
                self.speed_x = STANDARD_SPEED

                if self.y > hero.y:
                    self.y -= self.speed_y
                elif self.y < hero.y:
                    self.y += self.speed_y
                else:
                    self.speed_x = STANDARD_SPEED ** 1.5 * self.speed_rate
                self.speed_y = STANDARD_SPEED'''
            else:
                # 平均2s一次的随机转向
                if random.randint(1, 120) == 1:
                    # ang = random.randint(-180, 180)
                    ang = random.randint(0, 360)  # choice([0, 45, 90, 135, 180, 225, 270, 315])
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
        animate(self, duration=0.1, angle=30)
        clock.schedule(self.shake2, 0.1)
        clock.schedule(self.shake3, 0.3)
        clock.schedule(self.recover, 0.2)
        tone.play('A2', 0.1)

    def shake2(self):
        animate(self, duration=0.2, angle=-30)

    def shake3(self):
        animate(self, duration=0.1, angle=0)

    # 从迟缓状态恢复
    def reset_speed_rate(self):
        self.speed_rate /= 0.8


class Weapon(Actor):
    def __init__(self, image, type, distance, damage, price, MP_consuming, bullet_image, speed_rate, Note):
        super().__init__(image)
        self.type = int(type)  # 1为近战武器，2为远程武器
        self.distance = float(distance)  # 攻击距离
        self.damage = float(damage)  # 伤害
        self.price = float(price)  # 价格
        self.MP_consuming = float(MP_consuming)  # MP消耗
        self.bullet_image = bullet_image  # 子弹图像
        self.speed_rate = float(speed_rate)  # 子弹速度
        self.Note = Note  # 武器信息

    def attack(self, pos):
        global current_MP
        if self.MP_consuming > current_MP:
            return
        current_MP -= self.MP_consuming
        # 近战武器
        if self.type == 1:
            # clock.schedule_interval(animate_chop, 1)
            for monster in monsters:
                if hero.distance_to(monster) < self.distance:
                    ang = hero.angle_to(monster)
                    if ((step == 4 and -60 < ang < 60) or
                            (step == 5 and (120 < ang < 180 or -180 < ang < -120)) or
                            (step == 6 and 30 < ang < 150) or
                            (step == 7 and -150 < ang < -30)):
                        monster.HP.current_HP -= self.damage
                        if step == 4:
                            monster.x += STANDARD_SPEED * 10
                        elif step == 5:
                            monster.x -= STANDARD_SPEED * 10
                        elif step == 6:
                            monster.y -= STANDARD_SPEED * 10
                        elif step == 7:
                            monster.y += STANDARD_SPEED * 10
                        monster.HP.current_HP -= self.damage
                        if monster.HP.isdead():
                            monsters.remove(monster)
                            global Total
                            Total -= 1
                        monster.animate_shake()
                        monster.beaten = True

        # 远程武器
        elif self.type == 2:
            b = Bullet(self.bullet_image, self.distance, self.damage, self.speed_rate, hero.angle_to(pos))
            b.pos = hero.pos
            bullets.append(b)
            if self is qiang1:
                b1 = Bullet(self.bullet_image, self.distance, self.damage, self.speed_rate, hero.angle_to(pos) + 20)
                b2 = Bullet(self.bullet_image, self.distance, self.damage, self.speed_rate, hero.angle_to(pos) - 20)
                b1.pos = hero.pos
                b2.pos = hero.pos
                bullets.append(b1)
                bullets.append(b2)
            elif self is changmao1:
                mindis = 10000
                for monster in monsters:
                    dis = monster.distance_to(hero)
                    if dis < mindis:
                        mindis = dis
                        b.target = monster


class Bullet(Actor):
    def __init__(self, image, distance, damage, speed_rate, ang):
        super().__init__(image)
        self.damage = damage
        self.distance = distance
        self.angle = ang
        self.speed_x = STANDARD_SPEED ** 1.5 * math.cos(math.radians(ang)) * speed_rate
        self.speed_y = -STANDARD_SPEED ** 1.5 * math.sin(math.radians(ang)) * speed_rate
        self.count_time = 0  # 计时工具
        self.target = None  # 长矛1的跟踪对象
        self.speed_rate = speed_rate


'''# 近战动画
image_count = 1
def animate_chop():
    global image_count
    if(step == 4):
        hero.image = "prince_right_斧子{}".format(image_count)
    image_count += 1
    if image_count > 3:
        clock.unschedule(animate_chop)
        image_count = 1'''

##################全局变量global##########################
FGreader = csv.DictReader(FG)
dic = next(FGreader)

# 武器模块
# 参数依次为 image, type, distance, damage, price, MP_consuming
ls = list(csv.reader(FW))
fuzi = Weapon(*ls[1])
gong1 = Weapon(*ls[2])
gong2 = Weapon(*ls[3])  # 半透明代表未拥有
jian1 = Weapon(*ls[4])
jian2 = Weapon(*ls[5])
qiang1 = Weapon(*ls[6])
qiang2 = Weapon(*ls[7])
changmao1 = Weapon(*ls[8])
changmao2 = Weapon(*ls[9])
fuzi.pos = (370, 240)
gong1.pos = (405, 240)
gong2.pos = (445, 240)
jian1.pos = (480, 240)
jian2.pos = (520, 240)
qiang1.pos = (560, 240)
qiang2.pos = (590, 240)
changmao1.pos = (630, 240)
changmao2.pos = (370, 280)

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
bag.pos = 500, 300
bag_weapons = [fuzi, gong1]  # 已经拥有的武器
bag_open = False

# 武器
weapons = [fuzi, gong1, gong2, jian1, jian2, qiang1, qiang2, changmao1, changmao2]

# 金币，商店页面控制
coins = int(dic['coins'])
step_store = 0
step_store1 = 0

# 武器商店模块
store_button = Actor("store_button")
store_inner = Actor("store")
Pur_button = Actor("purchase")

# 标准速度
STANDARD_SPEED = float(dic['STANDARD_SPEED'])

# 地图与背景
background1 = Actor("bg1")  # 896, 448
background1.topleft = 0, 0  # background1.pos = 500, 300
boss = Actor("dinosaur")
boss.pos = 400, 400
WIDTH = background1.width  # + 100
HEIGHT = background1.height  # + 300

# 在场角色
hero = Actor("prince")
hero.pos = 100, 300
hero_HP = HP(float(dic['HP']), int(dic['LIFE']))  # 初始化王子HP
full_MP = float(dic['MP'])
HERO_SPEED = float(dic['HERO_SPEED'])
HERO_SPEED_DICT = {4: (HERO_SPEED, 0), 5: (-HERO_SPEED, 0), 6: (0, -HERO_SPEED), 7: (0, HERO_SPEED)}
current_MP = full_MP
MP_RECOVERY_SPEED = float(dic['MP_RECOVERY_SPEED'])  # 每次刷新的MP恢复量
monsters = []

# 游戏控制
isLoose = False
start = False
game = False
step = 99
Total = 0 #场上剩余怪物
BoxTotal = 0 #场上开了的盒子要和n相同

# 箱子部分
n = int(dic['box_num'])
m = n
print(f"box_set", n)
boxes = []
for _ in range(n):
    boxes.append(Actor('box_close'))

'''class Actor(boxes):
    def __init__(self):
        self.open = False

    def open(self):
        pass'''


send = Actor('传送门')
background1 = Actor('bg1')
send.bottomright = 1200, 450  # send.pos = 700, 500

#set是记录填充了的盒子
set = [0] * n
def Fill_box():
    for i in range(n):
        a = random.randint(100, 800)
        b = random.randint(150, 430)  # (150, 600)
        boxes[i].x = a
        boxes[i].y = b
        set.insert(i, 1)


################各类函数##############################
ls = list(csv.reader(FM))


def open_box():
    global check, coins, Total, BoxTotal
    j = check
    bit = random.randint(0, 30)
    if bit % 5 == 0:
        boxes[j].image = 'box_open'
        mon = Monster(*ls[1])
        mon.pos = boxes[j].pos
        monsters.append(mon)
        Total += 1
        BoxTotal += 1
    elif bit % 5 == 1:
        mon = Monster(*ls[2])
        mon.pos = boxes[j].pos
        monsters.append(mon)
        Total += 1
        BoxTotal += 1
    elif bit % 5 == 2:
        mon = Monster(*ls[3])
        mon.pos = boxes[j].pos
        monsters.append(mon)
        Total += 1
        BoxTotal += 1
    elif bit % 5 == 3 or bit % 5 == 4:
        boxes[j].image = 'gloden2'
        BoxTotal += 1
    set[j] = 1
    if boxes[j].image == 'gloden2':
        number = random.randint(20, 40)
        coins += number


# 画血条和蓝条
def draw_status_bar():
    global step
    if (hero_HP.isdead()):
        step = 3
    currentHP_bar = Rect(
        (27, 26), (235 * hero_HP.current_HP / hero_HP.full_HP, 13))  # 当前血量
    screen.blit('status_bar', (20, 20))
    screen.draw.filled_rect(currentHP_bar, 'red')

    currentMP_bar = Rect(
        (27, 54), (235 * current_MP / full_MP, 13))  # 当前血量
    screen.blit('status_bar', (20, 48))
    screen.draw.filled_rect(currentMP_bar, 'blue')


# 画金币
def draw_coins_bar():
    screen.blit('gloden', (20, 80))  # 20,60
    screen.draw.text(str(coins), (125, 97), fontsize=50, color='gold')  # 125 77


### 上下左右行走模块函数 ###
def left_movement():
    hero.image = f"prince_left_{current_weapon.image}"


def right_movement():
    hero.image = f"prince_right_{current_weapon.image}"


def up_movement():
    hero.image = "prince_back"


def down_movement():
    hero.image = f"prince_{current_weapon.image}"


# 商店的购买判断
def purchase_judge(n):
    global coins, step_store1, step_store
    if coins < weapons[step_store - 2].price:
        step_store1 = 20
        clock.schedule(reset_step_store1, 2)
    else:
        key = weapons[step_store - 2]
        key.image = f'{key.image[:-6]}'  # 将半透明图像替换为不透明图像
        coins = coins - weapons[step_store - 2].price
        bag_weapons.append(key)
        step_store = 1


# 用于clock.schedule调用，清除金钱不够的信息
def reset_step_store1():
    global step_store1
    step_store1 = 0


############按键与鼠标#########################

def on_mouse_down(pos, button):
    global coins
    global step_store, bag_open, current_weapon, current_weapon_id, weapons_on_bar
    if button == mouse.RIGHT:
        if step_store in range(2, 11):
            step_store = 1  # 返回商店初始界面
        else:
            step_store = 12  # 退出商店
        bag_open = False
    else:
        if weapon_bar.collidepoint(pos):
            bag_open = True
        if store_button.collidepoint(pos):
            step_store = 1
        else:
            if not step_store in range(1, 11) and not bag_open:  # 即未在商店和背包
                current_weapon.attack(pos)
            else:
                global weapons
                count = 2  # 标识第几个武器
                for i in weapons:
                    if i.collidepoint(pos):
                        if i in bag_weapons:
                            weapons_on_bar[current_weapon_id] = i
                            current_weapon_id = (current_weapon_id + 1) % 2
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
        gamemode()
    elif key == keys.K_2:
        step = 2
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

Firstround, Secondround, Thirdround, Finalround, End = True, False, False, False, False


def draw():
    global step, isLoose, start, game, WIDTH, HEIGHT, Firstround, Secondround, Thirdround, Finalround
    screen.fill('white')
    if step != 1 and step != 2:
        WIDTH = surface.width
        HEIGHT = surface.height
        surface.draw()
        screen.draw.text(" Welcome to the Game of Purifier\n\n"
                         " Press Number 1 to start the new game\n\n"
                         " Press Number 2 to exit the game\n\n", (350, 500), fontsize=60, color="darkgoldenrod")
        start = False
    else:
        start = True
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
        send.draw()

        if step == 2:
            isLoose = True
            screen.clear()
            screen.fill('white')
            screen.draw.text("You have lose your game, please exit!", (300, 300), fontsize=50, color="orange")
            FM.close()
            FW.close()
            FG.close()
            clock.schedule(exit, 3)

        ### 上下左右移动模块 ####
        if step == 4 or step == 5 or step == 6 or step == 7:
            print(f"MonsterTotal:", Total)
            print(f"BoxTotal:", BoxTotal)
            background1.draw()
            if Finalround:
                boss.draw()
            for monster in monsters:
                monster.draw()
                screen.draw.filled_rect(monster.HP_bar, 'gray')
                screen.draw.filled_rect(monster.currentHP_bar, 'red')

            hero.draw()
            if step == 4:
                clock.schedule(right_movement, 0.1)
            if step == 5:
                clock.schedule(left_movement, 0.1)
            if step == 6:
                clock.schedule(up_movement, 0.1)
            if step == 7:
                clock.schedule(down_movement, 0.1)

    # 游戏进行中
    if step in range(1, 8):
        for i in range(n):
            boxes[i].draw()
        send.draw()

        # HP、金币状态绘制
        draw_status_bar()
        draw_coins_bar()

        # 商店图标
        store_button.draw()

        # 子弹绘制
        for i in bullets:
            i.draw()
        for i in monster_bullets:
            i.draw()

        # 武器槽绘制
        weapon_bar.draw()
        screen.blit(weapons_on_bar[0].image, (285, 26))
        screen.blit(weapons_on_bar[1].image, (323, 26))

    # 背包绘制
    if bag_open:
        bag.draw()
        bag.pos = (500, 300)
        for w in weapons:
            w.draw()

    # 商店图标绘制
    store_button.pos = WIDTH - 50, 50  # (WIDTH-50,HEIGHT-50)
    if step_store == 1:
        store_inner.draw()
        store_inner.pos = (500, 300)
        for w in weapons:
            w.draw()
        fuzi.pos = (370, 240)
        gong1.pos = (405, 240)
        gong2.pos = (445, 240)
        jian1.pos = (480, 240)
        jian2.pos = (520, 240)
        qiang1.pos = (560, 240)
        qiang2.pos = (590, 240)
        changmao1.pos = (630, 240)
        changmao2.pos = (370, 280)
    # 购买点击图标
    x0, y0 = 400, 150
    x1, y1 = 400, 200
    x2, y2 = 500, 300

    if step_store in range(2, 11) and not bag_open:
        Pur_button.draw()
        Pur_button.pos = (x2, y2)
        screen.draw.text("Price: %d " % weapons[step_store - 2].price, (x1, y1), fontsize=50, color="gold")
        screen.draw.text(weapons[step_store - 2].Note, (x0, y0), fontsize=50, color="gold")

    if step_store1 == 20:
        screen.draw.text("Your coins are not ENOUGH!", (300, 400), fontsize=50, color="red")

    ####################update函数#################################


def update():
    global step, hero, game, check, current_MP, current_weapon, Total, BoxTotal, m, Firstround, Secondround, Thirdround, Finalround, End, boxes, boss
    # 往右走
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

        #####子弹更新模块#####
        for i in bullets:
            if i.image == '长矛1_bullet':
                ang = i.angle_to(i.target)
                i.speed_x = STANDARD_SPEED ** 1.5 * math.cos(math.radians(ang))
                i.speed_y = -STANDARD_SPEED ** 1.5 * math.sin(math.radians(ang))
                i.angle = ang
            i.x += i.speed_x
            i.y += i.speed_y
            i.count_time += 1
            if (i.count_time >= i.distance / STANDARD_SPEED ** 1.5):
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
                    global Total
                    Total -= 1

        for i in monster_bullets:
            i.x += i.speed_x
            i.y += i.speed_y
            i.count_time += 1
            if (i.count_time >= i.distance / STANDARD_SPEED ** 1.5):
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

        # 画箱子函数
        for j in range(n):
            if hero.colliderect(boxes[j]) and set[j] == 1:
                check = j
                boxes[j].image = 'box_open'
                clock.schedule_unique(open_box, 0.1)

        ###############画地图函数############
        if Firstround:
            Fill_box()
            send.pos = pos[0][0], pos[0][1]
            background1.image = 'bg1'
            if hero.colliderect(send) and Total == 0 and BoxTotal == 10:
                Fill_box()
                BoxTotal = 0
                boxes.clear()
                Secondround = True

        if Secondround:
            send.pos = pos[1][0], pos[1][1]
            background1.image = 'bg2'
            if hero.colliderect(send) and Total == 0 and BoxTotal == 10:
                Fill_box()
                BoxTotal = 0
                boxes.clear()
                Thirdround = True

        if Thirdround:
            send.pos = pos[2][0], pos[2][1]
            background1.image = 'bg3'
            if hero.colliderect(send) and Total == 0 and BoxTotal == 10:
                Fill_box()
                BoxTotal = 0
                boxes.clear()
                Finalround = True
                endgamemode()

        if Finalround:
            Boss()
        ################################################aa
    #### 简单的四边跑 ######
    for monster in monsters:
        if hero.colliderect(monster):
            # tone.play('G2', 0.5)
            hero_HP.current_HP -= monster.clash_damage
        for i in range(3):
            if hero.colliderect(boxes[i]):
                boxes[i].image = 'box_open'

###Boss绘画####
def Boss():
    r = random.randint(0, 30)
    if r % 5 == 0:
        boss.image = 'dinosaur'
    elif r % 5 == 1:
        boss.image = 'boss1'
    elif r % 5 == 2:
        boss.image = 'dragon1_l'
    elif r % 5 == 3:
        boss.image = 'dragon2_l'
    elif r % 5 == 4:
        boss.image = 'dragon3_l'


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
