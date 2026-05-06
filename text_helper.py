import pygame
from const import FONT_NAME


def draw_text(screen, text_size, text, color, center_pos):
    font = pygame.font.SysFont(FONT_NAME, text_size, bold=True)
    surf = font.render(text, True, color).convert_alpha()
    rect = surf.get_rect(center=center_pos)
    screen.blit(surf, rect)


def draw_text_left(screen, text_size, text, color, pos):
    font = pygame.font.SysFont(FONT_NAME, text_size, bold=True)
    surf = font.render(text, True, color).convert_alpha()
    rect = surf.get_rect(topleft=pos)
    screen.blit(surf, rect)
    return rect