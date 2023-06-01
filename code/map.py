import pygame
from settings import *
from state import State

class MapSprite(pygame.sprite.Sprite):
	def __init__(self, pos, size, name):
		self.name = name
		self.image = pygame.image.load(f'../assets/map_images/{self.name}.png').convert_alpha()
		self.rect = self.image.get_rect(center = pos)
		self.pos = pygame.math.Vector2(self.rect.center)

class Map(State):
	def __init__(self, game, zone):
		State.__init__(self, game)

		self.zone = zone
		self.offset = pygame.math.Vector2()

		self.map_surf = pygame.Surface((HALF_WIDTH * 1.5, HALF_HEIGHT * 1.5))
		self.map_surf.fill(GREY)
		self.map_rect = self.map_surf.get_rect(center = RES/2)

		self.current_zone_pos = MAP_DATA[self.zone.name]['pos']

		self.marker = MapSprite((self.map_surf.get_width()/2, self.map_surf.get_height()/2), (6, 6), 'marker')

		#self.marker.image.fill(WHITE)

		self.zone_sprites = self.get_zone_sprites()

	def get_zone_sprites(self):
		zone_sprites = []
		for zone, data in MAP_DATA.items():
			sprite = MapSprite(data['pos'], data['size'], zone)
			sprite.pos -= self.current_zone_pos - pygame.math.Vector2(self.map_surf.get_width()/2, self.map_surf.get_height()/2)
			zone_sprites.append(sprite)
		return zone_sprites

	def draw_map(self, surf):
		surf.fill(GREY)
		for zone in self.zone_sprites:
			# if zone.rect.colliderect(self.marker.rect) and zone.name == self.zone.name:
			# 	zone.image.fill(PINK)
			# else:
			# 	zone.image.fill(WHITE)
			surf.blit(zone.image, zone.rect)
		surf.blit(self.marker.image, self.marker.rect)
		self.marker.image.set_alpha(180)

	def update(self, dt):
		keys = pygame.key.get_pressed()

		for zone in self.zone_sprites:
			if zone != self.marker:

				if keys[pygame.K_RIGHT]:
					self.offset.x -= 0.1
				elif keys[pygame.K_LEFT]:
					self.offset.x += 0.1
				else:
					self.offset.x = 0
				if keys[pygame.K_DOWN]:
					self.offset.y -= 0.1
				elif keys[pygame.K_UP]:
					self.offset.y += 0.1
				else:
					self.offset.y = 0

				zone.pos += self.offset * dt
				zone.rect.center = zone.pos

				if self.offset.magnitude() > 0:
					self.offset = self.offset.normalize()

		if ACTIONS['return']: 
			self.exit_state()
			self.game.reset_keys()

	def draw(self, screen):
		self.prev_state.draw(screen)
		screen.blit(self.map_surf, self.map_rect)
		self.draw_map(self.map_surf)
		