class Settings():
	"""A class to store all settings for Alien Invasion."""
	
	def __init__(self):
		"""Initialize the game's settings."""
		# Screen settings
		self.screen_width = 1200
		self.screen_height = 800
		self.bg_color = (250, 250, 250)
		
		# Ship settings
		self.ship_speed_factor = 1.5
		self.ship_limit = 1
		
		# Bullet settings
		self.bullet_speed_factor = 3
		self.bullet_width = 3
		self.bullet_height = 15
		self.bullet_color = 60, 60, 60	
		self.bullets_allowed = 3
		#alien count
		self.alien_max_x = 5
		self.alien_max_y = 4
		# Alien bullet settings
		self.alien_bullets_allowed = 1
		# Alien settings
		self.alien_speed_factor = 0.3
		self.fleet_drop_speed = 10
		# fleet_direcion of 1 represents right; -1 represents left.
		self.fleet_direction = 1
		#lvl scale
		self.speedup_scale = 1.5
	def increase_difficulty(self,level):
		if level > 5:
			self.alien_max_y = 5
		self.alien_speed_factor *= self.speedup_scale
		self.alien_max_x +=1
		self.alien_bullets_allowed = 1+1
	def reset_difficulty(self):
		self.alien_speed_factor = 0.3
		self.fleet_drop_speed = 10
		self.alien_bullets_allowed = 1
		self.alien_max_x = 5
		self.alien_bullets_allowed = 1
    