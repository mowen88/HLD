import pygame, random
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
	def __init__(self, groups, pos, size, name):
		super().__init__(groups)

		self.name = name
		self.size = size
		self.image = pygame.Surface((self.size))
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

class AnimatedObject(pygame.sprite.Sprite):
	def __init__(self, game, zone, groups, pos, z, path):
		super().__init__(groups)

		self.game = game
		self.zone = zone
		self.z = z
		self.frames = self.game.get_folder_images(path)
		self.frame_index = 0
		self.image = self.frames[self.frame_index]
		self.rect = self.image.get_rect(center = pos)

		self.hitbox = self.rect.copy().inflate(0,0)
		self.alive = True

	def animate(self, animation_speed):
		self.frame_index += animation_speed
		self.frame_index = self.frame_index % len(self.frames)	
		self.image = self.frames[int(self.frame_index)]

	def update(self, dt):
		self.animate(0.2 * dt)

class Door(AnimatedObject):
	def __init__(self, game, zone, groups, pos, z, path, name):
		super().__init__(game, zone, groups, pos, z, path)

		self.name = name

	def open(self, dt):
		if self.rect.colliderect(self.zone.player.rect):
			for i in PLAYER_DATA['keys']:
				if i == self.name:
					self.zone.block_sprites.remove(self)
					self.frame_index += 0.2 * dt
					if self.frame_index >= len(self.frames) -1: self.frame_index = len(self.frames) -1
					else: self.frame_index = self.frame_index % len(self.frames)	
		else:
			self.frame_index -= 0.2 * dt
			if self.frame_index <= 0: self.frame_index = 0
			else: self.frame_index = self.frame_index % len(self.frames)

		self.image = self.frames[int(self.frame_index)]
		if self.frame_index == len(self.frames) -1: self.zone.block_sprites.remove(self)
		else: self.zone.block_sprites.add(self)	


	def update(self, dt):
		self.open(dt)



class Collectible(AnimatedObject):
	def __init__(self, game, zone, groups, pos, z, path, name):
		super().__init__(game, zone, groups, pos, z, path)

		self.name = name
		self.original_image = self.frames[self.frame_index]
		self.image = self.original_image
		self.pos = pos
		self.rotate = 0

	def animate(self, animation_speed):
		self.frame_index += animation_speed
		self.frame_index = self.frame_index % len(self.frames)
		self.original_image = self.frames[int(self.frame_index)]

	def rotation(self, dt):
		self.rotate += 3 * dt
		self.rotate = self.rotate % 360

		self.image = pygame.transform.rotate(self.original_image, self.rotate)
		self.rect = self.image.get_rect(center = self.rect.center)

		self.hitbox.center = self.rect.center

	def update(self, dt):
		self.rotation(dt)
		self.animate(0.2 * dt)		

class Sword(AnimatedObject):
	def __init__(self, game, zone, groups, pos, z, path):
		super().__init__(game, zone, groups, pos, z, path)

		self.opposite_frames = self.game.get_folder_images(path +'_2')

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

class Bullet(AnimatedObject):
	def __init__(self, game, zone, groups, pos, z, path):
		super().__init__(game, zone, groups, pos, z, path)

		self.speed = 5
		self.vel = self.zone.get_distance_direction_and_angle(self.rect.center, pygame.mouse.get_pos())[1] * self.speed
		self.vel = self.vel.rotate(random.randrange(-10, 10))
		self.pos = pygame.math.Vector2(self.rect.center)
		self.damage = 1

	def update(self, dt):
		self.animate(0.25 * dt)
		self.pos += self.vel * dt
		self.rect.center = self.pos

class AttackableTerrain(AnimatedObject):
	def __init__(self, game, zone, groups, pos, z, path):
		super().__init__(game, zone, groups, pos, z, path)

		self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.5, -self.rect.height * 0.7)
		self.alive = True

	def animate(self, animation_speed):
		if self.alive:
			self.frame_index = 0
		else:
			self.frame_index += animation_speed
			if self.frame_index >= len(self.frames)-1: self.frame_index = len(self.frames)-1
			else: self.frame_index = self.frame_index % len(self.frames)
			self.zone.attackable_sprites.remove(self)
			self.zone.block_sprites.remove(self)

		self.image = self.frames[int(self.frame_index)]

class Beam(AnimatedObject):
	def __init__(self, game, zone, groups, pos, z, path, fade_speed):
		super().__init__(game, zone, groups, pos, z, path)

		self.alpha = 255
		self.fade_speed = fade_speed
		self.damage = 3

	def animate(self, animation_speed):
		self.frame_index += animation_speed
		self.frame_index = self.frame_index % len(self.frames)
		self.image = self.frames[int(self.frame_index)]

	def update(self, dt):
		self.animate(0.2 * dt)
		self.alpha -= self.fade_speed * dt
		if self.alpha <= 0:
			self.kill()
		self.image.set_alpha(self.alpha)


			

			

		