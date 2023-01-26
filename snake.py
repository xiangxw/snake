import sys
import random
from collections import deque
import pygame
import pygame.locals as LOCALS

UP = 1 # up
DOWN = 2 # down
LEFT = 3 # left
RIGHT = 4 # right
SNAKE_WIDTH = 20 # width of snake, width of food, speed of snake
RATE = 6 # fps
DISPLAY_WIDTH = 640 # display width
DISPLAY_HEIGHT = 480 # display height
BACKGROUND_COLOR = pygame.Color(150, 150, 150) # background color
SNAKE_COLOR = pygame.Color(139, 105, 105) # color of snake
FOOD_COLOR = pygame.Color(165, 42, 42) # color of food
SCORE_COLOR = pygame.Color(0, 255, 0) # color of score text
GAME_OVER_COLOR = pygame.Color(255, 0, 0) # color game over text

class Game(object):
    def __init__(self):
        super(Game, self).__init__()
        self.display = None # display
        self.font = None # font
        self.clock = pygame.time.Clock() # for fps control
        pygame.init()
        pygame.display.set_caption("snake(move with WSAD)")
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
    
    # start game
    def startGame(self):
        while True:
            self.tick()
            self.clock.tick(RATE)
    
    # restart game
    def resetGame(self):
        self.snake = deque([[100, 100]]) # all parts of the snake
        self.direction = RIGHT # direction
        self.food = [300, 300] # position of food
        self.score = 0 # score
        self.gameOver = False # game is over or not
        pygame.mixer.music.play(-1)
    
    # end game
    def endGame(self):
        pygame.quit()
        sys.exit()
    
    def tick(self):
        self.handleEvent()
        if not self.gameOver:
            self.move()
            self.check()
        self.draw()
    
    # handle event
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
    
    # move
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
        if self.willCollide(self.snake[0], self.food): # eat food
            self.score += 1
            self.eatSound.play()
            self.genFood()
        else:
            self.snake.pop()
        self.snake.appendleft(head)
    
    # check
    def check(self):
        # check game over
        if self.isGameEnd():
            self.gameOver = True
            self.dieSound.play()
            pygame.mixer.music.stop()
    
    # draw
    def draw(self):
        # background
        self.display.fill(BACKGROUND_COLOR)
        # snake 
        for part in self.snake:
            pygame.draw.rect(self.display, SNAKE_COLOR, LOCALS.Rect(part[0], part[1], SNAKE_WIDTH, SNAKE_WIDTH))
        # food
        pygame.draw.rect(self.display, FOOD_COLOR, LOCALS.Rect(self.food[0], self.food[1], SNAKE_WIDTH, SNAKE_WIDTH))
        # score
        self.drawText("Score: %d" % self.score, SCORE_COLOR, (10, 10))
        # game over
        if self.gameOver:
            self.drawText("Game Over!", GAME_OVER_COLOR, (DISPLAY_WIDTH/2, DISPLAY_HEIGHT/2), 'center')
            self.display.blit(self.playImage, self.playImageRect)
        
        # refresh
        pygame.display.flip()
    
    # draw text
    def drawText(self, text, color, pos, posType = "topleft"):
        scoreSurf = self.font.render(text, True, color)
        scoreRect = scoreSurf.get_rect()
        setattr(scoreRect, posType, pos)
        self.display.blit(scoreSurf, scoreRect)
    
    # is game over
    def isGameEnd(self):
        # touching the boundary
        if self.snake[0][0] < 0 or self.snake[0][0] > DISPLAY_WIDTH - SNAKE_WIDTH \
            or self.snake[0][1] < 0 or self.snake[0][1] > DISPLAY_HEIGHT - SNAKE_WIDTH:
            return True

        # touching the snake
        for i in range(1, len(self.snake)):
            if self.willCollide(self.snake[0], self.snake[i]):
                return True

        return False

    # will collide
    def willCollide(self, pos1, pos2):
        rect1 = LOCALS.Rect(pos1[0], pos1[1], SNAKE_WIDTH, SNAKE_WIDTH)
        rect2 = LOCALS.Rect(pos2[0], pos2[1], SNAKE_WIDTH, SNAKE_WIDTH)
        return rect1.colliderect(rect2)
    
    # gen food
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