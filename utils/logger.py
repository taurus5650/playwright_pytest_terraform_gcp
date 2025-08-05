import logging
import os
import re
import sys
import uuid
from datetime import datetime, timedelta

# ===== 1. Setup Logger  =====
logger = logging.getLogger(name='')  # root logger
logger.setLevel(logging.DEBUG)

for h in logger.handlers[:]:
    logger.removeHandler(h)

correlation_id = uuid.uuid4()
formatter = logging.Formatter(f'%(asctime)s | %(name)s | %(levelname)s | {correlation_id} | %(message)s')

# ===== 2. Console handler =====
console_handler = logging.StreamHandler(sys.stderr)
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# ===== 3. File handler (log/yyyy-mm-dd_HHMMSS.log) =====
log_dir = "./log"
os.makedirs(log_dir, exist_ok=True)

timestamp = datetime.now().strftime('%Y-%m-%d_%H%M%S')
log_file_path = os.path.join(log_dir, f"{timestamp}.log")
logger.info(f'log_file_path={log_file_path}')

file_handler = logging.FileHandler(log_file_path, encoding="utf-8")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# ===== 4. Clean log =====
def cleanup_old_logs(directory: str, keep_days: int = 3):
    now = datetime.now()
    pattern = re.compile(r"(\d{4}-\d{2}-\d{2})_\d{6}\.log")

    for filename in os.listdir(directory):
        match = pattern.match(filename)
        if match:
            date_str = match.group(1)
            try:
                file_date = datetime.strptime(date_str, "%Y-%m-%d")
                if now - file_date > timedelta(days=keep_days):
                    os.remove(os.path.join(directory, filename))
                    logger.info(f'Delete log={filename}')
            except Exception as e:
                logger.warning(f"Log failed: {filename}: {e}")


cleanup_old_logs(directory=log_dir)
