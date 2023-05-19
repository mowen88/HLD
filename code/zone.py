import pygame, math
# from math import atan2, degrees, pi
from os import walk
from settings import *
from pytmx.util_pygame import load_pygame
from camera import Camera
from state import State
from player import Player

class Zone(State):
	def __init__(self, game):
		State.__init__(self, game)

		self.game = game
		self.cutscene_running = False

		# sprite groups
		self.rendered_sprites = Camera(self.game, self)
		self.updated_sprites = pygame.sprite.Group()
		self.block_sprites = pygame.sprite.Group()
		self.enemy_sprites = pygame.sprite.Group()
		self.gun_sprites = pygame.sprite.Group()

		#self.create_map()

		self.player = Player(self.game, self, [self.updated_sprites, self.rendered_sprites], (100, 100), LAYERS['player'])
		self.target = self.player

	def create_map(self):
		pass
		# tmx_data = load_pygame(f'../zones/{self.game.current_zone}.tmx')

		# # # add backgrounds
		# # Object(self.game, self, [self.rendered_sprites, Z_LAYERS[1]], (0,0), pygame.image.load('../assets/bg.png').convert_alpha())
		# # Object(self.game, self, [self.rendered_sprites, Z_LAYERS[2]], (0,TILESIZE), pygame.image.load('../zones/0.png').convert_alpha())

		# # add the player
		# for obj in tmx_data.get_layer_by_name('entities'):
		# 	if obj.name == 'player': self.player = Player(self.game, self, obj.name, [self.updated_sprites, self.rendered_sprites], (obj.x, obj.y), LAYERS['player'])
		# 	if obj.name == 'guard': Enemy(self.game, self, obj.name, [self.enemy_sprites, self.updated_sprites, self.rendered_sprites], (obj.x, obj.y), LAYERS['NPCs'])
		# 	if obj.name == 'sg_guard': Enemy(self.game, self, obj.name, [self.enemy_sprites, self.updated_sprites, self.rendered_sprites], (obj.x, obj.y), LAYERS['NPCs'])
		# 	self.target = self.player
			
		# self.create_guns()

		# for x, y, surf in tmx_data.get_layer_by_name('blocks').tiles():
		# 	Tile(self.game, self, [self.block_sprites, self.updated_sprites, self.rendered_sprites], (x * TILESIZE, y * TILESIZE), surf)
			

	def get_distance(self, point_1, point_2):
		distance = (pygame.math.Vector2(point_2) - pygame.math.Vector2(point_1))
		return distance

	def update(self, dt):
		
		if ACTIONS['return']: 
			self.exit_state()
			self.game.reset_keys()
		self.updated_sprites.update(dt)

	def draw(self, screen):
		screen.fill(GREEN)
		self.rendered_sprites.draw(screen)
		#self.rendered_sprites.offset_draw(self.target)
		self.game.render_text(self.player.acc, WHITE, self.game.small_font, RES/2)

