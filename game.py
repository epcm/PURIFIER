import pgzrun
import csv
import random
#import numpy as math
import math

FM = open('Monsters.csv', encoding = 'utf-8-sig')
FW = open('Weapons.csv', encoding = 'utf-8-sig')
FG = open('GlobalConst.csv', encoding = 'utf-8-sig')
#music.play('达拉崩吧')

###############类class######################

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
    # 参数传入亦可改写为args，更简洁美观，不过可读性下降
    def __init__(self, image, full_HP, attack_distance,attack_damage,clash_damage,speed_rate,bullet_image,bullet_speed_rate,autochase_distance):
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

    
    # 怪兽在被击退后重获速度
    def recover(self):
        self.beaten = False
    
    def attack(self):
        b = Bullet(self.bullet_image,self.attack_distance, self.attack_damage, self.bullet_speed_rate,self.angle_to(hero))
        b.pos = self.pos
        monster_bullets.append(b)
        
    # 每次uodate时更新怪兽的状态
    def move(self):
        self.HP_bar.topleft = self.x - 11, self.y - 18
        self.currentHP_bar.width = 28*self.HP.current_HP/self.HP.full_HP
        self.currentHP_bar.topleft = self.x - 11, self.y - 18
        #靠近至一定距离时怪兽主动接近
        if not self.beaten:
            if self.distance_to(hero) < self.autochase_distance:
                
                self.speed_x = STANDARD_SPEED **1.5 * math.cos(math.radians(self.angle_to(hero))) * self.speed_rate
                self.speed_y = -STANDARD_SPEED**1.5 * math.sin(math.radians(self.angle_to(hero))) * self.speed_rate
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
        global current_MP
        if self.MP_consuming > current_MP:
            return
        current_MP -= self.MP_consuming
        # 近战武器
        if self.type == 1:
            #clock.schedule_interval(animate_chop, 1)
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
                            global Total
                            Total -= 1
                        monster.animate_shake()
                        monster.beaten = True
        
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
hero_HP = HP(float(dic['HP']), int(dic['LIFE']))  #初始化王子HP
full_MP = float(dic['MP'])
HERO_SPEED = float(dic['HERO_SPEED'])
HERO_SPEED_DICT = {4:(HERO_SPEED, 0), 5:(-HERO_SPEED, 0), 6:(0, -HERO_SPEED), 7:(0, HERO_SPEED)}
current_MP = full_MP
MP_RECOVERY_SPEED = float(dic['MP_RECOVERY_SPEED']) #每次刷新的MP恢复量
monsters = []

# 游戏控制
isLoose = False
start = False
game = False
step = 99
Total = 3

# 箱子部分
n = int(dic['box_num'])
boxes = []
for _ in range(n):
    boxes.append(Actor('box_close'))
send = Actor('传送门')
background1 = Actor('bg1')
send.bottomright = 1200, 450#send.pos = 700, 500


for i in range(n):
    a = random.randint(100, 800)
    b = random.randint(150, 430)#(150, 600)
    boxes[i].x = a
    boxes[i].y = b
    boxes[i].open = False

################各类函数##############################
ls = list(csv.reader(FM))
def open_box():
    global check, coins
    j = check
    bit = random.randint(0, 30)
    if bit % 5 == 0:
        boxes[j].image = 'box_open'
        mon = Monster(*ls[1])
        mon.pos = boxes[j].pos
        monsters.append(mon)
    elif bit % 5 == 1:
        mon = Monster(*ls[2])
        mon.pos = boxes[j].pos
        monsters.append(mon)
    elif bit % 5 == 2:
        mon = Monster(*ls[3])
        mon.pos = boxes[j].pos
        monsters.append(mon)
    elif bit % 5 == 3 or bit % 5 == 4:
        boxes[j].image = 'gloden2'
    boxes[j].open = True
    if boxes[j].image == 'gloden2':
        number = random.randint(20, 40)
        coins += number

# 画血条和蓝条
def draw_status_bar():
    global step
    if (hero_HP.isdead()):
        step = 3
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
    screen.blit('gloden', (20, 80))  #20,60
    screen.draw.text(str(coins), (125, 97), fontsize=50, color = 'gold')  #125 77


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
    elif key == keys.K_2:
        step = 2
    elif key == keys.K_3:
        step = 3
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
        for monster in monsters:
            monster.draw()
            screen.draw.filled_rect(monster.HP_bar, 'gray')
            screen.draw.filled_rect(monster.currentHP_bar, 'black')
        send.draw()

        # elif step == 2:
        if step == 3:
            isLoose = True
            screen.clear()
            screen.fill('white')
            screen.draw.text("You have lose your game, please exit!", (200, 200), fontsize=50, color="orange")
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
        for i in range(n):
            boxes[i].draw()
        send.draw()

        #HP、金币状态绘制
        draw_status_bar()
        draw_coins_bar()

        # 商店图标
        store_button.draw()

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
    global step, hero, game, check, current_MP, current_weapon
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
                i.speed_x = STANDARD_SPEED **1.5 * math.cos(math.radians(ang))
                i.speed_y = -STANDARD_SPEED**1.5 * math.sin(math.radians(ang))
                i.angle = ang
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
                    global Total
                    Total -= 1
        
        for i in monster_bullets:
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

        # 画箱子函数
        for j in range(n):
            if hero.colliderect(boxes[j]) and boxes[j].open == False:
                check = j
                boxes[j].image = 'box_open'
                clock.schedule_unique(open_box, 0.1)

    #### 简单的四边跑 ######
    for monster in monsters:
        if hero.colliderect(monster):
            #tone.play('G2', 0.5)
            hero_HP.current_HP -= monster.clash_damage
        for i in range(3):
            if hero.colliderect(boxes[i]):
                boxes[i].image = 'box_open'


pgzrun.go()
