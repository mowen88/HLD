
from state import State
from zone import Zone
from cutscenes.transition import MenuTransition
from sprites import FadeSurf
from settings import *

class MainMenu(State):
	def __init__(self, game):
		State.__init__(self, game)

		self.game = game
		self.alpha = 255
		self.next_menu = None
		self.padding = 20

		self.buttons = {
						'Start': [(HALF_WIDTH, HALF_HEIGHT - self.padding), 'slot_menu'],
						'Options': [(HALF_WIDTH, HALF_HEIGHT), 'options_menu'],
						'Quit': [(HALF_WIDTH, HALF_HEIGHT + self.padding), 'slot_menu']
						}

		# menu transitioning
		self.transitioning = False
		self.transition_screen = MenuTransition(self)

	def render_button(self, screen, current_menu, next_menu, text_colour, button_colour, hover_colour, pos):
		mx, my = pygame.mouse.get_pos()

		colour = text_colour

		surf = self.game.small_font.render(current_menu, False, colour)
		rect = pygame.Rect(0,0, HALF_WIDTH, surf.get_height() * 1.5)
		rect.center = pos

		if rect.collidepoint(mx, my) and not self.transitioning:
			pygame.draw.rect(screen, hover_colour, rect, border_radius=4)#int(HEIGHT * 0.05))
			self.game.render_text(current_menu, text_colour, self.game.small_font, pos)
			if ACTIONS['left_click']:
				self.next_menu = next_menu
		else:
			pygame.draw.rect(screen, button_colour, rect, border_radius=4)#int(HEIGHT * 0.05))
			self.game.render_text(current_menu, text_colour, self.game.small_font, pos)

	def go_to(self, state):
		if state == 'slot_menu':
			SlotMenu(self.game).enter_state()
		elif state == 'options_menu':
			OptionsMenu(self.game).enter_state()
		elif state == 'main_menu':
			MainMenu(self.game).enter_state()
		elif state in '123':
			StartGameMenu(self.game).enter_state()
		else:
			Zone(self.game, PLAYER_DATA['current_zone'], PLAYER_DATA['entry_pos']).enter_state()

	def update(self, dt):
		self.transition_screen.update(dt)
		if self.next_menu is not None:
			self.transitioning = True

	def draw(self, screen):
		screen.fill(BLACK)

		for name, values in self.buttons.items():
			self.render_button(screen, name, values[1], BLACK, LIGHT_GREEN, PINK, values[0])

		self.transition_screen.draw(screen)

class SlotMenu(MainMenu):
	def __init__(self, game):
		super().__init__(game)

		self.buttons = {
				'Slot 1': [(HALF_WIDTH, HALF_HEIGHT - self.padding * 1.5), '1'],
				'Slot 2': [(HALF_WIDTH, HALF_HEIGHT - self.padding * 0.5), '2'],
				'Slot 3': [(HALF_WIDTH, HALF_HEIGHT + self.padding * 0.5), '3'],
				'Back': [(HALF_WIDTH, HALF_HEIGHT + self.padding * 1.5), 'main_menu'],
				}

	def get_slot(self):
		self.game.slot = self.next_menu
		self.game.read_data('player_data')
		self.game.read_data('completed_data')
		print(PLAYER_DATA)
		print(COMPLETED_DATA)

	def update(self, dt):
		self.game.slot = self.next_menu
		self.transition_screen.update(dt)
		if self.next_menu is not None:
			self.transitioning = True
			self.get_slot()

	def draw(self, screen):
		screen.fill(BLACK)
		
		for name, values in self.buttons.items():
			self.render_button(screen, name, values[1], BLACK, LIGHT_GREEN, PINK, values[0])

		self.transition_screen.draw(screen)


class OptionsMenu(MainMenu):
	def __init__(self, game):
		super().__init__(game)

		self.buttons = {
				'SFX': [(HALF_WIDTH, HALF_HEIGHT - self.padding), 'main_menu'],
				'Music': [(HALF_WIDTH, HALF_HEIGHT), 'main_menu'],
				'Back': [(HALF_WIDTH, HALF_HEIGHT + self.padding), 'main_menu']
				}

	def update(self, dt):
		self.transition_screen.update(dt)
		if self.next_menu is not None:
			self.transitioning = True

	def draw(self, screen):
		screen.fill(BLACK)
		
		for name, values in self.buttons.items():
			self.render_button(screen, name, values[1], BLACK, LIGHT_GREEN, PINK, values[0])

		self.transition_screen.draw(screen)

class StartGameMenu(MainMenu):
	def __init__(self, game):
		super().__init__(game)

		self.buttons = {
				'Continue': [(HALF_WIDTH, HALF_HEIGHT - self.padding * 0.5), 'GO!!!'],
				'Back': [(HALF_WIDTH, HALF_HEIGHT + self.padding * 0.5), 'slot_menu']
				}

	def update(self, dt):
		self.transition_screen.update(dt)
		if self.next_menu is not None:
			self.transitioning = True

	def draw(self, screen):
		screen.fill(BLACK)
		
		for name, values in self.buttons.items():
			self.render_button(screen, name, values[1], BLACK, LIGHT_GREEN, PINK, values[0])

		self.transition_screen.draw(screen)



