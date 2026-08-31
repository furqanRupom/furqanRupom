#!/usr/bin/env python3
"""Generate a matching ultra-cinematic dark neon teal footer SVG.

Produces: footer.svg (in project root)
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_FILE = os.path.join(BASE_DIR, "footer.svg")


def generate_footer():
    width = 900
    height = 80

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="{height}">
  <defs>
    <linearGradient id="footerBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#050807"/>
      <stop offset="50%" stop-color="#0a1210"/>
      <stop offset="100%" stop-color="#070c0b"/>
    </linearGradient>

    <linearGradient id="footerLine" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#00FFA3" stop-opacity="0"/>
      <stop offset="30%" stop-color="#00FFD1" stop-opacity="0.9"/>
      <stop offset="50%" stop-color="#80FFE8" stop-opacity="1"/>
      <stop offset="70%" stop-color="#00FFD1" stop-opacity="0.9"/>
      <stop offset="100%" stop-color="#00FFA3" stop-opacity="0"/>
    </linearGradient>

    <filter id="fGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="2" result="b"/>
      <feMerge>
        <feMergeNode in="b"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect width="100%" height="100%" rx="12" fill="url(#footerBg)" stroke="#162925" stroke-width="1"/>
  <line x1="80" y1="2" x2="820" y2="2" stroke="url(#footerLine)" stroke-width="2" filter="url(#fGlow)"/>

  <!-- Footer Tag -->
  <text x="450" y="45" text-anchor="middle" fill="#00FFD1" font-family="'JetBrains Mono', 'Courier New', monospace" font-size="12" font-weight="600" letter-spacing="2">
    BUILT WITH CURIOSITY <tspan fill="#00FFA3">●</tspan> POWERED BY CODE <tspan fill="#00FFA3">●</tspan> ALWAYS LEARNING
  </text>
</svg>'''

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Generated {OUTPUT_FILE}")


if __name__ == "__main__":
    generate_footer()
