import pygame, sys
from settings import *
from os import walk
from intro import Intro

class Game:
    def __init__(self):

        pygame.init()

        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((RES), pygame.FULLSCREEN|pygame.SCALED)
        self.running = True

        #font
        self.big_font =  pygame.font.Font(FONT, round(HEIGHT * 0.12))
        self.small_font = pygame.font.Font(FONT, round(HEIGHT * 0.05))

        # states
        self.stack = []
        self.screenshaking = False
      
        self.load_states()

        #stats
        self.current_health = PLAYER_DATA['max_health']
        self.current_bullets = PLAYER_DATA['max_bullets']

    def get_events(self):
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    ACTIONS['escape'] = True
                    self.running = False
                elif event.key == pygame.K_UP:
                    ACTIONS['up'] = True
                elif event.key == pygame.K_DOWN:
                    ACTIONS['down'] = True
                elif event.key == pygame.K_RIGHT:
                    ACTIONS['right'] = True
                elif event.key == pygame.K_LEFT:
                    ACTIONS['left'] = True
                elif event.key == pygame.K_SPACE:
                    ACTIONS['space'] = True
                elif event.key == pygame.K_RCTRL:
                    ACTIONS['right_ctrl'] = True
                elif event.key == pygame.K_RETURN:
                    ACTIONS['return'] = True
                elif event.key == pygame.K_BACKSPACE:
                    ACTIONS['backspace'] = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    ACTIONS['up'] = False
                elif event.key == pygame.K_DOWN:
                    ACTIONS['down'] = False
                elif event.key == pygame.K_RIGHT:
                    ACTIONS['right'] = False
                elif event.key == pygame.K_LEFT:
                    ACTIONS['left'] = False
                elif event.key == pygame.K_SPACE:
                    ACTIONS['space'] = False
                elif event.key == pygame.K_RETURN:
                    ACTIONS['return'] = False
                elif event.key == pygame.K_BACKSPACE:
                    ACTIONS['backspace'] = False

            if event.type == pygame.MOUSEWHEEL:

                if event.y == 1:
                    ACTIONS['scroll_up'] = True
                elif event.y == -1:
                    ACTIONS['scroll_down'] = True

            if event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1:
                    ACTIONS['left_click'] = True
                elif event.button == 3:
                    ACTIONS['right_click'] = True
                elif event.button == 4:
                    ACTIONS['scroll_down'] = True
                elif event.button == 2:
                    ACTIONS['scroll_up'] = True

            if event.type == pygame.MOUSEBUTTONUP:

                if event.button == 1:
                    ACTIONS['left_click'] = False
                elif event.button == 3:
                    ACTIONS['right_click'] = False
                elif event.button == 4:
                    ACTIONS['scroll_down'] = False
                elif event.button == 2:
                    ACTIONS['scroll_up'] = False

    def reset_keys(self):
        for action in ACTIONS:
            ACTIONS[action] = False

    def load_states(self):
        self.intro = Intro(self)
        self.stack.append(self.intro)

    def get_folder_images(self, path):
        surf_list = []
        for _, __, img_files in walk(path):
            for img in img_files:
                full_path = path + '/' + img
                img_surf = pygame.image.load(full_path).convert_alpha()
                surf_list.append(img_surf)

        return surf_list

    def custom_cursor(self, screen): 
        pygame.mouse.set_visible(False)
        cursor = self.get_image('../assets/cursor.png', pygame.mouse.get_pos())
        cursor[0].set_alpha(150)
        screen.blit(cursor[0], cursor[1])

    def get_image(self, path, pos):
        surf = pygame.image.load(path).convert_alpha()
        rect = surf.get_rect(center = pos)
        return(surf, rect)

    def render_text(self, text, colour, font, pos):
        surf = font.render(str(text), False, colour)
        rect = surf.get_rect(center = pos)
        self.screen.blit(surf, rect)

    def update(self, dt):
        pygame.display.set_caption(str(round(self.clock.get_fps(), 2)))
        self.stack[-1].update(dt)

    def draw(self, screen):

        self.stack[-1].draw(screen)
        self.custom_cursor(screen)
        pygame.display.flip()

    def main_loop(self):
        dt = (self.clock.tick()/1000) * FPS
        self.get_events()
        self.update(dt)
        self.draw(self.screen)        

if __name__ == "__main__":
    game = Game()
    while game.running:
        game.main_loop()