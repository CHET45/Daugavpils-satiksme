import asyncio
from playwright.async_api import async_playwright
def ToPDF(url):
    async def url_to_pdf(url, output_path):
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            await page.goto(url)
            await page.pdf(path=output_path)
            await browser.close()

    #
    url = 'https://satiksme.daugavpils.lv/tramvajs-nr-1-butlerova-iela-stacija'
    #

    output_path = 'satiksme.pdf'

    asyncio.run(url_to_pdf(url, output_path))
