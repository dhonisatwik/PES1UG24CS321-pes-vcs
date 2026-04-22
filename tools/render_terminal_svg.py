#!/usr/bin/env python3

import html
import pathlib
import sys


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: render_terminal_svg.py <input.txt> <output.svg>", file=sys.stderr)
        return 1

    input_path = pathlib.Path(sys.argv[1])
    output_path = pathlib.Path(sys.argv[2])
    text = input_path.read_text(encoding="utf-8")
    lines = text.splitlines() or [""]

    char_width = 9
    line_height = 22
    padding_x = 24
    padding_y = 56
    header_h = 34
    width = max(900, max(len(line) for line in lines) * char_width + padding_x * 2)
    height = max(240, len(lines) * line_height + padding_y * 2)

    escaped_lines = []
    y = padding_y
    for line in lines:
        escaped = html.escape(line)
        escaped_lines.append(
            f'<text x="{padding_x}" y="{y}" fill="#d6deeb">{escaped}</text>'
        )
        y += line_height

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <rect width="{width}" height="{height}" rx="16" fill="#0f172a"/>
  <rect x="0" y="0" width="{width}" height="{header_h}" rx="16" fill="#111827"/>
  <rect x="0" y="{header_h}" width="{width}" height="{height - header_h}" fill="#0f172a"/>
  <circle cx="24" cy="17" r="6" fill="#f87171"/>
  <circle cx="44" cy="17" r="6" fill="#fbbf24"/>
  <circle cx="64" cy="17" r="6" fill="#34d399"/>
  <text x="90" y="22" fill="#94a3b8" font-family="Menlo, Monaco, Consolas, monospace" font-size="14">terminal capture</text>
  <g font-family="Menlo, Monaco, Consolas, monospace" font-size="16">
    {' '.join(escaped_lines)}
  </g>
</svg>
"""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(svg, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
