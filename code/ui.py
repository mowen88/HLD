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
		
	def add_health(self):
		PLAYER_DATA['partial_healths'] += 1
		if PLAYER_DATA['partial_healths'] > 3:
			PLAYER_DATA['partial_healths'] = 0
			PLAYER_DATA['max_health'] += 1 
			self.game.current_health = PLAYER_DATA['max_health']
			return

	def draw(self, screen):
		self.health_display(screen)
		self.flash_icon()
		
