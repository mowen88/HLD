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

class Sword(pygame.sprite.Sprite):
	def __init__(self, game, zone, groups, pos, z, path):
		super().__init__(groups)

		self.game = game
		self.zone = zone
		self.z = z
		self.frames = self.game.get_folder_images(path)
		self.frame_index = 0
		self.image = self.frames[self.frame_index]
		self.rect = self.image.get_rect(center = pos)


	def animate(self, animation_speed):
		self.frame_index += animation_speed
		if self.frame_index >= len(self.frames)-1: self.kill()
		else: self.frame_index = self.frame_index % len(self.frames)
		self.image = self.frames[int(self.frame_index)]

	def update(self, dt):
		self.animate(0.2 * dt)

		if 45 < self.zone.player.angle < 135:
			self.image = pygame.transform.rotate(self.image, 270)
			self.rect = self.image.get_rect(midleft = self.zone.player.hitbox.midright)
		elif 135 < self.zone.player.angle < 225:
			self.image = pygame.transform.rotate(self.image, 180)
			self.rect = self.image.get_rect(midtop = self.zone.player.hitbox.midbottom)
		elif 225 < self.zone.player.angle < 315:
			self.image = pygame.transform.rotate(self.image, 90)
			self.rect = self.image.get_rect(midright = self.zone.player.hitbox.midleft)
		else:
			self.rect = self.image.get_rect(midbottom = self.zone.player.hitbox.midtop)
			

		