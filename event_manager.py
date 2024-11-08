# event_manager.py

import pygame
from utils import TILE_SIZE, GRID_WIDTH, GRID_HEIGHT


class EventManager:
    def __init__(self, grid, characters):
        self.grid = grid
        self.characters = characters

        # Definir eventos personalizados
        self.EVENT_EVERY_30_SECONDS = pygame.USEREVENT + 1

        # Configurar temporizador para el evento cada 30 segundos
        pygame.time.set_timer(self.EVENT_EVERY_30_SECONDS,
                              30000)

    def process_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                return False  # Señal para salir del juego

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    grid_x = mouse_pos[0] // TILE_SIZE
                    grid_y = mouse_pos[1] // TILE_SIZE
                    if 0 <= grid_x < GRID_WIDTH and 0 <= grid_y < GRID_HEIGHT:
                        if self.grid[grid_y][grid_x] == 0:
                            # Asignar el objetivo al primer personaje de tipo 1 (opcional)
                            pass

            elif event.type == self.EVENT_EVERY_30_SECONDS:
                print("Evento de 30 segundos disparado")
                # Disparar el evento para todos los personajes
                for character in self.characters:
                    character.event_triggered = True

            else:
                # Manejar otros eventos si es necesario
                pass

        return True
