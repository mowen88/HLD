import pygame, math, csv, random
from math import atan2, degrees, pi
from settings import *
from state import State
from camera import Camera
from create_zone import CreateZone
from particles import Shadow, Flash, Explosion
from sprites import Sword, Gun, Bullet, ShotgunShell, Grenade, Beam
from cutscenes.cutscene_manager import Cutscene, CollectionCutscene
from ui import UI
from map import Map
from pause import PauseMenu

class Zone(State):
	def __init__(self, game, name, entry_point):
		State.__init__(self, game)

		self.game = game
		self.name = name
		self.entry_point = entry_point
		self.zone_size = self.get_zone_size()
		
		PLAYER_DATA.update({'current_zone': self.name, 'entry_pos': self.entry_point})
		if self.name not in COMPLETED_DATA['visited_zones']:
			COMPLETED_DATA['visited_zones'].append(self.name)

		#sprites
		self.melee_sprite = None
		self.gun_sprite = None
		self.boss = None
		self.player_bullet_sprites = pygame.sprite.Group()
		self.shotgun_shell_sprites = pygame.sprite.Group()
		self.beam_sprites = pygame.sprite.Group()
		self.enemy_bullet_sprites = pygame.sprite.Group()
		self.grenade_sprites = pygame.sprite.Group()
		self.explosion_sprites = pygame.sprite.Group()

		# sprite groups
		self.rendered_sprites = Camera(self.game, self)
		self.updated_sprites = pygame.sprite.Group()
		self.cutscene_sprites = pygame.sprite.Group()
		self.exit_sprites = pygame.sprite.Group()
		self.block_sprites = pygame.sprite.Group()
		self.platform_sprites = pygame.sprite.Group()
		self.trigger_sprites = pygame.sprite.Group()
		self.barrier_sprites = pygame.sprite.Group()
		self.barrier_activator_sprites = pygame.sprite.Group()
		self.void_sprites = pygame.sprite.Group()
		self.enemy_sprites = pygame.sprite.Group()
		self.boss_sprites = pygame.sprite.Group()
		self.npc_sprites = pygame.sprite.Group()
		self.attackable_sprites = pygame.sprite.Group()
		self.health_sprites = pygame.sprite.Group()
		self.juice_sprites = pygame.sprite.Group()
		self.key_sprites = pygame.sprite.Group()
		self.gun_pickup_sprites = pygame.sprite.Group()

		CreateZone(self.game, self).create()

		self.game.current_health = PLAYER_DATA['max_health']
		self.screenshaking = False
		self.screenshake_timer = 0
		self.cutscene_running = False
		self.entering = True
		self.exiting = False
		self.locked_in = False
		self.new_zone = None

		self.ui = UI(self.game, self)
		self.pause = PauseMenu(self.game)

	def get_zone_size(self):
		with open(f'../zones/{self.name}/{self.name}_walls.csv', newline='') as csvfile:
		    reader = csv.reader(csvfile, delimiter=',')
		    for row in reader:
		        rows = (sum (1 for row in reader) + 1)
		        cols = len(row)
		return (cols * TILESIZE, rows * TILESIZE)

	def create_zone(self, zone):
		Zone(self.game, zone, self.entry_point).enter_state()

	def create_flash(self, pos, colour, size):
		self.flash = Flash(self.game, self, [self.updated_sprites, self.rendered_sprites], pos, colour, size, LAYERS['particles'])

	def create_melee(self):
		self.melee_sprite = Sword(self.game, self, [self.updated_sprites, self.rendered_sprites], self.player.hitbox.center, LAYERS['player'], '../assets/weapons/sword')
	
	def create_gun(self):
		self.gun_sprite = Gun(self.game, self, [self.updated_sprites, self.rendered_sprites], self.player.hitbox.center, LAYERS['player'], pygame.image.load(f'../assets/weapons/{self.player.gun}.png').convert_alpha())

	def create_player_bullet(self):
		self.bullet = Bullet(self.game, self, [self.player_bullet_sprites, self.updated_sprites, self.rendered_sprites], self.player.hitbox.center, LAYERS['player'], f'../assets/weapons/{self.player.gun}_bullet')

	def create_shotgun_shell(self):
		self.shotgun_shell = ShotgunShell(self.game, self, [self.player_bullet_sprites, self.shotgun_shell_sprites, self.updated_sprites, self.rendered_sprites], self.player.hitbox.center, LAYERS['player'], f'../assets/weapons/{self.player.gun}_bullet')

	def create_player_grenade(self):
		Grenade(self.game, self, [self.grenade_sprites, self.updated_sprites, self.rendered_sprites], self.player.hitbox.center, LAYERS['player'], f'../assets/weapons/grenade')

	def create_explosion(self, pos, damage, knockback_power):
		Explosion(self.game, self, [self.explosion_sprites, self.updated_sprites, self.rendered_sprites], pos, LAYERS['player'], f'../assets/particles/explosion', damage, knockback_power)


	def create_railgun_beam(self):
		angle = math.atan2(pygame.mouse.get_pos()[1]-self.player.hitbox.centery + self.rendered_sprites.offset[1], pygame.mouse.get_pos()[0]-self.player.hitbox.centerx + self.rendered_sprites.offset[0])
		x = math.hypot(WIDTH, HEIGHT) * math.cos(angle) + self.player.hitbox.centerx
		y = math.hypot(WIDTH, HEIGHT) * math.sin(angle) + self.player.hitbox.centery
		distance = ((x, y) - pygame.math.Vector2(self.player.hitbox.center)).magnitude()
		point_list = self.get_equidistant_points(self.player.hitbox.center - self.rendered_sprites.offset, (x - self.rendered_sprites.offset[0], y - self.rendered_sprites.offset[1]), int(distance/6))
		for num, point in enumerate(point_list):
			if num < 50: self.beam = Beam(self.game, self, [self.player_bullet_sprites, self.beam_sprites, self.updated_sprites, self.rendered_sprites], point + self.rendered_sprites.offset, LAYERS['particles'],  f'../assets/weapons/railgun_particle', 4)
			for sprite in self.block_sprites:
				if sprite not in self.attackable_sprites:
					if sprite.hitbox.collidepoint(point + self.rendered_sprites.offset):
						#BeamBlast(self.game, self, 'beam_blast', [self.updated_sprites, self.rendered_sprites], point, LAYERS['explosions'])
						return False

	def lerp(self, v0, v1, t):
		return v0 + t * (v1 - v0)

	def get_equidistant_points(self, point_1, point_2, num_of_points):
		return [(self.lerp(point_1[0], point_2[0], 1./num_of_points * i), self.lerp(point_1[1], point_2[1], 1./num_of_points * i)) for i in range(num_of_points + 1)]
			
	def enemy_shot_logic(self):
		for target in self.enemy_sprites:
			for bullet in self.player_bullet_sprites:
				if bullet.rect.colliderect(target.hitbox):
					if not target.invincible and target.alive:
						if not hasattr(bullet, 'alpha') or (hasattr(bullet, 'alpha') and bullet.alpha >= 255):
							target.health -= bullet.damage
							if bullet not in self.shotgun_shell_sprites:
								bullet.kill()
							target.invincible = True
							if bullet.damage > 3:
								target.get_knockback(self.player)
							if target.health <= 0:
								target.get_knockback(self.player)
								target.invincible = False
								target.alive = False
								self.enemy_sprites.remove(target)
								if target in self.boss_sprites:
									COMPLETED_DATA['bosses_defeated'].append(target.name)


	def collect(self):
		if self.player.z == LAYERS['player'] and not self.cutscene_running:
			for sprite in self.health_sprites:
				if self.player.hitbox.colliderect(sprite.hitbox):
					self.create_flash(sprite.rect.center, WHITE, 4)
					self.ui.add_health()
					COMPLETED_DATA['health'].append(sprite.name)
					self.cutscene_running = True
					CollectionCutscene(self.game, self, f"../assets/ui_images/partial_health_collected/{PLAYER_DATA['partial_healths']}").enter_state()
					sprite.alive = False
					sprite.kill()

			for sprite in self.juice_sprites:
				if self.player.hitbox.colliderect(sprite.hitbox):
					self.create_flash(sprite.rect.center, CYAN, 4)
					PLAYER_DATA['max_juice'] += 11
					COMPLETED_DATA['juice'].append(sprite.name)
					self.cutscene_running = True
					CollectionCutscene(self.game, self, f"../assets/ui_images/juice_collected/").enter_state()
					sprite.alive = False
					sprite.kill()

			for sprite in self.key_sprites:
				if self.player.hitbox.colliderect(sprite.hitbox):
					self.create_flash(sprite.rect.center, PINK, 5)
					COMPLETED_DATA['keys'].append(sprite.name)
					self.cutscene_running = True
					CollectionCutscene(self.game, self, f"../assets/ui_images/juice_collected/").enter_state()
					sprite.alive = False
					sprite.kill()

			for sprite in self.gun_pickup_sprites:
				if self.player.hitbox.colliderect(sprite.hitbox):
					self.create_flash(sprite.rect.center, PINK, 5)
					COMPLETED_DATA['guns'].append(sprite.name)
					self.cutscene_running = True
					CollectionCutscene(self.game, self, f"../assets/ui_images/juice_collected/").enter_state()
					sprite.alive = False
					sprite.kill()
					self.player.gun = COMPLETED_DATA['guns'][PLAYER_DATA['gun_index']]

	def activate_barriers(self):
		for sprite in self.barrier_activator_sprites:
			if self.player.hitbox.colliderect(sprite.rect):
				self.locked_in = True

	def activate_platforms(self, dt):
		for bullet in self.beam_sprites:
			for trigger in self.trigger_sprites:
				if bullet.rect.colliderect(trigger.rect):
					bullet.kill()
					self.create_flash(trigger.rect.center, YELLOW, 2)
					for platform in self.platform_sprites:
						if platform.number == trigger.number:
							self.rendered_sprites.add(platform)
							platform.active = True

	def activate_cutscene(self):
		for sprite in self.cutscene_sprites:
			if self.player.hitbox.colliderect(sprite.rect) and sprite.number not in COMPLETED_DATA['cutscenes']:
				COMPLETED_DATA['cutscenes'].append(sprite.number)
				# self.target.direction.update({key: False for key in self.target.direction})
				self.cutscene_running = True
				Cutscene(self.game, self, sprite.number).enter_state()

	def exit_zone(self):
		for sprite in self.exit_sprites:
			if self.player.hitbox.colliderect(sprite.rect):
				self.exiting = True
				self.new_zone = ZONE_DATA[self.name][sprite.name]
				self.entry_point = sprite.name
			
	def get_distance_direction_and_angle(self, point_1, point_2):
		pos_1 = pygame.math.Vector2(point_1 - self.rendered_sprites.offset)
		pos_2 = pygame.math.Vector2(point_2)
		distance = (pos_2 - pos_1).magnitude()

		if (pos_2 - pos_1).magnitude() != 0: direction = (pos_2 - pos_1).normalize()
		else: direction = pygame.math.Vector2(0.1,0.1)

		radians = atan2(-(point_1[0] - (pos_2.x + self.rendered_sprites.offset.x)), (point_1[1] - (pos_2.y + self.rendered_sprites.offset.y)))
		radians %= 2*pi
		angle = int(degrees(radians))

		dot_product_left = pygame.math.Vector2(direction.y, -direction.x).normalize()
		dot_product_right = pygame.math.Vector2(-direction.y, direction.x).normalize()

		return(distance, direction, angle, dot_product_left, dot_product_right)

	def update(self, dt):
		if self.player.z == LAYERS['player']:
			self.activate_platforms(dt)
			self.activate_barriers()
			self.activate_cutscene()
			self.collect()
			self.exit_zone()
			self.enemy_shot_logic()

		if ACTIONS['return']: 
			Map(self.game, self).enter_state()
			#self.exit_state()
			self.game.reset_keys()

		if ACTIONS['p']:
			self.pause.enter_state()
			self.game.reset_keys()
			# self.game.quit_write_data()
			# self.exit_state()
			# self.prev_state.exit_state()
			# self.game.reset_keys()

		self.updated_sprites.update(dt)
		self.ui.update(dt)

	def draw(self, screen):
		screen.fill(GREEN)

		self.rendered_sprites.offset_draw(screen, self.target.rect.center)

		#self.bloom_surf.draw(screen)
		self.ui.draw(screen)

		self.fade_surf.draw(screen)


		# self.game.render_text(str(round(self.game.clock.get_fps(), 2)), WHITE, self.game.small_font, (WIDTH * 0.5, HEIGHT * 0.1))
		# #self.game.render_text(self.player.vel, WHITE, self.game.small_font, RES/2)
		# self.game.render_text(COMPLETED_DATA['guns'], WHITE, self.game.small_font, (WIDTH * 0.5, HEIGHT * 0.9))
		
		
