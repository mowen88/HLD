import pygame, math, random
from settings import *

class Camera(pygame.sprite.Group):
	def __init__(self, game, zone):
		super().__init__()

		self.game = game
		self.zone = zone
		self.offset = pygame.math.Vector2()
		self.screenshake_timer = 0

	def screenshake(self):
		if self.game.screenshaking:
			self.screenshake_timer += 1
			if self.screenshake_timer < 120: self.offset += [random.randint(-1, 1), random.randint(-1, 1)]
			else: self.game.screenshaking = False

	def offset_draw(self, target):
		
		self.game.screen.fill(LIGHT_GREY)

		self.offset += (target.pos - self.offset - RES/2)

		#self.screenshake()

		for layer in LAYERS.values():
			for sprite in sorted(self.zone.rendered_sprites, key = lambda sprite: sprite.rect.centery):
				if sprite.z == layer:
					offset = sprite.rect.topleft - self.offset
					self.game.screen.blit(sprite.image, offset)