import time
import logging
from functools import wraps


def retry(max_attempts=3, interval=1, exceptions=(Exception,)):
    """
    重试装饰器
    
    Args:
        max_attempts: 最大尝试次数
        interval: 重试间隔（秒）
        exceptions: 需要重试的异常类型
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_attempts:
                        logging.error(f"[RETRY] {func.__name__} 重试 {max_attempts} 次后失败: {e}")
                        raise
                    logging.warning(f"[RETRY] {func.__name__} 第 {attempt} 次失败，{interval}秒后重试...")
                    time.sleep(interval)
        return wrapper
    return decorator
