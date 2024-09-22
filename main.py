import sys
import pygame
import os

##########################################################################################
# Galactic Clash - A Competitive Two-Player Game
#
# Description:
# This game, "Galactic Clash!", pits two players against each other in a space-themed battle.
# Each player controls a spaceship located on opposite sides of a central barrier. The
# objective is to maneuver their spaceship to avoid incoming bullets while simultaneously
# firing bullets at the opponent's spaceship. Spaceships can move in four directions:
# up, down, left, and right, providing dynamic gameplay and strategic positioning.
#
# Key Features:
# - 2D Graphics: Utilizes Pygame for rendering spaceships, bullets, and the game environment.
# - Controls: Players use keyboard inputs to control their respective spaceships. One player
#   uses the W, A, S, and D keys for movement and a specific key (e.g., Spacebar) to shoot.
#   The other player uses the Arrow keys for movement and another key (e.g., Enter) to shoot.
# - Bullet Mechanics: Each spaceship can shoot a limited number of bullets at a time. Bullets
#   that hit the opponent's spaceship decrease its health.
# - Health System: Each spaceship has a health meter. Health decreases when a spaceship is hit
#   by an opponent's bullet. The game ends when one spaceship's health drops below zero,
#   declaring the other player as the winner.
# - Sound Effects: Includes audio feedback for shooting bullets and when spaceships are hit.
#
# End Game:
# The game concludes when the health of one spaceship is depleted to less than 0, at which
# point a victory message is displayed, announcing the winner. The game then resets, ready
# for another round of play.
#
# Author: Sujit Perla
##########################################################################################


pygame.font.init()  # to initialize the font module
pygame.mixer.init()  # to initialize the mixer module

# to set a screen of width 1000 and height 600, use the following syntax.
WIDTH, HEIGHT = 1000, 600
surface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Galactic Clash")  # to set a title of the window

# create a border of the width by 2 and y = 0 because it starts and ends at screen, height should be HEIGHT.
# the border is a rectangle, so use "pygame.Rect" and give it the x, y, w, h. The x is in the middle of the screen.
BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

FPS = 60
VEL = 4
VEL_OF_BULLETS = 6
MAX_BULLETS = 3

# to load the image of the spaceship, use the following syntax. use "pygame.image.load".
# use pygame.transform.scale to change the size of the image according to (w,h).
SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))

# to get the image of the spaceship onto the screen. use "os.path.join" to get the image from the file
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
# to change the size according to (w,h) and change the angle. use "pygame.transform.size" and "pygame.transform.angle"
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (55, 40)), 90)

# same process for the second spaceship
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (55, 40)), 270)

# make two empty lists for bullets of each spaceship
red_bullets = []
yellow_bullets = []

# to create a custom event, use the following syntax
RED_HIT = pygame.USEREVENT + 1
YELLOW_HIT = pygame.USEREVENT + 2

# to load the sound of the bullet and the hit, use the following syntax
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))


def draw_screen(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    """
    This function is used to draw the screen, the border, the spaceships and the bullets.
    the screen is refreshed every time the function is called.
    """
    # to paste the image onto the screen, use the ".blit" method and (w,h) for position.
    surface.blit(SPACE, (0, 0))

    pygame.draw.rect(surface, BLACK, BORDER)  # draw the border to the screen using the "pygame.draw.rect" method.

    # to create a font, use the "pygame.font.SysFont" method and give it the font and size.
    health_font = pygame.font.SysFont('comicsans', 40)

    # to render the text, use the "font.render" method and give it the text, antialiasing and color.
    # for antialiasing, you always put 1 as an argument
    red_health_text = health_font.render(f"Health: {red_health}", 1, WHITE)
    yellow_health_text = health_font.render(f"Health: {yellow_health}", 1, WHITE)

    # to paste the text onto the screen, use the ".blit" method.
    # for position, you get the width and height of the text. and the x and y coordinates.
    surface.blit(red_health_text, (10, 10))
    surface.blit(yellow_health_text, (WIDTH - red_health_text.get_width() - 10, 10))

    # instead of hard coding, use the rectangle x and y coordinates, so you can move the image
    surface.blit(RED_SPACESHIP, (red.x, red.y))
    surface.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))

    # to draw the bullets, use the "pygame.draw.rect" method and give it the surface, color and bullet.
    for bullet in red_bullets:
        pygame.draw.rect(surface, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(surface, YELLOW, bullet)

    # to automatically update the last window created use this method of the display key.
    pygame.display.flip()


def red_joystick(keys, red):
    """
    This function is used to move the red spaceship using the keys "a, w, s, d". The width and height of the spaceship
    is also checked to make sure it does not go off the screen. It moves according to the VEL.
    """
    # if the specific "a" key is pressed, the x pos of red is deduced by 3 spaces, to move it to the LEFT.
    if keys[pygame.K_a] and red.x - VEL > 0:  # check if it is not going off the screen to the left
        red.x -= VEL
    if keys[pygame.K_d] and red.x + VEL + red.width < BORDER.x:
        red.x += VEL
    if keys[pygame.K_w] and red.y - VEL > 0:
        red.y -= VEL
    if keys[pygame.K_s] and red.y + VEL + red.height < HEIGHT - 15:
        red.y += VEL


def yellow_joystick(keys, yellow):
    """
    This function is used to move the yellow spaceship using the keys "left, right, up, down".
    The width and height of the spaceship is also checked to make sure it does not go off the screen.
    It moves according to the VEL.
    """
    if keys[pygame.K_LEFT] and yellow.x - VEL > BORDER.x + BORDER.width:
        yellow.x -= VEL
    if keys[pygame.K_RIGHT] and yellow.x + VEL + yellow.width < WIDTH:
        yellow.x += VEL
    if keys[pygame.K_UP] and yellow.y - VEL > 0:
        yellow.y -= VEL
    if keys[pygame.K_DOWN] and yellow.y + VEL + yellow.height < HEIGHT - 15:
        yellow.y += VEL


def handle_bullets(red_bullets, yellow_bullets, red, yellow):
    """
    This function is used to handle the bullets of the spaceships. The bullets are moved to the right and left
    depending on the spaceship. The bullets are removed from the list if they collide with the spaceship
    or go off-screen.
    """
    for bullet in red_bullets:  # to loop through the list of bullets
        bullet.x += VEL_OF_BULLETS  # to move the bullet to the RIGHT
        if yellow.colliderect(bullet):  # to check if the bullet collided with anything  **
            pygame.event.post(pygame.event.Event(YELLOW_HIT))  # to post the event
            red_bullets.remove(bullet)  # first remove the bullet from the list
        elif bullet.x > WIDTH:
            red_bullets.remove(bullet)  # to remove the bullet from the list

    for bullet in yellow_bullets:  # to loop through the list of bullets
        bullet.x -= VEL_OF_BULLETS  # to move the bullet to the LEFT
        if red.colliderect(bullet):  # to check if the bullet collided with anything  **
            pygame.event.post(pygame.event.Event(RED_HIT))  # to post the event
            yellow_bullets.remove(bullet)  # first remove the bullet from the list
        elif bullet.x < 0:
            yellow_bullets.remove(bullet)  # to remove the bullet from the list


def winner(text):
    """
    This function is used to display the winner of the game. The text is rendered, and the position is set in the middle
    """
    # to create the winner font, use the "pygame.font.SysFont" method and give it the font and size.
    winner_font = pygame.font.SysFont('comicsans', 150)
    winner_text = winner_font.render(text, 1, WHITE)  # render the text, antialiasing and color.

    # to paste the text onto the screen, use the ".blit" method. for position, you get the width and height of the text.
    # and you divide it by 2 to get the middle of the screen.
    surface.blit(winner_text, (WIDTH / 2 - winner_text.get_width() / 2, HEIGHT / 2 - winner_text.get_height() / 2))
    pygame.display.flip()  # to automatically update the last window created
    pygame.time.delay(5000)  # to delay the game for 5 seconds


def main():
    # create a rectangle that can move, give it x_pos, y_pos and w, h.
    red = pygame.Rect(100, 300, 55, 40)
    yellow = pygame.Rect(700, 300, 55, 40)
    clock = pygame.time.Clock()  # this is for the speed of the game. remember the syntax

    # create the health of the spaceships
    red_health = 5
    yellow_health = 5

    # the first thing to do is write a function and start with while loop
    while True:
        clock.tick(FPS)  # sets the FPS to 60.
        # always start with a for loop, the syntax is just getting all types of events in pygame in a list.
        # loop through the list and check if the type of event is "pygame.QUIT", if yes break the loop.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # bullets are pygame rectangles, and are controlled by left/right cmd keys
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB and len(red_bullets) < MAX_BULLETS:  # to limit the number of bullets
                    BULLET_FIRE_SOUND.play()  # to play the sound of the bullet
                    red_bullet_pos = red.x + red.width  # to get the bullet to the right of the spaceship
                    # to get the bullet in the middle of the spaceship, use the following syntax
                    bullet = pygame.Rect(red_bullet_pos, red.y + red.height // 2 - 2, 10, 5)
                    red_bullets.append(bullet)  # to add the bullet to the list

                # same process for the yellow spaceship
                if event.key == pygame.K_SPACE and len(yellow_bullets) < MAX_BULLETS:
                    BULLET_FIRE_SOUND.play()
                    bullet = pygame.Rect(yellow.x, yellow.y + yellow.height // 2 - 2, 10, 5)
                    yellow_bullets.append(bullet)

            # code to handle when the bullet hits the spaceship
            if event.type == RED_HIT:
                BULLET_HIT_SOUND.play()  # to play the sound of the hit
                red_health -= 1

            if event.type == YELLOW_HIT:
                BULLET_HIT_SOUND.play()  # to play the sound of the hit
                yellow_health -= 1

        # to check if the health of the spaceships is less than 0, if yes, the game is over.
        txt = ""
        if red_health <= 0:
            txt = "Yellow Wins!"
        elif yellow_health <= 0:
            txt = "Red Wins!"
        if txt != "":
            winner(txt)
            break
        keys = pygame.key.get_pressed()  # to get a list of all keys that are pressed or can be pressed
        # call the functions to move the spaceships and handle the bullets
        red_joystick(keys, red)
        yellow_joystick(keys, yellow)
        draw_screen(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)
        handle_bullets(red_bullets, yellow_bullets, red, yellow)
    main()  # to restart the game


if __name__ == "__main__":
    main()
