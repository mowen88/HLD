import pygame
from settings import *

class FadeSurf(pygame.sprite.Sprite):
	def __init__(self, zone, groups, pos, alpha = 255, z = LAYERS['foreground']):
		super().__init__(groups)

		self.zone = zone
		self.image = pygame.Surface((self.zone.zone_size))
		self.alpha = alpha
		self.z = z
		self.rect = self.image.get_rect(topleft = pos)

	def update(self, dt):
		if self.zone.cutscene_running:
			self.alpha += 4 * dt
			if self.alpha >= 255: 
				self.alpha = 255
				self.zone.exit_state()
				self.zone.create_zone(self.zone.new_zone)
			
		elif self.zone.entering:
			self.alpha -= 4 * dt
			if self.alpha <= 0:
				self.alpha = 0
				self.zone.entering = False

	def draw(self, screen):
		self.image.set_alpha(self.alpha)
		screen.blit(self.image, (0,0))

class Exit(pygame.sprite.Sprite):
	def __init__(self, groups, pos, name, surf = pygame.Surface((TILESIZE, TILESIZE))):
		super().__init__(groups)

		self.name = name
		self.image = surf
		self.rect = self.image.get_rect(topleft = pos)


class Object(pygame.sprite.Sprite):
	def __init__(self, game, zone, groups, pos, z, surf = pygame.Surface((TILESIZE, TILESIZE))):
		super().__init__(groups)

		self.zone = zone
		self.z = z
		self.image = surf
		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.copy().inflate(-self.rect.width *0.1, -self.rect.height *0.4)

class Void(Object):
	def __init__(self, game, zone, groups, pos, z, surf = pygame.Surface((TILESIZE, TILESIZE))):
		super().__init__(game, zone, groups, pos, z, surf)

		self.hitbox = self.rect.copy().inflate(-self.rect.width *0.4, 0)

class Tree(Object):
	def __init__(self, game, zone, groups, pos, z, surf):
		super().__init__(game, zone, groups, pos, z, surf)
		
		self.hitbox = self.rect.copy().inflate(-self.rect.width *0.05, -self.rect.height *0.3)

class Gun(Object):
	def __init__(self, game, zone, groups, pos, z, surf):
		super().__init__(game, zone, groups, pos, z, surf)

		self.zone = zone
		self.z = z
		self.original_image = surf
		self.image = self.original_image
		self.flipped_image = pygame.transform.flip(self.original_image, True, False)
		self.rect = self.image.get_rect(center = pos)
		self.angle = self.zone.get_distance_direction_and_angle(self.zone.player.hitbox.center, pygame.mouse.get_pos())[2]

	def rotate(self):
		self.angle = self.angle % 45
		self.angle = self.zone.get_distance_direction_and_angle(self.zone.player.hitbox.center, pygame.mouse.get_pos())[2]
		if self.angle >= 180: self.image = pygame.transform.rotate(self.flipped_image, -self.angle)
		else: self.image = pygame.transform.rotate(self.original_image, -self.angle)

	def update(self, dt):
		self.rotate()
		if 90 < self.angle < 270: self.rect = self.image.get_rect(center = (self.zone.player.rect.centerx, self.zone.player.rect.centery + 1))
		else: self.rect = self.image.get_rect(center = (self.zone.player.rect.centerx, self.zone.player.rect.centery - 1))

class Sword(pygame.sprite.Sprite):
	def __init__(self, game, zone, groups, pos, z, path):
		super().__init__(groups)

		self.game = game
		self.zone = zone
		self.z = z
		self.frames = self.game.get_folder_images(path)
		self.opposite_frames = self.game.get_folder_images(path +'_2')
		self.frame_index = 0
		self.image = self.frames[self.frame_index]
		self.rect = self.image.get_rect(center = pos)

	def animate(self, animation_speed):
		self.frame_index += animation_speed
		if self.frame_index >= len(self.frames)-1: self.kill()
		
		if self.zone.player.attack_count % 2 == 0: self.image = self.opposite_frames[int(self.frame_index)]
		else: self.image = self.frames[int(self.frame_index)]

	def update(self, dt):
		self.animate(0.25 * dt)

		if 45 < self.zone.player.angle < 135:
			self.image = pygame.transform.rotate(self.image, 270)
			self.rect = self.image.get_rect(midleft = self.zone.player.hitbox.center)
		elif 135 < self.zone.player.angle < 225:
			self.image = pygame.transform.rotate(self.image, 180)
			self.rect = self.image.get_rect(midtop = self.zone.player.hitbox.center)
		elif 225 < self.zone.player.angle < 315:
			self.image = pygame.transform.rotate(self.image, 90)
			self.rect = self.image.get_rect(midright = self.zone.player.hitbox.center)
		else:
			self.rect = self.image.get_rect(midbottom = self.zone.player.hitbox.center)


			

		