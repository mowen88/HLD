import math, random
from settings import *
from entities.NPCs import NPC

class Boss1(NPC):
	def __init__(self, game, zone, groups, pos, z, name):
		super().__init__(game, zone, groups, pos, z, name)

		self.state = Idle(self)
		self.data = ENEMY_DATA[name]

		self.speed = self.data['speed']
		self.lunge_speed = self.data['lunge_speed']
		self.health = self.data['health']
		self.max_health = self.health
		self.damage = self.data['damage']
		self.attack_radius = self.data['attack_radius']
		self.pursue_radius = self.data['pursue_radius']
		self.telegraphing_time = self.data['telegraphing_time']

		self.image = pygame.Surface((40, 40))
		self.rect = self.image.get_rect(center = pos)
		self.pos = pygame.math.Vector2(self.rect.center)
		self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.5, -self.rect.height * 0.7)

	def state_logic(self):
		new_state = self.state.state_logic(self)
		if new_state: self.state = new_state
		else: self.state

	def update(self, dt):
		self.invincibility(dt)
		if not self.zone.cutscene_running: self.state_logic()
		self.state.update(dt, self)
		if self.alive:
			if self.vel.x > 0: self.image = pygame.transform.flip(self.image, True, False)

class Idle:
	def __init__(npc, self):
		npc.frame_index = 0

	def state_logic(self, npc):
		if npc.alive:

			npc.explosion_damage_logic()

			if npc.zone.get_distance_direction_and_angle(npc.hitbox.center, npc.zone.player.hitbox.center - npc.zone.rendered_sprites.offset)[0] < npc.pursue_radius:
				return Move(npc)
		else:
			return Death(npc)

	def update(self, dt, npc):
		npc.animate('idle', 0.2 * dt)

class Move:
	def __init__(self, npc):
		npc.frame_index = 0

	def state_logic(self, npc):
		if npc.alive:

			npc.explosion_damage_logic()

			if npc.zone.get_distance_direction_and_angle(npc.hitbox.center, npc.zone.player.hitbox.center - npc.zone.rendered_sprites.offset)[0] > npc.pursue_radius:
				return Idle(npc)

			if npc.zone.get_distance_direction_and_angle(npc.hitbox.center, npc.zone.player.hitbox.center - npc.zone.rendered_sprites.offset)[0] < npc.attack_radius:
				return Telegraphing(npc)
		else:
			return Death(npc)

	def update(self, dt, npc):
		npc.acc = pygame.math.Vector2()
		
		npc.acc += npc.zone.get_distance_direction_and_angle(npc.hitbox.center, npc.zone.player.hitbox.center - npc.zone.rendered_sprites.offset)[1] * npc.speed

		npc.physics(dt)
		npc.animate('idle', 0.2 * dt)
		npc.direction = npc.get_direction()

class Telegraphing:
	def __init__(self, npc):
		npc.frame_index = 0
		self.timer = npc.telegraphing_time
		self.attack_direction = pygame.math.Vector2(npc.zone.player.rect.center - npc.zone.rendered_sprites.offset)

	def state_logic(self, npc):
		if npc.alive:

			npc.explosion_damage_logic()

			if npc.zone.get_distance_direction_and_angle(npc.hitbox.center, npc.zone.player.hitbox.center - npc.zone.rendered_sprites.offset)[0] > npc.pursue_radius:
				return Move(npc)

			if self.timer > npc.telegraphing_time/2:
				self.attack_direction = pygame.math.Vector2(npc.zone.player.rect.center - npc.zone.rendered_sprites.offset)

			elif self.timer < 0:
				return Jump(npc, self.attack_direction)
		else:
			return Death(npc)

	def update(self, dt, npc):
		if not npc.invincible:
			self.timer -= dt
		npc.animate('telegraphing', 0.15 * dt, False)

class Jump:
	def __init__(self, npc, attack_direction):

		self.timer = 40
		npc.dashing = True
		npc.frame_index = 0
		self.lunge_speed = npc.lunge_speed
		self.get_current_direction = attack_direction #npc.zone.player.rect.center - npc.zone.rendered_sprites.offset
		npc.vel = npc.zone.get_distance_direction_and_angle(npc.hitbox.center, self.get_current_direction)[1] * self.lunge_speed
		npc.angle = npc.zone.get_distance_direction_and_angle(npc.hitbox.center, self.get_current_direction)[2]

	def state_logic(self, npc):
		if npc.alive:
			if self.timer < 0 or npc.vel.magnitude() < 0.1:
				if npc.get_collide_list(npc.zone.void_sprites):
					npc.dashing = False
					npc.on_ground = False
					return FallDeath(npc)
				else: 
					npc.dashing = False
					return Idle(npc)

			elif npc.zone.get_distance_direction_and_angle(npc.hitbox.center, npc.zone.player.hitbox.center - npc.zone.rendered_sprites.offset)[0] > npc.pursue_radius:
				return Move(npc)
		else:
			return Death(npc)

	def update(self, dt, npc):
		
		npc.physics(dt)
		npc.animate('jumping', 0.2 * dt, False)

		self.timer -= dt

		npc.acc = pygame.math.Vector2()
		self.lunge_speed -= 0.05 * dt
		if npc.vel.magnitude() < 0.1: 
			npc.vel = pygame.math.Vector2()
		else:
			npc.vel = npc.vel.normalize() * self.lunge_speed
			npc.zone.player.enemy_attacking_logic()

class Landing:
	def __init__(self, npc):

		self.timer = 40

	def state_logic(self, npc):
		if npc.alive:

			if self.timer < 0:
				return Idle(npc)
		else:
			return Death(npc)

	def update(self, dt, npc):

		self.timer -= dt

		if self.timer > 10:
			npc.zone.player.enemy_attacking_logic()
		
		npc.physics(dt)
		npc.animate('landing', 0.2 * dt, False)
		npc.acc = pygame.math.Vector2()
	

class Death:
	def __init__(self, npc):
		npc.frame_index = 0
		self.current_direction = self.get_direction(npc)

	def get_direction(self, npc):
		if npc.hitbox.centerx < npc.zone.player.hitbox.centerx: direction = 'left'
		else: direction = 'right'
		return direction

	def state_logic(self, npc):
		pass

	def update(self, dt, npc):
		if self.current_direction == 'left': 
			npc.image = pygame.transform.flip(npc.image, True, False)

		npc.vel = pygame.math.Vector2()
		npc.animate('death', 0.15 * dt, False)

class FallDeath:
	def __init__(self, npc):
		self.frame_index = 0
		self.timer = 55

	def state_logic(self, npc):
		if self.timer <= 0: 
			npc.vel.y = 0
			npc.alive = False
			npc.kill()
			
	def update(self, dt, npc):
		npc.animate('telegraphing', 0.4 * dt, False)
		self.timer -= dt
		if self.timer > 0:
			npc.z = LAYERS['BG2']
			npc.vel.y += 0.15 * dt
			npc.pos += npc.vel
			npc.hitbox.centery = npc.pos.y
			npc.rect.centery = npc.hitbox.centery