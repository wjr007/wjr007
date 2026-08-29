#!/usr/bin/env python3
"""Generate theme-aware SVG profile banners from a local portrait.

Documentation: DOCUMENTACAO.md#banner
Dependencies: Pillow; a local head-and-shoulders image at work/profile-assets/profile-avatar.png.
Edit: change the PROFILE dictionary or PALETTES below, then run this script to regenerate dark.svg
and light.svg. The source photo is intentionally not committed.
"""

from __future__ import annotations

from html import escape
from pathlib import Path
import random

from PIL import Image, ImageEnhance, ImageFilter, ImageOps


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "work" / "profile-assets" / "profile-avatar.png"
OUT = ROOT / "work" / "profile-assets"

PROFILE = {
    "name": "WALTEIR JUNIOR",
    "handle": "@wjr007",
    "role": "AI & DATA SCIENCE",
    "origin": "BRAZIL",
    "education": "BSc AI & DATA SCIENCE",
    "status": "MACHINE LEARNING · DEEP LEARNING",
    "toolchain": "PYTHON · JAVA · DATABASES",
    "languages": "DATA ANALYTICS · MULTI-CLOUD",
    "frontend": "UI / UX · PRODUCT DESIGN",
    "backend": "FASTAPI · OOP · APIs",
    "database": "MYSQL · SQL",
    "infra": "MULTI-CLOUD · DOCKER · KUBERNETES",
    "mail": "junior57k@gmail.com",
    "portfolio": "github.com/wjr007",
    "linkedin": "linkedin.com/in/walteir-luiz-de-morais-junior-42a21928a",
}

PALETTES = {
    "dark": {"bg": "#0A101F", "panel": "#0D1526", "line": "#1D2A42", "ink": "#E7EEF9", "muted": "#94A3B8", "portrait": "#A78BFA", "chrome": "#22D3EE"},
    "light": {"bg": "#F7F9FC", "panel": "#FFFFFF", "line": "#CBD5E1", "ink": "#0F172A", "muted": "#475569", "portrait": "#7C3AED", "chrome": "#0891B2"},
}


def path_for_portrait(theme: str) -> str:
    """Turn the profile photo into an ordered 1-bit dot field made of SVG paths."""
    image = Image.open(SOURCE).convert("L")
    # A portrait-scale grid fills the visual panel while preserving head and shoulders.
    image = ImageOps.fit(image, (140, 160), method=Image.Resampling.LANCZOS, centering=(0.5, 0.36))
    image = ImageOps.autocontrast(image, cutoff=1)
    image = ImageEnhance.Contrast(image).enhance(1.3)
    image = image.filter(ImageFilter.UnsharpMask(radius=2, percent=140, threshold=2))

    pixels = image.load()
    commands: list[str] = []
    # Preserve the lit subject in both themes. Inverting the light version makes this
    # portrait's dark studio background dominate the panel instead of the person.
    for y in range(image.height):
        for x in range(image.width):
            level = pixels[x, y]
            ink = level
            if ink > 108:
                px, py = 70 + x * 2.25, 126 + y * 2.25
                size = 1.38 if ink < 185 else 1.72
                commands.append(f"M{px:.1f} {py:.1f}h{size:.1f}v{size:.1f}h-{size:.1f}z")
    # SVG path commands must live in a <path> element. Returning bare commands
    # would be treated as text and leave the portrait panel empty on GitHub.
    return f'<path d="{"".join(commands)}"/>'


def tech_mark(kind: str) -> str:
    """Return a deterministic dot cloud for a personal technical mark."""
    random.seed({"code": 7, "n8n": 17, "data": 29}[kind])
    points: list[tuple[float, float]] = []

    def segment_distance(px: float, py: float, x1: float, y1: float, x2: float, y2: float) -> float:
        dx, dy = x2 - x1, y2 - y1
        length_sq = dx * dx + dy * dy
        t = 0 if length_sq == 0 else max(0, min(1, ((px - x1) * dx + (py - y1) * dy) / length_sq))
        return ((px - (x1 + t * dx)) ** 2 + (py - (y1 + t * dy)) ** 2) ** 0.5

    for _ in range(3000):
        x, y = random.uniform(95, 370), random.uniform(150, 460)
        hit = False
        if kind == "code":
            lines = [(250, 185, 145, 305), (145, 305, 250, 425), (305, 185, 365, 305), (365, 305, 305, 425), (290, 175, 225, 435)]
            hit = min(segment_distance(x, y, *line) for line in lines) < 7.2
        elif kind == "n8n":
            nodes = [(160, 305), (280, 210), (280, 400)]
            node_hit = min(((x - nx) ** 2 + (y - ny) ** 2) ** 0.5 for nx, ny in nodes) < 42
            links = [(190, 282, 248, 230), (190, 328, 248, 378)]
            hit = node_hit or min(segment_distance(x, y, *line) for line in links) < 6.5
        else:
            # Database cylinder: intentionally geometric and readable at README scale.
            top = ((x - 230) / 100) ** 2 + ((y - 205) / 30) ** 2
            bottom = ((x - 230) / 100) ** 2 + ((y - 410) / 30) ** 2
            sides = min(abs(x - 130), abs(x - 330)) < 7 and 205 < y < 410
            bands = any(abs(y - band) < 5 and 130 < x < 330 for band in (205, 275, 345, 410))
            hit = abs(top - 1) < .17 or abs(bottom - 1) < .17 or sides or bands
        if hit and random.random() < .63:
            points.append((x, y))
        if len(points) >= 850:
            break

    path = "".join(f"M{x:.1f} {y:.1f}h1.8v1.8h-1.8z" for x, y in points)
    return f'<path d="{path}"/>'


def row(label: str, value: str, y: int, palette: dict[str, str]) -> str:
    dots = "." * max(3, 49 - len(label) - min(len(value), 35))
    return f'''<text x="500" y="{y}" class="label">{escape(label)}</text><text x="594" y="{y}" class="leaders">{dots}</text><text x="1108" y="{y}" text-anchor="end" class="value">{escape(value)}</text>'''


def banner(theme: str) -> str:
    p = PALETTES[theme]
    portrait = path_for_portrait(theme)
    code_mark = tech_mark("code")
    n8n_mark = tech_mark("n8n")
    data_mark = tech_mark("data")
    rows = [
        ("SUBJECT", PROFILE["name"]), ("ROLE", PROFILE["role"]), ("ORIGIN", PROFILE["origin"]),
        ("EDUCATION", PROFILE["education"]), ("STATUS", PROFILE["status"]), ("TOOLCHAIN", PROFILE["toolchain"]),
        ("CORE.LANG", PROFILE["languages"]), ("CORE.FRONTEND", PROFILE["frontend"]), ("CORE.BACKEND", PROFILE["backend"]),
        ("CORE.DATABASE", PROFILE["database"]), ("CORE.INFRA", PROFILE["infra"]), ("GRID.MAIL", PROFILE["mail"]),
        ("GRID.PORTFOLIO", PROFILE["portfolio"]), ("GRID.LINKEDIN", PROFILE["linkedin"]),
    ]
    y_rows = "".join(row(label, value, 139 + i * 26, p) for i, (label, value) in enumerate(rows))
    return f'''<!--
  Profile banner — generated from the current GitHub profile photo.
  Documentation: DOCUMENTACAO.md#banner
  Regenerate: python scripts/generate_profile_banner.py
-->
<svg xmlns="http://www.w3.org/2000/svg" width="1180" height="610" viewBox="0 0 1180 610" role="img" aria-labelledby="title desc">
  <title id="title">{escape(PROFILE['name'])} profile terminal</title><desc id="desc">Terminal-styled profile summary with a dot-rendered portrait.</desc>
  <style>
    .mono {{ font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
    .label {{ font: 13px ui-monospace, monospace; fill: {p['muted']}; letter-spacing: 1px; }}
    .leaders {{ font: 12px ui-monospace, monospace; fill: {p['line']}; letter-spacing: 1px; }}
    .value {{ font: 13px ui-monospace, monospace; fill: {p['ink']}; letter-spacing: .3px; }}
    .live {{ animation: pulse 1.2s ease-in-out infinite; }} @keyframes pulse {{ 50% {{ opacity: .35; }} }}
  </style>
  <rect width="1180" height="610" rx="16" fill="{p['bg']}"/>
  <rect x="1" y="1" width="1178" height="608" rx="15" fill="none" stroke="{p['line']}"/>
  <rect x="1" y="1" width="1178" height="47" rx="15" fill="{p['panel']}"/><path d="M1 47.5h1178" stroke="{p['line']}"/>
  <circle cx="27" cy="24" r="6" fill="#FB7185"/><circle cx="49" cy="24" r="6" fill="#FBBF24"/><circle cx="71" cy="24" r="6" fill="#34D399"/>
  <text x="590" y="29" text-anchor="middle" class="mono" font-size="14" fill="{p['muted']}">wjr007://profile --live</text>
  <rect x="25" y="77" width="408" height="488" rx="10" fill="{p['panel']}" stroke="{p['line']}"/>
  <text x="48" y="105" class="mono" font-size="12" letter-spacing="2" fill="{p['chrome']}">VISUAL.MAP</text>
  <path d="M48 114h362" stroke="{p['line']}"/>
  <defs><filter id="glow"><feGaussianBlur stdDeviation="3" result="blur"/><feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
  <rect x="45" y="121" width="368" height="366" rx="5" fill="none" stroke="{p['chrome']}" opacity=".55" filter="url(#glow)"/>
  <g fill="{p['portrait']}" shape-rendering="crispEdges" opacity=".96">
    <g opacity="1">{portrait}<animate attributeName="opacity" dur="14.2s" repeatCount="indefinite" values="1;1;0;0;0;0;0;0;0;1" keyTimes="0;.21;.28;.31;.48;.51;.68;.71;.78;1"/></g>
    <g opacity="0">{code_mark}<animate attributeName="opacity" dur="14.2s" repeatCount="indefinite" values="0;0;1;1;0;0;0;0;0;0" keyTimes="0;.26;.31;.43;.48;.51;.68;.71;.78;1"/></g>
    <g opacity="0">{n8n_mark}<animate attributeName="opacity" dur="14.2s" repeatCount="indefinite" values="0;0;0;0;0;1;1;0;0;0" keyTimes="0;.26;.31;.43;.48;.51;.63;.68;.78;1"/></g>
    <g opacity="0">{data_mark}<animate attributeName="opacity" dur="14.2s" repeatCount="indefinite" values="0;0;0;0;0;0;0;1;1;0" keyTimes="0;.26;.31;.43;.48;.51;.63;.68;.74;1"/></g>
  </g>
  <text x="48" y="506" class="mono" font-size="11" letter-spacing="1.4" fill="{p['chrome']}">VISUAL.MORPH :: PHOTO → CODE → n8n → DATA</text>
  <rect x="48" y="518" width="116" height="20" rx="10" fill="{p['portrait']}" opacity=".16"/><text x="106" y="532" text-anchor="middle" class="mono" font-size="9" fill="{p['portrait']}">AI / ML</text>
  <rect x="171" y="518" width="116" height="20" rx="10" fill="{p['chrome']}" opacity=".14"/><text x="229" y="532" text-anchor="middle" class="mono" font-size="9" fill="{p['chrome']}">AUTOMATION</text>
  <rect x="294" y="518" width="91" height="20" rx="10" fill="{p['portrait']}" opacity=".16"/><text x="339.5" y="532" text-anchor="middle" class="mono" font-size="9" fill="{p['portrait']}">DATA</text>
  <rect x="492" y="77" width="663" height="488" rx="10" fill="{p['panel']}" stroke="{p['line']}"/>
  <text x="520" y="105" class="mono" font-size="12" letter-spacing="2" fill="{p['chrome']}">SYSTEM.INFO</text>
  <circle class="live" cx="1016" cy="100" r="5" fill="#FB7185"/><text x="1029" y="105" class="mono" font-size="12" fill="#FB7185">LIVE</text>
  <rect x="1070" y="84" width="64" height="25" rx="12.5" fill="{p['portrait']}" opacity=".2"/><text x="1102" y="102" text-anchor="middle" class="mono" font-size="12" fill="{p['portrait']}">{escape(PROFILE['handle'])}</text>
  {y_rows}
  <text x="520" y="528" class="mono" font-size="12" fill="{p['chrome']}">›</text><text x="539" y="528" class="mono" font-size="12" fill="{p['muted']}">next_build = explore(\"ai + data + systems\")</text>
  <text x="48" y="552" class="mono" font-size="10" fill="{p['muted']}">PORTRAIT SOURCE: CURRENT GITHUB AVATAR · DOT-MORPH RENDER</text>
</svg>'''


def main() -> None:
    if not SOURCE.exists():
        raise FileNotFoundError(f"Missing portrait source: {SOURCE}")
    OUT.mkdir(parents=True, exist_ok=True)
    for theme in PALETTES:
        (OUT / f"{theme}.svg").write_text(banner(theme), encoding="utf-8")


if __name__ == "__main__":
    main()

