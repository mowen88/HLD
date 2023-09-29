import math
from settings import *
from entities.npc_fsm import Idle

class NPC(pygame.sprite.Sprite):
	def __init__(self, game, zone, groups, pos, z, name):
		super().__init__(groups)
		self.game = game
		self.zone = zone
		self.z = z
		self.name = name

		self.state = Idle('idle')
		self.invincible = False
		self.invincibility_timer = 0
		self.invincile_time = 6
		self.knocked_back = False
		self.knockback_direction = (0,0)
		self.knockback_speed = 2
		self.alive = True
		self.animations = {'idle':[], 'run':[], 'telegraphing':[], 'death':[], 'attack':[], 'fall':[]}

		if self.name: self.import_imgs()
		self.animation_type = 'loop'
		self.frame_index = 0
		self.image = pygame.Surface((24, 24))
		
		self.mask = pygame.mask.from_surface(self.image)
		self.mask_image = self.mask.to_surface()
		self.mask_image.set_colorkey((0, 0, 0))

		self.rect = self.image.get_rect(center = pos)
		self.pos = pygame.math.Vector2(self.rect.center)
		self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.5, -self.rect.height * 0.7)

		self.acc = pygame.math.Vector2()
		self.friction = -0.15
		self.vel = pygame.math.Vector2()
		self.speed = 0.6


		self.dashing = False
		self.on_ground = True
		self.on_platform = False
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

	def animate(self, state, animation_speed, loop=True):
		self.frame_index += animation_speed

		if not loop and self.frame_index >= len(self.animations[state])-1: 
			self.frame_index = len(self.animations[state])-1
		else: 
			self.frame_index = self.frame_index % len(self.animations[state])

		self.image = self.animations[state][int(self.frame_index)]


		self.mask = pygame.mask.from_surface(self.image)
		self.mask_image = self.mask.to_surface()
		self.mask_image.set_colorkey((0, 0, 0))

		if self.invincible: 
			self.image = self.mask_image
			self.vel = pygame.math.Vector2()

	def explosion_damage_logic(self):
		hits = pygame.sprite.spritecollide(self, self.zone.explosion_sprites, False, pygame.sprite.collide_circle_ratio(0.8))
		if not self.invincible and self.alive:
			for sprite in self.zone.explosion_sprites:
				if hits and sprite.frame_index < 1:
					self.health -= sprite.damage
					self.invincible = True
					self.get_knockback(sprite)
					if self.health <= 0:
						self.alive = False
						self.invincible = False
						self.zone.enemy_sprites.remove(self)
						if self in self.zone.boss_sprites:
							COMPLETED_DATA['bosses_defeated'].append(self.name)

	def get_knockback(self, other_sprite):
		self.knocked_back = True
		self.knockback_direction = other_sprite.rect.center

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
		self.rect.centerx = self.hitbox.centerx
		self.collisions('x', self.zone.block_sprites)
		#if self == self.zone.player: self.collisions('x', self.zone.enemy_sprites)
		#if self in self.zone.enemy_sprites: self.collisions('x', [self.zone.player])
		if not self.dashing: self.collisions('x', self.zone.void_sprites)
		
		#y direction
		self.acc.y += self.vel.y * self.friction
		self.vel.y += self.acc.y * dt
		self.pos.y += self.vel.y * dt + (0.5 * self.vel.y) * dt
		self.hitbox.centery = round(self.pos.y)
		self.rect.centery = self.hitbox.centery
		self.collisions('y', self.zone.block_sprites)
		#if self == self.zone.player: self.collisions('y', self.zone.enemy_sprites)
		#if self in self.zone.enemy_sprites: self.collisions('y', [self.zone.player])
		if not self.dashing: self.collisions('y', self.zone.void_sprites)
		
		if self == self.zone.player: 
			if self.vel.magnitude() >= self.speed: 
				self.vel = self.vel.normalize() * self.speed

	def invincibility(self, dt):
		if self.invincible:
			self.invincibility_timer += dt
			if self.invincibility_timer >= self.invincile_time:
				self.invincible = False
				self.invincibility_timer = 0

	def state_logic(self):
		new_state = self.state.state_logic(self)
		if new_state: self.state = new_state
		else: self.state

	def update(self, dt):
		self.state_logic()
		self.state.update(dt, self)

class Warrior(NPC):
	def __init__(self, game, zone, groups, pos, z, name):
		super().__init__(game, zone, groups, pos, z, name)

		self.mask = pygame.mask.from_surface(self.image)
		self.mask_image = self.mask.to_surface()
		self.mask_image.set_colorkey((0, 0, 0))

	def update(self, dt):
		self.animate('idle', 0.4 * dt, 'loop')

class Mercenary(NPC):
	def __init__(self, game, zone, groups, pos, z, name):
		super().__init__(game, zone, groups, pos, z, name)

		self.mask = pygame.mask.from_surface(self.image)
		self.mask_image = self.mask.to_surface()
		self.mask_image.set_colorkey((0, 0, 0))

	def update(self, dt):
		self.animate('idle', 0.2 * dt, 'loop')

