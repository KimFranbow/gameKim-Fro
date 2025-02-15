import sys
import pygame
import os

from pygame import mouse

from utils import load_and_scale_image, get_screen_size, load_image
from sprites import Button, Music, AnimatedSprite, NPC, JustSprite
from dialog import DialogWindow

if __name__ == "__main__":
    pygame.init()
    pygame.mixer.init()  # Инициализация микшера для работы с музыкой
    screen_width, screen_height = get_screen_size()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
    all_sprites = pygame.sprite.Group()
    collision_sprites = pygame.sprite.Group()
    nastr_spr = pygame.sprite.Group()
    task_spr = pygame.sprite.Group()
    islands = pygame.sprite.Group()

    # Загружаем начальный фон
    background = load_and_scale_image("background.png", screen_width, screen_height)

    # Загружаем музыку
    pygame.mixer.music.load('data\music.mp3')
    pygame.mixer.music.set_volume(0.5)  # Громкость

    # Создаем кнопки
    but_play = Button(all_sprites, "bt_start.png", "bt_start1.png")
    bt_rule = Button(all_sprites, "bt_rule.png", "bt_rule_1.png")
    bt_music = Music(all_sprites, "bt_music_on.png", "bt_music_off.png")
    bt_exit = Button(all_sprites, "bt_exit.png", "bt_exit_1.png")

    # Для понимания, где мы находимся
    is_in_location1 = False
    is_nastr = False
    is_quest = False
    is_gr = False
    is_bt = False

    running = True
    speed = 5
    dialog_window = None  # Окно диалога
    bt_perform = None

    bt_music.turn_music_on()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if is_gr and is_quest and bt_perform and bt_perform.mask.get_at(
                        (event.pos[0] - bt_music.rect.x, event.pos[1] - bt_music.rect.y)):
                    bt_perform.kill()
                    basetask = JustSprite(all_sprites, "basetask")
                    is_bt = True
                if is_gr and is_quest and greg.mask.get_at(
                        (event.pos[0] - bt_music.rect.x, event.pos[1] - bt_music.rect.y)):
                    bt_perform = Button(all_sprites, "bt_perform", "bt_perform_1")
                if bt_music.mask.get_at((event.pos[0] - bt_music.rect.x, event.pos[1] - bt_music.rect.y)):
                    bt_music.toggle_music()  # Переключаем музыку при нажатии
                if bt_exit.mask.get_at((event.pos[0] - bt_exit.rect.x, event.pos[1] - bt_exit.rect.y)):
                    running = False
                if is_nastr and bt_back.mask.get_at((event.pos[0] - bt_exit.rect.x, event.pos[1] - bt_exit.rect.y)):
                    is_nastr = False
                if but_play.mask.get_at((event.pos[0] - but_play.rect.x, event.pos[1] - but_play.rect.y)):
                    but_play.kill()
                    bt_rule.kill()
                    bt_music.kill()
                    bt_exit.kill()
                    background = load_and_scale_image("water.png", screen_width, screen_height)
                    island1 = Button(all_sprites, "island1.png", "island1.png")
                    island2 = Button(all_sprites, "island2.png", "island2.png")
                    island3 = Button(all_sprites, "island3.png", "island3.png")
                    island4 = Button(all_sprites, "island4.png", "island4.png")
                    island5 = Button(all_sprites, "island5.png", "island5.png")
                    islands.add(island1, island2, island3, island4, island5)
                if 'island1' in locals() and island1.mask.get_at(
                        (event.pos[0] - island1.rect.x, event.pos[1] - island1.rect.y)):
                    for el in islands:
                        el.kill()
                    # При нажатии на island1 создаем sand, sea и block
                    background = load_and_scale_image("sand.png", screen_width, screen_height)
                    sea = JustSprite(all_sprites, "sea.png")
                    hero = AnimatedSprite(all_sprites, load_image("hero.png"), 4, 4, screen_width // 2.9,
                                          screen_height // 2.6, collision_sprites)
                    npc1 = NPC(all_sprites, 'npc_1.png', 0, 0)
                    bt_setting = JustSprite(all_sprites, "bt_setting.png")
                    bt_quest = JustSprite(all_sprites, "bt_quest.png")
                    collision_sprites.add(sea, npc1)
                    is_in_location1 = True
                    pygame.mouse.set_visible(False)
                    # Останавливаем текущую музыку
                    pygame.mixer.music.stop()
                    # Загружаем и воспроизводим музыку для location1 (если флаг is_music_on = True)
                    if bt_music.is_music_on:
                        pygame.mixer.music.load(
                            'data\location1_music.mp3')
                        pygame.mixer.music.play(-1)  # Бесконечное воспроизведение
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    print(hero.rect)
                    running = False
                if event.key == pygame.K_n and is_in_location1:
                    # Настройки
                    is_nastr = not is_nastr
                if event.key == pygame.K_q and is_in_location1:
                    # Окно квеста
                    is_quest = not is_quest
                    # basetareg = Button(all_sprites, "greg1.png", "greg2.png")

                if event.key == pygame.K_r and is_in_location1:
                    pygame.mouse.set_visible(True)
                if event.key == pygame.K_e and is_in_location1:
                    # Проверяем, находится ли игрок рядом с NPC
                    if pygame.sprite.collide_rect(hero, npc1):
                        # Создаем окно диалога
                        dialog_window = DialogWindow(all_sprites, "dialog_window1.png", [
                            "Привет! Меня зовут Грег, мне нужна твоя помощь.",
                            "У меня есть задание для тебя.",
                            "Ты готов помочь?",
                            ""
                        ])
                    # if pygame.sprite.collide_rect(hero, npc2):
                    #     # Создаем окно диалога
                    #     dialog_window = DialogWindow(all_sprites, "dialog_window2.png", [])
                if event.key == pygame.K_SPACE and dialog_window:
                    # Переход к следующему тексту
                    dialog_window.next_text()
                    if dialog_window.current_text_index + 1 >= len(dialog_window.texts):
                        dialog_window.kill()
                        dialog_window = None
                        is_gr = True
                if event.key == pygame.K_ESCAPE and dialog_window:
                    # Закрываем окно диалога при нажатии ESC
                    dialog_window.kill()
                    dialog_window = None

        if is_nastr:
            pygame.mouse.set_visible(True)
            nastr = JustSprite(all_sprites, "nastr.png")
            bt_back = Button(all_sprites, "bt_back.png", "bt_back1.png")
            bt_rule = Button(all_sprites, "bt_rule.png", "bt_rule_1.png")
            bt_exit = Button(all_sprites, "bt_exit.png", "bt_exit_1.png")
            if bt_music.is_music_on:
                bt_music = Music(all_sprites, "bt_music_on.png", "bt_music_off.png")
            else:
                bt_music = Music(all_sprites, "bt_music_off.png", "bt_music_on.png")

            nastr_spr.add(nastr, bt_back, bt_rule, bt_music, bt_exit)
        else:
            for el in nastr_spr:
                el.kill()  # Удаляем спрайты из всех групп

        # dx dy персонажа
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if 'hero' in locals() and not dialog_window:  # Движение заблокировано, если диалог активен
            if keys[pygame.K_w]:
                dy = -speed
            if keys[pygame.K_s]:
                dy = speed
            if keys[pygame.K_a]:
                dx = -speed
            if keys[pygame.K_d]:
                dx = speed
            # Обновляем анимацию и позицию героя
            hero.update(dx, dy, screen_width, screen_height)

        # Обновляем состояние кнопок при движении мыши
        mouse_pos = pygame.mouse.get_pos()
        for button in all_sprites:
            if isinstance(button, Button):
                button.update(mouse_pos)

        screen.blit(background, (0, 0))
        all_sprites.draw(screen)
        if dialog_window:
            dialog_window.update()
            dialog_window.draw_text(screen)
        pygame.display.flip()
        clock.tick(60)

    # Останавливаем музыку при завершении игры
    pygame.mixer.music.stop()
    pygame.quit()
