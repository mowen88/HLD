import pygame
from settings import *

class UI:
	def __init__(self, game, zone):

		self.game = game
		self.zone = zone
		
		self.filled_health_icon = pygame.image.load('../assets/ui_images/filled_health_icon.png').convert_alpha()
		self.blank_health_icon = pygame.image.load('../assets/ui_images/blank_health_icon.png').convert_alpha()
		self.partial_icons = self.game.get_folder_images('../assets/ui_images/partial_health_icons')

		self.mask = pygame.mask.from_surface(self.blank_health_icon)
		self.mask_image = self.mask.to_surface()
		self.mask_image.set_colorkey((0, 0, 0))
		self.alpha = 255

		self.offset = 13
		self.padding = 8
		self.box_list = []
		self.gun_icon_size = [0, 0]

		self.gun_surf = pygame.image.load(f'../assets/ui_images/{self.zone.player.gun}.png').convert_alpha()
		self.gun_rect = self.gun_surf.get_rect(center = (self.offset + 5, self.padding + 28))

		self.gun_flash_surf = pygame.Surface((self.gun_icon_size))
		self.gun_flash_surf.fill(WHITE)
		self.gun_flash_rect = self.gun_flash_surf.get_rect(center = (self.gun_rect.center))

		self.juice_bar_length = 47
		self.juice_bar_ratio = PLAYER_DATA['max_juice'] / self.juice_bar_length
		

	def health_display(self, screen):
		
		for box in range(PLAYER_DATA['max_health'] + 1):
			if box < PLAYER_DATA['max_health']:
				box *= self.offset
				self.box_list.append(box)
				screen.blit(self.blank_health_icon, (self.padding + box, self.padding))
				for box in range(self.game.current_health):
					box *= self.offset
					screen.blit(self.filled_health_icon, (self.padding + box, self.padding))
			
			else:
				box *= self.offset
				screen.blit(self.partial_icons[PLAYER_DATA['partial_healths']], (self.padding + box, self.padding))

			if box == self.game.current_health:
				box *= self.offset
				
	def flash_icon(self):
		if self.zone.player.invincible:
			self.game.screen.blit(self.mask_image, (self.padding + self.box_list[self.game.current_health], self.padding))
			return

	def flash_gun(self):
		if self.zone.player.changing_weapon:
			self.game.screen.blit(self.gun_flash_surf, self.gun_flash_rect)
			self.gun_flash_surf.fill(WHITE)
			self.gun_flash_surf = pygame.transform.scale(self.gun_flash_surf, (self.gun_icon_size))
			self.gun_flash_rect = self.gun_flash_surf.get_rect(center = self.gun_rect.center)
			
			self.gun_flash_surf.set_alpha(self.alpha)
			if self.alpha <= 0:
				self.zone.player.changing_weapon = False
				self.alpha = 255
				self.gun_icon_size = [0,0]

	def gun_icon(self, screen):
		self.gun_surf = pygame.image.load(f'../assets/ui_images/{self.zone.player.gun}.png').convert_alpha()
		screen.blit(self.gun_surf, self.gun_rect)
		return

	def show_juice(self, screen):
		pygame.draw.rect(screen, BLACK, (8,22, PLAYER_DATA['max_juice'] / self.juice_bar_ratio + 4, 6), border_radius = 2)
		pygame.draw.rect(screen, WHITE, (10,24, self.game.current_juice / self.juice_bar_ratio, 2))
		
	def add_health(self):
		PLAYER_DATA['partial_healths'] += 1
		if PLAYER_DATA['partial_healths'] > 3:
			PLAYER_DATA['partial_healths'] = 0
			PLAYER_DATA['max_health'] += 1 
			self.game.current_health = PLAYER_DATA['max_health']
			return
	
	def update(self, dt):
		if self.zone.player.changing_weapon:
			self.alpha -= 12 * dt
			self.gun_icon_size[0] += 4 * dt
			self.gun_icon_size[1] += 4 * dt

		# if ACTIONS['up']:
		# 	self.game.reset_keys()
		# 	self.zone.add_subtract_juice(11, 'add')
		# if ACTIONS['down']:
		# 	self.game.reset_keys()
		# 	self.zone.add_subtract_juice(11, 'sub')

			
	
	def draw(self, screen):
		self.health_display(screen)
		self.flash_icon()
		self.gun_icon(screen)
		self.show_juice(screen)
		self.flash_gun()
		

		
