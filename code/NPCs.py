import math
from settings import *
from enemy_fsm import Idle

class NPC(pygame.sprite.Sprite):
	def __init__(self, game, zone, groups, pos, z, name):
		super().__init__(groups)
		self.game = game
		self.zone = zone
		self.z = z
		self.name = name

		self.state = Idle()
		self.alive = True
		self.animations = {'idle':[], 'telegraphing':[]}

		if self.name: self.import_imgs()
		self.animation_type = 'loop'
		self.frame_index = 0
		self.image = pygame.Surface((TILESIZE, TILESIZE))
		self.rect = self.image.get_rect(center = pos)
		self.pos = pygame.math.Vector2(self.rect.center)
		self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.6, -self.rect.height * 0.7)

		self.acc = pygame.math.Vector2()
		self.friction = -0.2
		self.vel = pygame.math.Vector2()

		self.dashing = False
		self.on_ground = True
		self.angle = 0

	def import_imgs(self):
		for animation in self.animations.keys():
			full_path = f'../assets/characters/{self.name}/' + animation
			self.animations[animation] = self.game.get_folder_images(full_path)

	def get_direction(self):
		if 45 < self.angle < 135: direction = 'right'
		elif 135 < self.angle < 225: direction = 'down'
		elif 225 < self.angle < 315: direction = 'left'
		else: direction = 'up'
		return direction

	def animate(self, state, animation_speed, anmimation_type):
		self.frame_index += animation_speed
		if anmimation_type == 'end' and self.frame_index >= len(self.animations[state])-1: self.frame_index = len(self.animations[state])-1
		else: self.frame_index = self.frame_index % len(self.animations[state])
		self.image = self.animations[state][int(self.frame_index)]

	def collisions(self, direction, group):
		hitlist = self.get_collide_list(group)
		for sprite in hitlist:
			if direction == 'x':
				if self.vel.x >= 0: self.hitbox.right = sprite.hitbox.left
				if self.vel.x <= 0: self.hitbox.left = sprite.hitbox.right
				self.rect.centerx = self.hitbox.centerx
				self.pos.x = self.hitbox.centerx
			if direction == 'y':			
				if self.vel.y >= 0: self.hitbox.bottom = sprite.hitbox.top	
				if self.vel.y <= 0: self.hitbox.top = sprite.hitbox.bottom
				self.rect.centery = self.hitbox.centery
				self.pos.y = self.hitbox.centery

	def get_collide_list(self, group): 
		hitlist = []
		for sprite in group:
			if sprite.hitbox.colliderect(self.hitbox): hitlist.append(sprite)
		return hitlist

	def physics(self, dt):
		
			# x direction
			self.acc.x += self.vel.x * self.friction
			self.vel.x += self.acc.x * dt
			self.pos.x += self.vel.x * dt + (0.5 * self.vel.x) * dt
			self.hitbox.centerx = round(self.pos.x)
			self.collisions('x', self.zone.block_sprites)
			if not self.dashing: self.collisions('x', self.zone.void_sprites)
			self.rect.centerx = self.hitbox.centerx
			
			#y direction
			self.acc.y += self.vel.y * self.friction
			self.vel.y += self.acc.y * dt
			self.pos.y += self.vel.y * dt + (0.5 * self.vel.y * dt) * dt
			self.hitbox.centery = round(self.pos.y)
			self.collisions('y', self.zone.block_sprites)
			if not self.dashing: self.collisions('y', self.zone.void_sprites)
			self.rect.centery = self.hitbox.centery


	def state_logic(self):
		new_state = self.state.state_logic(self)
		if new_state is not None: self.state = new_state
		else: self.state

	def update(self, dt):
		self.state_logic()
		self.state.update(dt, self)



		