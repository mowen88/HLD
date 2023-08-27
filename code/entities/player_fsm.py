import pygame
from settings import *

class Idle:
	def __init__(self, player, direction):
		player.frame_index = 0
		self.direction = direction

	def state_logic(self, player):
		keys = pygame.key.get_pressed()

		if keys[pygame.K_RCTRL] and player.game.current_juice >= GUN_DATA[player.gun]['cost']:
			return Shoot(player, self.direction)

		if ACTIONS['space']:
			return Heal(player, self.direction)

		if ACTIONS['scroll_down']:
			player.change_gun('scroll_down')

		if ACTIONS['scroll_up']:
			player.change_gun('scroll_up')

		if ACTIONS['right_click'] and player.dash_count < 3:
			return Dash(player, self.direction)

		if ACTIONS['left_click'] and player.attack_count < 3:
			return Attack(player, self.direction)

		for k, v in player.direction.items():
			if ACTIONS[k]: 
				v = True
				return Move(player, self.direction)

	def update(self, dt, player):
		player.animate(self.direction + '_idle', 0.2 * dt, 'loop')

class Move:
	def __init__(self, player, direction):
		player.frame_index = 0
		self.direction = direction

	def state_logic(self, player):
		keys = pygame.key.get_pressed()

		if keys[pygame.K_RCTRL] and player.game.current_juice >= GUN_DATA[player.gun]['cost']:
			return Shoot(player, self.direction)

		if ACTIONS['space']:
			return Heal(player, self.direction)

		if ACTIONS['scroll_down']:
			player.change_gun('scroll_down')
			
		if ACTIONS['scroll_up']:
			player.change_gun('scroll_up')

		if ACTIONS['right_click'] and player.dash_count < 3:
			return Dash(player, self.direction)

		if ACTIONS['left_click'] and player.attack_count < 3:
			return Attack(player, self.direction)
	
		for k, v in player.direction.items():
			if ACTIONS[k]: 
				self.direction = k
				player.direction[k] = True
			else: 
				player.direction[k] = False
				
		if player.vel.magnitude() < 0.05:
			return Idle(player, self.direction)

	def update(self, dt, player):

		player.acc = pygame.math.Vector2()

		# y direction increment acceleration
		if player.direction['down']: player.acc.y += 0.2
		elif player.direction['up']: player.acc.y -= 0.2
		# x direction increment acceleration
		if player.direction['right']: player.acc.x += 0.2
		elif player.direction['left']: player.acc.x -= 0.2

		player.physics(dt)
		player.animate(self.direction, 0.2 * dt, 'loop')

class Dash:
	def __init__(self, player, direction):

		ACTIONS['right_click'] = False

		player.frame_index = 0
		player.dash_count += 1
		player.dash_timer_running = True
		
		self.timer = 20
		player.dashing = True
		player.respawn_location = player.rect.center
		self.lunge_speed = 6
		self.get_current_direction = pygame.mouse.get_pos()
		player.vel = player.zone.get_distance_direction_and_angle(player.hitbox.center, self.get_current_direction)[1] * self.lunge_speed
		player.angle = player.zone.get_distance_direction_and_angle(player.hitbox.center, self.get_current_direction)[2]
		self.direction = player.get_direction()

	def state_logic(self, player):

		if self.timer < 0:
			if player.get_collide_list(player.zone.void_sprites):
				player.dashing = False
				player.on_ground = False
				return FallDeath(self.direction)
			else: 
				player.dashing = False
				return Idle(player, self.direction)

	def update(self, dt, player):

		self.timer -= dt

		player.physics(dt)
		player.animate(self.direction + '_dash', 0.2 * dt, 'loop')

		player.acc = pygame.math.Vector2()
		self.lunge_speed -= 0.4 * dt
		if player.vel.magnitude() != 0: player.vel = player.vel.normalize() * self.lunge_speed
		if player.vel.magnitude() < 0.1: player.vel = pygame.math.Vector2()	
		
class Attack:
	def __init__(self, player, direction):

		ACTIONS['left_click'] = False

		player.frame_index = 0
		player.attack_count += 1
		player.attack_timer_running = True

		self.timer = 20
		self.lunge_speed = 1
		self.get_current_direction = pygame.mouse.get_pos()
		player.vel = player.zone.get_distance_direction_and_angle(player.hitbox.center, self.get_current_direction)[1] * self.lunge_speed
		player.angle = player.zone.get_distance_direction_and_angle(player.hitbox.center, self.get_current_direction)[2]
		self.direction = player.get_direction()

		player.zone.create_melee()

	def state_logic(self, player):

		if ACTIONS['right_click']:
			player.zone.melee_sprite.kill()
			return Dash(player, self.direction)

		if self.timer < 0:
		# if player.vel.magnitude() < 0.05:
			return Idle(player, self.direction)

	def update(self, dt, player):

		if self.timer > 10: player.player_attacking_logic()

		player.attackable_terrain_logic()

		player.physics(dt)
		player.animate(self.direction + '_attack', 0.2 * dt, 'loop')
		
		self.timer -= dt
		player.acc = pygame.math.Vector2()
		self.lunge_speed -= 0.1 * dt
		if player.vel.magnitude() != 0: player.vel = player.vel.normalize() * self.lunge_speed
		if player.vel.magnitude() < 0.1: player.vel = pygame.math.Vector2()

class Shoot:
	def __init__(self, player, direction):

		player.frame_index = 0
		self.timer = GUN_DATA[player.gun]['cooldown']
		self.lunge_speed = GUN_DATA[player.gun]['knockback']
		self.get_current_direction = pygame.mouse.get_pos()
		player.vel = player.zone.get_distance_direction_and_angle(player.hitbox.center, self.get_current_direction)[1] * self.lunge_speed * -1
		player.angle = player.zone.get_distance_direction_and_angle(player.hitbox.center, self.get_current_direction)[2]
		self.direction = player.get_direction()

		player.zone.create_gun()
		
		player.add_subtract_juice(GUN_DATA[player.gun]['cost'], 'sub')
		if player.gun == 'pistol': player.zone.create_player_bullet()			
		else: player.zone.create_railgun_beam()
		
	def state_logic(self, player):

		if ACTIONS['right_click']:
			player.zone.gun_sprite.kill()
			return Dash(player, self.direction)

		if self.timer < 0:
			player.zone.gun_sprite.kill()
			return Idle(player, self.direction)

	def get_direction(self, player):
		if 45 < player.zone.gun_sprite.angle < 135: self.direction = 'right'
		elif 135 < player.zone.gun_sprite.angle < 225: self.direction = 'down'
		elif 225 < player.zone.gun_sprite.angle < 315: self.direction = 'left'
		else: self.direction = 'up'

	def update(self, dt, player):
		self.get_direction(player)
		player.physics(dt)
		player.animate(self.direction + '_dash', 0.2 * dt, 'end')
		
		self.timer -= dt

		player.acc = pygame.math.Vector2()
		self.lunge_speed -= 0.1 * dt
		if player.vel.magnitude() != 0: player.vel = player.vel.normalize() * self.lunge_speed
		if player.vel.magnitude() < 0.1: player.vel = pygame.math.Vector2()

class Heal:
	def __init__(self, player, direction):
		player.frame_index = 0
		self.direction = direction
		self.timer = 60

	def state_logic(self, player):
		if not ACTIONS['space'] or player.invincible:
			return Idle(player, self.direction)

		if self.timer <= 0:
			self.heal_player(player)
			return Idle(player, self.direction)

	def heal_player(self, player):
		if player.game.current_juice >= PLAYER_DATA['heal_cost']:
			player.zone.player.add_subtract_juice(PLAYER_DATA['heal_cost'], 'sub')
			if PLAYER_DATA['max_health'] >= player.game.current_health +1:
				player.game.current_health += 1

	def update(self, dt, player):
		self.timer -= dt
		player.animate(self.direction + '_heal', 0.2 * dt, 'end')



class FallDeath:
	def __init__(self, direction):
		self.frame_index = 0
		self.direction = direction
		self.timer = 55

	def state_logic(self, player):
		if self.timer <= 0: 
			player.zone.screenshaking = False
			player.z = LAYERS['player']
			player.on_ground = True
			player.vel.y = 0
			player.pos.x = player.respawn_location[0]
			player.pos.y = player.respawn_location[1]
			player.hitbox.center = (player.pos.x, player.pos.y)
			player.rect.center = player.hitbox.center
			player.reduce_health(1)
			return Idle(player, self.direction)

	def update(self, dt, player):
		
		player.animate(self.direction + '_fall', 0.2 * dt, 'end')

		self.timer -= dt
		if self.timer > 0:
			if self.timer < 15: player.zone.screenshaking = True
			player.z = LAYERS['BG2']
			player.vel.y += 0.15 * dt
			player.pos += player.vel
			player.hitbox.centery = player.pos.y
			player.rect.centery = player.hitbox.centery

		

