import pygame, math, random
from settings import *

class Camera(pygame.sprite.Group):
	def __init__(self, game, zone):
		super().__init__()

		self.game = game
		self.zone = zone
		self.offset = pygame.math.Vector2()
		self.camera_lag = 80

		# # fog variables
		# self.dark = True
		# self.main_fog = self.get_fog_image((255, 65, 125), (100,100), self.zone.zone_size)

	# def get_fog_image(self, colour, circle_size, canvas_size):
	# 	self.fog_colour = colour
	# 	self.fog_surf = pygame.Surface((canvas_size))
	# 	self.light_mask = pygame.image.load(f'../zones/{self.zone.name}/white.png').convert_alpha()
	# 	self.light_mask = pygame.transform.scale(self.light_mask, (circle_size))
	# 	self.light_rect = self.light_mask.get_rect()

	# def render_fog(self, screen, target):
	# 	self.fog_surf.fill(self.fog_colour)
	# 	self.light_rect.center = target
	# 	self.fog_surf.blit(self.light_mask, self.light_rect)
	# 	screen.blit(self.fog_surf, (0,0), special_flags = pygame.BLEND_MULT)

	def screenshake(self):
		if self.zone.screenshaking:
			self.zone.screenshake_timer += 1
			if self.zone.screenshake_timer < 30: 
				self.offset += [random.randint(-1, 1), random.randint(-1, 1)]
			else: 
				self.zone.screenshaking = False
				self.zone.screenshake_timer = 0

	def move_to(self, point):
		self.offset.y += (point[1] - self.offset.y)/self.camera_lag
		if self.offset.y < point[1]:
			self.offset.y = point[1]

	def offset_draw(self, screen, target):
		
		screen.fill(ZONE_DATA[self.zone.name]['bg_colour'])

		if target[1] < 190 and self.zone.name == 'scene_2':
			self.camera_lag = 80
			self.move_to([0,-HALF_WIDTH])

		elif target[1] < 250 and self.zone.name == 'pool':
			self.camera_lag = 80
			self.move_to([0,0])

		elif self.zone.cutscene_running or self.zone.target.dashing:
			self.camera_lag = 50
		else:
			self.camera_lag = 20

		if self.zone.cutscene_running:
			self.offset.x += (target[0] - HALF_WIDTH - self.offset.x)/self.camera_lag
			self.offset.y += (target[1] - HALF_HEIGHT - self.offset.y)/self.camera_lag
		else:
			self.offset.x += (target[0] - HALF_WIDTH - (HALF_WIDTH - pygame.mouse.get_pos()[0])/4 - self.offset.x)/self.camera_lag
			self.offset.y += (target[1] - HALF_HEIGHT - (HALF_HEIGHT - pygame.mouse.get_pos()[1])/4 - self.offset.y)/self.camera_lag

		#self.offset += (midpoint - RES - self.offset)/(distance/5)

		#self.offset += self.self.zone.get_distance_direction_and_angle(pygame.math.Vector2(target.rect.center), pygame.math.Vector2(pygame.mouse.get_pos()))[1]
	
		#limit offset to stop at edges
		if self.offset[0] < 0: self.offset[0] = 0
		elif self.offset[0] > self.zone.zone_size[0] - WIDTH: self.offset[0] = self.zone.zone_size[0] - WIDTH
		if self.offset[1] < 0: self.offset[1] = 0
		elif self.offset[1] > self.zone.zone_size[1] - HEIGHT: self.offset[1] = self.zone.zone_size[1] - HEIGHT

		self.screenshake()

		for layer in LAYERS.values():
			for sprite in sorted(self.zone.rendered_sprites, key = lambda sprite: sprite.rect.centery):
				if sprite.z == layer:
					offset = sprite.rect.topleft - self.offset
					screen.blit(sprite.image, (offset))

		# screen.blit(self.light_mask, (260 - self.offset[0], 330 - self.offset[1]))
		# # if self.dark:
		# # 	self.render_fog(self.game.screen, (320 - self.offset[0], 320 - self.offset[1]))