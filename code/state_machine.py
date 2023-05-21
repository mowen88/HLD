import pygame
from settings import *

class Idle:
	def __init__(self, direction):
		self.frame_index = 0
		self.direction = direction

	def state_logic(self, player):

		if ACTIONS['right_click']:
			return Dash(player, self.direction)

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
		if player.direction['down']: player.acc.y += 0.25
		elif player.direction['up']: player.acc.y -= 0.25
		# x direction increment acceleration
		if player.direction['right']: player.acc.x += 0.25
		elif player.direction['left']: player.acc.x -= 0.25

		player.physics(dt)
		player.animate(self.direction, 0.2 * dt, 'loop')

class Dash:
	def __init__(self, player, direction):
		
		ACTIONS['right_click'] = False

		self.frame_index = 0
		self.lunge_speed = 4
		self.get_current_direction = pygame.mouse.get_pos()
		player.vel = player.zone.get_distance_direction_and_angle(player.hitbox.center, self.get_current_direction)[1] * self.lunge_speed
		player.angle = player.zone.get_distance_direction_and_angle(player.hitbox.center, self.get_current_direction)[2]
		self.direction = player.get_direction()

	def state_logic(self, player):
		if player.vel.magnitude() < 0.05:
			return Idle(self.direction)

	def update(self, dt, player):
		player.acc = pygame.math.Vector2()

		self.lunge_speed -= 0.2 * dt
		#self.lunge_speed *= 0.99

		player.vel = player.vel.normalize() * self.lunge_speed

		player.physics(dt)
		player.animate(self.direction + '_dash', 0.2 * dt, 'end')

