import time
import logging
from core.utils.retry import retry


class ActionExecutor:
    """动作执行器 - 封装所有底层 UI 操作"""

    def __init__(self, driver, points=None, action_interval=0.5):
        self.driver = driver
        self.points = points or {}
        self.action_interval = action_interval

    @retry(max_attempts=2, interval=1)
    def click(self, x, y):
        """点击坐标"""
        logging.info(f"[ACTION] 点击坐标: ({x}, {y})")
        self.driver.tap([(int(x), int(y))], 100)
        time.sleep(self.action_interval)

    @retry(max_attempts=2, interval=1)
    def input(self, x, y, text):
        """点击坐标后输入文本"""
        logging.info(f"[ACTION] 点击 ({x}, {y}) 并输入: {text}")
        self.click(x, y)
        self.driver.execute_script("mobile: type", {"text": str(text)})
        time.sleep(self.action_interval)

    @retry(max_attempts=2, interval=1)
    def double_click(self, x, y):
        """双击坐标"""
        logging.info(f"[ACTION] 双击坐标: ({x}, {y})")
        self.driver.execute_script('mobile: doubleClickGesture', {
            'x': int(x),
            'y': int(y)
        })
        time.sleep(self.action_interval)

    def swipe(self, center_x, top_y, bottom_y, repeat=3, duration=300):
        """滑动操作"""
        logging.info(f"[ACTION] 滑动: center_x={center_x}, 从 {top_y} 到 {bottom_y}")
        pause = 0.05

        for _ in range(repeat):
            self.driver.swipe(
                int(center_x),
                int(top_y),
                int(center_x),
                int(bottom_y),
                duration
            )
            time.sleep(pause)

    def click_point(self, point_name):
        """
        通过点位名称点击（从 points.yaml 加载）
        point_name: 'home.intelligent_detection'
        """
        logging.info(f"[ACTION] click_point: {point_name}")
        
        try:
            keys = point_name.split(".")
            p = self.points
            for k in keys:
                p = p[k]

            self.click(p["x"], p["y"])
        except Exception as e:
            logging.error(f"[ERROR] click_point 失败: {point_name}, error={e}")
            raise

    def input_point(self, point_name, text):
        """通过点位名称输入文本"""
        logging.info(f"[ACTION] input_point: {point_name}, text={text}")
        
        try:
            keys = point_name.split(".")
            p = self.points
            for k in keys:
                p = p[k]

            self.input(p["x"], p["y"], text)
        except Exception as e:
            logging.error(f"[ERROR] input_point 失败: {point_name}, error={e}")
            raise
    