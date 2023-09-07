
from settings import *

class MenuTransition(pygame.sprite.Sprite):
	def __init__(self, menu):

		self.menu = menu
		self.surf = pygame.Surface((RES))
		self.surf.fill(WHITE)
		self.alpha = 255
		self.timer = RES * 0.1 # makes load time relative to zone size
		self.fade_in_duration = 30
		self.fade_out_duration = 10

	def update(self, dt):

		if not self.menu.transitioning:
			self.alpha -= self.fade_in_duration * dt
			if self.alpha <= 0: 
				self.alpha = 0
		else:
			self.alpha += self.fade_out_duration * dt
			if self.alpha >= 255:
				self.menu.go_to(self.menu.next_menu)

	def draw(self, screen):
		self.surf.set_alpha(self.alpha)
		screen.blit(self.surf, (0,0))