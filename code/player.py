import math
from settings import *
from state_machine import Idle

class Player(pygame.sprite.Sprite):
	def __init__(self, game, zone, groups, pos, z):
		super().__init__(groups)

		self.game = game
		self.zone = zone
		self.z = z

		self.max_speed = 2

		self.state = Idle(self, 'up')


		self.direction = {'left': False, 'right': False, 'up': False, 'down': False,}
	

		self.acc = pygame.math.Vector2()
		self.friction = -0.5
		self.vel = pygame.math.Vector2()
	
		self.image = pygame.Surface((16, 24))
		self.image.fill(BLUE)
		self.rect = self.image.get_rect(center = pos)
		self.pos = pygame.math.Vector2(self.rect.center)
		self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.5, -self.rect.height * 0.75)

	def import_imgs(self):
		self.animations = {'down_attack':[], 'up_attack':[], 'right_attack':[], 'left_attack':[],\
		'up':[], 'down':[], 'left':[], 'right':[], 'up_idle':[], 'down_idle':[], 'left_idle':[], 'right_idle':[]}

		for animation in self.animations.keys():
			full_path = '../assets/player/' + animation
			self.animations[animation] = self.game.import_folder(full_path)

	def animate(self, state, animation_speed, anmimation_type):
		self.frame_index += animation_speed
		if anmimation_type == 'end' and self.frame_index >= len(self.animations[state])-1:
			self.frame_index = len(self.animations[state])-1
		else:
			self.frame_index = self.frame_index % len(self.animations[state])
		self.image = self.animations[state][int(self.frame_index)]

	def object_collisions(self, direction):
		
		for sprite in self.zone.collidable_sprites:
			if hasattr(sprite, 'hitbox'):
				if sprite.hitbox.colliderect(self.hitbox):
					
					if direction == 'x':
						if self.vel.x > 0:
							self.hitbox.right = sprite.hitbox.left
							self.acc.x = 0
							
						if self.vel.x < 0:
							self.hitbox.left = sprite.hitbox.right
							self.acc.x = 0

						self.rect.centerx = self.hitbox.centerx
						self.pos.x = self.hitbox.centerx
				
					if direction == 'y':			
						if self.vel.y > 0:
							self.hitbox.bottom = sprite.hitbox.top	
							self.acc.y = 0	
							
						if self.vel.y < 0:
							self.hitbox.top = sprite.hitbox.bottom
							self.acc.y = 0
						
						self.rect.centery = self.hitbox.centery
						self.pos.y = self.hitbox.centery

	def input(self):
		if not self.zone.cutscene_running:
			keys = pygame.key.get_pressed()

			if keys[pygame.K_RIGHT]:
				self.direction['right'] = True
			elif keys[pygame.K_LEFT]:
				self.direction['left'] = True

			if keys[pygame.K_DOWN]:
				self.direction['down'] = True
			elif keys[pygame.K_UP]:
				self.direction['up'] = True

		
	def physics(self, dt):
		
		# x direction
		self.acc.x += self.vel.x * self.friction
		self.vel.x += self.acc.x * dt
		self.pos.x += self.vel.x * dt + (0.5 * self.vel.x) * dt
		if abs(self.vel.x) < 0.05: self.vel.x = 0 
		self.hitbox.centerx = round(self.pos.x)
		self.rect.centerx = self.hitbox.centerx
		
		#y direction
		self.acc.y += self.vel.y * self.friction
		self.vel.y += self.acc.y * dt
		self.pos.y += self.vel.y * dt + (0.5 * self.vel.y * dt) * dt
		if abs(self.vel.y) < 0.05: self.vel.y = 0 
		self.hitbox.centery = round(self.pos.y)
		self.rect.centery = self.hitbox.centery
		
		# if self.vel.magnitude() > self.max_speed:
		# 	self.vel = self.vel.normalize() * self.max_speed


		if self.vel.magnitude() > self.max_speed:
			self.vel = self.vel.normalize() * self.max_speed

		if self.acc.magnitude() < 0.1:
			self.acc = pygame.math.Vector2()

	def state_logic(self):
		new_state = self.state.state_logic(self)
		if new_state is not None: self.state = new_state
		else: self.state

	def update(self, dt):
		self.state.update(dt, self)
		self.state_logic()

		for j, i in enumerate(self.direction.values()):
			print(j, i)
