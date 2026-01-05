from appium import webdriver
from appium.options.android import UiAutomator2Options
import time


class DriverManager:

    def __init__(self, appium_url, caps):
        self.appium_url = appium_url
        self.caps = caps
        self.driver = None

    def start(self):
        self.driver = webdriver.Remote(
            self.appium_url,
            options=UiAutomator2Options().load_capabilities(self.caps)
        )
        self.activate_app()
        return self.driver

    def quit(self):
        if self.driver:
            self.driver.quit()

    def activate_app(self):
        """
        确保 App 在前台
        """
        try:
            self.driver.activate_app(self.caps['appPackage'])
        except Exception as e:
            print(f"[WARN] activate_app failed: {e}")

    #TODO：暂未迁移 【确认当前前台应用】 【check_session_valid】 【restart_appium_session】