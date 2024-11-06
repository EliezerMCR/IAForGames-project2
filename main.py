import pygame
from astar import AStar
from character import Character
from utils import *


def get_neighbors(x, y, grid):
    neighbors = []
    # Izquierda, derecha, arriba, abajo
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT:
            if grid[ny][nx] == 0:
                neighbors.append((nx, ny))
    return neighbors


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
    for y in range(5, 10):
        grid[y][7] = 1  # Obstáculo vertical
    for x in range(10, 15):
        grid[8][x] = 1  # Obstáculo horizontal

    show_connections = False  # Variable para controlar la visibilidad de las conexiones

    # Crear una instancia de AStar
    astar = AStar(grid)

    # Crear múltiples personajes
    characters = [
        Character(2, 2, grid, astar, ORANGE),
        Character(5, 12, grid, astar, RED),
        Character(15, 3, grid, astar, BLUE)
    ]

    # Asignar objetivos a los personajes
    characters[0].move_to(18, 15)
    characters[1].move_to(3, 8)
    characters[2].move_to(10, 14)

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Asignar nuevo objetivo al primer personaje al hacer clic
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    grid_x = mouse_pos[0] // TILE_SIZE
                    grid_y = mouse_pos[1] // TILE_SIZE
                    if 0 <= grid_x < GRID_WIDTH and 0 <= grid_y < GRID_HEIGHT:
                        if grid[grid_y][grid_x] == 0:
                            characters[0].move_to(grid_x, grid_y)

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

        # Dibujar el botón
        button_rect = draw_button(screen, 10, 10, 200, 40, "Conexiones: " +
                                  ("ON" if show_connections else "OFF"), show_connections)
        if button_rect.collidepoint(mouse_pos) and mouse_pressed[0]:
            show_connections = not show_connections
            pygame.time.delay(200)

        pygame.display.flip()
        clock.tick(5)

    pygame.quit()


if __name__ == "__main__":
    main()
