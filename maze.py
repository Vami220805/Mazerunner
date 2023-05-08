from pygame.locals import *
import pygame
import time
 
class Player:
    def __init__(self):
        self.maze = Maze()
        self.pos= 12
        self.move_counter =0

    def moveRight(self):
        self.old_pos = self.pos
        self.move_counter += 1
        self.pos = self.pos + 1
        
 
    def moveLeft(self):
        self.old_pos = self.pos
        self.move_counter += 1
        self.x = self.pos - 1
 
    def moveUp(self):
        self.old_pos = self.pos
        self.move_counter += 1
        self.y = self.pos - 10
 
    def moveDown(self):
        self.old_pos = self.pos
        self.move_counter += 1
        self.y = self.pos + 10

    def changeMaze(self):
        self.maze.maze[self.pos] =2
        if self.move_counter >0:
            self.maze.maze[self.old_pos] = 0
        print(self.maze.maze)
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
 
    def __init__(self):
        self._running = True
        self._display_surf = None
        self._image_surf = None
        self._block_surf = None
        self.player = Player()
        self.maze = Maze()
 
    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((self.windowWidth,self.windowHeight), pygame.HWSURFACE)
        
        pygame.display.set_caption('MAZERUNNER')
        self._running = True
        self._image_surf = pygame.image.load("player.png").convert()
        self._block_surf = pygame.image.load("block.png").convert()
 
    def on_event(self, event):
        if event.type == QUIT:
            self._running = False
 
    def on_loop(self):
        pass
    
    def on_render(self):
        self._display_surf.fill((0,0,0))
        # self._display_surf.blit(self._image_surf,(self.player.x,self.player.y))#dit movet de player
        self.player.changeMaze()
        self.player.draw_player(self._display_surf, self._image_surf)
        self.maze.draw(self._display_surf, self._block_surf)
        pygame.display.flip()
 
    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
 
        while( self._running ):
            pygame.event.pump()
            keys = pygame.key.get_pressed()
            
            if (keys[K_RIGHT]):
                self.player.moveRight()
 
            if (keys[K_LEFT]):
                self.player.moveLeft()
 
            if (keys[K_UP]):
                self.player.moveUp()
 
            if (keys[K_DOWN]):
                self.player.moveDown()
 
            if (keys[K_ESCAPE]):
                self._running = False
 
            self.on_loop()
            self.on_render()
            time.sleep(0.1)
        self.on_cleanup()
 
if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()