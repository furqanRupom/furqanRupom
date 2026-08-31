#!/usr/bin/env python3
"""Generate a clean, minimal, ultra-cinematic dark neon teal header banner SVG.

Contains strictly:
- Full Name: Furqan Ahmad Rupom
- Role: Backend Developer • Full Stack Developer

Produces: banner.svg (in project root)
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_FILE = os.path.join(BASE_DIR, "banner.svg")


def generate_banner():
    width = 900
    height = 180

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="{height}">
  <defs>
    <!-- Background Gradient -->
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#060b0a"/>
      <stop offset="50%" stop-color="#0a1210"/>
      <stop offset="100%" stop-color="#050807"/>
    </linearGradient>

    <!-- Top & Bottom Glow Lines -->
    <linearGradient id="tealGlowGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#00FFA3" stop-opacity="0"/>
      <stop offset="25%" stop-color="#00FFD1" stop-opacity="0.85"/>
      <stop offset="50%" stop-color="#00FFD1" stop-opacity="1"/>
      <stop offset="75%" stop-color="#0ABDC6" stop-opacity="0.85"/>
      <stop offset="100%" stop-color="#00FFA3" stop-opacity="0"/>
    </linearGradient>

    <!-- Title Gradient -->
    <linearGradient id="titleGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="40%" stop-color="#F0FFFB"/>
      <stop offset="75%" stop-color="#00FFD1"/>
      <stop offset="100%" stop-color="#00FFA3"/>
    </linearGradient>

    <!-- Subtitle Gradient -->
    <linearGradient id="subGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#00FFD1"/>
      <stop offset="50%" stop-color="#80FFE8"/>
      <stop offset="100%" stop-color="#00FFA3"/>
    </linearGradient>

    <!-- Cyber Grid Pattern -->
    <pattern id="cyberGrid" width="30" height="30" patternUnits="userSpaceOnUse">
      <path d="M 30 0 L 0 0 0 30" fill="none" stroke="#00FFD1" stroke-width="0.5" stroke-opacity="0.06"/>
      <circle cx="0" cy="0" r="0.8" fill="#00FFD1" fill-opacity="0.12"/>
    </pattern>

    <!-- Neon Glow Filter -->
    <filter id="neonGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3" result="blur1"/>
      <feGaussianBlur stdDeviation="7" result="blur2"/>
      <feMerge>
        <feMergeNode in="blur2"/>
        <feMergeNode in="blur1"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="subtleGlow" x="-10%" y="-10%" width="120%" height="120%">
      <feGaussianBlur stdDeviation="1.5" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <style>
      @keyframes pulseGlow {{
        0%, 100% {{ opacity: 0.6; }}
        50% {{ opacity: 1; }}
      }}
      .pulse {{ animation: pulseGlow 4s ease-in-out infinite; }}
      .mono {{ font-family: "JetBrains Mono", "Fira Code", "Courier New", monospace; }}
      .sans {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; }}
    </style>
  </defs>

  <!-- Base Card -->
  <rect width="100%" height="100%" rx="16" fill="url(#bgGrad)" stroke="#162925" stroke-width="1.5"/>

  <!-- Subtle Cyber Grid -->
  <rect width="100%" height="100%" rx="16" fill="url(#cyberGrid)"/>

  <!-- Minimal Corner Brackets -->
  <path d="M 22 38 L 22 22 L 38 22" fill="none" stroke="#00FFD1" stroke-width="1.8" opacity="0.5"/>
  <path d="M 878 38 L 878 22 L 862 22" fill="none" stroke="#00FFD1" stroke-width="1.8" opacity="0.5"/>
  <path d="M 22 142 L 22 158 L 38 158" fill="none" stroke="#00FFD1" stroke-width="1.8" opacity="0.5"/>
  <path d="M 878 142 L 878 158 L 862 158" fill="none" stroke="#00FFD1" stroke-width="1.8" opacity="0.5"/>

  <!-- Top Accent Neon Line -->
  <line x1="140" y1="2" x2="760" y2="2" stroke="url(#tealGlowGrad)" stroke-width="2.5" filter="url(#neonGlow)" class="pulse"/>

  <!-- Name / Title -->
  <g transform="translate(450, 84)">
    <text x="0" y="0" text-anchor="middle" fill="#00FFD1" font-size="40" font-weight="900" letter-spacing="4" filter="url(#neonGlow)" opacity="0.35" class="sans">
      FURQAN AHMAD RUPOM
    </text>
    <text x="0" y="0" text-anchor="middle" fill="url(#titleGrad)" font-size="40" font-weight="900" letter-spacing="4" class="sans">
      FURQAN AHMAD RUPOM
    </text>
  </g>

  <!-- Subtle Accent Divider -->
  <g transform="translate(290, 106)">
    <line x1="0" y1="0" x2="320" y2="0" stroke="url(#tealGlowGrad)" stroke-width="1.5"/>
    <polygon points="160,-3 164,0 160,3 156,0" fill="#00FFD1" filter="url(#subtleGlow)"/>
  </g>

  <!-- Role / Subtitle -->
  <g transform="translate(450, 136)">
    <text x="0" y="0" text-anchor="middle" fill="url(#subGrad)" font-size="14.5" font-weight="700" letter-spacing="3" class="mono">
      FULL STACK DEVELOPER • BACKEND DEVELOPER
    </text>
  </g>

  <!-- Bottom Accent Neon Line -->
  <line x1="220" y1="178" x2="680" y2="178" stroke="url(#tealGlowGrad)" stroke-width="2" filter="url(#subtleGlow)" opacity="0.6"/>
</svg>'''

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Generated clean minimal {OUTPUT_FILE}")


if __name__ == "__main__":
    generate_banner()
