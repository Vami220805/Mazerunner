from pygame.locals import *
import pygame
import time
import os
import json
 
class Data:
    def __init__(self):
        with open('data.json', 'r') as openfile:
            self.maze = json.load(openfile)
        self.game_over = False
        self.game_Won = False
        self.start = 11
        self.level = 0
        self.pos = self.start
        self.old_pos = 0
        self.move_counter =0
        self.M = 10
        self.N = 9

    def moveRight(self):
        self.old_pos = self.pos
        self.move_counter += 1
        self.pos += 1
        
    def moveLeft(self):
        self.old_pos = self.pos
        self.move_counter += 1
        self.pos -= 1
 
    def moveUp(self):
        self.old_pos = self.pos
        self.move_counter += 1
        self.pos -= self.M
 
    def moveDown(self):
        self.old_pos = self.pos
        self.move_counter += 1
        self.pos += self.M

    def changeMaze(self):
        try:
            print(self.maze[self.level])
            if self.maze[self.level][self.pos] == 1 or self.maze[self.level][self.pos] == 5:
                self.pos = self.old_pos
            elif self.move_counter >0:
                self.maze[self.level][self.old_pos] = 0
            self.maze[self.level][self.pos] = 2 
        except IndexError:
            self.maze[self.level][self.old_pos] = 0
            self.pos = self.start
            self.game_Won = True

    def draw(self,display_surf,image_surf, player, trap, fake_wall,floor):
       bx = 0
       by = 0
       for i in range(0,self.M*self.N):
            if self.maze[self.level][ bx + (by*self.M) ] == 0 or 2:
                display_surf.blit(floor,( bx * 100 , by * 100))
            if self.maze[self.level][ bx + (by*self.M) ] == 1:
                display_surf.blit(image_surf,( bx * 100 , by * 100))
            if self.maze[self.level][ bx + (by*self.M) ] == 2:
                display_surf.blit(player,( bx * 100 , by * 100))
                self.x_pos = bx * 100
                self.world_x_pos = -bx * 100
                self.y_pos = by* 100
                self.world_y_pos = -by* 100
            if self.maze[self.level][ bx + (by*self.M) ] == 5:
                display_surf.blit(trap,( bx * 100 , by * 100))
            if self.maze[self.level][ bx + (by*self.M) ] == 6:
                display_surf.blit(fake_wall,( bx * 100 , by * 100))
            
      
            bx = bx + 1
            if bx > self.M-1:
                bx = 0 
                by = by + 1
                

class Button():
	def __init__(self, image, pos, text_input, font, base_color, hovering_color):
		self.image = image
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.font = font
		self.base_color, self.hovering_color = base_color, hovering_color
		self.text_input = text_input
		self.text = self.font.render(self.text_input, True, self.base_color)
		if self.image is None:
			self.image = self.text
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

	def update(self, screen):
		if self.image is not None:
			screen.blit(self.image, self.rect)
		screen.blit(self.text, self.text_rect)

	def checkForInput(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False

	def changeColor(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.text = self.font.render(self.text_input, True, self.hovering_color)
		else:
			self.text = self.font.render(self.text_input, True, self.base_color)


class App:
    def __init__(self):
        self.windowWidth = 1200
        self.windowHeight = 1000
        self.game_state = "start_menu"
        self.FPS =60
        self._running = True
        self._display_surf = None
        self._screen = None
        self._image_surf = None
        self._block_surf = None
        self.fullscreen = False
        self.toggle_interval = 0.045
        self.data = Data()

    def on_init(self):
        pygame.init()
        pygame.mixer.init()
        pygame.font.init()
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (350,30)
        self._screen = pygame.display.set_mode((self.windowWidth/2,self.windowHeight/2))
        self.world = pygame.Surface((self.windowWidth,self.windowHeight)) # Create Map Surface
        self.world.fill((0, 0, 0)) # Fill Map Surface Black
        self._display_surf = pygame.display.set_mode((self.windowWidth,self.windowHeight), pygame.HWSURFACE)
        self._max_display = pygame.display.Info().current_w, pygame.display.Info().current_h
        self.scale = 3
        self.fullscreen = False
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('MAZERUNNER')
        self._running = True
        self._image_surf = pygame.image.load("images/player.png").convert()
        self._image_surf.set_colorkey((0, 0, 0))
        self._block_surf = pygame.image.load("images/block.png").convert()
        self._floor_surf = pygame.image.load("images/floor.png").convert()
        self._trap_surf = pygame.image.load("images/trap.png").convert()
        self._fake_wall_surf = pygame.image.load("images/fake_wall.png").convert()
        self.background = pygame.image.load("images/background.png")
    
    def on_render(self):
        if self.game_state == "start_menu":
            self.draw_start_menu()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                self.game_state = "game"

        if self.game_state == "game":
            self.data.changeMaze()
            self.world.fill((0, 0, 0)) # Fill Map Surface Black
            self._display_surf.fill((0, 0, 0)) # Fill Map Surface Black
            self.data.draw(self.world, self._block_surf, self._image_surf, self._trap_surf, self._fake_wall_surf, self._floor_surf)
            self._display_surf.blit(self.world,(self.data.world_x_pos + self.windowWidth / 3 ,self.data.world_y_pos+ self.windowHeight / 3))
            self._screen.blit(pygame.transform.scale(self._display_surf,(self.windowWidth,self.windowHeight)),(0,0))
            pygame.display.flip()

        if self.data.game_over == True:
            self.game_state = "game_over"
            self.draw_game_over_screen()
            keys = pygame.key.get_pressed()
            print(self.data.level)
            if keys[pygame.K_r]:
                self.game_state = "game"
                self.data.game_over = False
            if keys[K_LEFT]:
                if self.data.level >= 1:
                    self.data.level -=1
                    self.game_state = "game"
                    self.data.game_Won = False
        
        if self.data.game_Won == True:
            self.game_state = "game_Won"
            self.draw_game_Won_screen()

    def draw_start_menu(self):
        self._display_surf.blit(self.background, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = pygame.font.Font("font.ttf", 100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(self.windowWidth/2, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("images/Play Rect.png"), pos=(self.windowWidth/2, 250), 
                            text_input="PLAY", font=pygame.font.Font("font.ttf", 75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("images/Quit Rect.png"), pos=(self.windowWidth/2, 550), 
                            text_input="QUIT", font=pygame.font.Font("font.ttf", 75), base_color="#d7fcd4", hovering_color="White")

        self._display_surf.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(self._display_surf)
        
        for event in pygame.event.get():
            if event.type == QUIT:
                self._running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    self.game_state = "game"
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    self._running = False

        pygame.display.update()
 
    def draw_game_over_screen(self):
        self._display_surf.fill((0, 0, 0))
        font = pygame.font.SysFont('arial', 40)
        title = font.render('Game Over', True, (255, 255, 255))
        restart_button = font.render('R - Restart', True, (255, 255, 255))
        quit_button = font.render('ESC - Quit', True, (255, 255, 255))
        previous_level = font.render('< - previous', True, (255, 255, 255))
        self._display_surf.blit(title, (self.windowWidth/2 - title.get_width()/2, self.windowHeight/2 - title.get_height()/3))
        self._display_surf.blit(restart_button, (self.windowWidth/2 - restart_button.get_width()/2, self.windowHeight/1.9 + restart_button.get_height()))
        self._display_surf.blit(quit_button, (self.windowWidth/2 - quit_button.get_width()/2, self.windowHeight/2 + quit_button.get_height()/2))
        self._display_surf.blit(previous_level, ( 50, previous_level.get_height()/2))
        pygame.display.update()




    def draw_game_Won_screen(self):
        self._display_surf.blit(self.background, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = pygame.font.Font("font.ttf", 100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(self.windowWidth/2, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("images/Retry Rect.png"), pos=(self.windowWidth/2, 250), 
                            text_input="RETRY", font=pygame.font.Font("font.ttf", 75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("images/Quit Rect.png"), pos=(self.windowWidth/2, 550), 
                            text_input="QUIT", font=pygame.font.Font("font.ttf", 75), base_color="#d7fcd4", hovering_color="White")
        NEXT_BUTTON = Button(image=pygame.image.load("images/Next Rect.png"), pos=(self.windowWidth - self.windowWidth/4, 750), 
                            text_input="NEXT", font=pygame.font.Font("font.ttf", 75), base_color="#d7fcd4", hovering_color="White")
        PREV_BUTTON = Button(image=pygame.image.load("images/Prev Rect.png"), pos=(self.windowWidth/4, 750), 
                            text_input="PREV", font=pygame.font.Font("font.ttf", 75), base_color="#d7fcd4", hovering_color="White")

        self._display_surf.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, QUIT_BUTTON,NEXT_BUTTON,PREV_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(self._display_surf)
        
        for event in pygame.event.get():
            if event.type == QUIT:
                self._running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    self.game_state = "game"
                    self.data.game_Won = False
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    self._running = False
                if NEXT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    if self.data.level <(len(self.data.maze) -1):
                        self.data.level +=1
                        self.game_state = "game"
                        self.data.move_counter =0
                        self.data.game_Won = False
                if PREV_BUTTON.checkForInput(MENU_MOUSE_POS):
                    if self.data.level >= 1:
                        self.data.level -=1
                        self.game_state = "game"
                        self.data.move_counter =0
                        self.data.game_Won = False


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
 
    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
 
        while( self._running ):
            pygame.event.pump()
            keys = pygame.key.get_pressed()
            self.start_time = time.time()

            if self.game_state == "game":
                if (keys[K_RIGHT] or keys[K_d]):
                    self.data.moveRight()
    
                elif (keys[K_LEFT]or keys[K_a]):
                    self.data.moveLeft()
    
                elif (keys[K_UP]or keys[K_w]):
                    self.data.moveUp()
    
                elif (keys[K_DOWN]or keys[K_s]):
                    self.data.moveDown()
            
                # Wait until the desired interval is reached
                while time.time() - self.start_time < self.toggle_interval:
                    pass
    
                while time.time() - self.start_time < 2 * self.toggle_interval:
                    self.passtoggle_interval = 0.045
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
        self.on_cleanup()
 
if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()