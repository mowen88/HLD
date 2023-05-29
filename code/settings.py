import pygame

FPS = 60
TILESIZE = 16
RES = WIDTH, HEIGHT = pygame.math.Vector2(320, 180)#(360, 202.5)#(480, 270)#(640, 360)#(960, 540) or... (512, 288)
HALF_WIDTH, HALF_HEIGHT = RES/2

FONT = '../fonts/Pokemon Classic.ttf'

PLAYER_DATA = {'max_health': 6, 'max_bullets': 6}

ENEMY_DATA = {
	'grunt':{'speed': 0.1, 'lunge_speed': 2, 'knockback_speed': 1, 'damage': 1, 'health': 3, 'telegraphing_time': 30, 'attack_radius': 30, 'pursue_radius': 90},
	'hound':{'speed': 0.2, 'lunge_speed': 3, 'knockback_speed': 2, 'damage': 1, 'health': 2, 'telegraphing_time': 15, 'attack_radius': 60, 'pursue_radius': 90}
}

ZONE_DATA = {
	'garden':{'1': 'dungeon', '2': 'dungeon'},
	'dungeon':{'1':'garden', '2':'garden'},
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
	'foreground': 10
}

# key events
ACTIONS = {'escape': False, 'space': False, 'up': False, 'down': False, 'left': False,
			'right': False, 'return': False, 'right_ctrl': False, 'backspace': False, 'left_click': False, 
			'right_click': False, 'scroll_up': False, 'scroll_down': False}

# game colours
BLACK = ((9, 9, 14))
GREY = ((91,83,145))
LIGHT_GREY = ((146, 143, 184))
WHITE = ((255, 255, 255)) 
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