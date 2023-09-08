from state import State
from settings import *

class PauseMenu(State):
	def __init__(self, game):
		State.__init__(self, game)

	def update(self, dt):
		if ACTIONS['return']: 
			self.exit_state()
			self.game.reset_keys()

	def draw(self, screen):
		self.prev_state.draw(screen)

