import math
from settings import *
from NPCs import NPC
from enemy_fsm import Idle

class Grunt(NPC):
	def __init__(self, game, zone, groups, pos, z, name):
		super().__init__(game, zone, groups, pos, z, name)


