import math, random
from settings import *
from entities.NPCs import NPC

class MovingBlock(NPC):
	def __init__(self, game, zone, groups, pos, z, name, idle_time=100):
		super().__init__(game, zone, groups, pos, z, name)

		self.idle_time = idle_time
		self.direction = 1
		self.damage = 1
		self.speed = 4
		self.telegraphing_time = 20

		self.state = Idle(self)

		self.image = pygame.Surface((32, 48))
		self.rect = self.image.get_rect(topleft = pos)
		self.pos = pygame.math.Vector2(self.rect.center)
		self.hitbox = self.rect.copy().inflate(0, -self.rect.height * 0.5)

	def state_logic(self):
		new_state = self.state.state_logic(self)
		if new_state: self.state = new_state
		else: self.state

	def update(self, dt):
		if not self.zone.cutscene_running: self.state_logic()
		self.state.update(dt, self)


class Idle:
	def __init__(self, npc):

		npc.frame_index = 0
		self.timer = npc.idle_time

	def state_logic(self, npc):

		if self.timer < 0:
			return Telegraph(npc)

	def update(self, dt, npc):
		self.timer -= dt

class Telegraph:
	def __init__(self, npc):

		npc.frame_index = 0
		self.timer = npc.telegraphing_time

	def state_logic(self, npc):

		if self.timer < 0:
			return Attack(npc)

	def update(self, dt, npc):
		self.timer -= dt
		# npc.animate('telegraphing', 0.3 * dt)

class Attack:
	def __init__(self, npc):
		npc.frame_index = 0
		npc.direction *= -1

	def state_logic(self, npc):
		if npc.get_collide_list(npc.zone.block_sprites):
			return Idle(npc)

	def update(self, dt, npc):
		npc.vel = npc.direction * npc.speed
