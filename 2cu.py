import pygame
import time

WIDTH = 840
HEIGHT = 650
FPS = 60

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hom Tanks")
clock = pygame.time.Clock()
font_name = pygame.font.match_font('fonts/space_invaders.ttf')

def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, False, RED)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/tank.gif')
        self.image = pygame.transform.scale(self.image, (112, 104))
        self.rect = self.image.get_rect()
        self.rect.right = (WIDTH / 4) * 3
        self.rect.centery = HEIGHT / 2
        self.speed = 6
        self.bullet_speed = 4
        self.shoot_delay = 800
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_DOWN] and self.rect.y < 496:
            self.rect.y += self.speed

        if key[pygame.K_UP] and self.rect.y > 0:
            self.rect.y -= self.speed

        if key[pygame.K_RIGHT] and self.rect.x < 588:
            self.rect.x += self.speed

        if key[pygame.K_LEFT] and self.rect.x > 420:
            self.rect.x -= self.speed

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.centery, self.rect.left)
            all_sprites.add(bullet)
            bullets.add(bullet)


class Player1(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/tank2.gif")
        self.image = pygame.transform.scale(self.image, (112, 104))
        self.rect = self.image.get_rect()
        self.rect.left = WIDTH / 4
        self.rect.centery = HEIGHT / 2
        self.speed = 6
        self.bullet_speed = 4
        self.shoot_delay = 800
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_w] and self.rect.y > 0:
            self.rect.y -= self.speed

        if key[pygame.K_s] and self.rect.y < 496:
            self.rect.y += self.speed

        if key[pygame.K_d] and self.rect.x < 308:
            self.rect.x += self.speed

        if key[pygame.K_a] and self.rect.x > 140:
            self.rect.x -= self.speed

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet1 = Bullet1(self.rect.centery, self.rect.right)
            all_sprites.add(bullet1)
            bullets1.add(bullet1)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/canonball1.png')
        self.rect = self.image.get_rect()
        self.rect.right = y
        self.rect.centery = x
        self.speedx = 6

    def update(self):
        self.rect.x -= self.speedx
        if self.rect.right < 0:
            self.kill()


class Bullet1(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/canonball2.png')
        self.rect = self.image.get_rect()
        self.rect.left = y
        self.rect.centery = x
        self.speedx = 6

    def update(self):
        self.rect.x += self.speedx
        if self.rect.left > 840:
            self.kill()


class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


all_sprites = pygame.sprite.Group()
player_sprite = pygame.sprite.Group()
player_sprite1 = pygame.sprite.Group()
bullets1 = pygame.sprite.Group()
bullets = pygame.sprite.Group()
background_sprite = pygame.sprite.Group()
player = Player()
player1 = Player1()
all_sprites.add(player, player1)
y = 0
score = 0
score1 = 0

# Game loop
running = True
while running:
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player1.shoot()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_l:
                player.shoot()

    # Update
    all_sprites.update()

    # check for player bullet1 collision
    hits = pygame.sprite.spritecollide(player, bullets1, True)
    if hits:
        score1 += 1
        if score1 == 3:
            time.sleep(0.5)
            running = False

    # check for player1 bullet collision
    hits = pygame.sprite.spritecollide(player1, bullets, True)
    if hits:
        score += 1
        if score == 3:
            time.sleep(0.5)
            running = False

    # Draw / render
    screen.fill(BLACK)
    if y >= HEIGHT:
        y = 0
    else:
        y += 5
    background = Background('images/background.png', [0, y])
    background1 = Background('images/background.png', [0, y - 650])
    screen.blit(background.image, background.rect)
    screen.blit(background1.image, background1.rect)
    draw_text(screen, " Lives ", 50, (WIDTH / 2), 18)
    draw_text(screen, str(score1), 50, (WIDTH / 4), 18)
    draw_text(screen, str(score), 50, (WIDTH / 4) * 3, 18)

    all_sprites.draw(screen)
    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()