import pygame
from sprites import AnimatedObject
from settings import *

class Particle(pygame.sprite.Sprite):
	def __init__(self, game, zone, groups, pos, z = LAYERS['particles']):
		super().__init__(groups)

		self.zone = zone
		self.z = z
		self.image = pygame.Surface((TILESIZE, TILESIZE))
		self.rect = self.image.get_rect(topleft = pos)

class Explosion(AnimatedObject):
	def __init__(self, game, zone, groups, pos, z, path, damage, knockback_power):
		super().__init__(game, zone, groups, pos, z, path)

		self.damage = damage
		self.knockback_power = knockback_power

	def animate(self, animation_speed):

		self.frame_index += animation_speed
		self.frame_index = self.frame_index % len(self.frames)	
		self.image = self.frames[int(self.frame_index)]
		if self.frame_index > len(self.frames)-1:	
			self.kill()

	def update(self, dt):
		self.animate(0.2 * dt)

class Shadow(Particle):
	def __init__(self, game, zone, groups, pos, z, sprite, size):
		super().__init__(game, zone, groups, pos, z)

		self.zone = zone
		self.sprite = sprite
		self.size = size
		self.image = pygame.image.load(f'../assets/particles/shadow_{self.size}.png').convert_alpha()
		self.rect = self.image.get_rect(center = pos)

	def update(self, dt):
		if self.sprite in self.zone.enemy_sprites or self.sprite in self.zone.enemy_sprites or self.sprite == self.zone.player: 
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

class Flash(Particle):
	def __init__(self, game, zone, groups, pos, colour, size, z = LAYERS['foreground']):
		super().__init__(game, zone, groups, pos, z)

		self.zone = zone
		self.colour = colour
		self.size = size
		self.z = z
		self.pos = pos
		self.alpha = 255
		self.flash_size = [0, 0]
		self.image = pygame.Surface((self.flash_size))
		self.image.fill(self.colour)
		self.rect = self.image.get_rect(center = self.pos)

	def update(self, dt):
		
		self.image.fill(self.colour)
		self.alpha -= 12 * dt
		self.flash_size[0] += self.size * dt
		self.flash_size[1] += self.size * dt

		if self.alpha < 0:
			self.kill()

		self.image = pygame.transform.scale(self.image, (self.flash_size))
		self.image.set_alpha(self.alpha)
		self.rect = self.image.get_rect(center = self.pos)

		
		

			
