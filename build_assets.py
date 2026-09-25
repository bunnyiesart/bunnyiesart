"""Generate the animated SVG assets used by the profile README."""

import math
import textwrap
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).parent / "assets"
MONO = "'JetBrains Mono','Fira Code','SFMono-Regular',Menlo,Consolas,monospace"

CYAN = "#00e5ff"
VIOLET = "#7c5cff"
PINK = "#ff3d8b"
LIME = "#39d353"
TEXT = "#c9d4e5"
MUTED = "#6b7a90"


def typing_values(full_width: float, chars: int) -> str:
    """Discrete widths that reveal text one character at a time, hold, then reset."""
    step = full_width / chars
    typed = [f"{i * step:.1f}" for i in range(chars + 1)]
    hold = [typed[-1]] * 25
    return ";".join(typed + hold + ["0"])


def pill(x: float, y: float, label: str, color: str) -> tuple[str, float]:
    width = len(label) * 8.4 + 26
    svg = (
        f'<rect x="{x}" y="{y}" width="{width}" height="28" rx="14" '
        f'fill="{color}" fill-opacity=".08" stroke="{color}" stroke-opacity=".55"/>'
        f'<text x="{x + width / 2}" y="{y + 19}" text-anchor="middle" '
        f'class="mono" font-size="14" fill="{color}">{escape(label)}</text>'
    )
    return svg, width


def build_header() -> str:
    cx, cy, r = 1010, 160, 118

    def polar(angle_deg: float, radius: float) -> tuple[float, float]:
        a = math.radians(angle_deg)
        return cx + radius * math.sin(a), cy - radius * math.cos(a)

    edge_x, edge_y = polar(50, r)
    blips = [(35, 70, "C2", PINK, 0.4), (140, 95, "phish", "#ffb020", 1.6),
             (230, 55, "brute", PINK, 2.7), (300, 100, "beacon", CYAN, 3.5)]
    blip_svg = ""
    for angle, dist, label, color, delay in blips:
        bx, by = polar(angle, dist)
        blip_svg += (
            f'<circle cx="{bx:.1f}" cy="{by:.1f}" r="4" fill="{color}">'
            f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.05;.6;1" '
            f'dur="4s" begin="{delay}s" repeatCount="indefinite"/></circle>'
            f'<circle cx="{bx:.1f}" cy="{by:.1f}" r="4" fill="none" stroke="{color}">'
            f'<animate attributeName="r" values="4;20" dur="4s" begin="{delay}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0;.9;0;0" keyTimes="0;.05;.5;1" '
            f'dur="4s" begin="{delay}s" repeatCount="indefinite"/></circle>'
            f'<text x="{bx + 9:.1f}" y="{by - 8:.1f}" class="mono" font-size="11" fill="{color}" opacity="0">'
            f'{label}<animate attributeName="opacity" values="0;.9;.9;0" keyTimes="0;.05;.6;1" '
            f'dur="4s" begin="{delay}s" repeatCount="indefinite"/></text>'
        )

    typed = "$ transformando vulnerabilidades em código"
    typed_width = len(typed) * 10.8
    values = typing_values(typed_width, len(typed))
    frames = values.count(";") + 1
    duration = frames * 0.07
    cursor_values = ";".join(f"{68 + float(w):.1f}" for w in values.split(";"))

    pills, x = "", 64
    for label, color in [("SOC", CYAN), ("DFIR", VIOLET), ("Threat Intel", PINK),
                         ("MCP", LIME), ("FreeBSD", "#ff5f56"), ("Pentest", "#ffb020")]:
        svg, width = pill(x, 262, label, color)
        pills += svg
        x += width + 10

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="320" viewBox="0 0 1200 320">
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#06080d"/><stop offset="1" stop-color="#0d1422"/>
  </linearGradient>
  <radialGradient id="glowR" cx=".84" cy=".5" r=".45">
    <stop offset="0" stop-color="{CYAN}" stop-opacity=".16"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="glowL" cx=".05" cy="0" r=".7">
    <stop offset="0" stop-color="{VIOLET}" stop-opacity=".22"/><stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/>
  </radialGradient>
  <pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse">
    <path d="M32 0H0V32" fill="none" stroke="#16202f" stroke-width="1"/>
  </pattern>
  <linearGradient id="name" x1="0" x2="1">
    <stop offset="0" stop-color="{CYAN}"/><stop offset=".55" stop-color="{VIOLET}"/><stop offset="1" stop-color="{PINK}"/>
  </linearGradient>
  <linearGradient id="border" x1="0" x2="1">
    <stop offset="0" stop-color="{CYAN}" stop-opacity=".7"/><stop offset=".5" stop-color="{VIOLET}" stop-opacity=".25"/>
    <stop offset="1" stop-color="{PINK}" stop-opacity=".7"/>
  </linearGradient>
  <linearGradient id="scan" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{CYAN}" stop-opacity="0"/><stop offset=".5" stop-color="{CYAN}" stop-opacity=".07"/>
    <stop offset="1" stop-color="{CYAN}" stop-opacity="0"/>
  </linearGradient>
  <linearGradient id="sweep" x1="0" y1="1" x2="1" y2="0">
    <stop offset="0" stop-color="{CYAN}" stop-opacity="0"/><stop offset="1" stop-color="{CYAN}" stop-opacity=".35"/>
  </linearGradient>
  <clipPath id="frame"><rect width="1200" height="320" rx="18"/></clipPath>
  <clipPath id="typing"><rect x="64" y="210" height="36" width="0">
    <animate attributeName="width" values="{values}" dur="{duration:.2f}s" calcMode="discrete" repeatCount="indefinite"/>
  </rect></clipPath>
</defs>
<style>
  .mono {{ font-family: {MONO}; }}
  .glitch-a {{ animation: ga 5s infinite steps(1); }}
  .glitch-b {{ animation: gb 5s infinite steps(1); }}
  @keyframes ga {{ 0%,88%,100% {{ transform: translate(0,0); opacity: 0; }}
                  89% {{ transform: translate(-5px,2px); opacity: .8; }}
                  91% {{ transform: translate(4px,-1px); opacity: .8; }}
                  93% {{ transform: translate(-2px,0); opacity: .8; }} }}
  @keyframes gb {{ 0%,88%,100% {{ transform: translate(0,0); opacity: 0; }}
                  89% {{ transform: translate(5px,-2px); opacity: .8; }}
                  91% {{ transform: translate(-3px,2px); opacity: .8; }}
                  93% {{ transform: translate(2px,1px); opacity: .8; }} }}
  .blink {{ animation: blink 1s infinite steps(1); }}
  @keyframes blink {{ 50% {{ opacity: 0; }} }}
</style>
<g clip-path="url(#frame)">
  <rect width="1200" height="320" fill="url(#bg)"/>
  <rect width="1200" height="320" fill="url(#grid)"/>
  <rect width="1200" height="320" fill="url(#glowL)"/>
  <rect width="1200" height="320" fill="url(#glowR)"/>

  <text x="64" y="74" class="mono" font-size="15" fill="{MUTED}">
    <tspan fill="{LIME}">●</tspan> root@bsdtrust<tspan fill="{MUTED}">:</tspan><tspan fill="{CYAN}">~/bunnyiesart</tspan> <tspan fill="{MUTED}">[ blue team mode ]</tspan>
  </text>

  <g class="mono" font-size="62" font-weight="800" letter-spacing="2">
    <text x="64" y="148" fill="{CYAN}" class="glitch-a">GABRIEL COELHO</text>
    <text x="64" y="148" fill="{PINK}" class="glitch-b">GABRIEL COELHO</text>
    <text x="64" y="148" fill="url(#name)">GABRIEL COELHO</text>
  </g>
  <text x="64" y="188" class="mono" font-size="19" fill="{TEXT}">Cybersecurity Analyst · Blue Team · MCP Developer</text>

  <g clip-path="url(#typing)">
    <text x="64" y="234" class="mono" font-size="18" fill="{LIME}">{escape(typed)}</text>
  </g>
  <rect x="68" y="219" width="10" height="20" fill="{LIME}" class="blink">
    <animate attributeName="x" values="{cursor_values}" dur="{duration:.2f}s" calcMode="discrete" repeatCount="indefinite"/>
  </rect>

  {pills}

  <g stroke="{CYAN}" fill="none">
    <circle cx="{cx}" cy="{cy}" r="{r}" stroke-opacity=".45"/>
    <circle cx="{cx}" cy="{cy}" r="{r * 2 / 3:.1f}" stroke-opacity=".25"/>
    <circle cx="{cx}" cy="{cy}" r="{r / 3:.1f}" stroke-opacity=".2"/>
    <path d="M{cx - r} {cy}H{cx + r}M{cx} {cy - r}V{cy + r}" stroke-opacity=".15"/>
  </g>
  <g>
    <path d="M{cx} {cy}L{cx} {cy - r}A{r} {r} 0 0 1 {edge_x:.1f} {edge_y:.1f}Z" fill="url(#sweep)"/>
    <line x1="{cx}" y1="{cy}" x2="{edge_x:.1f}" y2="{edge_y:.1f}" stroke="{CYAN}" stroke-width="2"/>
    <animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" dur="4s" repeatCount="indefinite"/>
  </g>
  {blip_svg}
  <circle cx="{cx}" cy="{cy}" r="4" fill="{CYAN}"/>
  <text x="{cx}" y="{cy + r + 26}" text-anchor="middle" class="mono" font-size="12" fill="{MUTED}">threat radar · live</text>

  <rect y="-60" width="1200" height="60" fill="url(#scan)">
    <animateTransform attributeName="transform" type="translate" from="0 0" to="0 380" dur="6s" repeatCount="indefinite"/>
  </rect>
</g>
<rect x=".5" y=".5" width="1199" height="319" rx="18" fill="none" stroke="url(#border)"/>
</svg>
'''


def build_footer() -> str:
    # ECG-style trace: flat, spike, flat — "monitoring" heartbeat.
    points, x = [], 0
    while x <= 1200:
        points += [(x, 60), (x + 60, 60), (x + 70, 50), (x + 80, 60), (x + 92, 60),
                   (x + 100, 18), (x + 110, 96), (x + 120, 60), (x + 140, 60), (x + 152, 46), (x + 166, 60), (x + 240, 60)]
        x += 240
    path = "M" + " L".join(f"{px} {py}" for px, py in points)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="150" viewBox="0 0 1200 150">
<defs>
  <linearGradient id="trace" x1="0" x2="1">
    <stop offset="0" stop-color="{CYAN}"/><stop offset=".5" stop-color="{VIOLET}"/><stop offset="1" stop-color="{PINK}"/>
  </linearGradient>
  <linearGradient id="fade" x1="0" x2="1">
    <stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".15" stop-color="#fff"/>
    <stop offset=".85" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/>
  </linearGradient>
  <mask id="edges"><rect width="1200" height="120" fill="url(#fade)"/></mask>
</defs>
<style>
  .mono {{ font-family: {MONO}; }}
  .blink {{ animation: blink 1.2s infinite steps(1); }}
  @keyframes blink {{ 50% {{ opacity: 0; }} }}
</style>
<g mask="url(#edges)">
  <path d="{path}" fill="none" stroke="url(#trace)" stroke-opacity=".18" stroke-width="2"/>
  <path d="{path}" fill="none" stroke="url(#trace)" stroke-width="2.5" stroke-linejoin="round"
        stroke-dasharray="260 2400" filter="drop-shadow(0 0 4px {CYAN})">
    <animate attributeName="stroke-dashoffset" from="2660" to="0" dur="4s" repeatCount="indefinite"/>
  </path>
</g>
<text x="600" y="138" text-anchor="middle" class="mono" font-size="15" fill="{MUTED}">
  <tspan fill="{LIME}" class="blink">●</tspan> monitoring... all systems nominal <tspan fill="{CYAN}">// stay paranoid, patch often</tspan>
</text>
</svg>
'''


PROJECTS = [
    ("Gatte", "🛰️", "Go", "#00ADD8", CYAN,
     "Self-hosted MCP gateway: one authenticated endpoint for many MCP servers, with per-analyst audit and tool quarantine."),
    ("swiss", "🔪", "Python", "#3572A5", PINK,
     "Threat intel Swiss army knife over MCP. One IOC in, 20+ sources out: VirusTotal, AbuseIPDB, GreyNoise, Shodan, MISP and more."),
    ("mcp-iris", "🧬", "Python", "#3572A5", VIOLET,
     "Read-only MCP server for the DFIR-IRIS incident response platform. Hardened server-side limits the LLM cannot bypass."),
    ("mcp-opensearch", "🔎", "Python", "#3572A5", "#ffb020",
     "Read-only OpenSearch / SIEM MCP server: search, aggregations, PPL and time-window diffs, with write operations fully blocked."),
    ("bluearmory", "🛡️", "Python", "#3572A5", LIME,
     "Blue team MCP collection: SOC servers, Claude Code skills for IOC triage and incident reports, all in one catalog."),
    ("Fursec", "📚", "HTML", "#e34c26", "#ff5f56",
     "Free cybersecurity learning path: ~200 courses (PT-BR & EN), 33 portfolio projects, ~60 repos, books and a study method."),
]


def build_card(name: str, icon: str, lang: str, lang_color: str, accent: str, desc: str) -> str:
    lines = textwrap.wrap(desc, 50)
    desc_svg = "".join(
        f'<tspan x="28" dy="{0 if i == 0 else 19}">{escape(line)}</tspan>' for i, line in enumerate(lines)
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="460" height="170" viewBox="0 0 460 170">
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#0b111b"/><stop offset="1" stop-color="#0f1726"/>
  </linearGradient>
  <radialGradient id="glow" cx="1" cy="0" r=".9">
    <stop offset="0" stop-color="{accent}" stop-opacity=".22"/><stop offset="1" stop-color="{accent}" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="shine" x1="0" x2="1">
    <stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".06"/>
    <stop offset="1" stop-color="#fff" stop-opacity="0"/>
  </linearGradient>
  <clipPath id="c"><rect width="460" height="170" rx="14"/></clipPath>
</defs>
<style>.mono {{ font-family: {MONO}; }}</style>
<g clip-path="url(#c)">
  <rect width="460" height="170" fill="url(#bg)"/>
  <rect width="460" height="170" fill="url(#glow)"/>
  <rect width="4" height="170" fill="{accent}"/>
  <rect x="-200" width="120" height="170" fill="url(#shine)" transform="skewX(-20)">
    <animate attributeName="x" values="-200;700;700" keyTimes="0;.3;1" dur="6s" repeatCount="indefinite"/>
  </rect>
  <text x="28" y="46" font-size="22">{icon}</text>
  <text x="62" y="45" class="mono" font-size="21" font-weight="700" fill="#e6edf7">{escape(name)}</text>
  <text x="432" y="44" text-anchor="end" class="mono" font-size="13" fill="{accent}">↗</text>
  <text y="78" class="mono" font-size="12.5" fill="#9fb0c6">{desc_svg}</text>
  <circle cx="34" cy="148" r="6" fill="{lang_color}"/>
  <text x="48" y="153" class="mono" font-size="13" fill="#8b9bb0">{lang}</text>
</g>
<rect x=".5" y=".5" width="459" height="169" rx="14" fill="none" stroke="{accent}" stroke-opacity=".35"/>
</svg>
'''


def main() -> None:
    (ROOT / "header.svg").write_text(build_header(), encoding="utf-8")
    (ROOT / "footer.svg").write_text(build_footer(), encoding="utf-8")
    for project in PROJECTS:
        (ROOT / "cards" / f"{project[0].lower()}.svg").write_text(build_card(*project), encoding="utf-8")


if __name__ == "__main__":
    main()
