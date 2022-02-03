# Import the pygame module
import pygame
import random
from time import sleep



# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
P_SPEED = 1

# Define a player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("jet.png").convert()
        self.surf.set_colorkey((0,0,0), RLEACCEL)
        self.rect = self.surf.get_rect()
    # Move the sprite based on user keypresses
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -P_SPEED)
            move_up_sound.play()
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, P_SPEED)
            move_down_sound.play()
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-P_SPEED, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(P_SPEED, 0)
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("missile.png").convert()
        self.surf.set_colorkey((0,0,0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = (1)

    # Move the sprite based on speed
    # Remove the sprite when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

class Present(pygame.sprite.Sprite):
    def __init__(self):
        super(Present, self).__init__()
        self.surf = pygame.image.load("star.png").convert()
        self.surf.set_colorkey((0,0,0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = 1

    # Move the sprite based on speed
    # Remove the sprite when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load("cloud.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        # The starting position is randomly generated
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )

    # Move the cloud based on a constant speed
    # Remove the cloud when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-1, 0)
        if self.rect.right < 0:
            self.kill()

class Lives1(pygame.sprite.Sprite):
    def __init__(self):
        super(Lives1, self).__init__()
        self.surf = pygame.image.load("heart.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        # The starting position is top right
        self.rect = self.surf.get_rect(center=(SCREEN_WIDTH - 30, 30))

    def lose_life(self):
        self.kill()

class Lives2(pygame.sprite.Sprite):
    def __init__(self):
        super(Lives2, self).__init__()
        self.surf = pygame.image.load("heart.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        # The starting position is top right
        self.rect = self.surf.get_rect(center=(SCREEN_WIDTH - 80, 30))

    def lose_life(self):
        self.kill()

class Lives3(pygame.sprite.Sprite):
    def __init__(self):
        super(Lives3, self).__init__()
        self.surf = pygame.image.load("heart.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        # The starting position is top right
        self.rect = self.surf.get_rect(center=(SCREEN_WIDTH - 130, 30))

    def lose_life(self):
        self.kill()

# Initialize pygame
pygame.init()

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)

ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)

ADDPRESENT = pygame.USEREVENT + 3
pygame.time.set_timer(ADDPRESENT, 2000)

# Instantiate player. Right now, this is just a rectangle.
player = Player()
life1 = Lives1()
life2 = Lives2()
life3 = Lives3()

# Create groups to hold enemy sprites and all sprites
# - enemies is used for collision detection and position updates
# - all_sprites is used for rendering
enemies = pygame.sprite.Group()
presents = pygame.sprite.Group()
clouds = pygame.sprite.Group()
lives = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(life1)
all_sprites.add(life2)
all_sprites.add(life3)

# Variable to keep the main loop running
running = True

pygame.mixer.music.load("Electronic Fantasy.ogg")
pygame.mixer.music.play(loops=-1)

move_up_sound = pygame.mixer.Sound("avion.wav")
move_down_sound = pygame.mixer.Sound("avion2.wav")
collision_sound = pygame.mixer.Sound("explosion-01.wav")
bling_sound = pygame.mixer.Sound("bling.wav")

# Main loop
clock = pygame.time.Clock()
while running:
    # for loop through the event queue
    for event in pygame.event.get():

        # Check for KEYDOWN event
        if event.type == KEYDOWN:
            # If the Esc key is pressed, then exit the main loop
            if event.key == K_ESCAPE:
                running = False

        # Add a new enemy?
        elif event.type == ADDENEMY:
            # Create the new enemy and add it to sprite groups
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)        

        # Add a new present?
        elif event.type == ADDPRESENT:
            # Create the new present and add it to sprite groups
            new_present = Present()
            presents.add(new_present)
            all_sprites.add(new_present)
            
        # Add a new cloud?
        elif event.type == ADDCLOUD:
            # Create the new cloud and add it to sprite groups
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)

        # Check for QUIT event. If QUIT, then set running to false.
        elif event.type == QUIT:
            running = False

    pressed_keys = pygame.key.get_pressed()

    player.update(pressed_keys)
        
    enemies.update()
    presents.update()
    clouds.update()

    # Fill the screen with black
    screen.fill((135, 206, 250))

    # Draw all sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # Draw the player on the screen
    screen.blit(player.surf, player.rect)
    
    # Update the display
    pygame.display.flip()

    # Check if any enemies have collided with the player
    if pygame.sprite.spritecollideany(player, enemies):
        # If so, then remove the player and stop the loop
        move_up_sound.stop()
        move_down_sound.stop()
        collision_sound.play()
        sleep(3)
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        player.kill()
        running = False

    if pygame.sprite.spritecollideany(player, presents):
        bling_sound.play()
        new_present.kill()
        
    clock.tick(800)

# All done! Stop and quit the mixer.
