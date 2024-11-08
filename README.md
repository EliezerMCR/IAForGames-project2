# Representación del Mundo con Grid y Pathfinding A*

Este proyecto fue desarrollado como la base de un video juego para la asignatura "Inteligencia Artificial para Videojuegos - CI6450" de la Universidad Simon Bolivar. El cual representa un mundo basado en una cuadrícula (grid), donde múltiples personajes con diferentes comportamientos se mueven y reaccionan a eventos en el entorno. Utiliza Pygame para la visualización y el algoritmo A* para el cálculo de rutas, integrando conceptos de inteligencia artificial mediante árboles de decisión.

## Tabla de Contenidos

- [Características](#características)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Ejecución](#ejecución)
- [Cómo Jugar](#cómo-jugar)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Implementación Detallada](#implementación-detallada)
  - [1. Representación del Mundo](#1-representación-del-mundo)
  - [2. Algoritmo A* para Pathfinding](#2-algoritmo-a-para-pathfinding)
  - [3. Clases de Personajes y Árboles de Decisión](#3-clases-de-personajes-y-árboles-de-decisión)
  - [4. Gestión de Eventos](#4-gestión-de-eventos)
  - [5. Visualización e Interfaz](#5-visualización-e-interfaz)
- [Personalización](#personalización)
- [Créditos](#créditos)
- [Licencia](#licencia)

## Características

- **Grid basado en nodos:** El mundo se representa como una cuadrícula bidimensional donde cada celda puede ser transitable (`0`) o un obstáculo (`1`).
- **Obstáculos aleatorios:** Se generan aleatoriamente al menos 6 obstáculos de tamaño variable en el mapa, sin bloquear completamente el paso.
- **Tres tipos de personajes con comportamientos únicos:**
  - **Tipo 1 (Naranja):** Patrullan entre puntos predefinidos. Al activarse un evento, se dirigen a una posición específica.
  - **Tipo 2 (Rojo):** Siguen al personaje más cercano de otro tipo. Al activarse el evento, huyen a una posición segura.
  - **Tipo 3 (Azul):** Se mueven aleatoriamente. Al activarse el evento, se detienen.
- **Evitación de colisiones:** Los personajes evitan chocar entre sí y recalculan sus rutas si es necesario.
- **Eventos temporizados:** Cada 30 segundos, se activa un evento que afecta el comportamiento de los personajes.
- **Visualización interactiva:**
  - **Conexiones entre nodos:** Se puede mostrar u ocultar las conexiones entre nodos adyacentes en el grid mediante un botón.
  - **Indicación de alarma:** Cuando el evento está activo, el fondo cambia de color y aparece el mensaje "ALARM ACTIVE".
  - **Estados de los personajes:** Se muestra el estado actual de cada personaje sobre su posición en el grid.

## Requisitos

- **Python 3.x**
- **Pygame**

## Instalación

1. **Clonar el repositorio o descargar los archivos del proyecto.**

2. **Asegurarse de tener Pygame instalado en el entorno de Python.**

## Ejecución

Ejecuta el script `main.py` desde la línea de comandos:

    python main.py

## Cómo Jugar

- **Visualización de conexiones:**
  - Haz clic en el botón "Conexiones: ON/OFF" en la esquina superior izquierda para mostrar u ocultar las conexiones entre nodos en el grid.

- **Observa el comportamiento de los personajes:**
  - **Tipo 1 (Naranja):** Patrullan entre puntos predefinidos. Al activarse el evento, se dirigen a una posición específica.
  - **Tipo 2 (Rojo):** Siguen al personaje más cercano de otro tipo. Al activarse el evento, huyen a la esquina inferior derecha.
  - **Tipo 3 (Azul):** Se mueven aleatoriamente por el mapa. Al activarse el evento, se detienen.

- **Evento de alarma:**
  - Cada 30 segundos, se activa un evento que afecta a todos los personajes.
  - Cuando el evento está activo, el fondo cambia a un tono rojizo y aparece el mensaje "ALARM ACTIVE" en la parte superior de la pantalla.

## Estructura del Proyecto

- **`main.py`**: Archivo principal que ejecuta el programa. Configura el grid, genera los obstáculos y personajes, y contiene el bucle principal del juego.
- **`character.py`**: Define la clase `Character` que representa a los personajes en el juego. Incluye métodos para movimiento, cálculo de rutas y dibujo en pantalla.
- **`decision_tree.py`**: Implementa los nodos de decisión y acción para crear árboles de decisión que definen el comportamiento de los personajes.
- **`decision_trees.py`**: Contiene las funciones que construyen los árboles de decisión para cada tipo de personaje.
- **`astar.py`**: Implementa el algoritmo A* para el cálculo de rutas en el grid.
- **`node.py`**: Define la clase `Node` utilizada por el algoritmo A*.
- **`event_manager.py`**: Gestiona los eventos del juego, incluyendo el temporizador para activar el evento cada 30 segundos.
- **`utils.py`**: Contiene constantes y funciones utilitarias, como tamaños de grid, colores y dimensiones de la ventana.

## Implementación Detallada

### 1. Representación del Mundo

El mundo se representa mediante una matriz bidimensional (`grid`) donde cada elemento indica si una celda es transitable (`0`) u obstáculo (`1`).

- **Generación del grid:**
  - Se inicializa una matriz de ceros con dimensiones definidas por `GRID_WIDTH` y `GRID_HEIGHT`.
  - Se añaden paredes externas marcando las celdas en los bordes como obstáculos.
  - Se generan obstáculos aleatorios mediante la función `generate_random_obstacles`, que coloca rectángulos de tamaño y posición aleatoria en el grid, asegurando que no bloqueen completamente el mapa.

### 2. Algoritmo A* para Pathfinding

El algoritmo A* se utiliza para calcular la ruta más corta desde una posición inicial hasta un objetivo, teniendo en cuenta los obstáculos y el costo de movimiento.

- **Clase `AStar`:**
  - Implementa el algoritmo A* considerando movimiento en 8 direcciones (incluyendo diagonales).
  - Utiliza una heurística de distancia octil para estimar el costo restante hasta el objetivo.
  - Evita el corte de esquinas al no permitir movimientos diagonales si ambos adyacentes son obstáculos.

- **Clase `Node`:**
  - Representa un nodo en el grid, almacenando su posición, costos (`g`, `h`, `f`), y referencia al nodo padre para reconstruir el camino.

### 3. Clases de Personajes y Árboles de Decisión

Cada personaje se modela mediante la clase `Character`, que encapsula su estado, posición, color y lógica de movimiento. Los comportamientos se definen mediante árboles de decisión personalizados para cada tipo de personaje.

- **Clase `Character`:**
  - **Atributos principales:**
    - `x`, `y`: Posición en el grid.
    - `grid`: Referencia al grid del mundo.
    - `astar`: Instancia del algoritmo A* para calcular rutas.
    - `path`: Lista de posiciones que componen el camino hacia el objetivo.
    - `state`: Estado actual del personaje (`idle`, `moving`, `event`, `fleeing`, etc.).
    - `characters_list`: Lista de todos los personajes en el juego, necesaria para evitar colisiones y, en el caso de los personajes de Tipo 2, seguir a otros personajes.
    - `character_type`: Indica el tipo de personaje (1, 2 o 3).
  - **Métodos principales:**
    - `move_to(target_x, target_y)`: Establece un objetivo y calcula la ruta hacia él.
    - `calculate_path()`: Calcula la ruta evitando obstáculos y posiciones ocupadas por otros personajes.
    - `update()`: Actualiza el estado del personaje, evalúa su árbol de decisión y avanza en el camino si es posible.
    - `draw(screen)`: Dibuja el personaje en la pantalla, mostrando también su estado actual.

- **Árboles de decisión:**
  - **Implementación general:**
    - Utiliza nodos de decisión (`DecisionNode`) y nodos de acción (`ActionNode`) para crear una estructura que define el comportamiento del personaje en función de condiciones y acciones.
    - Cada personaje tiene su propio árbol de decisión construido mediante funciones en `decisions.py`.

  - **Tipo 1 (Naranja):**
    - **Comportamiento normal:** Patrulla entre puntos predefinidos.
    - **Evento activado:** Se mueve a una posición específica (por ejemplo, coordenadas `(2, 2)`).
    - **Árbol de decisión:**
      1. **¿Evento activado?**
         - **Sí:** Ejecuta `move_to_event_point()`.
         - **No:** Verifica si está `idle`.
            - **Sí:** Ejecuta `move_to_next_patrol_point()`.
            - **No:** No hace nada.

  - **Tipo 2 (Rojo):**
    - **Comportamiento normal:** Sigue al personaje más cercano de otro tipo.
    - **Evento activado:** Huye a una posición segura (esquina inferior derecha).
    - **Árbol de decisión:**
      1. **¿Evento activado?**
         - **Sí:** Ejecuta `flee_to_safe_spot()`.
         - **No:** Verifica si está `idle`.
            - **Sí:** Ejecuta `follow_closest_character()`.
            - **No:** No hace nada.

  - **Tipo 3 (Azul):**
    - **Comportamiento normal:** Se mueve aleatoriamente por el mapa.
    - **Evento activado:** Se detiene.
    - **Árbol de decisión:**
      1. **¿Evento activado?**
         - **Sí:** Ejecuta `stop_moving()`.
         - **No:** Verifica si está `idle`.
            - **Sí:** Ejecuta `move_randomly()`.
            - **No:** No hace nada.

### 4. Gestión de Eventos

El `EventManager` se encarga de procesar los eventos del juego, incluyendo el evento temporizado que afecta a los personajes.

- **Clase `EventManager`:**
  - Configura un temporizador que dispara un evento cada 30 segundos.
  - En el método `process_events()`, detecta cuando ocurre el evento y actualiza el atributo `event_triggered` de cada personaje a `True`.
  - También maneja eventos de teclado y ratón, como el cierre de la ventana o clics en la interfaz.

### 5. Visualización e Interfaz

El juego utiliza Pygame para la visualización gráfica, representando el grid, obstáculos, personajes y elementos de la interfaz.

- **Grid y obstáculos:**
  - Se dibujan rectángulos para cada celda del grid, coloreando los obstáculos de gris y las celdas transitables de un tono más claro.
  - Opcionalmente, se pueden mostrar las conexiones entre nodos adyacentes al activar la opción correspondiente.

- **Personajes:**
  - Se representan como círculos de colores (naranja, rojo o azul) dependiendo de su tipo.
  - Sobre cada personaje, se muestra su estado actual utilizando texto renderizado con Pygame.

- **Interfaz de usuario:**
  - **Botón de conexiones:** Permite al usuario mostrar u ocultar las conexiones entre nodos en el grid.
  - **Indicador de alarma:** Cuando el evento está activo, se muestra el mensaje "ALARM ACTIVE" en la parte superior de la pantalla, y el fondo cambia a un tono rojizo.

- **Bucle principal:**
  - En cada iteración, se procesan los eventos, se actualizan los personajes y se renderiza la escena completa, incluyendo la interfaz y elementos visuales.

## Personalización

- **Modificar el número y tamaño de obstáculos:**
  - En `main.py`, puedes ajustar los parámetros de la función `generate_random_obstacles` para cambiar el número y el tamaño máximo de los obstáculos.

        generate_random_obstacles(grid, num_obstacles=6, max_obstacle_size=10)

- **Ajustar comportamientos de personajes:**
  - Puedes modificar los árboles de decisión en `decision_trees.py` para alterar el comportamiento de los personajes o añadir nuevos tipos con comportamientos personalizados.
- **Cambiar frecuencias de eventos:**
  - En `event_manager.py`, puedes cambiar el intervalo del temporizador para que el evento ocurra con mayor o menor frecuencia.

        pygame.time.set_timer(self.EVENT_EVERY_30_SECONDS, 30000)  # 30000 ms = 30 segundos

- **Personalizar la interfaz:**
  - Puedes modificar el diseño y elementos visuales en `main.py` para cambiar la apariencia del juego, como colores, fuentes y disposición de elementos.

## Créditos
 Eliezer Cario 18-10605


---