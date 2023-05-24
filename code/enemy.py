import math
from settings import *
from NPCs import NPC
from enemy_fsm import Idle

class Grunt(NPC):
	def __init__(self, game, zone, groups, pos, z, name):
		super().__init__(game, zone, groups, pos, z, name)


class Bullet(pygame.sprite.Sprite):
	def __init__(self, game, zone, groups, pos, z, angle):
		super().__init__(groups)

		self.image = pygame.Surface((4,4))
		self.rect = self.image.get_rect(center = pos)
		self.z = z
		self.angle = angle
		#self.vel = pygame.math.Vector2(1, 0).rotate(self.angle) * 2
		self.pos = pygame.math.Vector2((self.rect.centerx, self.rect.centery - 20)).rotate(self.angle)

	def update(self, dt):
		# self.pos += self.vel
		self.rect.center = self.pos