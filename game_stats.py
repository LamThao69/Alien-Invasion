class GameStats():
	"""Track statistics for Alien Invasion."""
	
	def __init__(self, ai_settings):
		"""Initialize statistics."""
		self.ai_settings = ai_settings
		self.reset_stats()
		# Start Alien Invasion in an active state.
		self.game_active = True
		self.level = 1
		self.score = 0
		self.high_score = 0
		self.current_score = 0
		self.current_level = 1
	def reset_stats(self):
		"""Initialize statistics that can change during the game."""
		self.level = 1
		self.ships_left = 1
		self.score = 0
