"""
自定义点位功能测试用例
"""
import pytest
import logging
from core.driver.driver_manager import DriverManager
from core.executor.action_executor import ActionExecutor
from core.utils.points_loader import load_points
from core.utils.config_loader import ConfigLoader
from core.logger.logger import setup_logger
from core.utils.screenshot import ScreenshotHelper
from core.assertion.base_assert import BaseAssert
from workflows.custom_points_flow import CustomPointsFlow


@pytest.fixture(scope="session")
def driver():
    """会话级别的 driver fixture"""
    setup_logger()
    
    config_loader = ConfigLoader()
    caps = config_loader.get_merged_caps(device_key="default", app_key="peninsula")
    env_config = config_loader.get_env_config()
    
    dm = DriverManager(env_config['appium']['server_url'], caps)
    driver = dm.start()
    
    yield driver
    
    dm.quit()


@pytest.fixture(scope="function")
def executor(driver):
    """用例级别的 executor fixture"""
    points = load_points()
    return ActionExecutor(driver, points)


@pytest.fixture(scope="function")
def screenshot_helper(driver):
    """用例级别的截图助手 fixture"""
    return ScreenshotHelper(driver)


class TestCustomPoints:
    """自定义点位测试类"""

    def test_custom_points_full_flow(self, executor):
        """测试自定义点位完整流程"""
        logging.info("=" * 60)
        logging.info("开始测试: test_custom_points_full_flow")
        logging.info("=" * 60)
        
        flow = CustomPointsFlow(executor)
        result = flow.run_full_flow()
        
        # 断言返回值格式正确
        assert isinstance(result, list), "返回值应为列表"
        assert len(result) == 4, "返回值应包含4个元素"
        assert result[1] == 2 and result[2] == 1, "中间两位应为 [2, 1]"
        
        logging.info(f"测试通过，返回值: {result}")

    def test_custom_points_simple_flow(self, executor):
        """测试自定义点位简化流程"""
        logging.info("=" * 60)
        logging.info("开始测试: test_custom_points_simple_flow")
        logging.info("=" * 60)
        
        flow = CustomPointsFlow(executor)
        flow.run_simple_flow()
        
        logging.info("简化流程测试完成")

    @pytest.mark.parametrize("del_count,add_count", [
        (1, 1),
        (5, 3),
        (2, 8),
    ])
    def test_custom_points_calc(self, del_count, add_count):
        """测试点位计算逻辑"""
        from core.utils.custom_points_calc import compute_custom_points, split_points_for_values
        
        final_points = compute_custom_points(del_count, add_count)
        first, last = split_points_for_values(final_points)
        
        logging.info(f"删除: {del_count}, 添加: {add_count}, 最终点位: {final_points}, 拆分: [{first}, {last}]")
        
        assert final_points > 0, "最终点位数应大于0"
        assert first > 0 and last > 0, "拆分后的值应大于0"
