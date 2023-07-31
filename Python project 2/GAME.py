import pygame

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 15
BALL_RADIUS = 10
WHITE, BLACK, RED, BLUE, GREEN = (255, 255, 255), (0, 0, 0), (255, 0, 0), (0, 0, 255), (0, 255, 0)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Brick Breaker")

# Paddle class
class Paddle:
    def __init__(self):
        self.rect = pygame.Rect(SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2, SCREEN_HEIGHT - 50, PADDLE_WIDTH, PADDLE_HEIGHT)

    def move(self, direction):
        self.rect.x += direction
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

    def draw(self):
        pygame.draw.rect(screen, BLUE, self.rect)

# Ball class
class Ball:
    def __init__(self):
        self.rect = pygame.Rect(SCREEN_WIDTH // 2 - BALL_RADIUS, SCREEN_HEIGHT - 70 - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)
        self.speed_x = 5
        self.speed_y = -5

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.speed_x *= -1

        if self.rect.top <= 0:
            self.speed_y *= -1

    def check_collision(self, paddle):
        if self.rect.colliderect(paddle.rect):
            self.speed_y *= -1

    def hit_brick(self, brick):
        if self.rect.colliderect(brick.rect):
            self.speed_y *= -1
            return True
        return False

    def check_game_over(self):
        return self.rect.bottom >= SCREEN_HEIGHT

    def draw(self):
        pygame.draw.circle(screen, GREEN, self.rect.center, BALL_RADIUS)

# Brick class
class Brick:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)

    def draw(self):
        pygame.draw.rect(screen, RED, self.rect)

# Main function
def main():
    clock = pygame.time.Clock()
    paddle = Paddle()
    ball = Ball()

    bricks = []
    for row in range(3):
        for col in range(10):
            brick = Brick(col * (PADDLE_WIDTH + 5), row * (PADDLE_HEIGHT + 5) + 50)
            bricks.append(brick)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            paddle.move(-5)
        if keys[pygame.K_RIGHT]:
            paddle.move(5)

        ball.move()
        ball.check_collision(paddle)

        for brick in bricks[:]:
            if ball.hit_brick(brick):
                bricks.remove(brick)

        if ball.check_game_over():
            pygame.quit()
            return

        screen.fill(BLACK)
        paddle.draw()
        ball.draw()

        for brick in bricks:
            brick.draw()

        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()
