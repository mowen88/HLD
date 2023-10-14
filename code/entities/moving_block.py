import math, random
from settings import *
from entities.NPCs import NPC

class MovingBlock(NPC):
	def __init__(self, game, zone, groups, pos, z, name, wait_time=60, speed=(0,0)):
		super().__init__(game, zone, groups, pos, z, name)

		self.wait_time = wait_time
		self.direction = -1
		self.speed = pygame.math.Vector2(speed)
		self.health = 2
		self.telegraphing_time = 30
		self.attacking = False

		self.state = Idle(self)

		self.image = pygame.Surface((32, 48))
		self.rect = self.image.get_rect(topleft = pos)
		self.pos = pygame.math.Vector2(self.rect.center)
		self.hitbox = self.rect.copy().inflate(0, -self.rect.height * 0.3)

	def push_entity(self):

		if self.zone.player.hitbox.colliderect(self.hitbox):
			
			if self.attacking:
				self.zone.player.reduce_health(self.game.current_health)

			if self.zone.player.hitbox.right > self.hitbox.left:
				self.zone.player.hitbox.right = self.hitbox.left
				
			elif self.zone.player.hitbox.left < self.hitbox.right:
				self.zone.player.hitbox.left = self.hitbox.right
			
			if self.zone.player.hitbox.top < self.hitbox.bottom:
				self.zone.player.hitbox.top = self.hitbox.bottom

			elif self.zone.player.hitbox.bottom > self.hitbox.top:
				self.zone.player.hitbox.bottom = self.hitbox.top

	def state_logic(self):
		new_state = self.state.state_logic(self)
		if new_state: self.state = new_state
		else: self.state

	def update(self, dt):
		self.push_entity()
		if not self.zone.cutscene_running: self.state_logic()
		self.state.update(dt, self)


class Idle:
	def __init__(self, npc):
		npc.zone.block_sprites.add(npc)
		npc.frame_index = 0
		npc.attacking = False
		self.timer = npc.wait_time

	def state_logic(self, npc):
		if self.timer < 0:
			return Telegraphing(npc)

	def update(self, dt, npc):
		self.timer -= dt
		npc.animate('idle', 0.2 * dt)


class Attack:
	def __init__(self, npc):
		npc.zone.block_sprites.remove(npc)
		npc.frame_index = 0
		npc.attacking = True
		self.timer = 20

	def state_logic(self, npc):
		if self.timer < 0:
			npc.vel = pygame.math.Vector2()
			npc.direction *= -1
			return Idle(npc)

	def update(self, dt, npc):

		self.timer -= dt
		npc.physics(dt)
		npc.animate('attack', 0.2 * dt, False)

		npc.acc = pygame.math.Vector2()
		npc.vel = npc.speed * npc.direction


class Telegraphing:
	def __init__(self, npc):
		npc.frame_index = 0
		self.timer = npc.telegraphing_time
		
	def state_logic(self, npc):
		if self.timer < 0:
			if npc.speed.magnitude() == 0:
				return Idle(npc)
			else:
				return Attack(npc)


	def update(self, dt, npc):
		self.timer -= dt
	
		npc.animate('telegraphing', 0.15 * dt, False)