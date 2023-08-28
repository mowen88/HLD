
from state import State
from settings import *
from particles import Flash
from cutscenes.dialogue import Dialogue
from cutscenes.sequences import Sequences

class CollectionCutscene(State):
	def __init__(self, game, zone, number):
		State.__init__(self, game)

		self.zone = zone
		self.number = number
		self.target = pygame.math.Vector2(self.zone.target.rect.center)

		self.opening = True
		self.bar_height = 0
		self.target_height = HEIGHT * 0.1
		self.blackbar = pygame.Surface((WIDTH, self.bar_height))

		self.alpha = 0
		self.max_alpha = 255
		self.fadeout = False

		self.frames = self.game.get_folder_images(self.number)
		self.frame_index = 0
		self.image = self.frames[self.frame_index]
		self.rect = self.image.get_rect(center = RES/2)

	def blackbar_logic(self, dt):
		if not self.opening:
		    self.bar_height -= (self.target_height - self.bar_height) * 0.1 * dt

		    if self.bar_height <= 0:
		        self.bar_height = 0
		        self.opening = True
		        self.zone.cutscene_running = False
		        self.exit_state()

		elif self.bar_height < self.target_height - 1:  
		    self.bar_height += (self.target_height - self.bar_height) * 0.1 * dt

	def draw_blackbars(self, screen):
		pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, self.bar_height))
		pygame.draw.rect(screen, BLACK, (0, HEIGHT - self.bar_height, WIDTH, self.target_height))

	def animate(self, animation_speed):
		self.frame_index += animation_speed
		
		if self.frame_index >= len(self.frames) -1: 
			self.frame_index = len(self.frames) -1
			self.opening = False
		else:
			self.frame_index = self.frame_index % len(self.frames)	

		self.image = self.frames[int(self.frame_index)]

	def fade(self, dt):
		if self.opening:
			self.alpha += 10 * dt
			if self.alpha >= self.max_alpha:
				self.alpha = self.max_alpha
		else:
			self.alpha -= 10 * dt
			if self.alpha <= 0:
				self.alpha = 0
					
	def update(self, dt):
		self.game.reset_keys()
		self.fade(dt)
		self.animate(0.2 * dt)
		self.prev_state.update(dt)
		self.blackbar_logic(dt)

	def draw(self, screen):
		self.prev_state.rendered_sprites.offset_draw(screen, self.target)
		self.draw_blackbars(screen)

		screen.blit(self.image, self.rect)
		self.image.set_alpha(self.alpha)

class Cutscene(State):
	def __init__(self, game, zone, number):
		State.__init__(self, game)

		self.zone = zone
		self.number = number
		self.opening = True

		self.bar_height = 0
		self.target_height = HEIGHT * 0.1
		self.blackbar = pygame.Surface((WIDTH, self.bar_height))

		self.target = pygame.math.Vector2(self.zone.target.rect.center)
		self.new_pos = pygame.math.Vector2()

		self.timer = 0
		self.int_time = 0
		self.cutscene_sequence = Sequences(self)

	def create_dialogue(self, target_sprite, dialogue_index, duration):
		Dialogue(self.game, self.zone, self.number, target_sprite, dialogue_index, duration).enter_state()

	def move_camera(self, dt):
		self.target.x += (self.new_pos.x - self.target.x)
		self.target.y += (self.new_pos.y - self.target.y)
		
	def blackbar_logic(self, dt):
		if not self.opening:
		    self.bar_height -= (self.target_height - self.bar_height) * 0.1 * dt

		    if self.bar_height <= 0:
		        self.bar_height = 0
		        self.opening = True
		        self.zone.cutscene_running = False
		        self.exit_state()

		elif self.bar_height < self.target_height - 1:  
		    self.bar_height += (self.target_height - self.bar_height) * 0.1 * dt

	def draw_blackbars(self, screen):
		pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, self.bar_height))
		pygame.draw.rect(screen, BLACK, (0, HEIGHT - self.bar_height, WIDTH, self.target_height))

	def sequence(self, number):
		self.cutscene_sequence.run(number)

	def update(self, dt):
		self.game.reset_keys()
		self.timer += dt
		self.int_time = int(self.timer)
		self.prev_state.update(dt)

		self.move_camera(dt)
		self.blackbar_logic(dt)

	def draw(self, screen):
		self.sequence(self.number)
		self.prev_state.rendered_sprites.offset_draw(screen, self.target)
		self.draw_blackbars(screen)

		self.game.render_text(str(round(self.game.clock.get_fps(), 2)), WHITE, self.game.small_font, RES/2)


