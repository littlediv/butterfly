# url https://www.cnblogs.com/wuzhanpeng/p/4261015.html#3767420

import pygame                   # 导入 pygame 库
from pygame.locals import *     # 导入 pygame 库中的一些常量
from sys import exit            # 导入 sys 库中的exit 函数
import time
from random import randint

class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_surface, enemy_init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy_surface
        self.rect = self.image.get_rect()
        self.rect.topleft = enemy_init_pos
        self.speed = 2

        self.down_index = 0

    def update(self):
        self.rect.top += self.speed
        if self.rect.top >= SCREEN_HEIGHT:
            self.kill()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, bullet_surface, bullet_init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_surface
        self.rect = self.image.get_rect()
        self.rect.topleft = bullet_init_pos
        self.speed = 8

    def update(self):
        self.rect.top -= self.speed
        if self.rect.top <= - self.rect.height:
            self.kill()


class Hero(pygame.sprite.Sprite):

    def __init__(self, hero_surface, hero_init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = hero_surface
        self.rect = self.image.get_rect()
        self.rect.topleft = hero_init_pos
        self.speed = 6
        self.is_hit = False

        self.bullet1 = pygame.sprite.Group()

    def single_shoot(self, bullet1_surface):
        bullet1 = Bullet(bullet1_surface, self.rect.midtop)
        self.bullet1.add(bullet1)


    def move(self, offset):
        x = self.rect.left + offset[pygame.K_RIGHT]- offset[pygame.K_LEFT]
        y = self.rect.top + offset[pygame.K_DOWN] - offset[pygame.K_UP]

        if x <0:
            self.rect.left = 0
        elif x > SCREEN_WIDTH - self.rect.width:
            self.rect.left = SCREEN_WIDTH - self.rect.width
        else:
            self.rect.left = x

        if y <0:
            self.rect.top = 0
        elif x > SCREEN_HEIGHT - self.rect.height:
            self.rect.top = SCREEN_HEIGHT - self.rect.height
        else:
            self.rect.top = y

# 定义窗口的分辨率
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 640

ticks = 0
# 定义画面帧率
FRAME_RATE = 60
# 定义动画周期（帧数）
ANIMATE_CYCLE = 30

# 初始化游戏
pygame.init()
# 初始化一个用于显示的窗口
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
# 设置窗口标题
pygame.display.set_caption('this is my first pygame-program')

offset = {pygame.K_LEFT:0, pygame.K_RIGHT:0, pygame.K_UP:0, pygame.K_DOWN:0}



# 载入背景图
background = pygame.image.load('resources/image/background.png')
# 载入资源图片
shoot_img = pygame.image.load('resources/image/shoot.png')
# 用subsurface 剪切读入的图片
# hero1_rect = pygame.Rect(0,99,102, 126)
# hero2_rect = pygame.Rect(165,360,102,126)
# hero1 = shoot_img.subsurface(hero1_rect)
# hero2 = shoot_img.subsurface(hero2_rect)
hero_pos = [200,500]

bullet1_surface = shoot_img.subsurface(pygame.Rect(1004, 987, 9, 21))
enemy1_surface = shoot_img.subsurface(pygame.Rect(534, 612, 57, 43))

enemy1_down_surface = []
enemy1_down_surface.append(shoot_img.subsurface(pygame.Rect(267, 347, 57, 43)))
enemy1_down_surface.append(shoot_img.subsurface(pygame.Rect(873, 697, 57, 43)))
enemy1_down_surface.append(shoot_img.subsurface(pygame.Rect(267, 296, 57, 43)))
enemy1_down_surface.append(shoot_img.subsurface(pygame.Rect(930, 697, 57, 43)))

hero_surface = []
hero_surface.append(shoot_img.subsurface(pygame.Rect(0, 99, 102, 126)))
hero_surface.append(shoot_img.subsurface(pygame.Rect(165, 360, 102, 126)))
hero_surface.append(shoot_img.subsurface(pygame.Rect(165, 234, 102, 126)))
hero_surface.append(shoot_img.subsurface(pygame.Rect(330, 624, 102, 126)))
hero_surface.append(shoot_img.subsurface(pygame.Rect(330, 498, 102, 126)))
hero_surface.append(shoot_img.subsurface(pygame.Rect(432, 624, 102, 126)))

hero = Hero(hero_surface[0], hero_pos)

clock = pygame.time.Clock()

enemy_group = pygame.sprite.Group()
enemy_down_group = pygame.sprite.Group()


hero_down_index = 1
gameover = pygame.image.load('resources/image/gameover.png')
# 事件循环 (main loop)
while True:

    clock.tick(FRAME_RATE)

    # 绘制背景
    screen.blit(background, (0,0))

    if hero.is_hit:
        if ticks %(ANIMATE_CYCLE//2) ==0:
            hero_down_index +=1
        hero.image = hero_surface[hero_down_index]
        if hero_down_index == 5:
            break
    else:
        hero.image = hero_surface[ticks//(ANIMATE_CYCLE//2)]

    # if ticks % 50 <25:
    #     screen.blit(hero1, hero_pos)
    # else:
    #     screen.blit(hero2, hero_pos)
    if ticks >= ANIMATE_CYCLE:
        ticks = 0
    # hero.image = hero_surface[ticks//(ANIMATE_CYCLE//2)]

    if ticks %10 ==0:
        hero.single_shoot(bullet1_surface)
    hero.bullet1.update()
    hero.bullet1.draw(screen)

    if ticks %30 ==0:
        enemy = Enemy(enemy1_surface, [randint(0, SCREEN_WIDTH-enemy1_surface.get_width()),- enemy1_surface.get_height()])
        enemy_group.add(enemy)

    enemy_group.update()
    enemy_group.draw(screen)

    enemy_down_group.add(pygame.sprite.groupcollide(enemy_group, hero.bullet1, True, True))

    for enemy1_down in enemy_down_group:
        screen.blit(enemy1_down_surface[enemy1_down.down_index], enemy1_down.rect)
        if ticks % (ANIMATE_CYCLE//2) ==0:
            if enemy1_down.down_index <3:
                enemy1_down.down_index +=1
            else:
                enemy_down_group.remove(enemy1_down)


    enemy_down_list = pygame.sprite.spritecollide(hero, enemy_group, True)
    if len(enemy_down_list) >0:
        enemy_down_group.add(enemy_down_list)
        hero.is_hit = True

    screen.blit(hero.image, hero.rect)
    ticks += 1
    # 更新屏幕
    pygame.display.update()

    # 处理游戏推出
    # 从消息队列中循环取
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("exit")
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key in offset:
                offset[event.key] = 3
        elif event.type == pygame.KEYUP:
            if event.key in offset:
                offset[event.key] =0

    # offset_x = offset[pygame.K_RIGHT] - offset[pygame.K_LEFT]
    # offset_y = offset[pygame.K_DOWN] - offset[pygame.K_UP]
    # print(offset_x,"------", offset_y)
    #
    # time.sleep(1)
    # hero_pos = [hero_pos[0] + offset_x, hero_pos[1] + offset_y]
    hero.move(offset)

screen.blit(gameover, (0, 0))
# 玩家坠毁后退出游戏
while True:
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()