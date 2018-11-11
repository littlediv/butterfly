# url https://www.cnblogs.com/wuzhanpeng/p/4261015.html#3767420

import pygame                   # 导入 pygame 库
from pygame.locals import *     # 导入 pygame 库中的一些常量
from sys import exit            # 导入 sys 库中的exit 函数
import time

# 定义窗口的分辨率
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 640

ticks = 0

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
hero1_rect = pygame.Rect(0,99,102, 126)
hero2_rect = pygame.Rect(165,360,102,126)
hero1 = shoot_img.subsurface(hero1_rect)
hero2 = shoot_img.subsurface(hero2_rect)
hero_pos = [200,500]

# 事件循环 (main loop)
while True:

    # 绘制背景
    screen.blit(background, (0,0))

    if ticks % 50 <25:
        screen.blit(hero1, hero_pos)
    else:
        screen.blit(hero2, hero_pos)
    ticks += 1
    if ticks ==50:
        ticks =0
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

    offset_x = offset[pygame.K_RIGHT] - offset[pygame.K_LEFT]
    offset_y = offset[pygame.K_DOWN] - offset[pygame.K_UP]
    print(offset_x,"------", offset_y)

    time.sleep(1)
    hero_pos = [hero_pos[0] + offset_x, hero_pos[1] + offset_y]