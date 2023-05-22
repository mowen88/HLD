import pygame
from settings import *

class Idle:
	def __init__(self, direction):
		self.frame_index = 0
		self.direction = direction

	def state_logic(self, player):

		if ACTIONS['right_click']:
			return Dash(player, self.direction)

		if ACTIONS['left_click']:
			return Attack(player, self.direction)

		for k, v in player.direction.items():
			if ACTIONS[k]: 
				v = True
				return Move(self.direction)

	def update(self, dt, player):
		player.vel = pygame.math.Vector2()
		player.physics(dt)
		player.animate(self.direction + '_idle', 0.2 * dt, 'loop')

class Move:
	def __init__(self, direction):
		self.frame_index = 0
		self.direction = direction

	def state_logic(self, player):

		if ACTIONS['right_click']:
			return Dash(player, self.direction)

		if ACTIONS['left_click']:
			return Attack(player, self.direction)
	
		for k, v in player.direction.items():
			if ACTIONS[k]: 
				self.direction = k
				player.direction[k] = True
			else: 
				player.direction[k] = False
				
		if player.vel.magnitude() < 0.05:
			return Idle(self.direction)

	def update(self, dt, player):

		player.acc = pygame.math.Vector2()

		# y direction increment acceleration
		if player.direction['down']: player.acc.y += 0.2
		elif player.direction['up']: player.acc.y -= 0.2
		# x direction increment acceleration
		if player.direction['right']: player.acc.x += 0.2
		elif player.direction['left']: player.acc.x -= 0.2

		player.physics(dt)
		player.animate(self.direction, 0.2 * dt, 'loop')

class Dash:
	def __init__(self, player, direction):
		
		self.timer = 30
		player.dashing = True
		player.respawn_location = player.rect.center

		ACTIONS['right_click'] = False

		self.frame_index = 0
		self.lunge_speed = 5
		self.get_current_direction = pygame.mouse.get_pos()
		player.vel = player.zone.get_distance_direction_and_angle(player.hitbox.center, self.get_current_direction)[1] * self.lunge_speed
		player.angle = player.zone.get_distance_direction_and_angle(player.hitbox.center, self.get_current_direction)[2]
		self.direction = player.get_direction()

	def state_logic(self, player):

		if self.timer < 0:
			if player.get_collide_list(player.zone.void_sprites):
				player.dashing = False
				player.alive = False
				return FallDeath(self.direction)
			else: 
				player.dashing = False
				return Idle(self.direction)

	def update(self, dt, player):
		self.timer -= dt

		player.acc = pygame.math.Vector2()
		self.lunge_speed -= 0.3 * dt
		if player.vel.magnitude() != 0: player.vel = player.vel.normalize() * self.lunge_speed
		if player.vel.magnitude() < 0.1: player.vel = pygame.math.Vector2()

		player.physics(dt)
		player.animate(self.direction + '_dash', 0.2 * dt, 'end')

class Attack:
	def __init__(self, player, direction):

		ACTIONS['left_click'] = False

		self.timer = 25
		self.frame_index = 0
		self.lunge_speed = 1
		self.get_current_direction = pygame.mouse.get_pos()
		player.vel = player.zone.get_distance_direction_and_angle(player.hitbox.center, self.get_current_direction)[1] * self.lunge_speed
		player.angle = player.zone.get_distance_direction_and_angle(player.hitbox.center, self.get_current_direction)[2]
		self.direction = player.get_direction()

		player.zone.create_melee(self.direction)

	def state_logic(self, player):

		if ACTIONS['right_click']:
			player.zone.melee_sprite.kill()
			return Dash(player, self.direction)


		if self.timer < 0:
		# if player.vel.magnitude() < 0.05:
			return Idle(self.direction)

	def update(self, dt, player):
		self.timer -= dt

		player.acc = pygame.math.Vector2()
		self.lunge_speed -= 0.1 * dt
		if player.vel.magnitude() != 0: player.vel = player.vel.normalize() * self.lunge_speed
		if player.vel.magnitude() < 0.1: player.vel = pygame.math.Vector2()

		player.physics(dt)
		player.animate(self.direction + '_dash', 0.25 * dt, 'end')

class FallDeath:
	def __init__(self, direction):
		self.frame_index = 0
		self.direction = direction
		self.timer = 70

	def state_logic(self, player):
		if self.timer <= 0: 
			player.game.screenshaking = False
			player.z = LAYERS['player']
			player.alive = True
			player.pos.x = player.respawn_location[0]
			player.pos.y = player.respawn_location[1]
			return Idle(self.direction)

	def update(self, dt, player):
		self.timer -= dt
		if self.timer > 0:
			if self.timer > 28 and self.timer < 30: player.game.screenshaking = True
			player.z = LAYERS['BG2']
			player.vel.y += 0.15 * dt
			player.pos += player.vel
			player.hitbox.centery = player.pos.y
			player.rect.centery = player.hitbox.centery

		player.animate(self.direction + '_fall', 0.2 * dt, 'end')

