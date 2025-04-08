import pygame
from visualizer import main

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")

# Initialize Pygame font system
pygame.font.init()

if __name__ == "__main__":
    main(WIN, WIDTH) 