import pygame
import time
import random

pygame.font.init()

WIDTH, HEIGHT = 1000, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Meteor Dodger")

BG = pygame.transform.scale(pygame.image.load("bg.jpeg"), (WIDTH, HEIGHT))

PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60

PLAYER_VEL = 5
METEOR_WIDTH = 10
METEOR_HEIGHT = 20
METEOR_VEL = 3
LIVES = 3

FONT = pygame.font.SysFont("comicsans", 30)
FONT_LOSE = pygame.font.SysFont("comicsans", 40)


def draw(player, elapsed_time, meteors):
    WIN.blit(BG, (0, 0))

    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    LIVES_TEXT = FONT.render(f"Lives: {LIVES}", 1, "white")
    WIN.blit(time_text, (10, 10))
    WIN.blit(LIVES_TEXT, (15, 50))

    pygame.draw.rect(WIN, "red", player)

    for meteor in meteors:
        pygame.draw.rect(WIN, "white", meteor)

    pygame.display.update()


def main():
    global LIVES
    run = True

    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)

    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0

    meteor_add_increment = 2250
    meteor_count = 0

    meteors = []
    hit = False

    while run:
        meteor_count += clock.tick(60)
        elapsed_time = time.time() - start_time

        if meteor_count > meteor_add_increment:
            for _ in range(3):
                meteor_x = random.randint(0, WIDTH - METEOR_WIDTH)
                meteor = pygame.Rect(meteor_x, -METEOR_HEIGHT, METEOR_WIDTH, METEOR_HEIGHT)
                meteors.append(meteor)

            meteor_add_increment = max(200, meteor_add_increment - 50)
            meteor_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + player.width <= WIDTH:
            player.x += PLAYER_VEL

        for meteor in meteors[:]:
            meteor.y += METEOR_VEL
            if meteor.y > HEIGHT:
                meteors.remove(meteor)
            elif meteor.y >= player.y and meteor.colliderect(player):
                meteors.remove(meteor)
                hit = True
                break

        if hit:

            lost_text = FONT_LOSE.render("You lost.", 1, "white")
            if LIVES == 1:
                WIN.blit(lost_text, (WIDTH / 2 - lost_text.get_width() / 2, HEIGHT / 2 - lost_text.get_height() / 2))
                pygame.display.update()
                pygame.time.delay(4000)
                pygame.quit()
            else:
                LIVES = LIVES - 1
                main()

        draw(player, elapsed_time, meteors)

    pygame.quit()


if __name__ == "__main__":
    main()
