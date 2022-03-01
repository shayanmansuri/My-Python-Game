class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        self.sc_color= (255,0,0)
        # Ship settings
        # self.ship_speed = 6.0

        # Bullet settings
        self.bullet_speed = 10.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 5

        # Alien settings
        # self.alien_speed = 3.0
        # self.superalien_speed = 2.0

        self.ship_limit = 3

        # How quickly the game speeds up
        self.speedup_scale = 1.1
        self.speedup_scale_super = 0.3

        # How quickly the alien point values increase
        self.score_scale = 1.0

        self.initialize_dynamic_settings()


    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed = 6.0
        self.bullet_speed = 10.0
        self.alien_speed = 3.0
        self.superalien_speed= 2.0

        # Scoring
        self.alien_points = 50
        self.superalien_points = 75

        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1


    def increase_speed(self):
        """Increase speed settings."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.superalien_speed *= self.speedup_scale_super

        self.alien_points = int(self.alien_points * self.score_scale)
        self.superalien_points = int(self.superalien_points * self.score_scale)
        