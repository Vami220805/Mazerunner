from pygame.locals import *
import pygame
import time
 
class Player:
    def __init__(self):
        self.maze = Maze()
        self.game_over = False
        self.game_Won = False
        self.pos= self.maze.start
        self.move_counter =0

    def moveRight(self):
        self.old_pos = self.pos
        self.move_counter += 1
        self.pos = self.pos + 1
        
    def moveLeft(self):
        self.old_pos = self.pos
        self.move_counter += 1
        self.pos = self.pos - 1
 
    def moveUp(self):
        self.old_pos = self.pos
        self.move_counter += 1
        self.pos = self.pos - self.maze.M
 
    def moveDown(self):
        self.old_pos = self.pos
        self.move_counter += 1
        self.pos = self.pos + self.maze.M

    def changeMaze(self):
        try:
            if self.maze.maze[self.pos] == 1:
                self.pos = self.old_pos
            elif self.move_counter >0:
                self.maze.maze[self.old_pos] = 0

            self.maze.maze[self.pos] =2
            print(self.maze.maze)
        except IndexError:
            self.game_Won = True
            self.maze.maze[self.old_pos] = 0
            self.pos = self.maze.start
    
    def draw_player(self,display_surf,image_surf):
       bx = 0
       by = 0
       for i in range(0,self.maze.M*self.maze.N):
            if self.maze.maze[ bx + (by*self.maze.M) ] == 2:
               display_surf.blit(image_surf,( bx * 29 , by * 30))
            bx = bx + 1
            if bx > self.maze.M-1:
               bx = 0 
               by = by + 1
 
class Maze:
    def __init__(self):
       self.M = 10
       self.N = 9
       self.start = 11
       self.maze = [1,1,1,1,1,1,1,1,1,1,
                    1,0,1,0,0,0,0,1,0,1,
                    1,0,0,0,1,1,1,0,1,1,
                    1,0,1,0,0,0,0,0,0,1,
                    1,0,1,1,1,1,1,1,0,1,
                    1,0,0,0,0,0,0,1,0,1,
                    1,1,1,1,1,1,0,1,0,1,
                    1,0,0,0,0,0,0,1,0,1,
                    1,1,1,1,1,1,1,1,0,1]
    #    self.maze = [ 1,1,1,1,1,1,1,1,1,1,
    #                  1,0,0,0,0,0,0,0,0,1,
    #                  1,0,0,0,0,0,0,0,0,1,
    #                  1,0,1,1,1,1,1,1,0,1,
    #                  1,0,1,0,0,0,0,0,0,1,
    #                  1,0,1,0,1,1,1,1,0,1,
    #                  1,0,0,0,0,0,0,0,0,1,
    #                  1,1,1,1,1,1,1,1,1,1,]

    def draw(self,display_surf,image_surf):
       bx = 0
       by = 0
       for i in range(0,self.M*self.N):
           if self.maze[ bx + (by*self.M) ] == 1:
               display_surf.blit(image_surf,( bx * 29 , by * 30))
      
           bx = bx + 1
           if bx > self.M-1:
               bx = 0 
               by = by + 1


class App:
 
    windowWidth = 800
    windowHeight = 600
    player = 0
    game_state = "start_menu"
 
    def __init__(self):
        self._running = True
        self._display_surf = None
        self._image_surf = None
        self._block_surf = None
        self.player = Player()
        self.maze = Maze()

    def draw_start_menu(self):
        self._display_surf.fill((0,0,0))
        font = pygame.font.SysFont('arial', 40)
        title = font.render('My Game', True, (255, 255, 255))
        start_button = font.render('Start', True, (255, 255, 255))
        self._display_surf.blit(title, (self.windowWidth/2 - title.get_width()/2, self.windowHeight/2 - title.get_height()/2))
        self._display_surf.blit(start_button, (self.windowWidth/2 - start_button.get_width()/2, self.windowHeight/2 + start_button.get_height()/2))
        pygame.display.update()
 
    def draw_game_over_screen(self):
        self._display_surf.fill((0, 0, 0))
        font = pygame.font.SysFont('arial', 40)
        title = font.render('Game Over', True, (255, 255, 255))
        restart_button = font.render('R - Restart', True, (255, 255, 255))
        quit_button = font.render('ESC - Quit', True, (255, 255, 255))
        self._display_surf.blit(title, (self.windowWidth/2 - title.get_width()/2, self.windowHeight/2 - title.get_height()/3))
        self._display_surf.blit(restart_button, (self.windowWidth/2 - restart_button.get_width()/2, self.windowHeight/1.9 + restart_button.get_height()))
        self._display_surf.blit(quit_button, (self.windowWidth/2 - quit_button.get_width()/2, self.windowHeight/2 + quit_button.get_height()/2))
        pygame.display.update()

    def draw_game_Won_screen(self):
        self._display_surf.fill((0, 0, 0))
        font = pygame.font.SysFont('arial', 40)
        title = font.render('Game Won', True, (255, 255, 255))
        restart_button = font.render('R - Restart', True, (255, 255, 255))
        quit_button = font.render('ESC - Quit', True, (255, 255, 255))
        next_level = font.render('> - next', True, (255, 255, 255))
        previous_level = font.render('< - previous', True, (255, 255, 255))
        self._display_surf.blit(title, (self.windowWidth/2 - title.get_width()/2, self.windowHeight/2 - title.get_height()/3))
        self._display_surf.blit(restart_button, (self.windowWidth/2 - restart_button.get_width()/2, self.windowHeight/1.9 + restart_button.get_height()))
        self._display_surf.blit(quit_button, (self.windowWidth/2 - quit_button.get_width()/2, self.windowHeight/2 + quit_button.get_height()/2))
        self._display_surf.blit(next_level, (self.windowWidth/2 - next_level.get_width()/2, self.windowHeight * 0 + next_level.get_height()/2))
        self._display_surf.blit(previous_level, (self.windowWidth/2 - previous_level.get_width()/2, self.windowHeight* 0 + previous_level.get_height()/2))
        pygame.display.update()

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((self.windowWidth,self.windowHeight), pygame.HWSURFACE)
        
        pygame.display.set_caption('MAZERUNNER')
        self._running = True
        self._image_surf = pygame.image.load("images/player.png").convert()
        self._block_surf = pygame.image.load("images/block.png").convert()
 
    def on_event(self, event):
        if event.type == QUIT:
            self._running = False
 
    def on_loop(self):
        pass
    
    def on_render(self):
        if self.game_state == "start_menu":
            self.draw_start_menu()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                self.game_state = "game"

        if self.game_state == "game":
            self._display_surf.fill((0,0,0))
            self.player.changeMaze()
            self.player.draw_player(self._display_surf, self._image_surf)
            self.maze.draw(self._display_surf, self._block_surf)
            pygame.display.flip()

        if self.player.game_over == True:
            self.game_state = "game_over"
            self.draw_game_over_screen()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                self.game_state = "start_menu"
                self.player.game_over = False
        
        if self.player.game_Won == True:
            self.game_state = "game_Won"
            self.draw_game_Won_screen()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                self.game_state = "start_menu"
                self.player.game_Won = False
 
    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
 
        while( self._running ):
            pygame.event.pump()
            keys = pygame.key.get_pressed()
            
            if (keys[K_RIGHT] or keys[K_d]):
                self.player.moveRight()
 
            elif (keys[K_LEFT]or keys[K_a]):
                self.player.moveLeft()
 
            elif (keys[K_UP]or keys[K_w]):
                self.player.moveUp()
 
            elif (keys[K_DOWN]or keys[K_s]):
                self.player.moveDown()
 
            if (keys[K_ESCAPE]):
                self._running = False
 
            self.on_loop()
            self.on_render()
            time.sleep(0.15)
        self.on_cleanup()
 
if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()