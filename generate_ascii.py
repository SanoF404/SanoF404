from pathlib import Path
import argparse
import html
from PIL import Image

ASCII_CHARS = "@%#*+=-:. "

def image_to_ascii(image_path: Path, width: int = 90) -> list[str]:
    image = Image.open(image_path).convert("L")
    height = max(1, int(image.height / image.width * width * 0.48))
    image = image.resize((width, height))
    pixels = list(image.getdata())
    lines = []
    for row in range(height):
        line = "".join(
            ASCII_CHARS[min(len(ASCII_CHARS) - 1, pixel * len(ASCII_CHARS) // 256)]
            for pixel in pixels[row * width:(row + 1) * width]
        )
        lines.append(line)
    return lines

def main() -> None:
    parser = argparse.ArgumentParser(description="Generate an animated ASCII portrait SVG.")
    parser.add_argument("--input", default="assets/avatar.jpg", help="Input portrait image")
    parser.add_argument("--output", default="ascii_portrait.svg", help="Output SVG path")
    parser.add_argument("--width", type=int, default=90, help="ASCII character width")
    args = parser.parse_args()

    image_path = Path(args.input)
    if not image_path.is_file():
        raise SystemExit(f"Image not found: {image_path}. Add your own image first.")

    lines = image_to_ascii(image_path, max(20, min(args.width, 140)))
    line_height = 12
    padding = 20
    svg_width = max(len(line) for line in lines) * 7.2 + padding * 2
    svg_height = len(lines) * line_height + padding * 2
    escaped_lines = [html.escape(line) for line in lines]

    output = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{svg_width:.0f}" height="{svg_height}" viewBox="0 0 {svg_width:.0f} {svg_height}">',
        '<rect width="100%" height="100%" fill="#080b10" rx="12"/>',
        '<style>text{font-family:Consolas,Monaco,monospace;font-size:10px;fill:#67f5b5;white-space:pre}.line{opacity:0;animation:reveal .01s forwards}@keyframes reveal{to{opacity:1}}</style>',
        '<text x="20" y="16" fill="#8b949e">[ profile image :: ASCII render ]</text>',
    ]
    for index, line in enumerate(escaped_lines):
        y = padding + 10 + index * line_height
        output.append(
            f'<text class="line" x="20" y="{y}" style="animation-delay:{index * 0.035:.3f}s">{line}</text>'
        )
    output.append("</svg>")
    Path(args.output).write_text("\n".join(output), encoding="utf-8")
    print(f"Generated {args.output}")

if __name__ == "__main__":
    main()
