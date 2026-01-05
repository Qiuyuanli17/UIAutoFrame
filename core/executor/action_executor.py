import time
import logging

class ActionExecutor:

    def __init__(self, driver, points=None):
        self.driver = driver
        self.points = points or {}

    def click(self, x, y):
        self.driver.tap([(int(x), int(y))], 100)
        time.sleep(0.5)

    def input(self, x, y, text):
        self.click(x, y)
        self.driver.execute_script("mobile: type", {"text": str(text)})
        time.sleep(0.3)

    def double_click(self, x, y):
        self.driver.execute_script('mobile: doubleClickGesture',{
            'x':int(x),
            'y':int(y)
        })
        time.sleep(0.3)

    def swipe(self,center_x,top_y,bottom_y):
        # repeat = 3      #上滑次数
        # pause = 0.05    #滑动后的暂停时间
        # duration = 300  #滑动时长

        # start_y = int(bottom_y * 0.8)  # 从底部80%位置开始
        # end_y = int(top_y * 0.3)       # 到顶部30%位置结束

        # for i in range(repeat):
        #     self.driver.swipe(center_x, start_y, center_x, end_y, duration)
        #     time.sleep(pause)

        repeat = 3
        pause = 0.05
        duration = 300

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
            logging.error(f"[ERROR] click_point failed: {point_name}, error={e}")
            raise
    