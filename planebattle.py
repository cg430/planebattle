#! /usr/bin/env python
# coding=utf-8

import pygame
import random
import time
from pygame.locals import *


class Plane(object):
    """飞机基类"""
    def __init__(self, x, y, image):
        # 创建时飞机默认的位置
        self.x, self.y = x, y
        # 飞机图片
        self.image = pygame.image.load(image)
        # 放置子弹索引
        self.bullet_list = []

    def display(self, screen):
        # 飞机贴合到背景中去
        screen.blit(self.image, (self.x, self.y))
        for bullet in self.bullet_list:
            bullet.display(screen)
            if bullet.judge():
                self.bullet_list.remove(bullet)


class HeroPlane(Plane):
    def __init__(self):
        super().__init__(200, 600, "./feiji/hero1.png")
        self.name = 'hero'

    def keyHandle(self, direction):
        # 接收键盘事件控制英雄机移动
        if direction == 'left':
            self.x -= 5
        elif direction == 'right':
            self.x += 5
        elif direction == 'up':
            self.y -= 5
        elif direction == 'down':
            self.y += 5

    def fire(self):
        # 将子弹对象的引用保存
        self.bullet_list.append(HeroBullet(self.x, self.y))


class EnemyPlane(Plane):
    """敌机类"""
    def __init__(self, speed):
        random_num = random.randint(0, 2)
        super().__init__(random.randint(20, 400), random.randint(20, 400), './feiji/enemy'+str(random_num)
                        + '.png')
        # 敌机发射子弹按照时间间隙发射
        self.bullet_sleep_time = 0.3
        self.bullet_last_time = time.time()
        self.name = 'enemy'
        self.speed = speed

    def move(self):
        self.y += self.speed

    def judge(self):
        if self.y == 852:
            return True
        else:
            return False


class Bullet(object):
    def __init__(self, image, x, y):
        self.image = pygame.image.load(image)
        self.x = x
        self.y = y

    def display(self, screen):
        # 子弹贴合到背景中去
        screen.blit(self.image, (self.x, self.y))


class HeroBullet(Bullet):
    def __init__(self, x, y):
        super().__init__("./feiji/bullet.png", x+45, y-20)

    def judge(self):
        if self.y == 0:
            return True
        else:
            return False


class GameInit(object):
    """游戏初始化类"""
    # 类属性
    enemyList = []
    score = 0
    hero = object

    @classmethod
    def createEnemy(cls, speed):
        cls.enemyList.append(EnemyPlane(speed))

    @classmethod
    def createHero(cls):
        cls.hero = HeroPlane()

    @classmethod
    def gameInit(cls):
        cls.createHero()

    @classmethod
    def heroPlaneKey(cls, key_value):
        cls.hero.keyHandle(key_value)

    @classmethod
    def draw(cls, screen):
        del_plane_list = []
        count = 0
        for enemy in cls.enemyList:
            # 显示敌机
            enemy.display(screen)
            # 超出边界从列表中删除掉, 超出边界记录索引
            if enemy.y > 852:
                del_plane_list.append(count)
            count += 1
        for i in del_plane_list:
            del cls.enemyList[i]
        cls.hero.display(screen)

    # 更新敌机位置
    @classmethod
    def setXY(cls):
        for enemy in cls.enemyList:
            enemy.move()

    @classmethod
    def shoot(cls):
        cls.hero.fire()
        # 子弹打到敌机让敌机从列表中消失
        for enemy in cls.enemyList:
            enemy_rect = pygame.Rect(enemy.image.get_rect())
            for bullet in cls.hero.bullet_list:
                bullet_rect = pygame.Rect(bullet.image.get_rect())
                # 敌机的图片与子弹的图片相重叠，　意味着子弹击中
                # 将子弹列表中引用和敌机列表引用删除
                if enemy_rect.colliderect(bullet_rect):
                    if enemy_rect.width == 51:
                        cls.score += 10
                    cls.hero.bullet_list.remove(bullet)
                    cls.enemyList.remove(enemy)

    @classmethod
    def gameover(cls):
        hero_rect = pygame.Rect(cls.hero.image.get_rect())
        for enemy in cls.enemyList:
            enemy_rect = pygame.Rect(enemy.image.get_rect())
            if hero_rect.colliderect(enemy_rect):
                return True
            else:
                return False

    @staticmethod
    def terminate():
        pygame.quit()
        exit()

    @staticmethod
    def drawText(text, font, surface):
        content = font.render(text, False, (0, 0, 255))
        content_rect = content.get_rect()
        surface.blit(content, content_rect)


def main():
    # 初始化pygame
    pygame.init()
    # 创建窗口
    screen = pygame.display.set_mode((480, 852), 0, 32)
    pygame.display.set_caption('飞机大战')
    # 创建背景
    background = pygame.image.load('./feiji/background.png').convert()
    # gameover = pygame.image.load("./feiji/gameover.png")
    # font = pygame.font.SysFont(None, 64)
    font1 = pygame.font.SysFont(None, 24)
    GameInit.gameInit()
    start_time = time.time()
    while True:
        GameInit.drawText('score:%s' % GameInit.score, font1, screen)
        # 背景贴合到窗口中去
        screen.blit(background, (0, 0))
        last_time = time.time()
        # 每隔２秒创建敌机
        if last_time - start_time > 2:
            GameInit.createEnemy(1)
            start_time = last_time
        # 判断键盘事件
        for event in pygame.event.get():
            # 判断是否是点击了退出按钮
            if event.type == QUIT:
                print("exit")
                exit()
            # 判断是否是按下了键
            elif event.type == KEYDOWN:
                # 检测按键是否是a或者left
                if event.key == K_a or event.key == K_LEFT:
                    print('left')
                    GameInit.heroPlaneKey('left')
                # 检测按键是否是d或者right
                elif event.key == K_d or event.key == K_RIGHT:
                    print('right')
                    GameInit.heroPlaneKey('right')
                # 检测按键是否是w或Up
                elif event.key == K_w or event.key == K_UP:
                    print('up')
                    GameInit.heroPlaneKey('up')
                # 检测按键是否是s或down
                elif event.key == K_s or event.key == K_DOWN:
                    print('down')
                    GameInit.heroPlaneKey('down')
                # 检测按键是否是空格键
                elif event.key == K_SPACE:
                    print('space')
                    GameInit.shoot()
        GameInit.setXY()
        GameInit.draw(screen)
        # 刷新窗口
        pygame.display.update()
        # if GameInit.gameover():
        #     time.sleep(1)
        #     screen.blit(gameover, (0, 0))
        #     while True:
        #         GameInit.drawText('%s' % GameInit.score, font, screen)
        #         pygame.display.update()
        #         for event in pygame.event.get():
        #             # 判断是否是点击了退出按钮
        #             if event.type == QUIT:
        #                 print("exit")
        #                 exit()


if __name__ == '__main__':
    main()

