import pygame
from settings import *

class Idle:
	def __init__(self, player, direction):

		self.player = player

	def state_logic(self, player):
	
		if ACTIONS['down']:
			player.direction['down'] = True
			self.direction = 'down'
			return Move(player.vel, self.direction)

		elif ACTIONS['up']:
			player.direction['up'] = True
			self.direction = 'up'
			return Move(player.vel, self.direction)

		if ACTIONS['right']:
			player.direction['right'] = True
			self.direction = 'right'
			return Move(player.vel, self.direction)

		elif ACTIONS['left']:
			player.direction['left'] = True
			self.direction = 'left'
			return Move(player.vel, self.direction)

		

	def update(self, dt, player):
		player.physics(dt)

class Move:
	def __init__(self, vel, direction):
		self.direction = direction

	def state_logic(self, player):
	
		# y direction
		if ACTIONS['down']:
			player.direction['down'] = True
		else:
			player.direction['down'] = False		
		
		if ACTIONS['up']:
			player.direction['up'] = True	
		else:
			player.direction['up']= False

		# x direction
		if ACTIONS['right']:
			player.direction['right'] = True
		else:
			player.direction['right'] = False
			
		if ACTIONS['left']:
			player.direction['left'] = True
		else:
			player.direction['left'] = False


		if player.vel == pygame.math.Vector2():
			return Idle(player, self.direction)

	def update(self, dt, player):

		#player movement
		player.acc = pygame.math.Vector2()

		if player.direction['down'] and player.vel.y >= 0:
			player.acc.y += 1
		elif player.direction['up'] and player.vel.y <= 0:
			player.acc.y -= 1

		if player.direction['right'] and player.vel.x >= 0:
			player.acc.x += 1
		elif player.direction['left'] and player.vel.x <= 0:
			player.acc.x -= 1

		player.physics(dt)
