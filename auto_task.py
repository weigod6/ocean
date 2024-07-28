import subprocess
import sys
import time

import schedule


def run_script(script, max_retries=5, delay=5):
    retries = 0
    while retries < max_retries:
        try:
            result = subprocess.run([sys.executable, script], check=True)
            print(f"Successfully ran {script}: {result}")
            return True  # 成功运行后返回 True
        except subprocess.CalledProcessError as e:
            retries += 1
            print(f"Error occurred while running {script}: {e}")
            if retries < max_retries:
                print(f"Retrying {script} ({retries}/{max_retries}) in {delay} seconds...")
                time.sleep(delay)
            else:
                print(f"Failed to run {script} after {max_retries} attempts.")
                return False  # 达到最大重试次数后返回 False


def task():
    scripts = [
        "auto_download_nc.py",
        "auto_nctocsv.py",
        "auto_vis_sst.py",
        "auto_tiles.py"
    ]

    for script in scripts:
        success = run_script(script)
        if not success:
            print(f"Aborting the task due to failure in {script}.")
            break  # 如果脚本失败，停止运行后续脚本

# Schedule the task to run daily at midnight
schedule.every().day.at("18:21").do(task)

# Start the scheduler
print("Scheduler started. Waiting for the next scheduled download...")
while True:
    schedule.run_pending()

