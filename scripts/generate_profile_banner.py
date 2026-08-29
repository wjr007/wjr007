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

from PIL import Image, ImageEnhance, ImageFilter, ImageOps


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "work" / "profile-assets" / "profile-avatar.png"
OUT = ROOT / "work" / "profile-assets"

PROFILE = {
    "name": "WALTEIR JUNIOR",
    "handle": "@wjr007",
    "role": "IA & DATA SCIENCE STUDENT",
    "origin": "BRAZIL",
    "education": "BSc AI & DATA SCIENCE",
    "status": "BUILDING + LEARNING + SHIPPING",
    "toolchain": "VS CODE · GIT · DOCKER · FIGMA",
    "languages": "PYTHON · JAVA · JAVASCRIPT",
    "frontend": "HTML · CSS · IHM",
    "backend": "FASTAPI · OOP · APIs",
    "database": "MYSQL · SQL",
    "infra": "AWS · DOCKER · KUBERNETES",
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


def row(label: str, value: str, y: int, palette: dict[str, str]) -> str:
    dots = "." * max(3, 49 - len(label) - min(len(value), 35))
    return f'''<text x="500" y="{y}" class="label">{escape(label)}</text><text x="594" y="{y}" class="leaders">{dots}</text><text x="1108" y="{y}" text-anchor="end" class="value">{escape(value)}</text>'''


def banner(theme: str) -> str:
    p = PALETTES[theme]
    portrait = path_for_portrait(theme)
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
  <g fill="{p['portrait']}" shape-rendering="crispEdges" opacity=".96">{portrait}</g>
  <text x="48" y="492" class="mono" font-size="11" letter-spacing="1.4" fill="{p['chrome']}">FOCUS.MODULES</text>
  <rect x="48" y="503" width="91" height="23" rx="11.5" fill="{p['portrait']}" opacity=".16"/><text x="93.5" y="519" text-anchor="middle" class="mono" font-size="10" fill="{p['portrait']}">AI / ML</text>
  <rect x="148" y="503" width="91" height="23" rx="11.5" fill="{p['chrome']}" opacity=".14"/><text x="193.5" y="519" text-anchor="middle" class="mono" font-size="10" fill="{p['chrome']}">DATA</text>
  <rect x="248" y="503" width="111" height="23" rx="11.5" fill="{p['portrait']}" opacity=".16"/><text x="303.5" y="519" text-anchor="middle" class="mono" font-size="10" fill="{p['portrait']}">BACKEND</text>
  <rect x="492" y="77" width="663" height="488" rx="10" fill="{p['panel']}" stroke="{p['line']}"/>
  <text x="520" y="105" class="mono" font-size="12" letter-spacing="2" fill="{p['chrome']}">SYSTEM.INFO</text>
  <circle class="live" cx="1016" cy="100" r="5" fill="#FB7185"/><text x="1029" y="105" class="mono" font-size="12" fill="#FB7185">LIVE</text>
  <rect x="1070" y="84" width="64" height="25" rx="12.5" fill="{p['portrait']}" opacity=".2"/><text x="1102" y="102" text-anchor="middle" class="mono" font-size="12" fill="{p['portrait']}">{escape(PROFILE['handle'])}</text>
  {y_rows}
  <text x="520" y="528" class="mono" font-size="12" fill="{p['chrome']}">›</text><text x="539" y="528" class="mono" font-size="12" fill="{p['muted']}">next_build = explore(\"ai + data + systems\")</text>
  <text x="48" y="547" class="mono" font-size="10" fill="{p['muted']}">PORTRAIT SOURCE: CURRENT GITHUB AVATAR · 1-BIT DOT RENDER</text>
</svg>'''


def main() -> None:
    if not SOURCE.exists():
        raise FileNotFoundError(f"Missing portrait source: {SOURCE}")
    OUT.mkdir(parents=True, exist_ok=True)
    for theme in PALETTES:
        (OUT / f"{theme}.svg").write_text(banner(theme), encoding="utf-8")


if __name__ == "__main__":
    main()

