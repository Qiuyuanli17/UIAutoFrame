import logging
from core.utils.screenshot import ScreenshotHelper

#TODO：实际上元素无 resource-id class content-desc xpath UIAutomator（text instance index），后续改成图像识别断言？opencv,ocr
class BaseAssert:
    """基础断言类"""

    def __init__(self, driver, screenshot_helper=None):
        self.driver = driver
        self.screenshot_helper = screenshot_helper

    def _take_screenshot_on_failure(self, name):
        """断言失败时截图"""
        if self.screenshot_helper:
            filepath = self.screenshot_helper.take_screenshot(name)
            logging.error(f"断言失败截图已保存: {filepath}")

    def assert_element_exists(self, locator, message="元素不存在"):
        """断言元素存在"""
        try:
            elements = self.driver.find_elements(*locator)
            assert len(elements) > 0, message
            logging.info(f"[ASSERT] 元素存在检查通过: {locator}")
            return True
        except AssertionError as e:
            self._take_screenshot_on_failure("assert_element_exists_failed")
            logging.error(f"[ASSERT] {message}")
            raise

    def assert_text_in_element(self, locator, expected_text, message="文本不匹配"):
        """断言元素包含指定文本"""
        try:
            element = self.driver.find_element(*locator)
            actual_text = element.text
            assert expected_text in actual_text, f"{message}. 预期: {expected_text}, 实际: {actual_text}"
            logging.info(f"[ASSERT] 文本匹配检查通过: {expected_text}")
            return True
        except AssertionError as e:
            self._take_screenshot_on_failure("assert_text_failed")
            logging.error(f"[ASSERT] {e}")
            raise

    def assert_element_visible(self, locator, message="元素不可见"):
        """断言元素可见"""
        try:
            element = self.driver.find_element(*locator)
            assert element.is_displayed(), message
            logging.info(f"[ASSERT] 元素可见检查通过: {locator}")
            return True
        except AssertionError as e:
            self._take_screenshot_on_failure("assert_visible_failed")
            logging.error(f"[ASSERT] {message}")
            raise
