# 架构设计文档

## 设计理念

UIAutoFrame 基于以下核心理念设计：

1. **职责单一**：每一层只负责一件事
2. **分层清晰**：严格的层级边界，禁止跨层调用
3. **配置分离**：配置与代码完全分离
4. **高复用性**：核心层可跨项目复用
5. **易扩展性**：新增功能遵循现有模式即可

## 整体架构

```
┌─────────────────────────────────────────────────────────┐
│                     testcases/                          │
│               (测试用例层 - 断言执行)                    │
└──────────────────────┬──────────────────────────────────┘
                       │ 调用
┌──────────────────────▼──────────────────────────────────┐
│                    workflows/                           │
│              (业务流程层 - 流程编排)                     │
└──────────────────────┬──────────────────────────────────┘
                       │ 调用
┌──────────────────────▼──────────────────────────────────┐
│                     pages/                              │
│             (页面对象层 - 页面操作)                      │
└──────────────────────┬──────────────────────────────────┘
                       │ 调用
┌──────────────────────▼──────────────────────────────────┐
│                core/executor/                           │
│            (执行器层 - 原子操作)                         │
└──────────────────────┬──────────────────────────────────┘
                       │ 调用
┌──────────────────────▼──────────────────────────────────┐
│                core/driver/                             │
│             (驱动层 - Appium驱动)                        │
└─────────────────────────────────────────────────────────┘

                横向支撑层
┌─────────────────────────────────────────────────────────┐
│  config/  │  core/logger/  │  core/utils/  │  core/assertion/  │
│  (配置)   │    (日志)      │   (工具)      │     (断言)        │
└─────────────────────────────────────────────────────────┘
```

## 各层详细设计

### 1. 配置层 (config/)

**设计目标**：实现配置与代码的完全分离

#### 文件职责

| 文件 | 职责 | 示例 |
|------|------|------|
| device.yaml | 设备配置 | 平台、版本、设备ID |
| app.yaml | 应用配置 | 包名、Activity |
| env.yaml | 环境配置 | Appium地址、超时时间 |
| points.yaml | 坐标配置 | UI元素坐标 |

#### 设计原则

1. **单一数据源**：每个配置项只在一处定义
2. **环境隔离**：支持多环境配置（dev/test/prod）
3. **易于维护**：修改配置不需要改代码

#### 扩展性

```yaml
# 支持多设备配置
device1:
  deviceName: DEVICE_001

device2:
  deviceName: DEVICE_002

# 支持多应用配置
app1:
  appPackage: com.example.app1

app2:
  appPackage: com.example.app2
```

---

### 2. 核心层 (core/)

**设计目标**：提供框架级通用能力，与业务无关

#### 2.1 驱动管理 (core/driver/)

**职责**：管理 Appium 驱动的生命周期

```python
class DriverManager:
    """
    驱动管理器
    - 启动/关闭会话
    - 会话健康检查
    - 会话重启恢复
    """
    def start()           # 启动会话
    def quit()            # 关闭会话
    def check_session_valid()  # 检查会话
    def restart_session()      # 重启会话
```

**设计要点**：
- 支持会话重启恢复
- 支持应用自动激活
- 完善的异常处理

#### 2.2 动作执行器 (core/executor/)

**职责**：封装所有底层 UI 操作

```python
class ActionExecutor:
    """
    动作执行器
    - 点击、输入、滑动等原子操作
    - 基于坐标或点位名称操作
    - 自动重试和日志记录
    """
    def click(x, y)           # 点击坐标
    def input(x, y, text)     # 输入文本
    def double_click(x, y)    # 双击
    def swipe(...)            # 滑动
    def click_point(name)     # 点击点位（读取yaml）
```

**设计要点**：
- 所有操作自动添加日志
- 使用 @retry 装饰器自动重试
- 统一的操作间隔时间
- 禁止包含业务逻辑

#### 2.3 日志管理 (core/logger/)

**职责**：统一的日志输出和管理

```python
def setup_logger():
    """
    初始化日志配置
    - 按时间戳生成日志文件
    - 支持文件和控制台双输出
    - 统一的日志格式
    """
```

**日志格式**：
```
2026-01-14 10:30:45 | INFO | [HomePage] 进入自定义点位
2026-01-14 10:30:46 | INFO | [ActionExecutor] 点击坐标: (1905, 763)
```

#### 2.4 断言封装 (core/assertion/)

**职责**：封装常用断言，失败时自动截图

```python
class BaseAssert:
    """
    基础断言类
    - 元素存在性断言
    - 文本匹配断言
    - 元素可见性断言
    - 失败自动截图
    """
    def assert_element_exists()
    def assert_text_in_element()
    def assert_element_visible()
```

**设计要点**：
- 断言失败自动截图
- 详细的错误信息
- 支持自定义断言消息

#### 2.5 工具类 (core/utils/)

**职责**：提供通用工具函数

| 工具类 | 职责 |
|--------|------|
| config_loader.py | 加载 yaml 配置 |
| points_loader.py | 加载坐标配置 |
| screenshot.py | 截图功能 |
| retry.py | 重试装饰器 |
| generator.py | 数据生成器 |

---

### 3. 页面层 (pages/)

**设计目标**：封装页面元素和页面级操作

#### 设计模式

采用 **Page Object 模式**

```python
class CustomPointsPage:
    """
    页面类模板
    1. 元素定位（使用 points.yaml）
    2. 页面级原子操作
    3. 不包含业务流程
    """
    
    # 1. 元素定位符（静态常量）
    ADD = "custom_points.add"
    DELETE = "custom_points.delete"
    
    # 2. 初始化（注入 executor）
    def __init__(self, executor):
        self.ex = executor
    
    # 3. 页面级原子操作（单一职责）
    def click_add(self):
        """点击添加按钮"""
        self.ex.click_point(self.ADD)
    
    # 4. 批量操作（仍属页面级）
    def add_points(self, count):
        """批量添加点位"""
        for _ in range(count):
            self.click_add()
```

#### 职责边界

**✅ 允许**：
- 定义元素定位符
- 封装单个页面的操作
- 批量操作（同一页面内）

**❌ 禁止**：
- 跨页面操作（如点击返回后再进入）
- 业务断言（如验证添加成功）
- 复杂业务逻辑

#### 命名规范

- 类名：`XxxPage`
- 方法名：`click_xxx()`, `input_xxx()`, `get_xxx()`
- 常量名：大写 `ADD`, `DELETE`

---

### 4. 工作流层 (workflows/)

**设计目标**：组装页面操作，完成业务流程

#### 设计模式

采用 **Facade 模式** + **Strategy 模式**

```python
class CustomPointsFlow:
    """
    业务流程类模板
    1. 初始化依赖的页面对象
    2. 组装页面操作完成业务流程
    3. 处理流程中的数据传递
    """
    
    # 1. 初始化依赖
    def __init__(self, executor):
        self.home_page = HomePage(executor)
        self.custom_page = CustomPointsPage(executor)
        self.common_page = CommonPage(executor)
    
    # 2. 完整流程（主要方法）
    def run_full_flow(self):
        """执行完整流程"""
        # 步骤1：进入页面
        self.home_page.goto_custom_points()
        
        # 步骤2：执行操作
        self.custom_page.click_add()
        
        # 步骤3：返回
        self.common_page.go_back()
        
        # 步骤4：返回结果
        return result
    
    # 3. 简化流程（可选）
    def run_simple_flow(self):
        """简化版流程"""
        pass
```

#### 职责边界

**✅ 允许**：
- 组合多个页面操作
- 处理流程间的数据传递
- 业务逻辑判断（如随机选择）

**❌ 禁止**：
- 直接调用 executor（必须通过 pages）
- 业务断言（应在 testcases 层）
- 访问 driver（应通过 executor）

#### 组件化设计

`workflows/components/` 存放可复用的流程组件

```python
# 冻结并保存组件
class FreezeAndSaveStep:
    def execute(self):
        self.page.freeze()
        self.page.save()

# 在流程中使用
class DetectionFlow:
    def run(self):
        freeze_step = FreezeAndSaveStep()
        freeze_step.execute()
```

---

### 5. 测试用例层 (testcases/)

**设计目标**：编写测试用例，执行断言

#### 设计模式

采用 **pytest 框架** + **fixture 模式**

```python
# 全局 fixture（conftest.py）
@pytest.fixture(scope="session")
def driver():
    """会话级别的 driver"""
    # 启动
    dm = DriverManager(url, caps)
    driver = dm.start()
    yield driver
    # 清理
    dm.quit()

@pytest.fixture(scope="function")
def executor(driver):
    """用例级别的 executor"""
    return ActionExecutor(driver, points)

# 测试用例
class TestCustomPoints:
    def test_full_flow(self, executor):
        """测试完整流程"""
        # 1. 执行流程
        flow = CustomPointsFlow(executor)
        result = flow.run_full_flow()
        
        # 2. 断言
        assert isinstance(result, list)
        assert len(result) == 4
```

#### 职责边界

**✅ 允许**：
- 调用 workflows 执行流程
- 执行断言验证结果
- 使用 pytest 的各种特性

**❌ 禁止**：
- 直接调用 pages（必须通过 workflows）
- 直接调用 executor（必须通过 workflows）
- 包含业务逻辑（应在 workflows）

#### pytest 特性使用

```python
# 1. 参数化测试
@pytest.mark.parametrize("count", [1, 3, 5])
def test_add_points(executor, count):
    flow.add_points(count)

# 2. 标记测试
@pytest.mark.smoke
def test_smoke():
    pass

# 3. 跳过测试
@pytest.mark.skip(reason="待实现")
def test_feature():
    pass

# 4. 失败重跑
@pytest.mark.flaky(reruns=2)
def test_unstable():
    pass
```

---

## 数据流设计

### 正向流程

```
1. testcase 调用 workflow
   ↓
2. workflow 调用 pages
   ↓
3. pages 调用 executor
   ↓
4. executor 调用 driver
   ↓
5. driver 执行实际操作
```

### 返回流程

```
1. driver 返回执行结果
   ↑
2. executor 记录日志并返回
   ↑
3. pages 返回操作结果
   ↑
4. workflow 处理数据并返回
   ↑
5. testcase 接收结果并断言
```

---

## 依赖注入设计

采用**构造器注入**模式

```python
# 层级1：创建 driver
driver = DriverManager().start()

# 层级2：注入 driver 创建 executor
executor = ActionExecutor(driver, points)

# 层级3：注入 executor 创建 page
page = CustomPointsPage(executor)

# 层级4：注入 executor 创建 workflow
workflow = CustomPointsFlow(executor)
```

**优势**：
- 依赖关系清晰
- 易于测试（可注入 mock 对象）
- 支持灵活替换

---

## 异常处理设计

### 1. 分层异常处理

```
testcases:   记录失败、截图、报告
    ↓
workflows:   捕获并转换异常
    ↓
pages:       捕获并记录日志
    ↓
executor:    重试机制
    ↓
driver:      原始异常
```

### 2. 重试机制

```python
@retry(max_attempts=3, interval=1)
def click(self, x, y):
    # 失败自动重试3次
    pass
```

### 3. 失败截图

```python
try:
    flow.run()
except Exception as e:
    screenshot_helper.take_screenshot("failed")
    raise
```

---

## 扩展性设计

### 1. 新增页面

只需遵循现有模式创建新的 Page 类

### 2. 新增流程

组合现有 Pages 创建新的 Flow 类

### 3. 接入新项目

修改配置文件，新增业务层代码（pages/workflows/testcases）

### 4. 替换底层技术

只需修改 core 层，业务层无需改动

---

## 性能优化设计

### 1. 会话复用

- 使用 session 级别的 fixture
- 避免频繁启动关闭 driver

### 2. 并行执行

- 支持 pytest-xdist 并行测试
- 使用独立的 driver 实例

### 3. 智能等待

- 使用 implicit_wait 和 explicit_wait
- 避免硬编码的 sleep

---

## 安全性设计

### 1. 敏感信息管理

```yaml
# 敏感信息应使用环境变量
env:
  DEVICE_PASSWORD: ${DEVICE_PASSWORD}
```

### 2. 日志脱敏

敏感信息（密码、手机号等）不记录到日志

---

## 总结

### 设计优势

1. **职责清晰**：每层各司其职
2. **易于维护**：修改影响范围可控
3. **高复用性**：核心层可跨项目复用
4. **易于测试**：支持单元测试和集成测试
5. **团队协作**：多人可并行开发

### 适用场景

- 中小型自动化测试项目
- 需要长期维护的项目
- 需要支持多设备多应用的项目
- 需要团队协作的项目

### 后续优化方向

1. 增加单元测试覆盖
2. 支持分布式执行
3. 集成 CI/CD
4. 完善测试数据管理

---

**版本**: v1.0  
**最后更新**: 2026-01-14
