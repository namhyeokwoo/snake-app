from PIL import Image, ImageDraw
import os
import math

BG = (38, 36, 31)
SNAKE_BODY = (76, 175, 80)
SNAKE_HEAD = (165, 214, 167)
FOOD = (255, 82, 82)

# 10x10 pixel art: 0=bg, 1=body, 2=head, 3=food
# 뱀이 아이콘 가득 채우는 코일 형태 (8칸 폭)
PATTERN = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 2, 1, 1, 1, 1, 1, 1, 1, 0],  # 머리 → 오른쪽 8칸
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],  # 오른쪽 벽 아래로
    [0, 0, 0, 0, 3, 0, 0, 0, 1, 0],  # 먹이 + 오른쪽 벽
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],  # 왼쪽으로 8칸
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],  # 왼쪽 벽 아래로
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 0, 0, 0],  # 오른쪽으로 6칸
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],  # 꼬리
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]

GRID = len(PATTERN)

def render_pattern(size, bg_color, transparent_bg=False):
    mode = 'RGBA' if transparent_bg else 'RGB'
    bg = (0, 0, 0, 0) if transparent_bg else bg_color
    img = Image.new(mode, (size, size), bg)
    draw = ImageDraw.Draw(img)
    cell = size / GRID
    for row in range(GRID):
        for col in range(GRID):
            val = PATTERN[row][col]
            if val == 0:
                continue
            if val == 2:
                color = SNAKE_HEAD
            elif val == 3:
                color = FOOD
            else:
                color = SNAKE_BODY
            if transparent_bg:
                color = color + (255,)  # type: ignore
            x0 = int(col * cell)
            y0 = int(row * cell)
            x1 = int((col + 1) * cell) - 1
            y1 = int((row + 1) * cell) - 1
            draw.rectangle([x0, y0, x1, y1], fill=color)
    return img

def make_round(img):
    size = img.size[0]
    mask = Image.new('L', (size, size), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, size - 1, size - 1], fill=255)
    result = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    src = img.convert('RGBA')
    result.paste(src, mask=mask)
    return result

BASE = os.path.join(os.path.dirname(__file__), 'android', 'app', 'src', 'main', 'res')

LAUNCHER_SIZES = {
    'mipmap-mdpi':    48,
    'mipmap-hdpi':    72,
    'mipmap-xhdpi':   96,
    'mipmap-xxhdpi':  144,
    'mipmap-xxxhdpi': 192,
}

FOREGROUND_SIZES = {
    'mipmap-mdpi':    108,
    'mipmap-hdpi':    162,
    'mipmap-xhdpi':   216,
    'mipmap-xxhdpi':  324,
    'mipmap-xxxhdpi': 432,
}

for folder, size in LAUNCHER_SIZES.items():
    path = os.path.join(BASE, folder)
    os.makedirs(path, exist_ok=True)

    square = render_pattern(size, BG)
    square.save(os.path.join(path, 'ic_launcher.png'))

    rounded = make_round(render_pattern(size, BG))
    bg = Image.new('RGB', (size, size), BG)
    bg.paste(rounded, mask=rounded.split()[3])
    bg.save(os.path.join(path, 'ic_launcher_round.png'))

    print(f'{folder}: ic_launcher + ic_launcher_round ({size}x{size})')

for folder, size in FOREGROUND_SIZES.items():
    path = os.path.join(BASE, folder)
    os.makedirs(path, exist_ok=True)

    fg = render_pattern(size, BG, transparent_bg=True)
    fg.save(os.path.join(path, 'ic_launcher_foreground.png'))

    print(f'{folder}: ic_launcher_foreground ({size}x{size})')

print('\nDone.')
