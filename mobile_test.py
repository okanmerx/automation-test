import time
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.options.android import UiAutomator2Options
from selenium.common.exceptions import NoSuchElementException


def open_app_drawer(driver):
    """Swipe from bottom to top to open the app drawer."""
    size = driver.get_window_size()
    width = size["width"]
    height = size["height"]

    start_x = width / 2
    start_y = height * 0.9   # bottom
    end_y = height * 0.2     # top

    print("📱 Swiping up to open Apps screen...")
    driver.swipe(start_x, start_y, start_x, end_y, 600)
    time.sleep(1)


def scroll_into_view_by_text(driver, text, contains=False):
    """
    Scroll inside the current screen until an element with given text is found.
    contains=False  -> exact match  (text("..."))
    contains=True   -> partial match (textContains("..."))
    """
    if contains:
        ui_selector = f'new UiSelector().textContains("{text}")'
    else:
        ui_selector = f'new UiSelector().text("{text}")'

    query = (
        "new UiScrollable(new UiSelector().scrollable(true))"
        f".scrollIntoView({ui_selector})"
    )

    print(f"🔍 Scrolling to find: '{text}' ...")
    return driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, query)


def test_toggle_dark_theme():
    print("🚀 Starting Mobile Dark Theme Test...")

    caps = {
        "platformName": "Android",
        "automationName": "UiAutomator2",
        "deviceName": "Android Emulator",
        "noReset": True,
        "newCommandTimeout": 300,
    }

    driver = webdriver.Remote(
        "http://127.0.0.1:4723",
        options=UiAutomator2Options().load_capabilities(caps)
    )

    try:
        # 1) Ana ekrana dön
        print("🏠 Going to HOME screen...")
        driver.press_keycode(3)  # KEYCODE_HOME
        time.sleep(1)

        # 2) Uygulama menüsünü aç
        open_app_drawer(driver)

        # 3) SADECE 'Settings' ikonunu bul ve tıkla
        print("⚙️ Looking for 'Settings' app icon...")
        settings_icon = driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().text(\"Settings\")'
        )
        print("✅ 'Settings' icon found, opening...")
        settings_icon.click()
        time.sleep(2)

        # 4) 'Display & touch' satırını bul ve tıkla
        display_touch = scroll_into_view_by_text(
            driver, "Display & touch", contains=False
        )
        print("✅ 'Display & touch' row found, opening...")
        display_touch.click()
        time.sleep(2)

        # 5) Bu ekrandaki 'Dark theme' satırını bul ve tıkla
        print("🔍 Looking for 'Dark theme' row on Display & touch screen...")
        dark_theme_row = driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().textContains(\"Dark theme\")'
        )
        print("✅ 'Dark theme' row found, opening details...")
        dark_theme_row.click()
        time.sleep(2)

        # 6) Açılan ekranda 'Use dark theme' anahtarını bul
        print("🔍 Looking for 'Use dark theme' toggle...")
        use_dark_theme_label = driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().textContains(\"Use dark theme\")'
        )
        print("✅ 'Use dark theme' label found.")

        # Satırın tamamına tıklamak genelde switch'i toggle eder
        print("🌓 Toggling 'Use dark theme'...")
        use_dark_theme_label.click()
        time.sleep(2)

        print("🎉 Dark theme should now be ENABLED!")

        # 7) Geri ve HOME
        print("↩️ Going back and returning to HOME...")
        driver.back()  # Dark theme ekranından Display & touch'a
        time.sleep(1)
        driver.back()  # Display & touch'tan Settings'e
        time.sleep(1)
        driver.press_keycode(3)  # HOME
        time.sleep(1)

        print("✅ Test PASSED.")

    except NoSuchElementException as e:
        print(f"❌ Element NOT found: {e}")
    except Exception as e:
        print(f"❌ Test FAILED: {e}")
    finally:
        print("📱 Closing mobile session...")
        driver.quit()


if __name__ == "__main__":
    test_toggle_dark_theme()