import pygame
import time

from utils import load_and_scale_image, get_screen_size


class DialogWindow(pygame.sprite.Sprite):
    def __init__(self, all_sprites, npc, texts):
        super().__init__(all_sprites)
        screen_width, screen_height = get_screen_size()

        # Загружаем изображение окна диалога
        self.default_image = load_and_scale_image("dialog_window.png", screen_width, screen_height // 2.5, -1)
        self.image = self.default_image
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, screen_height // 1.7)

        # Загружаем изображение NPC и масштабируем его пропорционально
        # self.npc_image = npc.image
        # npc_width = screen_width // 8  # Ширина NPC как 1/8 ширины экрана
        # npc_height = int(self.npc_image.get_height() * (npc_width / self.npc_image.get_width()))  # Сохраняем соотношение сторон
        # self.npc_image = pygame.transform.scale(self.npc_image, (npc_width, npc_height))

        # Позиция NPC в окне диалога
        # self.npc_rect = self.npc_image.get_rect()
        # self.npc_rect.topleft = (20, self.rect.y + 20)  # Позиция NPC в окне
        #
        # # Добавляем изображение NPC на окно диалога
        # self.image.blit(self.npc_image, self.npc_rect.topleft)

        # Настройки текста
        self.font = pygame.font.Font(None, 36)
        self.texts = texts  # Список текстов для диалога
        self.current_text_index = 0  # Индекс текущего текста
        self.current_text = self.texts[self.current_text_index]  # Текущий текст
        self.lines = self.current_text.splitlines()  # Разделяем текст на строки
        self.current_lines = []  # Текущие строки, которые отображаются
        self.line_index = 0  # Индекс текущей строки
        self.text_index = 0  # Индекс текущего символа в строке
        self.typing_delay = 0.05  # Задержка между символами
        self.last_type_time = 0  # Время последнего обновления текста
        self.line_spacing = 10  # Расстояние между строками
        self.black = (0, 0, 0)  # Цвет текста

        # Звук печати
        try:
            self.typing_sound = pygame.mixer.Sound("data\Sounds_Key 1 press.wav")
        except pygame.error:
            print(f"Не удалось загрузить звук key_press.wav")
            self.typing_sound = None

    def update(self):
        """Обновляет текст с эффектом печати."""
        current_time = time.time()
        if self.line_index < len(self.lines):
            if self.text_index < len(self.lines[self.line_index]) and current_time - self.last_type_time >= self.typing_delay:
                if len(self.current_lines) <= self.line_index:
                    self.current_lines.append("")
                self.current_lines[self.line_index] += self.lines[self.line_index][self.text_index]
                self.text_index += 1
                self.last_type_time = current_time
                if self.typing_sound and self.text_index % 2 == 0:
                    self.typing_sound.play()
            elif self.text_index >= len(self.lines[self.line_index]):
                self.line_index += 1
                self.text_index = 0

    def next_text(self):
        """Переходит к следующему тексту в диалоге."""
        if self.current_text_index + 1 < len(self.texts):
            self.current_text_index += 1
            self.current_text = self.texts[self.current_text_index]
            self.lines = self.current_text.splitlines()
            self.current_lines = []
            self.line_index = 0
            self.text_index = 0


    def draw_text(self, screen):
        """Отрисовывает текст на экране."""
        y_offset = 521
        for i, line in enumerate(self.current_lines):
            text_surface = self.font.render(line, True, self.black)
            text_rect = text_surface.get_rect(topleft=(350, y_offset))
            screen.blit(text_surface, text_rect)
            y_offset += self.font.get_height() + self.line_spacing