import pygame
from settings import *
from state import State
from sprites import AnimatedObject

class CollectionCutscene(State):
	def __init__(self, game, zone, overlay_animation):
		State.__init__(self, game)

		
		self.zone = zone
		self.overlay_animation = overlay_animation

		self.alpha = 0
		self.max_alpha = 255
		self.fadeout = False

		self.frames = self.game.get_folder_images(self.overlay_animation)
		self.frame_index = 0
		self.image = self.frames[self.frame_index]
		self.rect = self.image.get_rect(center = RES/2)

	def animate(self, animation_speed):
		self.frame_index += animation_speed
		
		if self.frame_index >= len(self.frames) -1: 
			self.frame_index = len(self.frames) -1
			self.fadeout = True
		else:
			self.frame_index = self.frame_index % len(self.frames)	

		self.image = self.frames[int(self.frame_index)]

	def fade(self, dt):
		if not self.fadeout:
			self.alpha += 10 * dt
			if self.alpha >= self.max_alpha:
				self.alpha = self.max_alpha
		else:
			self.alpha -= 10 * dt
			if self.alpha <= 0:
				self.alpha = 0
				self.exit_state()	

	def update(self, dt):
		self.fade(dt)
		self.animate(0.2 * dt)

	def draw(self, screen):
		self.prev_state.draw(screen)
		screen.blit(self.image, self.rect)
		self.image.set_alpha(self.alpha)