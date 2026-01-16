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
    """自定义点位业务流程"""

    def __init__(self, executor):
        self.ex = executor
        self.home_page = HomePage(executor)
        self.custom_page = CustomPointsPage(executor)
        self.common_page = CommonPage(executor)

    def run_full_flow(self):
        """
        执行完整的自定义点位流程
        
        Returns:
            list: [first, 2, 1, last] 用于后续检测流程
        """
        logging.info("=" * 50)
        logging.info("【自定义点位】开始完整流程")
        logging.info("=" * 50)

        # 1. 进入自定义点位
        self.home_page.goto_custom_points()

        # 2. 选择人脸朝向
        self.custom_page.click_front_face()
        self.custom_page.click_side_face()
        self.custom_page.click_submentum()

        # 3. 打开第一个点位
        self.custom_page.click_first_point()

        # 4. 进入编辑模式并还原
        self.custom_page.click_edit()
        self.custom_page.click_restore()

        # 5. 随机删除点位
        del_count = random.randint(1, 10)
        logging.info(f"【自定义点位】准备删除点位数: {del_count}")
        self.custom_page.delete_points(del_count)

        # 6. 随机添加点位
        add_count = random.randint(1, 10)
        logging.info(f"【自定义点位】准备添加点位数: {add_count}")
        self.custom_page.add_points(add_count)

        # 7. 完成编辑并返回
        self.custom_page.click_finish()
        self.common_page.go_back()

        # 8. 计算最终点位数
        final_points = compute_custom_points(del_count, add_count)
        first, last = split_points_for_values(final_points)
        
        logging.info(f"【自定义点位】删除次数: {del_count}, 添加次数: {add_count}")
        logging.info(f"【自定义点位】最终点位总数: {final_points}")
        logging.info(f"【自定义点位】返回值: [{first}, 2, 1, {last}]")
        logging.info("=" * 50)

        return [first, 2, 1, last]

    def run_simple_flow(self):
        """
        简化流程：仅进入自定义点位页面并返回
        """
        logging.info("【自定义点位】执行简化流程")
        self.home_page.goto_custom_points()
        self.common_page.go_back()