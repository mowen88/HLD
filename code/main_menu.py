
from state import State
from zone import Zone
from cutscenes.transition import MenuTransition, MenuBG
from sprites import FadeSurf
from settings import *

class Intro(State):
	def __init__(self, game):
		State.__init__(self, game)

		self.game = game
		self.timer = 60

		# logo
		self.logo_surf = pygame.image.load('../assets/pygame_logo.png').convert_alpha()
		self.logo_rect = self.logo_surf.get_rect(center = (HALF_WIDTH, HEIGHT * 0.6))

		# menu transitioning
		self.transitioning = False
		self.transition_screen = MenuTransition(self)

	def go_to(self, state):
		MainMenu(self.game).enter_state()

	def update(self, dt):
		self.transition_screen.update(dt)

		self.timer -= dt
		if self.timer <= 0:
			self.next_menu = 'main_menu'
			self.transitioning = True
			self.game.reset_keys()

	def draw(self, screen):
		screen.fill(WHITE)

		screen.blit(self.logo_surf, self.logo_rect)

		self.game.render_text('Made with', BLACK, self.game.small_font, (HALF_WIDTH, HEIGHT * 0.3))

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
		self.boxes = self.get_boxes()

	def get_boxes(self):
		boxes = []
		for x in range(int(RES.magnitude()//2)):
			boxes.append(MenuBG(self))
		return boxes

	def render_button(self, screen, current_menu, next_menu, text_colour, button_colour, hover_colour, pos):
		mx, my = pygame.mouse.get_pos()

		colour = text_colour

		surf = self.game.small_font.render(current_menu, False, colour)
		rect = pygame.Rect(0,0, HALF_WIDTH, surf.get_height() * 1.5)
		rect.center = pos

		if rect.collidepoint(mx, my) and not self.transitioning:
			pygame.draw.rect(screen, hover_colour, rect)#int(HEIGHT * 0.05))
			self.game.render_text(current_menu, text_colour, self.game.small_font, pos)
			if ACTIONS['left_click']:
				self.next_menu = next_menu
		else:
			#pygame.draw.rect(screen, button_colour, rect)#int(HEIGHT * 0.05))
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

	def draw_bounding_box(self, screen):
		box = pygame.Rect(0,0,HALF_WIDTH, HEIGHT - 20)
		box.center = RES/2
		pygame.draw.rect(screen, WHITE, (box), 2)


	def update(self, dt):

		for box in self.boxes:
			box.update(dt)

		self.transition_screen.update(dt)
		if self.next_menu is not None:
			self.transitioning = True

	def draw(self, screen):
		screen.fill(BLACK)

		for box in self.boxes:
			box.draw(screen)

		for name, values in self.buttons.items():
			self.render_button(screen, name, values[1], WHITE, LIGHT_GREEN, PINK, values[0])

		self.draw_bounding_box(screen)

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
	
		for box in self.boxes:
			box.update(dt)

		self.get_slot()

		self.transition_screen.update(dt)
		if self.next_menu is not None:
			self.transitioning = True

	def draw(self, screen):
		screen.fill(BLACK)

		for box in self.boxes:
			box.draw(screen)

		for name, values in self.buttons.items():
			self.render_button(screen, name, values[1], WHITE, LIGHT_GREEN, PINK, values[0])

		self.draw_bounding_box(screen)

		self.transition_screen.draw(screen)

class OptionsMenu(MainMenu):
	def __init__(self, game):
		super().__init__(game)

		self.buttons = {
				'SFX (not available)': [(HALF_WIDTH, HALF_HEIGHT - self.padding), 'main_menu'],
				'Music (not available)': [(HALF_WIDTH, HALF_HEIGHT), 'main_menu'],
				'Back': [(HALF_WIDTH, HALF_HEIGHT + self.padding), 'main_menu']
				}

	def update(self, dt):
		for box in self.boxes:
			box.update(dt)

		self.transition_screen.update(dt)
		if self.next_menu is not None:
			self.transitioning = True

	def draw(self, screen):
		screen.fill(BLACK)

		for box in self.boxes:
			box.draw(screen)
		
		for name, values in self.buttons.items():
			self.render_button(screen, name, values[1], WHITE, LIGHT_GREEN, PINK, values[0])

		self.draw_bounding_box(screen)

		self.transition_screen.draw(screen)

class StartGameMenu(MainMenu):
	def __init__(self, game):
		super().__init__(game)

		self.buttons = {
				'Continue': [(HALF_WIDTH, HALF_HEIGHT + self.padding * 0.5), 'GO!!!'],
				'Delete Data': [(HALF_WIDTH, HALF_HEIGHT + self.padding * 1.5), 'DELETE_SLOT'],
				'Back': [(HALF_WIDTH, HALF_HEIGHT + self.padding * 2.5), 'slot_menu']
				}

	def show_stats(self):
		if self.game.slot is not None:
			self.game.render_text(f"Slot {self.game.slot}", WHITE, self.game.small_font, (HALF_WIDTH, HALF_HEIGHT - self.padding * 3))
			self.game.render_text(PLAYER_DATA['time'], WHITE, self.game.small_font, (HALF_WIDTH, HALF_HEIGHT - self.padding * 2))
			self.game.render_text(self.game.slot_data[self.game.slot]['percent complete'], WHITE, self.game.small_font, (HALF_WIDTH, HALF_HEIGHT - self.padding))
			

	def start_timer(self):
		if self.next_menu == 'GO!!!' and self.alpha >= 255:
			self.game.timer.stop_start()

	def update(self, dt):

		for box in self.boxes:
			box.update(dt)

		self.transition_screen.update(dt)
		if self.next_menu is not None:
			self.start_timer()
			self.transitioning = True

	def draw(self, screen):
		screen.fill(BLACK)

		for box in self.boxes:
			box.draw(screen)


		for name, values in self.buttons.items():
			self.render_button(screen, name, values[1], WHITE, LIGHT_GREEN, PINK, values[0])

		self.show_stats()
		self.draw_bounding_box(screen)

		self.transition_screen.draw(screen)


class AreYouSureMenu(MainMenu):
	def __init__(self, game):
		super().__init__(game)

		self.buttons = {
				'Confirm': [(HALF_WIDTH, HALF_HEIGHT), 'delete_confirmed'],
				'Back': [(HALF_WIDTH, HALF_HEIGHT + self.padding), 'slot_menu']
				}

	def delete_data(self):
		if self.next_menu == 'delete_confirmed':
			PLAYER_DATA.update({'current_zone': 'crashsite',
								'current_gun': 'nogun',
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
								  'guns': [],
								  'health': [],
								  'juice': [],
								  'keys':[],
								  'bosses_defeated':[]})

			self.game.write_data(PLAYER_DATA, 'player_data')
			self.game.write_data(COMPLETED_DATA,'completed_data')

	def update(self, dt):

		for box in self.boxes:
			box.update(dt)

		self.transition_screen.update(dt)
		if self.next_menu is not None:
			self.delete_data()
			self.transitioning = True

	def draw(self, screen):
		screen.fill(BLACK)

		for box in self.boxes:
			box.draw(screen)
		
		for name, values in self.buttons.items():
			self.render_button(screen, name, values[1], WHITE, LIGHT_GREEN, PINK, values[0])

		self.game.render_text(f"Delete slot {self.game.slot} data?", WHITE, self.game.small_font, (HALF_WIDTH, HALF_HEIGHT - self.padding * 1.5))
		self.draw_bounding_box(screen)

		self.transition_screen.draw(screen)

class Confirmation(MainMenu):
	def __init__(self, game):
		super().__init__(game)

		self.buttons = {
				'Continue': [(HALF_WIDTH, HALF_HEIGHT + self.padding * 0.5), 'slot_menu']
				}

	def update(self, dt):

		for box in self.boxes:
			box.update(dt)

		self.transition_screen.update(dt)
		if self.next_menu is not None:
			self.transitioning = True

	def draw(self, screen):
		screen.fill(BLACK)

		for box in self.boxes:
			box.draw(screen)

		# slot deleted confirmation message
		self.game.render_text(f"Slot {self.game.slot} deleted!", WHITE, self.game.small_font, (HALF_WIDTH, HALF_HEIGHT - self.padding))
		
		for name, values in self.buttons.items():
			self.render_button(screen, name, values[1], WHITE, LIGHT_GREEN, PINK, values[0])

		self.draw_bounding_box(screen)

		self.transition_screen.draw(screen)



