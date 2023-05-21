import pygame
from settings import *

class Object(pygame.sprite.Sprite):
	def __init__(self, game, zone, groups, pos, z, surf = pygame.Surface((TILESIZE, TILESIZE))):
		super().__init__(groups)

		self.zone = zone
		self.z = z
		self.image = surf
		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.copy().inflate(0, 0)

class Void(Object):
	def __init__(self, game, zone, groups, pos, z, surf = pygame.Surface((TILESIZE, TILESIZE))):
		super().__init__(game, zone, groups, pos, z, surf)

		self.hitbox = self.rect.copy().inflate(-self.rect.width *0.1, -self.rect.height *0.4)

class Tree(Object):
	def __init__(self, game, zone, groups, pos, z, surf):
		super().__init__(game, zone, groups, pos, z, surf)
		
		self.hitbox = self.rect.copy().inflate(-self.rect.width *0.05, -self.rect.height *0.3)