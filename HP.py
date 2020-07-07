class HP(object):

    def __init__(self, FullHP, num):
        self.FullHP = FullHP
        self.CurrentHP = FullHP
        self.num = num #命数
        self.count = 0 #复活次数
    
    #判断是否死亡并在可能的情形下复活
    def isdead(self):
        if self.CurrentHP > 0:
            return
        elif self.CurrentHP <= 0 & self.count < self.num: #能复活
            self.CurrentHP = self.FullHP
            return
        else:
            return False
