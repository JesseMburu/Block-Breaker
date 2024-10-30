import sys
import pygame

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BALL_COLOR = (200, 50, 50)
BLOCK_COLOR = (100, 100, 255)
PADDLE_COLOR = (0, 255, 0)

# Ball properties
BALL_RADIUS = 10
ball_x, ball_y = WIDTH // 2, HEIGHT // 2  # Starting position of the ball at screen center
ball_dx, ball_dy = 4, -4  # Initial velocity of the ball in x and y directions
ball_speed_increment = 2.5  # Increment for ball speed per block-hit threshold
ball_speed = 12

# Paddle properties
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 10
paddle_x = WIDTH // 2 - PADDLE_WIDTH // 2  # Starting x position of the paddle
paddle_y = HEIGHT - 40  # y position of the paddle (near the bottom)
paddle_speed = 15  # Speed of paddle movement

# Block properties
BLOCK_WIDTH = 30
BLOCK_HEIGHT = 25  
BLOCK_ROWS = 5  # Number of rows of blocks
BLOCK_COLS = 19  # Number of columns of blocks
blocks = []  # List to store block positions

# Score and game state
score = 0  # Initialize the score
blocks_hit_to_increase_speed = 3  # Ball speed increase threshold (every 3 blocks hit)
game_over = False  # Track if the game is over

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Set up game window
pygame.display.set_caption("Brick Breaker with Block Collision")  # Set window caption

# Font
font = pygame.font.Font(None, 36)  # Font setup for displaying text

# Initialize blocks
def create_blocks():
    """Creates the blocks and adds them to the 'blocks' list."""
    global blocks
    blocks = []
    for row in range(BLOCK_ROWS):  # Loop through rows
        for col in range(BLOCK_COLS):  # Loop through columns
            block_x = col * (BLOCK_WIDTH + 10) + 35  # Calculate x position of the block
            block_y = row * (BLOCK_HEIGHT + 10) + 50  # Calculate y position of the block
            blocks.append(pygame.Rect(block_x, block_y, BLOCK_WIDTH, BLOCK_HEIGHT))  # Add block to list

# Reset game state
def reset_game():
    """Resets the game to its initial state."""
    global ball_x, ball_y, ball_dx, ball_dy, paddle_x, score, game_over, blocks
    ball_x, ball_y = WIDTH // 2, HEIGHT // 2  # Reset ball position to center
    ball_dx, ball_dy = 4, -4  # Reset ball velocity
    paddle_x = WIDTH // 2 - PADDLE_WIDTH // 2  # Reset paddle position to center-bottom
    score = 0  # Reset score
    game_over = False  # Reset game over state
    create_blocks()  # Recreate blocks

# Initialize the blocks for the first time
create_blocks()

# Main game loop
while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Check for quit event
            pygame.quit()  # Quit pygame
            sys.exit()  # Exit the program

    # Get key states
    keys = pygame.key.get_pressed()

    if not game_over:
        # Paddle movement
        if keys[pygame.K_LEFT] and paddle_x > 0:  # Move left if left key pressed and paddle not at left edge
            paddle_x -= paddle_speed
        if keys[pygame.K_RIGHT] and paddle_x < WIDTH - PADDLE_WIDTH:  # Move right if right key pressed and paddle not at right edge
            paddle_x += paddle_speed

        # Ball movement
        ball_x += ball_dx  # Update ball's x position by its x velocity
        ball_y += ball_dy  # Update ball's y position by its y velocity

        # Ball collision with walls
        if ball_x - BALL_RADIUS <= 0 or ball_x + BALL_RADIUS >= WIDTH:  # Check for collision with left/right walls
            ball_dx = -ball_dx  # Reverse x direction on collision
        if ball_y - BALL_RADIUS <= 0:  # Check for collision with top wall
            ball_dy = -ball_dy  # Reverse y direction on collision

        # Ball collision with paddle
        paddle_rect = pygame.Rect(paddle_x, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT)  # Create paddle rectangle for collision detection
        if paddle_rect.collidepoint(ball_x, ball_y + BALL_RADIUS):  # Check if ball hits the paddle
            ball_dy = -ball_dy  # Reverse y direction on collision

        # Ball collision with blocks
        for block in blocks[:]:  # Loop through blocks
            if block.collidepoint(ball_x, ball_y):  # Check if ball hits a block
                if abs(ball_y - block.top) < BALL_RADIUS or abs(ball_y - block.bottom) < BALL_RADIUS:
                    ball_dy = -ball_dy  # Reverse vertical direction if hitting top/bottom
                elif abs(ball_x - block.left) < BALL_RADIUS or abs(ball_x - block.right) < BALL_RADIUS:
                    ball_dx = -ball_dx  # Reverse horizontal direction if hitting left/right

                blocks.remove(block)  # Remove block on collision
                score += 1  # Increase score

                # Increase ball speed after hitting a certain number of blocks
                if score % blocks_hit_to_increase_speed == 0:  # Check if speed increase threshold met
                    ball_dx *= 1.1 if ball_dx > 0 else -1.1  # Increase ball's x speed
                    ball_dy *= 1.1 if ball_dy > 0 else -1.1  # Increase ball's y speed
                break

        # Ball falls to the bottom - game over
        if ball_y + BALL_RADIUS >= HEIGHT:
            game_over = True  # Set game over state

    # Clear the screen
    screen.fill(BLACK)  # Fill screen with black

    # Draw blocks
    for block in blocks:  # Draw each block
        pygame.draw.rect(screen, BLOCK_COLOR, block)

    # Draw paddle
    paddle_rect = pygame.Rect(paddle_x, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT)
    pygame.draw.rect(screen, PADDLE_COLOR, paddle_rect)  # Draw paddle rectangle

    # Draw ball
    pygame.draw.circle(screen, BALL_COLOR, (ball_x, ball_y), BALL_RADIUS)  # Draw ball as a circle

    # Display score or game over message
    if game_over:
        game_over_text = font.render("Game Over! Press R to Restart", True, WHITE)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2))
        final_score_text = font.render(f'Final Score: {score}', True, WHITE)
        screen.blit(final_score_text, (WIDTH // 2 - final_score_text.get_width() // 2, HEIGHT // 2 + 40))

        # Restart game on pressing 'R'
        if keys[pygame.K_r]:
            reset_game()
    else:
        score_text = font.render(f"Score: {score}", True, WHITE)  # Render score text
        screen.blit(score_text, (10, 10))  # Display score on screen

    # Check for game over (all blocks destroyed)
    if not blocks and not game_over:  # If all blocks are destroyed
        win_text = font.render("You Win! Press R to Restart", True, WHITE)  # Render win text
        screen.blit(win_text, (WIDTH // 2 - 150, HEIGHT // 2))  # Display win text
        if keys[pygame.K_r]:  # Restart game if "R" key pressed
            reset_game()

    # Update display
    pygame.display.flip()  # Refresh the screen

    # Frame rate
    pygame.time.Clock().tick(60)  # Set the frame rate to 60 FPS
