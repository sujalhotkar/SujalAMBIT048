import pygame
import random

# =========================
# INITIALIZE
# =========================
pygame.init()

WIDTH = 600
HEIGHT = 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("3 Lane Racing Game")

clock = pygame.time.Clock()

# =========================
# COLORS
# =========================
WHITE = (255,255,255)
BLACK = (0,0,0)
GRAY = (60,60,60)
GREEN = (20,160,20)
RED = (255,0,0)
BLUE = (0,120,255)
YELLOW = (255,255,0)
DARK = (25,25,25)

# =========================
# FONTS
# =========================
font = pygame.font.SysFont("Arial", 38)
small_font = pygame.font.SysFont("Arial", 24)

# =========================
# ROAD SETTINGS
# =========================
ROAD_X = 100
ROAD_WIDTH = 400

line_y = 0

# 3 LANES
lanes = [155, 270, 385]

# =========================
# PLAYER
# =========================
player_width = 60
player_height = 110

player_lane = 1

player_x = lanes[player_lane]
player_y = HEIGHT - 150

# =========================
# GAME VARIABLES
# =========================
score = 0
level = 1
game_over = False

# =========================
# ENEMIES
# =========================
enemies = []

# =========================
# RESET GAME
# =========================
def reset_game():

    global enemies
    global score
    global level
    global player_lane
    global player_x
    global game_over

    enemies = []

    # EASY START
    for i in range(2):

        lane = random.randint(0,2)

        x = lanes[lane]
        y = random.randint(-900,-100)

        speed = random.randint(4,6)

        enemies.append([x,y,speed])

    score = 0
    level = 1

    player_lane = 1
    player_x = lanes[player_lane]

    game_over = False

reset_game()

# =========================
# DRAW ROAD
# =========================
def draw_road():

    global line_y

    # Grass
    screen.fill(GREEN)

    # Road
    pygame.draw.rect(screen,
                     GRAY,
                     (ROAD_X,0,ROAD_WIDTH,HEIGHT))

    # Side Borders
    pygame.draw.rect(screen,
                     WHITE,
                     (ROAD_X,0,8,HEIGHT))

    pygame.draw.rect(screen,
                     WHITE,
                     (ROAD_X+ROAD_WIDTH-8,0,8,HEIGHT))

    # Lane Lines
    for y in range(-50, HEIGHT, 50):

        pygame.draw.rect(screen,
                         WHITE,
                         (230,
                          y + line_y,
                          8,
                          30))

        pygame.draw.rect(screen,
                         WHITE,
                         (360,
                          y + line_y,
                          8,
                          30))

    # Road Animation
    line_y += 10

    if line_y >= 50:
        line_y = 0

# =========================
# DRAW PLAYER CAR
# =========================
def draw_player(x, y):

    # Shadow
    pygame.draw.rect(screen,
                     BLACK,
                     (x+5,y+5,60,110),
                     border_radius=12)

    # Body
    pygame.draw.rect(screen,
                     BLUE,
                     (x,y,60,110),
                     border_radius=12)

    # Window
    pygame.draw.rect(screen,
                     WHITE,
                     (x+10,y+10,40,25),
                     border_radius=5)

    # Wheels
    pygame.draw.circle(screen,
                       BLACK,
                       (x+8,y+20),
                       8)

    pygame.draw.circle(screen,
                       BLACK,
                       (x+52,y+20),
                       8)

    pygame.draw.circle(screen,
                       BLACK,
                       (x+8,y+90),
                       8)

    pygame.draw.circle(screen,
                       BLACK,
                       (x+52,y+90),
                       8)

# =========================
# DRAW ENEMY CAR
# =========================
def draw_enemy(x, y):

    # Shadow
    pygame.draw.rect(screen,
                     BLACK,
                     (x+5,y+5,60,110),
                     border_radius=12)

    # Body
    pygame.draw.rect(screen,
                     RED,
                     (x,y,60,110),
                     border_radius=12)

    # Window
    pygame.draw.rect(screen,
                     WHITE,
                     (x+10,y+10,40,25),
                     border_radius=5)

    # Wheels
    pygame.draw.circle(screen,
                       BLACK,
                       (x+8,y+20),
                       8)

    pygame.draw.circle(screen,
                       BLACK,
                       (x+52,y+20),
                       8)

    pygame.draw.circle(screen,
                       BLACK,
                       (x+8,y+90),
                       8)

    pygame.draw.circle(screen,
                       BLACK,
                       (x+52,y+90),
                       8)

# =========================
# COLLISION
# =========================
def collision(px, py, ex, ey):

    player_rect = pygame.Rect(px, py, 60, 110)

    enemy_rect = pygame.Rect(ex, ey, 60, 110)

    return player_rect.colliderect(enemy_rect)

# =========================
# MAIN GAME LOOP
# =========================
running = True

while running:

    clock.tick(60)

    # =====================
    # EVENTS
    # =====================
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            # LEFT
            if event.key == pygame.K_LEFT:

                if player_lane > 0:

                    player_lane -= 1
                    player_x = lanes[player_lane]

            # RIGHT
            if event.key == pygame.K_RIGHT:

                if player_lane < 2:

                    player_lane += 1
                    player_x = lanes[player_lane]

            # RESTART
            if game_over:

                if event.key == pygame.K_r:
                    reset_game()

    # =====================
    # DRAW ROAD
    # =====================
    draw_road()

    # =====================
    # GAMEPLAY
    # =====================
    if not game_over:

        # Enemy Movement
        for enemy in enemies:

            enemy[1] += enemy[2]

            # Respawn Enemy
            if enemy[1] > HEIGHT:

                lane = random.randint(0,2)

                enemy[0] = lanes[lane]
                enemy[1] = random.randint(-500,-100)

                score += 1

                # LEVEL UP
                if score % 20 == 0:

                    level += 1

                    for e in enemies:
                        e[2] += 0.5

            # Draw Enemy
            draw_enemy(enemy[0], enemy[1])

            # Collision
            if collision(player_x,
                         player_y,
                         enemy[0],
                         enemy[1]):

                game_over = True

        # Draw Player
        draw_player(player_x, player_y)

    else:

        # =====================
        # GAME OVER SCREEN
        # =====================
        over = font.render(
            "GAME OVER",
            True,
            RED
        )

        restart = small_font.render(
            "Press R To Restart",
            True,
            WHITE
        )

        final_score = small_font.render(
            f"Final Score: {score}",
            True,
            YELLOW
        )

        screen.blit(over, (170,250))
        screen.blit(final_score, (210,320))
        screen.blit(restart, (180,390))

    # =========================
    # MODERN HUD
    # =========================

    # HUD Background
    pygame.draw.rect(screen,
                     DARK,
                     (0,0,WIDTH,90))

    # Score Box
    pygame.draw.rect(screen,
                     (40,40,40),
                     (20,15,180,55),
                     border_radius=10)

    # Level Box
    pygame.draw.rect(screen,
                     (40,40,40),
                     (400,15,160,55),
                     border_radius=10)

    # Score Text
    score_title = small_font.render(
        "SCORE",
        True,
        YELLOW
    )

    score_value = font.render(
        str(score),
        True,
        WHITE
    )

    # Level Text
    level_title = small_font.render(
        "LEVEL",
        True,
        BLUE
    )

    level_value = font.render(
        str(level),
        True,
        WHITE
    )

    # Draw Score
    screen.blit(score_title, (35,18))
    screen.blit(score_value, (110,15))

    # Draw Level
    screen.blit(level_title, (420,18))
    screen.blit(level_value, (500,15))

    # =========================
    # PROGRESS BAR
    # =========================

    pygame.draw.rect(screen,
                     (70,70,70),
                     (210,30,180,20),
                     border_radius=10)

    progress = (score % 20) / 20

    pygame.draw.rect(screen,
                     (0,255,120),
                     (210,
                      30,
                      int(180 * progress),
                      20),
                     border_radius=10)

    progress_text = small_font.render(
        f"{int(progress*100)}%",
        True,
        BLACK
    )

    screen.blit(progress_text, (275,25))

    pygame.display.update()

pygame.quit()