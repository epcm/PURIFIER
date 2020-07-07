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

class weapon(Actor):
    def __init__(self, image, type, distance, damage, price):
        super().__init__(image)
        self.type = type # 1为近战武器，2为远程武器
        self.distance = distance
        self.damage = damage
        self.price = price
    
    def attack(self, pos):
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
            b.pos = hero.pos
            bullets.append(b)

class bullet(Actor):
    def __init__(self, distance, damage, ang):
        super().__init__('子弹特效1')
        self.damage = damage
        self.distance = distance
        self.angle = ang
        self.speed_x = standard_speed ** 1.5 *math.cos(math.radians(ang))
        self.speed_y = -standard_speed ** 1.5 *math.sin(math.radians(ang))
        self.count_time = 0 #计时工具


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


# 武器模块
#image, type, distance, damage, price
fuzi = weapon("斧子", 1, 100, 1, 2)
gong1 = weapon("弓1", 2, 300, 2, 1)
gong2 = weapon("弓2_trans", 2, 500, 3, 2)
jian1= weapon("剑1_trans", 1, 100, 1, 2)
jian2 = weapon("剑2_trans", 1, 100, 1, 2)
qiang1 = weapon("枪1_trans", 2, 100, 1, 2)
qiang2 = weapon("枪2_trans", 2, 100, 1, 2)
changmao1 = weapon("长矛1_trans", 1, 100, 1, 2)
changmao2 = weapon("长矛2_trans", 1, 100, 1, 2)
fuzi.pos = (370,240)
gong1.pos = (405,240)
gong2.pos = (445,240)
jian1.pos = (480,240)
jian2.pos = (520,240)
qiang1.pos = (560,240)
qiang2.pos = (590,240)
changmao1.pos = (630,240)
changmao2.pos = (370,280)

#背包与武器槽模块
weapon_bar = Actor('weapon_bar')
weapons_on_bar = [fuzi, gong1]
weapon_bar.pos = 300, 40
bag = Actor('背包')
bag.pos = 500,300
bag_weapons = [fuzi, gong1]
bag_open = False

weapons = [fuzi, gong1, gong2, jian1, jian2, qiang1, qiang2, changmao1, changmao2]
current_weapon_id = 0
current_weapon = weapons_on_bar[current_weapon_id]


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

# 箱子部分
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

coins = 10
step_store = 0
step_store1 = 0


WIDTH = background1.width + 100
HEIGHT = background1.height + 100
step = 99

monster.x = WIDTH / 2
monster.y = HEIGHT / 2


def game_over():
    pass


# 画血条
def draw_hp_bar():
    global step
    if (prince_HP.isdead()):
        step = 3
    HPBar = Rect((20, 20), (200, 35))  #血槽
    CurrentHPBar = Rect(
        (20, 20), (200 * prince_HP.CurrentHP / prince_HP.FullHP, 33))  #当前血量
    screen.draw.rect(HPBar, 'black')
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
    screen.draw.text(str(coins), (125, 77), fontsize=50, color = 'black')  #125 77


### 上下左右行走模块函数 ###
def left_movement():
    hero.image = f"prince_left_{current_weapon.image}"


def right_movement():
    hero.image = f"prince_right_{current_weapon.image}"


def up_movement():
    hero.image = "prince_back"


def down_movement():
    hero.image = f"prince_{current_weapon.image}"


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
            clock.schedule(exit, 3)

    ### 上下左右移动模块 ####
    if step == 4 or step == 5 or step == 6 or step == 7:
        background1.draw()
        monster.draw()
        for i in range(3):
            for i in range(4):
                boxes[i].draw()
        send.draw()


        # 优先级最高
        hero.draw()
        #HP、金币状态绘制
        draw_hp_bar()
        draw_coins_bar()
        # 子弹绘制
        for i in bullets:
            i.draw()
        if step == 4:
            clock.schedule(right_movement, 0.01)
        if step == 5:
            clock.schedule(left_movement, 0.01)
        if step == 6:
            clock.schedule(up_movement, 0.01)
        if step == 7:
            clock.schedule(down_movement, 0.01)
        
        #背包与武器槽绘制
        weapon_bar.draw()
        screen.blit(weapons_on_bar[0].image, (265, 26))
        screen.blit(weapons_on_bar[1].image, (303, 26))
        if bag_open:
            bag.draw()
            bag.pos = (500,300)
            for w in weapons:
                w.draw()
    #################################
    #商店图表绘制
    store_button.draw()
    store_button.pos=(WIDTH-50,HEIGHT-50)
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
    x1,y1 = 450,200
    x2,y2 = 500,300

    if step_store in range(2,11) and not bag_open:
        Pur_button.draw()
        Pur_button.pos = (x2,y2)
        screen.draw.text("Price: %d "%weapons[step_store-2].price,(x1,y1),fontsize=50,color = "black")

    if step_store1 == 20:
        screen.draw.text("Your coins are not ENOUGH!",(300,400),fontsize=50,color = "red")

    #################################

#武器商店模块
store_button = Actor("store_button")
store_inner = Actor("store")
# weapon = {fuzi1:(2,2), gong1:(1,3), gong2:(2,4), jian1:(1,5), jian2:(3,6), qiang1:(2,7), qiang2:(4,8), changmao1:(2,9), changmao2:(3,10)}
Pur_button = Actor("purchase")


def on_mouse_down(pos, button):
    global coins
    global step_store, bag_open, current_weapon, current_weapon_id, weapons_on_bar
    if button == mouse.RIGHT:
        step_store = 12
        bag_open = False
    else:
        if weapon_bar.collidepoint(pos):
            bag_open = True
        if store_button.collidepoint(pos):
            step_store = 1
        else:
            if not step_store in range(1, 11) and not bag_open:
                current_weapon.attack(pos)
            else:
                global weapons
                count = 2 #标识第几个武器
                for i in weapons:
                    if i.collidepoint(pos):
                        step_store = count
                        if i in bag_weapons:
                            weapons_on_bar[current_weapon_id] = i
                            current_weapon = weapons_on_bar[current_weapon_id]
                            current_weapon_id = (current_weapon_id+1)%2
                    count += 1
                if Pur_button.collidepoint(pos) and not bag_open:
                    purchase_judge(step_store)

def purchase_judge(n):
    global coins, step_store1, step_store
    if coins < weapons[step_store - 2].price:
        step_store1 = 20
        clock.schedule(reset_step_store1, 2)
    else:
        key = weapons[step_store - 2]
        key.image = f'{key.image[:-6]}'#将半透明图像替换为不透明图像
        coins = coins - weapons[step_store - 2].price
        bag_weapons.append(key)
        step_store = 1

# 用于clock.schedule调用，清除金钱不够的信息
def reset_step_store1():
    global step_store1
    step_store1 = 0
#################################################

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
        current_weapon = weapons_on_bar[current_weapon_id]

def update():
    global step, hero, speed_x, speed_y, game, check
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
            i.x += i.speed_x
            i.y += i.speed_y
            i.count_time += 1
            if(i.count_time >= i.distance/standard_speed**1.5):
                bullets.remove(i)
            if monster.colliderect(i):
                global monster_HP
                monster_HP.CurrentHP -= i.damage
                bullets.remove(i)
                tone.play('A1', 0.1)
                animate_shake(monster)
        if monster_HP.isdead():
            monster.x =-50
            monster.y = -50
        ##### 怪兽自己走模块 #####
        # monster.pos = random.randint(0, WIDTH), random.randint(0, HEIGHT)

        #靠近至一定距离时怪兽主动接近
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
                #平均2s一次的随机转向
                if random.randint(1, 120) == 1:
                    #ang = random.randint(-180, 180)
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

    #### 简单的四边跑 ######
    if hero.colliderect(monster):
        pass
        #tone.play('G2', 0.5)
        #prince_HP.CurrentHP -= 0.05
    for i in range(3):
        if hero.colliderect(boxes[i]):
            boxes[i].image = 'box_open'


pgzrun.go()
