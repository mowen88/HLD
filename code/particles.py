import pygame
from settings import *

class Particle(pygame.sprite.Sprite):
	def __init__(self, game, zone, groups, pos, z = LAYERS['particles']):
		super().__init__(groups)

		self.zone = zone
		self.z = z
		self.image = pygame.Surface((TILESIZE, TILESIZE))
		self.rect = self.image.get_rect(topleft = pos)

class Shadow(Particle):
	def __init__(self, game, zone, groups, pos, z, sprite, size):
		super().__init__(game, zone, groups, pos, z)

		self.zone = zone
		self.sprite = sprite
		self.size = size
		self.image = pygame.image.load(f'../assets/particles/shadow_{self.size}.png').convert_alpha()
		self.rect = self.image.get_rect(center = pos)

	def update(self, dt):
		if self.sprite in self.zone.enemy_sprites or self.sprite == self.zone.player: 
			if self.sprite.get_collide_list(self.zone.void_sprites) or not self.sprite.on_ground:
				self.image.set_alpha(0)
			else:
				self.image.set_alpha(80)
				self.rect = self.image.get_rect(center = (self.sprite.hitbox.midbottom[0], self.sprite.hitbox.midbottom[1] + self.rect.height))
		elif self.sprite.alive:
			self.image.set_alpha(80)
			self.rect = self.image.get_rect(center = (self.sprite.hitbox.midbottom[0], self.sprite.hitbox.midbottom[1] + self.rect.height))
		else:
			self.image.set_alpha(0)
			
