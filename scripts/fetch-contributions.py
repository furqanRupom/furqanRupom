#!/usr/bin/env python3
"""Fetch GitHub contribution data for a user.

Scrapes the public GitHub contribution calendar (no API token required).
Usage: python scripts/fetch_contributions.py
Output: data/contributions.json
"""

import json
import os
import re
from datetime import datetime, timedelta, timezone

import requests
from bs4 import BeautifulSoup

USERNAME = "furqanRupom"
CONTRIBUTIONS_URL = f"https://github.com/users/{USERNAME}/contributions"
OUTPUT_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data"
)
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "contributions.json")


def fetch_contribution_page():
    """Fetch the public contribution calendar HTML."""
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml",
    }
    try:
        resp = requests.get(CONTRIBUTIONS_URL, headers=headers, timeout=30)
        resp.raise_for_status()
        return resp.text
    except requests.RequestException as e:
        print(f"Error fetching contributions: {e}")
        return None


def parse_contributions(html):
    """Parse contribution data from the GitHub calendar HTML.

    GitHub renders contribution data as <td> or <rect> elements with
    data-date, data-level, and tooltip-based count information.
    """
    soup = BeautifulSoup(html, "html.parser")
    contributions = []

    # Strategy 1: Look for <td> elements with contribution data (newer GitHub layout)
    cells = soup.find_all("td", class_="ContributionCalendar-day")
    if not cells:
        # Strategy 2: Look for <rect> elements (SVG-based calendar)
        cells = soup.find_all("rect", attrs={"data-date": True})

    for cell in cells:
        date_str = cell.get("data-date")
        if not date_str:
            continue

        level = int(cell.get("data-level", 0))

        # Try to extract count from various sources
        count = 0
        # Check data-count attribute
        if cell.get("data-count"):
            try:
                count = int(cell["data-count"])
            except (ValueError, TypeError):
                pass

        # Check tool-tip child element
        if count == 0:
            tooltip = cell.find("tool-tip") or cell.find("span", class_="sr-only")
            if tooltip:
                text = tooltip.get_text(strip=True)
                match = re.search(r"(\d+)\s+contribution", text)
                if match:
                    count = int(match.group(1))

        # Check aria-label or title
        if count == 0:
            for attr in ("aria-label", "title"):
                val = cell.get(attr, "")
                match = re.search(r"(\d+)\s+contribution", val)
                if match:
                    count = int(match.group(1))
                    break

        # If we still have no count but level > 0, estimate from level
        if count == 0 and level > 0:
            count = level  # rough fallback

        contributions.append(
            {
                "date": date_str,
                "count": count,
                "level": level,
            }
        )

    # Sort by date
    contributions.sort(key=lambda x: x["date"])
    return contributions


def calculate_stats(contributions):
    """Calculate contribution statistics."""
    total = sum(c["count"] for c in contributions)

    # Best day
    best = max(contributions, key=lambda c: c["count"]) if contributions else None
    best_day = best["date"] if best else "N/A"
    best_count = best["count"] if best else 0

    # Streaks
    current_streak = 0
    longest_streak = 0
    streak = 0

    today = datetime.now(timezone.utc).date()
    yesterday = today - timedelta(days=1)

    # Build a set of dates with contributions
    contrib_dates = set()
    for c in contributions:
        if c["count"] > 0:
            try:
                contrib_dates.add(datetime.strptime(c["date"], "%Y-%m-%d").date())
            except ValueError:
                pass

    # Calculate longest streak
    if contributions:
        all_dates = sorted(contrib_dates)
        if all_dates:
            temp_streak = 1
            for i in range(1, len(all_dates)):
                if (all_dates[i] - all_dates[i - 1]).days == 1:
                    temp_streak += 1
                else:
                    longest_streak = max(longest_streak, temp_streak)
                    temp_streak = 1
            longest_streak = max(longest_streak, temp_streak)

    # Calculate current streak (must include today or yesterday)
    check_date = today
    if check_date not in contrib_dates and yesterday in contrib_dates:
        check_date = yesterday

    if check_date in contrib_dates:
        current_streak = 1
        d = check_date - timedelta(days=1)
        while d in contrib_dates:
            current_streak += 1
            d -= timedelta(days=1)

    return {
        "total_contributions": total,
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "best_day": best_day,
        "best_day_count": best_count,
    }


def group_into_weeks(contributions):
    """Group contributions into weekly buckets for the heatmap."""
    if not contributions:
        return []

    weeks = []
    current_week = []

    for c in contributions:
        try:
            dt = datetime.strptime(c["date"], "%Y-%m-%d")
        except ValueError:
            continue

        weekday = dt.weekday()  # Monday=0, Sunday=6
        # GitHub calendar starts on Sunday
        gh_weekday = (weekday + 1) % 7  # Sunday=0, Saturday=6

        if gh_weekday == 0 and current_week:
            weeks.append({"days": current_week})
            current_week = []

        current_week.append(c)

    if current_week:
        weeks.append({"days": current_week})

    return weeks


def main():
    print(f"Fetching contributions for {USERNAME}...")
    html = fetch_contribution_page()

    if not html:
        print("Failed to fetch contribution data. Creating empty data file.")
        data = {
            "username": USERNAME,
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "total_contributions": 0,
            "current_streak": 0,
            "longest_streak": 0,
            "best_day": "N/A",
            "best_day_count": 0,
            "weeks": [],
        }
    else:
        contributions = parse_contributions(html)
        print(f"Parsed {len(contributions)} contribution days.")

        stats = calculate_stats(contributions)
        weeks = group_into_weeks(contributions)

        data = {
            "username": USERNAME,
            "generated_at": datetime.now(timezone.utc).isoformat() + "Z",
            **stats,
            "weeks": weeks,
        }

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(data, f, indent=2)

    print(f"Saved contribution data to {OUTPUT_FILE}")
    print(f"  Total contributions: {data['total_contributions']}")
    print(f"  Current streak: {data['current_streak']} days")
    print(f"  Longest streak: {data['longest_streak']} days")
    print(f"  Best day: {data['best_day']} ({data['best_day_count']} contributions)")


if __name__ == "__main__":
    main()
