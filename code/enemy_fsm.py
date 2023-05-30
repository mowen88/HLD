import pygame
from settings import *

class Idle:
	def __init__(enemy, self):
		enemy.frame_index = 0

	def state_logic(self, enemy):
		if enemy.zone.get_distance_direction_and_angle(enemy.hitbox.center, enemy.zone.player.hitbox.center - enemy.zone.rendered_sprites.offset)[0] < enemy.pursue_radius:
			return Move(enemy)

	def update(self, dt, enemy):
		enemy.animate('idle', 0.2 * dt, 'loop')

class Move:
	def __init__(self, enemy):
		enemy.frame_index = 0

	def state_logic(self, enemy):
		if enemy.zone.get_distance_direction_and_angle(enemy.hitbox.center, enemy.zone.player.hitbox.center - enemy.zone.rendered_sprites.offset)[0] > enemy.pursue_radius:
			return Idle(enemy)

		if enemy.zone.get_distance_direction_and_angle(enemy.hitbox.center, enemy.zone.player.hitbox.center - enemy.zone.rendered_sprites.offset)[0] < enemy.attack_radius:
			return Telegraphing(enemy)

	def update(self, dt, enemy):
		enemy.acc = pygame.math.Vector2()
		enemy.acc += enemy.zone.get_distance_direction_and_angle(enemy.hitbox.center, enemy.zone.player.hitbox.center - enemy.zone.rendered_sprites.offset)[1] * enemy.speed

		enemy.physics(dt)
		enemy.animate('idle', 0.2 * dt, 'loop')
		enemy.direction = enemy.get_direction()

class Telegraphing:
	def __init__(self, enemy):
		enemy.frame_index = 0
		self.timer = enemy.telegraphing_time
		self.attack_direction = pygame.math.Vector2(enemy.zone.player.rect.center - enemy.zone.rendered_sprites.offset)

	def state_logic(self, enemy):
		if enemy.alive:
			if enemy.zone.get_distance_direction_and_angle(enemy.hitbox.center, enemy.zone.player.hitbox.center - enemy.zone.rendered_sprites.offset)[0] > enemy.pursue_radius:
				return Move(enemy)

			if self.timer > enemy.telegraphing_time/2:
				self.attack_direction = pygame.math.Vector2(enemy.zone.player.rect.center - enemy.zone.rendered_sprites.offset)
			elif self.timer < 0 and enemy.zone.player.dashing:
				return Idle(enemy)
			elif self.timer < 0:
				return Attack(enemy, self.attack_direction)
		else:
			return Knockback(enemy)

	def update(self, dt, enemy):
		if not enemy.invincible:
			self.timer -= dt
		enemy.animate('telegraphing', 0.4 * dt, 'loop')

class Attack:
	def __init__(self, enemy, attack_direction):
		self.timer = 40
		enemy.dashing = True
		enemy.frame_index = 0
		self.lunge_speed = enemy.lunge_speed
		self.get_current_direction = attack_direction #enemy.zone.player.rect.center - enemy.zone.rendered_sprites.offset
		enemy.vel = enemy.zone.get_distance_direction_and_angle(enemy.hitbox.center, self.get_current_direction)[1] * self.lunge_speed
		enemy.angle = enemy.zone.get_distance_direction_and_angle(enemy.hitbox.center, self.get_current_direction)[2]

	def state_logic(self, enemy):
		if enemy.alive:
			if self.timer < 0 or enemy.vel.magnitude() < 0.1:
				if enemy.get_collide_list(enemy.zone.void_sprites):
					enemy.dashing = False
					enemy.on_ground = False
					return FallDeath(enemy)
				else: 
					enemy.dashing = False
					return Idle(enemy)

			elif enemy.zone.get_distance_direction_and_angle(enemy.hitbox.center, enemy.zone.player.hitbox.center - enemy.zone.rendered_sprites.offset)[0] > enemy.pursue_radius:
				return Move(enemy)
		else:
			return Knockback(enemy)

	def update(self, dt, enemy):
		
		enemy.physics(dt)
		enemy.animate('idle', 0.2 * dt, 'end')

		self.timer -= dt

		enemy.acc = pygame.math.Vector2()
		self.lunge_speed -= 0.05 * dt
		if enemy.vel.magnitude() > 0.5: enemy.zone.enemy_attacking_logic()
		if enemy.vel.magnitude() != 0: enemy.vel = enemy.vel.normalize() * self.lunge_speed
		if enemy.vel.magnitude() < 0.1: enemy.vel = pygame.math.Vector2()

class Knockback:
	def __init__(self, enemy):
		enemy.dashing = True
		self.frame_index = 0
		self.current_direction = self.get_direction(enemy)
		self.knockback_speed = enemy.knockback_speed
		self.get_current_direction = enemy.zone.player.hitbox.center - enemy.zone.rendered_sprites.offset #enemy.zone.player.rect.center - enemy.zone.rendered_sprites.offset
		enemy.vel = enemy.zone.get_distance_direction_and_angle(enemy.hitbox.center, self.get_current_direction)[1] * self.knockback_speed *-1
		enemy.angle = enemy.zone.get_distance_direction_and_angle(enemy.hitbox.center, self.get_current_direction)[2]

	def get_direction(self, enemy):
		if enemy.hitbox.centerx < enemy.zone.player.hitbox.centerx: direction = 'left'
		else: direction = 'right'
		return direction

	def state_logic(self, enemy):

		if enemy.vel.magnitude() < 0.1:
			if enemy.get_collide_list(enemy.zone.void_sprites):
				enemy.dashing = False
				enemy.on_ground = False
				return FallDeath(enemy)
			else:
				enemy.vel = pygame.math.Vector2()

	def update(self, dt, enemy):
		
		enemy.physics(dt)
		enemy.animate('death', 0.2 * dt, 'end')
		if self.current_direction == 'left': enemy.image = pygame.transform.flip(enemy.image, True, False)
	
		enemy.acc = pygame.math.Vector2()
		self.knockback_speed -= 0.05 * dt
		if enemy.vel.magnitude() != 0: enemy.vel = enemy.vel.normalize() * self.knockback_speed
		if enemy.vel.magnitude() < 0.1: enemy.vel = pygame.math.Vector2()

class FallDeath:
	def __init__(self, enemy):
		self.frame_index = 0
		self.timer = 55

	def state_logic(self, enemy):
		if self.timer <= 0: 
			enemy.vel.y = 0
			enemy.alive = False
			enemy.kill()
			
	def update(self, dt, enemy):
		enemy.animate('telegraphing', 0.4 * dt, 'end')
		self.timer -= dt
		if self.timer > 0:
			enemy.z = LAYERS['BG2']
			enemy.vel.y += 0.15 * dt
			enemy.pos += enemy.vel
			enemy.hitbox.centery = enemy.pos.y
			enemy.rect.centery = enemy.hitbox.centery
