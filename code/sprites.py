import pygame, random
from settings import *

class Collider(pygame.sprite.Sprite):
	def __init__(self, groups, rect, number):
		super().__init__(groups)

		#self.image = pygame.Surface((size))
		self.rect = pygame.Rect(rect)
		self.number = int(number)

class Bloom(pygame.sprite.Sprite):
	def __init__(self, zone, groups, pos, z, bloom_surf_path, colour):

		self.zone = zone
		self.image = pygame.Surface((self.zone.zone_size))
		self.z = z
		self.colour = colour
		self.rect = self.image.get_rect(topleft = pos)

		self.fog_surf = pygame.Surface((self.zone.zone_size))
		self.bloom_surf = pygame.image.load(bloom_surf_path).convert_alpha()
		self.bloom_rect = self.bloom_surf.get_rect()

	def draw(self, screen):
		self.fog_surf.fill(self.colour)
		self.bloom_rect.topleft = (0,0) - self.zone.rendered_sprites.offset
		self.fog_surf.blit(self.bloom_surf, self.bloom_rect)
		screen.blit(self.fog_surf, (0,0), special_flags = pygame.BLEND_MULT)

class FadeSurf(pygame.sprite.Sprite):
	def __init__(self, game, zone, groups, pos, alpha = 255, z = LAYERS['foreground']):
		super().__init__(groups)

		self.zone = zone
		self.game = game
		self.image = pygame.Surface((self.zone.zone_size))
		self.alpha = alpha
		self.loading_text = True
		self.timer = pygame.math.Vector2(self.zone.zone_size).magnitude()/10 # makes load time relative to zone size
		self.fade_duration = 5
		self.z = z
		self.rect = self.image.get_rect(topleft = pos)

	def update(self, dt):

		if self.zone.exiting:
			self.alpha += self.fade_duration * dt
			if self.alpha >= 255: 
				self.alpha = 255
				self.zone.exit_state()
				self.zone.create_zone(self.zone.new_zone)
			
		else:
			self.timer -= dt
			if self.timer <= 0:
				self.zone.entering = False
				self.loading_text = False
				self.alpha -= self.fade_duration * dt
				if self.alpha <= 0:
					self.alpha = 0

	def draw(self, screen):
		self.image.set_alpha(self.alpha)
		screen.blit(self.image, (0,0))

		if self.loading_text:
			self.game.render_text('Loading...', WHITE, self.game.small_font, (RES/2 * 1.75))


class Exit(pygame.sprite.Sprite):
	def __init__(self, groups, pos, size, name):
		super().__init__(groups)

		self.name = name
		self.size = size
		self.image = pygame.Surface((self.size))
		self.rect = self.image.get_rect(topleft = pos)

class Decoration(pygame.sprite.Sprite):
	def __init__(self, game, zone, groups, pos, z, surf = pygame.Surface((TILESIZE, TILESIZE))):
		super().__init__(groups)
		self.z = z
		self.image = surf
		self.rect = self.image.get_rect(topleft = pos)

class Object(pygame.sprite.Sprite):
	def __init__(self, game, zone, groups, pos, z, surf = pygame.Surface((TILESIZE, TILESIZE))):
		super().__init__(groups)

		self.zone = zone
		self.z = z
		self.image = surf
		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.copy().inflate(-self.rect.width *0.1, -self.rect.height *0.4)

class BG(Object):
	def __init__(self, game, zone, groups, pos, z, surf, parralax_value = (0, 0)):
		super().__init__(game, zone, groups, pos, z, surf)

		self.zone = zone
		self.image = surf
		self.parralax_value = pygame.math.Vector2(parralax_value)
		self.offset = self.zone.rendered_sprites.offset
		self.rect = self.image.get_rect(topleft = pos)	
		self.z = z
		self.hitbox = self.rect.copy().inflate(0,0)	
		self.old_hitbox = self.hitbox.copy()
		self.pos = pygame.math.Vector2(self.rect.topleft)

	# def update(self, dt):
	# 	self.rect.topleft = (0 - self.offset[0] * self.parralax_value.x, 0 - self.offset[1] * self.parralax_value.y)

class Cloud(BG):
	def __init__(self, game, zone, groups, pos, z, surf, speed):
		super().__init__(game, zone, groups, pos, z, surf)

		self.speed = speed
		self.vel = pygame.math.Vector2(self.speed)

	def update(self, dt):
		self.pos.x += self.vel.x * dt
		self.rect.topleft = self.pos

		if self.rect.x > self.zone.zone_size[0]:
			self.pos.x = -self.rect.width

class Void(Object):
	def __init__(self, game, zone, groups, pos, z, surf = pygame.Surface((TILESIZE, TILESIZE))):
		super().__init__(game, zone, groups, pos, z, surf)

		self.hitbox = self.rect.copy().inflate(-self.rect.width *0.4, -self.rect.height*0.2)

class Pillar(Object):
	def __init__(self, game, zone, groups, pos, z, surf, number):
		super().__init__(game, zone, groups, pos, z, surf)
		
		self.number = number
		self.hitbox = self.rect.copy().inflate(-self.rect.width *0.1, -self.rect.height *0.4)

class Tree(Object):
	def __init__(self, game, zone, groups, pos, z, surf):
		super().__init__(game, zone, groups, pos, z, surf)
		
		self.hitbox = self.rect.copy().inflate(-self.rect.width *0.05, -self.rect.height *0.3)

class Gun(Object):
	def __init__(self, game, zone, groups, pos, z, surf):
		super().__init__(game, zone, groups, pos, z, surf)

		self.zone = zone
		self.z = z
		self.original_image = surf
		self.image = self.original_image
		self.flipped_image = pygame.transform.flip(self.original_image, True, False)
		self.rect = self.image.get_rect(center = pos)
		self.angle = self.zone.get_distance_direction_and_angle(self.zone.player.hitbox.center, pygame.mouse.get_pos())[2]

	def rotate(self):
		self.angle = self.angle % 45
		self.angle = self.zone.get_distance_direction_and_angle(self.zone.player.hitbox.center, pygame.mouse.get_pos())[2]
		if self.angle >= 180: self.image = pygame.transform.rotate(self.flipped_image, -self.angle)
		else: self.image = pygame.transform.rotate(self.original_image, -self.angle)

	def update(self, dt):
		self.rotate()
		if 90 < self.angle < 270: self.rect = self.image.get_rect(center = (self.zone.player.rect.centerx, self.zone.player.rect.centery + 1))
		else: self.rect = self.image.get_rect(center = (self.zone.player.rect.centerx, self.zone.player.rect.centery - 1))

class AnimatedObject(pygame.sprite.Sprite):
	def __init__(self, game, zone, groups, pos, z, path):
		super().__init__(groups)

		self.game = game
		self.zone = zone
		self.z = z
		self.frames = self.game.get_folder_images(path)
		self.frame_index = 0
		self.image = self.frames[self.frame_index]
		self.rect = self.image.get_rect(center = pos)

		self.hitbox = self.rect.copy().inflate(0,0)
		self.alive = True

	def animate(self, animation_speed, loop=True):

		self.frame_index += animation_speed

		if loop:
			self.frame_index = self.frame_index % len(self.frames)	
		else:
			if self.frame_index > len(self.frames)-1:	
				self.frame_index = len(self.frames)-1

		
		self.image = self.frames[int(self.frame_index)]

	def update(self, dt):
		self.animate(0.2 * dt)

class Platform(AnimatedObject):
	def __init__(self, game, zone, groups, pos, z, path, number, duration):
		super().__init__(game, zone, groups, pos, z, path)

		self.number = number
		self.duration = duration
		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.copy().inflate(TILESIZE * 0.5, TILESIZE * 0.5)
		self.active = False
		self.timer = 0

	def update(self, dt):

		if self.active:

			if self.zone.player.hitbox.colliderect(self.rect):
				self.zone.player.on_platform = True

			self.timer += dt
			if self.timer > self.duration:
				self.timer = 0
				self.active = False

			self.frame_index += 0.2 * dt
			if self.frame_index >= len(self.frames) -1: 
				self.frame_index = len(self.frames) -1

				self.zone.void_sprites.remove(self)
				self.zone.rendered_sprites.add(self)
	
		else:
			self.frame_index -= 0.2 * dt
			if self.frame_index <= 0: 
				self.frame_index = 0

				if self.zone.player.hitbox.colliderect(self.hitbox):
					self.zone.player.on_platform = False
					self.zone.player.on_ground = False

				self.zone.void_sprites.add(self)
				self.zone.rendered_sprites.remove(self)

		self.image = self.frames[int(self.frame_index)]

class Door(AnimatedObject):
	def __init__(self, game, zone, groups, pos, z, path, number):
		super().__init__(game, zone, groups, pos, z, path)

		self.number = number

	def open(self, dt):
		if self.rect.colliderect(self.zone.player.rect):
			if len(COMPLETED_DATA['keys']) >= int(self.number):
				self.zone.block_sprites.remove(self)
				self.frame_index += 0.2 * dt
				if self.frame_index >= len(self.frames) -1: self.frame_index = len(self.frames) -1
				else: self.frame_index = self.frame_index % len(self.frames)	
		else:
			self.frame_index -= 0.2 * dt
			if self.frame_index <= 0: self.frame_index = 0
			else: self.frame_index = self.frame_index % len(self.frames)

		self.image = self.frames[int(self.frame_index)]
		if self.frame_index == len(self.frames) -1: self.zone.block_sprites.remove(self)
		else: self.zone.block_sprites.add(self)	

	def update(self, dt):
		self.open(dt)

class Barrier(AnimatedObject):
	def __init__(self, game, zone, groups, pos, z, path, number):
		super().__init__(game, zone, groups, pos, z, path)

		self.number = number
		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.2,-self.rect.height * 0.2)

	def open(self, dt):
		if not self.zone.locked_in or len(self.zone.enemy_sprites) == 0:
			self.frame_index += 0.15 * dt
			if self.frame_index >= len(self.frames) -1: 
				self.frame_index = len(self.frames) -1
			else: 
				self.frame_index = self.frame_index % len(self.frames)	
		else:
			self.frame_index -= 0.15 * dt
			if self.frame_index <= 0: self.frame_index = 0
			else: self.frame_index = self.frame_index % len(self.frames)
			self.z = LAYERS['player']

		self.image = self.frames[int(self.frame_index)]
		if self.frame_index > 0: 
			self.zone.block_sprites.remove(self)
			self.z = LAYERS['floor']
		else: 
			self.zone.block_sprites.add(self)
			self.z = LAYERS['player']	

	def update(self, dt):
		self.open(dt)


class Collectible(AnimatedObject):
	def __init__(self, game, zone, groups, pos, z, path, name):
		super().__init__(game, zone, groups, pos, z, path)

		self.name = name
		self.original_image = self.frames[self.frame_index]
		self.image = self.original_image
		self.pos = pos
		self.rotate = 0

	def animate(self, animation_speed):
		self.frame_index += animation_speed
		self.frame_index = self.frame_index % len(self.frames)
		self.original_image = self.frames[int(self.frame_index)]

	def rotation(self, dt):
		self.rotate -= 3 * dt
		self.rotate = self.rotate % 360

		self.image = pygame.transform.rotate(self.original_image, self.rotate)
		self.rect = self.image.get_rect(center = self.rect.center)

		self.hitbox.center = self.rect.center

	def update(self, dt):
		self.rotation(dt)
		self.animate(0.2 * dt)		

class Sword(AnimatedObject):
	def __init__(self, game, zone, groups, pos, z, path):
		super().__init__(game, zone, groups, pos, z, path)

		self.opposite_frames = self.game.get_folder_images(path +'_2')

	def animate(self, animation_speed):
		self.frame_index += animation_speed
		if self.frame_index >= len(self.frames)-1: 
			self.kill()
			self.zone.melee_sprite = None
		
		if self.zone.player.attack_count % 2 == 0: self.image = self.opposite_frames[int(self.frame_index)]
		else: self.image = self.frames[int(self.frame_index)]

	def update(self, dt):
		self.animate(0.25 * dt)

		if 45 < self.zone.player.angle < 135:
			self.image = pygame.transform.rotate(self.image, 270)
			self.rect = self.image.get_rect(midleft = self.zone.player.hitbox.center)
		elif 135 < self.zone.player.angle < 225:
			self.image = pygame.transform.rotate(self.image, 180)
			self.rect = self.image.get_rect(midtop = self.zone.player.hitbox.center)
		elif 225 < self.zone.player.angle < 315:
			self.image = pygame.transform.rotate(self.image, 90)
			self.rect = self.image.get_rect(midright = self.zone.player.hitbox.center)
		else:
			self.rect = self.image.get_rect(midbottom = self.zone.player.hitbox.center)

class Bullet(AnimatedObject):
	def __init__(self, game, zone, groups, pos, z, path):
		super().__init__(game, zone, groups, pos, z, path)

		self.speed = 5
		self.vel = self.zone.get_distance_direction_and_angle(self.rect.center, pygame.mouse.get_pos())[1] * self.speed
		self.vel = self.vel.rotate(random.randrange(-10, 10))
		self.pos = pygame.math.Vector2(self.rect.center)
		self.damage = GUN_DATA[self.zone.player.gun]['damage']

	def collide(self):
		for sprite in self.zone.block_sprites:
			if self.rect.colliderect(sprite.hitbox):
				self.kill()

	def update(self, dt):
		self.collide()
		self.animate(0.25 * dt)
		self.pos += self.vel * dt
		self.rect.center = self.pos

class ShotgunShell(Bullet):
	def __init__(self, game, zone, groups, pos, z, path):
		super().__init__(game, zone, groups, pos, z, path)

		self.speed = 7
		self.vel = self.zone.get_distance_direction_and_angle(self.rect.center, pygame.mouse.get_pos())[1] * self.speed
		self.vel = self.vel.rotate(random.randrange(-10, 10))
		self.pos = pygame.math.Vector2(self.rect.center)
		self.damage = GUN_DATA[self.zone.player.gun]['damage']
		self.size = 0

	def collide(self):
		hits = pygame.sprite.spritecollide(self, self.zone.block_sprites, False, pygame.sprite.collide_rect_ratio(0.6))
		if hits:
			self.kill()

	def disperse(self, dt):
		self.size += 5 * dt
		self.image = pygame.transform.scale(self.image, (self.size, self.size))
		self.rect = self.image.get_rect(center = self.pos)
		if self.size > TILESIZE * 3:
			self.kill()

	def update(self, dt):
		self.collide()
		self.animate(0.4 * dt)
		self.disperse(dt)
		self.pos += self.vel * dt
		self.rect.center = self.pos

class Grenade(AnimatedObject):
	def __init__(self, game, zone, groups, pos, z, path):
		super().__init__(game, zone, groups, pos, z, path)

		self.speed = 6
		self.vel = self.zone.get_distance_direction_and_angle(self.rect.center, pygame.mouse.get_pos())[1]
		self.pos = pygame.math.Vector2(self.rect.topleft)
		self.damage = 2
		self.knockback_power = 5
		self.falling = False
		self.old_rect = self.rect.copy()

	def grenade_falling(self):
		for sprite in self.zone.void_sprites:
			if sprite.hitbox.colliderect(self.rect):
				self.falling = True

	def collisions(self, direction):
		for sprite in self.zone.block_sprites:
			if sprite.hitbox.colliderect(self.rect) and not self.falling:
				if direction == 'x':
					if self.rect.right >= sprite.hitbox.left and self.old_rect.right <= sprite.hitbox.right:
						self.rect.right = sprite.hitbox.left
						self.pos.x = self.rect.x
						self.vel.x *= -1

					if self.rect.left <= sprite.hitbox.right and self.old_rect.left >= sprite.hitbox.right:
						self.rect.left = sprite.hitbox.right
						self.pos.x = self.rect.x
						self.vel.x *= -1

				if direction == 'y':
					if self.rect.bottom >= sprite.hitbox.top and self.old_rect.bottom <= sprite.hitbox.top:
						self.rect.bottom = sprite.hitbox.top
						self.pos.y = self.rect.y
						self.vel.y *= -1

					if self.rect.top <= sprite.hitbox.bottom and self.old_rect.top >= sprite.hitbox.bottom:
						self.rect.top = sprite.hitbox.bottom
						self.pos.y = self.rect.y
						self.vel.y *= -1

	def animate(self, animation_speed):
		self.frame_index += animation_speed
		self.image = self.frames[int(self.frame_index)]
		if self.frame_index >= len(self.frames) -1:
			self.zone.create_explosion(self.rect.center, self.damage, self.knockback_power)
			self.zone.screenshaking = True
			self.kill()

	def update(self, dt):
		self.old_rect = self.rect.copy()
		
		self.grenade_falling()
		if self.falling:
			self.z = LAYERS['BG2']
			self.vel.y += 0.5 * dt

		self.speed *= 0.95

		self.pos.x += self.vel.x * self.speed * dt
		self.rect.centerx = round(self.pos.x)
		self.collisions('x')
		self.pos.y += self.vel.y * self.speed * dt
		self.rect.centery = round(self.pos.y)
		self.collisions('y')

		
		self.animate(0.25 * dt)
		

class AttackableTerrain(AnimatedObject):
	def __init__(self, game, zone, groups, pos, z, path):
		super().__init__(game, zone, groups, pos, z, path)

		self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.5, -self.rect.height * 0.7)
		self.alive = True
		self.health = 1

	def animate(self, animation_speed):
		if self.alive:
			self.frame_index = 0
		else:
			self.frame_index += animation_speed
			if self.frame_index >= len(self.frames)-1: 
				self.frame_index = len(self.frames)-1
				self.z = LAYERS['particles']
			else: 
				self.frame_index = self.frame_index % len(self.frames)
			self.zone.attackable_sprites.remove(self)
			self.zone.block_sprites.remove(self)

		self.image = self.frames[int(self.frame_index)]

class Beam(AnimatedObject):
	def __init__(self, game, zone, groups, pos, z, path, fade_speed):
		super().__init__(game, zone, groups, pos, z, path)

		self.alpha = 255
		self.fade_speed = fade_speed
		self.damage = 3

	def animate(self, animation_speed):
		self.frame_index += animation_speed
		self.frame_index = self.frame_index % len(self.frames)
		self.image = self.frames[int(self.frame_index)]

	def update(self, dt):
		self.animate(0.2 * dt)
		self.alpha -= self.fade_speed * dt
		if self.alpha <= 0:
			self.kill()
		self.image.set_alpha(self.alpha)


			

			

		