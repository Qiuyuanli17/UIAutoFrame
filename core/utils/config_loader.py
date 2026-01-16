import yaml
import os


class ConfigLoader:
    """配置加载器"""

    def __init__(self):
        self.base_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..")
        )

    def load_yaml(self, file_name):
        """加载 yaml 文件"""
        path = os.path.join(self.base_dir, "config", file_name)
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def get_device_caps(self, device_key="default"):
        """获取设备配置"""
        device_config = self.load_yaml("device.yaml")
        return device_config.get(device_key, device_config["default"])

    def get_app_config(self, app_key="peninsula"):
        """获取应用配置"""
        app_config = self.load_yaml("app.yaml")
        return app_config.get(app_key)

    def get_env_config(self):
        """获取环境配置"""
        return self.load_yaml("env.yaml")

    def get_merged_caps(self, device_key="default", app_key="peninsula"):
        """合并设备和应用配置，返回完整的 capabilities"""
        device_caps = self.get_device_caps(device_key)
        app_config = self.get_app_config(app_key)
        
        # 合并配置
        merged = {**device_caps, **app_config}
        return merged
