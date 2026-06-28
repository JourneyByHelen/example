import pygame
import random

# 화면 설정
COLS, ROWS = 10, 20
CELL = 30
WIDTH = COLS * CELL + 200
HEIGHT = ROWS * CELL

# 색상
BLACK  = (0, 0, 0)
GRAY   = (40, 40, 40)
WHITE  = (255, 255, 255)

SHAPES = [
    [[1,1,1,1]],                        # I
    [[1,1],[1,1]],                      # O
    [[0,1,0],[1,1,1]],                  # T
    [[1,0],[1,0],[1,1]],                # L
    [[0,1],[0,1],[1,1]],                # J
    [[0,1,1],[1,1,0]],                  # S
    [[1,1,0],[0,1,1]],                  # Z
]

COLORS = [
    (0, 240, 240),   # I - 청록
    (240, 240, 0),   # O - 노랑
    (160, 0, 240),   # T - 보라
    (240, 160, 0),   # L - 주황
    (0, 0, 240),     # J - 파랑
    (0, 240, 0),     # S - 초록
    (240, 0, 0),     # Z - 빨강
]

def rotate(shape):
    return [list(row) for row in zip(*shape[::-1])]

class Tetris:
    def __init__(self):
        self.board = [[0] * COLS for _ in range(ROWS)]
        self.score = 0
        self.level = 1
        self.lines = 0
        self.game_over = False
        self.spawn()

    def spawn(self):
        idx = random.randint(0, len(SHAPES) - 1)
        self.shape = SHAPES[idx]
        self.color = COLORS[idx]
        self.x = COLS // 2 - len(self.shape[0]) // 2
        self.y = 0
        if self.collides(self.shape, self.x, self.y):
            self.game_over = True

    def collides(self, shape, ox, oy):
        for r, row in enumerate(shape):
            for c, cell in enumerate(row):
                if cell:
                    nx, ny = ox + c, oy + r
                    if nx < 0 or nx >= COLS or ny >= ROWS:
                        return True
                    if ny >= 0 and self.board[ny][nx]:
                        return True
        return False

    def lock(self):
        for r, row in enumerate(self.shape):
            for c, cell in enumerate(row):
                if cell:
                    self.board[self.y + r][self.x + c] = self.color
        self.clear_lines()
        self.spawn()

    def clear_lines(self):
        full = [r for r in range(ROWS) if all(self.board[r])]
        for r in full:
            del self.board[r]
            self.board.insert(0, [0] * COLS)
        pts = [0, 100, 300, 500, 800]
        self.score += pts[len(full)] * self.level
        self.lines += len(full)
        self.level = self.lines // 10 + 1

    def move(self, dx, dy):
        if not self.collides(self.shape, self.x + dx, self.y + dy):
            self.x += dx
            self.y += dy
            return True
        return False

    def rotate(self):
        r = rotate(self.shape)
        if not self.collides(r, self.x, self.y):
            self.shape = r

    def hard_drop(self):
        while self.move(0, 1):
            pass
        self.lock()

    def draw(self, screen, font):
        screen.fill(BLACK)

        # 보드 그리드
        for r in range(ROWS):
            for c in range(COLS):
                rect = pygame.Rect(c * CELL, r * CELL, CELL - 1, CELL - 1)
                if self.board[r][c]:
                    pygame.draw.rect(screen, self.board[r][c], rect)
                else:
                    pygame.draw.rect(screen, GRAY, rect, 1)

        # 현재 블록
        for r, row in enumerate(self.shape):
            for c, cell in enumerate(row):
                if cell:
                    rect = pygame.Rect((self.x + c) * CELL, (self.y + r) * CELL, CELL - 1, CELL - 1)
                    pygame.draw.rect(screen, self.color, rect)

        # 고스트 블록
        ghost_y = self.y
        while not self.collides(self.shape, self.x, ghost_y + 1):
            ghost_y += 1
        for r, row in enumerate(self.shape):
            for c, cell in enumerate(row):
                if cell and ghost_y + r != self.y + r:
                    rect = pygame.Rect((self.x + c) * CELL, (ghost_y + r) * CELL, CELL - 1, CELL - 1)
                    pygame.draw.rect(screen, self.color, rect, 2)

        # 사이드 패널
        px = COLS * CELL + 10
        screen.blit(font.render("TETRIS", True, WHITE), (px, 20))
        screen.blit(font.render(f"Score", True, WHITE), (px, 80))
        screen.blit(font.render(f"{self.score}", True, COLORS[3]), (px, 105))
        screen.blit(font.render(f"Level", True, WHITE), (px, 150))
        screen.blit(font.render(f"{self.level}", True, COLORS[2]), (px, 175))
        screen.blit(font.render(f"Lines", True, WHITE), (px, 220))
        screen.blit(font.render(f"{self.lines}", True, COLORS[5]), (px, 245))
        screen.blit(font.render("←→ 이동", True, GRAY), (px, 320))
        screen.blit(font.render("↑  회전", True, GRAY), (px, 345))
        screen.blit(font.render("↓  내리기", True, GRAY), (px, 370))
        screen.blit(font.render("SPC 즉시", True, GRAY), (px, 395))

        if self.game_over:
            ov = font.render("GAME OVER", True, COLORS[6])
            screen.blit(ov, (COLS * CELL // 2 - ov.get_width() // 2, HEIGHT // 2 - 20))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 22, bold=True)

    game = Tetris()
    fall_time = 0

    while True:
        dt = clock.tick(60)
        fall_time += dt

        fall_speed = max(100, 600 - (game.level - 1) * 50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN and not game.game_over:
                if event.key == pygame.K_LEFT:
                    game.move(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    game.move(1, 0)
                elif event.key == pygame.K_DOWN:
                    game.move(0, 1)
                elif event.key == pygame.K_UP:
                    game.rotate()
                elif event.key == pygame.K_SPACE:
                    game.hard_drop()
            if event.type == pygame.KEYDOWN and game.game_over:
                if event.key == pygame.K_r:
                    game = Tetris()

        if not game.game_over and fall_time >= fall_speed:
            if not game.move(0, 1):
                game.lock()
            fall_time = 0

        game.draw(screen, font)
        pygame.display.flip()

if __name__ == "__main__":
    main()
