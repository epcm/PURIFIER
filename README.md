## PURIFIER非正式官方指南

欢迎来到PURIFIER！

这是2020年北京大学暑期学校python语言基础与应用16组的大作业，基于pygame zero开发。

__没有配置/不想配置相关环境的话请下载Releases中的exe版本（仅限windows），exe版本相关源码见For_EXE分支__

## 视频

https://www.bilibili.com/video/BV1XT4y177eE?p=16&share_source=copy_web

#### 故事背景

公元2020年7月8日，王浩然正在电脑前敲着暑校typhon课程的大作业代码。他是b大的一名学生。由于这场新冠肺炎疫情，他迟迟不能返回学校，一不小心寒假连休到了暑假。

头昏脑胀之际，一名自称神奇博士的人突然出现，声称这场瘟疫是远方山洞的一条恶龙所为，而恶龙身上的鳞片则是瘟疫的解药，并要求王浩然打败恶龙，解救人民。

> 我们王国遭遇了一场前所未有的新型瘟疫。越来越多的人染上瘟疫，民不聊生。我们需要你打败恶龙。
>
> 凭啥是我？
>
> 因为你是达拉崩吧斑得贝迪卜多比鲁翁和公主米娅莫拉苏娜丹妮谢莉红的儿子。
>
> ？Excuse me？
>
> 你的父亲——达拉崩吧斑得贝迪卜多比鲁翁他打败了恶龙昆图库塔卡提考特苏瓦西拉松，就把公主米娅莫拉苏娜丹妮谢莉红嫁给了达拉崩吧斑得贝迪卜多比鲁翁。
>
> 嗯，好吧？所以，你是？
>
> 我是来自公元前2020年的蒙达鲁克硫斯伯古比奇巴勒城的丞相，我叫..
>
> 别说你叫啥了。
>
> 哦，好吧，亲爱的王子。只有你才能战胜恶龙，拿到解药。你是达拉崩吧斑得贝迪卜多比鲁翁和公主米娅莫拉苏娜丹妮谢莉红的后代，你流淌的是勇士的血液！！！
>
> 那，我就试试吧！
>

于是，王浩然穿越回公元前2020年的蒙达鲁克硫斯伯古比奇巴勒城，带上最好的武器，翻过最高的山，闯进最深的森林，把解药带回面前！！！

#### 操作指南

* 使用 W A S D 键控制角色移动

* 单击鼠标左键进行攻击

* 当你使用斧头，剑等近程武器时，攻击方向为当前角色的朝向；使用枪，长矛等远程射击或投掷武器时，攻击方向为鼠标点击的方向

  每次使用武器时都会消耗MP，MP的恢复需要一定时间，所以请不要进行过于频繁的攻击哦~

* 按 Q 键实现左上角武器栏中的武器切换 

* 点击右上角的商店图标以购买武器，点击左上角的武器栏可以进入背包以更换武器，鼠标右键返回上一层

* 在打开所有宝箱并消灭所有怪物时传送门就会出现，通过传送门进入下一关

* 游戏中可以使用数字键3打开操作指南

#### 武器图鉴

|                             名称                             | 价格 | 伤害 | MP消耗 | 攻击距离 | 子弹速度 | 效果                               |
| :----------------------------------------------------------: | :--: | :--: | :----: | :------: | -------- | ---------------------------------- |
| ![](https://raw.githubusercontent.com/epcm/Pictures/master/Markdown/%E6%96%A7%E5%AD%90.png)斧子 |  0   |  2   |   10   |    60    | \        | 普通的斧子                         |
| ![](https://raw.githubusercontent.com/epcm/Pictures/master/Markdown/%E5%BC%931.png)弓箭 |  0   | 1.5  |   10   |   200    | 1.5      | 普通的弓箭                         |
| ![](https://raw.githubusercontent.com/epcm/Pictures/master/Markdown/%E5%BC%932.png)寒冰射手 |  30  | 1.5  |   15   |   200    | 1.5      | 使敌人一定时间内减速（对Boss无效） |
| ![](https://raw.githubusercontent.com/epcm/Pictures/master/Markdown/%E5%89%911.png)细剑 |  30  |  5   |   15   |    75    | \        | 高伤害                             |
| ![](https://raw.githubusercontent.com/epcm/Pictures/master/Markdown/%E5%89%912.png)大宝剑 |  30  |  3   |   15   |    75    | \        | 高击退效果                         |
| ![](https://raw.githubusercontent.com/epcm/Pictures/master/Markdown/%E6%9E%AA1.png)散射枪 |  40  |  1   |   20   |   200    | 1.5      | 一次散射3发                        |
| ![](https://raw.githubusercontent.com/epcm/Pictures/master/Markdown/%E6%9E%AA2.png)脉冲枪 |  40  |  3   |   20   |   200    | 2.5      | 高速高伤害                         |
| ![](https://raw.githubusercontent.com/epcm/Pictures/master/Markdown/%E9%95%BF%E7%9F%9B1.png)Tracer |  50  |  3   |   30   |   500    | 1.5      | 跟踪最近的敌人                     |
| ![](https://raw.githubusercontent.com/epcm/Pictures/master/Markdown/%E9%95%BF%E7%9F%9B2.png)屠龙神器 | 200  | 12/s |   40   |   300    | 2        | 贯穿敌人、在贯穿过程中造成持续伤害 |

#### 怪兽图鉴

| 名称                                                         | HP   | 速度 | 开始追击距离 | 攻击伤害 | 攻击的速度 | 攻击的距离 | 碰撞伤害 | 备注                                    |
| ------------------------------------------------------------ | ---- | ---- | ------------ | -------- | ---------- | ---------- | -------- | --------------------------------------- |
| ![](https://raw.githubusercontent.com/epcm/Pictures/master/Markdown/orange_dino.png)orange | 5    | 1.5  | 200          | 1        | 1.2        | 220        | 3/s      | 高速移动+随机转向                       |
| ![](https://raw.githubusercontent.com/epcm/Pictures/master/Markdown/green_dino.png)green | 5    | 1    | 200          | 1        | 1.5        | 220        | 3/s      | 高速攻击+随机转向                       |
| ![](https://raw.githubusercontent.com/epcm/Pictures/master/Markdown/red_dino.png)red | 5    | 1    | 200          | 1.5      | 1.2        | 220        | 3/s      | 高伤害+随机转向                         |
| ![](https://raw.githubusercontent.com/epcm/Pictures/master/Markdown/minotaur.png)minotaur | 10   | 1    | 200          | 2.5      | 1.2        | 220        | 6/s      | 血厚、伤害高+玩家未靠近时按固定轨迹运动 |

#### Boss恶龙

![](https://raw.githubusercontent.com/epcm/Pictures/master/Markdown/boss.png)

|     技能     |                 效果                 |                             演示                             |
| :----------: | :----------------------------------: | :----------------------------------------------------------: |
| 召唤师的技艺 |  召唤1个宝箱并有可能附送一个牛头怪   |                              \                               |
|    Magic!    | 对定位在玩家的魔法阵内进行流星雨攻击 | <img src="https://raw.githubusercontent.com/epcm/Pictures/master/Markdown/magic!.png" style="zoom:50%;" /> |
|     冲撞     |  在某一垂直位置上进行快速的前后冲撞  | <img src="https://raw.githubusercontent.com/epcm/Pictures/master/Markdown/20200711221643.png" style="zoom: 25%;" /> |
|     散弹     |           同时发出6个火球            | <img src="https://raw.githubusercontent.com/epcm/Pictures/master/Markdown/20200711222331.png" style="zoom: 33%;" /> |
|  自卫追踪弹  |    在靠近时会自动发射能追踪的火球    | <img src="https://raw.githubusercontent.com/epcm/Pictures/master/Markdown/auto_chase.jpg" style="zoom: 33%;" /> |

#### 来自开发者的通关小建议

* 开完宝箱不要留恋，赶快跑，万一开到的是怪兽呢？
* 斧头、剑等近战武器可以对当前位置前方的多个怪兽造成伤害，并产生击退效果，合理利用即可群体歼灭
* 我才不会告诉你最后一个武器是用来干什么的，当然使用其他武器通关游戏会更有趣
