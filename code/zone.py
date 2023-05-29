import pygame, math, csv, random
from math import atan2, degrees, pi
from os import walk
from settings import *
from pytmx.util_pygame import load_pygame
from sprites import FadeSurf, Exit, Object, Void, Gun, Sword, Bullet, Tree
from camera import Camera
from state import State
from particles import Particle, Shadow
from player import Player
from NPCs import Warrior
from enemy import Grunt, Hound

class Zone(State):
	def __init__(self, game, name, entry_point):
		State.__init__(self, game)

		
		self.game = game
		self.name = name
		self.entry_point = entry_point
		self.cutscene_running = False
		self.entering = True
		self.new_zone = None

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

		self.zone_size = self.get_zone_size()
		self.create_map()

		self.fade_surf = FadeSurf(self, [self.updated_sprites, self.rendered_sprites], (0,0))

	def get_zone_size(self):
		with open(f'../zones/{self.name}/{self.name}_walls.csv', newline='') as csvfile:
		    reader = csv.reader(csvfile, delimiter=',')
		    for row in reader:
		        rows = (sum (1 for row in reader) + 1)
		        cols = len(row)
		return (cols * TILESIZE, rows * TILESIZE)

	def create_map(self):
		tmx_data = load_pygame(f'../zones/{self.name}/{self.name}.tmx')
	
		# # add the player
		for obj in tmx_data.get_layer_by_name('entries'):
			if obj.name == self.entry_point:

				if obj.x > self.zone_size[0] - (self.zone_size[0]/5): self.start_direction = 'left'
				elif obj.x < self.zone_size[0]/5: self.start_direction = 'right'
				elif obj.y < self.zone_size[1]/2: self.start_direction = 'down'

				else: self.start_direction = 'up'

				self.player = Player(self.game, self, [self.updated_sprites, self.rendered_sprites], (obj.x, obj.y), LAYERS['player'])
				

		for obj in tmx_data.get_layer_by_name('exits'):
			if obj.name == '1': Exit([self.exit_sprites, self.updated_sprites], (obj.x, obj.y ), obj.name)
			if obj.name == '2': Exit([self.exit_sprites, self.updated_sprites], (obj.x, obj.y), obj.name)

		for obj in tmx_data.get_layer_by_name('entities'):
			#enemies
			if obj.name == 'grunt': self.grunt = Grunt(self.game, self, [self.enemy_sprites, self.updated_sprites, self.rendered_sprites], (obj.x, obj.y), LAYERS['player'], obj.name)
			if obj.name == 'hound': self.hound = Hound(self.game, self, [self.enemy_sprites, self.updated_sprites, self.rendered_sprites], (obj.x, obj.y), LAYERS['player'], obj.name)
			#NPCs
			if obj.name == 'warrior': self.warrior = Warrior(self.game, self, [self.updated_sprites, self.rendered_sprites], (obj.x, obj.y), LAYERS['player'], obj.name)

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

		# add static image layers
		Object(self.game, self, [self.rendered_sprites], (0,-8), LAYERS['BG1'], pygame.image.load(f'../zones/{self.name}/static_bg.png').convert_alpha())
		Object(self.game, self, [self.rendered_sprites], (0,-8), LAYERS['floor'], pygame.image.load(f'../zones/{self.name}/floor.png').convert_alpha())
		Object(self.game, self, [self.rendered_sprites], (0, 0), LAYERS['floor'], pygame.image.load(f'../zones/{self.name}/rocks.png').convert_alpha())
	
	def create_zone(self, zone):
		Zone(self.game, zone, self.entry_point).enter_state()

	def create_melee(self):
		self.melee_sprite = Sword(self.game, self, [self.updated_sprites, self.rendered_sprites], self.player.hitbox.center, LAYERS['player'], '../assets/weapons/sword')
	
	def create_gun(self):
		self.gun_sprite = Gun(self.game, self, [self.updated_sprites, self.rendered_sprites], self.player.hitbox.center, LAYERS['player'], pygame.image.load('../assets/weapons/gun.png').convert_alpha())

	def create_bullet(self):
		self.bulllet = Bullet(self.game, self, [self.updated_sprites, self.rendered_sprites], self.player.hitbox.center, LAYERS['particles'], '../assets/weapons/bullet')

	# def enemy_enemy_collisions(self):
	# 	enemies = []
	# 	for sprite in self.enemy_sprites:
	# 		enemies.append(sprite)
	# 	for i, enemy1 in enumerate(enemies):
	# 	    for enemy2 in enemies[i+1:]:
	# 	        if enemy1.hitbox.colliderect(enemy2.hitbox) and not enemy1.dashing and enemy2.alive:
	# 	        		if enemy1.vel.x != 0: enemy1.vel.x = 0
	# 	        		if enemy1.vel.y != 0:enemy1.vel.y = 0

	def player_attacking_logic(self):
		if self.melee_sprite:
			for target in self.enemy_sprites:
				if self.melee_sprite.rect.colliderect(target.hitbox) and self.melee_sprite.frame_index < 1:
					if not target.invincible and target.alive:
						target.invincible = True
						target.health -= 1
						if target.health <= 0:
							target.invincible = False
							target.alive = False
							

	def enemy_attacking_logic(self):
		for sprite in self.enemy_sprites:
			if not self.player.invincible and not sprite.invincible and self.player.alive and sprite.dashing:
				if sprite.hitbox.colliderect(self.player.hitbox):
					self.reduce_health(sprite.damage)
					self.game.screenshaking = True
					self.player.invincible = True
					if self.melee_sprite: self.melee_sprite.kill()
						
	def reduce_health(self, amount):
		if not self.player.invincible:
			self.game.current_health -= amount
			if self.game.current_health <= 0:
				self.player.alive = False
				self.game.current_health = PLAYER_DATA['max_health']
				self.exit_state()
				self.create_zone(self.name)

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

	def exiting(self):
		for sprite in self.exit_sprites:
			if sprite.rect.colliderect(self.player.hitbox):
				self.cutscene_running = True
				self.new_zone = ZONE_DATA[self.name][sprite.name]
				self.entry_point = sprite.name

	def update(self, dt):
		self.exiting()
		# self.enemy_enemy_collisions()
		self.fade_surf.update(dt)

		if ACTIONS['return']: 
			self.exit_state()
			self.game.reset_keys()
		self.updated_sprites.update(dt)

	def draw(self, screen):
		screen.fill(GREEN)
		self.rendered_sprites.offset_draw(self.player)
		self.fade_surf.draw(screen)
		# self.game.render_text(str(round(self.game.clock.get_fps(), 2)), WHITE, self.game.small_font, (WIDTH * 0.5, HEIGHT * 0.1))
		# self.game.render_text(self.grunt.state, PINK, self.game.small_font, RES/2)
		# self.game.render_text(self.player.invincible, WHITE, self.game.small_font, (WIDTH * 0.5, HEIGHT * 0.9))
		
