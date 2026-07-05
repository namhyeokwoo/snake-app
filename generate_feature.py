from PIL import Image, ImageDraw
import os

W, H = 1024, 500

BG          = (38, 36, 31)
GREEN_BOARD = (169, 192, 136)
SNAKE_BODY  = (76, 175, 80)
SNAKE_HEAD  = (165, 214, 167)
FOOD        = (255, 82, 82)
AMBER       = (255, 185, 0)
CREAM       = (243, 239, 227)
HEART_EMPTY = (80, 78, 73)

# 5×7 픽셀 폰트 (대문자)
GLYPHS = {
  'A': ["01110","10001","10001","11111","10001","10001","10001"],
  'B': ["11110","10001","10001","11110","10001","10001","11110"],
  'C': ["01110","10001","10000","10000","10000","10001","01110"],
  'D': ["11110","10001","10001","10001","10001","10001","11110"],
  'E': ["11111","10000","10000","11110","10000","10000","11111"],
  'K': ["10001","10010","10100","11000","10100","10010","10001"],
  'M': ["10001","11011","10101","10001","10001","10001","10001"],
  'N': ["10001","11001","10101","10011","10001","10001","10001"],
  'O': ["01110","10001","10001","10001","10001","10001","01110"],
  'R': ["11110","10001","10001","11110","10100","10010","10001"],
  'S': ["01110","10001","10000","01110","00001","10001","01110"],
  'X': ["10001","10001","01010","00100","01010","10001","10001"],
  '0': ["01110","10001","10011","10101","11001","10001","01110"],
  '1': ["00100","01100","00100","00100","00100","00100","01110"],
  '2': ["01110","10001","00001","00110","01000","10000","11111"],
  '3': ["11110","00001","00001","01110","00001","00001","11110"],
  '4': ["00010","00110","01010","10010","11111","00010","00010"],
  ' ': ["00000","00000","00000","00000","00000","00000","00000"],
  'X': ["10001","01010","00100","00100","01010","10001","10001"],
}

def draw_text(draw, text, x, y, scale, color):
    cx = x
    for ch in text:
        g = GLYPHS.get(ch.upper(), GLYPHS[' '])
        for row_i, row in enumerate(g):
            for col_i, px in enumerate(row):
                if px == '1':
                    rx = cx + col_i * scale
                    ry = y  + row_i * scale
                    draw.rectangle([rx, ry, rx+scale-1, ry+scale-1], fill=color)
        cx += (len(g[0]) + 1) * scale

def text_width(text, scale):
    total = 0
    for ch in text:
        g = GLYPHS.get(ch.upper(), GLYPHS[' '])
        total += (len(g[0]) + 1) * scale
    return total - scale

# 뱀 패턴 (그리드 좌표)
CELL = 28
SNAKE_CELLS = [
    # 머리 → 오른쪽
    (2,2),(3,2),(4,2),(5,2),(6,2),(7,2),(8,2),(9,2),(10,2),(11,2),(12,2),
    # 아래
    (12,3),(12,4),(12,5),
    # 왼쪽
    (11,5),(10,5),(9,5),(8,5),(7,5),(6,5),(5,5),(4,5),(3,5),(2,5),
    # 아래
    (2,6),(2,7),(2,8),
    # 오른쪽
    (3,8),(4,8),(5,8),(6,8),(7,8),(8,8),(9,8),(10,8),
    # 아래
    (10,9),(10,10),
    # 왼쪽
    (9,10),(8,10),(7,10),(6,10),(5,10),(4,10),(3,10),
]
HEAD = SNAKE_CELLS[0]
FOOD_CELL = (10, 7)

img  = Image.new('RGB', (W, H), BG)
draw = ImageDraw.Draw(img)

# 배경 격자 (은은하게)
for gx in range(0, W, CELL):
    draw.line([(gx, 0), (gx, H)], fill=(50, 48, 43), width=1)
for gy in range(0, H, CELL):
    draw.line([(0, gy), (W, gy)], fill=(50, 48, 43), width=1)

# 뱀 그리기
for i, (cx, cy) in enumerate(SNAKE_CELLS):
    x0 = cx * CELL + 2
    y0 = cy * CELL + 2
    x1 = x0 + CELL - 4
    y1 = y0 + CELL - 4
    color = SNAKE_HEAD if i == 0 else SNAKE_BODY
    draw.rectangle([x0, y0, x1, y1], fill=color)

# 눈 (머리)
hx = HEAD[0] * CELL
hy = HEAD[1] * CELL
draw.rectangle([hx+6,  hy+6,  hx+10, hy+10], fill=BG)
draw.rectangle([hx+18, hy+6,  hx+22, hy+10], fill=BG)

# 먹이
fx = FOOD_CELL[0] * CELL + 4
fy = FOOD_CELL[1] * CELL + 4
draw.ellipse([fx, fy, fx+CELL-8, fy+CELL-8], fill=FOOD)

# ── 오른쪽 패널 ──────────────────────────────
PX = 420   # 패널 시작 x

# SNAKE 제목
title  = "SNAKE"
tscale = 12
tw     = text_width(title, tscale)
tx     = PX + (W - PX - tw) // 2
draw_text(draw, title, tx, 80, tscale, AMBER)

# ARCADE 부제목
sub    = "ARCADE"
sscale = 6
sw     = text_width(sub, sscale)
sx     = PX + (W - PX - sw) // 2
draw_text(draw, sub, sx, 80 + 7*tscale + 14, sscale, CREAM)

# 구분선
line_y = 80 + 7*tscale + 14 + 7*sscale + 20
draw.line([(PX + 40, line_y), (W - 40, line_y)], fill=(80, 78, 73), width=2)

# 하트 표시
heart_y = line_y + 28
heart_x = PX + (W - PX) // 2 - 2 * 36
for i in range(5):
    hcol = FOOD if i < 5 else HEART_EMPTY
    hx2 = heart_x + i * 36
    draw_text(draw, chr(0x2665) if False else '', hx2, heart_y, 4, hcol)
# 하트를 직접 그림 (글리프 없음)
for i in range(5):
    bx = heart_x + i * 36
    by = heart_y
    s  = 4
    pts = [
        (bx+s,by),(bx+2*s,by-s),(bx+4*s,by),(bx+4*s,by+2*s),
        (bx+2*s,by+4*s),(bx,by+2*s),(bx,by)
    ]
    draw.polygon(pts, fill=FOOD)

# SCORE 표시
score_y = heart_y + 32
score_label = "SCORE"
score_val   = "0042"
lscale = 4
vscale = 7
lw = text_width(score_label, lscale)
vw = text_width(score_val, vscale)
lx = PX + (W - PX - lw) // 2
vx = PX + (W - PX - vw) // 2
draw_text(draw, score_label, lx, score_y, lscale, (120, 118, 110))
draw_text(draw, score_val,   vx, score_y + 7*lscale + 6, vscale, CREAM)

# COMBO 표시
combo_y = score_y + 7*lscale + 6 + 7*vscale + 16
combo_txt = "COMBO  X3"
cscale = 4
cw = text_width(combo_txt, cscale)
cx2 = PX + (W - PX - cw) // 2
draw_text(draw, combo_txt, cx2, combo_y, cscale, AMBER)

out = os.path.join(os.path.dirname(__file__), 'screenshots', 'feature_graphic.png')
os.makedirs(os.path.dirname(out), exist_ok=True)
img.save(out)
print(f"Saved: {out}  ({W}×{H})")
