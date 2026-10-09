"""
Gera ícone do app, ícone adaptativo, ícone temático (monocromático) e splash screen
do Android no tema do SISTEMA (fundo escuro + "S" brilhante azul num hexágono).

Uso (só precisa rodar de novo se quiser mudar o visual):
    pip install pillow fonttools brotli
    npm install            # para ter a fonte Orbitron em node_modules
    python3 scripts/gen_icons.py

Os arquivos vão direto para android/app/src/main/res/ e uma cópia grande
fica em resources/ (icon.png e splash.png) para referência.
"""
import io
import math
import os

from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RES = os.path.join(ROOT, 'android', 'app', 'src', 'main', 'res')
BG = (2, 5, 11)
BLUE = (63, 169, 255)
CYAN = (95, 227, 255)
DENSITIES = {'mdpi': 1, 'hdpi': 1.5, 'xhdpi': 2, 'xxhdpi': 3, 'xxxhdpi': 4}


def orbitron(size, weight=900):
    """Carrega a Orbitron (woff2 do @fontsource) convertendo para TTF em memória."""
    path = os.path.join(ROOT, 'node_modules', '@fontsource', 'orbitron', 'files',
                        f'orbitron-latin-{weight}-normal.woff2')
    font = TTFont(path)
    font.flavor = None
    buf = io.BytesIO()
    font.save(buf)
    buf.seek(0)
    return ImageFont.truetype(buf, size)


def hex_points(cx, cy, r):
    return [(cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a)))
            for a in (-90, -30, 30, 90, 150, 210)]


def background(size):
    """Fundo escuro com brilho azul radial."""
    img = Image.new('RGBA', (size, size), BG + (255,))
    glow = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(glow)
    r = size * 0.42
    d.ellipse([size / 2 - r, size * 0.46 - r, size / 2 + r, size * 0.46 + r], fill=BLUE + (120,))
    glow = glow.filter(ImageFilter.GaussianBlur(size * 0.16))
    img.alpha_composite(glow)
    # grade sutil de "holograma"
    grid = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    gd = ImageDraw.Draw(grid)
    step = max(4, size // 18)
    for y in range(0, size, step):
        gd.line([(0, y), (size, y)], fill=BLUE + (18,), width=max(1, size // 512))
    img.alpha_composite(grid)
    return img


def emblem(size, scale=1.0, mono=False):
    """Hexágono + "S" brilhante, centrado, num canvas transparente."""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    cx = cy = size / 2
    hr = size * 0.30 * scale
    stroke = max(2, int(size * 0.022 * scale))

    shape = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(shape)
    pts = hex_points(cx, cy, hr)
    if not mono:
        d.polygon(pts, fill=BLUE + (40,))
    d.line(pts + [pts[0]], fill=(255, 255, 255, 255) if mono else CYAN + (255,), width=stroke, joint='curve')

    font = orbitron(int(size * 0.34 * scale))
    d.text((cx, cy + size * 0.01 * scale), 'S', font=font, anchor='mm', fill=(255, 255, 255, 255))

    if not mono:
        glow = shape.filter(ImageFilter.GaussianBlur(size * 0.03 * scale))
        r, g, b, a = glow.split()
        tinted = Image.merge('RGBA', (Image.new('L', glow.size, BLUE[0]), Image.new('L', glow.size, BLUE[1]),
                                      Image.new('L', glow.size, BLUE[2]), a))
        img.alpha_composite(tinted)
        img.alpha_composite(tinted)
    img.alpha_composite(shape)
    return img


def rounded_mask(size, radius_ratio):
    m = Image.new('L', (size, size), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, size - 1, size - 1], radius=int(size * radius_ratio), fill=255)
    return m


def save(img, *parts):
    path = os.path.join(RES, *parts)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.save(path, optimize=True)


def main():
    big = 1024
    full_bg = background(big)
    full_icon = full_bg.copy()
    full_icon.alpha_composite(emblem(big, scale=1.35))
    os.makedirs(os.path.join(ROOT, 'resources'), exist_ok=True)
    full_icon.save(os.path.join(ROOT, 'resources', 'icon.png'))

    for name, k in DENSITIES.items():
        # Ícone clássico (quadrado arredondado) e redondo — 48dp
        s = int(48 * k)
        icon = full_icon.resize((s, s), Image.LANCZOS)
        sq = Image.new('RGBA', (s, s), (0, 0, 0, 0))
        sq.paste(icon, (0, 0), rounded_mask(s, 0.22))
        save(sq, f'mipmap-{name}', 'ic_launcher.png')
        rd = Image.new('RGBA', (s, s), (0, 0, 0, 0))
        circle = Image.new('L', (s, s), 0)
        ImageDraw.Draw(circle).ellipse([0, 0, s - 1, s - 1], fill=255)
        rd.paste(icon, (0, 0), circle)
        save(rd, f'mipmap-{name}', 'ic_launcher_round.png')

        # Ícone adaptativo (Android 8+) — camadas de 108dp, área segura de 66dp
        a = int(108 * k)
        save(background(a), f'mipmap-{name}', 'ic_launcher_background.png')
        save(emblem(a, scale=1.0), f'mipmap-{name}', 'ic_launcher_foreground.png')
        save(emblem(a, scale=1.0, mono=True), f'mipmap-{name}', 'ic_launcher_monochrome.png')

        # Ícone da splash do Android 12+ — canvas 288dp, círculo visível de 192dp
        p = int(288 * k)
        save(emblem(p, scale=1.0), f'drawable-{name}', 'splash_icon.png')

    # Splash antiga (Android 11 ou menos): imagem cheia retrato/paisagem
    sizes = {
        'port-mdpi': (320, 480), 'port-hdpi': (480, 800), 'port-xhdpi': (720, 1280),
        'port-xxhdpi': (960, 1600), 'port-xxxhdpi': (1280, 1920),
        'land-mdpi': (480, 320), 'land-hdpi': (800, 480), 'land-xhdpi': (1280, 720),
        'land-xxhdpi': (1600, 960), 'land-xxxhdpi': (1920, 1280),
    }
    for folder, (w, h) in list(sizes.items()) + [('', (480, 320))]:
        side = max(w, h)
        canvas = background(side).crop(((side - w) // 2, (side - h) // 2, (side - w) // 2 + w, (side - h) // 2 + h))
        m = int(min(w, h) * 0.62)
        canvas.alpha_composite(emblem(m, scale=1.35), ((w - m) // 2, int(h / 2 - m * 0.58)))
        d = ImageDraw.Draw(canvas)
        f = orbitron(max(12, int(min(w, h) * 0.055)), 700)
        text = 'S I S T E M A'
        d.text((w / 2, h / 2 + m * 0.42), text, font=f, anchor='mm', fill=(220, 238, 255, 255))
        save(canvas.convert('RGB'), f'drawable-{folder}' if folder else 'drawable', 'splash.png')
        if folder == 'port-xxxhdpi':
            canvas.save(os.path.join(ROOT, 'resources', 'splash.png'))
    print('Ícones e splash gerados em', RES)


if __name__ == '__main__':
    main()
