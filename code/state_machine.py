import pygame
from settings import *

class Idle:
	def __init__(self, direction):

		self.direction = direction

	def state_logic(self, player):

		for k, v in player.direction.items():
			if ACTIONS[k]: 
				v = True
				return Move(self.direction)

	def update(self, dt, player):
		player.physics(dt)

class Move:
	def __init__(self, direction):
		self.direction = direction

	def state_logic(self, player):
	
		for k, v in player.direction.items():
			if ACTIONS[k]: player.direction[k] = True
			else: player.direction[k] = False		
	
		if player.vel == pygame.math.Vector2():
			return Idle(self.direction)

	def update(self, dt, player):

		player.acc = pygame.math.Vector2()

		# y direction increment acceleration
		if player.direction['down'] and player.vel.y >= 0: player.acc.y += 0.5
		elif player.direction['up'] and player.vel.y <= 0: player.acc.y -= 0.5
		# x direction increment acceleration
		if player.direction['right'] and player.vel.x >= 0: player.acc.x += 0.5
		elif player.direction['left'] and player.vel.x <= 0: player.acc.x -= 0.5

		player.physics(dt)
