import pygame
import time

pygame.init()
pygame.mixer.init()

screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Multi-Line Typing Effect with Sound")

font = pygame.font.Font(None, 36)
text = """Привет! Меня зовут Грег, мне нужна твоя помощь."""
lines = text.splitlines()
current_lines = []
line_index = 0
text_index = 0
typing_delay = 0.05
last_type_time = 0
line_spacing = 10
black = (0, 0, 0)
white = (255, 255, 255)

try:
    typing_sound = pygame.mixer.Sound("Sounds_Key 1 press.wav")
except pygame.error as e:
    print(f"Не удалось загрузить звук key_press.wav: {e}")
    typing_sound = None


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    current_time = time.time()
    if line_index < len(lines):
        if text_index < len(lines[line_index]) and current_time - last_type_time >= typing_delay:
            if len(current_lines) <= line_index:
                current_lines.append("")
            current_lines[line_index] += lines[line_index][text_index]
            text_index += 1
            last_type_time = current_time
            if typing_sound and text_index % 2 == 0:
              typing_sound.play()

        elif text_index >= len(lines[line_index]):
             line_index += 1
             text_index = 0


    screen.fill(white)
    y_offset = screen_height // 2 - (len(current_lines) * (font.get_height() + line_spacing)) //2

    for i, line in enumerate(current_lines):
      text_surface = font.render(line, True, black)
      text_rect = text_surface.get_rect(center=(screen_width // 2, y_offset))
      screen.blit(text_surface, text_rect)
      y_offset += font.get_height() + line_spacing

    pygame.display.flip()

pygame.quit()