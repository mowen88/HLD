from state import State
from settings import *

class PauseMenu(State):
	def __init__(self, game):
		State.__init__(self, game)

		self.next_menu = None
		self.padding = 20

		self.buttons = {
						'Continue': [(HALF_WIDTH, HALF_HEIGHT), 'unpause'],
						'Quit to Menu': [(HALF_WIDTH, HALF_HEIGHT + self.padding), 'main_menu']
						}
		self.fade_surf = pygame.Surface((RES))
		self.fade_surf.fill(BLACK)

	def draw_bounding_box(self, screen):
		box = pygame.Rect(0,0,HALF_WIDTH - 60, HEIGHT - 50)
		box.center = RES/2
		pygame.draw.rect(screen, WHITE, (box), 2)

	def render_button(self, screen, current_menu, next_menu, text_colour, button_colour, hover_colour, pos):
		mx, my = pygame.mouse.get_pos()

		colour = text_colour

		surf = self.game.small_font.render(current_menu, False, colour)
		rect = pygame.Rect(0,0, HALF_WIDTH - 60, surf.get_height() * 1.5)
		rect.center = pos

		if rect.collidepoint(mx, my):
			pygame.draw.rect(screen, hover_colour, rect)#int(HEIGHT * 0.05))
			self.game.render_text(current_menu, text_colour, self.game.small_font, pos)
			if ACTIONS['left_click']:
				self.next_menu = next_menu
		else:
			#pygame.draw.rect(screen, button_colour, rect)#int(HEIGHT * 0.05))
			self.game.render_text(current_menu, text_colour, self.game.small_font, pos)

	def update(self, dt):
		if ACTIONS['p'] or self.next_menu == 'unpause':
			self.next_menu = None 
			self.exit_state()
			self.game.reset_keys()

		elif self.next_menu == 'main_menu':
			self.next_menu = None 
			self.game.quit_write_data()
			self.exit_state()
			self.prev_state.exit_state()
			self.prev_state.prev_state.exit_state()
			self.game.reset_keys()

	def draw(self, screen):
		self.prev_state.draw(screen)

		self.fade_surf.set_alpha(180)
		screen.blit(self.fade_surf, (0,0))

		self.game.render_text('Paused', WHITE, self.game.small_font, (HALF_WIDTH, HALF_HEIGHT - self.padding * 1.5))

		for name, values in self.buttons.items():
			self.render_button(screen, name, values[1], WHITE, LIGHT_GREEN, PINK, values[0])

		self.draw_bounding_box(screen)



