
import pygame
import random
import sys
import math

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("KALI KHUSHI RUNNER")

clock = pygame.time.Clock()

# Colors
BLACK = (15, 15, 15)
YELLOW = (255, 220, 0)
WHITE = (255, 255, 255)
GREEN = (30, 170, 65)
RED = (240, 50, 50)
SKY = (130, 200, 255)

font = pygame.font.SysFont("arial", 27, bold=True)
big_font = pygame.font.SysFont("arial", 55, bold=True)

# Dialogues
dialogues = [
    "Kali Khushi!",
    "Pagal Khushi!",
    "Dom Khushiii!",
    "Guuu khane wali Khushi!",
    "Tatti khane wali meri behan!"
]

game_over_dialogue = "Arey Kali Bhaus, tere wajah se haar gaya!"

# Optional voice using Windows SAPI
def speak(text):
    try:
        import subprocess
        safe_text = text.replace("'", "")
        subprocess.Popen(
            ["powershell", "-NoProfile", "-Command",
             "Add-Type -AssemblyName System.Speech; "
             "$s=New-Object System.Speech.Synthesis.SpeechSynthesizer; "
             "$s.Speak('" + safe_text + "')"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except Exception:
        pass

# Bull
bull_x = 100
ground_y = 400
bull_y = ground_y
velocity = 0
jumping = False

# Obstacles
obstacles = []

# Game variables
score = 0
speed = 6
game_over = False
dialogue_index = 0
last_dialogue_score = -1

def draw_bull(x, y):

    # Body
    pygame.draw.ellipse(screen, BLACK, (x, y+18, 85, 43))

    # Head
    pygame.draw.circle(screen, BLACK, (x+78, y+25), 25)

    # Ears
    pygame.draw.ellipse(screen, BLACK, (x+55, y-3, 25, 17))
    pygame.draw.ellipse(screen, BLACK, (x+88, y-3, 25, 17))

    # Horns
    pygame.draw.line(screen, WHITE, (x+65, y+8),
                     (x+53, y-12), 5)
    pygame.draw.line(screen, WHITE, (x+92, y+8),
                     (x+105, y-12), 5)

    # Eyes
    pygame.draw.circle(screen, WHITE, (x+85, y+18), 5)
    pygame.draw.circle(screen, BLACK, (x+87, y+18), 2)

    # Nose
    pygame.draw.ellipse(screen, (90, 90, 90),
                        (x+94, y+32, 19, 13))

    # Legs
    pygame.draw.line(screen, BLACK, (x+20, y+52),
                     (x+15, y+75), 7)
    pygame.draw.line(screen, BLACK, (x+45, y+52),
                     (x+45, y+75), 7)
    pygame.draw.line(screen, BLACK, (x+70, y+52),
                     (x+75, y+75), 7)

    # Tail
    pygame.draw.arc(screen, BLACK,
                    (x-13, y+25, 30, 35), 1, 4, 4)

def draw_obstacle(obstacle):

    x, y = obstacle

    # Yellow funny obstacle
    pygame.draw.ellipse(screen, YELLOW, (x, y, 48, 45))
    pygame.draw.ellipse(screen, (220, 170, 0),
                        (x+10, y+10, 28, 20))

    pygame.draw.circle(screen, WHITE, (x+16, y+15), 5)
    pygame.draw.circle(screen, WHITE, (x+32, y+15), 5)
    pygame.draw.circle(screen, BLACK, (x+17, y+15), 2)
    pygame.draw.circle(screen, BLACK, (x+33, y+15), 2)

def reset_game():

    global bull_y, velocity, jumping
    global obstacles, score, speed, game_over
    global last_dialogue_score, dialogue_index

    bull_y = ground_y
    velocity = 0
    jumping = False
    obstacles = []
    score = 0
    speed = 6
    game_over = False
    last_dialogue_score = -1
    dialogue_index = 0

def draw_text(text, font_type, color, x, y):
    image = font_type.render(text, True, color)
    screen.blit(image, (x, y))

def main():

    global bull_y, velocity, jumping
    global obstacles, score, speed, game_over
    global last_dialogue_score, dialogue_index

    running = True
    next_obstacle = 0
    current_dialogue = "Kali Khushi!"

    while running:

        clock.tick(60)
        screen.fill(SKY)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE and not game_over:
                    if not jumping:
                        velocity = -17
                        jumping = True

                if event.key == pygame.K_r and game_over:
                    reset_game()

            if event.type == pygame.MOUSEBUTTONDOWN:

                if game_over:
                    mouse = pygame.mouse.get_pos()
                    if restart_button.collidepoint(mouse):
                        reset_game()

        # Ground
        pygame.draw.rect(screen, GREEN,
                         (0, ground_y+75, WIDTH, 100))
        pygame.draw.line(screen, BLACK,
                         (0, ground_y+75),
                         (WIDTH, ground_y+75), 4)

        # Clouds
        pygame.draw.circle(screen, WHITE, (180, 90), 25)
        pygame.draw.circle(screen, WHITE, (210, 90), 30)
        pygame.draw.circle(screen, WHITE, (240, 90), 23)

        pygame.draw.circle(screen, WHITE, (600, 130), 25)
        pygame.draw.circle(screen, WHITE, (630, 130), 30)

        if not game_over:

            # Jump physics
            bull_y += velocity
            velocity += 0.8

            if bull_y >= ground_y:
                bull_y = ground_y
                velocity = 0
                jumping = False

            # Obstacles generation
            next_obstacle += 1

            if next_obstacle > random.randint(65, 105):
                obstacles.append([WIDTH, ground_y+35])
                next_obstacle = 0

            # Move obstacles
            for obstacle in obstacles:
                obstacle[0] -= speed

            obstacles = [
                o for o in obstacles if o[0] > -60
            ]

            # Collision
            bull_rect = pygame.Rect(
                bull_x+10, bull_y+5, 100, 65
            )

            for obstacle in obstacles:

                obstacle_rect = pygame.Rect(
                    obstacle[0]+5,
                    obstacle[1]+5,
                    38, 35
                )

                if bull_rect.colliderect(obstacle_rect):
                    game_over = True
                    speak(game_over_dialogue)

            # Score
            score += 1
            speed = min(13, 6 + score // 500)

            # Dialogues
            if score % 180 == 0 and score != last_dialogue_score:

                current_dialogue = dialogues[dialogue_index]

                speak(current_dialogue)

                dialogue_index = (
                    dialogue_index + 1
                ) % len(dialogues)

                last_dialogue_score = score

        # Draw game objects
        draw_bull(bull_x, bull_y)

        for obstacle in obstacles:
            draw_obstacle(obstacle)

        # Score
        draw_text(
            f"SCORE: {score//10}",
            font, BLACK, 20, 20
        )

        draw_text(
            "SPACE = JUMP",
            font, BLACK, 650, 20
        )

        # Dialogue bubble
        if not game_over:
            bubble = font.render(
                current_dialogue, True, BLACK
            )
            screen.blit(bubble, (bull_x-5, bull_y-45))

        # Game over screen
        if game_over:

            overlay = pygame.Surface(
                (WIDTH, HEIGHT), pygame.SRCALPHA
            )
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))

            title = big_font.render(
                "GAME OVER!", True, RED
            )
            screen.blit(title, (285, 130))

            draw_text(
                game_over_dialogue,
                font, WHITE, 130, 220
            )

            draw_text(
                f"FINAL SCORE: {score//10}",
                font, YELLOW, 340, 270
            )

            restart_button = pygame.Rect(
                340, 340, 220, 60
            )

            pygame.draw.rect(
                screen, GREEN,
                restart_button, border_radius=12
            )

            restart_text = font.render(
                "RESTART GAME", True, BLACK
            )

            screen.blit(
                restart_text,
                (restart_button.x+15,
                 restart_button.y+15)
            )

            draw_text(
                "Press R to restart",
                font, WHITE, 345, 420
            )

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
