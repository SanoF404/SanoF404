from pathlib import Path
import html
import os

def main() -> None:
    username = os.getenv("GITHUB_USERNAME", "SanoF404")
    title = "CYBERSECURITY PORTFOLIO"
    lines = [
        ("USER", username),
        ("FOCUS", "Defensive Security | Linux Hardening"),
        ("LANGUAGES", "Python | Bash | SQL"),
        ("TOOLS", "Linux | Git | GitHub"),
        ("PROJECTS", "Log Analysis | File Integrity | Cloud Scanner"),
        ("STATUS", "Building. Testing. Learning."),
    ]

    width, height = 760, 330
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" rx="14" fill="#0d1117" stroke="#30363d"/>',
        '<rect width="100%" height="42" rx="14" fill="#161b22"/>',
        '<rect y="28" width="100%" height="14" fill="#161b22"/>',
        '<circle cx="22" cy="21" r="5" fill="#ff5f56"/><circle cx="42" cy="21" r="5" fill="#ffbd2e"/><circle cx="62" cy="21" r="5" fill="#27c93f"/>',
        f'<text x="85" y="26" fill="#c9d1d9" font-family="monospace" font-size="13">{html.escape(title)}</text>',
        '<text x="28" y="75" fill="#67f5b5" font-family="monospace" font-size="15">$ whoami</text>',
        f'<text x="28" y="101" fill="#e6edf3" font-family="monospace" font-size="18">{html.escape(username)}</text>',
    ]
    y = 140
    for label, value in lines[1:]:
        parts.append(f'<text x="28" y="{y}" fill="#67f5b5" font-family="monospace" font-size="13">{html.escape(label):<12}</text>')
        parts.append(f'<text x="160" y="{y}" fill="#c9d1d9" font-family="monospace" font-size="13">{html.escape(value)}</text>')
        y += 31
    parts.append('<text x="28" y="309" fill="#8b949e" font-family="monospace" font-size="11">defensive security • open-source projects • continuous learning</text>')
    parts.append("</svg>")
    Path("terminal_card.svg").write_text("\n".join(parts), encoding="utf-8")
    print("Generated terminal_card.svg")

if __name__ == "__main__":
    main()
