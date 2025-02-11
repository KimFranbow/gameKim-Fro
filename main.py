import sys
import pygame
import os
import math

from pygame import mouse

from utils import load_and_scale_image, get_screen_size, load_image
from sprites import Button, Music, AnimatedSprite, NPC, JustSprite
from dialog import DialogWindow


def collide_v(hero, obj):
    # Вычисляем вектор
    delta_x = hero.rect.centerx - obj.rect.centerx
    delta_y = hero.rect.centery - obj.rect.centery
    distance = math.hypot(delta_x, delta_y)

    # Вектор
    if distance != 0:
        delta_x /= distance
        delta_y /= distance

    # Смещаем игрока на небольшое расстояние в противоположную сторону
    repel_strength = 5
    hero.rect.x += delta_x * repel_strength
    hero.rect.y += delta_y * repel_strength

    # Проверяем границы экрана после отталкивания
    if hero.rect.left < 0:
        hero.rect.left = 0
    if hero.rect.right > screen_width:
        hero.rect.right = screen_width
    if hero.rect.top < 0:
        hero.rect.top = 0
    if hero.rect.bottom > screen_height:
        hero.rect.bottom = screen_height


if __name__ == "__main__":
    pygame.init()
    pygame.mixer.init()  # Инициализация микшера для работы с музыкой
    screen_width, screen_height = get_screen_size()
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
    all_sprites = pygame.sprite.Group()

    # Загружаем начальный фон
    background = load_and_scale_image("background.png", screen_width, screen_height)

    # Загружаем музыку
    pygame.mixer.music.load('data\music.mp3')
    pygame.mixer.music.set_volume(0.5)  # Громкость

    # Создаем кнопки
    but_play = Button(all_sprites, "bt_start.png", "bt_start1.png")
    bt_save = Button(all_sprites, "bt_save.png", "bt_save_1.png")
    bt_music = Music(all_sprites, "bt_music_on.png", "bt_music_off.png")
    bt_exit = Button(all_sprites, "bt_exit.png", "bt_exit_1.png")

    # Для понимания, где мы находимся
    is_in_location1 = False
    is_nastr = False
    is_quest = False
    is_gr = False
    is_bt = False
    clock = pygame.time.Clock()
    running = True
    speed = 5
    dialog_window = None  # Окно диалога
    bt_perform = None

    # Включаем музыку при старте игры (если флаг is_music_on = True)
    bt_music.turn_music_on()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(mouse.get_pos())
                if is_gr and is_quest and bt_perform and bt_perform.mask.get_at(
                        (event.pos[0] - bt_music.rect.x, event.pos[1] - bt_music.rect.y)):
                    bt_perform.kill()
                    basetask = JustSprite(all_sprites, "basetask")
                    is_bt = True
                if is_gr and is_quest and greg.mask.get_at((event.pos[0] - bt_music.rect.x, event.pos[1] - bt_music.rect.y)):
                    bt_perform = Button(all_sprites, "bt_perform", "bt_perform_1")
                if bt_music.mask.get_at((event.pos[0] - bt_music.rect.x, event.pos[1] - bt_music.rect.y)):
                    bt_music.toggle_music()  # Переключаем музыку при нажатии
                if bt_exit.mask.get_at((event.pos[0] - bt_exit.rect.x, event.pos[1] - bt_exit.rect.y)):
                    running = False
                # if is_nastr and bt_back.mask.get_at((event.pos[0] - bt_exit.rect.x, event.pos[1] - bt_exit.rect.y)):
                    # bt_back.kill()
                #     bt_music.kill()
                #     bt_exit.kill()
                #     nastr.kill()
                if but_play.mask.get_at((event.pos[0] - but_play.rect.x, event.pos[1] - but_play.rect.y)):
                    but_play.kill()
                    bt_save.kill()
                    bt_music.kill()
                    bt_exit.kill()
                    background = load_and_scale_image("water.png", screen_width, screen_height)
                    island1 = Button(all_sprites, "island1.png", "island1.png")
                    island2 = Button(all_sprites, "island2.png", "island2.png")
                    island3 = Button(all_sprites, "island3.png", "island3.png")
                    island4 = Button(all_sprites, "island4.png", "island4.png")
                    island5 = Button(all_sprites, "island5.png", "island5.png")
                if 'island1' in locals() and island1.mask.get_at(
                        (event.pos[0] - island1.rect.x, event.pos[1] - island1.rect.y)):
                    island1.kill()
                    island2.kill()
                    island3.kill()
                    island4.kill()
                    island5.kill()
                    # При нажатии на island1 создаем sand, sea и block
                    background = load_and_scale_image("sand.png", screen_width, screen_height)
                    sea = JustSprite(all_sprites, "sea.png")
                    block = JustSprite(all_sprites, "block.png")
                    hero = AnimatedSprite(all_sprites, load_image("hero.png"), 4, 4, 820, 1)
                    npc1 = NPC(all_sprites, 'npc_1.png', 1235, 221)
                    bt_setting = JustSprite(all_sprites, "bt_setting.png")
                    bt_quest = JustSprite(all_sprites, "bt_quest.png")
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
                if event.key == pygame.K_n and is_in_location1 and is_nastr:
                    is_nastr = False
                    nastr.kill()
                    # bt_back.kill()
                    bt_music.kill()
                    bt_exit.kill()
                if event.key == pygame.K_n and is_in_location1 and not is_nastr:
                    # Настройки
                    is_nastr = True
                    nastr = JustSprite(all_sprites, "nastr.png")  # Фон
                    # Создаем кнопки
                    # bt_back = Button(all_sprites, "bt_back.png", "bt_back1.png")
                    bt_music = Music(all_sprites, "bt_music_on.png", "bt_music_off.png")
                    bt_exit = Button(all_sprites, "bt_exit.png", "bt_exit_1.png")
                    bt_exit.rect.topleft = (0, -250)
                if event.key == pygame.K_q and is_in_location1 and not is_quest:
                    # Окно квеста
                    is_quest = True
                    basetask = JustSprite(all_sprites, 'basetask.png')
                    if is_gr:
                        greg = Button(all_sprites, "greg1.png", "greg2.png")
                if event.key == pygame.K_q and is_in_location1 and is_quest:
                    is_quest = False
                    basetask.kill()
                    if is_gr:
                        greg.kill()
                    if bt_perform:
                        bt_perform.kill()


                if event.key == pygame.K_r and is_in_location1:
                    pygame.mouse.set_visible(True)
                if event.key == pygame.K_e and is_in_location1:
                    # Проверяем, находится ли игрок рядом с NPC
                    if pygame.sprite.collide_rect(hero, npc1):
                        # Создаем окно диалога
                        dialog_window = DialogWindow(all_sprites, npc1, [
                            "Привет! Меня зовут Грег, мне нужна твоя помощь.",
                            "У меня есть задание для тебя.",
                            "Ты готов помочь?",
                            ""
                        ])
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

        # Обновляем состояние кнопок при движении мыши
        mouse_pos = pygame.mouse.get_pos()
        for button in all_sprites:
            if isinstance(button, Button):
                button.update(mouse_pos)

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
            old_hero_rect = hero.rect.copy()
            # Обновляем анимацию и позицию героя
            hero.update(dx, dy, screen_width, screen_height)

            # Проверяем столкновение с block по маске
            if 'block' in locals() and hero.feet_mask.overlap(block.mask, (
                    block.rect.x - hero.feet_rect.x, block.rect.y - hero.feet_rect.y)):
                hero.rect = old_hero_rect

            if 'sea' in locals() and hero.feet_mask.overlap(sea.mask, (
                    sea.rect.x - hero.feet_rect.x, sea.rect.y - hero.feet_rect.y)):
                hero.rect = old_hero_rect

            # Проверяем столкновение с npc1 по маске
            if 'npc1' in locals() and pygame.sprite.collide_mask(hero, npc1):
                collide_v(hero, npc1)

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