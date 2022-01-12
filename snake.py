import json
import sys

import pygame
from pygame.locals import *
import time
import random

SIZE = 40
BACKGROUND_COLOR = (0, 51, 25)
obstacle_list = []
size_list = []

if len(sys.argv) == 2:
    f = open(sys.argv[1], "r")
    obstacles = json.load(f)
    for i in obstacles["obstacles"]:
        obstacle_list.append([int(i["x"]), int(i["y"])])
    for i in obstacles["size"]:
        size_list.append([int(i["x"]), int(i["y"])])
    size_x = size_list[0][0]
    size_y = size_list[0][1]


class Apple:
    def __init__(self, parent_screen):
        """
        Constructor for apple object
        :param parent_screen:
        """
        self.parent_screen = parent_screen
        self.image = pygame.image.load("resources/apple.jpg").convert()
        self.x = 120
        self.y = 120

    def draw(self):
        """"
        Draw apple
        """
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self, snake):
        """
        Randomly move apple to a spot on the table
        :param snake:object snake
        :return:
        """
        not_in_snake = 1
        while not_in_snake == 1:
            ok = 0
            x = random.randint(1, int(size_x / SIZE) - 1) * SIZE
            y = random.randint(1, int(size_y / SIZE) - 1) * SIZE
            for i in range(snake.length):
                if x == snake.x[i] and y == snake.y[i]:
                    ok = 1
            for i in range(len(obstacle_list)):
                # print(obstacle_list[i][0])
                # print(obstacle_list[i][1])
                if x == obstacle_list[i][0] and y == obstacle_list[i][1]:
                    ok = 1
            if ok == 0:
                self.x = x
                self.y = y
                not_in_snake = 0
    # not_in_snake = 1
    # while not_in_snake == 1:
    #     ok = 0
    #     x = random.randint(1, int(size_x / SIZE)) * SIZE
    #     y = random.randint(1, int(size_y / SIZE)) * SIZE
    #     snake_length = snake.length
    #     obstacle_length = len(obstacle)
    #     if snake_length >= obstacle_length:
    #         difference = snake_length - obstacle_length
    #         max_length = snake_length
    #     else:
    #         difference = obstacle_length - snake_length
    #         max_length = obstacle_length
    #     for i in range(max_length):
    #         if x == snake.x[i] and y == snake.y[i]:
    #             ok = 1
    #         if x == obstacle[i].x and y == obstacle[i].y:
    #             ok = 1
    #     for i in range(difference):
    #         if max_length == snake_length:
    #             if x == snake.x[i] and y == snake.y[i]:
    #                 ok = 1
    #         else:
    #             if x == obstacle[i].x and y == obstacle[i].y:
    #                 ok = 1
    #     if ok == 0:
    #         self.x = x
    #         self.y = y
    #         not_in_snake = 0


class Obstacle:
    def __init__(self, parent_screen, x, y):
        """
        Constructor for an obstacle
        :param parent_screen:
        :param x:
        :param y:
        """
        self.parent_screen = parent_screen
        self.image = pygame.image.load("resources/block2.jpg").convert()
        self.x = x
        self.y = y

    def draw(self):
        """
        Draw Obstacle
        :return:
        """
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()


class Snake:
    def __init__(self, parent_screen):
        """
        Constructor for snake object
        :param parent_screen:
        """
        self.parent_screen = parent_screen
        self.image = pygame.image.load("resources/block.jpg").convert()
        self.direction = 'down'

        self.length = 1
        self.x = [40]
        self.y = [40]

    def move_left(self):
        """
        Move snake tot the left
        :return:
        """
        if self.direction == 'right':
            self.direction = 'right'
        else:
            self.direction = 'left'

    def move_right(self):
        """
        Move snake to the right
        :return:
        """
        if self.direction == 'left':
            self.direction = 'left'
        else:
            self.direction = 'right'

    def move_up(self):
        """
        Move snake up
        :return:
        """
        if self.direction == 'down':
            self.direction = 'down'
        else:
            self.direction = 'up'

    def move_down(self):
        """
        Move snake down
        :return:
        """
        if self.direction == 'up':
            self.direction = 'up'
        self.direction = 'down'

    def walk(self):
        """
        Updating snake list after a movement and drawing the snake
        :return:
        """
        # update body
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        # update head
        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'right':
            self.x[0] += SIZE
        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE

        self.draw()

    def draw(self):
        """
        Drawing the snake
        :return:
        """
        for i in range(self.length):
            self.parent_screen.blit(self.image, (self.x[i], self.y[i]))

        pygame.display.flip()

    def increase_length(self):
        """
        Increasing length of snake
        :return:
        """
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)


class Game:
    def __init__(self):
        """
        Constructor of the Game object
        """
        pygame.init()
        pygame.display.set_caption("Snake by Vacaru Robert")

        pygame.mixer.init()
        self.play_background_music()

        self.surface = pygame.display.set_mode((size_x, size_y))
        self.snake = Snake(self.surface)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()
        self.obstacle = []
        for i in range(len(obstacle_list)):
            self.obstacle.append(Obstacle(self.surface, obstacle_list[i][0], obstacle_list[i][1]))
            self.obstacle[i].draw()
        self.highScore = 0

    def play_background_music(self):
        """
        Playing the background sound
        :return:
        """
        pygame.mixer.music.load('resources/SNAKE GAME.mp3')
        pygame.mixer.music.play(-1, 0)

    def play_sound(self, sound_name):
        """
        Playing sound on action
        :param sound_name: type of action that happened
        :return:
        """
        if sound_name == "crash":
            sound = pygame.mixer.Sound("resources/sfx-defeat1.mp3")
        elif sound_name == 'ding':
            sound = pygame.mixer.Sound("resources/EATING SOUND.mp3")

        pygame.mixer.Sound.play(sound)

    def reset(self):
        """
        Resetting the game
        :return:
        """
        self.snake = Snake(self.surface)
        self.apple = Apple(self.surface)

    def is_collision(self, x1, y1, x2, y2):
        """
        In case of collision
        :param x1: coordinates of head of snake
        :param y1: coordinates of head of snake
        :param x2: coordinates of the point that is colliding
        :param y2: coordinates of the point that is colliding
        :return: True or False in case of collision
        """
        if x2 <= x1 < x2 + SIZE:
            if y2 <= y1 < y2 + SIZE:
                return True
        return False

    def out_of_table(self, x1, y1, x2, y2):
        """
        In case the snake gets out of the table
        :param x1: coordinates of head of snake
        :param y1: coordinates of head of snake
        :param x2: coordinates of the point that is colliding
        :param y2: coordinates of the point that is colliding
        :return: True or false in case of colliding
        """
        if x1 > x2 or y1 > y2 or x1 < 0 or y1 < 0:
            return True
        return False

    def render_background(self):
        """
        Rendering the background image
        :return:
        """
        bg = pygame.image.load("resources/background-2.jpg")
        self.surface.blit(bg, (0, 0))

    def play(self):
        """
        Playing the game after one move and verifying if that move is eligible
        :return:
        """
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        for i in range(len(self.obstacle)):
            self.obstacle[i].draw()
        self.display_score()
        self.display_high()
        pygame.display.flip()

        # eating apple
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound("ding")
            self.snake.increase_length()
            self.apple.move(self.snake)

        # colliding with itself
        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound('crash')
                raise "Collision Occurred"
        # out of table
        if self.out_of_table(self.snake.x[0], self.snake.y[0], size_x, size_y):
            self.play_sound('crash')
            raise "Collision Occurred"
        # colliding with obstacle
        for i in range(len(self.obstacle)):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.obstacle[i].x, self.obstacle[i].y):
                self.play_sound('crash')
                raise "Collision Occurred"

    def display_score(self):
        """
        Displaying the score on the table
        :return:
        """
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f"Score: {self.snake.length}", True, (200, 200, 200))
        self.surface.blit(score, (size_x - 150, 10))

    def display_high(self):
        """
        Displaying the highScore on the table
        :return:
        """
        font = pygame.font.SysFont('arial', 20)
        score = font.render(f"HighScore: {self.highScore}", True, (200, 200, 200))
        self.surface.blit(score, (size_x - 150, 50))

    def show_game_over(self):
        """
        Displaying the Game Over tab
        :return:
        """
        if self.highScore < self.snake.length:
            self.highScore = self.snake.length
        self.render_background()
        font = pygame.font.SysFont('arial', int(size_x / 30))
        line1 = font.render(f"Game is over! Your score is {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(line1, (size_x / 5, size_y / 4 + 100))
        line2 = font.render("To play again press Enter. To exit press Escape!", True, (255, 255, 255))
        self.surface.blit(line2, (size_x / 5, size_y / 4 + 150))
        line3 = font.render(f"HighScore is {self.highScore}", True, (255, 255, 255))
        self.surface.blit(line3, (size_x / 5, size_y / 4 + 200))
        pygame.mixer.music.pause()
        pygame.display.flip()

    def run(self):
        """
        Running the game
        :return:
        """
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False

                    if not pause:
                        if event.key == K_LEFT:
                            self.snake.move_left()

                        if event.key == K_RIGHT:
                            self.snake.move_right()

                        if event.key == K_UP:
                            self.snake.move_up()

                        if event.key == K_DOWN:
                            self.snake.move_down()

                elif event.type == QUIT:
                    running = False
            try:

                if not pause:
                    self.play()

            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(.25)


if __name__ == '__main__':
    game = Game()
    game.run()
