import pygame
import time
import random

pygame.font.init()
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Space Dogde")


BG = pygame.transform.scale(pygame.image.load("background.jpg"),(WIDTH,HEIGHT))
try:
    HEART_IMG = pygame.image.load("hearttt.png").convert_alpha()
    HEART_IMG.set_colorkey((255,255,255))
    HEART_IMG = pygame.transform.scale(HEART_IMG,(32,32))
except Exception:
    HEART_IMG = None

print('HEART LOAD OK:',HEART_IMG is not True)
player_width = 40
player_height = 60
player_vel = 5

star_width = 10
star_height = 20
star_vel = 3

LIVES_START = 3
INVINCIBLE_MS = 800

FONT = pygame.font.SysFont("arialunicode", 30)

def draw(player, elapsed_time,stars , lives):
    WIN.blit(BG, (0,0))
    
    time_text = FONT.render(f'Time: {round(elapsed_time)}s',1,'white')
    WIN.blit(time_text,(10,10))
    
    if HEART_IMG:
        lives_text = FONT.render('Lives : ',True,'white')
        WIN.blit(lives_text,(10,40))

        text_width = lives_text.get_width()
        start_x = 10 + text_width + 10

        for i in range(lives):
            WIN.blit(HEART_IMG,(start_x + i * (HEART_IMG.get_width() + 5),38))
    else:
        lives_text = FONT.render(f'Lives : {lives}',True,'white')
        WIN.blit(lives_text,(10,40))

    pygame.draw.rect(WIN, "red", player)

    for star in stars:
        pygame.draw.rect(WIN, "white", star)
    pygame.display.update()

def main():
    run = True
    
    player = pygame.Rect(200,HEIGHT - player_height, player_width, player_height)

    clock = pygame.time.Clock()

    start_time = time.time()
    elapsed_time = 0

    star_add_increment = 2000
    star_count = 0

    stars = []
    hit = False

    lives = LIVES_START
    last_hit_ms = -10_000
    while run:
        star_count += clock.tick(60)
        elapsed_time = time.time() - start_time

        if star_count > star_add_increment:
            for _ in range(3):
                star_x = random.randint(0, WIDTH - star_width)
                star = pygame.Rect(star_x, -star_height, star_width, star_height)
                stars.append(star)

            star_add_increment = max(200, star_add_increment - 50 )
            star_count = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - player_vel >= 0:
            player.x -= player_vel
        if keys[pygame.K_RIGHT] and  player.x + player_vel + player_width <= WIDTH:
            player.x += player_vel

        for star in stars[:]:
            star.y += star_vel
            if star.y > HEIGHT:
                stars.remove(star)
            elif star.y + star.height >= player.y and star.colliderect(player):
                now_ms = pygame.time.get_ticks()
                if now_ms - last_hit_ms >= INVINCIBLE_MS:
                    last_hit_ms = now_ms
                    stars.remove(star)
                    lives -= 1

                    warn_text = FONT.render(f'{lives} left', True, 'yellow')
                    WIN.blit(warn_text, (WIDTH/2 - warn_text.get_width()/2, HEIGHT//2))
                    pygame.display.update()
                    pygame.time.delay(500)

                    if lives <= 0:
                        hit = True
                else:
                    pass
                break
        if hit:
            lost_text = FONT.render('You Lost!',1,'white')
            WIN.blit(lost_text,(WIDTH/2 -lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(4000)
            break
        draw(player, elapsed_time,stars,lives)

    pygame.quit()


if __name__ == "__main__":
    main()