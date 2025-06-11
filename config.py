import pygame

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
CELL_SIZE = 40
VISIBLE_RADIUS = 100 
SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
GRID_WIDTH = SCREEN_WIDTH // CELL_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // CELL_SIZE
