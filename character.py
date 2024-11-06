# character.py
import pygame
from utils import TILE_SIZE


class Character:
    def __init__(self, x, y, grid, astar, color=(255, 0, 0)):
        self.x = x  # Posición x en el grid
        self.y = y  # Posición y en el grid
        self.grid = grid  # Referencia al grid
        self.astar = astar  # Instancia de AStar
        self.path = []  # Lista de posiciones (x, y) que componen el camino
        self.index = 0  # Índice de la posición actual en el camino
        self.color = color  # Color del personaje

    def move_to(self, target_x, target_y):
        start = (self.x, self.y)
        end = (target_x, target_y)
        self.path = self.astar.find_path(start, end)
        self.index = 0  # Reiniciamos el índice al inicio del camino

    def update(self):
        if self.path and self.index < len(self.path):
            # Mover al siguiente nodo en el camino
            self.x, self.y = self.path[self.index]
            self.index += 1

    def draw(self, screen):
        # Dibujar el personaje como un círculo en el centro de la tile
        center_x = self.x * TILE_SIZE + TILE_SIZE // 2
        center_y = self.y * TILE_SIZE + TILE_SIZE // 2
        pygame.draw.circle(screen, self.color,
                           (center_x, center_y), TILE_SIZE // 3)
