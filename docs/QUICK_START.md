# 快速上手指南

## 前置条件

1. 安装 Python 3.8+
2. 安装 Appium Server（Node.js）
3. 连接 Android 设备或启动模拟器
4. 安装 ADB 并配置环境变量

## 环境搭建

### 1. 克隆项目（或创建项目）

```bash
cd UIAutoFrame
```

### 2. 创建虚拟环境（推荐）

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 验证设备连接

```bash
adb devices
```

确保看到你的设备 ID

## 配置项目

### 1. 配置设备

编辑 `config/device.yaml`：

```yaml
default:
  platformName: Android
  platformVersion: '15'           # 修改为你的设备版本
  deviceName: YOUR_DEVICE_ID      # 修改为你的设备ID
  automationName: UiAutomator2
  noReset: true
  newCommandTimeout: 600
```

### 2. 配置应用

编辑 `config/app.yaml`：

```yaml
peninsula:
  appPackage: com.ultrasound.peninsula      # 修改为你的应用包名
  appActivity: com.ultrasound.usdemo.MainActivity  # 修改为你的启动Activity
  appName: Peninsula超声应用
```

### 3. 配置坐标（可选）

如果需要修改坐标，编辑 `config/points.yaml`

### 4. 配置环境（可选）

编辑 `config/env.yaml`，修改 Appium 地址等

## 运行测试

### 1. 启动 Appium Server

```bash
appium
```

或使用 Appium Desktop

### 2. 运行测试用例

```bash
# 运行所有测试
pytest

# 运行单个测试文件
pytest testcases/test_custom_points.py

# 运行指定测试用例
pytest testcases/test_custom_points.py::TestCustomPoints::test_custom_points_full_flow

# 运行带标记的测试
pytest -m smoke
```

### 3. 快速调试（开发阶段）

```bash
python run.py
```

## 查看结果

### 1. 测试报告

打开 `artifacts/reports/report.html` 查看 HTML 测试报告

### 2. 日志文件

查看 `artifacts/logs/` 目录下的日志文件

### 3. 失败截图

查看 `artifacts/screenshots/` 目录下的截图

## 编写第一个测试用例

### 场景：测试进入自定义点位并返回

#### 1. 添加坐标（如果 points.yaml 中没有）

编辑 `config/points.yaml`：

```yaml
home:
  custom_points:
    x: 1905
    y: 763

common:
  back:
    x: 216
    y: 108
```

#### 2. 创建页面对象（如果不存在）

创建 `pages/home_page.py`：

```python
import logging

class HomePage:
    CUSTOM_POINTS = "home.custom_points"
    
    def __init__(self, executor):
        self.ex = executor
    
    def goto_custom_points(self):
        logging.info("[HomePage] 进入自定义点位")
        self.ex.click_point(self.CUSTOM_POINTS)
```

#### 3. 创建业务流程

创建 `workflows/simple_flow.py`：

```python
from pages.home_page import HomePage
from pages.common_page import CommonPage

class SimpleFlow:
    def __init__(self, executor):
        self.home_page = HomePage(executor)
        self.common_page = CommonPage(executor)
    
    def goto_custom_points_and_back(self):
        self.home_page.goto_custom_points()
        self.common_page.go_back()
```

#### 4. 创建测试用例

创建 `testcases/test_simple.py`：

```python
import pytest
import logging
from core.driver.driver_manager import DriverManager
from core.executor.action_executor import ActionExecutor
from core.utils.points_loader import load_points
from core.utils.config_loader import ConfigLoader
from core.logger.logger import setup_logger
from workflows.simple_flow import SimpleFlow

@pytest.fixture(scope="session")
def driver():
    setup_logger()
    config_loader = ConfigLoader()
    caps = config_loader.get_merged_caps()
    env_config = config_loader.get_env_config()
    
    dm = DriverManager(env_config['appium']['server_url'], caps)
    driver = dm.start()
    yield driver
    dm.quit()

@pytest.fixture(scope="function")
def executor(driver):
    points = load_points()
    return ActionExecutor(driver, points)

def test_simple_flow(executor):
    """测试简单流程"""
    flow = SimpleFlow(executor)
    flow.goto_custom_points_and_back()
    logging.info("测试通过")
```

#### 5. 运行测试

```bash
pytest testcases/test_simple.py -v
```

## 常见问题

### Q1: 提示找不到设备

**A**: 检查设备是否连接，运行 `adb devices` 确认

### Q2: 提示找不到元素

**A**: 检查 `config/points.yaml` 中坐标是否正确，可使用 Appium Inspector 获取坐标

### Q3: Appium 连接失败

**A**: 确保 Appium Server 已启动，检查 `config/env.yaml` 中的 server_url

### Q4: 测试运行很慢

**A**: 检查网络连接，调整 `config/env.yaml` 中的超时时间

### Q5: 如何获取元素坐标？

**A**: 使用 Appium Inspector：
1. 启动 Appium Server
2. 打开 Appium Inspector
3. 连接设备
4. 点击元素查看坐标

## 最佳实践

### 1. 开发流程

```
1. 在 config/points.yaml 添加坐标
2. 在 pages/ 创建页面对象
3. 在 workflows/ 创建业务流程
4. 在 testcases/ 编写测试用例
5. 运行 pytest 验证
```

### 2. 调试技巧

```bash
# 使用 run.py 快速调试单个流程
python run.py

# 使用 pytest 的 -s 参数查看 print 输出
pytest testcases/test_simple.py -s

# 查看详细日志
cat artifacts/logs/ui_auto_*.log
```

### 3. 代码规范

- 所有坐标必须配置在 `points.yaml`
- 页面操作必须封装在 `pages/`
- 业务流程必须封装在 `workflows/`
- 测试用例只调用 `workflows/`，不直接调用 `pages/`

### 4. 目录组织

```
我的测试项目/
  config/     - 配置我的设备和应用
  pages/      - 为我的应用创建页面对象
  workflows/  - 组织我的业务流程
  testcases/  - 编写我的测试用例
```

## 进阶使用

### 1. 使用参数化测试

```python
@pytest.mark.parametrize("count", [1, 3, 5])
def test_add_points(executor, count):
    page = CustomPointsPage(executor)
    page.add_points(count)
```

### 2. 使用标记

```python
@pytest.mark.smoke
def test_smoke_case(executor):
    # 冒烟测试
    pass

# 运行冒烟测试
pytest -m smoke
```

### 3. 生成自定义报告

```bash
pytest --html=my_report.html --self-contained-html
```

### 4. 并行执行（需要安装 pytest-xdist）

```bash
pip install pytest-xdist
pytest -n 2  # 2个进程并行
```

## 下一步

1. 阅读 [项目架构说明](../README.md)
2. 查看 [重构总结](REFACTOR_SUMMARY.md)
3. 学习 [AI 使用规则](../.cursorrules)
4. 开始编写你的测试用例！

## 获取帮助

- 查看日志文件：`artifacts/logs/`
- 查看截图：`artifacts/screenshots/`
- 查看测试报告：`artifacts/reports/report.html`
- 参考现有测试用例：`testcases/test_custom_points.py`

---

祝你使用愉快！
