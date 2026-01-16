import logging
import time


class CustomPointsPage:
    """自定义点位页面"""
    
    # 元素定位
    ADD = "custom_points.add"
    DELETE = "custom_points.delete"
    EDIT = "custom_points.edit"
    RESTORE = "custom_points.restore"
    FINISH = "custom_points.finish"
    FRONT_FACE = "custom_points.front_face"
    SIDE_FACE = "custom_points.side_face"
    SUBMENTUM = "custom_points.submentum"
    POINT_ITEM = "custom_points.point_item"
    
    def __init__(self, executor):
        self.ex = executor
    
    def click_front_face(self):
        """点击正脸"""
        logging.info("[CustomPointsPage] 点击正脸")
        self.ex.click_point(self.FRONT_FACE)
    
    def click_side_face(self):
        """点击侧脸"""
        logging.info("[CustomPointsPage] 点击侧脸")
        self.ex.click_point(self.SIDE_FACE)
    
    def click_submentum(self):
        """点击颏下"""
        logging.info("[CustomPointsPage] 点击颏下")
        self.ex.click_point(self.SUBMENTUM)
    
    def click_first_point(self):
        """点击第一个点位"""
        logging.info("[CustomPointsPage] 点击第一个点位")
        self.ex.click_point(self.POINT_ITEM)
    
    def click_edit(self):
        """点击编辑"""
        logging.info("[CustomPointsPage] 点击编辑")
        self.ex.click_point(self.EDIT)
    
    def click_restore(self):
        """点击还原"""
        logging.info("[CustomPointsPage] 点击还原")
        self.ex.click_point(self.RESTORE)
    
    def click_add(self):
        """点击添加（单次）"""
        logging.info("[CustomPointsPage] 点击添加")
        self.ex.click_point(self.ADD)
    
    def click_delete(self):
        """点击删除（单次）"""
        logging.info("[CustomPointsPage] 点击删除")
        self.ex.click_point(self.DELETE)
    
    def click_finish(self):
        """点击完成"""
        logging.info("[CustomPointsPage] 点击完成")
        self.ex.click_point(self.FINISH)
    
    def add_points(self, count):
        """批量添加点位"""
        logging.info(f"[CustomPointsPage] 批量添加点位: {count} 次")
        for _ in range(count):
            self.click_add()
    
    def delete_points(self, count):
        """批量删除点位"""
        logging.info(f"[CustomPointsPage] 批量删除点位: {count} 次")
        for _ in range(count):
            self.click_delete()