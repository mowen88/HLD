from state import State
from settings import *

class Sequences:
	def __init__(self, cutscene):

		self.cutscene = cutscene
	
	def run(self, number):
		if number == 0:

			if self.cutscene.int_time == 120:
				self.cutscene.create_dialogue(self.cutscene.zone.fallen_soldier, 0, 80)
			elif self.cutscene.int_time == 350:
				self.cutscene.create_dialogue(self.cutscene.zone.fallen_soldier, 1, 80)
			elif self.cutscene.int_time == 500:
				self.cutscene.create_dialogue(self.cutscene.zone.fallen_soldier, 2, 80)
			elif self.cutscene.int_time == 700:
				self.cutscene.create_dialogue(self.cutscene.zone.fallen_soldier, 3, 100)
			elif self.cutscene.int_time == 900:
				self.cutscene.create_dialogue(self.cutscene.zone.fallen_soldier, 4, 100)
			elif self.cutscene.int_time == 1200:
				self.cutscene.create_dialogue(self.cutscene.zone.fallen_soldier, 5, 60)

			# whilst running
			if self.cutscene.timer < 100:
				self.cutscene.target = pygame.math.Vector2(self.cutscene.zone.target.rect.center)

			elif self.cutscene.timer < 1400:
				self.cutscene.target = pygame.math.Vector2(self.cutscene.zone.fallen_soldier.rect.center)

			else:
				self.cutscene.target = pygame.math.Vector2(self.cutscene.zone.target.rect.center)
				self.cutscene.opening = False

		elif number == 1:

			if self.cutscene.int_time == 120:
				self.cutscene.create_dialogue(self.cutscene.zone.vertus, 0, 60)
			elif self.cutscene.int_time == 300:
				self.cutscene.create_dialogue(self.cutscene.zone.scientist, 1, 80)
			elif self.cutscene.int_time == 500:
				self.cutscene.create_dialogue(self.cutscene.zone.scientist, 2, 80)

			if self.cutscene.timer < 100:
				self.cutscene.target = pygame.math.Vector2(self.cutscene.zone.target.rect.center)

			elif self.cutscene.timer < 300:
				self.cutscene.target = pygame.math.Vector2(self.cutscene.zone.vertus.rect.center)

			elif self.cutscene.timer < 500:
				self.cutscene.target = pygame.math.Vector2(self.cutscene.zone.scientist.rect.center)

			elif self.cutscene.timer < 800:
				self.cutscene.target = pygame.math.Vector2(self.cutscene.zone.scientist.rect.center)
			else:
				self.cutscene.target = pygame.math.Vector2(self.cutscene.zone.target.rect.center)
				self.cutscene.opening = False

		

