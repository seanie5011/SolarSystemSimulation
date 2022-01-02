import pygame

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("slider")

#---Framerate---#
clock = pygame.time.Clock()
FPS = 60

#----Define Colours---#
BG = (144, 201, 120)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PINK = (235, 65, 54)
YELLOW = (236, 232, 11)

#---Define Fonts---#
MainFont = pygame.font.SysFont("Futura", 30)

#---Functions---#
def draw_text(text, font, text_colour, x, y, angle):
    img = pygame.transform.rotate(font.render(text, True, text_colour), angle)
    screen.blit(img, (x, y))

#---Classes---#
class Slider(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, colour, direction):
        pygame.sprite.Sprite.__init__(self)

        self.ogx = x
        self.ogy = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.colour = colour
        self.direction = direction.upper()

        self.rect = pygame.draw.rect(screen, self.colour, (self.x, self.y, self.width, self.height))
        self.rect.center = (self.x, self.y)

        self.clicked = False
        self.value = 50.0
        self.value2 = 50.0

    def checkclick(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.x - self.width / 2 < mouse_pos[0] < self.x + self.width / 2 and self.y - self.height / 2 < mouse_pos[1] < self.y + self.height / 2:
            self.clicked = True

    def unclick(self):
        self.clicked = False

    def update(self):
        if self.clicked == True:
            mouse_pos = pygame.mouse.get_pos()
            if self.direction == "HORIZONTAL":
                if self.ogx - 150 <= mouse_pos[0] <= self.ogx + 150:
                    self.x = mouse_pos[0]
                    self.value = (self.x - (self.ogx - 150)) * 100 / 300
            if self.direction == "VERTICAL":
                if self.ogy - 150 < mouse_pos[1] < self.ogy + 150:
                    self.y = mouse_pos[1]
                    self.value = -1 * (self.y - (self.ogy + 150)) * 100 / 300
            if self.direction == "BOTH":
                if self.ogx - 150 < mouse_pos[0] < self.ogx + 150 and self.ogy - 150 < mouse_pos[1] < self.ogy + 150:
                    self.x, self.y = mouse_pos
                    self.value = (self.x - (self.ogx - 150)) * 100 / 300 #x value
                    self.value2 = -1 * (self.y - (self.ogy + 150)) * 100 / 300 #y value

    def draw(self):
        if self.direction == "HORIZONTAL":
            pygame.draw.rect(screen, WHITE, (self.ogx - 150, self.ogy - 15, 300, 30), 0, 10)
            pygame.draw.rect(screen, self.colour, (self.ogx - 150, self.ogy - 15, 300, 30), 3, 10)
            
            draw_text(f"{self.value:0.2f}", MainFont, WHITE, self.ogx - 20, self.ogy - 50, 0)
        if self.direction == "VERTICAL":
            pygame.draw.rect(screen, WHITE, (self.ogx - 15, self.ogy - 150, 30, 300), 0, 10)
            pygame.draw.rect(screen, self.colour, (self.ogx - 15, self.ogy - 150, 30, 300), 3, 10)

            draw_text(f"{self.value:0.2f}", MainFont, WHITE, self.ogx - 20, self.ogy - 200, 0)
        if self.direction == "BOTH":
            pygame.draw.rect(screen, WHITE, (self.ogx - 150, self.ogy - 150, 300, 300), 0, 10)
            pygame.draw.rect(screen, self.colour, (self.ogx - 150, self.ogy - 150, 300, 300), 3, 10)

            draw_text(f"{self.value:0.2f}", MainFont, WHITE, self.ogx - 20, self.ogy - 200, 0)
            draw_text(f"{self.value2:0.2f}", MainFont, WHITE, self.ogx - 200, self.ogy - 20, 90) #angled 90 degrees

        self.rect.center = (self.x, self.y)
        pygame.draw.rect(screen, self.colour, self.rect)

slider = Slider(400, 400, 50, 50, RED, "vertical")
            
#---Main Game Loop---#
run = True
while run: #while run is true

    clock.tick(FPS)

    for event in pygame.event.get():
        #---Quit Game---#
        if event.type == pygame.QUIT:
            run = False
        #---Keys---#
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            slider.checkclick()

        if event.type == pygame.MOUSEBUTTONUP:
            slider.unclick()

    screen.fill(BLACK)

    slider.update()
    slider.draw()

    pygame.display.update()

pygame.quit()
