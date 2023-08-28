import pygame
from state import State
from settings import *

class Dialogue(State):
    def __init__(self, game, zone, cutscene_number, sprite, dialog_number, duration):
        super().__init__(game)

        self.game = game
        self.cutscene_number = cutscene_number
        self.sprite = sprite
        self.dialog_number = dialog_number
        self.sprite = sprite
        self.duration = duration
        self.offset = self.sprite.zone.rendered_sprites.offset

        self.opening = True

        # text box variables
        self.box_colour = BLACK
        self.text_colour = YELLOW
        self.box_width = 0
        self.center = (self.sprite.rect.centerx - self.offset.x, self.sprite.rect.top - 25 - self.offset.y)
        self.target_width = TILESIZE * 10
        self.line_spacing = 10

        self.lines = DIALOGUE[self.cutscene_number][self.dialog_number]
        self.char_indices = [0] * len(self.lines)

        self.timer = 0

    def text_update(self):
        if not self.char_indices[-1] >= len(self.lines[-1]):
            if self.timer > 2:
                self.timer = 0

                for line in range(len(self.lines)):
                    self.char_indices[line] += 1
                    if self.char_indices[line] > len(self.lines[line]):
                        self.char_indices[line] = len(self.lines[line])
                    else:
                        break

    def opening_box(self, dt):
        if not self.opening:
            self.box_width -= (self.target_width - self.box_width) * 0.3 * dt

            if self.box_width <= 0:
                self.box_width = 0
                self.opening = True
                self.exit_state()

        elif self.box_width < self.target_width - 1:
            self.box_width += (self.target_width - self.box_width) * 0.2 * dt

        self.center = (self.sprite.rect.centerx - self.offset.x, self.sprite.rect.top - 25 - self.offset.y)

    def draw_box(self, screen):
        if self.timer > self.duration:
            self.opening = False

        else:
            # draw arrow to sprite head
            vertices = [(self.center[0] - 5, self.center[1] + 20), (self.center[0] + 5, self.center[1] + 20), (self.sprite.rect.midtop - self.offset)]
            pygame.draw.polygon(self.game.screen, self.box_colour, vertices, 0)

        pygame.draw.rect(screen, self.box_colour, (self.center[0] - self.box_width/2, self.center[1] - 25, self.box_width, 45), border_radius = 8)

    def draw_text(self):
        total_height = len(self.lines) * self.line_spacing
        start_y = self.center[1] - total_height // 2
        
        if self.opening:
            for index, line in enumerate(self.lines):
                rendered_line = self.lines[index][:self.char_indices[index]]
                y_position = start_y + self.line_spacing * index
                self.game.render_text(rendered_line, self.text_colour, self.game.small_font, (self.center[0], y_position))

    def update(self, dt):
        self.timer += dt
        self.prev_state.update(dt)
        self.opening_box(dt)
        self.text_update()

    def draw(self, screen):
        self.prev_state.draw(screen)
        self.draw_box(screen)
        self.draw_text()
