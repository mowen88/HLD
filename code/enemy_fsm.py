import pygame
from settings import *

class Idle:
	def __init__(self):
		self.frame_index = 0

	def state_logic(self, enemy):
		if enemy.zone.get_distance_direction_and_angle(enemy.hitbox.center, enemy.zone.player.hitbox.center - enemy.zone.rendered_sprites.offset)[0] < 80:
			return Move(enemy)

	def update(self, dt, enemy):
		
		enemy.animate('idle', 0.2 * dt, 'loop')

class Move:
	def __init__(self, enemy):
		self.frame_index = 0

	def state_logic(self, enemy):
		if enemy.zone.get_distance_direction_and_angle(enemy.hitbox.center, enemy.zone.player.hitbox.center - enemy.zone.rendered_sprites.offset)[0] > 80:
			return Idle()

	def update(self, dt, enemy):
		enemy.acc = enemy.zone.get_distance_direction_and_angle(enemy.hitbox.center, enemy.zone.player.hitbox.center - enemy.zone.rendered_sprites.offset)[1] * 0.2
		enemy.physics(dt)
		if enemy.vel.magnitude() > 0.5:
			enemy.vel = enemy.vel.normalize() * 0.5
		enemy.animate('idle', 0.2 * dt, 'loop')
