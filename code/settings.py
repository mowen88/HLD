import pygame

FPS = 60
TILESIZE = 20
RES = WIDTH, HEIGHT = pygame.math.Vector2(480, 270)#(640, 360)#(960, 540) or... (512, 288)
HALF_WIDTH, HALF_HEIGHT = RES/2

FONT = '../fonts/Pokemon Classic.ttf'

LAYERS = {
	'BG0': 0,
	'BG1': 1,
	'BG2': 2,
	'Water': 3,
	'particles': 4,
	'NPCs': 5,
	'player':6,
	'weapons': 7,
	'blocks': 8,
	'explosions': 9,
	'foreground': 10
}

DATA = {
	'guns':{
			'blaster': {'ammo_type': None, 'bullet_type': 'projectile', 'cooldown': 10, 'speed': 4, 'damage': 50, 'path': '../assets/weapons/blaster.png'},
			'shotgun': {'ammo_type': 'shells', 'bullet_type': 'bullet', 'cooldown': 20, 'speed': 0, 'damage': 100, 'path': '../assets/weapons/shotgun.png'},
			'machine_gun': {'ammo_type': 'bullets', 'bullet_type': 'bullet', 'cooldown': 2, 'speed': 0, 'damage': 20, 'path': '../assets/weapons/machine_gun.png'},
			'grenade': {'ammo_type': 'grenades', 'bullet_type': 'grenade', 'cooldown': 40, 'speed': 4, 'damage': 250, 'path': '../assets/weapons/grenade.png'},
			'rocket_launcher': {'ammo_type': 'rockets', 'bullet_type': 'rocket', 'cooldown': 50, 'speed': 2, 'damage': 400, 'path': '../assets/weapons/rocket_launcher.png'},
			'railgun': {'ammo_type': 'slugs', 'bullet_type': 'beam', 'cooldown': 50, 'speed': 0, 'damage': 600, 'path': '../assets/weapons/railgun.png'},
			'hyper_blaster': {'ammo_type': 'cells', 'bullet_type': 'projectile', 'cooldown': 1, 'speed': 5, 'damage': 50, 'path': '../assets/weapons/hyper_blaster.png'},
			},
	'enemy_guns':{
			'guard': 'blaster',
			'sg_guard': 'shotgun',
			},
	'abilities':{
			'double_jump': True,
			'dash': False,
			'wall_jump': False,
			'hover': False,
			'ground_smash': False,
			},
		}

# key events
ACTIONS = {'escape': False, 'space': False, 'up': False, 'down': False, 'left': False,
			'right': False, 'return': False, 'backspace': False, 'left_click': False, 
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