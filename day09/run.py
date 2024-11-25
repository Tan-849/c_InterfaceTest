import os
import shutil
import time

import pytest

if __name__ == '__main__':
    pytest.main()
    os.system("allure generate ./reports/temps -o ./reports/allure --clean")
    # os.system("allure open ./reports/allure ")
    # 复制日志
    shutil.move(f"./logs/frame.log", f"./logs/frame_{str(int(time.time()))}.log")