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
							'up_attack':[], 'down_attack':[], 'left_attack':[], 'right_attack':[]}
	
		self.direction = {'up': False, 'down': False, 'left': False, 'right': False}
		
		self.gun_index = PLAYER_DATA['gun_index']
		self.gun = list(GUN_DATA.keys())[self.gun_index]
	
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
		self.attack_cooldown = 100

		# dashing
		self.dash_count = 0
		self.dash_timer_running = False
		self.dash_timer = 0
		self.dash_cooldown = 100

	def attack_logic(self, dt):
		if self.attack_timer_running: 
			self.attack_timer += 1 *dt
		if self.attack_timer >= self.attack_cooldown: 
			self.attack_timer_running = False
			self.attack_count = 0
			self.attack_timer = 0

	def dash_logic(self, dt):
		if self.dash_timer_running: 
			self.dash_timer += 1 *dt
		if self.dash_timer >= self.dash_cooldown: 
			self.dash_timer_running = False
			self.dash_count = 0
			self.dash_timer = 0

	
	def update(self, dt):
		self.invincibility(dt)
		self.attack_logic(dt)
		self.dash_logic(dt)
		if not self.zone.cutscene_running: self.state_logic()
		self.state.update(dt, self)
		
		


		
