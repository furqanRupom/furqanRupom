#!/usr/bin/env python3
"""Render a contribution heatmap SVG from contribution data.

Reads data/contributions.json and generates contrib-heatmap.svg.
Uses a dark neon teal theme optimized for GitHub README display.
"""

import json
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_FILE = os.path.join(BASE_DIR, "data", "contributions.json")
OUTPUT_FILE = os.path.join(BASE_DIR, "contrib-heatmap.svg")

# Color scheme — dark neon teal
COLORS = {
    0: "#161b22",
    1: "#003d33",
    2: "#006b5a",
    3: "#00a88a",
    4: "#00FFD1",
}
BG_COLOR = "#0d0d0d"
BORDER_COLOR = "#1a2a2a"
LABEL_COLOR = "#00FFD1"
TEXT_COLOR = "#C0C0C0"
DIM_COLOR = "#666666"
ACCENT_COLOR = "#00FFA3"

# Grid dimensions
CELL_SIZE = 11
CELL_GAP = 3
CELL_RADIUS = 2

MONTHS = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
]
DAYS = ["", "Mon", "", "Wed", "", "Fri", ""]


def load_data():
    """Load contribution data from JSON file."""
    if not os.path.exists(INPUT_FILE):
        print(f"Warning: {INPUT_FILE} not found. Generating placeholder heatmap.")
        return None

    try:
        with open(INPUT_FILE, "r") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        print(f"Warning: Error reading {INPUT_FILE}: {e}")
        return None


def build_grid(data):
    """Build a 53x7 contribution grid from the data."""
    grid = [[0] * 7 for _ in range(53)]

    if not data or not data.get("weeks"):
        return grid

    for w_idx, week in enumerate(data["weeks"]):
        if w_idx >= 53:
            break
        for day in week.get("days", []):
            try:
                dt = datetime.strptime(day["date"], "%Y-%m-%d")
                day_of_week = (dt.weekday() + 1) % 7  # Sunday=0
                level = min(day.get("level", 0), 4)
                grid[w_idx][day_of_week] = level
            except (ValueError, KeyError):
                continue

    return grid


def get_month_labels(data):
    """Determine month label positions based on the contribution data."""
    labels = []
    if not data or not data.get("weeks"):
        # Generate default month positions
        for i, month in enumerate(MONTHS):
            labels.append((i * 4.3, month))
        return labels

    seen_months = set()
    for w_idx, week in enumerate(data["weeks"]):
        for day in week.get("days", []):
            try:
                dt = datetime.strptime(day["date"], "%Y-%m-%d")
                month = dt.month
                if month not in seen_months:
                    seen_months.add(month)
                    labels.append((w_idx, MONTHS[month - 1]))
                break
            except (ValueError, KeyError):
                continue

    return labels


def render_svg(data):
    """Render the contribution heatmap as SVG."""
    grid = build_grid(data)
    month_labels = get_month_labels(data)

    # Stats
    total = data.get("total_contributions", 0) if data else 0
    current_streak = data.get("current_streak", 0) if data else 0
    longest_streak = data.get("longest_streak", 0) if data else 0
    best_day = data.get("best_day", "N/A") if data else "N/A"
    best_count = data.get("best_day_count", 0) if data else 0

    # Layout calculations
    left_pad = 40  # for day labels
    top_pad = 65  # for title + month labels
    grid_width = 53 * (CELL_SIZE + CELL_GAP)
    grid_height = 7 * (CELL_SIZE + CELL_GAP)
    stats_height = 60
    legend_height = 30
    padding = 20

    total_width = left_pad + grid_width + padding * 2
    total_height = top_pad + grid_height + stats_height + legend_height + padding * 2

    # Clamp width for display
    svg_width = max(860, total_width)

    svg_parts = []

    # SVG header
    svg_parts.append(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {total_height}" width="{svg_width}" height="{total_height}">
  <defs>
    <style>
      .hm-bg {{ fill: {BG_COLOR}; }}
      .hm-title {{ font-family: "JetBrains Mono", "Courier New", monospace; font-size: 16px; fill: {LABEL_COLOR}; font-weight: bold; }}
      .hm-month {{ font-family: "JetBrains Mono", "Courier New", monospace; font-size: 10px; fill: {DIM_COLOR}; }}
      .hm-day {{ font-family: "JetBrains Mono", "Courier New", monospace; font-size: 10px; fill: {DIM_COLOR}; }}
      .hm-stat-label {{ font-family: "JetBrains Mono", "Courier New", monospace; font-size: 11px; fill: {DIM_COLOR}; }}
      .hm-stat-value {{ font-family: "JetBrains Mono", "Courier New", monospace; font-size: 13px; fill: {LABEL_COLOR}; font-weight: bold; }}
      .hm-legend-text {{ font-family: "JetBrains Mono", "Courier New", monospace; font-size: 10px; fill: {DIM_COLOR}; }}
      .hm-cell {{ opacity: 0; animation: cellFade 0.3s forwards; }}
      @keyframes cellFade {{ to {{ opacity: 1; }} }}
    </style>
  </defs>

  <!-- Background -->
  <rect width="100%" height="100%" rx="12" class="hm-bg" stroke="{BORDER_COLOR}" stroke-width="1.5"/>

  <!-- Title -->
  <text x="{padding}" y="{padding + 20}" class="hm-title">Contribution Activity</text>
''')

    # Month labels
    for w_idx, label in month_labels:
        x = padding + left_pad + w_idx * (CELL_SIZE + CELL_GAP)
        y = top_pad - 8
        svg_parts.append(f'  <text x="{x}" y="{y}" class="hm-month">{label}</text>')

    # Day labels
    for d_idx, label in enumerate(DAYS):
        if label:
            y = top_pad + d_idx * (CELL_SIZE + CELL_GAP) + CELL_SIZE - 1
            svg_parts.append(
                f'  <text x="{padding + 5}" y="{y}" class="hm-day">{label}</text>'
            )

    # Contribution cells
    cell_count = 0
    for w_idx in range(53):
        for d_idx in range(7):
            level = grid[w_idx][d_idx]
            x = padding + left_pad + w_idx * (CELL_SIZE + CELL_GAP)
            y = top_pad + d_idx * (CELL_SIZE + CELL_GAP)
            color = COLORS.get(level, COLORS[0])
            delay = cell_count * 0.002
            svg_parts.append(
                f'  <rect x="{x}" y="{y}" width="{CELL_SIZE}" height="{CELL_SIZE}" '
                f'rx="{CELL_RADIUS}" fill="{color}" class="hm-cell" '
                f'style="animation-delay: {delay:.3f}s"/>'
            )
            cell_count += 1

    # Stats bar
    stats_y = top_pad + grid_height + 25
    stats = [
        ("Total", str(total)),
        ("Current Streak", f"{current_streak}d"),
        ("Longest Streak", f"{longest_streak}d"),
        ("Best Day", f"{best_day} ({best_count})"),
    ]

    stat_spacing = (svg_width - padding * 2) / len(stats)
    for i, (label, value) in enumerate(stats):
        x = padding + i * stat_spacing
        svg_parts.append(
            f'  <text x="{x}" y="{stats_y}" class="hm-stat-label">{label}</text>'
        )
        svg_parts.append(
            f'  <text x="{x}" y="{stats_y + 18}" class="hm-stat-value">{value}</text>'
        )

    # Legend
    legend_y = stats_y + 45
    legend_x = svg_width - padding - 180
    svg_parts.append(
        f'  <text x="{legend_x - 35}" y="{legend_y + 9}" class="hm-legend-text">Less</text>'
    )
    for i in range(5):
        svg_parts.append(
            f'  <rect x="{legend_x + i * 16}" y="{legend_y}" '
            f'width="{CELL_SIZE}" height="{CELL_SIZE}" rx="{CELL_RADIUS}" fill="{COLORS[i]}"/>'
        )
    svg_parts.append(
        f'  <text x="{legend_x + 5 * 16 + 5}" y="{legend_y + 9}" class="hm-legend-text">More</text>'
    )

    svg_parts.append("</svg>")

    return "\n".join(svg_parts)


def main():
    print("Loading contribution data...")
    data = load_data()

    print("Rendering heatmap SVG...")
    svg_content = render_svg(data)

    with open(OUTPUT_FILE, "w") as f:
        f.write(svg_content)

    print(f"Generated {OUTPUT_FILE}")

    if data:
        print(f"  Total contributions: {data.get('total_contributions', 0)}")
        print(f"  Current streak: {data.get('current_streak', 0)} days")
        print(f"  Longest streak: {data.get('longest_streak', 0)} days")


if __name__ == "__main__":
    main()
