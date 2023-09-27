import math
from settings import *
from entities.NPCs import NPC

class Grunt(NPC):
	def __init__(self, game, zone, groups, pos, z, name):
		super().__init__(game, zone, groups, pos, z, name)

		self.data = ENEMY_DATA[name]

		self.speed = self.data['speed']
		self.lunge_speed = self.data['lunge_speed']
		self.health = self.data['health']
		self.damage = self.data['damage']
		self.attack_radius = self.data['attack_radius']
		self.pursue_radius = self.data['pursue_radius']
		self.telegraphing_time = self.data['telegraphing_time']

	def update(self, dt):
		self.invincibility(dt)
		if not self.zone.cutscene_running: self.state_logic()
		self.state.update(dt, self)
		if self.alive:
			if self.vel.x > 0: self.image = pygame.transform.flip(self.image, True, False)

class Hound(Grunt):
	def __init__(self, game, zone, groups, pos, z, name):
		super().__init__(game, zone, groups, pos, z, name)

		self.speed = self.data['speed']
		self.lunge_speed = self.data['lunge_speed']
		self.health = self.data['health']
		self.damage = self.data['damage']
		self.attack_radius = self.data['attack_radius']
		self.pursue_radius = self.data['pursue_radius']
		self.telegraphing_time = self.data['telegraphing_time']

		self.image = pygame.Surface((16, 16))
		self.rect = self.image.get_rect(center = pos)
		self.pos = pygame.math.Vector2(self.rect.center)
		self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.5, -self.rect.height * 0.7)

class Pincer(Hound):
	def __init__(self, game, zone, groups, pos, z, name):
		super().__init__(game, zone, groups, pos, z, name)

		# self.speed = self.data['speed']
		# self.lunge_speed = self.data['lunge_speed']
		# self.health = self.data['health']
		# self.damage = self.data['damage']
		# self.attack_radius = self.data['attack_radius']
		# self.pursue_radius = self.data['pursue_radius']
		# self.telegraphing_time = self.data['telegraphing_time']

		self.image = pygame.Surface((20, 20))
		self.rect = self.image.get_rect(center = pos)
		self.pos = pygame.math.Vector2(self.rect.center)
		self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.5, -self.rect.height * 0.7)



