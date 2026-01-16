from appium import webdriver
from appium.options.android import UiAutomator2Options
import time
import logging


class DriverManager:

    def __init__(self, appium_url, caps):
        self.appium_url = appium_url
        self.caps = caps
        self.driver = None

    def start(self):
        """启动 Appium 会话"""
        logging.info(f"正在连接 Appium 服务器: {self.appium_url}")
        self.driver = webdriver.Remote(
            self.appium_url,
            options=UiAutomator2Options().load_capabilities(self.caps)
        )
        logging.info(f"连接成功，会话ID: {self.driver.session_id}")
        self.activate_app()
        return self.driver

    def quit(self):
        """关闭 Appium 会话"""
        if self.driver:
            try:
                self.driver.quit()
                logging.info("驱动已关闭")
            except Exception as e:
                logging.error(f"关闭驱动失败: {e}")

    def activate_app(self):
        """确保 App 在前台"""
        try:
            self.driver.activate_app(self.caps['appPackage'])
            logging.info(f"应用已激活: {self.caps['appPackage']}")
        except Exception as e:
            logging.warning(f"激活应用失败: {e}")

    def check_session_valid(self):
        """检查会话是否有效"""
        try:
            _ = self.driver.session_id
            return True
        except Exception:
            return False

    #TODO:未添加返回到主界面，可以测试一下
    def restart_session(self):
        """重启 Appium 会话"""
        logging.info("正在重启 Appium 会话...")
        try:
            # 先关闭当前会话
            try:
                self.driver.quit()
            except:
                pass
            
            time.sleep(5)
            
            # 重新启动
            self.driver = webdriver.Remote(
                self.appium_url,
                options=UiAutomator2Options().load_capabilities(self.caps)
            )
            logging.info("Appium 会话重启成功")
            
            # 重新激活应用
            self.activate_app()
            time.sleep(3)
            return True
            
        except Exception as e:
            logging.error(f"重启 Appium 会话失败: {e}")
            return False