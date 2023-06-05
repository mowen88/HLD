import pygame, math, csv, random
from math import atan2, degrees, pi
from os import walk
from settings import *
from pytmx.util_pygame import load_pygame
from state import State
from cutscenes import CollectionCutscene
from ui import UI
from map import Map
from sprites import FadeSurf, Exit, Object, Void, Collectible, Gun, Sword, Bullet, Tree, Beam, AttackableTerrain
from camera import Camera
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
		
		PLAYER_DATA.update({'current_zone': self.name, 'entry_pos': self.entry_point})
		COMPLETED_DATA['visited_zones'].append(self.name)

		self.screenshaking = False
		self.screenshake_timer = 0
		self.cutscene_running = False
		self.entering = True
		self.new_zone = None

		#sprites
		self.melee_sprite = pygame.sprite.GroupSingle()
		self.gun_sprite = pygame.sprite.GroupSingle()
		self.player_bullet_sprites = pygame.sprite.Group()
		self.enemy_bullet_sprites = pygame.sprite.Group()

		# sprite groups
		self.rendered_sprites = Camera(self.game, self)
		self.updated_sprites = pygame.sprite.Group()
		self.exit_sprites = pygame.sprite.Group()
		self.block_sprites = pygame.sprite.Group()
		self.void_sprites = pygame.sprite.Group()
		self.enemy_sprites = pygame.sprite.Group()
		self.npc_sprites = pygame.sprite.Group()
		self.attackable_sprites = pygame.sprite.Group()
		self.gun_sprites = pygame.sprite.Group()
		self.health_sprites = pygame.sprite.Group()
		self.juice_sprites = pygame.sprite.Group()

		self.zone_size = self.get_zone_size()
		self.create_map()

		self.ui = UI(self.game, self)
		self.fade_surf = FadeSurf(self, [self.updated_sprites, self.rendered_sprites], (0,0))
		self.collection_cutscene = CollectionCutscene(self.game, self)

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
				self.target = self.player
				

		for obj in tmx_data.get_layer_by_name('exits'):
			if obj.name == '1': Exit([self.exit_sprites, self.updated_sprites], (obj.x, obj.y ), obj.name)
			if obj.name == '2': Exit([self.exit_sprites, self.updated_sprites], (obj.x, obj.y), obj.name)
			if obj.name == '3': Exit([self.exit_sprites, self.updated_sprites], (obj.x, obj.y), obj.name)

		for obj in tmx_data.get_layer_by_name('entities'):
			#enemies
			if obj.name == 'grunt': self.grunt = Grunt(self.game, self, [self.enemy_sprites, self.updated_sprites, self.rendered_sprites], (obj.x, obj.y), LAYERS['player'], obj.name)
			if obj.name == 'hound': self.hound = Hound(self.game, self, [self.enemy_sprites, self.updated_sprites, self.rendered_sprites], (obj.x, obj.y), LAYERS['player'], obj.name)
			#NPCs
			if obj.name == 'warrior': self.warrior = Warrior(self.game, self, [self.npc_sprites, self.updated_sprites, self.rendered_sprites], (obj.x, obj.y), LAYERS['player'], obj.name)

		for obj in tmx_data.get_layer_by_name('collectibles'):
			if obj.name == 'juice': Collectible(self.game, self, [self.juice_sprites, self.updated_sprites, self.rendered_sprites], (obj.x, obj.y), LAYERS['player'], '../assets/collectibles/juice', obj.name)
			if obj.name not in COMPLETED_DATA['health']:
				if obj.name == 'health_1': self.health_1 = Collectible(self.game, self, [self.health_sprites, self.updated_sprites, self.rendered_sprites], (obj.x, obj.y), LAYERS['player'], '../assets/collectibles/health', obj.name)
				if obj.name == 'health_2': self.health_2 = Collectible(self.game, self, [self.health_sprites, self.updated_sprites, self.rendered_sprites], (obj.x, obj.y), LAYERS['player'], '../assets/collectibles/health', obj.name)
				if obj.name == 'health_3': self.health_3 = Collectible(self.game, self, [self.health_sprites, self.updated_sprites, self.rendered_sprites], (obj.x, obj.y), LAYERS['player'], '../assets/collectibles/health', obj.name)
				if obj.name == 'health_4': self.health_4 = Collectible(self.game, self, [self.health_sprites, self.updated_sprites, self.rendered_sprites], (obj.x, obj.y), LAYERS['player'], '../assets/collectibles/health', obj.name)
				if obj.name == 'health_5': self.health_5 = Collectible(self.game, self, [self.health_sprites, self.updated_sprites, self.rendered_sprites], (obj.x, obj.y), LAYERS['player'], '../assets/collectibles/health', obj.name)
				if obj.name == 'health_6': self.health_6 = Collectible(self.game, self, [self.health_sprites, self.updated_sprites, self.rendered_sprites], (obj.x, obj.y), LAYERS['player'], '../assets/collectibles/health', obj.name)
				if obj.name == 'health_7': self.health_7 = Collectible(self.game, self, [self.health_sprites, self.updated_sprites, self.rendered_sprites], (obj.x, obj.y), LAYERS['player'], '../assets/collectibles/health', obj.name)
				if obj.name == 'health_8': self.health_8 = Collectible(self.game, self, [self.health_sprites, self.updated_sprites, self.rendered_sprites], (obj.x, obj.y), LAYERS['player'], '../assets/collectibles/health', obj.name)

		for obj in tmx_data.get_layer_by_name('objects'):
			if obj.name == 'big tree': Tree(self.game, self, [self.block_sprites, self.updated_sprites, self.rendered_sprites], (obj.x, obj.y), LAYERS['player'], obj.image)
			if obj.name == 'medium tree': Tree(self.game, self, [self.block_sprites, self.updated_sprites, self.rendered_sprites], (obj.x, obj.y), LAYERS['player'], obj.image)
			if obj.name == 'tall tree': Tree(self.game, self, [self.block_sprites, self.updated_sprites, self.rendered_sprites], (obj.x, obj.y), LAYERS['player'], obj.image)
			if obj.name == 'red flower': AttackableTerrain(self.game, self, [self.block_sprites, self.attackable_sprites, self.updated_sprites, self.rendered_sprites], (obj.x, obj.y), LAYERS['player'], f'../assets/attackable_terrain/{obj.name}')
			if obj.name == 'blue flower': AttackableTerrain(self.game, self, [self.block_sprites, self.attackable_sprites, self.updated_sprites, self.rendered_sprites], (obj.x, obj.y), LAYERS['player'], f'../assets/attackable_terrain/{obj.name}')

		
		for x, y, surf in tmx_data.get_layer_by_name('walls').tiles():
			Object(self.game, self, [self.block_sprites, self.updated_sprites], (x * TILESIZE, y * TILESIZE), LAYERS['player'], surf)

		for x, y, surf in tmx_data.get_layer_by_name('void').tiles():
			Void(self.game, self, [self.void_sprites, self.updated_sprites], (x * TILESIZE, y * TILESIZE), LAYERS['player'], surf)
		# self.create_guns()

		# create shadows for player and NPCs
		Shadow(self.game, self, [self.updated_sprites, self.rendered_sprites], (self.player.hitbox.midbottom), LAYERS['particles'], self.player, 'medium')
		for sprite in self.npc_sprites:
			Shadow(self.game, self, [self.updated_sprites, self.rendered_sprites], (sprite.hitbox.midbottom), LAYERS['particles'], sprite, 'medium')
		for sprite in self.enemy_sprites:
			Shadow(self.game, self, [self.updated_sprites, self.rendered_sprites], (sprite.hitbox.midbottom), LAYERS['particles'], sprite, 'medium')
		for sprite in self.health_sprites:
			Shadow(self.game, self, [self.updated_sprites, self.rendered_sprites], (sprite.hitbox.midbottom), LAYERS['particles'], sprite, 'small')


		# add static image layers
		Object(self.game, self, [self.rendered_sprites], (0,-8), LAYERS['BG1'], pygame.image.load(f'../zones/{self.name}/static_bg.png').convert_alpha())
		Object(self.game, self, [self.rendered_sprites], (0,-8), LAYERS['floor'], pygame.image.load(f'../zones/{self.name}/floor.png').convert_alpha())
		Object(self.game, self, [self.rendered_sprites], (0, 0), LAYERS['floor'], pygame.image.load(f'../zones/{self.name}/rocks.png').convert_alpha())
	
	def create_zone(self, zone):
		Zone(self.game, zone, self.entry_point).enter_state()

	def create_melee(self):
		self.melee_sprite = Sword(self.game, self, [self.updated_sprites, self.rendered_sprites], self.player.hitbox.center, LAYERS['player'], '../assets/weapons/sword')
	
	def create_gun(self):
		self.gun_sprite = Gun(self.game, self, [self.updated_sprites, self.rendered_sprites], self.player.hitbox.center, LAYERS['player'], pygame.image.load(f'../assets/weapons/{self.player.gun}.png').convert_alpha())

	def create_player_bullet(self):
		self.bullet = Bullet(self.game, self, [self.updated_sprites, self.rendered_sprites], self.player.hitbox.center, LAYERS['player'], f'../assets/weapons/{self.player.gun}_bullet')
		self.player_bullet_sprites.add(self.bullet)

	def create_railgun_beam(self):
		angle = math.atan2(pygame.mouse.get_pos()[1]-self.player.hitbox.centery + self.rendered_sprites.offset[1], pygame.mouse.get_pos()[0]-self.player.hitbox.centerx + self.rendered_sprites.offset[0])
		x = math.hypot(WIDTH, HEIGHT) * math.cos(angle) + self.player.hitbox.centerx
		y = math.hypot(WIDTH, HEIGHT) * math.sin(angle) + self.player.hitbox.centery
		distance = ((x, y) - pygame.math.Vector2(self.player.hitbox.center)).magnitude()
		point_list = self.get_equidistant_points(self.player.hitbox.center - self.rendered_sprites.offset, (x - self.rendered_sprites.offset[0], y - self.rendered_sprites.offset[1]), int(distance/6))
		for num, point in enumerate(point_list):
			if 2 < num < 50: 
				self.beam = Beam(self.game, self, [self.updated_sprites, self.rendered_sprites], point + self.rendered_sprites.offset, LAYERS['particles'],  f'../assets/weapons/railgun_particle', 4)
				self.player_bullet_sprites.add(self.beam)
			for sprite in self.block_sprites:
				if sprite not in self.attackable_sprites:
					if sprite.hitbox.collidepoint(point + self.rendered_sprites.offset):
						#BeamBlast(self.game, self, 'beam_blast', [self.updated_sprites, self.rendered_sprites], point, LAYERS['explosions'])
						return False

	def lerp(self, v0, v1, t):
		return v0 + t * (v1 - v0)

	def get_equidistant_points(self, point_1, point_2, num_of_points):
		return [(self.lerp(point_1[0], point_2[0], 1./num_of_points * i), self.lerp(point_1[1], point_2[1], 1./num_of_points * i)) for i in range(num_of_points + 1)]
			
	def enemy_enemy_collisions(self):
		enemies = []
		for sprite in self.enemy_sprites:
			enemies.append(sprite)

		for i, enemy1 in enumerate(enemies):
		    for enemy2 in enemies[i+1:]:
		        if enemy1.hitbox.colliderect(enemy2.hitbox) and enemy2.alive:
	        		if enemy1.vel.x != 0:
	        			enemy1.vel.x = 0
	        		if enemy1.vel.y != 0:
	        			enemy1.vel.y = 0

	def enemy_shot_logic(self):
		for target in self.enemy_sprites:
			for bullet in self.player_bullet_sprites:
				if bullet.rect.colliderect(target.hitbox):
					if not target.invincible and target.alive:
						if not hasattr(bullet, 'alpha') or (hasattr(bullet, 'alpha') and bullet.alpha >= 255):
							target.health -= bullet.damage
							bullet.kill()
							target.invincible = True
							if target.health <= 0:
								target.invincible = False
								target.alive = False

				for sprite in self.block_sprites:
					if bullet.rect.colliderect(sprite.hitbox) and sprite not in self.attackable_sprites:
						bullet.kill()

	def collect(self):
		for sprite in self.health_sprites:
			if self.player.hitbox.colliderect(sprite.rect):
				self.ui.add_health()
				COMPLETED_DATA['health'].append(sprite.name)
				self.collection_cutscene.enter_state()
				sprite.alive = False
				sprite.kill()

		for sprite in self.juice_sprites:
			if self.player.hitbox.colliderect(sprite.hitbox):
				PLAYER_DATA['max_juice'] += 11
				sprite.alive = False
				sprite.kill()
				
		
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
			if self.player.rect.colliderect(sprite.rect):
				self.cutscene_running = True
				self.new_zone = ZONE_DATA[self.name][sprite.name]
				self.entry_point = sprite.name
			
	def update(self, dt):
		self.collect()
		self.exiting()
		self.enemy_shot_logic()
		self.enemy_enemy_collisions()
		self.fade_surf.update(dt)
		self.ui.update(dt)

		if ACTIONS['return']: 
			Map(self.game, self).enter_state()
			#self.exit_state()
			self.game.reset_keys()
		self.updated_sprites.update(dt)

	def draw(self, screen):
		screen.fill(GREEN)
		self.rendered_sprites.offset_draw(self.target)
		self.game.custom_cursor(screen)

		self.ui.draw(screen)
		self.fade_surf.draw(screen)

		self.game.render_text(str(round(self.game.clock.get_fps(), 2)), WHITE, self.game.small_font, (WIDTH * 0.5, HEIGHT * 0.1))
		self.game.render_text(self.player.changing_weapon, PINK, self.game.small_font, RES/2)
		self.game.render_text(self.player.invincible, WHITE, self.game.small_font, (WIDTH * 0.5, HEIGHT * 0.9))
		
