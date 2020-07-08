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