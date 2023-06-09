import math
from settings import *
from NPCs import NPC
from player_fsm import Idle

class Player(NPC):
	def __init__(self, game, zone, groups, pos, z, name = 'player'):
		super().__init__(game, zone, groups, pos, z, name)

		self.game = game
		self.zone = zone
		self.z = z

		self.state = Idle(self, self.zone.start_direction)

		self.animations = {'up':[], 'down':[], 'left':[], 'right':[], 'up_idle':[], 'down_idle':[], 'left_idle':[], 'right_idle':[],
							'up_dash':[], 'down_dash':[], 'left_dash':[], 'right_dash':[], 'up_fall':[], 'down_fall':[], 'left_fall':[], 'right_fall':[],
							'up_attack':[], 'down_attack':[], 'left_attack':[], 'right_attack':[], 'up_heal':[], 'down_heal':[], 'left_heal':[], 'right_heal':[]}
	
		self.direction = {'up': False, 'down': False, 'left': False, 'right': False}
		
		self.gun_index = PLAYER_DATA['gun_index']
		self.gun = list(GUN_DATA.keys())[self.gun_index]
		self.changing_weapon = False
	
		self.import_imgs()
		self.animation_type = 'loop'
		self.frame_index = 0
		self.image = self.animations['down'][self.frame_index]
		self.rect = self.image.get_rect(center = pos)
		self.pos = pygame.math.Vector2(self.rect.center)

		self.respawn_location = pygame.math.Vector2()

		# attacking
		self.attack_count = 0
		self.attack_timer_running = False
		self.attack_timer = 0
		self.attack_cooldown = 80

		# dashing
		self.dash_count = 0
		self.dash_timer_running = False
		self.dash_timer = 0
		self.dash_cooldown = 100

	def attack_timer_logic(self, dt):
		if self.attack_timer_running: 
			self.attack_timer += dt
		if self.attack_timer >= self.attack_cooldown: 
			self.attack_timer_running = False
			self.attack_count = 0
			self.attack_timer = 0

	def dash_timer_logic(self, dt):
		if self.dash_timer_running: 
			self.dash_timer += dt
		if self.dash_timer >= self.dash_cooldown: 
			self.dash_timer_running = False
			self.dash_count = 0
			self.dash_timer = 0

	def change_gun(self, direction):
		if not self.changing_weapon:

			if direction == 'scroll_down':
				if PLAYER_DATA['gun_index'] < len(list(GUN_DATA.keys()))-1: PLAYER_DATA['gun_index'] += 1
				else: PLAYER_DATA['gun_index'] = 0
				self.changing_weapon = True
				ACTIONS['scroll_down'] = False
			
			elif direction == 'scroll_up':
				if PLAYER_DATA['gun_index'] > 0: PLAYER_DATA['gun_index'] -= 1
				else: PLAYER_DATA['gun_index'] = len(list(GUN_DATA.keys()))-1
				self.changing_weapon = True
				ACTIONS['scroll_up'] = False

		self.gun = list(GUN_DATA.keys())[PLAYER_DATA['gun_index']]
	

	def attackable_terrain_logic(self):
		if self.zone.melee_sprite:
			for target in self.zone.attackable_sprites:
				if self.zone.melee_sprite.rect.colliderect(target.hitbox) and self.zone.melee_sprite.frame_index < 1:
					self.add_subtract_juice(5.5, 'add')
					target.alive = False

	def player_attacking_logic(self):
		if self.zone.melee_sprite:
			for target in self.zone.enemy_sprites:
				if self.zone.melee_sprite.rect.colliderect(target.hitbox) and self.zone.melee_sprite.frame_index < 1:
					if not target.invincible and target.alive:
						target.invincible = True
						self.add_subtract_juice(11, 'add')
						target.health -= 1
						if target.health <= 0:
							target.alive = False
							target.invincible = False

	def enemy_attacking_logic(self):
		for sprite in self.zone.enemy_sprites:
			if not self.invincible and not sprite.invincible and sprite.alive and self.alive and sprite.dashing:
				if sprite.hitbox.colliderect(self.hitbox):
					self.reduce_health(sprite.damage)
					self.screenshaking = True
					self.invincible = True
					if self.zone.melee_sprite: self.zone.melee_sprite.kill()

	def reduce_health(self, amount):
		if not self.invincible:
			self.game.current_health -= amount
			self.zone.ui.flash_icon()
			if self.game.current_health <= 0:
				self.alive = False
				self.game.current_health = PLAYER_DATA['max_health']
				self.zone.exit_state()
				self.zone.create_zone(self.zone.name)

	def add_subtract_juice(self, amount, direction):
		if direction == 'add': self.game.current_juice += amount
		else: self.game.current_juice -= amount
		if self.game.current_juice <= 0:self.game.current_juice = 0
		if self.game.current_juice > PLAYER_DATA['max_juice']: self.game.current_juice = PLAYER_DATA['max_juice']

	def update(self, dt):
		self.invincibility(dt)
		self.attack_timer_logic(dt)
		self.dash_timer_logic(dt)
		if not self.zone.cutscene_running: self.state_logic()
		self.state.update(dt, self)
		
		


		
