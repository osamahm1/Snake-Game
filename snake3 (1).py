import random
import sys
from collections import deque

import pygame

# ---------------------------
# Config
# ---------------------------
CELL_SIZE = 25
GRID_WIDTH = 40
GRID_HEIGHT = 40
FPS = 60
STEPS_PER_FRAME = 8

if GRID_WIDTH % 2 != 0 or GRID_HEIGHT % 2 != 0:
    raise ValueError("GRID_WIDTH and GRID_HEIGHT must be even for guaranteed win.")

WIDTH = GRID_WIDTH * CELL_SIZE
HEIGHT = GRID_HEIGHT * CELL_SIZE

BG_TOP = (19, 29, 48)
BG_BOTTOM = (11, 18, 30)
GRID_COLOR = (44, 62, 87)
HEAD_COLOR = (122, 255, 189)
BODY_COLOR = (76, 227, 156)
TAIL_COLOR = (56, 190, 130)
FOOD_OUTER = (255, 101, 120)
FOOD_INNER = (255, 182, 193)
HUD_BG = (8, 13, 23)
HUD_BORDER = (90, 200, 255)
TEXT_COLOR = (232, 242, 255)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
DIRS = [UP, DOWN, LEFT, RIGHT]


# ---------------------------
# Helpers
# ---------------------------
def random_food_position(snake):
    snake_set = set(snake)
    free_cells = [
        (x, y)
        for y in range(GRID_HEIGHT)
        for x in range(GRID_WIDTH)
        if (x, y) not in snake_set
    ]
    return random.choice(free_cells) if free_cells else None


def in_bounds(pos):
    x, y = pos
    return 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT


def neighbors(pos):
    for dx, dy in DIRS:
        nxt = (pos[0] + dx, pos[1] + dy)
        if in_bounds(nxt):
            yield nxt


def generate_hamiltonian_cycle(width, height):
    """Create a deterministic cycle that visits every cell exactly once."""
    cycle = [(0, 0)]

    for y in range(1, height):
        cycle.append((0, y))

    for x in range(1, width):
        if x % 2 == 1:
            for y in range(height - 1, 0, -1):
                cycle.append((x, y))
        else:
            for y in range(1, height):
                cycle.append((x, y))

    for x in range(width - 1, 0, -1):
        cycle.append((x, 0))

    return cycle


def cycle_distance(a_idx, b_idx, cycle_len):
    if b_idx >= a_idx:
        return b_idx - a_idx
    return cycle_len - a_idx + b_idx


def choose_fast_safe_move(snake, food, cycle, cycle_index):
    """
    Fast strategy with safety guarantees:
    - fallback to Hamiltonian next move (always safe)
    - take shortcut only if it keeps enough room before reaching tail
    """
    head = snake[0]
    tail = snake[-1]

    head_idx = cycle_index[head]
    tail_idx = cycle_index[tail]
    food_idx = cycle_index[food]
    cycle_len = len(cycle)

    default_next = cycle[(head_idx + 1) % cycle_len]
    body = set(snake)
    safe_candidates = []

    for nxt in neighbors(head):
        if nxt in body:
            continue

        nxt_idx = cycle_index[nxt]
        will_grow = nxt == food

        # Keep enough free cycle distance between new head and tail.
        min_gap = len(snake) + (1 if will_grow else 0)
        if cycle_distance(nxt_idx, tail_idx, cycle_len) < min_gap:
            continue

        dist_to_food = cycle_distance(nxt_idx, food_idx, cycle_len)
        tie_break = cycle_distance(nxt_idx, (head_idx + 1) % cycle_len, cycle_len)
        safe_candidates.append((dist_to_food, tie_break, nxt))

    if not safe_candidates:
        return default_next, "Hamiltonian"

    safe_candidates.sort(key=lambda item: (item[0], item[1]))
    best_move = safe_candidates[0][2]
    if best_move == default_next:
        return best_move, "Hamiltonian"
    return best_move, "Shortcut"


def direction_from_to(a, b):
    dx = b[0] - a[0]
    dy = b[1] - a[1]
    return (dx, dy)


def draw_background(surface):
    for y in range(HEIGHT):
        t = y / max(HEIGHT - 1, 1)
        r = int(BG_TOP[0] + (BG_BOTTOM[0] - BG_TOP[0]) * t)
        g = int(BG_TOP[1] + (BG_BOTTOM[1] - BG_TOP[1]) * t)
        b = int(BG_TOP[2] + (BG_BOTTOM[2] - BG_TOP[2]) * t)
        pygame.draw.line(surface, (r, g, b), (0, y), (WIDTH, y))


def draw_grid(surface):
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(surface, GRID_COLOR, (x, 0), (x, HEIGHT), 1)
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(surface, GRID_COLOR, (0, y), (WIDTH, y), 1)


def cell_rect(cell):
    return pygame.Rect(cell[0] * CELL_SIZE, cell[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)


def draw_food(surface, food):
    rect = cell_rect(food)
    center = rect.center
    outer_r = CELL_SIZE // 2 - 2
    inner_r = max(2, outer_r // 2)
    pygame.draw.circle(surface, FOOD_OUTER, center, outer_r)
    pygame.draw.circle(surface, FOOD_INNER, center, inner_r)


def draw_snake(surface, snake):
    if not snake:
        return

    for i, part in enumerate(snake):
        rect = cell_rect(part).inflate(-2, -2)
        center = rect.center
        radius = max(5, rect.width // 2 - 1)

        # Rounded segment body with subtle shading to look less blocky.
        if i == 0:
            base_color = (99, 222, 140)
        elif i == len(snake) - 1:
            base_color = (63, 150, 95)
        else:
            fade = min(45, i)
            base_color = (max(45, BODY_COLOR[0] - fade), max(120, BODY_COLOR[1] - fade), max(70, BODY_COLOR[2] - fade // 2))

        pygame.draw.circle(surface, base_color, center, radius)
        pygame.draw.circle(surface, (18, 55, 30), center, radius, width=1)

        # Soft highlight gives a more organic "skin" feel.
        highlight = (center[0] - radius // 3, center[1] - radius // 3)
        pygame.draw.circle(surface, (145, 255, 190), highlight, max(2, radius // 4))

    if len(snake) >= 2:
        head = snake[0]
        neck = snake[1]
        facing = direction_from_to(neck, head)
    else:
        facing = RIGHT

    hx = snake[0][0] * CELL_SIZE
    hy = snake[0][1] * CELL_SIZE
    eye_r = max(2, CELL_SIZE // 7)
    pupil_r = max(1, eye_r // 2)
    head_center = (hx + CELL_SIZE // 2, hy + CELL_SIZE // 2)

    # Stronger head shape to separate head from body.
    pygame.draw.circle(surface, HEAD_COLOR, head_center, CELL_SIZE // 2 - 2)
    pygame.draw.circle(surface, (30, 90, 55), head_center, CELL_SIZE // 2 - 2, width=1)

    if facing == UP:
        eyes = [(hx + CELL_SIZE // 3, hy + CELL_SIZE // 3), (hx + 2 * CELL_SIZE // 3, hy + CELL_SIZE // 3)]
    elif facing == DOWN:
        eyes = [(hx + CELL_SIZE // 3, hy + 2 * CELL_SIZE // 3), (hx + 2 * CELL_SIZE // 3, hy + 2 * CELL_SIZE // 3)]
    elif facing == LEFT:
        eyes = [(hx + CELL_SIZE // 3, hy + CELL_SIZE // 3), (hx + CELL_SIZE // 3, hy + 2 * CELL_SIZE // 3)]
    else:
        eyes = [(hx + 2 * CELL_SIZE // 3, hy + CELL_SIZE // 3), (hx + 2 * CELL_SIZE // 3, hy + 2 * CELL_SIZE // 3)]

    for eye in eyes:
        pygame.draw.circle(surface, (255, 255, 255), eye, eye_r)
        pygame.draw.circle(surface, (0, 0, 0), eye, pupil_r)

    # Small nose dot for a more expressive head.
    if facing == UP:
        nose = (hx + CELL_SIZE // 2, hy + CELL_SIZE // 5)
    elif facing == DOWN:
        nose = (hx + CELL_SIZE // 2, hy + 4 * CELL_SIZE // 5)
    elif facing == LEFT:
        nose = (hx + CELL_SIZE // 5, hy + CELL_SIZE // 2)
    else:
        nose = (hx + 4 * CELL_SIZE // 5, hy + CELL_SIZE // 2)
    pygame.draw.circle(surface, (32, 20, 20), nose, max(1, CELL_SIZE // 12))


def draw_hud(surface, score, snake_len, mode, won, font, small_font):
    panel = pygame.Rect(12, 12, 270, 94)
    pygame.draw.rect(surface, HUD_BG, panel, border_radius=12)
    pygame.draw.rect(surface, HUD_BORDER, panel, width=2, border_radius=12)

    title = font.render("Perfect Snake AI", True, TEXT_COLOR)
    stat = small_font.render(f"Score: {score}   Length: {snake_len}/{GRID_WIDTH * GRID_HEIGHT}", True, TEXT_COLOR)
    state_text = "Status: Victory" if won else f"Status: {mode}"
    state = small_font.render(state_text, True, (160, 255, 190) if won else (170, 220, 255))

    surface.blit(title, (24, 20))
    surface.blit(stat, (24, 54))
    surface.blit(state, (24, 78))


# ---------------------------
# Game
# ---------------------------
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Perfect Snake: 50x50 Grid")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("segoeui", 28, bold=True)
    small_font = pygame.font.SysFont("segoeui", 18)

    cycle = generate_hamiltonian_cycle(GRID_WIDTH, GRID_HEIGHT)
    cycle_index = {pos: i for i, pos in enumerate(cycle)}
    board_surface = pygame.Surface((WIDTH, HEIGHT))
    draw_background(board_surface)
    draw_grid(board_surface)

    snake = deque([cycle[0]])
    food = random_food_position(snake)
    score = 0
    mode = "Hamiltonian"
    won = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                snake = deque([cycle[0]])
                food = random_food_position(snake)
                score = 0
                won = False
                mode = "Hamiltonian"

        if food is not None and not won:
            for _ in range(STEPS_PER_FRAME):
                if food is None or won:
                    break

                next_head, mode = choose_fast_safe_move(snake, food, cycle, cycle_index)
                will_grow = next_head == food
                body_to_check = set(snake)

                if next_head in body_to_check:
                    # Safety fallback: move strictly along cycle.
                    head = snake[0]
                    next_head = cycle[(cycle_index[head] + 1) % len(cycle)]
                    will_grow = next_head == food

                snake.appendleft(next_head)
                if will_grow:
                    score += 1
                    food = random_food_position(snake)
                    if food is None:
                        won = True
                        mode = "Board fully filled"
                else:
                    snake.pop()

        screen.blit(board_surface, (0, 0))

        if food is not None:
            draw_food(screen, food)
        draw_snake(screen, snake)
        draw_hud(screen, score, len(snake), mode, won, font, small_font)

        if won:
            msg = font.render("Flawless Win! Press R to restart", True, (174, 255, 196))
            box = msg.get_rect(center=(WIDTH // 2, HEIGHT - 24))
            screen.blit(msg, box)

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()