from asyncio import get_running_loop, run, sleep

from playwright.async_api import Page, async_playwright

from src.config import (
    EMAIL,
    HEADLESS,
    PASSWORD,
    SLEEP_TIME_FOR_LOGIN,
    URL_LOGIN,
    URL_SEARCH,
)
from src.read_companies import read_companies, save_companies


async def get_number_of_employees(page: Page, url: str) -> int:
    await page.goto(f"{url}/people")
    await page.wait_for_load_state("load")

    # Pattern for: <h2 class="text-heading-xlarge">1,000 associated members</h2>
    text = await page.inner_text('h2[class="text-heading-xlarge"]')
    return int(
        text.split(" ")[0]
        .replace(  # Avoid comma and dot.
            ",", ""
        )
        .replace(".", "")
    )


async def login(page: Page, email: str, password: str) -> Page:
    await page.goto(URL_LOGIN)
    await page.wait_for_load_state("load")

    await page.get_by_label("Email or phone").click()
    await page.get_by_label("Email or phone").fill(email)
    await page.get_by_label("Password").click()
    await page.get_by_label("Password").fill(password)
    await (
        page.locator("#organic-div form")
        .get_by_role("button", name="Sign in")
        .click()
    )
    await page.wait_for_load_state("load")
    return page


async def search_company_url(page: Page, company_name: str) -> str | None:
    """Go to the LinkedIn search page and get the first company's URL
    from the search results. Need to solve login/captcha manually if necessary.
    """
    url = ""
    while "search/results/companies/" not in url:
        await page.goto(URL_SEARCH.format(company_name=company_name))
        await page.wait_for_load_state("load")
        url = page.url
        if "search/results/companies/" not in url:
            print(
                "Please, check if there is a captcha or login to you to solve. "
                "You will need to set HEADLESS=False in src/config.py if it is not. "
                f"Wait {SLEEP_TIME_FOR_LOGIN} seconds to try again."
            )
            await sleep(SLEEP_TIME_FOR_LOGIN)

    responses = (
        page.get_by_role("listitem")
        .filter(has_text=company_name)
        .filter(has=page.get_by_role("link"))
    )
    first_locator = (await responses.all())[0]

    # Get the first company's LinkedIn URL from the search results.
    return await first_locator.get_by_role(
        "link", name=company_name
    ).get_attribute("href")


async def main() -> None:
    loop = get_running_loop()
    companies = await loop.run_in_executor(None, read_companies)
    async with async_playwright() as p:
        # 1. Open a browser and login to LinkedIn.
        browser = await p.chromium.launch(headless=HEADLESS)
        page = await browser.new_page()
        await login(page, EMAIL, PASSWORD)

        # 2. Get the LinkedIn URL for each company.
        company_urls = {}
        for company in companies:
            print(f"Getting LinkedIn url for {company}")
            url = await search_company_url(page, company)
            if url is not None:
                company_urls[company] = url
            else:
                print(f"{company}'s not found.")

        # 3. Get the number of employees for each company.
        company_urls_employees = []
        for company, url in company_urls.items():
            print(f"Getting number of employees for {company}")
            employees = await get_number_of_employees(page, url)
            company_urls_employees.append((company, url, employees))

        await loop.run_in_executor(None, save_companies, company_urls_employees)
        await browser.close()


if __name__ == "__main__":
    run(main())
