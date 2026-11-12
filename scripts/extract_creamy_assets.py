from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "menu"
SRC = Path(r"C:\Users\regif\AppData\Local\Temp\codex-clipboard-c29f037f-cebd-4c22-a46b-f7060fdb1c21.png")

CROPS = [
    ("cremoso-mangonada-enchilada", (34, 184, 226, 402)),
    ("cremoso-alpinito-fresa", (228, 176, 476, 390)),
    ("cremoso-capuchino", (474, 176, 684, 390)),
    ("cremoso-crema-whisky", (94, 486, 340, 708)),
    ("cremoso-coco-loco", (330, 520, 550, 736)),
]


def feather_alpha(img: Image.Image) -> Image.Image:
    img = img.convert("RGBA")
    width, height = img.size
    alpha = Image.new("L", (width, height), 0)
    draw = ImageDraw.Draw(alpha)
    pad_x = int(width * 0.07)
    pad_y = int(height * 0.07)
    draw.rounded_rectangle((pad_x, pad_y, width - pad_x, height - pad_y), radius=34, fill=255)
    alpha = alpha.filter(ImageFilter.GaussianBlur(max(8, int(min(width, height) * 0.055))))
    img.putalpha(alpha)
    return img


def fit_canvas(img: Image.Image, size: int = 320) -> Image.Image:
    img = img.convert("RGBA")
    img.thumbnail((size - 14, size - 14), Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    canvas.alpha_composite(img, ((size - img.width) // 2, (size - img.height) // 2 - 4))
    return canvas


def make_contact(paths: list[tuple[str, Path]]) -> Path:
    font = ImageFont.load_default()
    sheet = Image.new("RGBA", (1100, 250), (238, 248, 252, 255))
    for index, (name, path) in enumerate(paths):
        img = Image.open(path).convert("RGBA")
        tile = Image.new("RGBA", (220, 250), (238, 248, 252, 255))
        img.thumbnail((190, 190), Image.Resampling.LANCZOS)
        tile.alpha_composite(img, ((220 - img.width) // 2, 12))
        ImageDraw.Draw(tile).text((10, 218), name[:30], fill=(18, 44, 61), font=font)
        sheet.alpha_composite(tile, (index * 220, 0))
    out = OUT / "cremosos-contact-sheet.png"
    sheet.save(out, optimize=True)
    return out


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    source = Image.open(SRC).convert("RGB")
    paths = []
    for name, box in CROPS:
        asset = fit_canvas(feather_alpha(source.crop(box)))
        out = OUT / f"{name}.png"
        asset.save(out, optimize=True)
        paths.append((name, out))
    print(make_contact(paths))


if __name__ == "__main__":
    main()
