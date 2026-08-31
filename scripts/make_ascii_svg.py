#!/usr/bin/env python3
"""Generate an animated 'dev sign' character SVG in Dark Neon Teal.

This replaces the old photo-to-ASCII pipeline (image_to_ascii) with a
drawn coder-mascot + hanging sign, while keeping the same card shell as
info-card.svg: 370x550, dark terminal card, glow filter, traffic-light
header dots, and the "furqanRupom.sh" title.

No input photo is required.

Produces: hxni-devsign.svg (in project root)
"""

import os

WIDTH = 370
HEIGHT = 550
TITLE = "furqanRupom.sh"
ACCENT = "#00FFD1"


def build_svg():
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" width="{WIDTH}" height="{HEIGHT}">
    <defs>
        <filter id="glow" x="-40%" y="-40%" width="180%" height="180%">
            <feGaussianBlur stdDeviation="1.4" result="coloredBlur"/>
            <feMerge>
                <feMergeNode in="coloredBlur"/>
                <feMergeNode in="SourceGraphic"/>
            </feMerge>
        </filter>
        <style>
            .bg {{ fill: #0a0f0d; stroke: #1a2a2a; stroke-width: 2px; }}
            .title {{
                font-family: "Courier New", Consolas, monospace;
                font-size: 14px;
                font-weight: bold;
                fill: #E0E0E0;
                text-anchor: middle;
            }}
            .sign-text {{
                font-family: "Courier New", Consolas, monospace;
                font-size: 13px;
                font-weight: bold;
                fill: {ACCENT};
                filter: url(#glow);
                text-anchor: middle;
            }}
            .sign-sub {{
                font-family: "Courier New", Consolas, monospace;
                font-size: 9px;
                fill: #7fffe0;
                text-anchor: middle;
            }}
            .screen-text {{
                font-family: "Courier New", Consolas, monospace;
                font-size: 9px;
                fill: {ACCENT};
                filter: url(#glow);
                text-anchor: middle;
            }}
            .line-sep {{ stroke: #1a2a2a; stroke-width: 1px; }}
            .fade {{ opacity: 0; animation: fin 0.5s forwards; }}
            .f0 {{ animation-delay: 0.05s; }}
            .f1 {{ animation-delay: 0.20s; }}
            .f2 {{ animation-delay: 0.35s; }}
            .f3 {{ animation-delay: 0.50s; }}
            .f4 {{ animation-delay: 0.65s; }}
            .f5 {{ animation-delay: 0.80s; }}
            @keyframes fin {{
                from {{ opacity: 0; transform: translateY(4px); }}
                to {{ opacity: 1; transform: translateY(0); }}
            }}
            @keyframes blink {{
                0%, 45%, 55%, 100% {{ opacity: 1; }}
                50% {{ opacity: 0.15; }}
            }}
            .cursor {{ animation: blink 1.2s step-end infinite; }}
        </style>
    </defs>

    <!-- Background Card -->
    <rect class="bg" width="100%" height="100%" rx="12" />

    <!-- Terminal Header (matching info-card.svg) -->
    <g transform="translate(15, 20)">
        <circle cx="0" cy="0" r="6" fill="#FF5F56" />
        <circle cx="20" cy="0" r="6" fill="#FFBD2E" />
        <circle cx="40" cy="0" r="6" fill="#27C93F" />
    </g>
    <text x="185" y="25" class="title">{TITLE}</text>
    <line x1="0" y1="40" x2="{WIDTH}" y2="40" class="line-sep" />

    <!-- Hanging dev sign -->
    <g class="fade f0" transform="translate(185, 75)">
        <rect x="-95" y="0" width="190" height="46" rx="6" fill="none" stroke="{ACCENT}" stroke-width="1" filter="url(#glow)"/>
        <text x="0" y="19" class="sign-text">&lt;/&gt; DEV MODE</text>
        <text x="0" y="34" class="sign-sub">STATUS: ONLINE</text>
        <line x1="-55" y1="46" x2="-55" y2="72" stroke="#1a2a2a" stroke-width="1.5"/>
        <line x1="55" y1="46" x2="55" y2="72" stroke="#1a2a2a" stroke-width="1.5"/>
    </g>

    <!-- Character: mascot at a laptop -->
    <g class="fade f1" transform="translate(185, 300)">
        <!-- ground shadow -->
        <ellipse cx="0" cy="205" rx="120" ry="14" fill="#101816"/>

        <!-- body -->
        <rect x="-65" y="10" width="130" height="110" rx="14" fill="none" stroke="{ACCENT}" stroke-width="1" filter="url(#glow)"/>

        <!-- head -->
        <circle cx="0" cy="-35" r="42" fill="none" stroke="{ACCENT}" stroke-width="1" filter="url(#glow)"/>
        <circle class="cursor" cx="-16" cy="-40" r="4" fill="{ACCENT}"/>
        <circle class="cursor" cx="16" cy="-40" r="4" fill="{ACCENT}"/>
        <path d="M -18 -22 Q 0 -10 18 -22" fill="none" stroke="{ACCENT}" stroke-width="2" stroke-linecap="round"/>

        <!-- chest badge -->
        <rect x="-45" y="30" width="90" height="18" rx="4" fill="none" stroke="{ACCENT}" stroke-width="0.75"/>
        <text x="0" y="43" class="screen-text" style="font-size:8px">CODE ON</text>

        <!-- arms -->
        <line x1="-65" y1="55" x2="-100" y2="80" stroke="{ACCENT}" stroke-width="1"/>
        <line x1="65" y1="55" x2="100" y2="80" stroke="{ACCENT}" stroke-width="1"/>

        <!-- laptop -->
        <g transform="translate(0, 100)">
            <rect x="-70" y="-14" width="140" height="10" rx="2" fill="none" stroke="{ACCENT}" stroke-width="1"/>
            <rect x="-55" y="-40" width="110" height="26" rx="2" fill="none" stroke="{ACCENT}" stroke-width="1"/>
            <text x="0" y="-24" class="screen-text">01001 &gt;_<tspan class="cursor">_</tspan></text>
        </g>
    </g>

    <!-- footer strip -->
    <g class="fade f2" transform="translate(185, 520)">
        <text x="0" y="0" class="sign-sub">-- built one commit at a time --</text>
    </g>
</svg>'''


def generate_svg(output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(build_svg())


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_path = os.path.join(base_dir, "hxni-devsign.svg")

    generate_svg(output_path)
    print(f"Success! Generated {output_path}")
