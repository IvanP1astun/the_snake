from random import choice, randint

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
BORDER_COLOR = (0, 255, 255)

# Цвет яблока
APPLE_COLOR = (124, 252, 0)

# Цвет змейки
SNAKE_COLOR = (255, 215, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()

class GameObject:
    def __init__(self) -> None:
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = None

    def draw(self):
        pass

class Apple(GameObject):
    def __init__(self):
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position()

    def randomize_position(self):
        self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                        randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    def draw(self):
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

class Snake(GameObject):
    def __init__(self):
        super().__init__()
        self.positions = [(GRID_SIZE * 5, GRID_SIZE * 5)]
        self.direction = RIGHT
        self.grow = False
        self.color = BORDER_COLOR
        self.body_color = SNAKE_COLOR
        self.last = None

    def get_head_position(self):
        return self.positions[0]

    def reset(self):
        self.positions = [(GRID_SIZE * 5, GRID_SIZE * 5)]
        self.direction = RIGHT
        self.grow = False

    def move(self):
        new_head = (self.positions[0][0] + self.direction[0] * GRID_SIZE,
                     self.positions[0][1] + self.direction[1] * GRID_SIZE)
        self.positions.insert(0, new_head)
        if not self.grow:
            self.positions.pop()
        else:
            self.grow = False

    def eat(self):
        self.grow = True

    def update_direction(self, new_direction):
        if (new_direction == UP and self.direction != DOWN) or \
            (new_direction == DOWN and self.direction != UP) or \
            (new_direction == LEFT and self.direction != RIGHT) or \
            (new_direction == RIGHT and self.direction != LEFT):
            self.direction = new_direction

def handle_keys(game_object):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.direction = RIGHT

def main():
    snake = Snake()
    apple = Apple()
    running = True
    game_over = False 

    while running:
        if not game_over:
            handle_keys(snake)
            snake.move()

            if snake.get_head_position() == apple.position:
                snake.eat()
                apple.randomize_position()

            if (snake.get_head_position()[0] < 0 or
                snake.get_head_position()[0] >= SCREEN_WIDTH or
                snake.get_head_position()[1] < 0 or
                snake.get_head_position() in snake.positions[1:]):
                game_over = True 

            screen.fill(BOARD_BACKGROUND_COLOR)  # Очистка экрана черным цветом

        # Отрисовка змейки
        for pos in snake.positions:
            rect = pygame.Rect(pos, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, snake.body_color, rect)
            pygame.draw.rect(screen, snake.color, rect, 1)

        # Отрисовка яблока
        apple.draw()

        # Обновление экрана
        pygame.display.flip()

        # Ограничение кадров в секунду
        clock.tick(SPEED)

        if game_over:
            font = pygame.font.Font(None, 74)
            text = font.render("Game Over", True, (255, 0, 0))
            screen.blit(text, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 3))
            pygame.display.flip()
            pygame.time.wait(2000)
            running = False

if __name__ == "__main__":
    pygame.init()
    main()
    pygame.quit()