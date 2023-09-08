import random
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

class MenuBG(pygame.sprite.Sprite):
	def __init__(self, menu):

		self.menu = menu
		self.image = pygame.Surface((random.random()*TILESIZE, random.random()*TILESIZE))
		self.image.fill(PURPLE)
		self.rect = self.image.get_rect()
		self.alpha = 255

		self.speed = (random.uniform(0.1, 1.0), random.uniform(0.1, 1.0))
		self.vel = pygame.math.Vector2(self.speed)
		self.pos = pygame.math.Vector2(self.rect.topleft)
		self.pos = (random.random() * WIDTH, random.random() * HEIGHT)

	def update(self, dt):
		self.alpha = random.randrange(0, 255)
		self.pos += self.vel * dt
		self.rect.topleft = self.pos

		if self.rect.x > WIDTH:
			self.pos.x = -self.rect.width
		if self.rect.y > HEIGHT:
			self.pos.y = -self.rect.height

	def draw(self, screen):
		self.image.set_alpha(self.alpha)
		screen.blit(self.image, self.rect)

