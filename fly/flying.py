import pygame                   # 导入 pygame 库
from pygame.locals import *     # 导入 pygame 库中的一些常量
from sys import exit            # 导入 sys 库中的exit 函数

# 定义窗口的分辨率
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 640

# 初始化游戏
pygame.init()
# 初始化一个用于显示的窗口
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
# 设置窗口标题
pygame.display.set_caption('this is my first pygame-program')

# 事件循环 (main loop)
while True:
    # 处理游戏推出
    # 从消息队列中循环取
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("exit")
            pygame.quit()
            exit()