import pygame
from os import walk
from settings import *
from pytmx.util_pygame import load_pygame
from map import Map
from sprites import Bloom, BG, Cloud, FadeSurf, Collider, Exit, Decoration, Object, Post, Pillar, AnimatedObject, \
Fountain, Water, Barrier, Door, Platform, Void, Collectible, Gun, Sword, Tree, Beam, AttackableTerrain
from particles import Particle, Shadow

from entities.player import Player
from entities.moving_block import MovingBlock
from entities.NPCs import FallenSoldier, Warrior, Mercenary
from entities.enemy import Grunt, Hound, Pincer
from entities.shooting_enemy import Musketeer
from entities.boss1 import Boss1

class CreateZone:
	def __init__(self, game, zone):
		self.game = game
		self.zone = zone

		self.zone.fade_surf = FadeSurf(self.game, self.zone, [self.zone.updated_sprites], (0,0))
		#self.zone.bloom_surf = Bloom(self.zone, [self.zone.updated_sprites, self.zone.rendered_sprites], (0,0))

		self.layers = []

	def create(self):

		tmx_data = load_pygame(f'../zones/{self.zone.name}/{self.zone.name}.tmx')

		for layer in tmx_data.layers:
			self.layers.append(layer.name)

		if 'entries' in self.layers:
			# add the player
			for obj in tmx_data.get_layer_by_name('entries'):
				if obj.name == self.zone.entry_point:

					if obj.x > self.zone.zone_size[0] - (self.zone.zone_size[0]/5): self.zone.start_direction = 'left'
					elif obj.x < self.zone.zone_size[0]/5: self.zone.start_direction = 'right'
					elif obj.y < self.zone.zone_size[1]/2: self.zone.start_direction = 'down'
					else: self.zone.start_direction = 'up'

					self.zone.player = Player(self.zone.game, self.zone, [self.zone.updated_sprites, self.zone.rendered_sprites], (obj.x, obj.y), LAYERS['player'])
					self.zone.target = self.zone.player

		if 'cutscenes' in self.layers:
			for obj in tmx_data.get_layer_by_name('cutscenes'):
				if obj.name == '0': Collider([self.zone.cutscene_sprites, self.zone.updated_sprites], (obj.x, obj.y, obj.width, obj.height), obj.name)
				if obj.name == '1': Collider([self.zone.cutscene_sprites, self.zone.updated_sprites], (obj.x, obj.y, obj.width, obj.height), obj.name)
				if obj.name == '2': Collider([self.zone.cutscene_sprites, self.zone.updated_sprites], (obj.x, obj.y, obj.width, obj.height), obj.name)
				if obj.name == '3': Collider([self.zone.cutscene_sprites, self.zone.updated_sprites], (obj.x, obj.y, obj.width, obj.height), obj.name)
				if obj.name == '4': Collider([self.zone.cutscene_sprites, self.zone.updated_sprites], (obj.x, obj.y, obj.width, obj.height), obj.name)
				if obj.name == '5': Collider([self.zone.cutscene_sprites, self.zone.updated_sprites], (obj.x, obj.y, obj.width, obj.height), obj.name)
				if obj.name == '6': Collider([self.zone.cutscene_sprites, self.zone.updated_sprites], (obj.x, obj.y, obj.width, obj.height), obj.name)
				if obj.name == '7': Collider([self.zone.cutscene_sprites, self.zone.updated_sprites], (obj.x, obj.y, obj.width, obj.height), obj.name)
				if obj.name == '8': Collider([self.zone.cutscene_sprites, self.zone.updated_sprites], (obj.x, obj.y, obj.width, obj.height), obj.name)
				if obj.name == '9': Collider([self.zone.cutscene_sprites, self.zone.updated_sprites], (obj.x, obj.y, obj.width, obj.height), obj.name)
				if obj.name == '10': Collider([self.zone.cutscene_sprites, self.zone.updated_sprites], (obj.x, obj.y, obj.width, obj.height), obj.name)

		if 'exits' in self.layers:
			for obj in tmx_data.get_layer_by_name('exits'):
				if obj.name == '1': Exit([self.zone.exit_sprites, self.zone.updated_sprites], (obj.x, obj.y), (obj.width, obj.height), obj.name)
				if obj.name == '2': Exit([self.zone.exit_sprites, self.zone.updated_sprites], (obj.x, obj.y), (obj.width, obj.height), obj.name)
				if obj.name == '3': Exit([self.zone.exit_sprites, self.zone.updated_sprites], (obj.x, obj.y), (obj.width, obj.height), obj.name)

		if 'entities' in self.layers:
			for obj in tmx_data.get_layer_by_name('entities'):
				if obj.name == '100': self.zone.block = MovingBlock(self.zone.game, self.zone, [self.zone.moving_block_sprites, self.zone.updated_sprites, self.zone.rendered_sprites], (obj.x, obj.y), LAYERS['player'], 'block', int(obj.name))

				#enemies
				if obj.name == 'grunt': self.zone.grunt = Grunt(self.zone.game, self.zone, [self.zone.enemy_sprites, self.zone.updated_sprites, self.zone.rendered_sprites], (obj.x, obj.y), LAYERS['player'], obj.name)
				if obj.name == 'hound': self.zone.hound = Hound(self.zone.game, self.zone, [self.zone.enemy_sprites, self.zone.updated_sprites, self.zone.rendered_sprites], (obj.x, obj.y), LAYERS['player'], obj.name)
				if obj.name == 'pincer': self.zone.pincer = Pincer(self.zone.game, self.zone, [self.zone.enemy_sprites, self.zone.updated_sprites, self.zone.rendered_sprites], (obj.x, obj.y), LAYERS['player'], obj.name)
				if obj.name == 'musketeer': self.zone.musketeer = Musketeer(self.zone.game, self.zone, [self.zone.enemy_sprites, self.zone.shooting_enemy_sprites, self.zone.updated_sprites, self.zone.rendered_sprites], (obj.x, obj.y), LAYERS['player'], obj.name)
				#NPCs
				if obj.name == 'apothecary': self.zone.warrior = Warrior(self.zone.game, self.zone, [self.zone.npc_sprites, self.zone.updated_sprites, self.zone.rendered_sprites], (obj.x, obj.y), LAYERS['player'], obj.name)
				if obj.name == 'warrior': Warrior(self.zone.game, self.zone, [self.zone.npc_sprites, self.zone.updated_sprites, self.zone.rendered_sprites], (obj.x, obj.y), LAYERS['player'], obj.name)
				if obj.name == 'mercenary': self.zone.mercenary = Mercenary(self.zone.game, self.zone, [self.zone.npc_sprites, self.zone.updated_sprites, self.zone.rendered_sprites], (obj.x, obj.y), LAYERS['player'], obj.name)
				if obj.name == 'fallen_soldier': self.zone.fallen_soldier = FallenSoldier(self.zone.game, self.zone, [self.zone.npc_sprites, self.zone.updated_sprites, self.zone.rendered_sprites], (obj.x, obj.y), LAYERS['player'], obj.name)
				if obj.name == 'scientist': self.zone.scientist = Mercenary(self.zone.game, self.zone, [self.zone.npc_sprites, self.zone.updated_sprites, self.zone.rendered_sprites], (obj.x, obj.y), LAYERS['player'], obj.name)
				if obj.name == 'scientist_2': self.zone.scientist_2 = Mercenary(self.zone.game, self.zone, [self.zone.npc_sprites, self.zone.updated_sprites, self.zone.rendered_sprites], (obj.x, obj.y), LAYERS['player'], obj.name)
				#bosses
				if obj.name == 'boss1' and obj.name not in COMPLETED_DATA['bosses_defeated']: self.zone.boss = Boss1(self.zone.game, self.zone, [self.zone.boss_sprites, self.zone.enemy_sprites, self.zone.updated_sprites, self.zone.rendered_sprites], (obj.x, obj.y), LAYERS['player'], obj.name)

		if 'barriers' in self.layers:
			for obj in tmx_data.get_layer_by_name('barriers'):
				if obj.name == 'barrier': Barrier(self.zone.game, self.zone, [self.zone.barrier_sprites, self.zone.updated_sprites, self.zone.rendered_sprites], (obj.x, obj.y), LAYERS['player'], f'../assets/{obj.name}/', obj.name)
				if obj.name == '0': Collider([self.zone.barrier_activator_sprites, self.zone.updated_sprites], (obj.x, obj.y, obj.width, obj.height), obj.name)

		if 'collectibles' in self.layers:
			for obj in tmx_data.get_layer_by_name('collectibles'):
				if obj.name not in COMPLETED_DATA['guns']:
					if obj.name == 'pistol': Collectible(self.zone.game, self.zone, [self.zone.gun_pickup_sprites, self.zone.updated_sprites, self.zone.rendered_sprites], (obj.x, obj.y), LAYERS['player'], '../assets/collectibles/pistol', obj.name)
					if obj.name == 'railgun': Collectible(self.zone.game, self.zone, [self.zone.gun_pickup_sprites, self.zone.updated_sprites, self.zone.rendered_sprites], (obj.x, obj.y), LAYERS['player'], '../assets/collectibles/railgun', obj.name)
					if obj.name == 'shotgun': Collectible(self.zone.game, self.zone, [self.zone.gun_pickup_sprites, self.zone.updated_sprites, self.zone.rendered_sprites], (obj.x, obj.y), LAYERS['player'], '../assets/collectibles/shotgun', obj.name)
				if obj.name not in COMPLETED_DATA['keys']:
					if obj.name == 'key_0': Collectible(self.zone.game, self.zone, [self.zone.key_sprites, self.zone.updated_sprites, self.zone.rendered_sprites], (obj.x, obj.y), LAYERS['player'], '../assets/collectibles/key', obj.name)
					if obj.name == 'key_1': Collectible(self.zone.game, self.zone, [self.zone.key_sprites, self.zone.updated_sprites, self.zone.rendered_sprites], (obj.x, obj.y), LAYERS['player'], '../assets/collectibles/key', obj.name)
				if obj.name not in COMPLETED_DATA['juice']:
					if obj.name == 'juice_1': Collectible(self.zone.game, self.zone, [self.zone.juice_sprites, self.zone.updated_sprites, self.zone.rendered_sprites], (obj.x, obj.y), LAYERS['player'], '../assets/collectibles/juice', obj.name)
					if obj.name == 'juice_2': Collectible(self.zone.game, self.zone, [self.zone.juice_sprites, self.zone.updated_sprites, self.zone.rendered_sprites], (obj.x, obj.y), LAYERS['player'], '../assets/collectibles/juice', obj.name)
					if obj.name == 'juice_3':Collectible(self.zone.game, self.zone, [self.zone.juice_sprites, self.zone.updated_sprites, self.zone.rendered_sprites], (obj.x, obj.y), LAYERS['player'], '../assets/collectibles/juice', obj.name)
					if obj.name == 'juice_4': Collectible(self.zone.game, self.zone, [self.zone.juice_sprites, self.zone.updated_sprites, self.zone.rendered_sprites], (obj.x, obj.y), LAYERS['player'], '../assets/collectibles/juice', obj.name)
					if obj.name == 'juice_5': Collectible(self.zone.game, self.zone, [self.zone.juice_sprites, self.zone.updated_sprites, self.zone.rendered_sprites], (obj.x, obj.y), LAYERS['player'], '../assets/collectibles/juice', obj.name)
					if obj.name == 'juice_6': Collectible(self.zone.game, self.zone, [self.zone.juice_sprites, self.zone.updated_sprites, self.zone.rendered_sprites], (obj.x, obj.y), LAYERS['player'], '../assets/collectibles/juice', obj.name)
				if obj.name not in COMPLETED_DATA['health']:
					if obj.name == 'health_0': Collectible(self.zone.game, self.zone, [self.zone.health_sprites, self.zone.updated_sprites, self.zone.rendered_sprites], (obj.x, obj.y), LAYERS['player'], '../assets/collectibles/health', obj.name)
					if obj.name == 'health_1': Collectible(self.zone.game, self.zone, [self.zone.health_sprites, self.zone.updated_sprites, self.zone.rendered_sprites], (obj.x, obj.y), LAYERS['player'], '../assets/collectibles/health', obj.name)
					if obj.name == 'health_2': Collectible(self.zone.game, self.zone, [self.zone.health_sprites, self.zone.updated_sprites, self.zone.rendered_sprites], (obj.x, obj.y), LAYERS['player'], '../assets/collectibles/health', obj.name)
					if obj.name == 'health_3': Collectible(self.zone.game, self.zone, [self.zone.health_sprites, self.zone.updated_sprites, self.zone.rendered_sprites], (obj.x, obj.y), LAYERS['player'], '../assets/collectibles/health', obj.name)
					if obj.name == 'health_4': Collectible(self.zone.game, self.zone, [self.zone.health_sprites, self.zone.updated_sprites, self.zone.rendered_sprites], (obj.x, obj.y), LAYERS['player'], '../assets/collectibles/health', obj.name)
					if obj.name == 'health_5': Collectible(self.zone.game, self.zone, [self.zone.health_sprites, self.zone.updated_sprites, self.zone.rendered_sprites], (obj.x, obj.y), LAYERS['player'], '../assets/collectibles/health', obj.name)
					if obj.name == 'health_6': Collectible(self.zone.game, self.zone, [self.zone.health_sprites, self.zone.updated_sprites, self.zone.rendered_sprites], (obj.x, obj.y), LAYERS['player'], '../assets/collectibles/health', obj.name)
					if obj.name == 'health_7': Collectible(self.zone.game, self.zone, [self.zone.health_sprites, self.zone.updated_sprites, self.zone.rendered_sprites], (obj.x, obj.y), LAYERS['player'], '../assets/collectibles/health', obj.name)
					if obj.name == 'health_8': Collectible(self.zone.game, self.zone, [self.zone.health_sprites, self.zone.updated_sprites, self.zone.rendered_sprites], (obj.x, obj.y), LAYERS['player'], '../assets/collectibles/health', obj.name)
					if obj.name == 'health_9': Collectible(self.zone.game, self.zone, [self.zone.health_sprites, self.zone.updated_sprites, self.zone.rendered_sprites], (obj.x, obj.y), LAYERS['player'], '../assets/collectibles/health', obj.name)
					if obj.name == 'health_10': Collectible(self.zone.game, self.zone, [self.zone.health_sprites, self.zone.updated_sprites, self.zone.rendered_sprites], (obj.x, obj.y), LAYERS['player'], '../assets/collectibles/health', obj.name)
					if obj.name == 'health_11': Collectible(self.zone.game, self.zone, [self.zone.health_sprites, self.zone.updated_sprites, self.zone.rendered_sprites], (obj.x, obj.y), LAYERS['player'], '../assets/collectibles/health', obj.name)

		if 'objects' in self.layers:
			for obj in tmx_data.get_layer_by_name('objects'):
				if obj.name == 'grass': Decoration(self.zone.game, self.zone, [self.zone.rendered_sprites], (obj.x, obj.y), LAYERS['particles'], obj.image)
				if obj.name == 'grass 1': Decoration(self.zone.game, self.zone, [self.zone.rendered_sprites], (obj.x, obj.y), LAYERS['particles'], obj.image)
				if obj.name == 'grass 2': Decoration(self.zone.game, self.zone, [self.zone.rendered_sprites], (obj.x, obj.y), LAYERS['particles'], obj.image)
				if obj.name == 'grass 3': Decoration(self.zone.game, self.zone, [self.zone.rendered_sprites], (obj.x, obj.y), LAYERS['particles'], obj.image)
				if obj.name == 'grass 4': Decoration(self.zone.game, self.zone, [self.zone.rendered_sprites], (obj.x, obj.y), LAYERS['particles'], obj.image)
				if obj.name == 'grass 5': Decoration(self.zone.game, self.zone, [self.zone.rendered_sprites], (obj.x, obj.y), LAYERS['particles'], obj.image)

				if obj.name == 'water_1': Water(self.zone.game, self.zone, [self.zone.updated_sprites, self.zone.rendered_sprites], (obj.x, obj.y), LAYERS['BG1'], f'../decoration/{obj.name}')
				if obj.name == 'waterfall': Water(self.zone.game, self.zone, [self.zone.updated_sprites, self.zone.rendered_sprites], (obj.x, obj.y), LAYERS['BG1'], f'../decoration/{obj.name}')

				if obj.name == 'red flower': AttackableTerrain(self.zone.game, self.zone, [self.zone.block_sprites, self.zone.attackable_sprites, self.zone.updated_sprites, self.zone.rendered_sprites], (obj.x, obj.y), LAYERS['player'], f'../assets/attackable_terrain/{obj.name}')
				if obj.name == 'blue flower': AttackableTerrain(self.zone.game, self.zone, [self.zone.block_sprites, self.zone.attackable_sprites, self.zone.updated_sprites, self.zone.rendered_sprites], (obj.x, obj.y), LAYERS['player'], f'../assets/attackable_terrain/{obj.name}')
				if obj.name == 'box': AttackableTerrain(self.zone.game, self.zone, [self.zone.block_sprites, self.zone.attackable_sprites, self.zone.updated_sprites, self.zone.rendered_sprites], (obj.x, obj.y), LAYERS['player'], f'../assets/attackable_terrain/{obj.name}')
				if obj.name == 'box 2': AttackableTerrain(self.zone.game, self.zone, [self.zone.block_sprites, self.zone.attackable_sprites, self.zone.updated_sprites, self.zone.rendered_sprites], (obj.x, obj.y), LAYERS['player'], f'../assets/attackable_terrain/{obj.name}')
				if obj.name == 'tall box': AttackableTerrain(self.zone.game, self.zone, [self.zone.block_sprites, self.zone.attackable_sprites, self.zone.updated_sprites, self.zone.rendered_sprites], (obj.x, obj.y), LAYERS['player'], f'../assets/attackable_terrain/{obj.name}')
				if obj.name == 'wide box': AttackableTerrain(self.zone.game, self.zone, [self.zone.block_sprites, self.zone.attackable_sprites, self.zone.updated_sprites, self.zone.rendered_sprites], (obj.x, obj.y), LAYERS['player'], f'../assets/attackable_terrain/{obj.name}')
				if obj.name == 'open box': AttackableTerrain(self.zone.game, self.zone, [self.zone.block_sprites, self.zone.attackable_sprites, self.zone.updated_sprites, self.zone.rendered_sprites], (obj.x, obj.y), LAYERS['player'], f'../assets/attackable_terrain/{obj.name}')
				if obj.name == 'white box': AttackableTerrain(self.zone.game, self.zone, [self.zone.block_sprites, self.zone.attackable_sprites, self.zone.updated_sprites, self.zone.rendered_sprites], (obj.x, obj.y), LAYERS['player'], f'../assets/attackable_terrain/{obj.name}')
				if obj.name == 'small box': AttackableTerrain(self.zone.game, self.zone, [self.zone.block_sprites, self.zone.attackable_sprites, self.zone.updated_sprites, self.zone.rendered_sprites], (obj.x, obj.y), LAYERS['player'], f'../assets/attackable_terrain/{obj.name}')
				if obj.name == 'fountain': Fountain(self.zone.game, self.zone, [self.zone.block_sprites, self.zone.block_sprites, self.zone.updated_sprites, self.zone.rendered_sprites], (obj.x, obj.y), LAYERS['player'], f'../animated_objects/{obj.name}')

				if obj.name == 'blue tree': Tree(self.zone.game, self.zone, [self.zone.block_sprites, self.zone.updated_sprites, self.zone.rendered_sprites], (obj.x, obj.y), LAYERS['player'], obj.image)
				if obj.name == 'big tree': Tree(self.zone.game, self.zone, [self.zone.block_sprites, self.zone.updated_sprites, self.zone.rendered_sprites], (obj.x, obj.y), LAYERS['player'], obj.image)
				if obj.name == 'medium tree': Tree(self.zone.game, self.zone, [self.zone.block_sprites, self.zone.updated_sprites, self.zone.rendered_sprites], (obj.x, obj.y), LAYERS['player'], obj.image)
				if obj.name == 'medium tree 2': Tree(self.zone.game, self.zone, [self.zone.block_sprites, self.zone.updated_sprites, self.zone.rendered_sprites], (obj.x, obj.y), LAYERS['player'], obj.image)
				if obj.name == 'medium tree 3': Tree(self.zone.game, self.zone, [self.zone.block_sprites, self.zone.updated_sprites, self.zone.rendered_sprites], (obj.x, obj.y), LAYERS['player'], obj.image)
				if obj.name == 'small tree': Tree(self.zone.game, self.zone, [self.zone.block_sprites, self.zone.updated_sprites, self.zone.rendered_sprites], (obj.x, obj.y), LAYERS['player'], obj.image)
				if obj.name == 'small tree 2': Tree(self.zone.game, self.zone, [self.zone.block_sprites, self.zone.updated_sprites, self.zone.rendered_sprites], (obj.x, obj.y), LAYERS['player'], obj.image)
				if obj.name == 'tall tree': Tree(self.zone.game, self.zone, [self.zone.block_sprites, self.zone.updated_sprites, self.zone.rendered_sprites], (obj.x, obj.y), LAYERS['player'], obj.image)
				if obj.name == 'small_bust': Tree(self.zone.game, self.zone, [self.zone.block_sprites, self.zone.updated_sprites, self.zone.rendered_sprites], (obj.x, obj.y), LAYERS['player'], obj.image)
				if obj.name == 'post': Post(self.zone.game, self.zone, [self.zone.block_sprites, self.zone.updated_sprites, self.zone.rendered_sprites], (obj.x, obj.y), LAYERS['player'], obj.image)
				if obj.name == 'post_right': Post(self.zone.game, self.zone, [self.zone.block_sprites, self.zone.updated_sprites, self.zone.rendered_sprites], (obj.x, obj.y), LAYERS['player'], obj.image)
				if obj.name == 'post_left': Post(self.zone.game, self.zone, [self.zone.block_sprites, self.zone.updated_sprites, self.zone.rendered_sprites], (obj.x, obj.y), LAYERS['player'], obj.image)
				if obj.name == 'post_left_right': Post(self.zone.game, self.zone, [self.zone.block_sprites, self.zone.updated_sprites, self.zone.rendered_sprites], (obj.x, obj.y), LAYERS['player'], obj.image)
				if obj.name == 'post_middle': Post(self.zone.game, self.zone, [self.zone.block_sprites, self.zone.updated_sprites, self.zone.rendered_sprites], (obj.x, obj.y), LAYERS['player'], obj.image)
				if obj.name == 'post_down': Post(self.zone.game, self.zone, [self.zone.block_sprites, self.zone.updated_sprites, self.zone.rendered_sprites], (obj.x, obj.y), LAYERS['player'], obj.image)
				if obj.name == 'post_down_middle': Post(self.zone.game, self.zone, [self.zone.block_sprites, self.zone.updated_sprites, self.zone.rendered_sprites], (obj.x, obj.y), LAYERS['player'], obj.image)

				if obj.name == 'radio_shack_bottom': Post(self.zone.game, self.zone, [self.zone.block_sprites, self.zone.updated_sprites, self.zone.rendered_sprites], (obj.x, obj.y), LAYERS['player'], obj.image)
				if obj.name == 'big_chamber': Post(self.zone.game, self.zone, [self.zone.block_sprites, self.zone.updated_sprites, self.zone.rendered_sprites], (obj.x, obj.y), LAYERS['player'], obj.image)
				if obj.name == 'small_chamber': Post(self.zone.game, self.zone, [self.zone.block_sprites, self.zone.updated_sprites, self.zone.rendered_sprites], (obj.x, obj.y), LAYERS['player'], obj.image)
				if obj.name == 'lab_table': Post(self.zone.game, self.zone, [self.zone.block_sprites, self.zone.updated_sprites, self.zone.rendered_sprites], (obj.x, obj.y), LAYERS['player'], obj.image)
				if obj.name == 'lab_computer': Post(self.zone.game, self.zone, [self.zone.block_sprites, self.zone.updated_sprites, self.zone.rendered_sprites], (obj.x, obj.y), LAYERS['player'], obj.image)
				if obj.name == 'lab_computer_2': Post(self.zone.game, self.zone, [self.zone.block_sprites, self.zone.updated_sprites, self.zone.rendered_sprites], (obj.x, obj.y), LAYERS['player'], obj.image)

		if 'doors' in self.layers:
			for obj in tmx_data.get_layer_by_name('doors'):
				if obj.name == '0': Door(self.zone.game, self.zone, [self.zone.block_sprites, self.zone.updated_sprites, self.zone.rendered_sprites], (obj.x, obj.y), LAYERS['player'], f'../doors/{obj.name}', obj.name)
				if obj.name == '1': Door(self.zone.game, self.zone, [self.zone.block_sprites, self.zone.updated_sprites, self.zone.rendered_sprites], (obj.x, obj.y), LAYERS['player'], f'../doors/{obj.name}', obj.name)
				if obj.name == '2': Door(self.zone.game, self.zone, [self.zone.block_sprites, self.zone.updated_sprites, self.zone.rendered_sprites], (obj.x, obj.y), LAYERS['player'], f'../doors/{obj.name}', obj.name)

		if 'platforms' in self.layers:
			for obj in tmx_data.get_layer_by_name('platforms'):
				if obj.name == '0': Platform(self.zone.game, self.zone, [self.zone.platform_sprites, self.zone.updated_sprites], (obj.x, obj.y), LAYERS['floor'], f'../platforms/{obj.name}', obj.name, 80)
				if obj.name == '1': Platform(self.zone.game, self.zone, [self.zone.platform_sprites, self.zone.updated_sprites], (obj.x, obj.y), LAYERS['floor'], f'../platforms/{obj.name}', obj.name, 150)

		if 'triggers' in self.layers:
			for obj in tmx_data.get_layer_by_name('triggers'):
				if obj.name == '0': Pillar(self.zone.game, self.zone, [self.zone.trigger_sprites, self.zone.block_sprites, self.zone.updated_sprites, self.zone.rendered_sprites], (obj.x, obj.y), LAYERS['player'], obj.image, obj.name)
				if obj.name == '1': Pillar(self.zone.game, self.zone, [self.zone.trigger_sprites, self.zone.block_sprites, self.zone.updated_sprites, self.zone.rendered_sprites], (obj.x, obj.y), LAYERS['player'], obj.image, obj.name)
			# tilesets
			# for x, y, surf in tmx_data.get_layer_by_name('floor').tiles():
			# 	Object(self.zone.game, self.zone, [self.zone.rendered_sprites], (x * TILESIZE, y * TILESIZE), LAYERS['floor'], surf)

		if 'walls' in self.layers:
			for x, y, surf in tmx_data.get_layer_by_name('walls').tiles():
				Object(self.zone.game, self.zone, [self.zone.block_sprites, self.zone.rendered_sprites], (x * TILESIZE, y * TILESIZE), LAYERS['player'], surf)

		# if 'floor' in self.layers:
		# 	for x, y, surf in tmx_data.get_layer_by_name('floor').tiles():
		# 		Object(self.zone.game, self.zone, [self.zone.rendered_sprites], (x * TILESIZE, y * TILESIZE), LAYERS['floor'], surf)
			
		if 'void' in self.layers:
			for x, y, surf in tmx_data.get_layer_by_name('void').tiles():
				Void(self.zone.game, self.zone, [self.zone.void_sprites, self.zone.updated_sprites], (x * TILESIZE, y * TILESIZE + 8), LAYERS['player'], surf)
			# for x, y, surf in tmx_data.get_layer_by_name('platforms').tiles():
			# 	Platform(self.zone.game, self.zone, [self.zone.platform_sprites, self.zone.updated_sprites, self.zone.rendered_sprites], (x * TILESIZE, y * TILESIZE), LAYERS['floor'], f'../platforms/0')

		# create shadows for player and NPCs
		Shadow(self.zone.game, self.zone, [self.zone.updated_sprites, self.zone.rendered_sprites], (self.zone.player.hitbox.midbottom), LAYERS['particles'], self.zone.player, 'medium')
		for sprite in self.zone.npc_sprites:
			if hasattr(self.zone, 'fallen_soldier'):
				if not sprite == self.zone.fallen_soldier:
					Shadow(self.zone.game, self.zone, [self.zone.updated_sprites, self.zone.rendered_sprites], (sprite.hitbox.midbottom), LAYERS['particles'], sprite, 'medium')
				else:
					pass
			else:
				Shadow(self.zone.game, self.zone, [self.zone.updated_sprites, self.zone.rendered_sprites], (sprite.hitbox.midbottom), LAYERS['particles'], sprite, 'medium')

		for sprite in self.zone.enemy_sprites:
			if sprite.shadow:
				if sprite in self.zone.boss_sprites:
					Shadow(self.zone.game, self.zone, [self.zone.updated_sprites, self.zone.rendered_sprites], (sprite.hitbox.midbottom), LAYERS['particles'], sprite, 'big')
				else:
					Shadow(self.zone.game, self.zone, [self.zone.updated_sprites, self.zone.rendered_sprites], (sprite.hitbox.midbottom), LAYERS['particles'], sprite, 'medium')

		for sprite in self.zone.health_sprites:
			Shadow(self.zone.game, self.zone, [self.zone.updated_sprites, self.zone.rendered_sprites], (sprite.hitbox.midbottom), LAYERS['particles'], sprite, 'medium')
		for sprite in self.zone.juice_sprites:
			Shadow(self.zone.game, self.zone, [self.zone.updated_sprites, self.zone.rendered_sprites], (sprite.hitbox.midbottom), LAYERS['particles'], sprite, 'medium')
		for sprite in self.zone.key_sprites:
			Shadow(self.zone.game, self.zone, [self.zone.updated_sprites, self.zone.rendered_sprites], (sprite.hitbox.midbottom), LAYERS['particles'], sprite, 'medium')
		for sprite in self.zone.gun_pickup_sprites:
			Shadow(self.zone.game, self.zone, [self.zone.updated_sprites, self.zone.rendered_sprites], (sprite.hitbox.midbottom), LAYERS['particles'], sprite, 'medium')

		if 'images' in self.layers:
			for obj in tmx_data.get_layer_by_name('images'):
				if obj.name == 'static_bg': BG(self.zone.game, self.zone, [self.zone.rendered_sprites], (obj.x, obj.y), LAYERS['BG1'], pygame.image.load(f'../zones/{self.zone.name}/{obj.name}.png').convert_alpha())
				if obj.name == 'bg': BG(self.zone.game, self.zone, [self.zone.updated_sprites, self.zone.rendered_sprites], (obj.x, obj.y), LAYERS['BG0'], pygame.image.load(f'../zones/{self.zone.name}/{obj.name}.png').convert_alpha())
				if obj.name == 'floor': BG(self.zone.game, self.zone, [self.zone.rendered_sprites], (obj.x, obj.y), LAYERS['floor'], pygame.image.load(f'../zones/{self.zone.name}/{obj.name}.png').convert_alpha())
				if obj.name == 'foreground': BG(self.zone.game, self.zone, [self.zone.updated_sprites, self.zone.rendered_sprites], (obj.x, obj.y), LAYERS['foreground'], pygame.image.load(f'../zones/{self.zone.name}/{obj.name}.png').convert_alpha())

		# add static image layers
		for _, __, img_files in walk(f'../zones/{self.zone.name}'):
			for img in img_files:
		# 		if img == 'static_bg.png': BG(self.zone.game, self.zone, [self.zone.rendered_sprites], (0, 0), LAYERS['BG1'], pygame.image.load(f'../zones/{self.zone.name}/{img}').convert_alpha())
		# 		if img == 'bg.png': BG(self.zone.game, self.zone, [self.zone.updated_sprites, self.zone.rendered_sprites], (0, 0), LAYERS['BG0'], pygame.image.load(f'../zones/{self.zone.name}/{img}').convert_alpha())
		# 		if img == 'floor.png': BG(self.zone.game, self.zone, [self.zone.rendered_sprites], (0, 0), LAYERS['floor'], pygame.image.load(f'../zones/{self.zone.name}/{img}').convert_alpha())
		# 		if img == 'foreground.png': BG(self.zone.game, self.zone, [self.zone.updated_sprites, self.zone.rendered_sprites], (0,0), LAYERS['foreground'], pygame.image.load(f'../zones/{self.zone.name}/{img}').convert_alpha())
		# 		# if img == 'foreground.png': BG(self.zone.game, self.zone, [self.zone.updated_sprites, self.zone.rendered_sprites], (16 * TILESIZE, TILESIZE), LAYERS['foreground'], pygame.image.load(f'../zones/{self.zone.name}/{img}').convert_alpha())
		# 		# if img == 'foreground.png': BG(self.zone.game, self.zone, [self.zone.updated_sprites, self.zone.rendered_sprites], (21 * TILESIZE, TILESIZE), LAYERS['foreground'], pygame.image.load(f'../zones/{self.zone.name}/{img}').convert_alpha())
		 		# moving bgs clouds
		 		if img == 'cloud.png': Cloud(self.zone.game, self.zone, [self.zone.updated_sprites, self.zone.rendered_sprites], (self.zone.zone_size[0]*0.3, 32), LAYERS['BG1'], pygame.image.load(f'../zones/{self.zone.name}/{img}').convert_alpha(), (0.05, 0))
		 		if img == 'cloud2.png': Cloud(self.zone.game, self.zone, [self.zone.updated_sprites, self.zone.rendered_sprites], (0, 120), LAYERS['BG1'], pygame.image.load(f'../zones/{self.zone.name}/{img}').convert_alpha(), (0.1, 0))
		 		if img == 'cloud2.png': Cloud(self.zone.game, self.zone, [self.zone.updated_sprites, self.zone.rendered_sprites], (self.zone.zone_size[0]*0.6, 90), LAYERS['BG1'], pygame.image.load(f'../zones/{self.zone.name}/{img}').convert_alpha(), (0.1, 0))
		 		if img == 'cloud3.png': Cloud(self.zone.game, self.zone, [self.zone.updated_sprites, self.zone.rendered_sprites], (self.zone.zone_size[0]*0.2, 166), LAYERS['BG1'], pygame.image.load(f'../zones/{self.zone.name}/{img}').convert_alpha(), (0.2, 0))

		
				# if img == 'static_bg.png': Object(self.zone.game, self.zone, [self.zone.rendered_sprites], (0, 0), LAYERS['BG1'], pygame.image.load(f'../zones/{self.zone.name}/{img}').convert_alpha())
				# #if img == 'floor.png': Object(self.zone.game, self.zone, [self.zone.rendered_sprites], (0, 0), LAYERS['floor'], pygame.image.load(f'../zones/{self.zone.name}/{img}').convert_alpha())
				# if img == 'spaceship.png': Object(self.zone.game, self.zone, [self.zone.rendered_sprites], (0, 0), LAYERS['foreground'], pygame.image.load(f'../zones/{self.zone.name}/{img}').convert_alpha())
	