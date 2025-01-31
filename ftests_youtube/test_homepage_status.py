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

@allure.parent_suite("YouTube Tests")
@allure.suite("Home Page")
@allure.title("Check YouTube homepage accessibility")
def test_youtube_homepage_status(page: Page):
    """Test that YouTube homepage is accessible and returns status code 200."""
    url = "https://www.youtube.com/"
    with allure.step("Opening YouTube homepage"):
        response = page.goto(url)
        allure.attach(
            page.screenshot(), name="YouTube Homepage Screenshot", attachment_type=allure.attachment_type.PNG
        )
    with allure.step("Verifying status code"):
        assert response.status == 200, f"Expected status 200, but got {response.status}"
    print("YouTube homepage is accessible and returned status code 200.")
