import pygame, os, random

# Untuk USEREVENT
from pygame.locals import * 

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()

# Windows and game 
sWidth = 500
sHeight =  500
DS = pygame.display.set_mode((sWidth, sHeight))
pygame.display.set_caption("Flappy Bird Concepts")

CLOCK = pygame.time.Clock()
FPS = 30
pygame.time.set_timer(USEREVENT+1, random.randrange(3000, 5000))

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Backgrounds and images
bg = pygame.transform.scale(pygame.image.load(os.path.join("assets", "mountain.png")).convert(), (sWidth, sHeight))
bgX = 0
bgX2 = sWidth

# Fonts and sounds
myfont = pygame.font.SysFont("Calibri", 30, True, True)
overFont = pygame.font.SysFont("Calibri", 40, True)
hpFont = pygame.font.SysFont("Calibri", 20, True)
scoreSound = pygame.mixer.Sound(os.path.join("assets","score.wav"))
hurtSound = pygame.mixer.Sound(os.path.join("assets", "hurt.wav"))

class character(object):
    images = [pygame.transform.scale(pygame.image.load(os.path.join("assets\\bird", str(x) + ".png")).convert_alpha(), (70, 50)) for x in range(1, 9)]
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hitbox = (self.x, self.y, self.width, self.height)
        self.fallSpeed = 2
        self.jumpSpeed = 8
        self.coolDown = 0
        self.animationCount = 0
        self.jumping = False
        self.lifePoints = 5
        self.hitCooldown = 0

    def draw(self, DS):
        if self.jumping:
            if self.animationCount > 23:
                self.animationCount = 0
            DS.blit(pygame.transform.rotate(self.images[self.animationCount//3], 20), (self.x, self.y))
            self.animationCount += 1
        else:
            # Display character animation for every 3 frames in the game
            if self.animationCount > 23:
                self.animationCount = 0
            DS.blit(self.images[self.animationCount//3], (self.x, self.y))
            self.animationCount += 1

        self.hitbox = (self.x, self.y, self.width, self.height)
        pygame.draw.rect(DS, WHITE, self.hitbox, 2)
        
        # HP Bar
        pygame.draw.rect(DS, RED, (30, 30, 200, 20), 0)
        pygame.draw.rect(DS, GREEN, (30, 30, (self.lifePoints/5 * 200), 20), 0)

class pipes(object):
    # Convert alpha to retain transparency
    image = pygame.transform.scale(pygame.image.load(os.path.join("assets", "pipe.png")).convert_alpha(), (64, 200))
    def __init__(self, x, y, width, height, flipped):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hitbox = (self.x, self.y, self.width, self.height)
        self.flipped = flipped
        self.scored = False

    def draw(self, DS):
        self.hitbox = (self.x, self.y, self.width, self.height)
        if not self.flipped:
            DS.blit(self.image, (self.x, self.y))
        else:
            DS.blit(pygame.transform.flip(self.image, False, True), (self.x, self.y))
        pygame.draw.rect(DS, WHITE, self.hitbox, 2)
    
    def collide(self, playerObj):
        if playerObj.hitbox[1] < self.hitbox[1] + self.hitbox[3] and playerObj.hitbox[1] + playerObj.hitbox[3] > self.hitbox[1]:
            if playerObj.hitbox[0] + playerObj.hitbox[2] > self.hitbox[0] and playerObj.hitbox[0] < self.hitbox[0] + self.hitbox[2]:
                # Benerin posisi bird saat nabrak
                if self.flipped:
                    playerObj.y = self.hitbox[1] + self.hitbox[3] + 1
                else:
                    playerObj.y = self.hitbox[1] - playerObj.hitbox[3] - 1
                return True
        return False

def gameOver(DS):
    overText = overFont.render("Game Over !", 1, BLACK)
    overRect = overText.get_rect()
    overRect.center = (sWidth//2, sHeight//2 - 25)
 
    descText = myfont.render("Press right click to restart the game!", 1, (0,0,0))
    descRect = descText.get_rect()
    descRect.center = (sWidth//2, sHeight//2 + 25)

    pausing = True
    while (pausing):
        CLOCK.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3: #Right click
                    return True

        DS.fill(WHITE)
        DS.blit(overText, overRect)
        DS.blit(descText, descRect)
        pygame.display.update()

def drawWindow(score):
    DS.blit(bg, (bgX, 0))
    DS.blit(bg, (bgX2, 0))

    for ob in obstacles:
        ob.draw(DS)

    scoreText = myfont.render('Score : ' + str(score), 1, BLACK, 1)
    textRect = scoreText.get_rect()
    textRect.center = (sWidth - 80, 40)
    DS.blit(scoreText, textRect)

    hpText = hpFont.render("Health", 1, BLACK)
    DS.blit(hpText, (30, 10))

    player.draw(DS) 
    pygame.display.update()

# Initialization characters and obstacles
player = character(100, 250, 70, 50)
obstacles = []

obstacles.append(pipes(200, 0, 64, 200, True))
obstacles.append(pipes(300, 300, 64, 200, False))

scrollingSpeed = 2.0
score = 0
restart = False

i = 0
# Main loop
run =  True
while run:
    if player.y >= sHeight or player.y + player.height < 0:
        player.lifePoints = 0

    if player.lifePoints == 0:
        restart = gameOver(DS)
        if not restart:
            run = False
        else:
            obstacles.clear()
            player.lifePoints = 5
            score = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
        
        if event.type == pygame.USEREVENT+1:
            flippedSelect = random.randrange(0, 2)
            if flippedSelect == 1:
                obstacles.append(pipes(600, 0, 64, 200, True))
            else:
                obstacles.append(pipes(600, 300, 64, 200, False))

    # Move the background and obstacles
    bgX -= scrollingSpeed
    bgX2 -= scrollingSpeed

    if bgX < sWidth * (-1):
        bgX = sWidth
    if bgX2 < sWidth * (-1):
        bgX2 = sWidth

    for ob in obstacles:
        ob.x -= scrollingSpeed
        if ob.x + ob.width < player.x and not ob.scored:
            score += 1
            ob.scored = True
            scoreSound.play()

        if ob.x + ob.width < 0:
            obstacles.pop(obstacles.index(ob))
        
        if ob.collide(player) and player.hitCooldown == 0:
            hurtSound.play()
            player.lifePoints -= 1
            player.hitCooldown = 1
            print('hit' + str(i))
            i += 1

    # Hit cooldown
    if player.hitCooldown > 0:
        player.hitCooldown += 1
    if player.hitCooldown == 30:
        player.hitCooldown = 0

    # Cooldown so they can't spam it
    if player.coolDown > 0:
        player.coolDown += 1
    if player.coolDown == 2:
        player.coolDown = 0
        player.jumping = False
    
    # Player interaction
    player.y += player.fallSpeed
    key = pygame.key.get_pressed()
    if key[pygame.K_SPACE] and player.coolDown == 0:
        player.y -= player.jumpSpeed
        player.coolDown = 1
        player.jumping = True

    drawWindow(score)
    CLOCK.tick(FPS)
    