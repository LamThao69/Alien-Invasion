import sys
from time import sleep
import pygame
from bullet import Bullet
from alien import Alien
import random
from alien_bullet import AlienBullet

def get_number_aliens_x(ai_settings, alien_width):
	"""Determine the number of aliens which fit in the row."""
	available_space_x = ai_settings.screen_width - 2 * alien_width
	number_aliens_x = int(available_space_x / (2 * alien_width))
	return number_aliens_x
	
def get_number_rows(ai_settings, ship_height, alien_height):
	"""Determine the number of rows of aliens that fit in the screen."""
	available_space_y = (ai_settings.screen_height-(3*alien_height)-ship_height)
	number_rows = int(available_space_y/(2*alien_height))
	return number_rows
	
def create_alien(ai_settings, screen, aliens, alien_number, row_number):
	"""Create an alien and place it in the row of aliens."""
	alien = Alien(ai_settings, screen)
	alien_width = alien.rect.width
	alien.x = alien_width + 2 * alien_width * alien_number
	alien.rect.x = alien.x
	alien.rect.y = alien.rect.height+2*alien.rect.height*row_number
	aliens.add(alien)	
	
def create_fleet(ai_settings, screen, ship, aliens):
	"""Create a full fleet of aliens."""
	# Create an alien and find the number of aliens in a row.
	alien = Alien(ai_settings, screen)
	number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
	number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
	
	# Create the fleet of aliens.
	#for row_number in range(number_rows):
	#	for alien_number in range(number_aliens_x):
	#		create_alien(ai_settings, screen, aliens, alien_number, row_number)

	for row_number in range(ai_settings.alien_max_y):
		if (number_aliens_x >= ai_settings.alien_max_x):
			for alien_number in range(ai_settings.alien_max_x):
				create_alien(ai_settings, screen, aliens, alien_number, row_number)
		else:
			for alien_number in range(number_aliens_x):
				create_alien(ai_settings, screen, aliens, alien_number, row_number)
			
def check_fleet_edges(ai_settings, aliens):
	"""Act properly when alien hits an edge."""
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_direction(ai_settings, aliens)
			break
			
def change_fleet_direction(ai_settings, aliens):
	"""Drop the entire fleet and change its' direction."""
	for alien in aliens.sprites():
		alien.rect.y += ai_settings.fleet_drop_speed
	ai_settings.fleet_direction *= -1 # to change direction in next drop
	
def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
	"""Respond to ship being hit by alien."""
	if stats.ships_left > 0:
		# Decrrement ships_left
		stats.ships_left -= 1
	
		# Empty the list of aliens and bullets.
		aliens.empty()
		bullets.empty()
	
		# Create a new fleet and center the ship.
		create_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()
		# Pause.
		sleep(0.5)

	else:
		ai_settings.reset_difficulty() # Reset difficulty to default
		stats.game_active = False
			
def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets):
	"""Check if any aliens have reached the bottom of the screen."""
	screen_rect = screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom >= screen_rect.bottom:
			# Treat this the same as if the ship got hit.
			ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
			break
	
def update_aliens(ai_settings, stats, screen, ship, aliens, bullets,alien_bullets):
	"""Check if the fleet is at an edge and update the positions of all aliens in the fleet"""
	check_fleet_edges(ai_settings, aliens)
	aliens.update()
	
	# Look for alien-ship collisions.
	if pygame.sprite.spritecollideany(ship, aliens):
		ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
		
	# Check for aliens hitting the bottom of the screen.
	check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets)

	if random.randint(0, 100) < 2:  # 2% cơ hội mỗi frame
		alien_fire(ai_settings, screen, aliens, alien_bullets)

def update_alien_bullets(ai_settings, stats, screen, ship, aliens, bullets, alien_bullets):
	"""Cập nhật vị trí và kiểm tra va chạm"""
	alien_bullets.update()

	# Xóa các đạn ngoài màn hình
	for bullet in alien_bullets.copy():
		if bullet.rect.top > 800:  # Chiều cao màn hình
			alien_bullets.remove(bullet)

	# Kiểm tra va chạm giữa alien bullet và ship
	if pygame.sprite.spritecollideany(ship, alien_bullets):
		alien_bullets.empty()
		if (stats.ships_left > 0):
			# Decrrement ships_left
			stats.ships_left -= 1
		else:
			ai_settings.reset_difficulty() # Reset difficulty to default
			stats.game_active = False
		# Empty the list of aliens and bullets.
		

def check_events(ai_settings, screen, stats, play_button, ship, bullets, aliens):
	"""Respond to keypressed and mouse events."""
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			check_keydown_events(event, ai_settings, screen, ship, bullets)	
		elif event.type == pygame.KEYUP:
			check_keyup_events(event, ship)
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_x, mouse_y = pygame.mouse.get_pos()
			check_play_button(ai_settings,screen,stats, play_button, mouse_x, mouse_y,ship,aliens,bullets)
			
def check_play_button(ai_settings,screen,stats, play_button, mouse_x, mouse_y,ship,aliens,bullets):
	"""Start a new game when Play button pressed."""
	if play_button.rect.collidepoint(mouse_x, mouse_y):
		# Reset the game settings.
		# Empty the list of aliens and bullets.
		aliens.empty()
		bullets.empty()
	
		# Create a new fleet and center the ship.
		create_fleet(ai_settings, screen, ship, aliens)
		if (stats.high_score < stats.score):
				stats.high_score = stats.score
		stats.reset_stats()
		stats.game_active = True
				
def check_keydown_events(event, ai_settings, screen, ship, bullets):
	"""Respond to keypresses."""
	# Right - Left
	if event.key == pygame.K_RIGHT:
		ship.moving_right = True
	elif event.key == pygame.K_LEFT:
		ship.moving_left = True
	# Up - Down
	elif event.key == pygame.K_UP:
		ship.moving_up = True
	elif event.key == pygame.K_DOWN:
		ship.moving_down = True
	# Spacebar - shooting
	elif event.key == pygame.K_SPACE:
		fire_bullet(ai_settings, screen, ship, bullets)
	elif event.key == pygame.K_q:
		sys.exit()

			
def fire_bullet(ai_settings, screen, ship, bullets):
	"""Fire a bullet if limit is not reached yet."""
	# Create a new bullet and add it to the bullets group
	if len(bullets) < ai_settings.bullets_allowed:
		new_bullet = Bullet(ai_settings, screen, ship)
		bullets.add(new_bullet)

def alien_fire(ai_settings, screen, aliens, alien_bullets):

	if len(alien_bullets) < ai_settings.alien_bullets_allowed:
		shooting_alien = random.choice(aliens.sprites())
		new_bullet = AlienBullet(ai_settings, screen, shooting_alien)
		alien_bullets.add(new_bullet)

def check_keyup_events(event, ship):
	"""Respond to key releases."""
	# Right - Left
	if event.key == pygame.K_RIGHT:
		ship.moving_right = False
	elif event.key == pygame.K_LEFT:
		ship.moving_left = False
		
	# Up - Down
	if event.key == pygame.K_UP:
		ship.moving_up = False
	elif event.key == pygame.K_DOWN:
		ship.moving_down = False
				
def update_screen(ai_settings, screen, stats, ship, aliens, bullets, play_button,alien_bullets):
	"""Update images on the screen and flip to the new screen."""
	# Redraw the screen during each pass through the loop
	screen.fill(ai_settings.bg_color)

	# Redraw all bullets behind ship and aliens.
	for bullet in bullets.sprites():
		bullet.draw_bullet()

	ship.blitme()
	aliens.draw(screen)

	# Draw the score
	font = pygame.font.SysFont(None, 48)  # Chọn phông chữ và kích thước
	score_image = font.render("Score: " + str(stats.score), True, (30, 30, 30))  # Render điểm
	screen.blit(score_image, (10, 10))  # Vị trí hiển thị điểm trên màn hình	

	level_image = font.render("Level: " + str(stats.level), True, (30, 30, 30))
	screen.blit(level_image, (10,40))

	ship_left_image = font.render("Ships Left: " + str(stats.ships_left), True, (30, 30, 30))
	screen.blit(ship_left_image, (10,70))

	for bullet in alien_bullets.sprites():
		bullet.draw_bullet()

	# Draw the play button if the game is inactive.
	if not stats.game_active:

		high_score_image = font.render("High Score: " + str(stats.high_score), True, (30, 30, 30))
		screen.blit(high_score_image, (screen.get_rect().centerx-120, screen.get_rect().centery+30))
		screen.blit(score_image, (screen.get_rect().centerx-120, screen.get_rect().centery+60))
		play_button.draw_button()
	
	# Make the most recently drawn screen visible
	pygame.display.flip()
	
def update_bullets(ai_settings, screen,stats, ship, aliens, bullets):
	"""Update position of the bullets and rid of old bullets."""
	# Update bullet positions.
	bullets.update()
		
	# Get rid of bullets that have disappeared
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)
	
	check_bullet_alien_collision(ai_settings, screen, stats, ship, aliens, bullets)
			
def check_bullet_alien_collision(ai_settings, screen,stats, ship, aliens, bullets):
	"""Respond to bullet-alien collision."""
	# Remove any bullets and aliens that have collided.
	collisions = pygame.sprite.groupcollide(bullets, aliens, True, True) # reference in Pygame docs
	if collisions:
		for aliens in collisions.values():
			stats.score += 10
	if len(aliens) == 0:
		# Destroy existing bullets and create new fleet.
		bullets.empty()
		create_fleet(ai_settings, screen, ship, aliens)
		stats.level += 1
		ai_settings.increase_difficulty(stats.level) # Increase difficulty based on level
		
