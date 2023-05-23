import pygame, math, random
from settings import *

class Camera(pygame.sprite.Group):
	def __init__(self, game, zone):
		super().__init__()

		self.game = game
		self.zone = zone
		self.offset = pygame.math.Vector2()
		self.screenshake_timer = 0

		self.BG0 = pygame.image.load(f'../assets/zones/{self.game.current_zone}/bg.png').convert_alpha()

	def screenshake(self):
		if self.game.screenshaking:
			self.screenshake_timer += 1
			if self.screenshake_timer < 120: 
				self.offset += [random.randint(-1, 1), random.randint(-1, 1)]
			else: 
				self.game.screenshaking = False
				self.screenshake_timer = 0

	def offset_draw(self, target):
		
		# draw parralax backgrounds
		self.game.screen.fill(LIGHT_GREY)
		self.game.screen.blit(self.BG0, (0 - self.offset[0] * 0.2, 0 - self.offset[1] * 0.2))


		self.offset += (target.rect.center - self.offset - RES/2)

		# limit offset to stop at edges
		if self.offset[0] <= 0: self.offset[0] = 0
		elif self.offset[0] >= self.zone.zone_size[0] - WIDTH: self.offset[0] = self.zone.zone_size[0] - WIDTH
		if self.offset[1] <= 0: self.offset[1] = 0
		elif self.offset[1] >= self.zone.zone_size[1] - HEIGHT: self.offset[1] = self.zone.zone_size[1] - HEIGHT

		self.screenshake()

		

		for layer in LAYERS.values():
			for sprite in sorted(self.zone.rendered_sprites, key = lambda sprite: sprite.rect.centery):
				if sprite.z == layer:
					offset = sprite.rect.topleft - self.offset
					self.game.screen.blit(sprite.image, offset)