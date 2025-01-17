import sys
import pygame
import os
import math

def get_screen_size():
    """Возвращает размеры экрана в пикселях."""
    try:
        return (pygame.display.Info().current_w, pygame.display.Info().current_h)
    except Exception:
        try:
            import ctypes
            user32 = ctypes.windll.user32
            return (user32.GetSystemMetrics(0), user32.GetSystemMetrics(1))
        except ImportError:
            return (1024, 768)

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image

def load_and_scale_image(image_path, width, height, colorkey=None):
    """Загружает и масштабирует изображение до указанных размеров."""
    original_image = load_image(image_path, colorkey=None)
    scaled_image = pygame.transform.scale(original_image, (width, height))
    return scaled_image

class Button(pygame.sprite.Sprite):
    def __init__(self, all_sprites, image_path, hover_image_path):
        super().__init__(all_sprites)
        screen_width, screen_height = get_screen_size()
        self.default_image = load_and_scale_image(image_path, screen_width, screen_height)
        self.hover_image = load_and_scale_image(hover_image_path, screen_width, screen_height)
        self.image = self.default_image
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, mouse_pos):
        """Обновляет состояние кнопки в зависимости от положения мыши."""
        local_x = mouse_pos[0] - self.rect.x
        local_y = mouse_pos[1] - self.rect.y

        if 0 <= local_x < self.rect.width and 0 <= local_y < self.rect.height:
            if self.mask.get_at((local_x, local_y)):
                self.image = self.hover_image
            else:
                self.image = self.default_image
        else:
            self.image = self.default_image

class Music(pygame.sprite.Sprite):
    def __init__(self, all_sprites, image_path, hover_image_path):
        super().__init__(all_sprites)
        screen_width, screen_height = get_screen_size()
        self.default_image = load_and_scale_image(image_path, screen_width, screen_height)
        self.hover_image = load_and_scale_image(hover_image_path, screen_width, screen_height)
        self.image = self.default_image
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)
        self.mask = pygame.mask.from_surface(self.image)
        self.is_music_on = True  # Флаг для отслеживания состояния музыки

    def toggle_music(self):
        """Переключает состояние музыки и меняет изображение кнопки."""
        self.is_music_on = not self.is_music_on
        if self.is_music_on:
            self.image = self.default_image
            self.turn_music_on()  # Включить музыку
        else:
            self.image = self.hover_image
            self.turn_music_off()  # Выключить музыку

    def turn_music_on(self):
        """Включает музыку."""
        if self.is_music_on:  # Проверяем флаг перед воспроизведением
            pygame.mixer.music.play(-1)

    def turn_music_off(self):
        """Выключает музыку."""
        pygame.mixer.music.stop()

class Mainhero(pygame.sprite.Sprite):
    def __init__(self, all_sprites):
        super().__init__(all_sprites)
        original_image = load_image("myhero.png")
        scale_factor = 1
        self.image = pygame.transform.scale(
            original_image,
            (int(original_image.get_width() * scale_factor), int(original_image.get_height() * scale_factor))
        )
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = 10
        self.rect.y = 400

    def update(self, dx=0, dy=0, screen_width=0, screen_height=0):
        self.rect.x += dx
        self.rect.y += dy
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_width:
            self.rect.right = screen_width
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height


class NPC(pygame.sprite.Sprite):
    def __init__(self, all_sprites, name, x, y):
        super().__init__(all_sprites)
        original_image = load_image(name)
        scale_factor = 1
        self.image = pygame.transform.scale(
            original_image,
            (int(original_image.get_width() * scale_factor), int(original_image.get_height() * scale_factor))
        )
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y


class DialogWindow(pygame.sprite.Sprite):
    def __init__(self, all_sprites):
        super().__init__(all_sprites)
        screen_width, screen_height = get_screen_size()
        self.image = load_and_scale_image("dialog_window.png", screen_width, screen_height // 2.5, -1)
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, screen_height // 1.5)


if __name__ == "__main__":
    pygame.init()
    pygame.mixer.init()  # Инициализация микшера для работы с музыкой
    screen_width, screen_height = get_screen_size()
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
    all_sprites = pygame.sprite.Group()

    # Загружаем начальный фон
    background = load_and_scale_image("background.png", screen_width, screen_height)

    # Загружаем музыку для главного меню
    pygame.mixer.music.load('data\music.mp3')  # Убедитесь, что файл music.mp3 находится в той же директории
    pygame.mixer.music.set_volume(0.5)  # Устанавливаем громкость (от 0.0 до 1.0)

    # Создаем кнопки
    but_play = Button(all_sprites, "bt_start.png", "bt_start1.png")
    bt_save = Button(all_sprites, "bt_save.png", "bt_save_1.png")
    bt_music = Music(all_sprites, "bt_music_on.png", "bt_music_off.png")
    bt_exit = Button(all_sprites, "bt_exit.png", "bt_exit_1.png")

    location1 = None
    is_in_location1 = False
    clock = pygame.time.Clock()
    running = True
    speed = 5
    dialog_window = None  # Окно диалога

    # Включаем музыку при старте игры (если флаг is_music_on = True)
    bt_music.turn_music_on()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if bt_exit.mask.get_at((event.pos[0] - bt_exit.rect.x, event.pos[1] - bt_exit.rect.y)):
                    running = False
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
                if 'island1' in locals() and island1.mask.get_at((event.pos[0] - island1.rect.x, event.pos[1] - island1.rect.y)):
                    if location1 is None:
                        # Останавливаем текущую музыку
                        pygame.mixer.music.stop()
                        # Загружаем и воспроизводим музыку для location1 (если флаг is_music_on = True)
                        if bt_music.is_music_on:
                            pygame.mixer.music.load('data\location1_music.mp3')  # Убедитесь, что файл location1_music.mp3 существует
                            pygame.mixer.music.play(-1)  # Бесконечное воспроизведение

                        location1 = Button(all_sprites, "location1.png", "location1.png")
                        hero = Mainhero(all_sprites)
                        npc1 = NPC(all_sprites, 'npc_1.png', 360, 210)
                        pygame.mouse.set_visible(False)
                        is_in_location1 = True
                if bt_music.mask.get_at((event.pos[0] - bt_music.rect.x, event.pos[1] - bt_music.rect.y)):
                    bt_music.toggle_music()  # Переключаем музыку при нажатии
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q and is_in_location1:
                    running = False
                if event.key == pygame.K_e and is_in_location1:
                    # Проверяем, находится ли игрок рядом с NPC
                    if pygame.sprite.collide_rect(hero, npc1):
                        # Создаем окно диалога
                        dialog_window = DialogWindow(all_sprites)
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

            # Сохраняем текущие координаты для отката
            prev_x, prev_y = hero.rect.x, hero.rect.y
            hero.update(dx, dy, screen_width, screen_height)

            # Проверяем столкновение с NPC
            if 'npc1' in locals() and pygame.sprite.collide_mask(hero, npc1):
                # Вычисляем вектор от NPC к игроку
                delta_x = hero.rect.centerx - npc1.rect.centerx
                delta_y = hero.rect.centery - npc1.rect.centery
                distance = math.hypot(delta_x, delta_y)

                # Нормализуем вектор (делаем его длиной 1)
                if distance != 0:
                    delta_x /= distance
                    delta_y /= distance

                # Смещаем игрока на небольшое расстояние в противоположную сторону
                repel_strength = 5  # Сила отталкивания
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

        screen.blit(background, (0, 0))
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    # Останавливаем музыку при завершении игры
    pygame.mixer.music.stop()
    pygame.quit()