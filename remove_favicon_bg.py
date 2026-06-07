from rembg import remove
from PIL import Image
import io, glob, os

def remove_bg(img):
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    out = remove(buf.getvalue())
    return Image.open(io.BytesIO(out)).convert('RGBA')

def remove_bg_small(img, scale=8):
    """Upscale tiny image, remove bg, downscale back for clean edges."""
    orig = img.size
    big = img.resize((orig[0]*scale, orig[1]*scale), Image.LANCZOS)
    big_clean = remove_bg(big)
    return big_clean.resize(orig, Image.LANCZOS)

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# apple-touch-icon (180x180) — use normal rembg
print('apple-touch-icon.png ...', flush=True)
remove_bg(Image.open('apple-touch-icon.png')).save('apple-touch-icon.png')

# 32x32 and 16x16 — upscale first
for name in ('favicon-32x32.png', 'favicon-16x16.png'):
    print(f'{name} ...', flush=True)
    remove_bg_small(Image.open(name)).save(name)

# 10 animation frames
for i in range(10):
    name = f'favicon-frame-{i:02d}.png'
    print(f'{name} ...', flush=True)
    remove_bg_small(Image.open(name)).save(name)

# Regenerate favicon.ico (embeds 32x32 + 16x16 transparent)
print('Regenerating favicon.ico ...', flush=True)
img32 = Image.open('favicon-32x32.png').convert('RGBA')
img32.save('favicon.ico', format='ICO', sizes=[(16,16),(32,32)])

# Regenerate favicon.gif with transparency
print('Regenerating favicon.gif ...', flush=True)

def rgba_to_gif_frame(rgba_img):
    mask = rgba_img.getchannel('A')
    rgb = Image.new('RGB', rgba_img.size, (0, 0, 0))
    rgb.paste(rgba_img.convert('RGB'), mask=mask)
    p = rgb.quantize(colors=255, dither=1)
    # Shift indices +1 to free slot 0 for transparency
    data = bytes([min(b + 1, 255) for b in p.tobytes()])
    palette = [0, 0, 0] + list(p.getpalette())[:255*3]
    p2 = Image.frombytes('P', p.size, data)
    p2.putpalette(palette)
    px = list(p2.getdata())
    alpha_data = list(mask.getdata())
    for idx, a in enumerate(alpha_data):
        if a < 128:
            px[idx] = 0
    p2.putdata(px)
    return p2

gif_frames = [rgba_to_gif_frame(Image.open(f'favicon-frame-{i:02d}.png').convert('RGBA')) for i in range(10)]
gif_frames[0].save(
    'favicon.gif', save_all=True, append_images=gif_frames[1:],
    duration=120, loop=0, transparency=0, disposal=2,
)

# Update all HTML to reference PNG favicons (modern browsers prefer PNG over GIF for transparency)
print('Updating HTML favicon tags ...', flush=True)

OLD1 = '    <link rel="icon" type="image/gif" href="/favicon.gif">\n    <link rel="icon" href="/favicon.ico">'
NEW1 = '    <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">\n    <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">\n    <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">\n    <link rel="icon" href="/favicon.ico">'

OLD2 = '<link rel="icon" type="image/gif" href="/favicon.gif">\n<link rel="icon" href="/favicon.ico">'
NEW2 = '<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">\n<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">\n<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">\n<link rel="icon" href="/favicon.ico">'

# Also handle the 4-space-indented version with apple-touch-icon already present
OLD3 = '    <link rel="icon" type="image/gif" href="/favicon.gif">\n    <link rel="icon" href="/favicon.ico">\n    <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">'
NEW3 = NEW1  # same target

updated = 0
for path in glob.glob('**/*.html', recursive=True):
    c = open(path, encoding='utf-8').read()
    n = c.replace(OLD3, NEW3).replace(OLD1, NEW1).replace(OLD2, NEW2)
    # Also remove duplicate apple-touch-icon if any
    dup = '<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">\n    <link rel="apple-touch-icon"'
    if dup in n:
        n = n.replace('<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">\n    <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">', '<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">')
    if n != c:
        open(path, 'w', encoding='utf-8').write(n)
        updated += 1

print(f'Updated {updated} HTML files.')
print('ALL DONE!')
