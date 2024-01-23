import pygame
import math

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
DARK_GRAY = (75, 75, 75)
LIGHT_GRAY = (150, 150, 150)

# Field const
FIELD_WIDTH = 961
FIELD_HEIGHT = 727


# grid dist = 115

class Automator:
    """Path selection system"""

    def __init__(self):
        """Initialize automator"""
        # set up basic background
        self._init_pygame()
        # set base in-game vars
        self.selecting_start = True  # has the start been selected
        self.default_color = WHITE
        self.under_pathPoints = pygame.sprite.Group()
        self.pathPoints = pygame.sprite.Group()
        self.over_pathPoints = pygame.sprite.Group()
        self.prev_pathPoint = None
        self.clickable = True
        # make field
        self.field = Field(self.under_pathPoints, (0, 0))
        # make info boxes
        self.infobox = InfoBox(self.under_pathPoints, 100, (FIELD_WIDTH // 2, FIELD_HEIGHT + 75),
                               "Set the starting position", 'freesansbold.ttf', 32)
        self.codeBox = InfoBox(self.under_pathPoints, 700, (FIELD_WIDTH + 200, 400),
                               "Code will be here", 'JetBrainsMonoNL-Light.ttf', 15, width=350)
        # create finish button
        self.fin_button = FinishButton(self.under_pathPoints, height=40,
                                       location=(FIELD_WIDTH - 200, FIELD_HEIGHT + 75), initial_text="Finish path",
                                       font='freesansbold.ttf', size=28, width=225)
        # add starting points
        for x_pos in range(195, 771, 115):
            PathPoint(self.pathPoints, (x_pos, 650), DARK_GRAY, LIGHT_GRAY)  # 80, 650
    def main_loop(self):
        """Main loop of the program"""
        while True:
            self._handle_input()
            self._process_game_logic()
            self._draw()

    def _init_pygame(self):
        """Set up pygame window"""
        pygame.init()
        self.size = (FIELD_WIDTH + 400, FIELD_HEIGHT + 200)
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Path Automator")
        # fps counter
        self.clock = pygame.time.Clock()

    def _handle_input(self):
        """One of the main 3 parts of our main loop, handles all input"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_click(pygame.mouse.get_pos())

    def _process_game_logic(self):
        """Updates all sprites"""
        # update PathPoint sprites
        self.pathPoints.update()
        # update under sprites
        self.under_pathPoints.update()
        # update over sprites
        self.over_pathPoints.update()

    def _draw(self):
        """Draws all sprites to screen"""
        # set screen to default
        self.screen.fill(self.default_color)
        # draw sprites under PathPoints
        self.under_pathPoints.draw(self.screen)
        # draw PathPoint sprites
        self.pathPoints.draw(self.screen)
        # draw sprites over PathPoints
        self.over_pathPoints.draw(self.screen)
        # display images
        pygame.display.flip()
        # wait 1/60 of a second
        self.clock.tick(60)

    def _handle_click(self, mouse_pos):
        """Handles all clicks"""
        # check if accepting clicks
        if not self.clickable:
            return
        # check if any PathPoint was clicked
        for pathPoint in self.pathPoints:
            if pathPoint.is_in(mouse_pos):
                # check if start point has been selected
                if self.selecting_start:
                    self.logic = Logic(pathPoint.get_pos())  # set up logic system (code generation)
                    self._fill_field()  # add all remaining PathPoints to field
                    self.infobox.set_text("Select the path")  # change infoBox
                    self.selecting_start = False
                else:
                    self.logic.move_to(pathPoint.get_pos())  # add next point to logic
                    PathLine(self.over_pathPoints, self.prev_pathPoint.get_pos(), pathPoint.get_pos(),
                             ORANGE)  # create line between previous and new point
                self.prev_pathPoint = pathPoint
                pathPoint.set_selected()  # make sure PathPoint is marked as clicked
                self.codeBox.set_text(self.logic.print_code())  # add new code to code box
                break  # only one PathPoint can be clicked at a time
        if self.fin_button.is_in(mouse_pos) and not self.selecting_start:
            self.infobox.set_text("Finished, copied to clipboard")
            print(self.logic.print_code())
            self.clickable = False

    def _fill_field(self):
        """Add every PathPoint that is not in the starting set"""
        # middle square
        for y_pos in range(77, 593, 57):
            for x_pos in range(138, 771, 57):
                PathPoint(self.pathPoints, (x_pos, y_pos), DARK_GRAY, LIGHT_GRAY)  # 80, 650
        # fill in starting row
        for x_pos in range(138, 828, 114):
            PathPoint(self.pathPoints, (x_pos, 650), DARK_GRAY, LIGHT_GRAY)
        # fill in left square
        for y_pos in range(134, 593, 57):
            PathPoint(self.pathPoints, (80, y_pos), DARK_GRAY, LIGHT_GRAY)
        # fill in right square
        for y_pos in range(362, 593, 57):
            for x_pos in range(827, 885, 57):
                PathPoint(self.pathPoints, (x_pos, y_pos), DARK_GRAY, LIGHT_GRAY)


class Field(pygame.sprite.Sprite):
    """Sprite for background image (field)"""

    def __init__(self, group, location):
        super().__init__(group)
        self.image = pygame.image.load("Full_Volume_field.png")
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


class InfoBox(pygame.sprite.Sprite):
    """Sprite for text box with information"""

    def __init__(self, group, height, location, initial_text, font, size, width=FIELD_WIDTH):
        """Initialize text box"""

        super().__init__(group)
        # set base vars
        self.LINE_LENGTH = 10
        self.COLOR = WHITE
        self.size = size + round(size / 3)
        self.font = pygame.font.Font(font, size)
        self.text = initial_text
        self.width = width
        self.height = height
        # create surface to write text to
        self.image = pygame.surface.Surface((width, height))
        self.image.fill(self.COLOR)
        # get and set location
        self.rect = self.image.get_rect()
        self.rect.center = location
        # set initial text
        self.set_text(initial_text)

    def set_text(self, text):
        """Set text of textbox"""

        self.image.fill(self.COLOR)  # fill entire box to white
        self.text = [x for x in text.split("\n") if x != '']  #
        if len(self.text) > 22:
            self.text = self.text[-22:]
        prev_cent = self.rect.center
        height = 1
        for line in self.text:
            text_line = self.font.render(line, True, BLACK)
            self.image.blit(text_line, (20, height))
            height += self.size + self.LINE_LENGTH
        self.rect = self.image.get_rect()
        self.rect.center = prev_cent


class PathPoint(pygame.sprite.Sprite):
    """Sprite for every point on the map that can be clicked by the user"""

    def __init__(self, group, location, color, hover_color):
        super().__init__(group)
        self.RADIUS = 15
        self.TRANSPARENCY = 175
        self.image = pygame.surface.Surface((self.RADIUS * 2, self.RADIUS * 2), pygame.SRCALPHA, 32)
        self.image = self.image.convert_alpha()
        self.color = (color[0], color[1], color[2], self.TRANSPARENCY)
        self.hover_color = (hover_color[0], hover_color[1], hover_color[2], self.TRANSPARENCY)
        self.cur_color = 1  # 1 = normal color, -1 = hover color
        pygame.draw.circle(self.image, self.color, (self.RADIUS, self.RADIUS), self.RADIUS)
        # set position
        self.rect = self.image.get_rect()
        self.rect.center = location
        # state variables
        self.selected = False

    def update(self):
        if self.selected:
            return
        mouse_pos = pygame.mouse.get_pos()
        if self.is_in(mouse_pos):
            self.image.fill((0, 0, 0, 0))
            pygame.draw.circle(self.image, self.hover_color, (self.RADIUS, self.RADIUS), self.RADIUS)
            self.cur_color = -1
        elif self.cur_color == -1:
            self.image.fill((0, 0, 0, 0))
            pygame.draw.circle(self.image, self.color, (self.RADIUS, self.RADIUS), self.RADIUS)
            self.cur_color = 1

    def is_in(self, mouse_pos):
        """Check if mouse position is inside the PathPoint (over it)"""
        if math.sqrt(
                (self.rect.center[0] - mouse_pos[0]) ** 2 + (
                        self.rect.center[1] - mouse_pos[1]) ** 2) <= self.RADIUS: return True
        return False

    def __str__(self):
        return f"PathPoint at {self.rect.center}"

    def set_selected(self):
        """Make PathPoint orange after it's clicked"""
        self.image.fill((0, 0, 0, 0))
        pygame.draw.circle(self.image, ORANGE, (self.RADIUS, self.RADIUS), self.RADIUS)
        self.selected = True

    def get_pos(self):
        return self.rect.center


class PathLine(pygame.sprite.Sprite):
    """Sprite for lines connecting path points"""

    def __init__(self, group, p1, p2, color):
        super().__init__(group)
        self.p1 = p1
        self.p2 = p2
        self.color = color
        self.color = (color[0], color[1], color[2], 255)
        self.image = pygame.surface.Surface((abs(p1[0] - p2[0]) + 10, abs(p1[1] - p2[1]) + 10), pygame.SRCALPHA, 32)
        self.image = self.image.convert_alpha()
        # pick how to draw line
        if self.p1[1] < self.p2[1]:
            if self.p1[0] < self.p2[0]:
                pygame.draw.line(self.image, self.color, (0, 0), (abs(p1[0] - p2[0]), abs(p1[1] - p2[1])), width=10)
            else:
                pygame.draw.line(self.image, self.color, (abs(p1[0] - p2[0]), 0), (0, abs(p1[1] - p2[1])), width=10)
        else:
            if self.p2[0] < self.p1[0]:
                pygame.draw.line(self.image, self.color, (0, 0), (abs(p1[0] - p2[0]), abs(p1[1] - p2[1])), width=10)
            else:
                pygame.draw.line(self.image, self.color, (abs(p1[0] - p2[0]), 0), (0, abs(p1[1] - p2[1])), width=10)
        # set position
        self.rect = self.image.get_rect()
        self.rect.center = (p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2

    def __str__(self):
        return f"PathLine at points {self.p1} and {self.p2}; center {self.rect.center}"


class Logic:
    """Class to handle creating the code"""

    def __init__(self, s_pos):
        self.points = []  # list of visited points
        self.code = []  # code for bot
        self.bot_dir = 0  # bot direction (0-360)
        self.points.append(s_pos)  # add starting point

    def move_to(self, pos):
        """Calculates necessary movements for robot to get to a point"""
        codeBit = ""  # lines of code we will add to main code
        prev_pos = self.points[-1]  # point bot starts at
        y_chng = prev_pos[1] - pos[1]
        x_chng = prev_pos[0] - pos[0]
        rot = (math.atan2(x_chng,
                          y_chng) * 180 / math.pi * -1) % 360  # conv to degrees and mult by -1 to correct for coord
        # layout, mod 360 to convert into our units
        # check whether turning right or left is faster
        if (self.bot_dir - rot) % 360 < (rot - self.bot_dir) % 360:
            rot_chng = -((self.bot_dir - rot) % 360)
        else:
            rot_chng = (rot - self.bot_dir) % 360
        # add turn code to program
        if rot_chng < 0:
            codeBit += f"gyro_turn(-{abs(rot_chng)}, {5})"
        elif rot_chng > 0:
            codeBit += f"gyro_turn({abs(rot_chng)}, {5})"
        self.bot_dir = rot  # since we already moved by rot_chng, our bot should be a rot rotation
        dist = round(
            math.sqrt(x_chng ** 2 + y_chng ** 2) * 2.6)  # conv rate between our units and mm is 300/115 or approx 2.6
        codeBit += f"\nforward({dist})"  # add forward movement to bot
        self.points.append(pos)  # add new points to points
        self.code.append(codeBit)  # add code lines to main code

    def print_code(self):
        """Returns the full code for the bot"""
        return "\n".join(self.code)


class FinishButton(InfoBox):
    """Button for ending path"""

    def __init__(self, group, height, location, initial_text, font, size, width=FIELD_WIDTH):
        # most is copied from InfoBox class
        super().__init__(group, height, location, initial_text, font, size, width=width)

    def update(self):
        """Allow button to change color when mouse is over it"""
        m_pos = pygame.mouse.get_pos()
        if self.is_in(m_pos):
            self.COLOR = LIGHT_GRAY
            self.set_text("\n".join(self.text))
        elif self.COLOR == LIGHT_GRAY:
            self.COLOR = WHITE
            self.set_text("\n".join(self.text))

    def is_in(self, pos):
        """Check if point is in finish button"""
        center = self.rect.center
        if (center[0] - self.width // 2 <= pos[0] <= center[0] + self.width // 2) and (
                center[1] - self.height // 2 <= pos[1] <= center[1] + self.height // 2):
            return True
        else:
            return False


a = Automator()
a.main_loop()
