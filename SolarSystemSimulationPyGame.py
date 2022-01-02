import pygame

pygame.init()

SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 800

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Solar System")

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

#---Define Param---#
G = 6.6741*(10**(-11))
ratio = 20 / 149597870700 #20px = 1AU
oldratio = ratio
dt = 30000

#Sun body
xS = SCREEN_WIDTH / 2
yS = SCREEN_HEIGHT / 2
MS = 1.989*(10**30)

#---Load Images / Make Rects---#
sun_image = pygame.transform.scale(pygame.image.load(f"img\\sun.png").convert_alpha(), (10, 10))
sun_rect = sun_image.get_rect()
sun_rect.center = (xS, yS)

#---Classes---#
class PlanetCircle(pygame.sprite.Sprite):
    def __init__(self, vx, vy, x, y, M, R, displayR, colour):
        pygame.sprite.Sprite.__init__(self)

        self.vx = vx
        self.vy = vy
        self.x = x
        self.y = y
        self.M = M
        self.R = R
        self.displayR = displayR
        self.colour = colour

        self.rect = pygame.draw.circle(screen, colour, (xS + x * ratio, yS + y * ratio), displayR)

    def update(self):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.vx -= dt * (G * MS * self.x) / (((self.x**2 + self.y**2)**0.5)**3)
        self.vy -= dt * (G * MS * self.y) / (((self.x**2 + self.y**2)**0.5)**3)

        self.rect.center = (xS + self.x * ratio, yS + self.y * ratio)

    def draw(self):
        pygame.draw.circle(screen, self.colour, self.rect.center, self.displayR)

class PlanetImage(pygame.sprite.Sprite):
    def __init__(self, vpe, pe, ap, a, b, M, R, planet, displayR):
        pygame.sprite.Sprite.__init__(self)

        self.vx = 0
        self.vy = vpe
        self.x = pe
        self.y = 0
        self.vpe = vpe
        self.pe = pe
        self.ap = ap
        self.a = a
        self.b = b
        self.M = M
        self.R = R
        self.displayR = displayR
        self.planet = planet
        self.changevar = False

        img = pygame.image.load(f"img\\Planets\\{planet}").convert_alpha() #f string for easy path
        self.image = pygame.transform.scale(img, (displayR * 2, displayR * 2))

        self.rect = self.image.get_rect()
        self.rect.center = (xS + self.x * ratio, yS + self.y * ratio)

    def update(self):
        self.x += self.vx * dt #ensure in this order as others are unstable
        self.y += self.vy * dt
        self.vx -= dt * (G * MS * self.x) / (((self.x**2 + self.y**2)**0.5)**3)
        self.vy -= dt * (G * MS * self.y) / (((self.x**2 + self.y**2)**0.5)**3)

        if self.changevar == True:
            self.change()
            self.changevar = False

        self.rect.center = (xS + self.x * ratio, yS + self.y * ratio)

        self.draw()

    def draw(self):
        if self.pe * ratio + xS < SCREEN_WIDTH and self.pe * ratio + xS > 0: #still messes up when moving left/right/up/down AND zooming in/out at the same time, bug on pygame.draw.ellipse part?
            #draw trail
            pygame.draw.ellipse(screen, WHITE, (xS - self.ap * ratio, yS - self.b * ratio, 2 * self.a * ratio, 2 * self.b * ratio), 1) #display, colour, (left, top, width, height)
        #draw planet
        screen.blit(self.image, self.rect)

    def change(self):
        img = pygame.image.load(f"img\\Planets\\{self.planet}").convert_alpha() #f string for easy path
        self.image = pygame.transform.scale(img, (int(self.displayR * 2 * ratio/oldratio), int(self.displayR * 2 * ratio/oldratio)))

        self.rect = self.image.get_rect()

mercury = PlanetImage(61826, 4.3*(10**10), 7.0*(10**10), 5.65*(10**10), 5.49*(10**10), 3.285*(10**23), 2439700, "mercury.png", 1) #vpe, pe, ap, a, b, M, R, planet, displayR
venus = PlanetImage(35252, 1.07*(10**11), 1.09*(10**11), 1.08*(10**11), 1.08*(10**11), 4.867*(10**24), 6051800, "venus.png", 3)
earth = PlanetImage(30282, 1.47*(10**11), 1.52*(10**11), 1.5*(10**11), 1.5*(10**11), 5.972*(10**24), 6371000, "earth.png", 4)
mars = PlanetImage(26489, 2.07*(10**11), 2.49*(10**11), 2.28*(10**11), 2.27*(10**11), 6.39*(10**23), 3389500, "mars.png", 2)
jupiter = PlanetImage(13708, 7.41*(10**11), 8.17*(10**11), 7.79*(10**11), 7.78*(10**11), 1.898*(10**27), 69911000, "jupiter.png", 20)
saturn = PlanetImage(10180, 1.35*(10**12), 1.51*(10**12), 1.43*(10**12), 1.43*(10**12), 5.683*(10**26), 58232000, "saturn.png", 15)
uranus = PlanetImage(7115, 2.74*(10**12), 3.01*(10**12), 2.88*(10**12), 2.87*(10**12), 8.681*(10**25), 25362000, "uranus.png", 12)
neptune = PlanetImage(5478, 4.46*(10**12), 4.54*(10**12), 4.50*(10**12), 4.50*(10**12), 1.024*(10**26), 24622000, "neptune.png", 10)

#---Create Sprite Groups---#
planet_group = pygame.sprite.Group()

#-Planet Group-#
planet_group.add(mercury, venus, earth, mars, jupiter, saturn, uranus, neptune)

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

            if event.key == pygame.K_z: #zoom in
                for planet in planet_group:
                    planet.changevar = True

                sun_image = pygame.transform.scale(pygame.image.load(f"img\\sun.png").convert_alpha(), (int(10 * ratio/oldratio), int(10 * ratio/oldratio)))
                sun_rect = sun_image.get_rect()
                sun_rect.center = (xS, yS)

                ratio += 10 / 149597870700
            if event.key == pygame.K_x: #zoom out
                for planet in planet_group:
                    planet.changevar = True #change planet scale

                sun_image = pygame.transform.scale(pygame.image.load(f"img\\sun.png").convert_alpha(), (int(10 * ratio/oldratio), int(10 * ratio/oldratio))) #change sun scale
                sun_rect = sun_image.get_rect()
                sun_rect.center = (xS, yS)

                ratio -= 10 / 149597870700

            if event.key == pygame.K_i: #go up
                yS += 20
                for planet in planet_group:
                    planet.changevar = True

                sun_image = pygame.transform.scale(pygame.image.load(f"img\\sun.png").convert_alpha(), (int(10 * ratio/oldratio), int(10 * ratio/oldratio)))
                sun_rect = sun_image.get_rect()
                sun_rect.center = (xS, yS)
            if event.key == pygame.K_k: #go down
                yS -= 20
                for planet in planet_group:
                    planet.changevar = True

                sun_image = pygame.transform.scale(pygame.image.load(f"img\\sun.png").convert_alpha(), (int(10 * ratio/oldratio), int(10 * ratio/oldratio)))
                sun_rect = sun_image.get_rect()
                sun_rect.center = (xS, yS)
            if event.key == pygame.K_j: #go left
                xS += 20
                for planet in planet_group:
                    planet.changevar = True

                sun_image = pygame.transform.scale(pygame.image.load(f"img\\sun.png").convert_alpha(), (int(10 * ratio/oldratio), int(10 * ratio/oldratio)))
                sun_rect = sun_image.get_rect()
                sun_rect.center = (xS, yS)
            if event.key == pygame.K_l: #go right
                xS -= 20
                for planet in planet_group:
                    planet.changevar = True

                sun_image = pygame.transform.scale(pygame.image.load(f"img\\sun.png").convert_alpha(), (int(10 * ratio/oldratio), int(10 * ratio/oldratio)))
                sun_rect = sun_image.get_rect()
                sun_rect.center = (xS, yS)

    screen.fill(BLACK)

    screen.blit(sun_image, sun_rect)

    planet_group.update()

    pygame.display.update()

pygame.quit()
