import pygame
import random
import sys

# Initialisation de pygame
pygame.init()

# =========================
# Configuration du jeu
# =========================
WIDTH = 600
HEIGHT = 700
FPS = 60

PLAYER_SPEED = 6
BULLET_SPEED = 9

ENEMY_COLS = 8
ENEMY_ROWS = 3
ENEMY_WIDTH = 36
ENEMY_HEIGHT = 24

# =========================
# Couleurs
# =========================
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (40, 40, 60)

RED = (220, 50, 50)
CYAN = (0, 230, 255)
YELLOW = (255, 220, 0)
GREEN = (0, 220, 100)
ORANGE = (255, 140, 0)

# =========================
# Fenêtre du jeu
# =========================
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

clock = pygame.time.Clock()

# =========================
# Polices
# =========================
font_big = pygame.font.SysFont("consolas", 48, bold=True)
font_medium = pygame.font.SysFont("consolas", 28, bold=True)
font_small = pygame.font.SysFont("consolas", 20)

# =========================
# Fond étoilé
# =========================
stars = []

for _ in range(120):
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    radius = random.randint(1, 3)

    stars.append([x, y, radius])


def draw_background():
    screen.fill((5, 5, 20))

    for star in stars:
        star[1] += star[2]

        if star[1] > HEIGHT:
            star[1] = 0
            star[0] = random.randint(0, WIDTH)

        pygame.draw.circle(
            screen,
            (180, 180, 220),
            (star[0], star[1]),
            star[2]
        )


# =========================
# Dessin du joueur
# =========================
def draw_player(player_rect):

    center_x = player_rect.centerx

    pygame.draw.polygon(
        screen,
        CYAN,
        [
            (center_x, player_rect.top),
            (player_rect.right, player_rect.bottom),
            (player_rect.left, player_rect.bottom)
        ]
    )

    pygame.draw.polygon(
        screen,
        WHITE,
        [
            (center_x, player_rect.top + 6),
            (center_x + 8, player_rect.bottom - 4),
            (center_x - 8, player_rect.bottom - 4)
        ]
    )

    pygame.draw.rect(
        screen,
        ORANGE,
        (center_x - 5, player_rect.bottom, 10, 6),
        border_radius=3
    )


# =========================
# Dessin des ennemis
# =========================
def draw_enemy(enemy_rect, color):

    center_x = enemy_rect.centerx
    center_y = enemy_rect.centery

    pygame.draw.rect(
        screen,
        color,
        enemy_rect,
        border_radius=6
    )

    # Yeux
    pygame.draw.circle(screen, BLACK, (center_x - 8, center_y - 3), 5)
    pygame.draw.circle(screen, BLACK, (center_x + 8, center_y - 3), 5)

    pygame.draw.circle(screen, YELLOW, (center_x - 8, center_y - 3), 3)
    pygame.draw.circle(screen, YELLOW, (center_x + 8, center_y - 3), 3)


# =========================
# Création des ennemis
# =========================
def create_enemies():

    enemies = []

    padding_x = (
        WIDTH - ENEMY_COLS * (ENEMY_WIDTH + 12)
    ) // 2

    for row in range(ENEMY_ROWS):

        for col in range(ENEMY_COLS):

            x = padding_x + col * (ENEMY_WIDTH + 12)
            y = 70 + row * (ENEMY_HEIGHT + 16)

            color = [RED, ORANGE, YELLOW][row % 3]

            enemy = {
                "rect": pygame.Rect(
                    x,
                    y,
                    ENEMY_WIDTH,
                    ENEMY_HEIGHT
                ),
                "color": color
            }

            enemies.append(enemy)

    return enemies


# =========================
# Affichage HUD
# =========================
def draw_hud(score, lives, level):

    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, 48))

    score_text = font_small.render(
        f"SCORE {score:05d}",
        True,
        CYAN
    )

    level_text = font_small.render(
        f"LEVEL {level}",
        True,
        YELLOW
    )

    screen.blit(score_text, (12, 14))
    screen.blit(level_text, (220, 14))

    # Affichage des vies
    for i in range(lives):
        pygame.draw.circle(
            screen,
            RED,
            (WIDTH - 30 - i * 30, 24),
            8
        )


# =========================
# Particules d'explosion
# =========================
particles = []


def spawn_explosion(x, y, color):

    for _ in range(15):

        particle = [
            x,
            y,
            random.randint(-4, 4),
            random.randint(-4, 4),
            random.randint(10, 20),
            color
        ]

        particles.append(particle)


def update_particles():

    for particle in particles[:]:

        particle[0] += particle[2]
        particle[1] += particle[3]

        particle[4] -= 1

        pygame.draw.circle(
            screen,
            particle[5],
            (int(particle[0]), int(particle[1])),
            3
        )

        if particle[4] <= 0:
            particles.remove(particle)


# =========================
# Fonction principale
# =========================
def play():

    player = pygame.Rect(
        WIDTH // 2 - 20,
        HEIGHT - 60,
        40,
        50
    )

    bullets = []
    enemy_bullets = []

    enemies = create_enemies()

    score = 0
    lives = 3
    level = 1

    enemy_direction = 1
    enemy_speed = 1

    shoot_cooldown = 0
    enemy_cooldown = 0

    running = True

    while running:

        clock.tick(FPS)

        # =========================
        # Gestion des événements
        # =========================
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # =========================
        # Contrôles joueur
        # =========================
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and player.left > 0:
            player.x -= PLAYER_SPEED

        if keys[pygame.K_RIGHT] and player.right < WIDTH:
            player.x += PLAYER_SPEED

        # =========================
        # Tir
        # =========================
        shoot_cooldown -= 1

        if keys[pygame.K_SPACE] and shoot_cooldown <= 0:

            bullet = pygame.Rect(
                player.centerx - 3,
                player.top,
                6,
                12
            )

            bullets.append(bullet)

            shoot_cooldown = max(8, 18 - level)

        # =========================
        # Déplacement des balles
        # =========================
        for bullet in bullets:
            bullet.y -= BULLET_SPEED

        bullets = [
            bullet for bullet in bullets
            if bullet.y > -20
        ]

        # =========================
        # Déplacement ennemis
        # =========================
        move_down = False

        for enemy in enemies:

            enemy["rect"].x += int(
                enemy_speed * enemy_direction
            )

            if (
                enemy["rect"].right > WIDTH
                or enemy["rect"].left < 0
            ):
                move_down = True

        if move_down:

            enemy_direction *= -1

            for enemy in enemies:
                enemy["rect"].y += 20

        # =========================
        # Collisions
        # =========================
        for bullet in bullets[:]:

            for enemy in enemies[:]:

                if enemy["rect"].colliderect(bullet):

                    spawn_explosion(
                        enemy["rect"].centerx,
                        enemy["rect"].centery,
                        enemy["color"]
                    )

                    if bullet in bullets:
                        bullets.remove(bullet)

                    if enemy in enemies:
                        enemies.remove(enemy)

                    score += 10

                    break

        # =========================
        # Niveau suivant
        # =========================
        if not enemies:

            level += 1

            if level == 5:
                return score, True

            enemies = create_enemies()

            enemy_speed += 0.5

        # =========================
        # Dessin
        # =========================
        draw_background()

        draw_hud(score, lives, level)

        for enemy in enemies:
            draw_enemy(enemy["rect"], enemy["color"])

        draw_player(player)

        for bullet in bullets:
            pygame.draw.rect(screen, YELLOW, bullet)

        update_particles()

        pygame.display.flip()


# =========================
# Lancement du jeu
# =========================
while True:

    score, win = play()

    print("Score :", score)
    print("Victoire :", win)