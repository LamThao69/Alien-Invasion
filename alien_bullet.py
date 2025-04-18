import pygame
from pygame.sprite import Sprite

class AlienBullet(Sprite):
    """A class to manage bullets fired by aliens."""

    def __init__(self, ai_settings, screen, alien):
        super().__init__()
        self.screen = screen

        # Create a bullet rect at the alien's current position
        self.rect = pygame.Rect(0, 0, 3, 15)
        self.rect.centerx = alien.rect.centerx
        self.rect.top = alien.rect.bottom

        self.y = float(self.rect.y)

        self.color = (255, 0, 0)  # Màu đạn của alien (đỏ)
        self.speed_factor = 1     # Tốc độ đạn rơi

    def update(self):
        """Move the bullet down the screen."""
        self.y += self.speed_factor
        self.rect.y = self.y

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
