#!/usr/bin/env python3
import os


def generate_info_card(output_path):
    width = 490
    height = 550

    data = [
        ("OS", "Ubuntu / Linux"),
        ("Host", "GitHub"),
        ("Role", "Backend / Full Stack Developer"),
        ("Experience", "~10 Months"),
        ("Location", "Feni, Chittagong, Bangladesh"),
        ("", ""),
        ("Backend", "Node.js · Express · NestJS · FastAPI"),
        ("Frontend", "React · Next.js · TypeScript"),
        ("Database", "PostgreSQL · MongoDB · MySQL"),
        ("DevOps", "Docker · GitHub · Vercel"),
        ("", ""),
        ("Portfolio", "furqan-ahmad.vercel.app"),
        ("GitHub", "github.com/furqanRupom"),
        ("LinkedIn", "linkedin.com/in/furqan-ahmad-rupom"),
    ]

    svg_header = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
    <defs>
        <style>
            .bg {{ fill: #0a0f0d; rx: 12px; stroke: #1a2a2a; stroke-width: 2px; }}
            .text {{ font-family: "Courier New", Consolas, monospace; font-size: 14px; }}
            .label {{ fill: #00FFD1; font-weight: bold; }}
            .value {{ fill: #C0C0C0; }}
            .title {{ fill: #E0E0E0; font-weight: bold; font-size: 16px; text-anchor: middle; }}
            .line {{ stroke: #1a2a2a; stroke-width: 1px; }}

            .row {{ opacity: 0; animation: fadeIn 0.5s forwards; }}
            @keyframes fadeIn {{
                to {{ opacity: 1; }}
            }}
'''

    styles = []
    anim_index = 0
    for i, (label, val) in enumerate(data):
        if label or val:
            delay = anim_index * 0.15
            styles.append(
                f"            .r{anim_index} {{ animation-delay: {delay}s; }}"
            )
            anim_index += 1

    svg_header += "\n".join(styles)
    svg_header += """
        </style>
    </defs>
    <rect class="bg" width="100%" height="100%" />

    <!-- Header -->
    <g transform="translate(15, 20)">
        <circle cx="0" cy="0" r="6" fill="#FF5F56" />
        <circle cx="20" cy="0" r="6" fill="#FFBD2E" />
        <circle cx="40" cy="0" r="6" fill="#27C93F" />
    </g>
    <text x="245" y="25" class="text title">The Cipher Stack</text>
    <line x1="0" y1="40" x2="490" y2="40" class="line" />

    <g transform="translate(30, 80)">
"""

    svg_lines = []
    y_pos = 0
    anim_index = 0
    for label, val in data:
        if label or val:
            svg_lines.append(f'        <g class="row r{anim_index}">')
            svg_lines.append(
                f'            <text x="0" y="{y_pos}" class="text label">{label}</text>'
            )
            svg_lines.append(
                f'            <text x="120" y="{y_pos}" class="text value">{val}</text>'
            )
            svg_lines.append("        </g>")
            anim_index += 1
            y_pos += 30
        else:
            y_pos += 15  # separator space

    svg_footer = """
    </g>
</svg>"""

    with open(output_path, "w") as f:
        f.write(svg_header + "\n".join(svg_lines) + svg_footer)


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_path = os.path.join(base_dir, "info-card.svg")
    generate_info_card(output_path)
    print(f"Success! Generated {output_path}")
