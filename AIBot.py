#  INITIAL SOURCE CODE
# Sample Python/Pygame Programs
# Simpson College Computer Science
# http://programarcadegames.com/
# http://simpson.edu/computer-science/

#  ---  Modified by Steve Stoll 2017-18  ---

"""
                ot              II                             IBo
                AI              Bo                             otA
                                tAI              otAI-BotA     AI-
   BotAI-BotAI  ot              I-BotAI-BotA    tAI-BotAI-B   I-BotAI-Bo
            -B  AI   tAI-BotAI  Bot      AI-B  AI-       otA   otA
    -BotAI-Bot  -B   I-BotAI-B  tA        Bot  -B        AI-   AI-
  -BotAI-BotAI  ot              I-         AI  ot        -Bo   -Bo
  ot        -B  AI              Bo        I-B  AI-       otA   otA
  AI-BotAI-Bot  -B              tAI-BotAI-Bo   -BotAI-BotAI    AI-BotAI-
   BotAI-BotAI  ot              I-BotAI-Bot     tAI-BotAI-B     BotAI-Bo


GAME DESCRIPTION
================

Players create an AI script to control the movement of a Sprite in order to cover
    as much of the screen as possible.  The screen will have obsticles (barriers)
    around which AIBot will need to navigate.

Player's will use these these commands to manipulate AIBot:
    - forward()     *** Moves AIBot forward.  May include the # of pixels to move.
    - reverse()     *** Moves AIBot in reverse. Need to include the number of
                        pixels to move (probably limit to twenty pixels).
    - heading(angle?)   *** Move AI -Bot in one of the eight symetrical directions.
    - rotate(radians)  *** An improved version of direction that will be
                            implemented at a later date.
Modules / Functions
There are two primary files used for this:
    1) A driver module named AIBot.py that creates the screen, tracks the player
        score, and the parts of the screen that have been covered. The coverage
        will be tracked using a 2d array (Python list).
    2) Students will create a sub-class that inherits from AIBot.py
    3) Students will override the aI() method to control their robot. The aI() method
        that will be executed every so many frames (game loop iterations).

Example:
- AIBot.py:
1) imports AIBot_classes.py and AIBot_constants.py (among other modules)
2) Create the game board, scoreing blocks, barriers and AIBot.
3) Create mapList[]. 2d array of screen (each cell represents 10x10 pixel square). Values
    1s - AIBot has not been here yet.
    2s - Indicate barriers.
    0s - AIBot has been here.

4) Starts the timer
5) The player's Sprite (inherited from AIBot), "Block" Sprites that are consumed by
    AIBot, and barrier Sprites are displayed on the screen.
6) Each game loop (frame), zero to many of the player commands will be executed, the

7) Every so many loop iterations, or when a collision with a barrier occurs, the
    player aI() function will be called.  This function will analyze the mapList[]
    and tell AIBot what to do next.
8) When the timer reaches a specific value, game over screen is displayed. It would be nice
    if the "score" and "possible score" displayed here.
Challenges:
    - If AIBot is trying to go around a barrier, how does it know when it has gone
        covered that side of the barrier (when it is time to turn).
            - Maybe we need to add a bump() function that will allow AIBot to move
                to side, determining if a collision occurs.  When there is no
                collision, AIBot should know it is time to turn.
    - Calculating "Possible Score" is complex.  It will be difficult to calculate
        a perfect run by AIBot, covering the entire screen.
    - direction() Should I use the trig angles, compass angles, or protractor?
        Keep in mind, direction() is the simple function that will move in only
        eight directions.  A rotate() function will be written at a later date.
"""

import pygame
import random
from AIBot_classes import *
from AIBot_constants import *

# Initialize Pygame
pygame.init()

BLOCK_WIDTH = 10
BLOCK_HEIGHT = 10
BOUNCE_PIXELS = 20

START_X = 20
START_Y = 1
SPEED = 10
START_HEADING = "R"
START_DIRECTION = "Forward"

estimated_block_gap = int((BLOCK_WIDTH + BLOCK_HEIGHT) / 2)

# Set the height and width of the screen
SCREEN_WIDTH  = 1000
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT])

# This is a list of 'sprites.' Each block in the program is
# added to this list. The list is managed by a class called 'Group.'
block_list = pygame.sprite.Group()
barrier_list = pygame.sprite.Group()

# This is a list of every sprite. (Including barriers and AIBot)
all_sprites_list = pygame.sprite.Group()

###MAP
# Create a 2d list that acts like a map of the screen (used by aI() functions)
mapList = []
for i in range(0, int(SCREEN_HEIGHT / BLOCK_HEIGHT)):
    mapList.append([])
    for j in range(0, int(SCREEN_WIDTH / BLOCK_WIDTH)):
        mapList[i].append(1)


#  Create the type 1 array of Blocks (circles in this case) on the screen.
for row in range(0, SCREEN_HEIGHT, BLOCK_HEIGHT):  #estimated_block_gap
    for col in range(0, SCREEN_WIDTH, BLOCK_WIDTH): #estimated_block_gap

        # This represents a block
        block = Block(1, GREEN_TRANSPARENT, BLOCK_WIDTH, BLOCK_HEIGHT, row, col)

        # Set the location for the block
        block.rect.y = row
        block.rect.x = col
        ##print("Row:", row, "Col:", col)

        # Add the block to the list of objects
        block_list.add(block)
        all_sprites_list.add(block)

# Create an image AIBot block
bot = AIBot("robot_square.png", START_X, START_Y, START_HEADING, SPEED, mapList)

all_sprites_list.add(bot)

# Draw the walls using values: 1=Top; 2=Right; 3=bottom; 4=Left
for i in range(1, 5):
    #  Create type 2 WALL (barrier) BLOCKS (blue) at screen edges.
    if i == 1 or i == 3:
        block = Block(2, BLUE, SCREEN_WIDTH, 5, 0, 0)
    elif i ==2 or i == 4:
        block = Block(2, BLUE, 5, SCREEN_HEIGHT, 0, 0)

    # Set the location of the "x" variables for the walls
    if i == 2:
        block.rect.x = SCREEN_WIDTH - 5
    else:
        block.rect.x = 0
    # Set the location of the "y" variables for the walls
    if i == 3:
        block.rect.y = SCREEN_HEIGHT - 5
    else:
        block.rect.y = 0

    # Add the block to the list of objects
    barrier_list.add(block)
    all_sprites_list.add(block)

#  Create the type 2 barrier Blocks (red rectangles) on the screen.
for i in range(5, 1, -1):
    # Generate random numbers used to place the block on the screen
    #random_x = random.randint(200, (SCREEN_WIDTH - 210))
    #random_y = random.randint(50, (SCREEN_HEIGHT - 60))

    random_x = i * 100
    random_y = i * 150


    barrier_width = 200
    barrier_height = 50
    barrier_x = int(random_x / BLOCK_WIDTH)
    barrier_y = int(random_y /  BLOCK_HEIGHT)

    # This represents a barrier block  int(random_y / BLOCK_HEIGHT gives us the row...)
    block = Block(2, RED, barrier_width, barrier_height, barrier_x, barrier_y)
    ###print("Barrier Block Row:", block.row, "Barrier Block Column", block.col)

    # Update the mapList[]
    for row in range(barrier_y, int(barrier_y + barrier_height / BLOCK_HEIGHT)):
        for col in range(barrier_x, int(barrier_x + barrier_width / BLOCK_WIDTH)):
            mapList[row][col] = 2

    # Set the location for the block
    block.rect.x = random_x
    block.rect.y = random_y

    # Add the block to the list of objects
    barrier_list.add(block)
    all_sprites_list.add(block)

#Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

score = 0
x_speed = SPEED
y_speed = SPEED

# -------- Main Program Loop -----------
while done == False:
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done = True # Flag that we are done so we exit this loop

        elif event.type == pygame.KEYDOWN:
            # Figure out if it was an arrow key. If so
            # adjust speed.
            if event.key == pygame.K_LEFT:
                x_speed = -SPEED
            elif event.key == pygame.K_RIGHT:
                x_speed = SPEED
            elif event.key == pygame.K_UP:
                y_speed = -SPEED
            elif event.key == pygame.K_DOWN:
                y_speed = SPEED

            # Rotation using "f" (rotate right) and "d" (rotate left)
            elif event.key == pygame.K_d:
                x_temp = bot.rect.x
                y_temp = bot.rect.y
                bot.image = pygame.transform.rotate(bot.image, 90)
                bot.rect = bot.image.get_rect()
                bot.rect.x = x_temp
                bot.rect.y = y_temp
            elif event.key == pygame.K_f:
                x_temp = bot.rect.x
                y_temp = bot.rect.y
                bot.image = pygame.transform.rotate(bot.image, 270)
                bot.rect = bot.image.get_rect()
                bot.rect.x = x_temp
                bot.rect.y = y_temp
        # User let up on a key
        elif event.type == pygame.KEYUP:
            # If it is an arrow key, reset vector back to zero
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                x_speed = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                y_speed = 0

    bot.rect.x += x_speed
    bot.rect.y += y_speed

   # Clear the screen
    screen.fill(DARK_GREEN)


    # See if AIBot has collided with anything.
    blocks_hit_list = pygame.sprite.spritecollide(bot, block_list, False)

    # Check the list of collisions.
    for block in blocks_hit_list:
        score +=1
        print(score,"- block sprites deleted.")
        mapList[block.row][block.col] = 0
        block.kill()

    blocks_hit_barrier_list = pygame.sprite.spritecollide(bot, barrier_list, False)


    #blocks_hit_list = pygame.sprite.groupcollide(blueSpriteGroup, redSpriteGroup, False, False)


    # Check the list of collisions if collision occurs, bounce back BOUNCE_PIXELS amount.
    if len(blocks_hit_barrier_list) > 0:
        if x_speed > 0:
            bot.rect.x -= BOUNCE_PIXELS
        elif x_speed < 0:
            bot.rect.x += BOUNCE_PIXELS

        if y_speed > 0:
            bot.rect.y -= BOUNCE_PIXELS
        elif y_speed < 0:
            bot.rect.y += BOUNCE_PIXELS

        # Call aI() here
        x_speed, y_speed = bot.aI()

    # Draw all the spites
    all_sprites_list.draw(screen)
    barrier_list.draw(screen)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # Limit to 26 frames per second
    clock.tick(26)


# Print mapList for debugging
print("Modified mapList:")
mapListCounter = 0
while mapListCounter < len(mapList):
    print(mapList[mapListCounter])
    mapListCounter += 1


pygame.quit()