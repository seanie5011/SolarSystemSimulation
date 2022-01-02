import pygame

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Solar System")

#---Framerate---#
clock = pygame.time.Clock()
FPS = 60

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

    pygame.display.update()

pygame.quit()
