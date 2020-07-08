import pgzrun
import turtle
import random
import math

music.play('达拉崩吧')

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
    def __init__(self, image, full_HP):
        super().__init__(image)
        self.list = []
        self.HP = HP(full_HP, 1)
        self.HP_bar = Rect((0, 0), (28, 5))
        self.currentHP_bar = Rect((0, 0), (28, 5))
        self.speed_x = random.choice([1, -1]) * standard_speed
        self.speed_y = random.choice([1, -1]) * standard_speed
        self.attack_distance = 250
        self.attack_damage = 1
        self.beaten = False
    
    # 怪兽在被击退后重获速度
    def recover(self):
        self.beaten = False
    
    def attack(self):
        b = Bullet(self.attack_distance, self.attack_damage, self.angle_to(hero))
        b.image = 'fireball'
        b.pos = self.pos
        monster_bullets.append(b)
        
    # 每次uodate时更新怪兽的状态
    def move(self):
        self.HP_bar.topleft = self.x - 11, self.y - 18
        self.currentHP_bar.width = 28*self.HP.current_HP/self.HP.full_HP
        self.currentHP_bar.topleft = self.x - 11, self.y - 18
        #靠近至一定距离时怪兽主动接近
        if not self.beaten:
            if self.distance_to(hero) < 200:
                '''#if random.randint(1,6) == 1:
                self.speed_x = standard_speed**1.5 * math.cos(radians(self.angle_to(hero)))
                self.speed_y = -standard_speed**1.5 * math.sin(radians(self.angle_to(hero)))'''
                ## 注意以下模块中speed维持非负
                if self.x > hero.x:
                    self.x -= self.speed_x
                elif self.x < hero.x:
                    self.x += self.speed_x
                else:
                    self.speed_y = standard_speed ** 1.5
                self.speed_x = standard_speed

                if self.y > hero.y:
                    self.y -= self.speed_y
                elif self.y < hero.y:
                    self.y += self.speed_y
                else:
                    self.speed_x = standard_speed ** 1.5
                self.speed_y = standard_speed

            else:
                #平均2s一次的随机转向
                if random.randint(1, 120) == 1:
                    #ang = random.randint(-180, 180)
                    ang = random.choice([0, 45, 90, 135, 180, 225, 270, 315])
                    self.speed_x = standard_speed ** 1.5 * math.cos(math.radians(ang))
                    self.speed_x = -standard_speed ** 1.5 * math.sin(math.radians(ang))
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

class Weapon(Actor):
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
                        monster.HP.current_HP -= self.damage
                        if step == 4:
                            monster.x += standard_speed*10
                        elif step == 5:
                            monster.x -= standard_speed*10
                        elif step == 6:
                            monster.y -= standard_speed*10
                        elif step == 7:
                            monster.y += standard_speed*10
                        monster.HP.current_HP -= self.damage
                        if monster.HP.isdead():
                            monsters.remove(monster)
                        monster.animate_shake()
                        monster.beaten = True
        
        # 远程武器
        elif self.type == 2:
            b = Bullet(self.distance, self.damage, hero.angle_to(pos))
            b.pos = hero.pos
            bullets.append(b)

class Bullet(Actor):
    def __init__(self, distance, damage, ang):
        super().__init__('子弹特效1')
        self.damage = damage
        self.distance = distance
        self.angle = ang
        self.speed_x = standard_speed ** 1.5 *math.cos(math.radians(ang))
        self.speed_y = -standard_speed ** 1.5 *math.sin(math.radians(ang))
        self.count_time = 0 #计时工具



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

# 武器模块
# 参数依次为 image, type, distance, damage, price
fuzi = Weapon("斧子", 1, 100, 1, 2)
gong1 = Weapon("弓1", 2, 300, 2, 1)
gong2 = Weapon("弓2_trans", 2, 500, 3, 2) # 半透明代表未拥有
jian1= Weapon("剑1_trans", 1, 100, 1, 2)
jian2 = Weapon("剑2_trans", 1, 100, 1, 2)
qiang1 = Weapon("枪1_trans", 2, 100, 1, 2)
qiang2 = Weapon("枪2_trans", 2, 100, 1, 2)
changmao1 = Weapon("长矛1_trans", 1, 100, 1, 2)
changmao2 = Weapon("长矛2_trans", 1, 100, 1, 2)
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
weapon_bar.pos = 300, 40
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
coins = 10
step_store = 0
step_store1 = 0

#武器商店模块
store_button = Actor("store_button")
store_inner = Actor("store")
Pur_button = Actor("purchase")

# 标准速度
standard_speed = 2

# 地图与背景
background1 = Actor("bg1")  # 896, 448
background1.topleft = 0, 0#background1.pos = 500, 300
WIDTH = background1.width #+ 100
HEIGHT = background1.height #+ 300

# 在场角色
hero = Actor("prince")
hero_HP = HP(1000, 3)  #初始化王子HP
monsters = []

# 游戏控制
isLoose = False
start = False
game = False
step = 99

# 箱子部分
n = 3
box = Actor('box_close')
box1 = Actor('box_close')
box2 = Actor('box_close')
box3 = Actor('box_close')
send = Actor('传送门')
background1 = Actor('bg1')
send.bottomright = 1200, 450#send.pos = 700, 500

boxes = [box, box1, box2, box3]

for i in range(4):
    a = random.randint(100, 800)
    b = random.randint(150, 430)#(150, 600)
    boxes[i].x = a
    boxes[i].y = b
    boxes[i].open = False

################各类函数##############################

def open_box():
    global check, coins
    j = check
    bit = random.randint(0, 30)
    if bit % 5 == 0:
        boxes[j].image = 'box_open'
        mon = Monster('red_dino', 10)
        mon.pos = boxes[j].pos
        monsters.append(mon)
    elif bit % 5 == 1:
        mon = Monster('green_din', 10)
        mon.pos = boxes[j].pos
        monsters.append(mon)
    elif bit % 5 == 2:
        mon = Monster('red_din', 10)
        mon.pos = boxes[j].pos
        monsters.append(mon)
    elif bit % 5 == 3 or bit % 5 == 4:
        boxes[j].image = 'gloden2'
    boxes[j].open = True
    if boxes[j].image == 'gloden2':
        number = random.randint(20, 40)
        coins += number

# 画血条
def draw_hp_bar():
    global step
    if (hero_HP.isdead()):
        step = 3
    HPBar = Rect((20, 20), (200, 35))  #血槽
    currentHP_bar = Rect(
        (20, 20), (200 * hero_HP.current_HP / hero_HP.full_HP, 33))  #当前血量
    screen.draw.rect(HPBar, 'black')
    screen.draw.filled_rect(currentHP_bar, 'black')

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

# 商店的购买判断
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

############按键与鼠标#########################

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
            screen.draw.filled_rect(monster.currentHP_bar, 'white')
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
        for monster in monsters:
            monster.draw()
            screen.draw.filled_rect(monster.HP_bar, 'gray')
            screen.draw.filled_rect(monster.currentHP_bar, 'white')
        for i in range(3):
            for i in range(4):
                boxes[i].draw()
        send.draw()


        hero.draw()

        if step == 4:
            clock.schedule(right_movement, 0.01)
        if step == 5:
            clock.schedule(left_movement, 0.01)
        if step == 6:
            clock.schedule(up_movement, 0.01)
        if step == 7:
            clock.schedule(down_movement, 0.01)
    

    #HP、金币状态绘制
    draw_hp_bar()
    draw_coins_bar()

    # 子弹绘制
    for i in bullets:
        i.draw()
    for i in monster_bullets:
        i.draw()

    #武器槽绘制
    weapon_bar.draw()
    screen.blit(weapons_on_bar[0].image, (265, 26))
    screen.blit(weapons_on_bar[1].image, (303, 26))
    
    ######注：上面三部分绘制会在开始界面出现，我不是很懂开始界面的逻辑，希望能修正，感觉加个if判断就行

    # 背包绘制
    if bag_open:
        bag.draw()
        bag.pos = (500,300)
        for w in weapons:
            w.draw()

    #商店图标绘制
    store_button.draw()
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
    x1,y1 = 450,200
    x2,y2 = 500,300

    if step_store in range(2,11) and not bag_open:
        Pur_button.draw()
        Pur_button.pos = (x2,y2)
        screen.draw.text("Price: %d "%weapons[step_store-2].price,(x1,y1),fontsize=50,color = "black")

    if step_store1 == 20:
        screen.draw.text("Your coins are not ENOUGH!",(300,400),fontsize=50,color = "red")

    ####################update函数#################################

def update():
    global step, hero, game, check
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
            for monster in monsters:
                if monster.colliderect(i):
                    monster.HP.current_HP -= i.damage
                    bullets.remove(i)
                    tone.play('A1', 0.1)
                    monster.animate_shake()
                if monster.HP.isdead():
                    monsters.remove(monster)
        
        for i in monster_bullets:
            i.x += i.speed_x
            i.y += i.speed_y
            i.count_time += 1
            if(i.count_time >= i.distance/standard_speed**1.5):
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
        for j in range(0, 4):
            if hero.colliderect(boxes[j]) and boxes[j].open == False:
                check = j
                boxes[j].image = 'box_open'
                clock.schedule_unique(open_box, 0.1)

    #### 简单的四边跑 ######
    for monster in monsters:
        if hero.colliderect(monster):
            #tone.play('G2', 0.5)
            hero_HP.current_HP -= 0.05
        for i in range(3):
            if hero.colliderect(boxes[i]):
                boxes[i].image = 'box_open'


pgzrun.go()
