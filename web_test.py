from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import os

def test_search_duckduckgo():
    print("🕷️ Starting Web Automation Test (DuckDuckGo)...")

    # Browser config (local vs CI)
    options = Options()
    if os.getenv("CI") == "true":
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
    else:
        options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 10)

    try:
        driver.get("https://duckduckgo.com/")
        print("🌍 Page loaded!")

        print("⌨️ Typing into search box...")
        search_box = wait.until(
            EC.presence_of_element_located((By.ID, "searchbox_input"))
        )
        search_box.clear()
        search_box.send_keys("Appium mobile automation", Keys.ENTER)

        print("🔍 Waiting for search results...")
        results = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[data-testid='result-title-a']"))
        )

        if len(results) > 0:
            print(f"✅ Search results are displayed. Found {len(results)} items.")
            print("🎉 Test passed!")
        else:
            print("❌ No results found. Test failed!")

    except Exception as e:
        print(f"❌ Exception during test: {e}")

    finally:
        print("🧹 Closing browser...")
        time.sleep(2)
        driver.quit()


if __name__ == "__main__":
    test_search_duckduckgo()