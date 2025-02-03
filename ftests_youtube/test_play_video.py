import os
import json
import pytest
from playwright.sync_api import Page, expect
import allure

# ficsture for profile state
@pytest.fixture(scope="session")
def storage_state_file(tmp_path_factory):
    storage_state = os.getenv("YT_STORAGE_STATE")
    if not storage_state:
        pytest.skip("Authorization state incorrect (There is no YT_STORAGE_STATE)")
    # tem file for profile state
    storage_state_path = tmp_path_factory.mktemp("data") / "storage_state.json"
    with open(storage_state_path, "w", encoding="utf-8") as f:
        f.write(storage_state)
    return str(storage_state_path)

@pytest.fixture(scope="function")
def page_with_auth(playwright, storage_state_file):
    browser = playwright.chromium.launch(
        headless=True,
        args=["--autoplay-policy=no-user-gesture-required"]
    )
    with open(storage_state_file, "r", encoding="utf-8") as f:
        storage_state = json.load(f)
    context = browser.new_context(storage_state=storage_state, locale="en-US")
    page = context.new_page()
    yield page
    browser.close()

@allure.parent_suite("YouTube Tests")
@allure.suite("Video Playback")
@allure.title("Check YouTube video playback2 (with auth)")
def test_youtube_video_playback(page_with_auth: Page):
    """Test that a video on YouTube can be played with an authenticated session."""
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

    with allure.step("Opening YouTube video page"):
        page_with_auth.goto(url)
        allure.attach(
            page_with_auth.screenshot(), name="YouTube Video Page", attachment_type=allure.attachment_type.PNG
        )

    with allure.step("Skipping ad if present"):
        try:
            skip_button = page_with_auth.wait_for_selector(".ytp-skip-ad-button", timeout=31000)
            skip_button.click()
            allure.attach(page_with_auth.screenshot(), name="Ad Skipped", attachment_type=allure.attachment_type.PNG)
        except Exception:
            allure.attach(page_with_auth.screenshot(), name="No Ad Found", attachment_type=allure.attachment_type.PNG)

    with allure.step("Checking if video player is present"):
        page_with_auth.wait_for_selector("video", state="attached", timeout=5000)

    with allure.step("Verifying video playback"):
        page_with_auth.wait_for_timeout(5000)  # buff
        is_playing = page_with_auth.evaluate("document.querySelector('video') && !document.querySelector('video').paused")
        if not is_playing:
            play_button = page_with_auth.locator("button.ytp-play-button")
            play_button.click()
            page_with_auth.wait_for_timeout(3000)
            is_playing = page_with_auth.evaluate("document.querySelector('video') && !document.querySelector('video').paused")
        assert is_playing, "Video is not playing!"

    with allure.step("Checking Play/Pause button state"):
        play_button = page_with_auth.locator(".ytp-play-button")
        expect(play_button).to_have_attribute("aria-label", "Pause (k)")

    allure.attach(page_with_auth.screenshot(), name="Final Video State", attachment_type=allure.attachment_type.PNG)
    print("✅ YouTube video playback test passed.")
