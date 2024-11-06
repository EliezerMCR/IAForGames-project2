# astar.py
import heapq
from math import sqrt
from node import Node


class AStar:
    def __init__(self, grid):
        self.grid = grid  # El grid que representa el mapa
        self.grid_width = len(grid[0])
        self.grid_height = len(grid)

    def heuristic(self, start, end):
        # Heurística de distancia octil para movimiento en 8 direcciones
        dx = abs(start[0] - end[0])
        dy = abs(start[1] - end[1])
        D = 1
        D2 = sqrt(2)
        return D * (dx + dy) + (D2 - 2 * D) * min(dx, dy)

    def get_neighbors(self, node: Node):
        neighbors = []
        x, y = node.position
        # Movimientos: 8 direcciones (incluyendo diagonales)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1),
                      (-1, -1), (-1, 1), (1, -1), (1, 1)]

        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            # Verificar límites del grid
            if 0 <= nx < self.grid_width and 0 <= ny < self.grid_height:
                # Verificar si es un obstáculo
                if self.grid[ny][nx] == 0:
                    # Prevenir el corte de esquinas
                    if dx != 0 and dy != 0:
                        if self.grid[y][nx] != 0 and self.grid[ny][x] != 0:
                            continue  # Si ambos adyacentes son obstáculos, no permitir movimiento diagonal
                    # Calcular el costo de movimiento
                    if dx == 0 or dy == 0:
                        move_cost = 1  # Movimiento ortogonal
                    else:
                        move_cost = sqrt(2)  # Movimiento diagonal
                    neighbor = Node((nx, ny), node)
                    neighbor.move_cost = move_cost
                    neighbors.append(neighbor)
        return neighbors

    def find_path(self, start, end):
        start_node = Node(start)
        end_node = Node(end)

        open_list = []
        open_dict = {}
        closed_set = set()

        counter = 0  # Contador para desempate en el heap

        heapq.heappush(open_list, (start_node.f, counter, start_node))
        open_dict[start_node.position] = start_node
        counter += 1

        while open_list:
            current_node = heapq.heappop(open_list)[2]
            del open_dict[current_node.position]
            closed_set.add(current_node.position)

            if current_node == end_node:
                # Reconstruir el camino
                path = []
                while current_node:
                    path.append(current_node.position)
                    current_node = current_node.parent
                return path[::-1]  # Devolver el camino invertido

            neighbors = self.get_neighbors(current_node)

            for neighbor in neighbors:
                if neighbor.position in closed_set:
                    continue

                tentative_g = current_node.g + neighbor.move_cost

                if neighbor.position in open_dict:
                    existing_node = open_dict[neighbor.position]
                    if tentative_g < existing_node.g:
                        # Actualizar el nodo en open_list con mejor g
                        existing_node.g = tentative_g
                        existing_node.f = tentative_g + \
                            self.heuristic(neighbor.position,
                                           end_node.position)
                        existing_node.parent = current_node
                else:
                    neighbor.g = tentative_g
                    neighbor.h = self.heuristic(
                        neighbor.position, end_node.position)
                    neighbor.f = neighbor.g + neighbor.h
                    heapq.heappush(open_list, (neighbor.f, counter, neighbor))
                    open_dict[neighbor.position] = neighbor
                    counter += 1

        return None  # No se encontró un camino
