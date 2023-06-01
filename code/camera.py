import pygame, math, random
from settings import *

class Camera(pygame.sprite.Group):
	def __init__(self, game, zone):
		super().__init__()

		self.game = game
		self.zone = zone
		self.offset = pygame.math.Vector2()

		self.BG0 = pygame.image.load(f'../zones/{self.zone.name}/bg.png').convert_alpha()

	def screenshake(self):
		if self.zone.screenshaking:
			self.zone.screenshake_timer += 1
			if self.zone.screenshake_timer < 120: 
				self.offset += [random.randint(-1, 1), random.randint(-1, 1)]
			else: 
				self.zone.screenshaking = False
				self.zone.screenshake_timer = 0

	def midpoint(self, p1, p2):
		return ((p1.x + p2.x)/4, (p1.x + p2.y)/4)

	def offset_draw(self, target):
		
		# draw parralax backgrounds
		self.game.screen.fill(LIGHT_GREY)
		self.game.screen.blit(self.BG0, (0 - self.offset[0] * 0.2, 0 - self.offset[1] * 0.2))

		distance = self.zone.get_distance_direction_and_angle(pygame.mouse.get_pos() - self.offset, target.rect.center)[0]
		scroll = pygame.math.Vector2(target.rect.center) + pygame.math.Vector2(pygame.mouse.get_pos())
		midpoint = self.midpoint(pygame.math.Vector2(target.rect.center - self.offset), pygame.math.Vector2(pygame.mouse.get_pos()))

		self.offset += (target.rect.center - RES/2 - self.offset)
		self.offset += (midpoint - RES - self.offset)/(distance/5)

		#self.offset += self.self.zone.get_distance_direction_and_angle(pygame.math.Vector2(target.rect.center), pygame.math.Vector2(pygame.mouse.get_pos()))[1]
	
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

		pygame.draw.circle(self.game.screen, GREEN, midpoint, 4)