import pygame
from settings import *
from state import State
from sprites import Collectible

class MapSprite(pygame.sprite.Sprite):
	def __init__(self, pos, name):
		self.name = name
		self.image = pygame.image.load(f'../assets/map_images/{self.name}.png').convert_alpha()
		self.rect = self.image.get_rect(center = pos)
		self.pos = pygame.math.Vector2(self.rect.center)

class Map(State):
	def __init__(self, game, zone):
		State.__init__(self, game)

		self.game = game
		self.zone = zone
		self.zone.cutscene_running = True
		self.offset = pygame.math.Vector2()

		self.alpha = 0
		self.max_alpha = 200
		self.fadeout = False

		self.map_surf = pygame.Surface((HALF_WIDTH * 1.5, HALF_HEIGHT * 1.5), pygame.SRCALPHA)
		self.map_rect = self.map_surf.get_rect(center = RES/2)

		self.map_bg_surf = self.map_surf.copy()
		self.map_bg_surf.fill(PURPLE)
		self.current_zone_pos = MAP_DATA[self.zone.name]['pos']

		self.marker = MapSprite((self.map_surf.get_width()/2, self.map_surf.get_height()/2), 'marker')
		
		#self.marker = MapSprite((self.map_surf.get_width()/2, self.map_surf.get_height()/2), (6, 6), 'marker')
		
		self.zone_sprites = self.get_zone_sprites()
		self.key_surf = pygame.image.load('../assets/collectibles/key/0.png').convert_alpha()
		self.key_rect = self.key_surf.get_rect(center = (self.map_rect.right -TILESIZE, self.map_rect.top + TILESIZE))

	def get_zone_sprites(self):
		zone_sprites = []
		for zone, data in MAP_DATA.items():
			if zone in COMPLETED_DATA['visited_zones']:
				sprite = MapSprite(data['pos'], zone)
				sprite.pos -= self.current_zone_pos - pygame.math.Vector2(self.map_surf.get_width()/2, self.map_surf.get_height()/2)
				if zone == self.zone.name:
					self.player_pos = sprite.pos
					self.player = MapSprite(self.player_pos, 'player')
				zone_sprites.append(sprite)
				
		return zone_sprites

	def draw_map(self, surf, screen):
		surf.fill(0)
		for zone in self.zone_sprites:
			if zone.name == self.zone.name:
				self.player_pos = zone.pos - (self.player.image.get_width()/2,self.player.image.get_height()/2)

			# if zone.rect.colliderect(self.marker.rect) and zone.name == self.zone.name:
			# 	zone.image.fill(PINK)
			# else:
			# 	zone.image.fill(WHITE)

			surf.blit(zone.image, zone.rect)

		surf.blit(self.player.image, self.player_pos)
		surf.blit(self.marker.image, self.marker.rect)

	
	def fade(self, dt):
		if not self.fadeout:
			self.alpha += 10 * dt
			if self.alpha >= self.max_alpha:
				self.alpha = self.max_alpha
		else:
			self.alpha -= 10 * dt
			if self.alpha <= 0:
				self.alpha = 0
				self.zone.cutscene_running = False
				self.exit_state()
				
	def scroll_logic(self, dt):

		keys = pygame.key.get_pressed()

		for zone in self.zone_sprites:
			if zone != self.marker:
				#if self.player.rect.centerx > self.map_rect.left:
				if keys[pygame.K_RIGHT]: self.offset.x = -1
				elif keys[pygame.K_LEFT]: self.offset.x = 1
				else: self.offset.x = 0
				if keys[pygame.K_DOWN]: self.offset.y = -1
				elif keys[pygame.K_UP]: self.offset.y = 1
				else: self.offset.y = 0	

				zone.pos += self.offset
				zone.rect.center = zone.pos

				if self.offset.magnitude() > 0: self.offset = self.offset.normalize()

	def update(self, dt):
		self.fade(dt)
		self.scroll_logic(dt)

		if ACTIONS['return']:
			self.fadeout = True

	def draw(self, screen):

		self.prev_state.draw(screen)
		
		# blit transparent purple map background
		screen.blit(self.map_bg_surf, self.map_rect)
		self.map_bg_surf.set_alpha(self.alpha)

		#blit map surface with details
		if self.alpha >= self.max_alpha:
			screen.blit(self.map_surf, self.map_rect)
			self.draw_map(self.map_surf, screen)

		# map text
		self.game.render_text('MAP', WHITE, self.game.small_font, (HALF_WIDTH, TILESIZE * 2))
		pygame.draw.rect(screen, WHITE, (self.map_rect.x -3, self.map_rect.y -3, self.map_rect.width + 6, self.map_rect.height + 6), 2)

		# draw the keys collected icon and number
		if len(COMPLETED_DATA['keys']) > 0:
			pygame.draw.rect(screen, BLACK, (self.key_rect.x -2, self.key_rect.y -2, self.key_rect.width + 4, self.key_rect.height + 4), border_radius=2)
			self.game.render_text('x' + str(len(COMPLETED_DATA['keys'])), WHITE, self.game.small_font, (self.key_rect.x - TILESIZE, TILESIZE * 2))
			screen.blit(self.key_surf, self.key_rect)
		
