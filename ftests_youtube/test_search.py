import pytest
from playwright.sync_api import Page
import allure

@pytest.fixture(scope="function")
def page(playwright):
    # Launch the browser in headless mode with English locale
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context(locale="en-US")
    page = context.new_page()
    yield page
    browser.close()

@allure.title("Test YouTube search functionality")
def test_youtube_search(page: Page):
    """Test that YouTube search works and displays results."""
    url = "https://www.youtube.com/"
    search_query = "automation testing"

    # Step 1: Open YouTube homepage
    with allure.step("Opening YouTube homepage"):
        page.goto(url)
        allure.attach(
            page.screenshot(), name="Homepage Screenshot", attachment_type=allure.attachment_type.PNG
        )

    # Step 2: Wait for the search input to appear
    with allure.step("Waiting for the search input"):
        page.wait_for_selector("input[name='search_query'].ytSearchboxComponentInput")

    # Step 3: Enter the search query
    with allure.step("Entering search query"):
        search_input = page.locator("input[name='search_query'].ytSearchboxComponentInput")
        search_input.fill(search_query)
        allure.attach(
            page.screenshot(), name="Search Query Entered", attachment_type=allure.attachment_type.PNG
        )

    # Step 4: Perform the search
    with allure.step("Executing search"):
        search_input.press("Enter")

    # Step 5: Verify search results are displayed
    with allure.step("Verifying search results"):
        page.wait_for_selector("img.yt-core-image")
        allure.attach(
            page.screenshot(), name="Search Results Screenshot", attachment_type=allure.attachment_type.PNG
        )

    print("Search functionality works as expected, including image results.")

