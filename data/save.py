import pygame

pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Scrolling Quests with Scrollbar")

# --- Загрузка ресурсов ---
font = pygame.font.Font(None, 30)
quest_background = pygame.Surface((screen_width - 40, 80))
quest_background.fill((200, 200, 200))

# Загрузка изображений для скроллбара и бегунка
scrollbar_image = pygame.image.load("scrollbar.png")  # Замените на путь к вашему изображению
thumb_image = pygame.image.load("thumb.png")  # Замените на путь к вашему изображению

# --- Класс для квеста (спрайта) ---
class Quest(pygame.sprite.Sprite):
    def __init__(self, text, y_pos, font, background):
        pygame.sprite.Sprite.__init__(self)
        self.text = text
        self.y_pos = y_pos
        self.image = background.copy()
        text_surface = font.render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.image.get_rect().center)
        self.image.blit(text_surface, text_rect)
        self.rect = self.image.get_rect(topleft=(20, y_pos))

# --- Создание квестов ---
quests = []
for i in range(20):
    quests.append(Quest(f"Quest #{i+1}: Destroy the evil thing",
                      80 * i + 20,
                      font,
                      quest_background))

# --- Группа для спрайтов квестов ---
quest_group = pygame.sprite.Group(quests)

# --- Управление камерой ---
camera_y = 0
scroll_speed = 30

# --- Скроллбар ---
scrollbar_width = scrollbar_image.get_width()
scrollbar_height = scrollbar_image.get_height()
scrollbar_x = screen_width - scrollbar_width - 10
scrollbar_y = 20
scrollbar_rect = pygame.Rect(scrollbar_x, scrollbar_y, scrollbar_width, scrollbar_height)

# Бегунок
thumb_width = thumb_image.get_width()
thumb_height = thumb_image.get_height()
thumb_y = scrollbar_y
thumb_rect = pygame.Rect(scrollbar_x, thumb_y, thumb_width, thumb_height)

thumb_dragging = False
total_height = (len(quests) * 80 + 20)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # --- Обработка событий мыши ---
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
               if thumb_rect.collidepoint(event.pos):
                   thumb_dragging = True

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                thumb_dragging = False

        if event.type == pygame.MOUSEMOTION:
           if thumb_dragging:
              thumb_y = max(scrollbar_y, min(scrollbar_y + scrollbar_height - thumb_height, event.pos[1] - thumb_height//2))
              thumb_rect.y = thumb_y

        if event.type == pygame.MOUSEBUTTONDOWN:  # Обработка прокрутки колесиком
            if event.button == 4: # Колесико вверх
                camera_y = max(0, camera_y - scroll_speed)
                if total_height > screen_height:  # Пересчитываем бегунок
                    scroll_ratio = camera_y / (total_height - screen_height) # Теперь по камере
                    thumb_y = scrollbar_y + scroll_ratio * (scrollbar_height - thumb_height)
                    thumb_y = max(scrollbar_y, min(scrollbar_y + scrollbar_height - thumb_height, thumb_y))
                    thumb_rect.y = thumb_y
            if event.button == 5: # Колесико вниз
                max_scroll = len(quests) * 80 - screen_height + 20
                camera_y = min(max_scroll, camera_y + scroll_speed)
                if total_height > screen_height:  # Пересчитываем бегунок
                    scroll_ratio = camera_y / (total_height - screen_height) # Теперь по камере
                    thumb_y = scrollbar_y + scroll_ratio * (scrollbar_height - thumb_height)
                    thumb_y = max(scrollbar_y, min(scrollbar_y + scrollbar_height - thumb_height, thumb_y))
                    thumb_rect.y = thumb_y

        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_UP:
            camera_y = max(0, camera_y - scroll_speed)
            if total_height > screen_height:  # Пересчитываем бегунок
                scroll_ratio = camera_y / (total_height - screen_height) # Теперь по камере
                thumb_y = scrollbar_y + scroll_ratio * (scrollbar_height - thumb_height)
                thumb_y = max(scrollbar_y, min(scrollbar_y + scrollbar_height - thumb_height, thumb_y))
                thumb_rect.y = thumb_y

          if event.key == pygame.K_DOWN:
            max_scroll = len(quests) * 80 - screen_height + 20
            camera_y = min(max_scroll, camera_y + scroll_speed)
            if total_height > screen_height:  # Пересчитываем бегунок
                scroll_ratio = camera_y / (total_height - screen_height) # Теперь по камере
                thumb_y = scrollbar_y + scroll_ratio * (scrollbar_height - thumb_height)
                thumb_y = max(scrollbar_y, min(scrollbar_y + scrollbar_height - thumb_height, thumb_y))
                thumb_rect.y = thumb_y
    # --- Расчет позиции камеры на основе позиции бегунка ---
    if total_height > screen_height:
        scroll_ratio = (thumb_y - scrollbar_y) / (scrollbar_height - thumb_height)
        camera_y = scroll_ratio * (total_height - screen_height)
    else:
       camera_y = 0


    screen.fill((0, 0, 0))

    # -- отрисовка квестов --
    for quest in quests:
        quest_rect = quest.rect.copy()
        quest_rect.y -= camera_y
        screen.blit(quest.image, quest_rect)

    # -- Отрисовка скроллбара и бегунка --
    screen.blit(scrollbar_image, (scrollbar_x, scrollbar_y))
    screen.blit(thumb_image, (scrollbar_x, thumb_y))

    pygame.display.flip()

pygame.quit()