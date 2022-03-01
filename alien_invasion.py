# pylint: disable=no-member

import sys
import pygame
from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien
from super_alien import SuperAliens
from time import sleep
from button import Button
from scoreboard import Scoreboard

class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.settings = Settings()
        

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        # for full screen :
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height

        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self) 
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

        # Make the Play button.
        self.play_button = Button(self, "Play")

        self.superaliens = pygame.sprite.Group()
        self._create_super()
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)


    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                self._update_superaliens()
                

            self._update_screen()
            



    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
                
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

                


    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_DOWN:
            # Move the ship to the down.
            self.ship.moving_down = True

        # Move the ship to the up.
        elif event.key == pygame.K_UP:
            self.ship.moving_up = True
                
        # Move the ship to the right.
        elif event.key == pygame.K_RIGHT:
            self.ship.moving_right = True

        # Move the ship to the left.
        elif event.key == pygame.K_LEFT :
            self.ship.moving_left = True
        
        elif event.key == pygame.K_q:
            sys.exit()

        elif event.key == pygame.K_SPACE:
               self._fire_bullet()


    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_DOWN:
            self.ship.moving_down = False

        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
                
        elif event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
            
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
    



    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
    


    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions.
        self.bullets.update()

        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.right >= self.settings.screen_width:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()
        self._check_bullet_superalien_collisions()
                
       
        
        
        

        

        


    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        # Redraw the screen during each pass through the loop.
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        self.superaliens.draw(self.screen)

        # Draw the score information.
        self.sb.show_score()

        # Draw the play button if the game is inactive.
        if not self.stats.game_active:
            self.play_button.draw_button()


        # Make the most recently drawn screen visible.
        pygame.display.flip()

        
    


    def _create_fleet(self):
        """Create the fleet of aliens."""
        # Make an alien.
        alien = Alien(self)
        self.aliens.add(alien)


    
    def _create_super(self):
        """Create the fleet of aliens."""
        # Make an alien. 
        superalien= SuperAliens(self)
        self.superaliens.add(superalien)




    def _update_aliens(self):
        """Update the positions of all aliens in the fleet."""
        self.aliens.update()
        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship ,self.aliens):
            self._ship_hit()
        
        self._check_aliens_left()
        
             
    

    
    def _update_superaliens(self):
        """Update the positions of all aliens in the fleet."""
        self.superaliens.update()
        if pygame.sprite.spritecollideany(self.ship ,self.superaliens):
            self._ship_hit2()

        self._check_superaliens_left()




    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        # Check for any bullets that have hit aliens.
        #   If so, get rid of the bullet and the alien.
        collisions = pygame.sprite.groupcollide( self.bullets, self.aliens, True, True)
        if not self.aliens:
            # Destroy existing bullets and create new fleet.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            
        if collisions:
            for aliens in collisions.values():
               self.stats.score += self.settings.alien_points * len(aliens)
               
               
            
            self.sb.prep_score()
            self.sb.check_high_score()
            



    
    def _check_bullet_superalien_collisions(self):
        collisions_superaliens = pygame.sprite.groupcollide( self.bullets, self.superaliens, True, False)
        if not self.superaliens:
            self.bullets.empty()
            self._create_super()
            self.settings.increase_speed()

        if collisions_superaliens:
            for superaliens_hit in collisions_superaliens.values():
               self.stats.score += self.settings.superalien_points * len(superaliens_hit)
               
               superaliens_hit[0].health -= 1
               if superaliens_hit[0].health <= 0 :
                   self.superaliens.remove(superaliens_hit)

            self.sb.prep_score()
            self.sb.check_high_score()
            
            

    

    def _check_aliens_left(self):
        """Check if any aliens have reached the left of the screen."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.left <= screen_rect.left:
                self._ship_hit()
                break
                
                


    def _check_superaliens_left(self):
        """Check if any superaliens have reached the left of the screen."""
        screen_rect = self.screen.get_rect()
        for alien in self.superaliens.sprites():
            if alien.rect.left <= screen_rect.left:
                self._ship_hit2()
                break
                
                

    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        # Get rid of any remaining aliens and bullets.
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.sb.prep_healths()
            self.aliens.empty()
            # self.bullets.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)
        


    def _ship_hit2(self):
        """Respond to the ship being hit by an alien."""
        if self.stats.ships_left > 0:
        # Get rid of any remaining aliens and bullets.
            self.stats.ships_left -= 1
            self.sb.prep_healths()
            self.superaliens.empty()
            # self.bullets.empty()

            # Create a new fleet and center the ship.
            self._create_super()
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)



    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Reset the game settings.
            self.settings.initialize_dynamic_settings()

            # Reset the game statistics.
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_healths()

            # Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self._create_super()

            # Hide the mouse cursor.
            pygame.mouse.set_visible(False)


if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()


    