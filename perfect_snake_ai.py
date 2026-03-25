# import random
# import sys
# from collections import deque

# import pygame

# # ---------------------------
# # Configuration
# # ---------------------------
# CELL_SIZE = 25
# GRID_WIDTH = 30
# GRID_HEIGHT = 20
# FPS = 15000  # Extremely fast so you don't have to wait to see it win

# if GRID_WIDTH % 2 != 0 or GRID_HEIGHT % 2 != 0:
#     raise ValueError("Grid width and height must be even numbers.")

# WIDTH = GRID_WIDTH * CELL_SIZE
# HEIGHT = GRID_HEIGHT * CELL_SIZE

# BG_COLOR = (18, 18, 18)
# GRID_COLOR = (35, 35, 35)
# SNAKE_HEAD_COLOR = (255, 200, 40)
# SNAKE_BODY_COLOR = (200, 150, 20)
# FOOD_COLOR = (220, 60, 60)
# TEXT_COLOR = (240, 240, 240)
# SNAKE_TAIL_COLOR = (40, 100, 255)

# UP = (0, -1)
# DOWN = (0, 1)
# LEFT = (-1, 0)
# RIGHT = (1, 0)
# DIRS = [UP, DOWN, LEFT, RIGHT]

# # ---------------------------
# # Helpers
# # ---------------------------
# def add_pos(a, b):
#     return a[0] + b[0], a[1] + b[1]

# def in_bounds(pos):
#     x, y = pos
#     return 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT

# def get_neighbors(pos):
#     for d in DIRS:
#         nxt = add_pos(pos, d)
#         if in_bounds(nxt):
#             yield nxt

# def random_food_position(snake):
#     snake_set = set(snake)
#     free_cells = [
#         (x, y) for y in range(GRID_HEIGHT) for x in range(GRID_WIDTH)
#         if (x, y) not in snake_set
#     ]
#     return random.choice(free_cells) if free_cells else None

# def draw_cell(surface, color, pos):
#     x, y = pos
#     rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
#     pygame.draw.rect(surface, color, rect)

# def draw_grid(surface):
#     for x in range(0, WIDTH, CELL_SIZE):
#         pygame.draw.line(surface, GRID_COLOR, (x, 0), (x, HEIGHT))
#     for y in range(0, HEIGHT, CELL_SIZE):
#         pygame.draw.line(surface, GRID_COLOR, (0, y), (WIDTH, y))

# def draw_text(surface, text, font, x, y, color=TEXT_COLOR):
#     img = font.render(text, True, color)
#     surface.blit(img, (x, y))

# # ---------------------------
# # Hamiltonian Cycle Generation
# # ---------------------------
# def generate_hamiltonian_cycle(width, height):
#     """Generates a perfect zig-zag path covering the entire grid."""
#     cycle = []
#     for x in range(width):
#         cycle.append((x, 0))

#     for x in range(width - 1, -1, -1):
#         if (width - 1 - x) % 2 == 0:
#             for y in range(1, height):
#                 cycle.append((x, y))
#         else:
#             for y in range(height - 1, 0, -1):
#                 cycle.append((x, y))
#     return cycle

# # ---------------------------
# # The Flawless Hybrid AI
# # ---------------------------
# def get_perfect_move(snake, food, cycle_idx):
#     area = GRID_WIDTH * GRID_HEIGHT
#     head = snake[0]
#     tail = snake[-1]
    
#     h_idx = cycle_idx[head]
#     f_idx = cycle_idx[food]
#     t_idx = cycle_idx[tail]

#     # Calculate 1D distance along the Hamiltonian track
#     def dist(a, b):
#         if a == b: return area
#         return (b - a + area) % area

#     dist_food = dist(h_idx, f_idx)
#     dist_tail = dist(h_idx, t_idx)

#     # 1. The default, absolutely safe move (just follow the track)
#     default_move = None
#     for nxt in get_neighbors(head):
#         if cycle_idx[nxt] == (h_idx + 1) % area:
#             default_move = nxt
#             break

#     best_move = default_move
#     mode = "Safe Track"
#     max_leap = 0

#     # 2. Late Game: If the snake is massive, stop risking shortcuts. 
#     # Just ride the track to inevitable victory.
#     if len(snake) > area * 0.85:
#         return default_move, "Victory Lap (Strict)"

#     # 3. Look for safe mathematical shortcuts
#     for nxt in get_neighbors(head):
#         if nxt == default_move:
#             continue
            
#         n_idx = cycle_idx[nxt]
#         leap = dist(h_idx, n_idx)

#         # Rules for a flawless shortcut:
#         # A. We must leap forward (handled by math)
#         # B. We must not leap past the food
#         # C. We must strictly leave room before the tail
#         if leap <= dist_food and leap < dist_tail:
#             # D. Ensure we aren't jumping onto our own body
#             if nxt not in snake:
#                 # Pick the shortcut that skips the most useless track
#                 if leap > max_leap:
#                     max_leap = leap
#                     best_move = nxt
#                     mode = "Shortcut (Fast)"

#     return best_move, mode

# # ---------------------------
# # Main Game Loop
# # ---------------------------
# def main():
#     pygame.init()
#     screen = pygame.display.set_mode((WIDTH, HEIGHT))
#     pygame.display.set_caption("The Flawless Snake AI")
#     clock = pygame.time.Clock()
#     font = pygame.font.SysFont(None, 28)

#     # Precompute the perfect path
#     cycle = generate_hamiltonian_cycle(GRID_WIDTH, GRID_HEIGHT)
#     cycle_idx = {pos: i for i, pos in enumerate(cycle)}

#     snake = deque([cycle[0]])
#     food = random_food_position(snake)
#     score = 0
#     game_over = False
#     mode = ""

#     while True:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()

#         if not game_over and food is not None:
#             new_head, mode = get_perfect_move(snake, food, cycle_idx)

#             will_grow = (new_head == food)
#             snake.appendleft(new_head)

#             if will_grow:
#                 score += 1
#                 food = random_food_position(snake)
#                 if food is None:
#                     game_over = True
#                     mode = "Perfect Score!"
#             else:
#                 snake.pop()

#         # Render
#         screen.fill(BG_COLOR)
#         draw_grid(screen)

#         if food is not None:
#             draw_cell(screen, FOOD_COLOR, food)

#         for i, segment in enumerate(snake):
#             if i == 0:
#                 color = SNAKE_HEAD_COLOR  
#             elif i == len(snake) - 1 and len(snake) > 1:
#                 color = SNAKE_TAIL_COLOR  
#             else:
#                 color = SNAKE_BODY_COLOR  
                
#             draw_cell(screen, color, segment)

#         draw_text(screen, f"Score: {score} / {GRID_WIDTH * GRID_HEIGHT}", font, 10, 10)
        
#         m_color = (100, 255, 100) if "Shortcut" in mode else (255, 150, 50)
#         if "Victory" in mode: m_color = (50, 200, 255)
        
#         draw_text(screen, f"AI State: {mode}", font, 10, 40, m_color)

#         if game_over:
#             draw_text(screen, "FLAWLESS VICTORY!", font, 10, 100, (100, 255, 100))

#         pygame.display.flip()
#         clock.tick(FPS)

# if __name__ == "__main__":
#     main()

import random
import sys
from collections import deque

import pygame

# ---------------------------
# Configuration & Modern UI Palette
# ---------------------------
CELL_SIZE = 25
GRID_WIDTH = 30
GRID_HEIGHT = 20
FPS = 15000000  # Extremely fast so you don't have to wait to see it win

if GRID_WIDTH % 2 != 0 or GRID_HEIGHT % 2 != 0:
    raise ValueError("Grid width and height must be even numbers.")

WIDTH = GRID_WIDTH * CELL_SIZE
HEIGHT = GRID_HEIGHT * CELL_SIZE

# Modern Colors
BG_COLOR_1 = (24, 24, 28)
BG_COLOR_2 = (30, 30, 36)
SNAKE_HEAD_COLOR = (0, 255, 170)  # Neon Green/Cyan
SNAKE_BODY_COLOR = (0, 200, 130)
SNAKE_TAIL_COLOR = (0, 150, 200)
FOOD_COLOR = (255, 60, 80)       # Bright Neon Red/Pink
FOOD_GLOW_COLOR = (150, 30, 40)
TEXT_COLOR = (255, 255, 255)
TEXT_SHADOW_COLOR = (0, 0, 0)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
DIRS = [UP, DOWN, LEFT, RIGHT]

# ---------------------------
# Helpers
# ---------------------------
def add_pos(a, b):
    return a[0] + b[0], a[1] + b[1]

def in_bounds(pos):
    x, y = pos
    return 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT

def get_neighbors(pos):
    for d in DIRS:
        nxt = add_pos(pos, d)
        if in_bounds(nxt):
            yield nxt

def random_food_position(snake):
    snake_set = set(snake)
    free_cells = [
        (x, y) for y in range(GRID_HEIGHT) for x in range(GRID_WIDTH)
        if (x, y) not in snake_set
    ]
    return random.choice(free_cells) if free_cells else None

# ---------------------------
# New UI Drawing Functions
# ---------------------------
def draw_checkered_background(surface):
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            color = BG_COLOR_1 if (x + y) % 2 == 0 else BG_COLOR_2
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(surface, color, rect)

def draw_snake_segment(surface, color, pos, is_head=False):
    x, y = pos
    # Add padding to make the snake look slightly detached from the grid edges
    padding = 1 if is_head else 2
    rect = pygame.Rect(x * CELL_SIZE + padding, y * CELL_SIZE + padding, 
                       CELL_SIZE - padding*2, CELL_SIZE - padding*2)
    # Rounded corners for a modern look
    radius = 8 if is_head else 5
    pygame.draw.rect(surface, color, rect, border_radius=radius)

def draw_food(surface, pos):
    x, y = pos
    center = (int(x * CELL_SIZE + CELL_SIZE / 2), int(y * CELL_SIZE + CELL_SIZE / 2))
    radius = int(CELL_SIZE / 2) - 3
    
    # Draw Glow
    pygame.draw.circle(surface, FOOD_GLOW_COLOR, center, radius + 3)
    # Draw Core
    pygame.draw.circle(surface, FOOD_COLOR, center, radius)

def draw_text_with_shadow(surface, text, font, x, y, color=TEXT_COLOR):
    # Shadow
    shadow_img = font.render(text, True, TEXT_SHADOW_COLOR)
    surface.blit(shadow_img, (x + 2, y + 2))
    # Main Text
    img = font.render(text, True, color)
    surface.blit(img, (x, y))

# ---------------------------
# Hamiltonian Cycle Generation
# ---------------------------
def generate_hamiltonian_cycle(width, height):
    """Generates a perfect zig-zag path covering the entire grid."""
    cycle = []
    for x in range(width):
        cycle.append((x, 0))

    for x in range(width - 1, -1, -1):
        if (width - 1 - x) % 2 == 0:
            for y in range(1, height):
                cycle.append((x, y))
        else:
            for y in range(height - 1, 0, -1):
                cycle.append((x, y))
    return cycle

# ---------------------------
# The Flawless Hybrid AI
# ---------------------------
def get_perfect_move(snake, food, cycle_idx):
    area = GRID_WIDTH * GRID_HEIGHT
    head = snake[0]
    tail = snake[-1]
    
    h_idx = cycle_idx[head]
    f_idx = cycle_idx[food]
    t_idx = cycle_idx[tail]

    def dist(a, b):
        if a == b: return area
        return (b - a + area) % area

    dist_food = dist(h_idx, f_idx)
    dist_tail = dist(h_idx, t_idx)

    default_move = None
    for nxt in get_neighbors(head):
        if cycle_idx[nxt] == (h_idx + 1) % area:
            default_move = nxt
            break

    best_move = default_move
    mode = "Safe Track"
    max_leap = 0

    if len(snake) > area * 0.85:
        return default_move, "Victory Lap (Strict)"

    for nxt in get_neighbors(head):
        if nxt == default_move:
            continue
            
        n_idx = cycle_idx[nxt]
        leap = dist(h_idx, n_idx)

        if leap <= dist_food and leap < dist_tail:
            if nxt not in snake:
                if leap > max_leap:
                    max_leap = leap
                    best_move = nxt
                    mode = "Shortcut (Fast)"

    return best_move, mode

# ---------------------------
# Main Game Loop
# ---------------------------
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("The Flawless Snake AI")
    clock = pygame.time.Clock()
    
    # Better Font styling
    font = pygame.font.SysFont('Segoe UI, Arial', 26, bold=True)
    large_font = pygame.font.SysFont('Segoe UI, Arial', 48, bold=True)

    cycle = generate_hamiltonian_cycle(GRID_WIDTH, GRID_HEIGHT)
    cycle_idx = {pos: i for i, pos in enumerate(cycle)}

    snake = deque([cycle[0]])
    food = random_food_position(snake)
    score = 0
    game_over = False
    mode = ""

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if not game_over and food is not None:
            new_head, mode = get_perfect_move(snake, food, cycle_idx)

            will_grow = (new_head == food)
            snake.appendleft(new_head)

            if will_grow:
                score += 1
                food = random_food_position(snake)
                if food is None:
                    game_over = True
                    mode = "Perfect Score!"
            else:
                snake.pop()

        # 1. Draw Checkered Background
        draw_checkered_background(screen)

        # 2. Draw Food
        if food is not None:
            draw_food(screen, food)

        # 3. Draw Snake
        for i, segment in enumerate(snake):
            is_head = (i == 0)
            if is_head:
                color = SNAKE_HEAD_COLOR  
            elif i == len(snake) - 1 and len(snake) > 1:
                color = SNAKE_TAIL_COLOR  
            else:
                # Slight gradient/variation for the body could be added here
                color = SNAKE_BODY_COLOR  
                
            draw_snake_segment(screen, color, segment, is_head)

        # 4. Draw UI Texts
        draw_text_with_shadow(screen, f"Score: {score} / {GRID_WIDTH * GRID_HEIGHT}", font, 15, 10)
        
        m_color = (100, 255, 150) if "Shortcut" in mode else (255, 200, 50)
        if "Victory" in mode: m_color = (50, 200, 255)
        
        draw_text_with_shadow(screen, f"AI State: {mode}", font, 15, 40, m_color)

        if game_over:
            # Semi-transparent overlay for Game Over
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(150)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))
            
            text = "FLAWLESS VICTORY!"
            text_rect = large_font.render(text, True, (255, 255, 255)).get_rect(center=(WIDTH/2, HEIGHT/2))
            draw_text_with_shadow(screen, text, large_font, text_rect.x, text_rect.y, SNAKE_HEAD_COLOR)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()