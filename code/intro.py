from state import State
from zone import Zone
from settings import *

class Intro(State):
	def __init__(self, game):
		State.__init__(self, game)

	def update(self, dt):
		if ACTIONS['return']: Zone(self.game, 'dungeon', '0').enter_state()
		self.game.reset_keys()

	def draw(self, screen):
		screen.fill(GREY)

