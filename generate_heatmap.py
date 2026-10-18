from datetime import datetime, timezone
from pathlib import Path
import json
import os
import urllib.error
import urllib.request
import html

USERNAME = os.getenv("GITHUB_USERNAME", "SanoF404")
TOKEN = os.getenv("GITHUB_TOKEN", "")
OUTPUT = Path("contribution_heatmap.svg")

QUERY = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks {
          contributionDays {
            date
            contributionCount
            color
          }
        }
      }
    }
  }
}
"""

def fetch_contributions() -> dict:
    if not TOKEN:
        raise SystemExit("Set GITHUB_TOKEN to a GitHub token with public profile read access.")
    payload = json.dumps({"query": QUERY, "variables": {"login": USERNAME}}).encode()
    request = urllib.request.Request(
        "https://api.github.com/graphql",
        data=payload,
        headers={
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/json",
            "User-Agent": "SanoF404-contribution-heatmap",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            data = json.load(response)
    except urllib.error.URLError as exc:
        raise SystemExit(f"GitHub API request failed: {exc}") from exc
    if data.get("errors"):
        raise SystemExit(f"GitHub API error: {data['errors']}")
    user = data.get("data", {}).get("user")
    if not user:
        raise SystemExit(f"GitHub user not found: {USERNAME}")
    return user["contributionsCollection"]["contributionCalendar"]

def main() -> None:
    calendar = fetch_contributions()
    days = [day for week in calendar["weeks"] for day in week["contributionDays"]]
    cell, gap, left, top = 11, 3, 28, 58
    columns = (len(days) + 6) // 7
    width = left * 2 + columns * (cell + gap)
    height = 175
    max_count = max((day["contributionCount"] for day in days), default=0)
    colors = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" rx="12" fill="#0d1117" stroke="#30363d"/>',
        f'<text x="{left}" y="27" fill="#e6edf3" font-family="monospace" font-size="14">{calendar["totalContributions"]} contributions in the last year</text>',
        '<text x="28" y="45" fill="#8b949e" font-family="monospace" font-size="10">LESS</text>',
    ]
    for index, day in enumerate(days):
        col, row = divmod(index, 7)
        count = day["contributionCount"]
        if count == 0 or max_count == 0:
            level = 0
        else:
            level = min(4, max(1, int(count / max_count * 4) + 1))
        x = left + col * (cell + gap)
        y = top + row * (cell + gap)
        title = html.escape(f'{day["date"]}: {count} contributions')
        svg.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="2" fill="{colors[level]}"><title>{title}</title></rect>')
    legend_x = width - 100
    svg.append(f'<text x="{legend_x - 32}" y="45" fill="#8b949e" font-family="monospace" font-size="10">MORE</text>')
    for i, color in enumerate(colors):
        svg.append(f'<rect x="{legend_x + i * 14}" y="36" width="10" height="10" rx="2" fill="{color}"/>')
    svg.append(f'<text x="{left}" y="{height - 10}" fill="#8b949e" font-family="monospace" font-size="10">Updated {datetime.now(timezone.utc).strftime("%Y-%m-%d")} UTC</text>')
    svg.append("</svg>")
    OUTPUT.write_text("\n".join(svg), encoding="utf-8")
    print(f"Generated {OUTPUT}")

if __name__ == "__main__":
    main()
