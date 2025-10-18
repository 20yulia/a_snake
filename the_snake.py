from random import randint
from typing import Optional, Tuple

import pygame


# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для всех игровых объектов."""

    def __init__(
        self, body_color: Optional[Tuple[int, int, int]] = None
    ) -> None:
        """
        Инициализирует игровой объект.

        Args:
            body_color: Цвет объекта (по умолчанию None)
        """
        self.position: Tuple[int, int] = (
            (SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2)
        )
        self.body_color = body_color

    def draw(self) -> None:
        """Абстрактный метод для отрисовки объекта."""
        pass


class Apple(GameObject):
    """Класс для представления яблока в игре."""

    def __init__(self) -> None:
        """Инициализирует яблоко со случайной позицией."""
        super().__init__(APPLE_COLOR)
        self.randomize_position()

    def randomize_position(self) -> None:
        """Устанавливает случайную позицию для яблока."""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    def draw(self) -> None:
        """Отрисовывает яблоко на игровом поле."""
        if self.body_color is None:
            return
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс для представления змейки в игре."""

    def __init__(self) -> None:
        """Инициализирует змейку с начальными параметрами."""
        super().__init__(SNAKE_COLOR)
        self.positions: list[Tuple[int, int]] = []
        self.direction: Tuple[int, int] = RIGHT
        self.next_direction: Optional[Tuple[int, int]] = None
        self.last: Optional[Tuple[int, int]] = None
        self.reset()

    def reset(self) -> None:
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def update_direction(self) -> None:
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self) -> Tuple[int, int]:
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def move(self) -> None:
        """Перемещает змейку в текущем направлении."""
        head = self.get_head_position()
        x, y = self.direction
        new_x = (head[0] + (x * GRID_SIZE)) % SCREEN_WIDTH
        new_y = (head[1] + (y * GRID_SIZE)) % SCREEN_HEIGHT
        new_position = (new_x, new_y)

        if len(self.positions) > 1:
            self.last = self.positions[-1]
        else:
            self.last = None

        self.positions.insert(0, new_position)

        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self) -> None:
        """Отрисовывает змейку на игровом поле."""
        if self.body_color is None:
            return

        for position in self.positions[:-1]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        if self.positions:
            head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, head_rect)
            pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


def handle_keys(game_object: Snake) -> None:
    """
    Обрабатывает нажатия клавиш для управления змейкой.

    Args:
        game_object: Объект змейки, которым управляет игрок
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main() -> None:
    """Основная функция игры, содержащая главный игровой цикл."""
    pygame.init()

    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)

        handle_keys(snake)

        snake.update_direction()

        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
            while apple.position in snake.positions:
                apple.randomize_position()

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()

        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()

        pygame.display.update()


if __name__ == '__main__':
    main()
