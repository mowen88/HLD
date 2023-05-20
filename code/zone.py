import pygame, math, csv
# from math import atan2, degrees, pi
from os import walk
from settings import *
from pytmx.util_pygame import load_pygame
from sprites import Object, Tree
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

		self.create_map()
		self.zone_size = self.get_zone_size()

	def get_zone_size(self):
		with open(f'../assets/zones/{self.game.current_zone}/{self.game.current_zone}.csv', newline='') as csvfile:
		    reader = csv.reader(csvfile, delimiter=',')
		    for row in reader:
		        rows = (sum (1 for row in reader) + 1)
		        cols = len(row)
		return (cols * TILESIZE, rows * TILESIZE)

	def create_map(self):
		tmx_data = load_pygame(f'../assets/zones/{self.game.current_zone}/{self.game.current_zone}.tmx')

		# add static image layers
		Object(self.game, self, [self.rendered_sprites], (0,0), LAYERS['BG1'], pygame.image.load(f'../assets/zones/{self.game.current_zone}/static_bg.png').convert_alpha())
		Object(self.game, self, [self.rendered_sprites], (0,0), LAYERS['floor'], pygame.image.load(f'../assets/zones/{self.game.current_zone}/floor.png').convert_alpha())

		# # add the player
		for obj in tmx_data.get_layer_by_name('entities'):
			if obj.name == '0': self.player = Player(self.game, self, [self.updated_sprites, self.rendered_sprites], (obj.x, obj.y), LAYERS['player'])
			self.target = self.player

		# add objects
		for obj in tmx_data.get_layer_by_name('objects'):
			if obj.name == 'big tree': Tree(self.game, self, [self.rendered_sprites], (obj.x, obj.y), LAYERS['player'], obj.image)
			if obj.name == 'medium tree': Tree(self.game, self, [self.rendered_sprites], (obj.x, obj.y), LAYERS['player'], obj.image)
			if obj.name == 'tall tree': Tree(self.game, self, [self.rendered_sprites], (obj.x, obj.y), LAYERS['player'], obj.image)
			if obj.name == 'red flower': Tree(self.game, self, [self.rendered_sprites], (obj.x, obj.y), LAYERS['player'], obj.image)
			if obj.name == 'blue flower': Tree(self.game, self, [self.rendered_sprites], (obj.x, obj.y), LAYERS['player'], obj.image)
			
		# self.create_guns()

		# for x, y, surf in tmx_data.get_layer_by_name('blocks').tiles():
		# 	Tile(self.game, self, [self.block_sprites, self.updated_sprites, self.rendered_sprites], (x * TILESIZE, y * TILESIZE), surf)
			

	def get_distance(self, point_1, point_2):
		distance = (pygame.math.Vector2(point_2) - pygame.math.Vector2(point_1))
		return distance

	def update(self, dt):
		if ACTIONS['space']: 
			self.game.screenshaking = True
		
		if ACTIONS['return']: 
			self.exit_state()
			self.game.reset_keys()
		self.updated_sprites.update(dt)

	def draw(self, screen):

		screen.fill(GREEN)
		self.rendered_sprites.offset_draw(self.target)

		self.game.render_text(str(round(self.game.clock.get_fps(), 2)), WHITE, self.game.small_font, (WIDTH * 0.5, HEIGHT * 0.1))
		self.game.render_text(self.player.state, WHITE, self.game.small_font, RES/2)

		print(self.game.screenshaking)
