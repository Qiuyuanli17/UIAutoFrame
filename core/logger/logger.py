import logging
import os
from datetime import datetime

def setup_logger():
    log_dir = os.path.join("artifacts", "logs")
    os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(
        log_dir,
        f"ui_auto_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    )

    
    root_logger = logging.getLogger()
    if not root_logger.hasHandlers():  # 避免重复添加 handler
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s | %(levelname)s | %(message)s",
            handlers=[
                logging.FileHandler(log_file, encoding="utf-8"),
                # logging.StreamHandler()
                ]
        )