import math
from settings import *
from NPCs import NPC
from enemy_fsm import Idle

class Grunt(NPC):
	def __init__(self, game, zone, groups, pos, z, name):
		super().__init__(game, zone, groups, pos, z, name)

		self.pursue_radius = 90
		self.attack_radius = 30
		self.telegraphing_time = 40

		self.data = ENEMY_DATA[name]

		self.speed = self.data['speed']
		self.health = self.data['health']
		self.damage = self.data['damage']
		self.attack_radius = self.data['attack_radius']
		self.pursue_radius = self.data['pursue_radius']
		self.telegraphing_time = self.data['telegraphing_time']

	def update(self, dt):
		if not self.zone.cutscene_running: self.state_logic()
		self.state.update(dt, self)
		if self.vel.x > 0: self.image = pygame.transform.flip(self.image, True, False)

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