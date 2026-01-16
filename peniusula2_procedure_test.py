from appium import webdriver
from selenium.webdriver.common.by import By
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.options.android import UiAutomator2Options
import time
import hashlib
import random
import string


# ============ 配置区域 ============

APPIUM_SERVER_URL = 'http://localhost:4723'  # Appium服务器地址
DEVICE_NAME = 'AU6NBB5328000488'             # 设备名称
EXECUTE_COUNT = 1                           # 流程循环次数


# 请根据你的实际情况修改以下配置
desired_caps = {
    'platformName': 'Android',           # 平台名称
    'platformVersion': '15',             # 安卓版本号（可通过 adb shell getprop ro.build.version.release 查看）
    'deviceName': DEVICE_NAME,    # 设备名称（可随意填写） AU6NBB5313000930（白色） A6XYBB4C17000140（黑色）
    'appPackage': 'com.ultrasound.peninsula',     # 应用的包名（请修改为你的应用包名）
    'appActivity': 'com.ultrasound.usdemo.MainActivity',      # 启动的Activity（请修改为你的主Activity）
    'noReset': True,                     # 不重置应用数据
    'newCommandTimeout': 600,            # 命令超时时间（秒）
    'automationName': 'UiAutomator2'    # 自动化引擎
}
# ============ 初始化驱动 ============
print("正在连接Appium服务器...")
driver = webdriver.Remote(
    APPIUM_SERVER_URL,
    options=UiAutomator2Options().load_capabilities(desired_caps)
)
print(f"连接成功！会话ID: {driver.session_id}")

# 尝试强制启动并前置应用
pkg = desired_caps.get('appPackage')
act = desired_caps.get('appActivity')
try:
    print("尝试激活应用...")
    driver.activate_app(pkg)
except Exception as e1:
    print(f"activate_app 失败: {e1}")
    try:
        # 确保 Activity 为全类名
        full_act = act if act.startswith('.') or '.' in act else f".{act}"
        print(f"尝试 start_activity: {pkg}/{full_act}")
        driver.start_activity(pkg, full_act)
    except Exception as e2:
        print(f"start_activity 也失败: {e2}")

# 确认当前前台应用
try:
    print(f"当前包名: {driver.current_package}")
    print(f"当前Activity: {getattr(driver, 'current_activity', 'N/A')}")
    if driver.current_package != pkg:
        print("警告：当前不在目标应用，再次尝试激活...")
        driver.activate_app(pkg)
except Exception as e3:
    print(f"获取当前应用信息失败: {e3}")

# 设置等待时间（此处设置，确保 driver 已就绪）
wait = WebDriverWait(driver, 10)
driver.implicitly_wait(5)

# ============ 辅助函数 ============
def check_session_valid():
    """检查会话是否有效"""
    try:
        _ = driver.session_id
        return True
    except Exception:
        return False

def restart_appium_session():
    """
    重启 Appium 会话
    """
    print(" 正在重启 Appium 会话...")
    global driver
    
    try:
        # 先尝试优雅关闭
        try:
            driver.quit()
        except:
            pass
        
        # 等待一段时间让资源释放
        time.sleep(5)
        
        # 重新初始化驱动
        driver = webdriver.Remote(
            APPIUM_SERVER_URL,
            options=UiAutomator2Options().load_capabilities(desired_caps)
        )
        print("√ Appium 会话重启成功")
        
        # 重新激活应用
        pkg = desired_caps.get('appPackage')
        try:
            driver.activate_app(pkg)
            time.sleep(3)
        except Exception as e:
            print(f"激活应用失败: {e}")
            
 # ============ 新增：返回到主界面 ============
        print(" 正在返回到主界面...")
        
        def is_on_main_interface():
            """通过检查'设置'元素判断是否在主界面"""
            try:
                # 使用 accessibility id 查找"设置"元素
                setting_element = driver.find_element(AppiumBy.ACCESSIBILITY_ID, "设置")
                return setting_element is not None and setting_element.is_displayed()
            except Exception:
                return False
        
        # 先检查是否已经在主界面
        if is_on_main_interface():
            print("√ 当前已在主界面")
            return True
        
        # 方法1: 直接重启应用
        try:
            driver.terminate_app(pkg)
            time.sleep(2)
            driver.activate_app(pkg)
            time.sleep(3)
            print("√ 应用重启完成")
        except Exception as e:
            print(f"重启应用失败: {e}")
        
        # 方法2: 检查是否在软件主界面，如果不是则点击主界面元素
        if not is_on_main_interface():
            print(" 不在软件主界面，尝试点击主界面元素...")
            try:
                # 尝试点击主界面的某个元素，比如"智能检测"
                click_by_coordinates(1096, 763)
                time.sleep(2)
            except Exception as e:
                print(f"点击主界面元素失败: {e}")
        
        # 最终确认是否在主界面
        if is_on_main_interface():
            print("√ 已回到软件主界面")
            return True
        else:
            print("× 无法回到软件主界面")
            return False
        # ============ 新增结束 ============

        
        
    except Exception as e:
        print(f"× 重启 Appium 会话失败: {e}")
        return False

# ====================点击函数======================
def click_by_coordinates(x, y, duration=100):
    """
    通过坐标点击屏幕
    :param x: X坐标
    :param y: Y坐标
    :param duration: 点击持续时间（毫秒），默认100ms
    """
    driver.tap([(x, y)], duration)
    print(f"点击坐标: ({x}, {y})")
    time.sleep(0.5)  # 点击后短暂等待

def uiautomator_double_tap(x, y):
    """
    修复版UIAutomator2双击 - 只使用支持的doubleClickGesture命令
    """
    try:
        print(f"🔧 UIAutomator2双击: 坐标({x}, {y})")
        
        # 直接使用支持的doubleClickGesture命令
        driver.execute_script('mobile: doubleClickGesture', {
            'x': int(x), 
            'y': int(y)
        })
        
        print(f"UIAutomator2双击成功")
        time.sleep(0.3)
        return True
        
    except Exception as e:
        print(f"UIAutomator2双击失败: {e}")
        return False

def click_and_input(x, y, text, wait_time=1):
    """
    点击坐标后，在弹出的输入框中输入数据
    :param x: 点击的X坐标
    :param y: 点击的Y坐标
    :param text: 要输入的文字
    :param wait_time: 点击后等待输入框出现的时间（秒）
    """
    # 先点击坐标
    click_by_coordinates(x, y)
    time.sleep(wait_time)
    
    # 方法4: 使用mobile: type命令（Appium UiAutomator2支持）[有效]
    try:
        driver.execute_script('mobile: type', {'text': text})
        print(f"通过mobile:type输入文本: {text}")
        time.sleep(0.5)
        return
    except:
        pass

    # 方法1: 尝试找到聚焦的EditText输入
    try:
        input_element = driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().className("android.widget.EditText").focused(true)'
        )
        input_element.clear()
        input_element.send_keys(text)
        print(f"输入文本1: {text}")
        time.sleep(0.5)
        return
    except:
        pass
    
    # 方法2: 尝试找到所有EditText，点击第一个可见的
    try:
        input_elements = driver.find_elements(AppiumBy.CLASS_NAME, 'android.widget.EditText')
        for element in input_elements:
            if element.is_displayed():
                element.click()
                time.sleep(0.3)
                element.clear()
                element.send_keys(text)
                print(f"输入文本2: {text}")
                time.sleep(0.5)
                return
    except:
        pass
    
    # 方法3: 使用ADB命令直接输入（如果Appium支持）
    try:
        driver.execute_script('mobile: shell', {
            'command': 'input',
            'args': ['text', text]
        })
        print(f"通过ADB输入文本: {text}")
        time.sleep(0.5)
        return
    except:
        pass
    

    
    print(f"警告: 无法找到输入框，已尝试多种方法输入文本: {text}")


def scroll_list_top_to_bottom_fast(list_center_x, list_top_y, list_bottom_y, repeat=3, duration=300, pause=0.05):
    """
    快速在列表区域内从下往上滑动，使内容从最顶端滚到最底端。
    :param list_center_x: 列表区域中线X坐标
    :param list_top_y: 列表可视区域顶部Y
    :param list_bottom_y: 列表可视区域底部Y
    :param repeat: 上滑次数（减少到3-4次）
    :param duration: 每次滑动时长（减少到300ms）
    :param pause: 每次滑动后的暂停（减少到0.05秒）
    """
    # 增加滑动距离 - 从更靠下的位置开始，到更靠上的位置结束
    start_y = int(list_bottom_y * 0.8)  # 从底部80%位置开始
    end_y = int(list_top_y * 0.3)       # 到顶部30%位置结束
    
    for i in range(repeat):
        print(f"  快速上滑 {i+1}/{repeat}")
        driver.swipe(list_center_x, start_y, list_center_x, end_y, duration)
        time.sleep(pause)

# =====================工具函数========================
def get_id_value(driver):
    """
    获取以"ID："开头的元素并提取ID值（适用于新版本Appium）
    
    Returns:
        str: ID值，如果找不到返回None
    """
    try:
        # 使用新的查找元素方式
        elements = driver.find_elements(AppiumBy.XPATH, "//*[starts-with(@text, 'ID:')]")
        
        if not elements:
            # 如果text属性没有，尝试content-desc
            elements = driver.find_elements(AppiumBy.XPATH, "//*[starts-with(@content-desc, 'ID:')]")
        
        if elements:
            # 获取第一个匹配元素的文本
            element = elements[0]
            full_text = element.get_attribute("text") or element.get_attribute("content-desc")
            
            if full_text:
                # 提取"ID："后面的值
                id_value = full_text.replace("ID:", "").strip()
                print(f"找到ID元素: {full_text}")
                print(f"提取的ID值: {id_value}")
                return id_value
        
        print("未找到以'ID:'开头的元素")
        return None
        
    except Exception as e:
        print(f"获取ID值失败: {e}")
        return None

def generate_unique_phone():
    """
    生成唯一的11位手机号码，确保每次调用都不同
    使用时间戳+随机数来保证唯一性
    """
    # 获取当前时间戳的最后几位作为基础
    timestamp_part = str(int(time.time() * 1000000))[-6:]
    
    # 生成随机部分
    random_part = ''.join([str(random.randint(0, 9)) for _ in range(5)])
    
    # 组合成11位手机号 (1 + 随机第二位 + 时间戳部分 + 随机部分)
    second_digit = str(random.randint(3, 9))
    phone_number = '1' + second_digit + timestamp_part + random_part
    
    # 确保长度是11位
    phone_number = phone_number[:11]
    
    return phone_number

def generate_random_name():
    """
    生成随机字母组合的名字（1-5个字符）
    """
    # 使用当前时间的纳秒部分作为随机种子
    random.seed(time.time_ns())
    
    # 随机决定名字长度（1-5个字符）
    name_length = random.randint(1, 5)
    
    # 生成随机字母组合
    # 首字母大写，其余小写
    first_letter = random.choice(string.ascii_uppercase)
    other_letters = ''.join(random.choice(string.ascii_lowercase) for _ in range(name_length - 1))
    
    return first_letter + other_letters

def random_age_selection(picker_center_x, picker_top_y, picker_bottom_y):
    """
    在年龄选择器中随机滑动选择年龄
    """
    # 计算选择器中间位置（Y坐标）
    picker_center_y = (picker_top_y + picker_bottom_y) // 2
    
    # 计算选择器高度
    picker_height = picker_bottom_y - picker_top_y
    
    # 随机选择滑动方向和距离
    direction = random.choice([-1, 1])  # -1向上，1向下
    swipe_distance = random.randint(picker_height // 4, picker_height // 2)
    
    # 计算起始和结束位置
    start_y = picker_center_y
    end_y = start_y + (direction * swipe_distance)
    
    # 确保不超出选择器范围
    end_y = max(picker_top_y, min(picker_bottom_y, end_y))
    
    # 执行滑动
    driver.swipe(picker_center_x, start_y, picker_center_x, end_y, 300)
    print(f"随机滑动选择年龄: 从 {start_y} 到 {end_y}")
    time.sleep(0.5)


def get_version_random_coordinates(detection_type="智能检测"):
    """
    根据检测类型随机选择坐标和对应的数值元组
    
    Args:
        detection_type: 检测类型，可选"智能检测"或"再次检测"，默认为"智能检测"
    
    Returns:
        list: [检测类型字符串, 坐标位置, 数值元组]
    """
    
    # 智能检测的三个版本坐标和数值
    smart_detection_versions = [
        {
            "version":"标准版",
            "coordinates": (942, 597),
            "values": [4, 2 , 1 ,5]
        },
        {   
            "version":"全案版",
            "coordinates": (1500, 597),
            "values": [11 , 2 , 1 , 11]
        },
        {   
            "version":"自定义",
            "coordinates": (2059, 597),
            "values": [2 , 2 , 1 ,3]
        }
    ]
    
    # 再次检测的三个版本坐标和数值
    redetection_versions = [
        {    
            "version":"标准版",
            "coordinates": (942, 913),
            "values": [4, 2 , 1 ,5]
        },
        {
            "version":"全案版",
            "coordinates": (1500, 913),
            "values": [11 , 2 , 1 , 11]
        },
        {
            "version":"自定义",
            "coordinates": (2059, 913),
            "values": [2 , 2 , 1 ,3]
        }
    ]
    
    if detection_type == "智能检测":
        selected_version = random.choice(smart_detection_versions)
        return [selected_version["version"], selected_version["coordinates"], selected_version["values"].copy()]
    elif detection_type == "再次检测":
        selected_version = random.choice(redetection_versions)
        return [selected_version["version"], selected_version["coordinates"], selected_version["values"].copy()]
    else:
        # 如果传入的参数不是预期的，默认使用智能检测
        selected_version = random.choice(smart_detection_versions)
        return [selected_version["version"], selected_version["coordinates"], selected_version["values"].copy()]

def rerun_measurement(measurement_name="某点位"):
    """
    重新测量指定点位的完整流程
    
    Args:
        measurement_name (str): 测量点位的名称，用于日志输出
    """
    print(f"\n开始重新测量: {measurement_name}")
    
    # 定义重测步骤的坐标列表
    rerun_steps = [
        (2803, 959, "点击存图"),
        (2121, 1496, "点击其他位置"), 
        (2561, 1749, "点击结束检测")
    ]
    
    # 遍历执行每个步骤
    for x, y, step_name in rerun_steps:
        print(f"【智能检测】-【检测报告】-【重测某点位】 {step_name}")
        click_by_coordinates(x, y)
        # time.sleep(1)  # 每个步骤后等待1秒
    
    print(f"{measurement_name} 重新测量流程完成")
    return True

def compute_custom_points(del_count, add_count):
    """
    真实测量点位数量计算逻辑
    d > a → 真删双侧点位
    d ≤ a → 是否隐藏最后一个点位取决于奇偶
    """
    base = 21
    d = del_count
    a = add_count

    if d <= a:  # 删除次数不超过添加次数
        diff = a - d
        return 21 if diff % 2 == 0 else 20

    # 真正删除上方双侧点位
    removed_pairs = d - a
    final = base - removed_pairs * 2
    return max(final, 1)


def split_points_for_values(total_points: int):
    """
    按最新规则拆分 values:
    - 奇数：ceil & floor → 后者+1 → N+1
    - 偶数：N/2 & N/2 → 后者+1 → N+1
    """
    N = int(total_points)
    first = (N + 1) // 2
    second = (N // 2) + 1
    return first, second


# ==========================流程函数=================================
def routine_detection_process():
    """执行常规检测的完整操作流程"""
    print("【常规检测】步骤1: 点击常规检测")
    click_by_coordinates(1905, 1306)

    print("【常规检测】步骤2: 点击冻结")
    click_by_coordinates(2696, 1616)
    time.sleep(0.5)

    print("【常规检测】步骤3: 点击解冻")
    click_by_coordinates(2696, 1616)

    print("【常规检测】步骤4: 点击返回")
    click_by_coordinates(216, 108)

def custom_points_flow():
    """执行自定义点位的完整操作流程"""
    print("【自定义点位】步骤1: 点击自定义点位")
    click_by_coordinates(1905, 763)

    print("【自定义点位】步骤2: 点击正脸")
    click_by_coordinates(656, 1712)   

    print("【自定义点位】步骤3: 点击侧脸")
    click_by_coordinates(892, 1712)

    print("【自定义点位】步骤4: 点击颏下")
    click_by_coordinates(1128, 1712)

    print("【自定义点位】步骤5: 点击第一个点位")
    click_by_coordinates(2142, 431)

    print("【自定义点位】-【编辑】步骤1: 点击编辑")
    click_by_coordinates(2157, 1748)

    print("【自定义点位】-【编辑】步骤2: 点击还原")
    click_by_coordinates(1987, 1740)

    print("【自定义点位】-【编辑】步骤3: 点击删除")
    del_count = random.randint(1, 10)
    for _ in range(del_count):
        click_by_coordinates(2469, 431)

    print("【自定义点位】-【编辑】步骤4: 点击添加")
    add_count = random.randint(1, 10)
    for _ in range(add_count):
        click_by_coordinates(2469, 1519)

    print("【自定义点位】-【编辑】步骤5: 点击完成")
    click_by_coordinates(2329, 1748)

    print("【自定义点位】-【编辑】步骤6: 点击返回")
    click_by_coordinates(216, 108)

    # 计算最终点位数
    final_points = compute_custom_points(del_count, add_count)
    first, last = split_points_for_values(final_points)

    # 传回给主流程使用
    return [first, 2, 1, last]

def face_rerun_measurement(steps_list):
    """
    简化版的面部测量步骤执行方法
    
    Args:
        steps_list (list): 步骤列表，每个元素是(类型, 参数)元组
    """
    for i, (step_type, *params) in enumerate(steps_list, 1):
        step_names = {
            "click": "点击点位",
            "scroll": "滑动点位", 
            "double_tap": "重测点位",
            "rerun": "点击重新测量"
        }
        
        print(f"【智能检测】-【检测报告】-【测量列表】 {i}: {step_names.get(step_type, '执行操作')}")
        
        try:
            if step_type == "click":
                click_by_coordinates(params[0], params[1])
            elif step_type == "scroll":
                scroll_list_top_to_bottom_fast(params[0], params[1], params[2])
            elif step_type == "double_tap":
                uiautomator_double_tap(params[0], params[1])
            elif step_type == "rerun":
                rerun_measurement(params[0])
                
            time.sleep(1)
            
        except Exception as e:
            print(f" {i}执行失败: {e}")

def intelligent_detection_process(process_name,index,position_control):
    """
    执行完整的检测流程
    
    Args:
        process_name (str): 流程名称，用于替换打印信息中的文字
    """
    
    # 智能检测部分
    print(f"【{process_name}】 步骤{index+1}: 点击冻结")
    click_by_coordinates(2599, 959)
    time.sleep(1)

    print(f"【{process_name}】 步骤{index+2}: 点击解冻")
    click_by_coordinates(2599, 959)

    print(f"【{process_name}】 步骤{index+3}: 点击存图（循环{position_control[0]}次）")
    for i in range(position_control[0]):
        print(f"  第 {i+1}/{position_control[0]} 次点击存图")
        click_by_coordinates(2803, 959)
        time.sleep(0.5)

    print(f"【{process_name}】 步骤{index+4}: 点击上一点位（循环{position_control[1]}次）")
    for i in range(position_control[1]):
        print(f"  第 {i+1}/{position_control[1]} 次点击上一点位")
        click_by_coordinates(1010, 1749)
        time.sleep(0.5)

    print(f"【{process_name}】 步骤{index+5}: 点击下一点位（循环{position_control[2]}次）")
    for i in range(position_control[2]):
        print(f"  第 {i+1}/{position_control[2]} 次点击下一点位")
        click_by_coordinates(1510, 1749)
        time.sleep(0.5)

    print(f"【{process_name}】 步骤{index+6}: 点击解冻")
    click_by_coordinates(2599, 959)

    print(f"【{process_name}】 步骤{index+7}: 点击存图")
    click_by_coordinates(2803, 959)

    print(f"【{process_name}】 步骤{index+8}：点击上一点位")
    click_by_coordinates(1010, 1749)

    print(f"【{process_name}】 步骤{index+9}: 点击存图（循环{position_control[3]}次）")
    for i in range(position_control[3]):
        print(f"  第 {i+1}/{position_control[3]} 次点击存图")
        click_by_coordinates(2803, 959)
        time.sleep(0.5)

    print(f"【{process_name}】 步骤{index+10}: 点击查看报告")
    click_by_coordinates(2561, 1749)
    click_by_coordinates(2561, 1749)
    time.sleep(0.5)

    # 检测报告部分
    print(f"【{process_name}】-【检测报告】 步骤1: 测试 正脸R 列表")
    # 正脸R测量步骤配置
    front_r_face_steps = [
        ("click", 563, 755),           # 点击正脸R点位
        ("scroll", 527, 688, 1730),    # 滑动正脸R点位
        ("double_tap", 563, 896),     # 重测正脸R点位
        ("rerun", "正脸-(R)点位")   # 点击重新测量
    ]
    # 执行正脸R测量
    face_rerun_measurement(front_r_face_steps)

    print(f"【{process_name}】-【检测报告】 步骤2: 测试 正脸L 列表")
    # 正脸L测量步骤配置
    front_l_face_steps = [
        ("click", 2437, 758),          # 点击正脸L点位
        ("scroll", 2430, 715, 1688),   # 滑动正脸L点位
        ("double_tap", 2437, 905),    # 重测正脸L点位
        ("rerun", "正脸-(L)点位")   # 点击重新测量
    ]
    # 执行正脸L测量
    face_rerun_measurement(front_l_face_steps)

    print(f"【{process_name}】-【检测报告】 步骤3: 点击左脸")
    click_by_coordinates(1500, 440)
    time.sleep(1)

    print(f"【{process_name}】-【检测报告】 步骤4: 测试 左脸 列表")
    # 左脸测量步骤配置
    left_face_steps = [
        ("click", 1890, 891),         # 点击左脸点位
        ("scroll", 1883, 816, 1684),   # 滑动左脸点位
        ("double_tap", 1890, 1032),    # 重测左脸点位
        ("rerun", "左脸-点位")       # 点击重新测量
    ]
    # 执行左脸测量
    face_rerun_measurement(left_face_steps)

    print(f"【{process_name}】-【检测报告】 步骤5: 点击右脸")
    click_by_coordinates(1874, 440)
    time.sleep(1)

    print(f"【{process_name}】-【检测报告】 步骤6: 测试 右脸 列表")
    # 右脸测量步骤配置
    right_face_steps = [
        ("click", 1890, 891),         # 点击右脸点位
        ("scroll", 1883, 816, 1684),   # 滑动右脸点位
        ("double_tap", 1890, 1032),    # 重测右脸点位
        ("rerun", "右脸-点位")       # 点击重新测量
    ]
    # 执行右脸测量
    face_rerun_measurement(right_face_steps)

    print(f"【{process_name}】-【检测报告】 步骤7: 返回")
    click_by_coordinates(216, 108)

def create_medical_record(process_name="建立档案"):
    """
    执行建立档案的完整流程
    
    Args:
        process_name (str): 流程名称，用于替换打印信息中的文字
    """
    print(f"【智能检测】-【检测报告】-【{process_name}】 步骤1: 点击电话输入框")
    click_by_coordinates(1575, 797)

    print(f"【智能检测】-【检测报告】-【{process_name}】 步骤2: 输入电话")
    phone_number = generate_unique_phone()
    click_and_input(1575, 427, phone_number)

    print(f"【智能检测】-【检测报告】-【{process_name}】 步骤3: 点击年龄输入框")
    click_by_coordinates(1500, 591)

    print(f"【智能检测】-【检测报告】-【{process_name}】 步骤4: 选择年龄")
    random_age_selection(1504, 1102, 1800)

    print(f"【智能检测】-【检测报告】-【{process_name}】 步骤5: 选择年龄完成")
    click_by_coordinates(2141, 664)

    print(f"【智能检测】-【检测报告】-【{process_name}】 步骤6: 点击并输入姓名")
    name = generate_random_name()
    click_and_input(1575, 703, name)

    print(f"【智能检测】-【检测报告】-【{process_name}】 步骤7: 收起键盘")
    click_by_coordinates(2910, 1125)

    print(f"【智能检测】-【检测报告】-【{process_name}】 步骤8: 点击建立档案")
    click_by_coordinates(1713, 1269)
    
    return name

def search_user_record(user_id, user_name):
    print("【用户档案】-【档案列表】-【查询】步骤1: 输入ID")
    click_and_input(467, 395,user_id)

    print("【用户档案】-【档案列表】-【查询】步骤2: 输入姓名")
    click_and_input(1074, 395,user_name)

    print("【用户档案】-【档案列表】-【查询】步骤3: 点击检测日期")
    click_by_coordinates(1901, 395)

    print("【用户档案】-【档案列表】-【查询】步骤4: 选择检测日期")
    date_coordinate = random.choice([(1911, 395),(1911, 515),(1911, 635),(1911, 755),(1911, 875)])
    click_by_coordinates(*date_coordinate)

    print("【用户档案】-【档案列表】-【查询】步骤3: 点击查询")
    click_by_coordinates(2690, 396)

    print("【用户档案】-【档案列表】-【查询】步骤4: 点击重置")
    click_by_coordinates(2429, 396)

def modify_user_profile():
    print("【用户档案】-【个人档案】-【修改】步骤1: 点击用户记录")
    click_by_coordinates(1501, 776)

    print("【用户档案】-【个人档案】-【修改】步骤2: 点击修改")
    click_by_coordinates(2464, 396)

    print("【用户档案】-【个人档案】-【修改】步骤3: 修改姓名")
    new_user_name = generate_random_name()
    click_and_input(873, 396,new_user_name)

    print("【用户档案】-【个人档案】-【修改】步骤4: 修改年龄")
    click_and_input(1287, 396,random.randint(1, 100))

    print("【用户档案】-【个人档案】-【修改】步骤5: 修改电话号码")
    new_phone_number = generate_unique_phone()
    click_and_input(2069, 396,new_phone_number)

    print("【用户档案】-【个人档案】-【修改】步骤6: 点击确认")
    click_by_coordinates(2464, 396)


# ============ 软件流程自动化 ============
print("\n开始执行软件流程...")

# 等待应用完全启动
time.sleep(2)

# ============ 流程步骤 ============

def main_simple_flow(loop_count=3):
    """
    简单主函数 - 按顺序执行流程，支持循环次数
    
    """
    # 1.常规检测部分
    # routine_detection_process()
    print(f"开始执行简单流程，循环 {loop_count} 次")
    
    for i in range(1, loop_count + 1):
        print(f"\n 第 {i}/{loop_count} 次循环开始")
        print("-" * 30)
        
        try:
            # 循环开始前检查会话
            if not check_session_valid():
                print("会话无效，尝试恢复...")
                if not restart_appium_session():
                    print("× 无法恢复会话，跳过本次循环")
                    continue

            # 2.自定义点位界面
            new_values = custom_points_flow()


            # 3.智能检测
            print("【智能检测】 步骤1: 点击智能检测")
            click_by_coordinates(1096, 763)
            time.sleep(10)

            print("【智能检测】 步骤2: 选择版本")
            selected_smart_detection_version = get_version_random_coordinates("智能检测")

            # 只有当选中的版本是“自定义”才覆盖 values
            if "自定义" in selected_smart_detection_version[0]:
                # new_values 是 custom_points_flow() 返回的 [first,2,1,last]
                selected_smart_detection_version[2] = new_values
                print(f"已使用自定义 values: {selected_smart_detection_version[2]}")
            else:
                print(f"选择了版本: {selected_smart_detection_version[0]}，保持其原始 values: {selected_smart_detection_version[2]}")

            # 点击所选版本坐标
            click_by_coordinates(selected_smart_detection_version[1][0], selected_smart_detection_version[1][1])

            print("【智能检测】 步骤3: 选择性别")
            gender_coordinate = random.choice([(1157, 1281), (1844, 1281)])
            click_by_coordinates(*gender_coordinate)
            time.sleep(1)

            intelligent_detection_process("智能检测",3,selected_smart_detection_version[2])

            # 获取当前用户ID值
            user_id = get_id_value(driver)

            # 建立档案
            user_name = create_medical_record()

            # 4.执行再次检测流程
            print("【用户档案】 步骤1: 点击用户档案")
            click_by_coordinates(1096, 1306)

            # 查询用户记录
            search_user_record(user_id,user_name)

            # 修改用户记录
            modify_user_profile()

            # 再次检测
            print("【再次检测】 步骤1: 点击再次检测")
            click_by_coordinates(2754, 396)

            print("【再次检测】 步骤2: 选择版本")
            selected_redetection_version = get_version_random_coordinates("再次检测")

            # 只有当选中的版本是“自定义”才覆盖 values
            if "自定义" in selected_redetection_version[0]:
                # new_values 是 custom_points_flow() 返回的 [first,2,1,last]
                selected_redetection_version[2] = new_values
                print(f"已使用自定义 values: {selected_redetection_version[2]}")
            else:
                print(f"选择了版本: {selected_redetection_version[0]}，保持其原始 values: {selected_redetection_version[2]}")

            click_by_coordinates(selected_redetection_version[1][0], selected_redetection_version[1][1])
            time.sleep(1)

            intelligent_detection_process("再次检测",2,selected_redetection_version[2])

            # 1.常规检测部分
            routine_detection_process()

            print(f"第 {i}/{loop_count} 次循环完成")

        except Exception as e:
            print(f"× 第 {i} 次循环出现严重错误: {e}")
            # 尝试恢复会话并重新开始当前循环
            if restart_appium_session():
                print(" 会话恢复成功，重新开始当前循环...")
                i -= 1  # 重新执行当前循环
            else:
                print(" 会话恢复失败，跳过当前循环")

        # 循环间隔
        if i < loop_count:
            print("等待2秒后继续...")
            time.sleep(2)
    
    print(f"\n简单流程执行完毕，共完成 {loop_count} 次循环")



if __name__ == "__main__":
    # main_simple_flow(EXECUTE_COUNT)  # 执行循环
    click_and_input(1043,383,"ha")


# ============ 流程结束 ============
print("\n流程执行完成！")

# ============ 清理 ============
try:
    if check_session_valid():
        driver.quit()
        print("驱动已关闭")
    else:
        print("会话已失效")
except Exception as e:
    print(f"关闭驱动时出错: {e}")
