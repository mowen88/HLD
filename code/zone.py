import pygame, math, csv, random
from math import atan2, degrees, pi
from os import walk
from settings import *
from pytmx.util_pygame import load_pygame
from sprites import Object, Void, Gun, Sword, Tree
from camera import Camera
from state import State
from particles import Particle, Shadow
from player import Player
from enemy import Grunt, Bullet

class Zone(State):
	def __init__(self, game):
		State.__init__(self, game)

		self.game = game
		self.cutscene_running = False

		#sprites
		self.melee_sprite = pygame.sprite.GroupSingle()
		self.gun_sprite = pygame.sprite.GroupSingle()
		# sprite groups
		self.rendered_sprites = Camera(self.game, self)
		self.updated_sprites = pygame.sprite.Group()
		self.block_sprites = pygame.sprite.Group()
		self.void_sprites = pygame.sprite.Group()
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
		Object(self.game, self, [self.rendered_sprites], (0,-8), LAYERS['BG1'], pygame.image.load(f'../assets/zones/{self.game.current_zone}/static_bg.png').convert_alpha())
		Object(self.game, self, [self.rendered_sprites], (0,-8), LAYERS['floor'], pygame.image.load(f'../assets/zones/{self.game.current_zone}/floor.png').convert_alpha())
		Object(self.game, self, [self.rendered_sprites], (0,0), LAYERS['floor'], pygame.image.load(f'../assets/zones/{self.game.current_zone}/rocks.png').convert_alpha())

		# # add the player
		for obj in tmx_data.get_layer_by_name('entities'):
			if obj.name == '0': self.player = Player(self.game, self, [self.updated_sprites, self.rendered_sprites], (obj.x, obj.y), LAYERS['player'])
			if obj.name == 'grunt': self.grunt = Grunt(self.game, self, [self.enemy_sprites, self.updated_sprites, self.rendered_sprites], (obj.x, obj.y), LAYERS['player'], obj.name)
			self.target = self.player

		for obj in tmx_data.get_layer_by_name('objects'):
			if obj.name == 'big tree': Tree(self.game, self, [self.block_sprites, self.updated_sprites, self.rendered_sprites], (obj.x, obj.y), LAYERS['player'], obj.image)
			if obj.name == 'medium tree': Tree(self.game, self, [self.block_sprites, self.updated_sprites, self.rendered_sprites], (obj.x, obj.y), LAYERS['player'], obj.image)
			if obj.name == 'tall tree': Tree(self.game, self, [self.block_sprites, self.updated_sprites, self.rendered_sprites], (obj.x, obj.y), LAYERS['player'], obj.image)
			if obj.name == 'red flower': Tree(self.game, self, [self.block_sprites, self.updated_sprites, self.rendered_sprites], (obj.x, obj.y), LAYERS['player'], obj.image)
			if obj.name == 'blue flower': Tree(self.game, self, [self.block_sprites, self.updated_sprites, self.rendered_sprites], (obj.x, obj.y), LAYERS['player'], obj.image)
		
		for x, y, surf in tmx_data.get_layer_by_name('walls').tiles():
			Object(self.game, self, [self.block_sprites, self.updated_sprites], (x * TILESIZE, y * TILESIZE), LAYERS['player'], surf)

		for x, y, surf in tmx_data.get_layer_by_name('void').tiles():
			Void(self.game, self, [self.void_sprites, self.updated_sprites], (x * TILESIZE, y * TILESIZE), LAYERS['player'], surf)
		# self.create_guns()

		# create shadows for player and NPCs
		Shadow(self.game, self, [self.updated_sprites, self.rendered_sprites], (self.player.hitbox.midbottom), LAYERS['particles'], self.player)
		for sprite in self.enemy_sprites:
			Shadow(self.game, self, [self.updated_sprites, self.rendered_sprites], (sprite.hitbox.midbottom), LAYERS['particles'], sprite)

	def create_melee(self):
		self.melee_sprite = Sword(self.game, self, [self.updated_sprites, self.rendered_sprites], self.player.hitbox.center, LAYERS['player'], '../assets/weapons/sword_1/')
	
	def create_gun(self):
		self.gun_sprite = Gun(self.game, self, [self.updated_sprites, self.rendered_sprites], self.player.hitbox.center, LAYERS['player'], pygame.image.load('../assets/weapons/gun.png').convert_alpha())

	def get_distance_direction_and_angle(self, point_1, point_2):
		pos_1 = pygame.math.Vector2(point_1 - self.rendered_sprites.offset)
		pos_2 = pygame.math.Vector2(point_2)
		distance = (pos_2 - pos_1).magnitude()
		if (pos_2 - pos_1).magnitude() != 0: direction = (pos_2 - pos_1).normalize()
		else: direction = pygame.math.Vector2(0.1,0.1)
		radians = atan2(-(point_1[0] - (pos_2.x + self.rendered_sprites.offset.x)), (point_1[1] - (pos_2.y + self.rendered_sprites.offset.y)))
		radians %= 2*pi
		angle = int(degrees(radians))

		return(distance, direction, angle)

	def update(self, dt):
		
		if ACTIONS['return']: 
			self.exit_state()
			self.game.reset_keys()
		self.updated_sprites.update(dt)

	def draw(self, screen):
		screen.fill(GREEN)
		self.rendered_sprites.offset_draw(self.target)
		self.game.render_text(str(round(self.game.clock.get_fps(), 2)), WHITE, self.game.small_font, (WIDTH * 0.5, HEIGHT * 0.1))
		self.game.render_text(self.grunt.alive, PINK, self.game.small_font, RES/2)
		self.game.render_text(self.player.state, WHITE, self.game.small_font, (WIDTH * 0.5, HEIGHT * 0.9))
