import pygame

pygame.init()

time_clock = pygame.time.Clock()

window = pygame.display.set_mode((1155, 650))
pygame.display.set_caption('Dino-Chrome на Python')

icon_game = pygame.image.load('game_Dino-Chrome/dino_icon.png').convert_alpha()
pygame.display.set_icon(icon_game)

# Музыка фоновая
music_fon_game = pygame.mixer.Sound('sound_game/game_fon_sound.mp3')
music_fon_game.play(0)

# Музыка проигрыша
music_game_over = pygame.mixer.Sound('sound_game/game_over.mp3')

fon_game = pygame.image.load('fon_game/game_pole.png').convert_alpha()

# Позиция дино
dino_x, dino_y = 50, 323
# Движение дино
dino_run = [
    pygame.image.load('dino_player_right/dino_run1.png').convert_alpha(),
    pygame.image.load('dino_player_right/dino_run2.png').convert_alpha()
]

dino_run_left = [
    pygame.image.load('dino_player_left/dino_run1 (1).png').convert_alpha(),
    pygame.image.load('dino_player_left/dino_run2 (1).png').convert_alpha()
]

dino_run_down = [
    pygame.image.load('dino_down/dino_down1.png').convert_alpha(),
    pygame.image.load('dino_down/dino_down2.png').convert_alpha()
]
dino_active = 0

fly_boo_x = 1157
fly_dino_boo = [
    pygame.image.load('dino_fly/fly1.png').convert_alpha(),
    pygame.image.load('dino_fly/fly2.png').convert_alpha()
]

fly_active = 0

fon_x = 0

# Кнопка рестарта
restart_img = pygame.image.load('fon_game/restart.png').convert_alpha()

# Дино прыжок
prig_dino = False
jump_count = 10

# Дино движение
dino_speed = 25

# Летающие динозаврики
fly_boo_spisok = []
# Таймер появления
fly_timer = pygame.USEREVENT + 1
pygame.time.set_timer(fly_timer, 2200)

# Проверка на проигрыш
game_play = True
font_sms = pygame.font.SysFont("monospace", 65)
font_sms_restart = pygame.font.SysFont("monospace", 45)
lose_sms_str = font_sms.render("Вы проиграли!", True, (193, 196, 199))
restart_game = font_sms_restart.render("Играть заново", True, (98, 193, 68))
restart_game_rect = restart_game.get_rect(topleft=(400, 400))

running_game = True
while running_game:

    keys_pressed = pygame.key.get_pressed()

    # Фон игровое поле
    window.blit(fon_game, (fon_x, 0))
    window.blit(fon_game, (fon_x + 1155, 0))

    if game_play:
        fon_x -= 10
        if fon_x == -1160:
            fon_x = 0

        # Персонаж дино
        if keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a]:
            window.blit(dino_run_left[dino_active], (dino_x, dino_y))
        elif keys_pressed[pygame.K_DOWN] or keys_pressed[pygame.K_s]:
            window.blit(dino_run_down[dino_active], (dino_x, dino_y + 30))
        else:
            window.blit(dino_run[dino_active], (dino_x, dino_y))

        if dino_active == 1:
            dino_active = 0
        else:
            dino_active += 1

        # Прыжок
        if not prig_dino:
            if keys_pressed[pygame.K_SPACE] or keys_pressed[pygame.K_UP] or keys_pressed[pygame.K_w]:
                prig_dino = True
        else:
            if jump_count >= -10:
                if jump_count > 0:
                    dino_y -= (jump_count ** 2) / 2
                else:
                    dino_y += (jump_count ** 2) / 2
                jump_count -= 1

            else:
                prig_dino = False
                jump_count = 10

        # Двигать
        if keys_pressed[pygame.K_RIGHT] and dino_x < 1000 or keys_pressed[pygame.K_d] and dino_x < 1000:
            dino_x += dino_speed
        elif keys_pressed[pygame.K_LEFT] and dino_x > 50 or keys_pressed[pygame.K_a] and dino_x > 50:
            dino_x -= dino_speed

        # Птица настройки
        if fly_active == 1:
            fly_active = 0
        else:
            fly_active += 1

        # Прикосновение
        dino_rect_left = dino_run_left[0].get_rect(topleft=(dino_x - 2, dino_y + 5))
        dino_rect_down = dino_run_left[0].get_rect(topleft=(dino_x, dino_y + 5))

        if fly_boo_spisok:
            for (num_index, el) in enumerate(fly_boo_spisok):
                window.blit(fly_dino_boo[fly_active], el)
                el.x -= 30

                if el.x == -10:
                    fly_boo_spisok.pop(num_index)

                if dino_rect_left.colliderect(el) or dino_rect_down.colliderect(el):
                    print("\nВЫ СТОЛКНУЛИСЬ!")
                    music_fon_game.stop()
                    game_play = False
                    music_game_over.play(0)
    else:
        window.fill((87, 88, 89))
        window.blit(lose_sms_str, (350, 200))
        window.blit(restart_img, (350, 400))
        window.blit(restart_game, restart_game_rect)

        mouse = pygame.mouse.get_pos()
        if restart_game_rect.collidepoint(mouse) and pygame.mouse.get_pressed():
            game_play = True
            music_fon_game.play(0)
            dino_x = 50
            fly_boo_spisok.clear()

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running_game = False
        if event.type == fly_timer:
            fly_boo_spisok.append(fly_dino_boo[fly_active].get_rect(topleft=(1157, 250)))

    time_clock.tick(13)

pygame.quit()
