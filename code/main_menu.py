
from state import State
from zone import Zone
from cutscenes.transition import MenuTransition
from sprites import FadeSurf
from settings import *

class Intro(State):
	def __init__(self, game):
		State.__init__(self, game)

		self.game = game
		self.alpha = 255
		self.next_menu = None
		self.padding = 20

		self.buttons = {
						'Start': [(HALF_WIDTH, HALF_HEIGHT - self.padding), 'slot_menu'],
						}

		# menu transitioning
		self.transitioning = False
		self.transition_screen = MenuTransition(self)

	def render_button(self, screen, current_menu, text_colour, button_colour, hover_colour, pos):
		mx, my = pygame.mouse.get_pos()

		colour = text_colour

		surf = self.game.small_font.render(current_menu, False, colour)
		rect = pygame.Rect(0,0, HALF_WIDTH, surf.get_height() * 1.5)
		rect.center = pos

		if rect.collidepoint(mx, my) and not self.transitioning:
			pygame.draw.rect(screen, hover_colour, rect, border_radius=4)#int(HEIGHT * 0.05))
			self.game.render_text(current_menu, text_colour, self.game.small_font, pos)
			if ACTIONS['left_click']:
				self.transitioning = True
		else:
			pygame.draw.rect(screen, button_colour, rect, border_radius=4)#int(HEIGHT * 0.05))
			self.game.render_text(current_menu, text_colour, self.game.small_font, pos)

	def go_to(self, state):
		MainMenu(self.game).enter_state()

	def update(self, dt):
		self.transition_screen.update(dt)

	def draw(self, screen):
		screen.fill(BLACK)

		self.render_button(screen, 'Press Enter', BLACK, LIGHT_GREEN, PINK, RES/2)

		self.transition_screen.draw(screen)

class MainMenu(State):
	def __init__(self, game):
		State.__init__(self, game)

		if len(self.game.stack) > 1:
			self.game.stack.pop()

		self.game = game
		self.alpha = 255
		self.next_menu = None
		self.padding = 20

		self.buttons = {
						'Start': [(HALF_WIDTH, HALF_HEIGHT - self.padding), 'slot_menu'],
						'Options': [(HALF_WIDTH, HALF_HEIGHT), 'options_menu'],
						'Quit': [(HALF_WIDTH, HALF_HEIGHT + self.padding), 'quit']
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
		if state == 'quit':
			self.game.quit_write_data()
			self.game.running = False

		elif state == 'slot_menu':
			SlotMenu(self.game).enter_state()
		elif state == 'options_menu':
			OptionsMenu(self.game).enter_state()
		elif state == 'main_menu':
			MainMenu(self.game).enter_state()
		elif state in '123':
			StartGameMenu(self.game).enter_state()
		elif state == 'DELETE_SLOT':
			AreYouSureMenu(self.game).enter_state()
		elif state == 'delete_confirmed':
			Confirmation(self.game).enter_state()
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
		if self.next_menu is not None and self.next_menu in '123':
			self.game.read_data('player_data')
			self.game.read_data('completed_data')

	def update(self, dt):
		self.get_slot()
		self.transition_screen.update(dt)
		if self.next_menu is not None:
			self.transitioning = True

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
				'Continue': [(HALF_WIDTH, HALF_HEIGHT - self.padding), 'GO!!!'],
				'Clear Data': [(HALF_WIDTH, HALF_HEIGHT), 'DELETE_SLOT'],
				'Back': [(HALF_WIDTH, HALF_HEIGHT + self.padding), 'slot_menu']
				}

	def show_stats(self):
		if self.game.slot is not None:
			self.game.render_text(self.game.slot_data[self.game.slot]['percent complete'], WHITE, self.game.small_font, (HALF_WIDTH, HALF_HEIGHT - self.padding * 2))
			self.game.render_text(PLAYER_DATA['time'], WHITE, self.game.small_font, (HALF_WIDTH, HALF_HEIGHT - self.padding * 3))

	def start_timer(self):
		if self.next_menu == 'GO!!!' and self.alpha >= 255:
			self.game.timer.stop_start()

	def update(self, dt):
		self.transition_screen.update(dt)
		if self.next_menu is not None:
			self.start_timer()
			self.transitioning = True

	def draw(self, screen):
		screen.fill(BLACK)

		self.show_stats()
		
		for name, values in self.buttons.items():
			self.render_button(screen, name, values[1], BLACK, LIGHT_GREEN, PINK, values[0])

		self.transition_screen.draw(screen)


class AreYouSureMenu(MainMenu):
	def __init__(self, game):
		super().__init__(game)

		self.buttons = {
				'Delete Data': [(HALF_WIDTH, HALF_HEIGHT - self.padding * 0.5), 'delete_confirmed'],
				'Back': [(HALF_WIDTH, HALF_HEIGHT + self.padding * 0.5), 'slot_menu']
				}

	def delete_data(self):
		if self.next_menu == 'delete_confirmed':
			PLAYER_DATA.update({'current_zone': 'crashsite',
				 				'entry_pos': '0', 
				 				'keys': [],
				 				'gun_index': 0, 
				 				'max_health': 4,
				 				'max_juice': 99,
				 				'heal_cost': 11,
				 				'partial_healths': 0,
				 				'time': "00:00:00"})
			COMPLETED_DATA.update({'cutscenes': [],
								  'visited_zones': [],
								  'health': [],
								  'juice': [],
								  'keys':[],
								  'bosses_defeated':[]})

			self.game.write_data(PLAYER_DATA, 'player_data')
			self.game.write_data(COMPLETED_DATA,'completed_data')

	def update(self, dt):
		self.transition_screen.update(dt)
		if self.next_menu is not None:
			self.delete_data()
			self.transitioning = True

	def draw(self, screen):
		screen.fill(BLACK)
		
		for name, values in self.buttons.items():
			self.render_button(screen, name, values[1], BLACK, LIGHT_GREEN, PINK, values[0])

		self.transition_screen.draw(screen)

class Confirmation(MainMenu):
	def __init__(self, game):
		super().__init__(game)

		self.buttons = {
				'Continue': [(HALF_WIDTH, HALF_HEIGHT + self.padding * 0.5), 'slot_menu']
				}

	def update(self, dt):
		self.transition_screen.update(dt)
		if self.next_menu is not None:
			self.transitioning = True

	def draw(self, screen):
		screen.fill(BLACK)

		# slot deleted confirmation message
		self.game.render_text(f"Slot {self.game.slot} deleted", WHITE, self.game.small_font, (HALF_WIDTH, HALF_HEIGHT - self.padding * 0.5))
		
		for name, values in self.buttons.items():
			self.render_button(screen, name, values[1], BLACK, LIGHT_GREEN, PINK, values[0])

		self.transition_screen.draw(screen)



