"""Generate the boykisser-style SVG assets used by the profile README.

The character image is embedded as base64 because GitHub renders README SVGs
as <img>, which cannot load external files.
"""

import base64
import textwrap
from pathlib import Path
from xml.sax.saxutils import escape

HERE = Path(__file__).parent
ASSETS = HERE / "assets"
CHARACTER = HERE / "src" / "boykisser-cut.png"
CHARACTER_SIZE = (225, 236)

FONT = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
INK = "#111111"
SOFT_INK = "#4a4a4a"
BLUSH = "#e8223a"
PINK = "#ffd6e4"
PAPER = "#fff6f9"

HEART = "M0 -3 C-2 -8 -10 -7 -10 -1 C-10 5 -3 8 0 12 C3 8 10 5 10 -1 C10 -7 2 -8 0 -3Z"


def character_href() -> str:
    return "data:image/png;base64," + base64.b64encode(CHARACTER.read_bytes()).decode()


def blush_mark(x: float, y: float, scale: float = 1) -> str:
    """The little red zigzag the character has on its cheeks."""
    return (
        f'<path transform="translate({x} {y}) scale({scale})" d="M0 7 L5 1 L6 7 L11 1" '
        f'fill="none" stroke="{BLUSH}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>'
    )


def floating_hearts(spots: list[tuple[float, float, float, float]]) -> str:
    """(x, y, scale, delay) hearts that rise and fade out."""
    out = ""
    for x, y, scale, delay in spots:
        out += (
            f'<g opacity="0"><path d="{HEART}" fill="{BLUSH}" transform="scale({scale})"/>'
            f'<animateTransform attributeName="transform" type="translate" '
            f'values="{x} {y};{x + 6} {y - 40};{x - 4} {y - 80}" dur="4s" begin="{delay}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.15;.6;1" '
            f'dur="4s" begin="{delay}s" repeatCount="indefinite"/></g>'
        )
    return out


def heart_pattern() -> str:
    return (
        f'<pattern id="hearts" width="64" height="64" patternUnits="userSpaceOnUse">'
        f'<path d="{HEART}" fill="{PINK}" transform="translate(16 18) scale(.7)"/>'
        f'<path d="{HEART}" fill="{PINK}" transform="translate(48 50) scale(.5)"/></pattern>'
    )


def pill(x: float, y: float, label: str) -> tuple[str, float]:
    width = len(label) * 8 + 28
    svg = (
        f'<rect x="{x}" y="{y}" width="{width}" height="30" rx="15" fill="#fff" stroke="{INK}" stroke-width="2"/>'
        f'<text x="{x + width / 2}" y="{y + 20}" text-anchor="middle" font-size="14" font-weight="600" fill="{INK}">'
        f"{escape(label)}</text>"
    )
    return svg, width


def svg_open(width: int, height: int) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'width="{width}" height="{height}" viewBox="0 0 {width} {height}" font-family="{FONT}">'
    )


def build_header() -> str:
    w, h = 1000, 380
    char_h = 300
    char_w = char_h * CHARACTER_SIZE[0] / CHARACTER_SIZE[1]
    char_x, char_y = 675, h - char_h

    pills, x = "", 44
    for label in ["soc", "dfir", "threat intel", "mcp", "freebsd", "pentest"]:
        svg, width = pill(x, 318, label)
        pills += svg
        x += width + 10

    return f'''{svg_open(w, h)}
<defs>
  {heart_pattern()}
  <clipPath id="card"><rect x="6" y="6" width="{w - 12}" height="{h - 12}" rx="28"/></clipPath>
</defs>
<g clip-path="url(#card)">
  <rect width="{w}" height="{h}" fill="{PAPER}"/>
  <rect width="{w}" height="{h}" fill="url(#hearts)"/>

  <text x="44" y="66" font-size="19" font-weight="700" fill="{INK}">gabriel silva coelho <tspan fill="{SOFT_INK}" font-weight="500">· bunnyiesart</tspan></text>
  {blush_mark(372, 54)}

  <path d="M600 196 L688 238 L596 226 Z" fill="#fff" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>
  <rect x="40" y="92" width="580" height="160" rx="32" fill="#fff" stroke="{INK}" stroke-width="3"/>
  <path d="M603 199 L680 236 L599 223 Z" fill="#fff"/>
  <text font-size="38" font-weight="800" fill="{INK}">
    <tspan x="76" y="160">you like reading my code,</tspan>
    <tspan x="76" y="212">don't you?</tspan>
  </text>

  <text x="44" y="294" font-size="17" fill="{SOFT_INK}">cybersecurity analyst @ BSDTrust · blue team · mcp developer</text>
  {pills}

  <image x="{char_x}" y="{char_y}" width="{char_w:.1f}" height="{char_h}" href="{character_href()}">
    <animateTransform attributeName="transform" type="translate" values="0 6;0 0;0 6" dur="3s" repeatCount="indefinite"/>
  </image>
  {floating_hearts([(700, 150, 1, 0), (955, 130, .8, 1.3), (930, 210, 1.1, 2.6), (720, 240, .7, 3.4)])}
</g>
<rect x="6" y="6" width="{w - 12}" height="{h - 12}" rx="28" fill="none" stroke="{INK}" stroke-width="3"/>
</svg>
'''


PROJECTS = [
    ("Gatte", "Go",
     "self-hosted MCP gateway: one authenticated endpoint for many MCP servers, with per-analyst audit and tool quarantine."),
    ("swiss", "Python",
     "threat intel over MCP. one IOC in, 20+ sources out: VirusTotal, AbuseIPDB, GreyNoise, Shodan, MISP and more."),
    ("mcp-iris", "Python",
     "read-only MCP server for the DFIR-IRIS incident response platform, with hard limits the LLM cannot bypass."),
    ("mcp-opensearch", "Python",
     "read-only OpenSearch / SIEM MCP server: search, aggregations, PPL and time-window diffs. writes are blocked."),
    ("bluearmory", "Python",
     "blue team MCP collection: SOC servers plus Claude Code skills for IOC triage and incident reports."),
    ("Fursec", "HTML",
     "free cybersecurity learning path: ~200 courses in PT-BR and EN, 33 portfolio projects, books and a study method."),
]


def build_card(name: str, lang: str, desc: str) -> str:
    w, h = 460, 214
    top, bottom, left, right, r = 42, 208, 6, 454, 22
    # One outline for card and ears, so the ears grow out of the card like a head.
    outline = (
        f"M{left + r} {top} L40 {top} L54 8 L102 {top} L128 {top} L176 8 L190 {top} "
        f"L{right - r} {top} Q{right} {top} {right} {top + r} L{right} {bottom - r} "
        f"Q{right} {bottom} {right - r} {bottom} L{left + r} {bottom} Q{left} {bottom} {left} {bottom - r} "
        f"L{left} {top + r} Q{left} {top} {left + r} {top} Z"
    )
    lines = textwrap.wrap(desc, 52)
    desc_svg = "".join(f'<tspan x="30" dy="{0 if i == 0 else 22}">{escape(line)}</tspan>' for i, line in enumerate(lines))
    return f'''{svg_open(w, h)}
<path d="{outline}" fill="#fff" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>
<text x="30" y="88" font-size="23" font-weight="800" fill="{INK}">{escape(name)}</text>
{blush_mark(396, 72)}{blush_mark(414, 72)}
<text y="122" font-size="15" fill="{SOFT_INK}">{desc_svg}</text>
<circle cx="36" cy="187" r="5" fill="{INK}"/>
<text x="48" y="192" font-size="14" font-weight="600" fill="{SOFT_INK}">{lang}</text>
</svg>
'''


def build_footer() -> str:
    w, h = 1000, 220
    char_h = 190
    char_w = char_h * CHARACTER_SIZE[0] / CHARACTER_SIZE[1]
    return f'''{svg_open(w, h)}
<text x="{w / 2}" y="46" text-anchor="middle" font-size="22" font-weight="800" fill="#888">thanks for stopping by, have a nice day :3</text>
<image x="{(w - char_w) / 2:.1f}" y="{h - 118}" width="{char_w:.1f}" height="{char_h}" href="{character_href()}">
  <animateTransform attributeName="transform" type="translate" values="0 18;0 0;0 0;0 18" keyTimes="0;.2;.8;1" dur="5s" repeatCount="indefinite"/>
</image>
{floating_hearts([(420, 170, .9, 0), (580, 160, 1, 1.5), (450, 120, .6, 2.8)])}
</svg>
'''


def main() -> None:
    for old in ASSETS.rglob("*.svg"):
        old.unlink()
    (ASSETS / "cards").mkdir(parents=True, exist_ok=True)
    (ASSETS / "header.svg").write_text(build_header(), encoding="utf-8")
    (ASSETS / "footer.svg").write_text(build_footer(), encoding="utf-8")
    for name, lang, desc in PROJECTS:
        (ASSETS / "cards" / f"{name.lower()}.svg").write_text(build_card(name, lang, desc), encoding="utf-8")


if __name__ == "__main__":
    main()
