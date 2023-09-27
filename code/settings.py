import pygame

FPS = 60
TILESIZE = 16
RES = WIDTH, HEIGHT = pygame.math.Vector2(320, 180)#(384, 216)#(512, 288)#(320, 180)#(480, 270)#(640, 360)#(960, 540)#(512, 288)
HALF_WIDTH, HALF_HEIGHT = RES/2

#FONT = '../fonts/Pokemon Classic.ttf'
#FONT = '../fonts/Typori-Regular.ttf'
FONT = '../fonts/homespun.ttf'

# game colours
BLACK = ((20, 14, 30))
GREY = ((91,83,145))
LIGHT_GREY = ((146, 143, 184))
WHITE = ((250, 255, 255)) 
BLUE = ((20, 68, 145))
LIGHT_BLUE = ((113, 181, 219))
RED = ((156, 50, 71))
ORANGE = ((227, 133, 36))
PINK = ((255, 65, 125))
GREEN = ((88, 179, 150))
LIGHT_GREEN = ((106, 226, 145))
PURPLE = ((57, 41, 70))
CYAN = ((0, 255, 255))
MAGENTA = ((153, 60, 139))
YELLOW = ((224, 225, 146))

# data that is dynamic and changes throughout play
PLAYER_DATA = {'current_zone': 'crashsite',
				'current_gun': 'nogun',
 				'entry_pos': '0', 
 				'keys': [],
 				'gun_index': 0, 
 				'max_health': 4,
 				'max_juice': 99,
 				'heal_cost': 11,
 				'partial_healths': 0,
 				'time': 0}

COMPLETED_DATA = {'cutscenes': [],
				  'visited_zones': [],
				  'guns': [],
				  'health': [],
				  'juice': [],
				  'keys':[],
				  'bosses_defeated':[]}

GUN_DATA = {
	'nogun':{'cost': 0, 'damage': 0, 'cooldown': 0, 'knockback': 0},
	'pistol':{'cost': 11, 'damage': 1, 'cooldown': 10, 'knockback': 1},
	'railgun':{'cost': 33, 'damage': 4, 'cooldown': 100, 'knockback': 2},
	'shotgun':{'cost': 22, 'damage': 5, 'cooldown': 60, 'knockback': 1.5},
}

ENEMY_DATA = {
	'grunt':{'speed': 0.1, 'lunge_speed': 2,'damage': 1, 'health': 3, 'telegraphing_time': 40, 'attack_radius': 30, 'pursue_radius': 110},
	'hound':{'speed': 0.2, 'lunge_speed': 3, 'damage': 1, 'health': 2, 'telegraphing_time': 15, 'attack_radius': 60, 'pursue_radius': 90},
	'musketeer':{'speed': 0.05, 'lunge_speed': 1, 'damage': 1, 'health': 2, 'telegraphing_time': 60, 'attack_radius': 90, 'pursue_radius': 120},
	 #bosses
	'boss1':{'colour': YELLOW, 'speed': 0.1, 'lunge_speed': 2, 'damage': 1, 'health': 15, 'telegraphing_time': 40, 'attack_radius': 50, 'pursue_radius': 120}
}
# entry and exit data for zones, does not change
ZONE_DATA = {
	'garden':{'bg_colour': PINK, '1': 'boss_room_1', '2': 'first_dungeon', '3':'datacentre'},
	'dungeon':{'bg_colour': BLACK,'1':'garden', '2':'garden'},
	'datacentre':{'bg_colour': GREEN,'1':'garden', '2':'garden', '3':'garden'},
	# actual levels start here !!!
	'crashsite':{'bg_colour': LIGHT_GREEN,'1':'garden', '2':'dungeon', '3':'scene_2'},
	'scene_2':{'bg_colour': LIGHT_GREEN,'1':'garden', '2':'first_dungeon', '3':'crashsite'},
	'first_dungeon':{'bg_colour': BLACK, '1': 'dungeon_exit', '2': 'scene_2', '3':'datacentre'},
	'dungeon_exit':{'bg_colour': BLACK, '1': 'first_dungeon', '2': 'pool', '3':'radio_shack'},
	'radio_shack':{'bg_colour': BLACK, '1': 'first_dungeon', '2': 'pool', '3':'dungeon_exit'},
	'pool':{'bg_colour': BLACK, '1': 'apothecary', '2': 'dungeon_exit', '3':'crashsite'},
	
	'boss_room_1':{'bg_colour': YELLOW, '1': 'garden', '2': 'dungeon', '3':'garden'}
}
MAP_DATA = {
	'first_dungeon':{'pos': (-20,-20)},
	'garden':{'pos': (30,10)},
	'dungeon':{'pos': (60,20)},
	'datacentre':{'pos': (0,20)},
	# actual maps start here !!!
	'crashsite':{'pos': (0,0)},
	'scene_2':{'pos': (-40,0)},
	'first_dungeon':{'pos': (-40,30)},
	'dungeon_exit':{'pos': (-60,54)},
	'radio_shack':{'pos': (-30,60)},
	'pool':{'pos': (-60,0)}
}

DIALOGUE = {
			0: [['Dude, where the hell are','you going ?'],
				['Sorry pal, gotta go!','Places to go....','People to see....']], 
			1: [['This is more dialogue for','a second cutscene.','Tell me if it worked ?'], 
				['How do you expect me to','hear you from there ?']],
			2: [['I am on my bike and loving it!', 'Whatcha think?'], 
				['Anyway. . . '],
				["It's time to get outta here!"]]
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
			'right': False, 'return': False, 'right_ctrl': False, 'backspace': False, 'g': False, 'p': False, 'n': False, 'm': False, 'left_click': False, 
			'right_click': False, 'scroll_up': False, 'scroll_down': False}

