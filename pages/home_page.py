import logging


class HomePage:
    """主页 - 四个主功能入口"""
    
    # 元素定位
    INTELLIGENT_DETECTION = "home.intelligent_detection"
    CUSTOM_POINTS = "home.custom_points"
    MEDICAL_RECORD = "home.medical_record"
    ROUTINE_DETECTION = "home.routine_detection"
    
    def __init__(self, executor):
        self.ex = executor
    
    def goto_intelligent_detection(self):
        """进入智能检测"""
        logging.info("[HomePage] 进入智能检测")
        self.ex.click_point(self.INTELLIGENT_DETECTION)
    
    def goto_custom_points(self):
        """进入自定义点位"""
        logging.info("[HomePage] 进入自定义点位")
        self.ex.click_point(self.CUSTOM_POINTS)
    
    def goto_medical_record(self):
        """进入用户档案"""
        logging.info("[HomePage] 进入用户档案")
        self.ex.click_point(self.MEDICAL_RECORD)
    
    def goto_routine_detection(self):
        """进入常规检测"""
        logging.info("[HomePage] 进入常规检测")
        self.ex.click_point(self.ROUTINE_DETECTION)
    