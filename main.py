import pygame
from title_screen import run_title_screen

pygame.init()

screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("CS Escape Room")
clock = pygame.time.Clock()

run_title_screen(screen, clock)

pygame.quit()