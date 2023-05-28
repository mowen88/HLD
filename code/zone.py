import pygame, math, csv, random
from math import atan2, degrees, pi
from os import walk
from settings import *
from pytmx.util_pygame import load_pygame
from sprites import Object, Exit, Void, Gun, Sword, Tree
from camera import Camera
from state import State
from particles import Particle, Shadow
from player import Player
from enemy import Grunt, Bullet

class Zone(State):
	def __init__(self, game, zone_name, entry_point):
		State.__init__(self, game)

		
		self.game = game
		self.zone_name = zone_name
		self.entry_point = entry_point
		self.cutscene_running = False
		self.exiting = False
		self.entering = True
		self.new_zone = None

		self.fade_surf = pygame.Surface((RES))
		self.fade_surf.fill(BLACK)
		self.alpha = 255

		self.cutscene_running = False
		self.dialog_running = False
		self.npc_collided = False
		self.fade_timer = 0

		#sprites
		self.melee_sprite = pygame.sprite.GroupSingle()
		self.gun_sprite = pygame.sprite.GroupSingle()
		# sprite groups
		self.rendered_sprites = Camera(self.game, self)
		self.updated_sprites = pygame.sprite.Group()
		self.exit_sprites = pygame.sprite.Group()
		self.block_sprites = pygame.sprite.Group()
		self.void_sprites = pygame.sprite.Group()
		self.enemy_sprites = pygame.sprite.Group()
		self.gun_sprites = pygame.sprite.Group()

		self.create_map()
		self.zone_size = self.get_zone_size()


	def get_zone_size(self):
		with open(f'../zones/{self.zone_name}/{self.zone_name}_walls.csv', newline='') as csvfile:
		    reader = csv.reader(csvfile, delimiter=',')
		    for row in reader:
		        rows = (sum (1 for row in reader) + 1)
		        cols = len(row)
		return (cols * TILESIZE, rows * TILESIZE)

	def create_map(self):
		tmx_data = load_pygame(f'../zones/{self.zone_name}/{self.zone_name}.tmx')

		# add static image layers
		Object(self.game, self, [self.rendered_sprites], (0,-8), LAYERS['BG1'], pygame.image.load(f'../zones/{self.zone_name}/static_bg.png').convert_alpha())
		Object(self.game, self, [self.rendered_sprites], (0,-8), LAYERS['floor'], pygame.image.load(f'../zones/{self.zone_name}/floor.png').convert_alpha())
		Object(self.game, self, [self.rendered_sprites], (0, 0), LAYERS['floor'], pygame.image.load(f'../zones/{self.zone_name}/rocks.png').convert_alpha())

		# # add the player
		for obj in tmx_data.get_layer_by_name('entries'):
			if obj.name == self.entry_point: self.player = Player(self.game, self, [self.updated_sprites, self.rendered_sprites], (obj.x, obj.y), LAYERS['player'])
			

		for obj in tmx_data.get_layer_by_name('exits'):
			if obj.name == '1': Exit([self.exit_sprites, self.updated_sprites], (obj.x, obj.y ), obj.name)
			if obj.name == '2': Exit([self.exit_sprites, self.updated_sprites], (obj.x, obj.y), obj.name)

		for obj in tmx_data.get_layer_by_name('entities'):
			if obj.name == 'grunt': self.grunt = Grunt(self.game, self, [self.enemy_sprites, self.updated_sprites, self.rendered_sprites], (obj.x, obj.y), LAYERS['player'], obj.name)

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

	def exit_zone(self):
		for sprite in self.exit_sprites:
			if sprite.rect.colliderect(self.player.hitbox):
				self.cutscene_running = True
				self.new_zone = ZONE_DATA[self.zone_name][sprite.name]
				self.entry_point = sprite.name
				self.exiting = True

	def fade_update(self, dt):
		if self.exiting:
			self.alpha += 4 * dt
			if self.alpha >= 255: 
				self.alpha = 255
				self.exit_state()
				Zone(self.game, self.new_zone, self.entry_point).enter_state()
			
		elif self.entering:
			self.alpha -= 4 * dt
			if self.alpha <= 0:
				self.alpha = 0
				self.entering = False

	def fade_draw(self, screen):
		self.fade_surf.set_alpha(self.alpha)
		screen.blit(self.fade_surf, (0,0))

	def update(self, dt):
		self.exit_zone()
		self.fade_update(dt)
		
		if ACTIONS['return']: 
			self.exit_state()
			self.game.reset_keys()
		self.updated_sprites.update(dt)

	def draw(self, screen):
		screen.fill(GREEN)
		self.rendered_sprites.offset_draw(self.player)
		self.fade_draw(screen)
		self.game.render_text(str(round(self.game.clock.get_fps(), 2)), WHITE, self.game.small_font, (WIDTH * 0.5, HEIGHT * 0.1))
		self.game.render_text(self.zone_name, PINK, self.game.small_font, RES/2)
		self.game.render_text(self.player.state, WHITE, self.game.small_font, (WIDTH * 0.5, HEIGHT * 0.9))
		
