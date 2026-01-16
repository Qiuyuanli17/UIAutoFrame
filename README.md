# UIAutoFrame - Android UI 自动化测试框架

基于 Appium + Pytest + Page Object 模式的 Android UI 自动化测试框架

## 项目特点

- 分层架构清晰，职责边界明确
- 配置与代码分离，支持多设备多应用
- 支持失败重试、失败截图、测试报告
- 高复用性，易扩展

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置设备和应用

修改 `config/device.yaml` 和 `config/app.yaml`

### 3. 启动 Appium 服务

```bash
appium
```

### 4. 运行测试

```bash
# 运行所有测试
pytest

# 运行单个测试文件
pytest testcases/test_custom_points.py

# 快速调试（开发阶段）
python run.py
```

### 5. 查看报告

测试报告：`artifacts/reports/report.html`  
日志文件：`artifacts/logs/`  
截图文件：`artifacts/screenshots/`

## 目录结构

```
UIAutoFrame/
├── config/                      # 配置层
│   ├── device.yaml              # 设备配置
│   ├── app.yaml                 # 应用配置
│   ├── env.yaml                 # 环境配置
│   └── points.yaml              # 坐标点位配置
│
├── core/                        # 核心能力层（框架级）
│   ├── driver/                  # 驱动管理
│   ├── executor/                # 动作执行器
│   ├── logger/                  # 日志管理
│   ├── assertion/               # 断言封装
│   └── utils/                   # 工具类
│
├── pages/                       # 页面对象层（业务级）
│   ├── common_page.py           # 通用页面
│   ├── home_page.py             # 主页
│   ├── custom_points_page.py    # 自定义点位页面
│   └── ...
│
├── workflows/                   # 业务流程层（业务级）
│   ├── custom_points_flow.py   # 自定义点位流程
│   └── components/              # 可复用流程组件
│
├── testcases/                   # 测试用例层（业务级）
│   ├── test_custom_points.py   # 自定义点位测试
│   └── ...
│
├── artifacts/                   # 输出产物
│   ├── logs/                    # 日志
│   ├── screenshots/             # 截图
│   └── reports/                 # 测试报告
│
├── .cursorrules                 # AI 使用规则文件
├── pytest.ini                   # pytest 配置
├── conftest.py                  # pytest 全局配置
├── requirements.txt             # 依赖管理
├── run.py                       # 快速调试入口
└── README.md                    # 项目说明
```

## 架构设计

### 分层职责

| 层级 | 职责 | 示例 |
|------|------|------|
| testcases | 编写测试用例，执行断言 | `test_custom_points.py` |
| workflows | 组装页面操作，完成业务流程 | `CustomPointsFlow` |
| pages | 封装页面元素和页面级操作 | `CustomPointsPage` |
| core | 提供框架级通用能力 | `ActionExecutor`, `DriverManager` |
| config | 存储配置，实现配置代码分离 | `device.yaml`, `points.yaml` |

### 数据流向

```
testcases → workflows → pages → core/executor → core/driver
```

严格禁止跨层级调用！

## 新增功能示例

### 示例1：新增一个页面

1. 在 `config/points.yaml` 添加坐标：
```yaml
new_page:
  button1:
    x: 100
    y: 200
```

2. 在 `pages/` 创建 `new_page.py`：
```python
class NewPage:
    BUTTON1 = "new_page.button1"
    
    def __init__(self, executor):
        self.ex = executor
    
    def click_button1(self):
        self.ex.click_point(self.BUTTON1)
```

3. 在 `workflows/` 创建业务流程：
```python
class NewPageFlow:
    def __init__(self, executor):
        self.page = NewPage(executor)
    
    def run_flow(self):
        self.page.click_button1()
```

4. 在 `testcases/` 编写测试用例：
```python
def test_new_page_flow(executor):
    flow = NewPageFlow(executor)
    flow.run_flow()
```

### 示例2：接入新设备

修改 `config/device.yaml`：
```yaml
new_device:
  platformName: Android
  platformVersion: '14'
  deviceName: NEW_DEVICE_ID
  automationName: UiAutomator2
```

测试时指定设备：
```python
caps = config_loader.get_merged_caps(device_key="new_device")
```

## 最佳实践

1. **配置与代码分离**：所有硬编码必须迁移到 yaml
2. **职责单一**：每个类、每个方法只做一件事
3. **日志完善**：关键操作必须记录日志
4. **失败处理**：使用重试机制，失败时自动截图
5. **代码复用**：相同操作必须封装，禁止复制粘贴

## 维护建议

- 新增页面时同步更新 `points.yaml`
- 定期检查和清理 `artifacts/` 目录
- 测试用例失败时优先查看日志和截图
- 保持 `.cursorrules` 文件更新

## 常见问题

### Q: 如何切换设备？
A: 修改 `config/device.yaml` 或在代码中指定 `device_key`

### Q: 如何添加新的坐标？
A: 在 `config/points.yaml` 中添加，格式参考现有配置

### Q: 测试失败如何调试？
A: 查看 `artifacts/logs/` 日志和 `artifacts/screenshots/` 截图

### Q: 如何生成测试报告？
A: 运行 `pytest` 后查看 `artifacts/reports/report.html`

## 项目状态

- ✅ 配置层完善
- ✅ 核心层增强（断言、截图、重试）
- ✅ Pages 层重构
- ✅ Workflows 层完善
- ✅ 测试用例层建立
- ✅ 自定义点位功能迁移完成
- 🚧 其他功能（智能检测、常规检测等）待迁移

## 许可证

MIT

## 联系方式

如有问题请提 Issue
