"""
Pytest 全局配置文件
"""
import pytest
import logging
from datetime import datetime
import os


def pytest_configure(config):
    """pytest 初始化配置"""
    # 创建 artifacts 目录
    os.makedirs("artifacts/reports", exist_ok=True)
    os.makedirs("artifacts/logs", exist_ok=True)
    os.makedirs("artifacts/screenshots", exist_ok=True)


def pytest_html_report_title(report):
    """自定义 HTML 报告标题"""
    report.title = "UI 自动化测试报告"
