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

		self.state = Idle('down')
		self.animations = {'up':[], 'down':[], 'left':[], 'right':[], 'up_idle':[], 'down_idle':[], 'left_idle':[], 'right_idle':[],
							'up_dash':[], 'down_dash':[], 'left_dash':[], 'right_dash':[], 'up_fall':[], 'down_fall':[], 'left_fall':[], 'right_fall':[]}
	
		self.direction = {'up': False, 'down': False, 'left': False, 'right': False}
	
		self.import_imgs()
		self.animation_type = 'loop'
		self.frame_index = 0
		self.image = self.animations['down'][self.frame_index]
		self.rect = self.image.get_rect(center = pos)
		self.pos = pygame.math.Vector2(self.rect.center)
		self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.6, -self.rect.height * 0.7)


		self.respawn_location = pygame.math.Vector2()

	def update(self, dt):
		if not self.zone.cutscene_running and self.zone.alpha < 100: self.state_logic()
		self.state.update(dt, self)
		

		
