import pygame
from settings import *

# 1. create icons for health - blanks and filled slots
# 2. create partial icons in image folder i.e. 1, 2, 3, 4
# 3. append partial image icon to end of health display (0 being black image, so therefore will only show when start collecting..)
# 4. when 4 are collected - reset partial chips to 0 in PLAYER_DATA

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

	def health_display(self, screen):
		offset = 13
		padding = 8
		for box in range(PLAYER_DATA['max_health'] + 1):
			if box < PLAYER_DATA['max_health']:
				box *= offset
				screen.blit(self.blank_health_icon, (padding + box, padding))
				for box in range(self.game.current_health):
					box *= offset
					screen.blit(self.filled_health_icon, (padding + box, padding))
					#screen.blit(self.mask_image, (padding + box, padding))
			elif PLAYER_DATA['partial_healths'] > 0:
				box *= offset
				screen.blit(self.partial_icons[PLAYER_DATA['partial_healths']], (padding + box, padding))
				
	def logic(self):
		PLAYER_DATA['partial_healths'] += 1
		if PLAYER_DATA['partial_healths'] >= 3:
			PLAYER_DATA['partial_healths'] = 0
			PLAYER_DATA['max_health'] += 1 
			self.game.current_health += 1
			return

	def update(self, dt):
		self.alpha -= 2 * dt
		if self.alpha <= 0: self.alpha = 0

	def draw(self, screen):
		self.mask_image.set_alpha(self.alpha)
		self.health_display(screen)

