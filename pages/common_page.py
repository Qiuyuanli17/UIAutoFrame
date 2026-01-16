import logging


class CommonPage:
    """通用页面 - 跨页面的公共元素和操作"""
    
    # 元素定位
    BACK = "common.back"
    
    def __init__(self, executor):
        self.ex = executor
    
    def go_back(self):
        """返回上一页"""
        logging.info("[CommonPage] 点击返回")
        self.ex.click_point(self.BACK)