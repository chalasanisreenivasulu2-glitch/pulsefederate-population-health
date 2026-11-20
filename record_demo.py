from playwright.sync_api import sync_playwright
import time

def record_demo():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=150)
        context = browser.new_context(record_video_dir="videos/", record_video_size={"width": 1280, "height": 720})
        page = context.new_page()
        page.set_default_timeout(180000)
        try:
            print("[1/6] Home page")
            page.goto("http://localhost:3000/")
            page.wait_for_load_state("networkidle")
            time.sleep(4)
            print("[2/6] Admin page")
            page.goto("http://localhost:3000/admin")
            page.wait_for_load_state("networkidle")
            time.sleep(4)
            print("[3/6] Clicking to train")
            train_btn = page.locator("button:has-text('Run Federated Training')")
            train_btn.wait_for(state="visible", timeout=10000)
            time.sleep(2)
            train_btn.click()
            time.sleep(3)
            print("Waiting for results...")
            page.wait_for_selector("text=Final Accuracy", timeout=180000)
            print("Results appeared!")
            time.sleep(8)
            print("[4/6] Hospital page")
            page.goto("http://localhost:3000/hospital")
            page.wait_for_load_state("networkidle")
            time.sleep(5)
            print("[5/6] Swagger Docs")
            page.goto("http://localhost:8000/docs")
            page.wait_for_load_state("networkidle")
            time.sleep(4)
            print("[6/6] Clicking /api/train in Swagger")
            try:
                page.locator("button:has-text('/api/train')").first.click(timeout=5000)
            except:
                page.locator("text=/api/train").first.click(timeout=5000)
            time.sleep(6)
            print("SUCCESS")
        except Exception as e:
            print(f"FAILED: {e}")
            page.screenshot(path="failure-screenshot.png")
            raise
        finally:
            context.close()
            browser.close()
            print("Video saved")

if __name__ == "__main__":
    record_demo()