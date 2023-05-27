import pygame, random
from settings import *

class Idle:
	def __init__(self):
		self.frame_index = 0

	def state_logic(self, enemy):
		if enemy.zone.get_distance_direction_and_angle(enemy.hitbox.center, enemy.zone.player.hitbox.center - enemy.zone.rendered_sprites.offset)[0] < enemy.pursue_radius:
			return Move(enemy)

	def update(self, dt, enemy):
		
		enemy.animate('idle', 0.2 * dt, 'loop')

class Move:
	def __init__(self, enemy):
		self.frame_index = 0

	def state_logic(self, enemy):
		if enemy.zone.get_distance_direction_and_angle(enemy.hitbox.center, enemy.zone.player.hitbox.center - enemy.zone.rendered_sprites.offset)[0] > enemy.pursue_radius:
			return Idle()

		if enemy.zone.get_distance_direction_and_angle(enemy.hitbox.center, enemy.zone.player.hitbox.center - enemy.zone.rendered_sprites.offset)[0] < enemy.attack_radius:
			return Telegraphing(enemy)

	def update(self, dt, enemy):
		enemy.acc = enemy.zone.get_distance_direction_and_angle(enemy.hitbox.center, enemy.zone.player.hitbox.center - enemy.zone.rendered_sprites.offset)[1] * enemy.speed
		
		# if enemy.zone.player.rect.centery > enemy.rect.centery:
		# 	enemy.acc.x += random.randint(-1, 1)

		enemy.physics(dt)
		if enemy.vel.magnitude() > 0.5:
			enemy.vel = enemy.vel.normalize() * 0.5
		enemy.animate('idle', 0.2 * dt, 'loop')


class Telegraphing:
	def __init__(self, enemy):
		self.frame_index = 0
		self.timer = enemy.telegraphing_time

	def state_logic(self, enemy):
		if enemy.zone.get_distance_direction_and_angle(enemy.hitbox.center, enemy.zone.player.hitbox.center - enemy.zone.rendered_sprites.offset)[0] > enemy.pursue_radius:
			return Move(enemy)

		if self.timer < 0:
			return Attack(enemy)

	def update(self, dt, enemy):
		self.timer -= dt
		enemy.animate('telegraphing', 0.4 * dt, 'loop')

class Attack:
	def __init__(self, enemy):
		self.timer = 50
		enemy.dashing = True
		self.frame_index = 0
		self.lunge_speed = 3
		self.get_current_direction = enemy.zone.player.rect.center - enemy.zone.rendered_sprites.offset
		enemy.vel = enemy.zone.get_distance_direction_and_angle(enemy.hitbox.center, self.get_current_direction)[1] * self.lunge_speed
		enemy.angle = enemy.zone.get_distance_direction_and_angle(enemy.hitbox.center, self.get_current_direction)[2]
		self.direction = enemy.get_direction()


	def state_logic(self, enemy):
		if enemy.zone.get_distance_direction_and_angle(enemy.hitbox.center, enemy.zone.player.hitbox.center - enemy.zone.rendered_sprites.offset)[0] > enemy.pursue_radius:
			return Move(enemy)

		if self.timer <= 0:
			if enemy.get_collide_list(enemy.zone.void_sprites):
				enemy.dashing = False
				enemy.on_ground = False
				return FallDeath(enemy)
			else: 
				enemy.dashing = False
				return Idle()

	def update(self, dt, enemy):
		
		enemy.physics(dt)
		enemy.animate('idle', 0.2 * dt, 'loop')

		self.timer -= dt

		enemy.acc = pygame.math.Vector2()
		self.lunge_speed -= 0.1 * dt
		if enemy.vel.magnitude() != 0: enemy.vel = enemy.vel.normalize() * self.lunge_speed
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
