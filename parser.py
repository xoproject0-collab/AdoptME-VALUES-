import asyncio, json
from playwright.async_api import async_playwright

async def parse():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        await page.goto("https://elvebredd.com/")

        # скроллим чтобы загрузить ВСЁ
        for _ in range(25):
            await page.mouse.wheel(0, 10000)
            await page.wait_for_timeout(1000)

        pets = await page.evaluate("""
        () => {
            let data = []
            document.querySelectorAll(".card").forEach(el => {
                let text = el.innerText.split("\\n")
                let name = text[0]
                let value = parseFloat(text[1]) || 0
                data.push({name, value})
            })
            return data
        }
        """)

        await browser.close()

        unique = {p["name"]: p for p in pets}

        with open("pets.json", "w") as f:
            json.dump(list(unique.values()), f)

        print("✅ pets updated:", len(unique))