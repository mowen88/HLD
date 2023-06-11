import pygame

FPS = 60
TILESIZE = 16
RES = WIDTH, HEIGHT = pygame.math.Vector2(320, 180)#(360, 202.5)#(480, 270)#(640, 360)#(960, 540) or... (512, 288)
HALF_WIDTH, HALF_HEIGHT = RES/2

FONT = '../fonts/Pokemon Classic.ttf'

# data that is dynamic and changes throughout play

PLAYER_DATA = {'current_zone': 'start', 'entry_pos': '0', 'keys': ['blue_door'], 'gun_index': 0, 'max_health': 4, 'max_juice': 99, 'heal_cost': 11, 'partial_healths': 0}

COMPLETED_DATA = {'visited_zones': [], 'health': [], 'juice': []}

GUN_DATA = {
	'pistol':{'cost': 11, 'damage': 1, 'cooldown': 20, 'knockback': 1},
	'railgun':{'cost': 33, 'damage': 2, 'cooldown': 50, 'knockback': 2}
}

ENEMY_DATA = {
	'grunt':{'speed': 0.1, 'lunge_speed': 2, 'knockback_speed': 1, 'damage': 1, 'health': 3, 'telegraphing_time': 20, 'attack_radius': 30, 'pursue_radius': 110},
	'hound':{'speed': 0.2, 'lunge_speed': 3, 'knockback_speed': 2, 'damage': 1, 'health': 2, 'telegraphing_time': 15, 'attack_radius': 60, 'pursue_radius': 90}
}
# entry and exit data for zones, does not change
ZONE_DATA = {
	'start':{'1': 'garden', '2': 'dungeon', '3':'datacentre'},
	'garden':{'1': 'start', '2': 'dungeon', '3':'datacentre'},
	'dungeon':{'1':'garden', '2':'garden'},
	'datacentre':{'1':'garden', '2':'garden', '3':'garden'},
}
MAP_DATA = {
	'start':{'pos': (-20,-20)},
	'garden':{'pos': (30,10)},
	'dungeon':{'pos': (60,20)},
	'datacentre':{'pos': (0,20)},
}

LAYERS = {
	'BG0': 0,
	'BG1': 1,
	'BG2': 2,
	'floor': 3,
	'particles': 4,
	'NPCs': 5,
	'player':6,
	'weapons': 7,
	'blocks': 8,
	'explosions': 9,
	'foreground': 10,
	'ui': 11
}

# key events
ACTIONS = {'escape': False, 'space': False, 'up': False, 'down': False, 'left': False,
			'right': False, 'return': False, 'right_shift': False, 'backspace': False, 'left_click': False, 
			'right_click': False, 'scroll_up': False, 'scroll_down': False}

# game colours
BLACK = ((20, 14, 30))
GREY = ((91,83,145))
LIGHT_GREY = ((146, 143, 184))
WHITE = ((223, 234, 228)) 
BLUE = ((20, 68, 145))
LIGHT_BLUE = ((113, 181, 219))
RED = ((112, 21, 31))
ORANGE = ((227, 133, 36))
PINK = ((195, 67, 92))
GREEN = ((88, 179, 150))
LIGHT_GREEN = ((106, 226, 145))
PURPLE = ((66, 0, 78))
CYAN = ((0, 255, 255))
MAGENTA = ((153, 60, 139))
YELLOW = ((224, 225, 146))