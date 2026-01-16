"""
快速调试入口
仅用于开发阶段快速验证功能，正式测试请使用 testcases 下的 pytest 用例
"""
import logging
from core.driver.driver_manager import DriverManager
from core.executor.action_executor import ActionExecutor
from core.utils.points_loader import load_points
from core.utils.config_loader import ConfigLoader
from core.logger.logger import setup_logger
from workflows.custom_points_flow import CustomPointsFlow

# TODO:未做断言，失败截屏，testcases整理，测试报告，整理requirements
# TODO:是否需要将日志，截图，报告以时间戳方式展示
# TODO:后续怎么串联多个流程模块测试，按顺序执行testcases？
# TODO:logger.py和pytest.ini是否冲突
def main():
    # 初始化日志
    setup_logger()
    logging.info("=" * 60)
    logging.info("快速调试运行开始")
    logging.info("=" * 60)

    # 加载配置
    config_loader = ConfigLoader()
    caps = config_loader.get_merged_caps(device_key="default", app_key="peninsula")
    env_config = config_loader.get_env_config()
    
    logging.info(f"使用设备: {caps['deviceName']}")
    logging.info(f"测试应用: {caps['appPackage']}")

    # 启动驱动
    dm = DriverManager(env_config['appium']['server_url'], caps)
    driver = dm.start()

    try:
        # 加载坐标点位
        points = load_points()
        executor = ActionExecutor(driver, points)

        # 执行自定义点位流程
        flow = CustomPointsFlow(executor)
        result = flow.run_full_flow()

        logging.info(f"流程执行完成，返回值: {result}")

    except Exception as e:
        logging.error(f"执行失败: {e}", exc_info=True)
    
    finally:
        # 清理资源
        dm.quit()
        logging.info("=" * 60)
        logging.info("快速调试运行结束")
        logging.info("=" * 60)


if __name__ == "__main__":
    main()
