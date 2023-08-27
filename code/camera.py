import pygame, math, random
from settings import *

class Camera(pygame.sprite.Group):
	def __init__(self, game, zone):
		super().__init__()

		self.game = game
		self.zone = zone
		self.offset = pygame.math.Vector2()

		self.BG0 = pygame.image.load(f'../zones/{self.zone.name}/bg.png').convert_alpha()

	# 	# fog variables
	# 	self.dark = True
	# 	self.main_fog = self.get_fog_image(YELLOW, (self.zone.zone_size), self.zone.zone_size)

	# def get_fog_image(self, colour, circle_size, canvas_size):
	# 	self.fog_colour = colour
	# 	self.fog_surf = pygame.Surface((canvas_size))
	# 	self.light_mask = pygame.image.load(f'../zones/{self.zone.name}/2x6_white.png').convert_alpha()
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
			if self.zone.screenshake_timer < 120: 
				self.offset += [random.randint(-1, 1), random.randint(-1, 1)]
			else: 
				self.zone.screenshaking = False
				self.zone.screenshake_timer = 0

	def midpoint(self, p1, p2):
		return ((p1.x + p2.x)/4, (p1.x + p2.y)/4)

	def offset_draw(self, screen, target):
		
		# draw parralax backgrounds
		screen.fill(LIGHT_GREY)
		screen.blit(self.BG0, (0 - self.offset[0] * 0.2, 0 - self.offset[1] * 0.2))

		distance = self.zone.get_distance_direction_and_angle(pygame.mouse.get_pos() - self.offset, target)[0]
		scroll = pygame.math.Vector2(target) + pygame.math.Vector2(pygame.mouse.get_pos())
		midpoint = self.midpoint(pygame.math.Vector2(target - self.offset), pygame.math.Vector2(pygame.mouse.get_pos()))

		if self.zone.cutscene_running:
			self.offset.x += (target[0] - HALF_WIDTH - self.offset.x)/200
			self.offset.y += (target[1] - HALF_HEIGHT - self.offset.y)/200
		else:
			self.offset.x += (target[0] - HALF_WIDTH - (HALF_WIDTH - pygame.mouse.get_pos()[0])/4 - self.offset.x)/80
			self.offset.y += (target[1] - HALF_HEIGHT - (HALF_HEIGHT - pygame.mouse.get_pos()[1])/4 - self.offset.y)/80

		#self.offset += (midpoint - RES - self.offset)/(distance/5)

		#self.offset += self.self.zone.get_distance_direction_and_angle(pygame.math.Vector2(target.rect.center), pygame.math.Vector2(pygame.mouse.get_pos()))[1]
	
		#limit offset to stop at edges
		if self.offset[0] <= 0: self.offset[0] = 0
		elif self.offset[0] >= self.zone.zone_size[0] - WIDTH: self.offset[0] = self.zone.zone_size[0] - WIDTH
		if self.offset[1] <= 0: self.offset[1] = 0
		elif self.offset[1] >= self.zone.zone_size[1] - HEIGHT: self.offset[1] = self.zone.zone_size[1] - HEIGHT

		self.screenshake()

		for layer in LAYERS.values():
			for sprite in sorted(self.zone.rendered_sprites, key = lambda sprite: sprite.rect.centery):
				if sprite.z == layer:
					offset = sprite.rect.topleft - self.offset
					screen.blit(sprite.image, offset)

		# if self.dark:
		# 	self.render_fog(self.game.screen, (0 - self.offset[0] * 0.5, 0 - self.offset[1] * 0.5))