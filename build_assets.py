"""Generate the FreeBSD-console SVG assets used by the profile README.

Each screen is written as 80-column text with inline color markup:
  {w} bright white   {r} FreeBSD red   {u} underlined   {/} back to console gray
"""

import re
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).parent / "assets"

FONT = "'DejaVu Sans Mono','Menlo','Consolas','Liberation Mono',monospace"
FONT_SIZE = 16
CHAR_W = 9.63
LINE_H = 20
PAD = 24

BG = "#000000"
GRAY = "#aaaaaa"
WHITE = "#ffffff"
RED = "#d0282a"

STYLES = {
    "w": f'fill="{WHITE}" font-weight="bold"',
    "r": f'fill="{RED}"',
    "u": f'fill="{GRAY}" text-decoration="underline"',
}

TOKEN = re.compile(r"\{([wru/])\}")


def render_line(line: str) -> str:
    """Turn one marked-up line into tspans."""
    parts, style = [], None
    for i, chunk in enumerate(TOKEN.split(line)):
        if i % 2:
            style = None if chunk == "/" else chunk
        elif chunk:
            attrs = f" {STYLES[style]}" if style else ""
            parts.append(f"<tspan{attrs}>{escape(chunk)}</tspan>")
    return "".join(parts)


def screen(rows: list[str], extra: str = "", cols: int = 80) -> str:
    width = round(cols * CHAR_W + 2 * PAD)
    height = len(rows) * LINE_H + 2 * PAD
    body = "\n".join(
        f'<text x="{PAD}" y="{PAD + (i + 1) * LINE_H - 5}">{render_line(row)}</text>'
        for i, row in enumerate(rows)
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<style>
  text {{ font-family: {FONT}; font-size: {FONT_SIZE}px; fill: {GRAY}; white-space: pre; }}
  .blink {{ animation: blink 1s steps(1) infinite; }}
  @keyframes blink {{ 50% {{ opacity: 0; }} }}
</style>
<rect width="{width}" height="{height}" fill="{BG}"/>
<g xml:space="preserve">
{body}
</g>
{extra}
</svg>
'''


def cursor(col: int, row: int) -> str:
    x = PAD + col * CHAR_W
    y = PAD + row * LINE_H + LINE_H - 7
    return f'<rect class="blink" x="{x:.1f}" y="{y}" width="{CHAR_W:.1f}" height="3" fill="{GRAY}"/>'


# --- loader ---------------------------------------------------------------

WORDMARK = [
    r" ______               ____   _____ _____  ",
    r"|  ____|             |  _ \ / ____|  __ \ ",
    r"| |___ _ __ ___  ___ | |_) | (___ | |  | |",
    r"|  ___| '__/ _ \/ _ \|  _ < \___ \| |  | |",
    r"| |   | | |  __/  __/| |_) |____) | |__| |",
    r"| |   | | |    |    ||     |      |      |",
    r"|_|   |_|  \___|\___||____/|_____/|_____/ ",
]

ORB = [
    r"  ```                        `",
    r" s` `.....---.......--.```   -/",
    r" +o   .--`         /y:`      +.",
    r"  yo`:.            :o      `+-",
    r"   y/               -/`   -o/",
    r"  .-                  ::/sy+:.",
    r"  /                     `--  /",
    r" `:                          :`",
    r" `:                          :`",
    r"  /                          /",
    r"  .-                        -.",
    r"   --                      -.",
    r"    `:`                  `:`",
    r"      .--             `--.",
    r"         .---.....----.",
]

MENU = [
    "{w}1.{/} Boot {w}B{/}lue Team {w}[Enter]{/}",
    "{w}2.{/} Boot {w}P{/}entest (single user)",
    "{w}3.{/} {w}E{/}scape to loader prompt",
    "{w}4.{/} {w}R{/}eboot",
    "{w}5.{/} {w}C{/}ons: Video",
    "",
    "Options:",
    "{w}6.{/} {w}K{/}ernel: soc/kernel (1 of 3)",
    "{w}7.{/} Boot Environments",
    "{w}8.{/} Boot {w}O{/}ptions",
]

BOX_W = 46


def visible_len(line: str) -> int:
    return len(TOKEN.sub("", line))


def build_loader() -> str:
    title = " Welcome to bunnyiesart "
    side = (BOX_W - 2 - len(title)) // 2
    top = "┌" + "─" * side + title + "─" * (BOX_W - 2 - side - len(title)) + "┐"
    box = [top, "│" + " " * (BOX_W - 2) + "│"]
    for item in MENU:
        box.append("│  " + item + " " * (BOX_W - 4 - visible_len(item)) + "│")
    box += ["│" + " " * (BOX_W - 2) + "│"] * 2
    box.append("└" + "─" * (BOX_W - 2) + "┘")

    rows = [""] * 25
    for i, line in enumerate(WORDMARK):
        rows[1 + i] = "{r}" + line + "{/}"
    box_top, orb_top = 9, 9
    for i in range(25):
        left = box[i - box_top] if 0 <= i - box_top < len(box) else ""
        orb = ORB[i - orb_top] if 0 <= i - orb_top < len(ORB) else ""
        base = rows[i] or left
        if orb:
            base += " " * (BOX_W + 2 - visible_len(base)) + "{r}" + orb + "{/}"
        rows[i] = base

    # Countdown: one digit per second, 10 → 1, then loop.
    countdown_row = 24
    rows[countdown_row] = "   Autoboot in    seconds. [Space] to pause"
    digit_x = PAD + 17 * CHAR_W
    digit_y = PAD + (countdown_row + 1) * LINE_H - 5
    total = 10
    digits = ""
    for n in range(total, 0, -1):
        start = (total - n) / total
        end = (total - n + 1) / total
        values, times = ("1;0", f"0;{end:.2f}") if start == 0 else ("0;1;0", f"0;{start:.2f};{end:.2f}")
        if end == 1:
            values, times = "0;1", f"0;{start:.2f}"
        digits += (
            f'<text x="{digit_x:.1f}" y="{digit_y}" text-anchor="end" fill="{WHITE}" font-weight="bold">{n}'
            f'<animate attributeName="opacity" values="{values}" keyTimes="{times}" '
            f'dur="{total}s" calcMode="discrete" repeatCount="indefinite"/></text>'
        )
    return screen(rows, digits)


# --- boot + login -----------------------------------------------------------

BOOT = [
    "---<<BOOT>>---",
    "Copyright (c) 1992-2026 The FreeBSD Project.",
    "FreeBSD 14.3-RELEASE bunnyiesart #0: Thu Sep 25 2026",
    "    gabriel@bunnyiesart:/usr/obj/usr/src/amd64.amd64/sys/SOC amd64",
    "CPU: Gabriel Silva Coelho (Cybersecurity Analyst @ BSDTrust)",
    "  Origin=\"Brasil\"  Lang=pt_BR.UTF-8,en_US.UTF-8",
    "blueteam0: <Security Operations Center> on nexus0",
    "dfir0: <Incident response, DFIR-IRIS> on blueteam0",
    "ti0: <Threat intelligence, 20+ sources> on blueteam0",
    "siem0: <Wazuh / Graylog / OpenSearch> on blueteam0",
    "pentest0: <Blackbox and web application security> port 443",
    "gatte0: <MCP gateway, audit, tool quarantine> on mcpbus0",
    "Trying to mount root from zfs:zroot/ROOT/default []...",
    "Starting sshd.",
    "Starting coffee.",
    "",
    "FreeBSD/amd64 (bunnyiesart) (ttyv0)",
    "",
    "login: gabriel",
    "Password:",
    "Last login: Thu Sep 25 03:14:07 on ttyv0",
    "gabriel@bunnyiesart:~ % {w}man bunnyiesart{/}",
]


def build_boot() -> str:
    rows = BOOT
    step, hold = 0.22, 8.0
    total = len(rows) * step + hold
    height = len(rows) * LINE_H + 2 * PAD
    width = round(80 * CHAR_W + 2 * PAD)
    lines = ""
    for i, row in enumerate(rows):
        begin = i * step / total
        lines += (
            f'<text x="{PAD}" y="{PAD + (i + 1) * LINE_H - 5}" opacity="0">{render_line(row)}'
            f'<animate attributeName="opacity" values="0;1" keyTimes="0;{begin:.3f}" '
            f'dur="{total:.2f}s" calcMode="discrete" repeatCount="indefinite"/></text>\n'
        )
    last = len(rows) - 1
    blink = cursor(visible_len(rows[last]) + 1, last)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<style>
  text {{ font-family: {FONT}; font-size: {FONT_SIZE}px; fill: {GRAY}; white-space: pre; }}
  .blink {{ animation: blink 1s steps(1) infinite; }}
  @keyframes blink {{ 50% {{ opacity: 0; }} }}
</style>
<rect width="{width}" height="{height}" fill="{BG}"/>
<g xml:space="preserve">
{lines}</g>
{blink}
</svg>
'''


# --- man page ---------------------------------------------------------------

MAN = [
    "BUNNYIESART(7)     FreeBSD Miscellaneous Information Manual     BUNNYIESART(7)",
    "",
    "{w}NAME{/}",
    "     {w}bunnyiesart{/} – Gabriel Silva Coelho, cybersecurity analyst",
    "",
    "{w}SYNOPSIS{/}",
    "     {w}bunnyiesart{/} [{w}-bdp{/}] [{w}-f{/} {u}focus{/}] [{w}--mcp{/} {u}server ...{/}]",
    "",
    "{w}DESCRIPTION{/}",
    "     {w}bunnyiesart{/} is a blue team analyst at BSDTrust, Brazil.  Works SOC and",
    "     incident response, and writes the tooling that makes that work faster.",
    "",
    "     The options are as follows:",
    "",
    "     {w}-b{/}      Blue team: SOC, DFIR, threat intel, detection engineering.",
    "",
    "     {w}-d{/}      Develop MCP servers that give AI assistants access to real SOC",
    "             tooling.  Read-only by default, audited, hardened server-side.",
    "",
    "     {w}-p{/}      Pentest: blackbox and web application security.",
    "",
    "     {w}-f{/} {u}focus{/}",
    "             FreeBSD, kernel hardening, self-hosting.",
    "",
    "{w}IMPLEMENTATION NOTES{/}",
    "           analyst + claude",
    "                  |",
    "               {w}gatte{/}(8)          one endpoint, per-analyst audit",
    "                  |",
    "       +----------+----------------+----------------+",
    "       |          |                |                |",
    "    {w}swiss{/}(1)  {w}mcp-iris{/}(8)  {w}mcp-opensearch{/}(8)  {w}bluearmory{/}(7)",
    "    threat     DFIR-IRIS      SIEM search         graylog + skills",
    "    intel      cases",
    "",
    "{w}ENVIRONMENT{/}",
    "     {w}STACK{/}   Python, Go, JavaScript/TypeScript, Docker, sh(1)",
    "     {w}TOOLS{/}   Wazuh, Graylog, OpenSearch, DFIR-IRIS, MISP, Burp Suite",
    "     {w}LANG{/}    pt_BR.UTF-8, en_US.UTF-8",
    "",
    "{w}SEE ALSO{/}",
    "     {w}gatte{/}(8), {w}swiss{/}(1), {w}mcp-iris{/}(8), {w}mcp-opensearch{/}(8), {w}bluearmory{/}(7),",
    "     {w}fursec{/}(7)",
    "",
    "{w}BUGS{/}",
    "     Transforma vulnerabilidades em código.  Not a bug, a feature.",
    "",
    "FreeBSD 14.3                  September 25, 2026                  FreeBSD 14.3",
]


def main() -> None:
    for old in ROOT.rglob("*.svg"):
        old.unlink()
    (ROOT / "loader.svg").write_text(build_loader(), encoding="utf-8")
    (ROOT / "boot.svg").write_text(build_boot(), encoding="utf-8")
    (ROOT / "man.svg").write_text(screen(MAN), encoding="utf-8")


if __name__ == "__main__":
    main()
