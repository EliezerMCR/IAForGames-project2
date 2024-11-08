# main.py
import pygame
from astar import AStar
from character import Character
from utils import *
from event_manager import EventManager
from decision_tree import DecisionNode, ActionNode
from decisions import *


def draw_button(screen, x, y, width, height, text, active):
    rect = pygame.Rect(x, y, width, height)
    color = (0, 200, 0) if active else (200, 0, 0)
    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, (0, 0, 0), rect, 2)
    font = pygame.font.SysFont(None, 24)
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)
    return rect


def get_neighbors(x, y, grid):
    neighbors = []
    # Movimientos en 8 direcciones (incluyendo diagonales)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1),
                  (-1, -1), (-1, 1), (1, -1), (1, 1)]

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT:
            if grid[ny][nx] == 0:
                # Prevenir el corte de esquinas
                if dx != 0 and dy != 0:
                    if grid[y][nx] != 0 and grid[ny][x] != 0:
                        continue  # Si ambos adyacentes son obstáculos, no permitir movimiento diagonal
                neighbors.append((nx, ny))
    return neighbors


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(
        "World Representation with Grid and A* Pathfinding")
    clock = pygame.time.Clock()

    # Crear el mapa (grid) como una matriz 2D
    grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

    # Añadir paredes externas
    for x in range(GRID_WIDTH):
        grid[0][x] = 1  # Pared superior
        grid[GRID_HEIGHT - 1][x] = 1  # Pared inferior
    for y in range(GRID_HEIGHT):
        grid[y][0] = 1  # Pared izquierda
        grid[y][GRID_WIDTH - 1] = 1  # Pared derecha

    # Añadir obstáculos internos
    for y in range(5, 15):
        grid[y][15] = 1  # Obstáculo vertical
    for x in range(15, 25):
        grid[10][x] = 1  # Obstáculo horizontal

    show_connections = False  # Variable para controlar la visibilidad de las conexiones

    # Crear una instancia de AStar
    astar = AStar(grid)

    # Crear seis personajes, dos de cada tipo
    characters = []

    # Tipo 1
    character1 = Character(
        2, 2, grid, astar, build_decision_tree_type1, 1, ORANGE)
    character2 = Character(
        3, 3, grid, astar, build_decision_tree_type1, 1, ORANGE)
    characters.extend([character1, character2])

    # Tipo 2
    character3 = Character(
        5, 12, grid, astar, build_decision_tree_type2, 2, RED)
    character4 = Character(
        6, 13, grid, astar, build_decision_tree_type2, 2, RED)
    characters.extend([character3, character4])

    # Tipo 3
    character5 = Character(
        15, 3, grid, astar, build_decision_tree_type3, 3, BLUE)
    character6 = Character(
        16, 4, grid, astar, build_decision_tree_type3, 3, BLUE)
    characters.extend([character5, character6])

    # Asignar la lista de personajes a cada personaje
    for character in characters:
        character.characters_list = characters

    # Inicializar el EventManager
    event_manager = EventManager(grid, characters)

    running = True
    while running:
        # Manejar eventos
        running = event_manager.process_events()

        # Manejar el botón para mostrar/ocultar conexiones
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        button_rect = draw_button(screen, 10, 10, 200, 40, "Conexiones: " +
                                  ("ON" if show_connections else "OFF"), show_connections)
        if button_rect.collidepoint(mouse_pos) and mouse_pressed[0]:
            show_connections = not show_connections
            pygame.time.delay(200)

        # Actualizar personajes
        for character in characters:
            character.update()

        # Dibujar el fondo
        screen.fill((255, 255, 255))

        # Dibujar las tiles y la cuadrícula
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                rect = pygame.Rect(x * TILE_SIZE, y *
                                   TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if grid[y][x] == 1:
                    pygame.draw.rect(screen, (100, 100, 100), rect)
                else:
                    pygame.draw.rect(screen, (200, 200, 200), rect)
                pygame.draw.rect(screen, (0, 0, 0), rect, 1)

                # Dibujar conexiones entre nodos
                if show_connections and grid[y][x] == 0:
                    neighbors = get_neighbors(x, y, grid)
                    for nx, ny in neighbors:
                        start_pos = (x * TILE_SIZE + TILE_SIZE //
                                     2, y * TILE_SIZE + TILE_SIZE // 2)
                        end_pos = (nx * TILE_SIZE + TILE_SIZE // 2,
                                   ny * TILE_SIZE + TILE_SIZE // 2)
                        pygame.draw.line(screen, (0, 0, 255),
                                         start_pos, end_pos, 1)

        # Dibujar el camino de los personajes
        for character in characters:
            if character.path:
                for pos in character.path[character.index:]:
                    x, y = pos
                    rect = pygame.Rect(x * TILE_SIZE, y *
                                       TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    pygame.draw.rect(screen, (0, 255, 0), rect)

        # Dibujar personajes
        for character in characters:
            character.draw(screen)

        pygame.display.flip()
        clock.tick(5)

    pygame.quit()


if __name__ == "__main__":
    main()
