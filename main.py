import pygame
import random
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('STRAY DOG')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_active = True
score = 0
level = 1

# Background
sky_surface = pygame.image.load('graphic/01.png').convert()
ground_surface = pygame.image.load('graphic/ground.png').convert()

# Score

def draw_score():
    score_surf = test_font.render(f'- STRAY DOG -  Score: {score}  Level: {level}', False, 'red')
    score_rect = score_surf.get_rect(center=(400, 50))
    pygame.draw.rect(screen, 'Gray', score_rect, 3, 10)
    screen.blit(score_surf, score_rect)

# Background Music
pygame.mixer.music.load("F:/CODING/game/Stary Dog/graphic/bg.mp3")
pygame.mixer.music.play(-1)

# Coin
coin_img = pygame.image.load("F:/CODING/game/Stary Dog/graphic/coin.png").convert_alpha()
coin_rect = coin_img.get_rect(center=(random.randint(100, 700), 250))

# Dog enemy animation
dog_imgs = [
    pygame.image.load('graphic/dog/dog1.png').convert_alpha(),
    pygame.image.load('graphic/dog/dog2.png').convert_alpha()
]
dog_frame_index = 0
dog_animation_speed = 0.1

def create_dog():
    rect = dog_imgs[0].get_rect(topleft=(random.randint(800, 1200), 260))
    return rect

dogs = [create_dog()]

# Player animations
stand_img = pygame.image.load('graphic/player/stand.png').convert_alpha()
run_imgs = [
    pygame.image.load('graphic/player/run_1.png').convert_alpha(),
    pygame.image.load('graphic/player/run_2.png').convert_alpha()
]
player_frame_index = 0
animation_speed = 0.1
facing_right = True
current_player_img = stand_img

player_rect = stand_img.get_rect(topleft=(300, 230))
player_gravity = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                    player_gravity = -22
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                player_rect.topleft = (300, 230)
                player_gravity = 0
                player_frame_index = 0
                score = 0
                level = 1
                coin_rect.center = (random.randint(100, 700), 250)
                dogs = [create_dog()]

    if game_active:
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))
        draw_score()

        # Animate dogs
        dog_frame_index += dog_animation_speed
        if dog_frame_index >= len(dog_imgs):
            dog_frame_index = 0
        current_dog_img = dog_imgs[int(dog_frame_index)]

        # Move dogs and check collision
        for dog in dogs:
            dog.right -= 2 + level  # Speed increases with level
            if dog.right <= 0:
                dog.left = random.randint(800, 1200)
            screen.blit(current_dog_img, dog)

            if dog.colliderect(player_rect):
                game_active = False

        # Player input
        keys = pygame.key.get_pressed()
        moving = keys[pygame.K_a] or keys[pygame.K_d]

        if keys[pygame.K_d]:
            player_rect.left += 2
            facing_right = True
        if keys[pygame.K_a]:
            player_rect.right -= 2
            facing_right = False
        if keys[pygame.K_s]:
            player_rect.bottom += 2

        # Player animation
        if moving:
            player_frame_index += animation_speed
            if player_frame_index >= len(run_imgs):
                player_frame_index = 0
            current_player_img = run_imgs[int(player_frame_index)]
        else:
            current_player_img = stand_img
            player_frame_index = 0

        if not facing_right:
            current_player_img = pygame.transform.flip(current_player_img, True, False)

        # Gravity
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300:
            player_rect.bottom = 300

        screen.blit(current_player_img, player_rect)

        # Coin draw
        screen.blit(coin_img, coin_rect)

        # Coin collision
        if player_rect.colliderect(coin_rect):
            score += 1
            coin_rect.center = (random.randint(100, 700), 250)

            # Level up every 5 coins
            if score % 5 == 0:
                level += 1
                dogs.append(create_dog())

    else:
        screen.fill('White')
        over_surf = test_font.render('- - GAME OVER  - - ', False, 'red')
        over_rect = over_surf.get_rect(center=(400, 150))
        screen.blit(over_surf, over_rect)

        scor_surf = test_font.render('press   spacebar   to   restart ', False, 'black')
        scor_rect = scor_surf.get_rect(center=(400, 200))
        screen.blit(scor_surf, scor_rect)

    pygame.display.update()
    clock.tick(60)
