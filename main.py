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


def get_random_position(grid, occupied_positions):
    grid_width = len(grid[0])
    grid_height = len(grid)
    while True:
        x = random.randint(1, grid_width - 2)
        y = random.randint(1, grid_height - 2)
        if grid[y][x] == 0 and (x, y) not in occupied_positions:
            return x, y


def generate_random_obstacles(grid, num_obstacles=6, max_obstacle_size=10):
    grid_width = len(grid[0])
    grid_height = len(grid)
    for _ in range(num_obstacles):
        # Generar tamaño aleatorio para el obstáculo
        obstacle_width = random.randint(1, max_obstacle_size)
        obstacle_height = random.randint(1, max_obstacle_size)

        # Generar posición aleatoria para el obstáculo
        start_x = random.randint(1, grid_width - obstacle_width - 2)
        start_y = random.randint(1, grid_height - obstacle_height - 2)

        # Marcar las celdas del obstáculo en el grid
        for x in range(start_x, start_x + obstacle_width):
            for y in range(start_y, start_y + obstacle_height):
                grid[y][x] = 1  # Marcamos como obstáculo


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(
        "World Representation with Grid and A* Pathfinding")
    clock = pygame.time.Clock()
    random.seed()  # Inicializar la semilla aleatoria

    # Crear el mapa (grid) como una matriz 2D
    grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

    # Añadir paredes externas
    for x in range(GRID_WIDTH):
        grid[0][x] = 1  # Pared superior
        grid[GRID_HEIGHT - 1][x] = 1  # Pared inferior
    for y in range(GRID_HEIGHT):
        grid[y][0] = 1  # Pared izquierda
        grid[y][GRID_WIDTH - 1] = 1  # Pared derecha

    # Generar obstáculos aleatorios
    generate_random_obstacles(grid, num_obstacles=6, max_obstacle_size=10)

    show_connections = False  # Variable para controlar la visibilidad de las conexiones

    # Crear una instancia de AStar
    astar = AStar(grid)

    # Crear seis personajes, dos de cada tipo
    characters = []
    # Lista de posiciones ocupadas por otros personajes
    occupied_positions = set()

    # Tipo 1
    for _ in range(2):
        x, y = get_random_position(grid, occupied_positions)
        occupied_positions.add((x, y))
        character = Character(
            x, y, grid, astar, build_decision_tree_type1, 1, ORANGE)
        characters.append(character)

    # Tipo 2
    for _ in range(2):
        x, y = get_random_position(grid, occupied_positions)
        occupied_positions.add((x, y))
        character = Character(
            x, y, grid, astar, build_decision_tree_type2, 2, RED)
        characters.append(character)

    # Tipo 3
    for _ in range(2):
        x, y = get_random_position(grid, occupied_positions)
        occupied_positions.add((x, y))
        character = Character(
            x, y, grid, astar, build_decision_tree_type3, 3, BLUE)
        characters.append(character)

    # Asignar la lista de personajes a cada personaje
    for character in characters:
        character.characters_list = characters

    # Inicializar el EventManager
    event_manager = EventManager(grid, characters)

    running = True
    while running:
        # Process events
        running = event_manager.process_events()

        # Get mouse position and state
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        # Update characters
        for character in characters:
            character.update()

        # Check if any character is in alarm state
        alarm_active = any(character.state == 'event' or character.state ==
                           'fleeing' for character in characters)

        # Draw the background
        screen.fill((255, 200, 200) if alarm_active else (255, 255, 255))

        # Draw the tiles and grid
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                rect = pygame.Rect(x * TILE_SIZE, y *
                                   TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if grid[y][x] == 1:
                    pygame.draw.rect(screen, (100, 100, 100), rect)
                else:
                    pygame.draw.rect(screen, (200, 200, 200), rect)
                pygame.draw.rect(screen, (0, 0, 0), rect, 1)

        # Draw connections between nodes
        if show_connections:
            for y in range(GRID_HEIGHT):
                for x in range(GRID_WIDTH):
                    if grid[y][x] == 0:
                        neighbors = get_neighbors(x, y, grid)
                        for nx, ny in neighbors:
                            start_pos = (x * TILE_SIZE + TILE_SIZE //
                                         2, y * TILE_SIZE + TILE_SIZE // 2)
                            end_pos = (nx * TILE_SIZE + TILE_SIZE //
                                       2, ny * TILE_SIZE + TILE_SIZE // 2)
                            pygame.draw.line(
                                screen, (0, 0, 255), start_pos, end_pos, 1)

        # Draw the path of the characters
        for character in characters:
            if character.path:
                for pos in character.path[character.index:]:
                    x, y = pos
                    rect = pygame.Rect(x * TILE_SIZE, y *
                                       TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    pygame.draw.rect(screen, (0, 255, 0), rect)

        # Draw characters
        for character in characters:
            character.draw(screen)

        # Draw the alarm message if active
        if alarm_active:
            font = pygame.font.SysFont(None, 48)
            alarm_text = font.render("ALARM ACTIVE", True, (255, 0, 0))
            text_rect = alarm_text.get_rect(center=(WIDTH // 2, 50))
            screen.blit(alarm_text, text_rect)

        # Draw the button after everything else
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
