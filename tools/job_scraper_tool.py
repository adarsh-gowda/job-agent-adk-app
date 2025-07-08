"""
Job Scraper Tool

This tool uses Playwright to scrape job descriptions from job portals like LinkedIn or Indeed.
It returns the job title, company, and full job description in a structured dictionary.
"""
import os
from typing import Dict, Any
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError

from dotenv import load_dotenv
load_dotenv()


LINKEDIN_USERNAME = os.getenv("LINKEDIN_USERNAME")
LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD")

async def extract_job_description(page) -> str:
    """
    Try multiple known selectors to extract job description text.

    Args:
        page (Page): Playwright page object.

    Returns:
        str: Extracted job description or a fallback message.
    """
    possible_selectors = [
        "div.description",
        "div.jobs-description",
        "div.jobsearch-jobDescriptionText",              # Indeed
        "section.jobs-description-content",
        "div[data-testid='jobDescriptionText']",         # Indeed new layout
        "div.show-more-less-html__markup",               # LinkedIn
        "div.description__text",
        "section[class*='description']",
        "article",
        "section",
    ]

    for selector in possible_selectors:
        try:
            desc = await page.locator(selector).first.text_content()
            if desc and len(desc.strip()) > 200:
                return desc.strip()
        except Exception:
            continue

    return "No description found"

async def login_to_linkedin(page):
    print("🔐 Logging into LinkedIn...")
    await page.goto("https://www.linkedin.com/login", timeout=60000)
    await page.fill("input[name='session_key']", LINKEDIN_USERNAME)
    await page.fill("input[name='session_password']", LINKEDIN_PASSWORD)
    await page.click("button[type='submit']")
    await page.wait_for_load_state("networkidle")  # ensures login has settled
    print("✅ Logged in successfully!")

async def get_job_description(job_url: str) -> Dict[str, Any]:
    """
    Scrape a job listing from a given URL.

    Args:
        job_url (str): The URL of the job listing.

    Returns:
        Dict[str, Any]: Dictionary containing job title, company name, and job description.
    """
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            context = await browser.new_context()
            page = await context.new_page()

            # Login first
            await login_to_linkedin(page)

            await page.goto(job_url, timeout=60000)

            # Try to extract common selectors. Adjust as needed per platform.
            title = await page.locator("h1").first.text_content() 
            company = await page.locator("span:below(h1)").nth(0).text_content()
            description = await extract_job_description(page)

            await browser.close()

            return {
                "result": {
                    "job_title": title.strip() if title else "Unknown Title",
                    "company": company.strip() if company else "Unknown Company",
                    "description": description.strip(),
                },
                "stats": {
                    "source_url": job_url,
                    "success": True,
                },
                "additional_info": {
                    "platform": "LinkedIn",
                    "scrape_type": "playwright-logged-in",
                }
            }
    except PlaywrightTimeoutError as timeout_err:
        return {
            "result": {"job_title": None, "company": None, "description": None},
            "stats": {"source_url": job_url, "success": False},
            "additional_info": {"error": f"Timeout: {timeout_err}"}
        }

    except Exception as e:
        return {
            "result": {
                "job_title": None,
                "company": None,
                "description": None,
            },
            "stats": {
                "source_url": job_url,
                "success": False,
            },
            "additional_info": {
                "error": str(e),
            }
        }
