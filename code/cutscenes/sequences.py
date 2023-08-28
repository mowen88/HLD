from state import State
from settings import *

class Sequences:
	def __init__(self, cutscene):

		self.cutscene = cutscene
	
	def run(self, number):
		if number == 0:

			if self.cutscene.int_time == 120:
				self.cutscene.create_dialogue(self.cutscene.zone.warrior, 0, 60)
			elif self.cutscene.int_time == 300:
				self.cutscene.create_dialogue(self.cutscene.zone.player, 1, 100)

			if self.cutscene.timer < 100:
				self.cutscene.target = pygame.math.Vector2(self.cutscene.zone.target.rect.center)

			elif self.cutscene.timer < 300:
				self.cutscene.target = pygame.math.Vector2(self.cutscene.zone.warrior.rect.center)

			elif self.cutscene.timer < 600:
				self.cutscene.target = pygame.math.Vector2(self.cutscene.zone.target.rect.center)
			else:
				self.cutscene.target = pygame.math.Vector2(self.cutscene.zone.target.rect.center)
				self.cutscene.opening = False

