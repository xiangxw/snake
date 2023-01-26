import sys
import random
from collections import deque
import pygame
import pygame.locals as LOCALS

UP = 1 # 向上
DOWN = 2 # 向下
LEFT = 3 # 向左
RIGHT = 4 # 向右
SNAKE_WIDTH = 20 # 蛇的宽度，食物的宽度、蛇的移动速度和蛇的宽度一样
RATE = 6 # 画面每秒刷新次数
DISPLAY_WIDTH = 640 # 画面宽度
DISPLAY_HEIGHT = 480 # 画面高度
BACKGROUND_COLOR = pygame.Color(150, 150, 150) # 背景颜色
SNAKE_COLOR = pygame.Color(139, 105, 105) # 蛇的颜色
FOOD_COLOR = pygame.Color(165, 42, 42) # 食物颜色
SCORE_COLOR = pygame.Color(0, 255, 0) # 分数的颜色
GAME_OVER_COLOR = pygame.Color(255, 0, 0) # 游戏结束的颜色

class Game(object):
    def __init__(self):
        super(Game, self).__init__()
        self.display = None # 显示
        self.font = None # 字体
        self.clock = pygame.time.Clock() # 控制画面刷新频率
        pygame.init()
        pygame.display.set_caption("贪吃蛇(使用WSAD移动)")
        pygame.mixer.init()
        pygame.mixer.music.load("sound/bg.ogg")
        pygame.mixer.music.set_volume(0.7)
        self.display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        self.font = pygame.font.SysFont("kaiti", 32)
        self.eatSound = pygame.mixer.Sound("sound/eat.ogg")
        self.dieSound = pygame.mixer.Sound("sound/die.wav")
        self.playImage = pygame.image.load("image/play.png")
        self.playImageRect = self.playImage.get_rect()
        self.playImageRect.centerx = self.display.get_rect().centerx
        self.playImageRect.centery = self.display.get_rect().centery + 100
        self.resetGame()
    
    # 启动游戏
    def startGame(self):
        while True:
            self.tick()
            self.clock.tick(RATE)
    
    # 重新开始游戏
    def resetGame(self):
        self.snake = deque([[100, 100]]) # 蛇身位置列表
        self.direction = RIGHT # 方向
        self.food = [300, 300] # 食物位置
        self.score = 0 # 分数
        self.gameOver = False # 游戏是否结束
        pygame.mixer.music.play(-1)
    
    # 结束游戏
    def endGame(self):
        pygame.quit()
        sys.exit()
    
    def tick(self):
        self.handleEvent()
        if not self.gameOver:
            self.move()
            self.check()
        self.draw()
    
    # 处理事件
    def handleEvent(self):
        for event in pygame.event.get():
            if event.type == LOCALS.QUIT:
                self.endGame()
            elif event.type == LOCALS.KEYDOWN:
                direction = self.direction
                if event.key == LOCALS.K_w and self.direction != DOWN:
                    direction = UP
                elif event.key == LOCALS.K_s and self.direction != UP:
                    direction = DOWN
                elif event.key == LOCALS.K_a and self.direction != RIGHT:
                    direction = LEFT
                elif event.key == LOCALS.K_d and self.direction != LEFT:
                    direction = RIGHT
                self.direction = direction
            elif event.type == LOCALS.MOUSEBUTTONDOWN:
                if self.gameOver and self.playImageRect.collidepoint(event.pos):
                    self.resetGame()
    
    # 移动
    def move(self):
        head = [self.snake[0][0], self.snake[0][1]]
        if self.direction == UP:
            head[1] -= SNAKE_WIDTH
        elif self.direction == DOWN:
            head[1] += SNAKE_WIDTH
        elif self.direction == LEFT:
            head[0] -= SNAKE_WIDTH
        else:
            head[0] += SNAKE_WIDTH
        if self.willCollide(self.snake[0], self.food): # 吃到食物
            self.score += 1
            self.eatSound.play()
            self.genFood()
        else:
            self.snake.pop()
        self.snake.appendleft(head)
    
    # 检查
    def check(self):
        # 检查游戏是否结束
        if self.isGameEnd():
            self.gameOver = True
            self.dieSound.play()
            pygame.mixer.music.stop()
    
    # 绘图
    def draw(self):
        # 背景
        self.display.fill(BACKGROUND_COLOR)
        # 蛇
        for part in self.snake:
            pygame.draw.rect(self.display, SNAKE_COLOR, LOCALS.Rect(part[0], part[1], SNAKE_WIDTH, SNAKE_WIDTH))
        # 食物
        pygame.draw.rect(self.display, FOOD_COLOR, LOCALS.Rect(self.food[0], self.food[1], SNAKE_WIDTH, SNAKE_WIDTH))
        # 分数
        self.drawText("分数: %d" % self.score, SCORE_COLOR, (10, 10))
        # 游戏结束
        if self.gameOver:
            self.drawText("游戏结束!", GAME_OVER_COLOR, (DISPLAY_WIDTH/2, DISPLAY_HEIGHT/2), 'center')
            self.display.blit(self.playImage, self.playImageRect)
        
        # 刷新
        pygame.display.flip()
    
    # 写字
    def drawText(self, text, color, pos, posType = "topleft"):
        scoreSurf = self.font.render(text, True, color)
        scoreRect = scoreSurf.get_rect()
        setattr(scoreRect, posType, pos)
        self.display.blit(scoreSurf, scoreRect)
    
    # 游戏是否结束
    def isGameEnd(self):
        # 碰到边界
        if self.snake[0][0] < 0 or self.snake[0][0] > DISPLAY_WIDTH - SNAKE_WIDTH \
            or self.snake[0][1] < 0 or self.snake[0][1] > DISPLAY_HEIGHT - SNAKE_WIDTH:
            return True

        # 碰到自己
        for i in range(1, len(self.snake)):
            if self.willCollide(self.snake[0], self.snake[i]):
                return True

        return False

    # 是否会发生碰撞
    def willCollide(self, pos1, pos2):
        rect1 = LOCALS.Rect(pos1[0], pos1[1], SNAKE_WIDTH, SNAKE_WIDTH)
        rect2 = LOCALS.Rect(pos2[0], pos2[1], SNAKE_WIDTH, SNAKE_WIDTH)
        return rect1.colliderect(rect2)
    
    # 产生食物
    def genFood(self):
        while True:
            x = random.randint(0, DISPLAY_WIDTH - SNAKE_WIDTH)
            y = random.randint(0, DISPLAY_HEIGHT - SNAKE_WIDTH)
            success = True
            for part in self.snake:
                if self.willCollide(part, [x, y]):
                    success = False
                    break
            if success:
                self.food = [x, y]
                break

game = Game()
game.startGame()