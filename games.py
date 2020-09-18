import sys, os
import pygame as pg
from snake import Snake
from sudoku import Sudoku

class GameSelect():
    def __init__(self):
        self.path = os.path.dirname(".\\snake.py")
        
        self.WIDTH = 500
        self.HEIGHT = 500
        self.WIN = pg.display.set_mode((self.WIDTH, self.HEIGHT))
        pg.display.set_caption("Games")
        pg.display.set_icon(pg.image.load(f"{self.path}\\games.png"))
        
        self.BLACK = (255, 255, 255)
        self.WHITE = (0, 0, 0)
        
        self.font = pg.font.SysFont("calibri", 45)
        self.select_text = self.font.render("Select a game", True, self.BLACK)

        self.snake_button = pg.Rect(20, self.HEIGHT // 3, self.WIDTH // 2 - 30, self.HEIGHT // 3 + 75)
        self.sudoku_button = pg.Rect(self.WIDTH // 2 + 10, self.HEIGHT // 3, self.WIDTH // 2 - 30, self.HEIGHT // 3 + 75)

        self.game_font = pg.font.SysFont("calibri", 40)
    
        self.snake_text = self.game_font.render("Snake", True, self.BLACK)
        self.snake_text_size = self.game_font.size("Snake")
        
        self.sudoku_text = self.game_font.render("Sudoku", True, self.BLACK)
        self.sudoku_text_size = self.game_font.size("Sudoku")
        
 
    
    
    def run(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    sys.exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    if self.snake_button.collidepoint(pg.mouse.get_pos()):
                        Snake().run()
                        self.__init__()
                    if self.sudoku_button.collidepoint(pg.mouse.get_pos()):
                        Sudoku().run()
                        self.__init__()

            self.WIN.fill(self.WHITE)
        
            self.WIN.blit(self.select_text, (int(self.WIDTH / 2 - self.font.size("Select a game")[0] / 2), 25))

            pg.draw.rect(self.WIN, self.BLACK, self.snake_button, 5)
            pg.draw.rect(self.WIN, self.BLACK, self.sudoku_button, 5)

            self.WIN.blit(self.snake_text, (int(self.snake_button.centerx - self.snake_text_size[0] / 2), \
                                            int(self.snake_button.centery - self.snake_text_size[1] / 2)))
            self.WIN.blit(self.sudoku_text, (int(self.sudoku_button.centerx - self.sudoku_text_size[0] / 2), \
                                            int(self.sudoku_button.centery - self.sudoku_text_size[1] / 2)))
            
            
            pg.display.update()





if __name__ == "__main__":
    game = GameSelect()
    game.run()