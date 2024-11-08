# decision_trees.py

from decision_tree import DecisionNode, ActionNode
import random


def build_decision_tree_type1(character):
    # Tipo 1: Patrulla entre puntos predefinidos. Si el evento se dispara, se mueve a una posición específica.

    patrol_points = [(5, 5), (15, 5), (15, 15), (5, 15)]
    # Usamos una lista para permitir modificación en closure
    current_patrol_index = [0]

    # Acciones
    def move_to_next_patrol_point():
        target = patrol_points[current_patrol_index[0]]
        character.move_to(*target)
        current_patrol_index[0] = (
            current_patrol_index[0] + 1) % len(patrol_points)

    def move_to_event_point():
        if character.state != 'event':
            character.move_to(2, 2)
            character.state = 'event'
            character.event_triggered = False

    # Condiciones
    def is_event_triggered():
        return character.event_triggered

    def is_idle():
        return character.state == 'idle'

    # Árbol de decisión
    root = DecisionNode(
        is_event_triggered,
        ActionNode(move_to_event_point),
        DecisionNode(
            is_idle,
            ActionNode(move_to_next_patrol_point),
            ActionNode(lambda: None)  # No hacer nada
        )
    )

    return root


def build_decision_tree_type2(character):
    # Tipo 2: Sigue al personaje más cercano de otro tipo. Si el evento se dispara, huye a una posición segura.

    # Acciones
    def follow_closest_character():
        # Filtrar personajes de otros tipos
        other_characters = [c for c in character.characters_list if c !=
                            character and c.character_type != character.character_type]
        if not other_characters:
            return  # No hay personajes de otros tipos para seguir

        closest_character = min(
            other_characters,
            key=lambda c: (c.x - character.x) ** 2 + (c.y - character.y) ** 2,
            default=None
        )
        if closest_character:
            # Intentar moverse a una posición adyacente al personaje más cercano
            target_positions = [
                (closest_character.x + dx, closest_character.y + dy)
                for dx in [-1, 0, 1]
                for dy in [-1, 0, 1]
                if (dx != 0 or dy != 0)
            ]
            # Filtrar posiciones válidas y no ocupadas
            valid_targets = [
                (x, y) for x, y in target_positions
                if 0 <= x < character.grid_width and 0 <= y < character.grid_height
                and character.grid[y][x] == 0
                and all((x, y) != (other.x, other.y) for other in character.characters_list)
            ]
            if valid_targets:
                # Elegir la posición más cercana
                target = min(valid_targets, key=lambda pos: (
                    pos[0] - character.x) ** 2 + (pos[1] - character.y) ** 2)
                character.move_to(*target)
            else:
                # No hay posiciones válidas, esperar
                pass

    def flee_to_safe_spot():
        if character.state != 'fleeing':
            character.move_to(character.grid_width - 2,
                              character.grid_height - 2)
            character.state = 'fleeing'
            character.event_triggered = False

    # Condiciones
    def is_event_triggered():
        return character.event_triggered

    def is_idle():
        return character.state == 'idle'

    # Árbol de decisión
    root = DecisionNode(
        is_event_triggered,
        ActionNode(flee_to_safe_spot),
        DecisionNode(
            is_idle,
            ActionNode(follow_closest_character),
            ActionNode(lambda: None)  # No hacer nada
        )
    )

    return root


def build_decision_tree_type3(character):
    # Tipo 3: Se mueve aleatoriamente. Si el evento se dispara, se detiene.

    # Acciones
    def move_randomly():
        if character.state != 'moving':
            while True:
                target_x = random.randint(1, character.grid_width - 2)
                target_y = random.randint(1, character.grid_height - 2)
                if character.grid[target_y][target_x] == 0:
                    break
            character.move_to(target_x, target_y)
            character.state = 'moving'

    def stop_moving():
        character.path = []
        character.index = 0
        character.state = 'stopped'
        character.event_triggered = False

    # Condiciones
    def is_event_triggered():
        return character.event_triggered

    def is_idle():
        return character.state == 'idle'

    # Árbol de decisión
    root = DecisionNode(
        is_event_triggered,
        ActionNode(stop_moving),
        DecisionNode(
            is_idle,
            ActionNode(move_randomly),
            ActionNode(lambda: None)  # No hacer nada
        )
    )

    return root
