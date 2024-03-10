import pygame
import random

# 파이게임 초기화
pygame.init()

# 화면 설정
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 8, 8
BLOCK_SIZE = WIDTH // COLS
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("간단한 캔디 크러시")

# 색깔 정의
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)

# 캔디 종류 정의
CANDY_COLORS = [RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE]

# 게임 보드 생성
board = [[random.choice(CANDY_COLORS) for _ in range(COLS)] for _ in range(ROWS)]

# 선택한 블록 위치
selected_block = None

# 블록 이동 애니메이션 관련 변수
falling_blocks = []

# 보드 업데이트 함수
def update_board():
    for col in range(COLS):
        empty_cells = 0
        for row in range(ROWS-1, -1, -1):
            if board[row][col] is None:
                empty_cells += 1
            elif empty_cells > 0:
                board[row + empty_cells][col] = board[row][col]
                board[row][col] = None
                falling_blocks.append({'color': board[row + empty_cells][col], 'row': row + empty_cells, 'col': col, 'y': row * BLOCK_SIZE, 'target_y': (row + empty_cells) * BLOCK_SIZE})
    for col in range(COLS):
        for row in range(ROWS):
            if board[row][col] is None:
                board[row][col] = random.choice(CANDY_COLORS)

# 보드에서 터지는 블록 찾기
def find_matches():
    matches = []
    for row in range(ROWS):
        for col in range(COLS - 2):
            if board[row][col] == board[row][col + 1] == board[row][col + 2] and board[row][col] is not None:
                matches.append((row, col))
                matches.append((row, col + 1))
                matches.append((row, col + 2))
    for col in range(COLS):
        for row in range(ROWS - 2):
            if board[row][col] == board[row + 1][col] == board[row + 2][col] and board[row][col] is not None:
                matches.append((row, col))
                matches.append((row + 1, col))
                matches.append((row + 2, col))
    return matches

# 게임 루프
running = True
while running:
    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            col = mouse_x // BLOCK_SIZE
            row = mouse_y // BLOCK_SIZE
            if selected_block is None:
                selected_block = (row, col)
            else:
                selected_row, selected_col = selected_block
                if abs(row - selected_row) + abs(col - selected_col) == 1:
                    # 선택한 블록의 위치와 이동할 위치에 블록이 터지는지 확인
                    if (row, col) not in find_matches() and (selected_row, selected_col) not in find_matches():
                        board[row][col], board[selected_row][selected_col] = board[selected_row][selected_col], board[row][col]
                    selected_block = None

    # 보드 업데이트
    update_board()

    # 터지는 블록 찾기
    matches = find_matches()

    # 터진 블록 처리
    if matches:
        for row, col in matches:
            board[row][col] = None

    # 화면 지우기
    screen.fill(WHITE)

    # 보드 그리기
    for row in range(ROWS):
        for col in range(COLS):
            color = board[row][col]
            if color is not None:
                rect = pygame.Rect(col * BLOCK_SIZE, row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, (0, 0, 0), rect, 1)

    # 선택한 블록 표시
    if selected_block is not None:
        row, col = selected_block
        pygame.draw.rect(screen, (255, 255, 0), (col * BLOCK_SIZE, row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 4)

    # 블록이 아래로 이동하는 애니메이션 처리
    for block in falling_blocks:
        if block['y'] < block['target_y']:
            block['y'] += 0.5  # 이동 속도 조절
        else:
            falling_blocks.remove(block)
        pygame.draw.rect(screen, block['color'], (block['col'] * BLOCK_SIZE, block['y'], BLOCK_SIZE, BLOCK_SIZE))

    # 화면 업데이트
    pygame.display.flip()

# 게임 종료
pygame.quit()
