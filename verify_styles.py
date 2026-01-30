
import asyncio
from playwright.async_api import async_playwright

async def verify_grey_fields():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto("http://localhost:5000")

        # Select a section
        await page.select_option('select[name="section_name"]', label="Athlétisme")
        await page.click('button:has-text("Continuer")')

        # Go to Budget form
        await page.click('.card:has-text("1. Budget prévisionnel") a.btn-royal')

        # Check if the field is greyed out
        field = page.locator('input[data-multiplier]')
        await field.wait_for()

        # Scroll to it
        await field.scroll_into_view_if_needed()

        # Get computed styles
        bg_color = await field.evaluate("el => window.getComputedStyle(el).backgroundColor")
        print(f"Background color: {bg_color}")

        await page.screenshot(path="verification/grey_field_check_v5.png", full_page=True)

        await browser.close()

if __name__ == "__main__":
    import subprocess
    import time
    import os

    if not os.path.exists("verification"):
        os.makedirs("verification")

    server = subprocess.Popen(["python3", "app.py"])
    time.sleep(2)
    try:
        asyncio.run(verify_grey_fields())
    finally:
        server.terminate()
