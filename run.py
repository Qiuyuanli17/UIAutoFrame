import time
from core.driver.driver_manager import DriverManager
from core.executor.action_executor import ActionExecutor
from core.utils.points_loader import load_points
from pages.home_page import HomePage
from workflows.custom_points_flow import CustomPointsFlow
from workflows.home_navigation_flow import HomeNavigationFlow
from core.logger.logger import setup_logger

DEVICE_NAME = 'AU6NBB5328000488'             # 设备名称

def main():
    caps = {
        'platformName': 'Android',           # 平台名称
        'platformVersion': '15',             # 安卓版本号（可通过 adb shell getprop ro.build.version.release 查看）
        'deviceName': DEVICE_NAME,    # 设备名称（可随意填写） AU6NBB5313000930（白色） A6XYBB4C17000140（黑色）
        'appPackage': 'com.ultrasound.peninsula',     # 应用的包名（请修改为你的应用包名）
        'appActivity': 'com.ultrasound.usdemo.MainActivity',      # 启动的Activity（请修改为你的主Activity）
        'noReset': True,                     # 不重置应用数据
        'newCommandTimeout': 600,            # 命令超时时间（秒）
        'automationName': 'UiAutomator2'    # 自动化引擎
    }

    dm = DriverManager("http://127.0.0.1:4723", caps)
    driver = dm.start()

    print("session id:", driver.session_id)

    # 初始化日志配置
    setup_logger()

    # TODO:未做断言，失败截屏，testcases整理，测试报告，整理requirements

    #---------------临时验证点-----------------
    points = load_points()
    executor  = ActionExecutor(driver, points)


    flow = CustomPointsFlow(executor)
    result = flow.run_full_flow()

    print("custom points result:", result)
    # 👉 临时验证点位
    # ex.click_point(HomePage.CUSTOM_POINTS)
    # time.sleep(1)
    # ex.click_point("common.back")
    # flow = HomeNavigationFlow(ex)
    # flow.enter_intelligent_detection_and_back()

    # flow = CustomPointsFlow(ex)
    # flow.open_point_and_back()
    



if __name__ == "__main__":
    main()
