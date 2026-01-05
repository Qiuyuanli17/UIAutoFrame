import yaml
import os

def load_points():
    """
    加载 config/points.yaml
    """
    base_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..")
    )
    path = os.path.join(base_dir, "config", "points.yaml")

    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)