"""Capture preview.html with Playwright (headless Chromium, deterministic)."""
from __future__ import annotations
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
URL = (ROOT / "preview.html").as_uri()
OUT = ROOT / "docs" / "screenshots"
OUT.mkdir(parents=True, exist_ok=True)

with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    # desktop
    pg = b.new_page(viewport={"width": 1440, "height": 900}, device_scale_factor=2)
    pg.goto(URL, wait_until="domcontentloaded")
    pg.wait_for_timeout(900)
    pg.screenshot(path=str(OUT / "preview-desktop.png"))
    pg.screenshot(path=str(OUT / "preview-full.png"), full_page=True)
    pg.close()
    # mobile
    m = b.new_page(viewport={"width": 390, "height": 844}, device_scale_factor=2, is_mobile=True)
    m.goto(URL, wait_until="domcontentloaded")
    m.wait_for_timeout(900)
    m.screenshot(path=str(OUT / "preview-mobile.png"))
    m.close()
    b.close()
print(f"done -> {OUT}")
for f in sorted(OUT.glob("*.png")):
    print(f.name, f.stat().st_size)
