import os
import sys
import pygame
import ctypes

def get_screen_size():
    """Возвращает размеры экрана в пикселях."""
    try:
        return (pygame.display.Info().current_w, pygame.display.Info().current_h)
    except Exception:
        try:
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