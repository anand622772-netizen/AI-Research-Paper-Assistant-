"""
Index-based screenshot capture of all 9 tabs in the AI Research Paper Assistant.
"""

import time
from pathlib import Path
from playwright.sync_api import sync_playwright

OUTPUT_DIR = Path("outputs/report_assets")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def capture_all_tabs_by_index():
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="msedge", headless=True)
        context = browser.new_context(viewport={"width": 1400, "height": 920})
        page = context.new_page()

        print("Navigating to http://localhost:8501...")
        page.goto("http://localhost:8501", timeout=60000)
        time.sleep(4)

        tabs_info = [
            ("screenshot_1_paper_portal.png", "1. Paper Portal"),
            ("screenshot_2_research_material.png", "2. Research Material"),
            ("screenshot_3_paper_outline.png", "3. Paper Outline"),
            ("screenshot_4_literature_review.png", "4. Literature Review"),
            ("screenshot_5_section_writing.png", "5. Section Writing"),
            ("screenshot_6_refinement_review.png", "6. Refinement & Review"),
            ("screenshot_7_plots_visuals.png", "7. Plots & Visuals"),
            ("screenshot_8_latex_manuscript.png", "8. LaTeX Manuscript"),
            ("screenshot_9_final_paper_export.png", "9. Final Paper & Export")
        ]

        tabs_locator = page.locator('[role="tab"]')
        count = tabs_locator.count()
        print(f"Detected {count} tabs!")

        for idx, (fname, label) in enumerate(tabs_info):
            if idx < count:
                tabs_locator.nth(idx).click()
                time.sleep(2)
                page.screenshot(path=str(OUTPUT_DIR / fname))
                print(f"Captured tab {idx}: {label} -> {fname}")

        browser.close()
        print("Completed capture of all tabs!")

if __name__ == "__main__":
    capture_all_tabs_by_index()
