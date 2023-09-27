import math, random
from settings import *
from entities.NPCs import NPC

class Musketeer(NPC):
	def __init__(self, game, zone, groups, pos, z, name):
		super().__init__(game, zone, groups, pos, z, name)

		self.state = Idle(self)
		self.data = ENEMY_DATA[name]

		self.speed = self.data['speed']
		self.lunge_speed = self.data['lunge_speed']
		self.health = self.data['health']
		self.damage = self.data['damage']
		self.attack_radius = self.data['attack_radius']
		self.pursue_radius = self.data['pursue_radius']
		self.telegraphing_time = self.data['telegraphing_time']

		self.aim_anlge = 0
		self.aiming = False
		self.zone.create_enemy_gun(self, self.aim_anlge)

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
	def __init__(self, npc):
		npc.aiming = False
		npc.frame_index = 0
		self.timer = random.randrange(60, 180)

	def state_logic(self, npc):
		if npc.alive:
			npc.explosion_damage_logic()

			if self.timer < 0:
				return Roam(npc)

			if npc.knocked_back:
				return Knockback(npc)

			if npc.zone.get_distance_direction_and_angle(npc.hitbox.center, npc.zone.player.hitbox.center - npc.zone.rendered_sprites.offset)[0] < npc.pursue_radius:
				npc.aiming = True
				return Aim(npc)
		else:
			return Knockback(npc)

	def update(self, dt, npc):
		self.timer -= dt
		npc.animate('idle', 0.2 * dt)

class Roam:
	def __init__(self, npc):
		npc.frame_index = 0
		self.timer = random.randrange(30, 120)
		self.direction = self.get_random_direction()

	def get_random_direction(self):
		return random.choice([-1, 1])

	def state_logic(self, npc):
		if npc.alive:
			npc.explosion_damage_logic()
			if self.timer < 0:
				return Idle(npc)

			if npc.zone.get_distance_direction_and_angle(npc.hitbox.center, npc.zone.player.hitbox.center - npc.zone.rendered_sprites.offset)[0] < npc.pursue_radius:
				npc.aiming = True
				return Aim(npc)

		else:
			return Knockback(npc)

	def update(self, dt, npc):

		self.timer -= dt

		npc.acc = pygame.math.Vector2()
		
		npc.acc.x += self.direction * npc.speed
		npc.acc.y += self.direction * npc.speed * 0.5

		npc.physics(dt)
		npc.animate('run', 0.2 * dt)
		npc.direction = npc.get_direction()

class Aim:
	def __init__(self, npc):
		npc.frame_index = 0
		self.timer = 30

	def state_logic(self, npc):
		if npc.alive:
			npc.explosion_damage_logic()
			if self.timer < 0:
				npc.zone.create_enemy_bullet(npc)
				return Evade(npc)

			if npc.knocked_back:
				return Knockback(npc)
		else:
			return Knockback(npc)

	def update(self, dt, npc):
		self.timer -= dt
		npc.animate('idle', 0.2 * dt)

class Evade:
	def __init__(self, npc):
		npc.frame_index = 0
		self.timer = random.randrange(30, 60)
		self.random_direction = random.randrange(3,4) # dot product left or right

	def state_logic(self, npc):
		if npc.alive:
			npc.explosion_damage_logic()

			if npc.knocked_back:
				return Knockback(npc)

			if self.timer <= 0:
				return Idle(npc)

		else:
			return Knockback(npc)

	def update(self, dt, npc):

		self.timer -= dt
		npc.acc = pygame.math.Vector2()
		
		if npc.zone.get_distance_direction_and_angle(npc.hitbox.center, npc.zone.player.hitbox.center - npc.zone.rendered_sprites.offset)[0] < npc.attack_radius:
			npc.acc += npc.zone.get_distance_direction_and_angle(npc.hitbox.center, npc.zone.player.hitbox.center - npc.zone.rendered_sprites.offset)[1] * npc.speed *-1
		else:
			npc.acc += npc.zone.get_distance_direction_and_angle(npc.hitbox.center, npc.zone.player.hitbox.center - npc.zone.rendered_sprites.offset)\
			[self.random_direction] * npc.speed

		npc.physics(dt)
		npc.animate('idle', 0.2 * dt)
		npc.direction = npc.get_direction()

class Knockback:
	def __init__(self, npc):

		npc.dashing = True
		self.frame_index = 0
		self.timer = 100
		self.current_direction = self.get_direction(npc)
		self.knockback_speed = npc.knockback_speed
		self.get_current_direction = npc.knockback_direction - npc.zone.rendered_sprites.offset #npc.zone.player.rect.center - npc.zone.rendered_sprites.offset
		npc.vel = npc.zone.get_distance_direction_and_angle(npc.hitbox.center, self.get_current_direction)[1] * self.knockback_speed *-1
		npc.angle = npc.zone.get_distance_direction_and_angle(npc.hitbox.center, self.get_current_direction)[2]

	def get_direction(self, npc):
		if npc.hitbox.centerx < npc.zone.player.hitbox.centerx: direction = 'left'
		else: direction = 'right'
		return direction

	def state_logic(self, npc):
		if self.timer <= 0 and npc.alive:
			npc.knocked_back = False
			npc.knockback_direction = (0,0)
			return Idle(npc)

		if npc.vel.magnitude() < 0.1:
			if npc.get_collide_list(npc.zone.void_sprites):
				npc.dashing = False
				npc.on_ground = False
				return FallDeath(npc)
			else:
				npc.vel = pygame.math.Vector2()

	def update(self, dt, npc):

		self.timer -= dt
		
		npc.physics(dt)
		npc.animate('death', 0.2 * dt, False)
		if self.current_direction == 'left': npc.image = pygame.transform.flip(npc.image, True, False)
	
		npc.acc = pygame.math.Vector2()
		self.knockback_speed -= 0.05 * dt
		if npc.vel.magnitude() != 0: npc.vel = npc.vel.normalize() * self.knockback_speed
		if npc.vel.magnitude() < 0.1: npc.vel = pygame.math.Vector2()

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
