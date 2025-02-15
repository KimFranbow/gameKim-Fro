import math

import pygame
from utils import load_and_scale_image, get_screen_size, load_image


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


class JustSprite(pygame.sprite.Sprite):
    def __init__(self, all_sprites, image_path):
        super().__init__(all_sprites)
        screen_width, screen_height = get_screen_size()
        self.default_image = load_and_scale_image(image_path, screen_width, screen_height)
        self.image = self.default_image
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)
        self.mask = pygame.mask.from_surface(self.image)



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
        self.is_music_on = True  # Флаг для отслеживания состояния музыки (по умолчанию False)

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


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, all_sprites, sheet, columns, rows, x, y, collision_sprites):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.collision_sprites = collision_sprites  # Спрайты, с которыми проверяем коллизии

        self.direction = "down"  # Направление движения (по умолчанию "вниз")
        self.animation_speed = 0.3  # Скорость анимации
        self.frame_counter = 0
        self.is_moving = False  # Флаг для отслеживания движения
        self.mask = pygame.mask.from_surface(self.image)  # Маска для коллизий
        self.feet_mask = self.create_feet_mask()
        self.feet_rect = self.get_feet_rect()  # Получаем rect для ног

    def cut_sheet(self, sheet, columns, rows):
        """Разрезает спрайт-лист на кадры."""
        self.rect = sheet.get_rect()
        self.frame_width = self.rect.width // columns
        self.frame_height = self.rect.height // rows
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.frame_width * i, self.frame_height * j)
                frame = sheet.subsurface(pygame.Rect(frame_location, (self.frame_width, self.frame_height)))
                self.frames.append(frame)

    def create_feet_mask(self):
        """Создает маску для ног, охватывающую нижнюю часть спрайта."""
        feet_height = self.rect.height // 4  # Нижняя четверть спрайта
        feet_surface = pygame.Surface((self.rect.width, feet_height), pygame.SRCALPHA)
        feet_surface.blit(self.image, (0, -self.rect.height + feet_height))
        return pygame.mask.from_surface(feet_surface)

    def get_feet_rect(self):
        """Создает rect для ног."""
        feet_height = self.rect.height // 4  # Нижняя четверть спрайта
        feet_rect = pygame.Rect(self.rect.x, self.rect.y + self.rect.height - feet_height, self.rect.width, feet_height)
        return feet_rect

    def move(self, dx, dy):
        """Перемещает спрайт на указанное расстояние."""
        self.rect.x += dx
        self.rect.y += dy

    def collision(self):
        """Обрабатывает коллизии с другими спрайтами."""
        for col in self.collision_sprites:
            if isinstance(col, NPC): #если он встречается с Npc - другой колайд
                if pygame.sprite.collide_mask(self, col):
                    # Вычисляем вектор
                    delta_x = self.rect.centerx - col.rect.centerx
                    delta_y = self.rect.centery - col.rect.centery
                    distance = math.hypot(delta_x, delta_y)

                    # Вектор
                    if distance != 0:
                        delta_x /= distance
                        delta_y /= distance

                    # Смещаем игрока на небольшое расстояние в противоположную сторону
                    repel_strength = 5
                    self.rect.x += delta_x * repel_strength
                    self.rect.y += delta_y * repel_strength
                    break  # Прерываем цикл, чтобы не проверять остальные спрайты
            if self.feet_mask.overlap(col.mask, (col.rect.x - self.feet_rect.x, col.rect.y - self.feet_rect.y)):
                # Если есть коллизия, возвращаем спрайт на предыдущую позицию
                self.rect = self.old_hero_rect.copy()
                break  # Прерываем цикл, чтобы не проверять остальные спрайты

    def update(self, dx=0, dy=0, screen_width=0, screen_height=0):
        """Обновляет состояние спрайта."""
        # Сохраняем текущую позицию для обработки коллизий
        self.old_hero_rect = self.rect.copy()

        # Обновляем позицию
        self.move(dx, dy)

        # Определяем направление движения
        if dx > 0:
            self.direction = "right"
            self.is_moving = True
        elif dx < 0:
            self.direction = "left"
            self.is_moving = True
        elif dy > 0:
            self.direction = "down"
            self.is_moving = True
        elif dy < 0:
            self.direction = "up"
            self.is_moving = True
        else:
            self.is_moving = False

        # Обновляем анимацию
        if self.is_moving:
            self.frame_counter += self.animation_speed
            if self.frame_counter >= 1:
                self.frame_counter = 0
                self.cur_frame = (self.cur_frame + 1) % 4  # 4 кадра в строке
        else:
            # Если персонаж не двигается, устанавливаем первый кадр текущего направления
            self.cur_frame = 0

        # Выбираем строку анимации в зависимости от направления
        if self.direction == "right":
            self.image = self.frames[self.cur_frame + 4]  # Первый кадр для "вправо"
        elif self.direction == "down":
            self.image = self.frames[self.cur_frame]  # Первый кадр для "вниз"
        elif self.direction == "up":
            self.image = self.frames[self.cur_frame + 8]  # Первый кадр для "вверх"
        elif self.direction == "left":
            self.image = self.frames[self.cur_frame + 12]  # Первый кадр для "влево"

        # Обновляем маску для коллизий
        self.mask = pygame.mask.from_surface(self.image)
        # Обновляем rect для ног
        self.feet_rect = self.get_feet_rect()

        # коллизии
        self.collision()

        # Проверяем границы экрана
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
        self.image = original_image
        # self.image = pygame.transform.scale(
        #     original_image,
        #     (int(original_image.get_width() * scale_factor), int(original_image.get_height() * scale_factor))
        # )
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y
