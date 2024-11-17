import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
LINE_Y = 500  # Line where notes should be hit
MAX_MISSES = 10  # Maximum number of misses before game over

# Setup screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Rhythm Game")

# Game clock
clock = pygame.time.Clock()

# Define a Note class
class Note:
    def __init__(self, x, y, color, key):
        self.x = x
        self.y = y
        self.color = color
        self.key = key  # The key to press (e.g., 'a', 's', 'd', etc.)

    def update(self):
        self.y += 5  # Speed of falling notes

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), 20)

# Define the Player class (character as a square)
class Player:
    def __init__(self):
        self.x = SCREEN_WIDTH // 2 - 25  # Starting position in the middle
        self.y = SCREEN_HEIGHT - 50  # Place it near the bottom
        self.width = 50  # Width of the square
        self.height = 50  # Height of the square
        self.color = (0, 0, 255)  # Blue color for the player

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

# Function to generate random notes
def generate_notes():
    notes = []
    note_keys = ['a', 's', 'd', 'f']  # keys the player will press
    note_x_positions = [200, 300, 400, 500]  # X positions for notes

    for _ in range(10):  # Generate 10 notes for now
        note_key = random.choice(note_keys)
        note_x = random.choice(note_x_positions)
        note = Note(note_x, 0, random.choice([RED, GREEN]), note_key)
        notes.append(note)
    
    return notes

# Function to handle the Quit button click
def quit_button_click(pos):
    quit_button_rect = pygame.Rect(SCREEN_WIDTH // 3, SCREEN_HEIGHT // 1.5, 200, 50)  # Button rect
    return quit_button_rect.collidepoint(pos)

# Main game loop
def game_loop():
    running = True
    score = 0
    misses = 0
    player = Player()
    notes = generate_notes()

    while running:
        screen.fill(WHITE)
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                player_input = None
                if event.key == pygame.K_a:
                    player_input = 'a'
                elif event.key == pygame.K_s:
                    player_input = 's'
                elif event.key == pygame.K_d:
                    player_input = 'd'
                elif event.key == pygame.K_f:
                    player_input = 'f'

                # Check if the player pressed the correct key at the right time
                for note in notes[:]:  # Iterate over a copy of notes list to modify during loop
                    if note.y >= LINE_Y - 20 and note.y <= LINE_Y + 20:
                        if note.key == player_input:
                            score += 1
                            notes.remove(note)  # Remove the note once caught

        # Update and draw notes
        for note in notes[:]:  # Iterate over a copy of notes list to modify during loop
            note.update()
            note.draw()

            # If a note has passed the line, it's a miss
            if note.y >= LINE_Y + 20:  # If the note is below the line
                misses += 1
                notes.remove(note)

        # Check if the number of misses exceeds the max allowed
        if misses >= MAX_MISSES:
            running = False

        # Draw the line where the notes should be hit
        pygame.draw.line(screen, BLACK, (0, LINE_Y), (SCREEN_WIDTH, LINE_Y), 5)

        # Display the score and miss count
        font = pygame.font.SysFont("Arial", 30)
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        miss_text = font.render(f"Misses: {misses}/{MAX_MISSES}", True, BLACK)
        screen.blit(miss_text, (SCREEN_WIDTH - 150, 10))

        # Draw the player character (the square)
        player.draw()

        # Game over check
        if misses >= MAX_MISSES:
            game_over_font = pygame.font.SysFont("Arial", 50)
            game_over_text = game_over_font.render("Game Over!", True, RED)
            screen.blit(game_over_text, (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 3))

            restart_text = font.render("Press Enter to Restart", True, BLACK)
            screen.blit(restart_text, (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2))

            # Draw the quit button
            quit_button_rect = pygame.Rect(SCREEN_WIDTH // 3, SCREEN_HEIGHT // 1.5, 200, 50)
            pygame.draw.rect(screen, BLACK, quit_button_rect)
            quit_text = font.render("Quit", True, WHITE)
            screen.blit(quit_text, (SCREEN_WIDTH // 2 - 40, SCREEN_HEIGHT // 1.5 + 10))

            pygame.display.update()

            # Wait for player input to restart or quit
            waiting_for_input = True
            while waiting_for_input:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        waiting_for_input = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:  # Enter key pressed
                            game_loop()  # Restart the game
                            waiting_for_input = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if quit_button_click(event.pos):  # If Quit button clicked
                            running = False
                            waiting_for_input = False

            break  # Exit the game loop after restart or quit

        # Update the screen
        pygame.display.update()
        
        # Cap the frame rate
        clock.tick(60)

# Run the game
if __name__ == "__main__":
    game_loop()
    pygame.quit()
