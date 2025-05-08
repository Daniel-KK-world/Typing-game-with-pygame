import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FALL_SPEED = 0.8  # Reasonable speed
SPAWN_RATE = 100  # Frames between new words
MAX_MISSED = 5

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)  # Current input

# Fonts
font = pygame.font.SysFont("Arial", 30)

class FallingWord:
    def __init__(self, text):
        self.text = text
        self.x = random.randint(50, WIDTH - 50)
        self.y = 0
        self.speed = FALL_SPEED
        self.is_active = True
        self.typed_so_far = ""  # Track progress

    def update(self):
        self.y += self.speed
        if self.y > HEIGHT:
            self.is_active = False
            return "missed"  # 🔥 Only counts if it falls off-screen
        return "active"

    def draw(self, screen):
        # Highlight correct/incorrect parts
        correct = font.render(self.text[:len(self.typed_so_far)], True, GREEN)
        remaining = font.render(self.text[len(self.typed_so_far):], True, RED)
        screen.blit(correct, (self.x, self.y))
        screen.blit(remaining, (self.x + correct.get_width(), self.y))

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Falling Words Typing Game")

    word_list = ["python", "game", "typing", "keyboard", "code", "easy", "fun"]
    active_words = []
    current_input = ""
    score = 0
    missed_words = 0
    clock = pygame.time.Clock()
    spawn_timer = 0

    running = True
    while running:
        screen.fill(BLACK)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_BACKSPACE:
                    current_input = current_input[:-1]
                else:
                    current_input += event.unicode.lower()

        # Check for matches in real-time
        for word in active_words[:]:
            if current_input.lower() == word.text:
                score += len(word.text)
                active_words.remove(word)  # 🔥 Remove immediately on success
                current_input = ""
                break

        # Update words and count ONLY truly missed words
        for word in active_words[:]:
            result = word.update()
            if result == "missed":  # 🔥 Only count if it fell
                active_words.remove(word)
                missed_words += 1

        # Track typing progress for all words
        for word in active_words:
            word.typed_so_far = ""
            for i in range(min(len(current_input), len(word.text))):
                if current_input[i] == word.text[i]:
                    word.typed_so_far += current_input[i]
                else:
                    break

        # Spawn new words
        spawn_timer += 1
        if spawn_timer >= SPAWN_RATE:
            active_words.append(FallingWord(random.choice(word_list)))
            spawn_timer = 0

        # Draw everything
        for word in active_words:
            word.draw(screen)

        # UI
        input_surface = font.render(f"Typing: {current_input}", True, BLUE)
        screen.blit(input_surface, (20, HEIGHT - 50))

        score_surface = font.render(f"Score: {score} | Missed: {missed_words}/{MAX_MISSED}", True, WHITE)
        screen.blit(score_surface, (20, 20))

        # Game over check
        if missed_words >= MAX_MISSED:
            game_over_text = font.render("GAME OVER! Press ESC to quit", True, RED)
            screen.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 2))
            pygame.display.flip()
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                        waiting = False
                        running = False
            break

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()