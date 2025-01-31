import pytest
from playwright.sync_api import Page, expect
import allure


@pytest.fixture(scope="function")
def page(playwright):
    # Запускаем браузер в headless-режиме с отключенной политикой автозапуска
    browser = playwright.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled"])
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
    )
    context = browser.new_context(locale="en-US")
    page = context.new_page()
    yield page
    browser.close()


@allure.parent_suite("YouTube Tests")
@allure.suite("Video Playback")
@allure.title("Check YouTube video playback")
def test_youtube_video_playback(page: Page):
    """Test that a video on YouTube can be played."""
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

    with allure.step("Opening YouTube video page"):
        page.goto(url)
        allure.attach(
            page.screenshot(), name="YouTube Video Page", attachment_type=allure.attachment_type.PNG
        )

    # Шаг 1: Пропуск рекламы, если она появляется
    with allure.step("Skipping ad if present"):
        try:
            skip_button = page.wait_for_selector(".ytp-skip-ad-button", timeout=31000)
            skip_button.click()
            allure.attach(page.screenshot(), name="Ad Skipped", attachment_type=allure.attachment_type.PNG)
        except Exception:
            allure.attach(page.screenshot(), name="No Ad Found", attachment_type=allure.attachment_type.PNG)

    # Шаг 2: Проверка наличия видеоэлемента в DOM (он может быть скрыт в headless‑режиме)
    with allure.step("Checking if video player is present"):
        page.wait_for_selector("video", state="attached", timeout=5000)

    # Шаг 3: Проверка, что видео воспроизводится
    with allure.step("Verifying video playback"):
        page.wait_for_timeout(5000)  # даем время на буферизацию
        is_playing = page.evaluate("document.querySelector('video') && !document.querySelector('video').paused")
        # Если видео не воспроизводится, пробуем кликнуть по кнопке воспроизведения
        if not is_playing:
            play_button = page.locator("button.ytp-play-button")
            play_button.click()
            page.wait_for_timeout(3000)
            is_playing = page.evaluate("document.querySelector('video') && !document.querySelector('video').paused")
        assert is_playing, "Video is not playing!"

    # Шаг 4: Проверка состояния кнопки Play/Pause (она должна указывать, что видео воспроизводится)
    with allure.step("Checking Play/Pause button state"):
        play_button = page.locator(".ytp-play-button")
        expect(play_button).to_have_attribute("aria-label", "Pause (k)")

    allure.attach(page.screenshot(), name="Final Video State", attachment_type=allure.attachment_type.PNG)
    print("✅ YouTube video playback test passed.")
