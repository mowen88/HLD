import pygame
from settings import *

class Idle:
	def __init__(self):
		self.frame_index = 0

	def state_logic(self, enemy):
		pass

	def update(self, dt, enemy):
		enemy.animate('idle', 0.2 * dt, 'loop')