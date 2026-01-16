import os
from datetime import datetime


class ScreenshotHelper:
    """截图辅助类"""

    def __init__(self, driver, save_path="artifacts/screenshots"):
        self.driver = driver
        self.save_path = save_path
        os.makedirs(self.save_path, exist_ok=True)

    def take_screenshot(self, name="screenshot"):
        """截图并保存"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{timestamp}.png"
        filepath = os.path.join(self.save_path, filename)
        
        try:
            self.driver.save_screenshot(filepath)
            return filepath
        except Exception as e:
            print(f"截图失败: {e}")
            return None
