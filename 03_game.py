import pygame
import time
import random

pygame.font.init()

Width, Height = (1000, 800)
Win = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("Space Dodge")

BG = pygame.transform.scale(pygame.image.load("bg.jpeg"), (Width, Height))

player_width = 40
player_height = 60
player_VEL = 5
bullet_width = 5
bullet_height = 15
bullet_VEL = 7
STAR_WIDTH = 10
STAR_HEIGHT = 20
star_vel = 2

class Bullet:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, bullet_width, bullet_height)
    def move(self):
        self.rect.y -= bullet_VEL

class Star:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, STAR_WIDTH, STAR_HEIGHT)

FONT = pygame.font.SysFont("comicsans", 30)
SCORE_FONT = pygame.font.SysFont("comicsans", 50)

def draw(player, elapsed_time, stars, bullets, score, level):
    Win.blit(BG, (0,0))
    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    Win.blit(time_text, (10, 10))

    pygame.draw.rect(Win,"red",player)

    for bullet in bullets:
        pygame.draw.rect(Win, "blue", bullet.rect)

    for star in stars:
        pygame.draw.rect(Win, "white", star.rect)

    score_text = SCORE_FONT.render(f"Score: {score}", 1, "white")
    Win.blit(score_text, (Width - score_text.get_width() - 10, 10))

    level_text = SCORE_FONT.render(f"Level: {level}", 1, "white")
    Win.blit(level_text, (Width - level_text.get_width() - 10, 70))

    pygame.display.update()

def main():
    run = True

    player = pygame.Rect(200, Height - player_height,
                         player_width, player_height)
    clock = pygame.time.Clock()
    start_time = time.time()

    star_add_increment = 1500
    star_count = 0

    bullets = []
    stars = []
    score = 0
    level = 1
    hit = False

    while run:
        star_count += clock.tick(60)
        elapsed_time = time.time() - start_time

        if star_count > star_add_increment:
            for _ in range(3):
                star_x = random.randint(0, Width - STAR_WIDTH)
                new_star = Star(star_x, -STAR_HEIGHT)
                stars.append(new_star)

            star_add_increment = max(1000, star_add_increment - 50)
            star_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                new_bullet = Bullet(player.x + player_width/2 - bullet_width/2, player.y)
                bullets.append(new_bullet)

        key = pygame.key.get_pressed()
        if key[pygame.K_a] and player.x - player_VEL >= 0:
            player.x -= player_VEL
        if key[pygame.K_d] and player.x + player_VEL + player_width <= Width:
            player.x += player_VEL

        stars_to_remove = []

        for star in stars:
            star.rect.y += star_vel
            if star.rect.y > Height:
                stars_to_remove.append(star)
                if not hit:
                    score += 10
            elif star.rect.colliderect(player):
                stars_to_remove.append(star)
                hit = True

        for star in stars_to_remove:
            stars.remove(star)

        for bullet in bullets[:]:
            bullet.move()
            for star in stars[:]:
                if bullet.rect.colliderect(star.rect):
                    bullets.remove(bullet)
                    stars.remove(star)
                    score += 20

        if score >= 500 * level:
            level += 1

        if hit:
            lost_text = FONT.render("You Lost!", 1, "white")
            Win.blit(lost_text, (Width/2 - lost_text.get_width()/2, Height/2 - lost_text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(4000)
            break

        draw(player, elapsed_time, stars, bullets, score, level)

    pygame.quit()

if __name__ == "__main__":
    main()

