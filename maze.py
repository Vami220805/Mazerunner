from pygame.locals import *
import pygame
import time
 
class Player:
    def __init__(self):
        self.maze = Maze()
        self.game_over = False
        self.game_Won = False
        self.pos= self.maze.start
        self.old_pos = 0
        self.move_counter =0
        self.x_pos = 0
        self.y_pos = 0

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

            self.maze.maze[self.pos] = 2
        except IndexError:
            self.maze.maze[self.old_pos] = 0
            self.pos = self.maze.start
            self.game_Won = True
    
    def draw_player(self,display_surf,image_surf):
       bx = 0
       by = 0
       color = (0, 0, 0)
       for i in range(0,self.maze.M*self.maze.N):
            if self.maze.maze[ bx + (by*self.maze.M) ] == 2:
                display_surf.blit(image_surf,( bx * 29 , by * 30))
                self.x_pos = bx * 29
                self.world_x_pos = -bx * 29
                self.y_pos = by* 30
                self.world_y_pos = -by* 30
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
               display_surf.blit(image_surf,( bx * 29 , by * 31))
      
           bx = bx + 1
           if bx > self.M-1:
               bx = 0 
               by = by + 1


class App:
 
    windowWidth = 800
    windowHeight = 600
    player = 0
    game_state = "start_menu"
    FPS =60
 
    def __init__(self):
        self._running = True
        self.zoom = 1
        self._display_surf = None
        self._screen = None
        self._image_surf = None
        self._block_surf = None
        self.fullscreen = False
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
        self._display_surf.blit(next_level, (self.windowWidth  - next_level.get_width() * 1.5, self.windowHeight * 0 + next_level.get_height()/2))
        self._display_surf.blit(previous_level, ( 50, previous_level.get_height()/2))
        pygame.display.update()

    def set_display(self):
        pygame.Surface(self.get_resolution())
        if self.fullscreen:
            pygame.Surface(self._max_display)
            pygame.display.set_mode(self._max_display, pygame.FULLSCREEN)
        else:
            pygame.Surface((self.windowWidth,self.windowHeight))
            pygame.display.set_mode((self.windowWidth,self.windowHeight))
        return
    
    
    def get_resolution(self):
        if self.fullscreen:
            return self._max_display[0] * self.scale, self._max_display[1] * self.scale
        else:
            return self.windowWidth * self.scale, self.windowHeight * self.scale

    def on_init(self):
        pygame.init()
        pygame.mixer.init()
        pygame.font.init()
        # self._draw_surface = pygame.Surface((self.windowWidth,self.windowHeight))
        self._screen = pygame.display.set_mode((self.windowWidth/2,self.windowHeight/2))
        self.world = pygame.Surface((self.windowWidth,self.windowHeight)) # Create Map Surface
        self.world.fill((0, 0, 0)) # Fill Map Surface Black
        # self._display_surf = pygame.display.set_mode((self.windowWidth,self.windowHeight))
        self._display_surf = pygame.display.set_mode((self.windowWidth,self.windowHeight), pygame.HWSURFACE)
        self._max_display = pygame.display.Info().current_w, pygame.display.Info().current_h
        self.scale = 1
        self.fullscreen = False
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('MAZERUNNER')
        self._running = True
        self._image_surf = pygame.image.load("images/player.png").convert()
        self._image_surf.set_colorkey((0, 0, 0))
        self._block_surf = pygame.image.load("images/block.png").convert()
    
    def on_render(self):
        if self.game_state == "start_menu":
            self.draw_start_menu()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                self.game_state = "game"

        if self.game_state == "game":
            self.player.changeMaze()
            # self._display_surf = pygame.Surface((int(self.windowWidth / self.zoom), int(self.windowHeight / self.zoom)))
            # self._display_surf = pygame.display.set_mode((int(self.windowWidth / self.zoom), int(self.windowHeight / self.zoom)))         
            self.world.fill((0, 0, 0)) # Fill Map Surface Black
            self._display_surf.fill((0, 0, 0)) # Fill Map Surface Black
            self.maze.draw(self.world, self._block_surf)
            self.player.draw_player(self.world, self._image_surf)
            # print(self.player.x_pos, self.player.y_pos, self.player.world_x_pos, self.player.world_y_pos)
            self._display_surf.blit(self.world,(self.player.world_x_pos + self.windowWidth / 3 ,self.player.world_y_pos+ self.windowHeight / 3))
            self._screen.blit(pygame.transform.scale(self._display_surf,(self.windowWidth,self.windowHeight)),(0,0))
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

            if self.game_state == "game":
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

            for event in pygame.event.get():
                if event.type == QUIT:
                    self._running = False
            
            if (keys[K_f]):
                self.fullscreen = not self.fullscreen
                self.set_display()
 
            self.clock.tick(self.FPS)
            self.on_render()
            time.sleep(0.1)
        self.on_cleanup()
 
if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()