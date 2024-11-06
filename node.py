# node.py

from math import sqrt


class Node:
    def __init__(self, position, parent=None):
        self.position = position  # Posición del nodo en el grid (x, y)
        self.parent = parent      # Nodo padre en el camino
        self.g = 0                # Costo desde el inicio hasta este nodo
        self.h = 0                # Heurística (estimación) hasta el objetivo
        self.f = 0                # Costo total (g + h)
        # Costo de movimiento desde el padre a este nodo (por defecto 1)
        self.move_cost = 1

    def __eq__(self, other):
        return self.position == other.position
