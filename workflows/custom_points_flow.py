import random
import logging
from pages.common_page import CommonPage
from pages.home_page import HomePage
from pages.custom_points_page import CustomPointsPage
from core.utils.custom_points_calc import (
    compute_custom_points,
    split_points_for_values
)

class CustomPointsFlow:

    def __init__(self, executor):
        self.ex = executor

    def enter_custom_points(self):
        self.ex.click_point(HomePage.CUSTOM_POINTS)

    def select_face_parts(self):
        self.ex.click_point(CustomPointsPage.FRONT_FACE)      # 正脸
        self.ex.click_point(CustomPointsPage.SIDE_FACE)       # 侧脸
        self.ex.click_point(CustomPointsPage.SUBMENTUM)       # 颏下

    def open_first_point(self):
        self.ex.click_point(CustomPointsPage.POINT_ITEM)

    def reset_points(self):
        self.ex.click_point(CustomPointsPage.EDIT)  # 编辑
        self.ex.click_point(CustomPointsPage.RESTORE)  # 还原

    def delete_points(self):
        del_count = random.randint(1, 10)
        for _ in range(del_count):
            self.ex.click_point(CustomPointsPage.DELETE)
        return del_count

    def add_points(self):
        add_count = random.randint(1, 10)
        for _ in range(add_count):
            self.ex.click_point(CustomPointsPage.ADD)
        return add_count

    def finish_and_back(self):
        self.ex.click_point(CustomPointsPage.FINISH)
        self.ex.click_point(CommonPage.BACK)

    def run_full_flow(self):
        """
        执行完整的自定义点位流程（等价于原一次性脚本）
        """

        logging.info("【自定义点位】开始完整流程")

        self.enter_custom_points()
        logging.info("【自定义点位】进入自定义点位页面")

        self.select_face_parts()
        logging.info("【自定义点位】遍历人脸朝向")

        self.open_first_point()
        logging.info("【自定义点位】点击第一个点位")

        self.reset_points()
        logging.info("【自定义点位】点位还原完成")

        del_count = self.delete_points()
        logging.info(f"【自定义点位】删除点位数: {del_count}")

        add_count = self.add_points()
        logging.info(f"【自定义点位】新增点位数: {add_count}")

        self.finish_and_back()
        logging.info("【自定义点位】完成并返回")

        final_points = compute_custom_points(del_count, add_count)
        first, last = split_points_for_values(final_points)
        logging.info(f"【自定义点位】最终点位结果: {final_points}")

        return [first, 2, 1, last]