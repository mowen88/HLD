import pygame, random
from settings import *

class Idle:
	def __init__(npc, self):
		npc.frame_index = 0

	def state_logic(self, npc):
		if npc.alive:
			if npc.zone.get_distance_direction_and_angle(npc.hitbox.center, npc.zone.player.hitbox.center - npc.zone.rendered_sprites.offset)[0] < npc.pursue_radius:
				return Move(npc)
		else:
			return Knockback(npc)

	def update(self, dt, npc):
		npc.animate('idle', 0.2 * dt)

class Move:
	def __init__(self, npc):
		npc.frame_index = 0

	def state_logic(self, npc):
		if npc.alive:

			if npc.zone.melee_sprite or npc.zone.gun_sprite:
				return Evade(npc)

			if npc.zone.get_distance_direction_and_angle(npc.hitbox.center, npc.zone.player.hitbox.center - npc.zone.rendered_sprites.offset)[0] > npc.pursue_radius:
				return Idle(npc)

			if npc.zone.get_distance_direction_and_angle(npc.hitbox.center, npc.zone.player.hitbox.center - npc.zone.rendered_sprites.offset)[0] < npc.attack_radius:
				return Telegraphing(npc)
		else:
			return Knockback(npc)

	def update(self, dt, npc):
		npc.acc = pygame.math.Vector2()
		
		npc.acc += npc.zone.get_distance_direction_and_angle(npc.hitbox.center, npc.zone.player.hitbox.center - npc.zone.rendered_sprites.offset)[1] * npc.speed

		npc.physics(dt)
		npc.animate('idle', 0.2 * dt)
		npc.direction = npc.get_direction()

class Evade:
	def __init__(self, npc):
		npc.frame_index = 0
		self.timer = random.randrange(30, 60)
		self.random_direction = random.randrange(3,4)

	def state_logic(self, npc):
		if npc.alive:

			if self.timer <= 0:
				return Move(npc)

			if npc.zone.get_distance_direction_and_angle(npc.hitbox.center, npc.zone.player.hitbox.center - npc.zone.rendered_sprites.offset)[0] > npc.pursue_radius:
				return Idle(npc)

			if npc.zone.get_distance_direction_and_angle(npc.hitbox.center, npc.zone.player.hitbox.center - npc.zone.rendered_sprites.offset)[0] < npc.attack_radius:
				return Telegraphing(npc)
		else:
			return Knockback(npc)

	def update(self, dt, npc):

		self.timer -= dt
		npc.acc = pygame.math.Vector2()
		
		npc.acc += npc.zone.get_distance_direction_and_angle(npc.hitbox.center, npc.zone.player.hitbox.center - npc.zone.rendered_sprites.offset)\
		[self.random_direction] * npc.speed

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
			if npc.zone.get_distance_direction_and_angle(npc.hitbox.center, npc.zone.player.hitbox.center - npc.zone.rendered_sprites.offset)[0] > npc.pursue_radius:
				return Move(npc)

			if self.timer > npc.telegraphing_time/2:
				self.attack_direction = pygame.math.Vector2(npc.zone.player.rect.center - npc.zone.rendered_sprites.offset)
			elif self.timer < 0 and npc.zone.player.dashing:
				return Idle(npc)
			elif self.timer < 0:
				return Attack(npc, self.attack_direction)
		else:
			return Knockback(npc)

	def update(self, dt, npc):
		if not npc.invincible:
			self.timer -= dt
		npc.animate('telegraphing', 0.4 * dt)

class Attack:
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
			return Knockback(npc)

	def update(self, dt, npc):
		
		npc.physics(dt)
		npc.animate('idle', 0.2 * dt, False)

		self.timer -= dt

		npc.acc = pygame.math.Vector2()
		self.lunge_speed -= 0.05 * dt
		if npc.vel.magnitude() > 0.5: npc.zone.player.enemy_attacking_logic()
		if npc.vel.magnitude() != 0: npc.vel = npc.vel.normalize() * self.lunge_speed
		if npc.vel.magnitude() < 0.1: npc.vel = pygame.math.Vector2()

class Jump:
	def __init__(self, npc, attack_direction):

		self.gravity = 0.2
		npc.vel.y = 5

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
			return Knockback(npc)

	def update(self, dt, npc):
		
		npc.physics(dt)
		npc.animate('idle', 0.2 * dt, False)

		self.timer -= dt

		npc.zone.player.enemy_attacking_logic()

		npc.acc = pygame.math.Vector2()
		self.lunge_speed -= 0.05 * dt
		npc.vel.y += self.gravity
		if npc.vel.magnitude() != 0: npc.vel = npc.vel.normalize() * self.lunge_speed
		if npc.vel.magnitude() < 0.1: npc.vel = pygame.math.Vector2()

class Knockback:
	def __init__(self, npc):
		npc.dashing = True
		self.frame_index = 0
		self.current_direction = self.get_direction(npc)
		self.knockback_speed = npc.knockback_speed
		self.get_current_direction = npc.zone.player.hitbox.center - npc.zone.rendered_sprites.offset #npc.zone.player.rect.center - npc.zone.rendered_sprites.offset
		npc.vel = npc.zone.get_distance_direction_and_angle(npc.hitbox.center, self.get_current_direction)[1] * self.knockback_speed *-1
		npc.angle = npc.zone.get_distance_direction_and_angle(npc.hitbox.center, self.get_current_direction)[2]

	def get_direction(self, npc):
		if npc.hitbox.centerx < npc.zone.player.hitbox.centerx: direction = 'left'
		else: direction = 'right'
		return direction

	def state_logic(self, npc):

		if npc.vel.magnitude() < 0.1:
			if npc.get_collide_list(npc.zone.void_sprites):
				npc.dashing = False
				npc.on_ground = False
				return FallDeath(npc)
			else:
				npc.vel = pygame.math.Vector2()

	def update(self, dt, npc):
		
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
