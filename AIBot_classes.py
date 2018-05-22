import pygame
from AIBot_constants import *
import random

# This class represents the player on the screen
# It inherits PyGame's "Sprite" class (Sprite=Superclass; Player=Subclass)
class Robot(pygame.sprite.Sprite):

    def __init__(self, image):
        # Call the parent class (Sprite) constructor
        super().__init__()
        # Load the image from the disk.
        self.image = pygame.image.load(image).convert_alpha()
        #self.image.set_colorkey(BLACK)


class AIBot(Robot):
    def __init__(self, image, startX, startY, heading, speed, mapList):
        super(AIBot, self).__init__(image)
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.original_image = self.image

        self.rect.x = startX
        self.rect.y = startY
        self.directionX = 0
        self.directionY = 0
        self.direction = "Forward"
        self.waitFrames = 999999
        self.heading = "DR"
        self.speed = speed
        self.mapList = mapList

    def scan(self, scanDirection):
        # Determine where AIbot is on the screen using center_x and center_y
        print("scan() method - get center_x and center_y -- not coded yet")

        moveCount = 0

        top_right_x, top_right_y = self.rect.topright
        bottom_right_x, bottom_right_y = self.rect.bottomright
        if scanDirection == "R":

            #row = int(top_right_y / self.rect.height)
            #col = int(top_right_x / self.rect.width)
            row = top_right_y
            col = top_right_x



            print("debug: rowCount - ", len(self.mapList), " colCount - ", len(self.mapList[0]))


            for i in range(row, len(self.mapList)):
                for j in range(col, len(self.mapList[i])):


                    #print("debug:  - row ", row, " col - ", col, "\n", " top_right_y: ", top_right_y, " top_right_x: ", top_right_x)
                    print("debug - i:", i, "j:", j)



                    if self.mapList[row][col] == 2:
                        break
                    col += 1
                    moveCount += 1
                row += 1

        print("MOVE COUNT - -MOVE COUNT: ", str(moveCount))
        return moveCount

        print("Not coded yet - scan in the specified direction using HALs width, center_x, center_y, and the direction passed into the scan method")


    def aI(self):
        heading = self.getHeading()


        """ Eventually the following decision logic should be pulled out into its own
            module/function for the students to code.
            The function will return heading, direction and waitframes
        """

        # Scan logic - Evaluate the mapList[] or call the scan() function
        distance = self.scan("R")
        print("Distance from Scan(\"R\"):", distance)
        if distance > 2000:
            heading = "R"


        # Temporary code to generate random direction.
        # Temporary code to generate random direction.
        # Temporary code to generate random direction.
        randomHeading = random.randint(1, 8)
        if randomHeading == 1:
            heading = "U"
        elif randomHeading == 2:
            heading = "UR"
        elif randomHeading == 3:
            heading = "R"
        elif randomHeading == 4:
            heading = "DR"
        elif randomHeading == 5:
            heading = "D"
        elif randomHeading == 6:
            heading = "DL"
        elif randomHeading == 7:
            heading = "L"
        elif randomHeading == 8:
            heading = "UL"


        """ Eventually the previous decision logic should be pulled out into its own
            module/function for the students to code.
            The function will return heading, direction and waitframes
        """

        directionX, directionY = self.setHeading(heading)
        self.setDirection("Forward")
        self.setWaitFrames(55)
        return directionX * self.speed, directionY * self.speed


    # Make AIBot move in a specific direction
    def setHeading(self, heading="R"):
        self.heading = heading

        if heading == "U":
            self.directionX = 0
            self.directionY = -1

        elif heading == "UR":
            self.directionX = 1
            self.directionY = -1

        elif heading == "R":
            self.directionX = 1
            self.directionY = 0

        elif heading == "DR":
            self.directionX = 1
            self.directionY = 1

        elif heading == "D":
            self.directionX = 0
            self.directionY = 1

        elif heading == "DL":
            self.directionX = -1
            self.directionY = 1

        elif heading == "L":
            self.directionX = -1
            self.directionY = 0

        elif heading == "UL":
            self.directionX = -1
            self.directionY = -1

        return self.directionX, self.directionY

    def setDirection(self, direction):
        self.direction = direction

    def getDirection(self):
        return self.direction

    def getHeading(self):
        return self.heading

    def setWaitFrames(self, frames):
        self.waitFrames = frames

    def rotate(self, direction, degrees):
        print("The rotate method will use trigonometry to allow for better control over AIBot.")

    """
    AIBot ROTATION LOGIC
    R O T A T I O N ---- ### R O T A T I O N ---- ### R O T A T I O N

    **** Save the original image  ****
    **** Save the original image  ****
    **** Save the original image  ****

     def __init__(self, pos=(0, 0), size=(200, 200)):
            super(Player, self).__init__()
            self.original_image = pygame.Surface(size)
            pygame.draw.line(self.original_image, (255, 0, 255), (size[0] / 2, 0), (size[0] / 2, size[1]), 3)
            pygame.draw.line(self.original_image, (0, 255, 255), (size[1], 0), (0, size[1]), 3)
            self.image = self.original_image
            self.rect = self.image.get_rect()
            self.rect.center = pos
            self.angle = 0

     def update(self):
            self.image = pygame.transform.rotate(self.original_image, self.angle)
            self.angle += 1 % 360  # Value will reapeat after 359. This prevents angle to overflow.
            x, y = self.rect.center  # Save its current center.
            self.rect = self.image.get_rect()  # Replace old rect with new rect.
            self.rect.center = (x, y)  # Put the new rect's center at old center.
    """

# This class represents the dots on the screen
# It inherits PyGame's "Sprite" class (Sprite=Superclass; Block=Subclass)
class Block(pygame.sprite.Sprite):

    # Constructor.
    """Pass in the block type, block color, and its x and y position.
        ** Block type 1: circles, destroyed upon collide with Player.
        ** Block type 2: blocks that stop the Player when they collide.
    """
    def __init__(self, type, color, width, height, row, col):
        # Call the parent class (Sprite) constructor
        super().__init__()

        # Create block image, and fill it with a color.
        self.type = type
        self.image = pygame.Surface([width, height])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)
        self.row = row
        self.col = col

        # Modify row and column values to remove spacing for height and width
        #   if necessary.
        if self.row > 10:
            self.row = int(self.row / height)
        if self.col > 10:
            self.col = int(self.col / width)
        self.waitFrames = 99999

        if type == 1:
            pygame.draw.ellipse(self.image, color, [0, 0, width, height])
        elif type == 2:
            pygame.draw.rect(self.image, color, (50, 50, width, height), 1)
            self.image.fill(color)
        else:
            print("Error - Unknown type passed into the Block class")

        # Fetch the rectangle object that has the dimensions of the image.
        # Update position by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect()
