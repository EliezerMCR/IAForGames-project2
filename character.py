# character.py

import pygame
from utils import TILE_SIZE
from decision_tree import DecisionNode, ActionNode
import random
from astar import AStar


class Character:
    def __init__(self, x, y, grid, astar, decision_tree_builder, character_type, color=(255, 0, 0)):
        self.x = x  # Posición x en el grid
        self.y = y  # Posición y en el grid
        self.grid = grid  # Referencia al grid
        self.astar = astar  # Instancia de AStar
        self.grid_width = len(grid[0])
        self.grid_height = len(grid)
        self.path = []  # Lista de posiciones (x, y) que componen el camino
        self.index = 0  # Índice de la posición actual en el camino
        self.color = color  # Color del personaje

        self.event_triggered = False  # Indica si el evento se ha disparado
        self.state = 'idle'  # Estado actual del personaje
        self.target = None  # Objetivo actual (x, y)
        self.user_target = None  # Objetivo asignado por el usuario
        self.characters_list = []  # Lista de todos los personajes
        self.character_type = character_type  # Tipo de personaje (1, 2, o 3)

        # Crear el árbol de decisión utilizando la función proporcionada
        self.decision_tree = decision_tree_builder(self)

    def move_to(self, target_x, target_y):
        self.target = (target_x, target_y)
        self.calculate_path()
        self.state = 'moving'

    def calculate_path(self):
        start = (self.x, self.y)
        end = self.target

        # Crear un conjunto de posiciones ocupadas por otros personajes, excluyendo el objetivo
        occupied_positions = set(
            (other.x, other.y)
            for other in self.characters_list
            if other != self and (other.x, other.y) != self.target
        )

        # Crear una copia temporal del grid para tener en cuenta las posiciones ocupadas
        temp_grid = [row[:] for row in self.grid]
        for pos in occupied_positions:
            x, y = pos
            if 0 <= x < self.grid_width and 0 <= y < self.grid_height:
                temp_grid[y][x] = 1  # Marcamos como obstáculo

        # Crear una instancia temporal de AStar con el grid modificado
        temp_astar = AStar(temp_grid)

        # Intentar encontrar un camino hacia el objetivo
        self.path = temp_astar.find_path(start, end)
        self.index = 0  # Reiniciamos el índice al inicio del camino

        # Crear una instancia temporal de AStar con el grid modificado
        temp_astar = AStar(temp_grid)

        # Intentar encontrar un camino hacia el objetivo
        self.path = temp_astar.find_path(start, end)
        self.index = 0  # Reiniciamos el índice al inicio del camino

    def update(self):
        # Evaluar el árbol de decisión
        self.decision_tree.evaluate()

        # Moverse a lo largo del camino si es posible
        if self.path and self.index < len(self.path):
            next_x, next_y = self.path[self.index]

            # Verificar colisiones con otros personajes
            collision = False
            for other in self.characters_list:
                if other != self and (other.x, other.y) == (next_x, next_y):
                    collision = True
                    break

            if not collision:
                # No hay colisión, moverse al siguiente nodo
                self.x, self.y = next_x, next_y
                self.index += 1
                if self.index >= len(self.path):
                    # Llegó al final del camino
                    self.state = 'idle'
                    self.target = None
            else:
                # Hay colisión, esperar o recalcular ruta
                self.calculate_path()
        else:
            self.state = 'idle'

    def draw(self, screen):
        # Dibujar el personaje como un círculo en el centro de la tile
        center_x = self.x * TILE_SIZE + TILE_SIZE // 2
        center_y = self.y * TILE_SIZE + TILE_SIZE // 2
        pygame.draw.circle(screen, self.color,
                           (center_x, center_y), TILE_SIZE // 3)
