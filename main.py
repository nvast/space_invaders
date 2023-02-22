import pygame
import os
import json

pygame.font.init()

window = pygame.display.set_mode((540, 600))
pygame.display.set_caption("Space Invaders")

FPS = 60
SCORE_FONT = pygame.font.SysFont("comicsans", 30)
GAME_OVER_FONT = pygame.font.SysFont("comicsans", 70)

ship = pygame.image.load(os.path.join("Assets", "player.png"))
invader_1_stand = pygame.image.load(os.path.join("Assets", "invader-1-stand.png"))
invader_1_stand = pygame.transform.scale(invader_1_stand, (30, 20))
invader_1_walk = pygame.image.load(os.path.join("Assets", "invader-1-walk.png"))
invader_1_walk = pygame.transform.scale(invader_1_walk, (30, 20))
invader_2_stand = pygame.image.load(os.path.join("Assets", "invader-2-stand.png"))
invader_2_stand = pygame.transform.scale(invader_2_stand, (30, 30))
invader_2_walk = pygame.image.load(os.path.join("Assets", "invader-2-walk.png"))
invader_2_walk = pygame.transform.scale(invader_2_walk, (30, 30))
invader_3_stand = pygame.image.load(os.path.join("Assets", "invader-3-stand.png"))
invader_3_stand = pygame.transform.scale(invader_3_stand, (30, 30))
invader_3_walk = pygame.image.load(os.path.join("Assets", "invader-3-walk.png"))
invader_3_walk = pygame.transform.scale(invader_3_walk, (30, 30))
wall = pygame.image.load(os.path.join("Assets", "wall.png"))
dead = pygame.image.load(os.path.join("Assets", "dead.png"))
dead = pygame.transform.scale(dead, (30, 30))

invader1_hit = pygame.USEREVENT + 1
invader2_hit = pygame.USEREVENT + 2
invader3_hit = pygame.USEREVENT + 3


def draw_window(player, invaders1, invaders2, invaders3, bullets, ticks_passed, score, highest_score):
    window.fill((0, 0, 0))
    pygame.draw.rect(window, (173, 255, 47), pygame.Rect(0, 0, 4, 600))
    pygame.draw.rect(window, (173, 255, 47), pygame.Rect(0, 0, 550, 4))
    pygame.draw.rect(window, (173, 255, 47), pygame.Rect(536, 0, 4, 600))
    pygame.draw.rect(window, (173, 255, 47), pygame.Rect(0, 596, 550, 4))
    window.blit(ship, (player.x, player.y))
    window.blit(wall, (50, 420))
    window.blit(wall, (175, 420))
    window.blit(wall, (300, 420))
    window.blit(wall, (425, 420))

    score_text = SCORE_FONT.render("Score: " + str(score), 1, (255, 255, 255))
    window.blit(score_text, (20, 20))

    highest_score_text = SCORE_FONT.render("Highest score: " + str(highest_score), 1, (255, 255, 255))
    window.blit(highest_score_text, (520 - highest_score_text.get_width(), 20))

    for bullet in bullets:
        pygame.draw.rect(window, (255, 255, 0), bullet)

    invaders = [(invaders3, invader_3_stand, invader_3_walk),
                (invaders2, invader_2_stand, invader_2_walk),
                (invaders1, invader_1_stand, invader_1_walk)]

    for invader_group, stand_image, walk_image in invaders:
        for invader in invader_group:
            if score < 20:
                if ticks_passed < 30:
                    window.blit(stand_image, (invader.x, invader.y))
                else:
                    window.blit(walk_image, (invader.x, invader.y))
            elif any(start <= ticks_passed <= end for start, end in [(10, 20), (30, 40), (50, 60)]):
                window.blit(stand_image, (invader.x, invader.y))
            else:
                window.blit(walk_image, (invader.x, invader.y))

    pygame.display.update()


def player_movement(player):
    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[pygame.K_LEFT] and player.x - 10 > -1:
        player.x -= 4
    if keys_pressed[pygame.K_RIGHT] and player.x + 10 < 480:
        player.x += 4


def invader_movement(invaders1, invaders2, invaders3, movement):
    list_of_invaders = invaders1 + invaders2 + invaders3

    for invader in list_of_invaders:
        if invader.x > 2 or invader.x < 498:
            invader.x += movement[0]
        if invader.x <= 2 or invader.x >= 508:
            movement[0] = -movement[0]
            for _ in list_of_invaders:
                _.y += 5

            # code in comment simplified by chatGPT
            if abs(movement[0]) > 5:
                movement[0] = 5 if movement[0] > 0 else -5
            direction = 1 if movement[0] > 0 else -1
            if (direction == 1 and invader.x <= 2) or (direction == -1 and invader.x >= 508):
                invader.x += direction * min(abs(movement[0]), 6)

            # if movement[0] == 1:
            #     if invader.x <= 2:
            #         invader.x += 1
            # elif movement[0] == -1:
            #     if invader.x >= 508:
            #         invader.x -= 1
            # elif movement[0] == 2:
            #     if invader.x <= 2:
            #         invader.x += 2
            # elif movement[0] == -2:
            #     if invader.x >= 508:
            #         invader.x -= 2
            # elif movement[0] == 3:
            #     if invader.x <= 2:
            #         invader.x += 3
            # elif movement[0] == -3:
            #     if invader.x >= 508:
            #         invader.x -= 3
            # elif movement[0] == 4:
            #     if invader.x <= 2:
            #         invader.x += 5
            # elif movement[0] == -4:
            #     if invader.x >= 508:
            #         invader.x -= 5
            # elif movement[0] == 5:
            #     if invader.x <= 2:
            #         invader.x += 6
            # elif movement[0] == -5:
            #     if invader.x >= 508:
            #         invader.x -= 6

        if invader.y > 390:
            game_over()


def handle_bullets(bullets, invaders1, invaders2, invaders3):
    list_of_invaders = invaders1 + invaders2 + invaders3

    for bullet in bullets:
        bullet.y -= 5
        for invader in list_of_invaders:
            if (bullet.y <= (invader.y + invader.height // 4) and bullet.y >= invader.y) and (
                    invader.x < bullet.x < invader.x + 30):
                if bullet in bullets:
                    bullets.remove(bullet)
                    if invader in invaders1:
                        window.blit(dead, (invader.x, invader.y))
                        pygame.display.update()
                        invaders1.remove(invader)
                        pygame.event.post(pygame.event.Event(invader1_hit))
                    elif invader in invaders2:
                        window.blit(dead, (invader.x, invader.y))
                        pygame.display.update()
                        invaders2.remove(invader)
                        pygame.event.post(pygame.event.Event(invader2_hit))
                    elif invader in invaders3:
                        window.blit(dead, (invader.x, invader.y))
                        pygame.display.update()
                        invaders3.remove(invader)
                        pygame.event.post(pygame.event.Event(invader3_hit))

            if (invader.y >= bullet.y >= invader.y + 50) and (
                    bullet.x >= invader.x >= bullet.x):
                if bullet in bullets:
                    bullets.remove(bullet)

        if bullet in bullets and bullet.y < 0:
            bullets.remove(bullet)
        elif bullet.y == 470 and (50 <= bullet.x <= 100):
            bullets.remove(bullet)
        elif bullet.y == 470 and (175 <= bullet.x <= 225):
            bullets.remove(bullet)
        elif bullet.y == 470 and (300 <= bullet.x <= 350):
            bullets.remove(bullet)
        elif bullet.y == 470 and (425 <= bullet.x <= 475):
            bullets.remove(bullet)


def draw_invaders(invaders1, invaders2, invaders3):
    vertical = 0
    horizontal = 0
    for first in range(11):
        horizontal += 40
        new_invader = pygame.Rect(0 + horizontal, 100, 50, 50)
        invaders3.append(new_invader)

    for two in range(2):
        vertical += 40
        horizontal = 0
        for first in range(11):
            horizontal += 40
            new_invader = pygame.Rect(0 + horizontal, 100 + vertical, 50, 50)
            invaders2.append(new_invader)

    for two in range(2):
        vertical += 40
        horizontal = 0
        for first in range(11):
            horizontal += 40
            new_invader = pygame.Rect(0 + horizontal, 100 + vertical, 50, 50)
            invaders1.append(new_invader)


def game_over():
    game_over_text = GAME_OVER_FONT.render("GAME OVER", 1, (173, 255, 47))
    window.blit(game_over_text, (270 - game_over_text.get_width() / 2, 100))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return main()
            if event.type == pygame.QUIT:
                pygame.quit()


def load_high_score():
    try:
        with open('high_score.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return 0


def save_high_score(score):
    with open('high_score.json', 'w') as file:
        json.dump(score, file)


def intensity(next_level, score, movement):
    if (20 <= score < 100) and not next_level[0]:
        next_level[0] = True
        if movement[0] == 1:
            movement[0] = 2
        elif movement[0] == -1:
            movement[0] = -2
    elif score >= 100 and next_level[0]:
        next_level[0] = False
        if movement[0] == 2:
            movement[0] = 3
        elif movement[0] == -2:
            movement[0] = -3
    elif score >= 200 and not next_level[0]:
        next_level[0] = True
        if movement[0] == 3:
            movement[0] = 4
        elif movement[0] == -3:
            movement[0] = -4
    elif score >= 500 and next_level[0]:
        next_level[0] = False
        if movement[0] == 4:
            movement[0] = 5
        elif movement[0] == -4:
            movement[0] = -5


def main():
    player = pygame.Rect(240, 500, 50, 50)
    invaders3 = []
    invaders2 = []
    invaders1 = []
    bullets = []

    draw_invaders(invaders1, invaders2, invaders3)

    clock = pygame.time.Clock()
    score = 0
    movement = [1]
    run = True
    next_level = [False]
    ticks_passed = 0
    while run:
        clock.tick(FPS)
        ticks_passed += 1
        if ticks_passed == FPS:
            ticks_passed = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(bullets) < 4:
                    bullet = pygame.Rect(player.x + player.width // 2, player.y, 5, 10)
                    bullets.append(bullet)

            if event.type == invader1_hit:
                score += 1
            elif event.type == invader2_hit:
                score += 2
            elif event.type == invader3_hit:
                score += 3

        intensity(next_level, score, movement)

        if invaders1 == [] and invaders2 == [] and invaders3 == []:
            draw_invaders(invaders1, invaders2, invaders3)

        if score > load_high_score():
            high_score = score
            save_high_score(high_score)

        draw_window(player, invaders1, invaders2, invaders3, bullets, ticks_passed, score, load_high_score())
        player_movement(player)

        invader_movement(invaders1, invaders2, invaders3, movement)
        handle_bullets(bullets, invaders1, invaders2, invaders3)

    main()


if __name__ == "__main__":
    main()
