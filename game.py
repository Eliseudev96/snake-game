import pygame
import random

width = 800
height = 600
grid_size = 20

# Define colors
snake_color = (0, 255, 0)  # Green
food_color = (255, 0, 0)   # Red
background_color = (0, 0, 0)  # Black

class Square:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.velx = 0
        self.vely = 0

    def setVel(self, newx, newy):
        self.velx = newx
        self.vely = newy

    def update(self):
        self.x += self.velx
        self.y += self.vely

class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Snake Game")

        self.snake = [Square(20, 20, snake_color)]
        self.food = Square(
            random.randint(1, (width / grid_size) - 1) * grid_size,
            random.randint(1, (height / grid_size) - 1) * grid_size,
            food_color,
        )

        self.vel = (grid_size, 0)  # Initial velocity
        self.clock = pygame.time.Clock()

    def move(self, x, y):
        self.vel = (x, y)

    def is_collision(self, x1, y1, x2, y2, size):
        return x1 == x2 and y1 == y2

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.move(0, -grid_size)
                elif event.key == pygame.K_DOWN:
                    self.move(0, grid_size)
                elif event.key == pygame.K_RIGHT:
                    self.move(grid_size, 0)
                elif event.key == pygame.K_LEFT:
                    self.move(-grid_size, 0)

    def run(self):
        while True:
            self.handle_events()

            head = self.snake[0]
            new_head = Square(head.x + self.vel[0], head.y + self.vel[1], snake_color)

            # Check for collisions with food
            if self.is_collision(new_head.x, new_head.y, self.food.x, self.food.y, grid_size):
                self.snake.insert(0, new_head)
                self.food = Square(
                    random.randint(1, (width / grid_size) - 1) * grid_size,
                    random.randint(1, (height / grid_size) - 1) * grid_size,
                    food_color,
                )
            else:
                self.snake.insert(0, new_head)
                self.snake.pop()

            # Check for collisions with walls or self
            if (
                new_head.x < 0
                or new_head.x >= width
                or new_head.y < 0
                or new_head.y >= height
                or any(
                    self.is_collision(new_head.x, new_head.y, segment.x, segment.y, grid_size)
                    for segment in self.snake[1:]
                )
            ):
                pygame.quit()
                exit()

            self.window.fill(background_color)
            pygame.draw.rect(self.window, food_color, (self.food.x, self.food.y, grid_size, grid_size))
            for segment in self.snake:
                pygame.draw.rect(self.window, snake_color, (segment.x, segment.y, grid_size, grid_size))
            pygame.display.flip()

            self.clock.tick(10)

if __name__ == "__main__":
    g = Game()
    g.run()
