import random
import sys
import os
import pygame

pygame.init()


class Snake():
    def __init__(self):
        self.path = os.path.dirname(".\\snake.py")
        
        self.running = True
        self.width = 20
        self.height = 20
        self.screen = pygame.display.set_mode((self.x_to_pxl(self.width),
                                               self.y_to_pxl(self.height)))
        pygame.display.set_caption('Snake')
        pygame.display.set_icon(pygame.image.load(f'{self.path}\\Snake_dep\\snake.png'))

        self.xaccel = 1
        self.yaccel = 0
        self.x = self.width // 2
        self.y = self.height // 2
        self.parts = [[self.x, self.y], [self.x - 1, self.y - 1]]
        self.score = 2
        self.food = Food(self)

        self.clock = pygame.time.Clock()

        self.score_font = pygame.font.Font('freesansbold.ttf', 20)
        
        self.return_button_text = self.score_font.render("Return", True, (255, 255, 255))
        self.rb_dims = self.score_font.size("Return")
        self.return_button_rect = pygame.Rect(self.x_to_pxl(self.width) - self.rb_dims[0] - 5, 8, \
                                         self.rb_dims[0], self.rb_dims[1])


    def x_to_pxl(self, v):
        return v * 20
    def y_to_pxl(self, v):
        return v * 20 + 30 

    def move(self):
        for i in reversed(range(len(self.parts))):
            if i == 0:
                self.parts[i][0] += self.xaccel
                self.parts[i][1] += self.yaccel
            else:
                self.parts[i][0] = self.parts[i-1][0]
                self.parts[i][1] = self.parts[i-1][1]

    def grow(self, foodx, foody):
        if self.parts[0] == [foodx, foody]:
            self.parts.append([self.parts[-1][0], self.parts[-1][1]])
            self.score += 1

    def display(self, part):
        pygame.draw.rect(self.screen, (255, 0, 0),
                         (self.x_to_pxl(part[0]), self.y_to_pxl(part[1]),
                          self.x_to_pxl(1), self.x_to_pxl(1)))

    def game_over(self):
        gameover = True

        font = pygame.font.Font('freesansbold.ttf', 40)
        small_font = pygame.font.Font('freesansbold.ttf', 20)

        text = font.render(f'Score: {self.score}', True, (255, 255, 255))
        text_size = font.size(f'Score: {self.score}')

        text2 = small_font.render(
            'Press \'space\' to play again', True, (255, 255, 255))
        text2_size = small_font.size('Press \'space\' to play again')

        texts_height = text_size[1] + text2_size[1] + 20

        while gameover:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                    gameover = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.return_button_rect.collidepoint(pygame.mouse.get_pos()):
                        self.running = False
                        gameover = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.xaccel = 1
                        self.yaccel = 0
                        self.x = self.width // 2
                        self.y = self.height // 2
                        self.parts = [[self.x, self.y],
                                      [self.x - 1, self.y - 1]]
                        self.score = 2
                        self.food = Food(self)
                        gameover = False

            self.screen.fill((0, 0, 0))
            pygame.draw.rect(self.screen, (50, 50, 50), (0, 0, self.x_to_pxl(self.width), 30))

            self.screen.blit(text, (int(self.x_to_pxl(self.width) / 2 -
                                        text_size[0] / 2), int(self.y_to_pxl(self.height) / 2 - texts_height / 2)))
            self.screen.blit(text2, (int(self.x_to_pxl(self.width) / 2 - text2_size[0] / 2), int(
                self.y_to_pxl(self.height) / 2 - texts_height / 2 + text2_size[1] + 20)))

            self.screen.blit(self.return_button_text, (self.return_button_rect.left, self.return_button_rect.top))

            pygame.display.update()
            self.clock.tick(10)

    def run(self):
        while self.running:
            self.clock.tick(10)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.return_button_rect.collidepoint(pygame.mouse.get_pos()):
                        self.running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        if self.yaccel == 0:
                            self.xaccel = 0
                            self.yaccel = -1
                    elif event.key == pygame.K_s:
                        if self.yaccel == 0:
                            self.xaccel = 0
                            self.yaccel = 1
                    elif event.key == pygame.K_a:
                        if self.xaccel == 0:
                            self.xaccel = -1
                            self.yaccel = 0
                    elif event.key == pygame.K_d:
                        if self.xaccel == 0:
                            self.xaccel = 1
                            self.yaccel = 0

            self.screen.fill((0, 0, 0))
            pygame.draw.rect(self.screen, (50, 50, 50), (0, 0, self.x_to_pxl(self.width), 30))

            self.food.display()
            self.move()

            if not 0 <= self.parts[0][0] <= self.width - 1 or \
               not 0 <= self.parts[0][1] <= self.height - 1 or \
               self.parts[0] in self.parts[1:]:
                self.game_over()

            if self.running:
                for i in self.parts:
                    self.display(i)

                
                score_text = self.score_font.render(str(self.score), True, (255, 255, 255))
                self.screen.blit(score_text, (5, 7))

                self.screen.blit(self.return_button_text, (self.return_button_rect.left, self.return_button_rect.top))

                self.grow(self.food.fx, self.food.fy)
                self.food.eat(self.parts[0])
                pygame.display.update()


class Food():
    def __init__(self, master_snake):
        self.master_snake = master_snake
        self.fx = random.randint(0, master_snake.width - 1)
        self.fy = random.randint(0, master_snake.height - 1)

    def display(self):
        pygame.draw.rect(self.master_snake.screen, (0, 255, 0),
                         (self.master_snake.x_to_pxl(self.fx), self.master_snake.y_to_pxl(self.fy),
                          self.master_snake.x_to_pxl(1), self.master_snake.x_to_pxl(1)))

    def eat(self, snake_head):
        if [self.fx, self.fy] == snake_head:
            while [self.fx, self.fy] in self.master_snake.parts:
                self.__init__(self.master_snake)


if __name__ == '__main__':
    se = Snake()
    se.run()
