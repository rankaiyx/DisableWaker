# -*- coding: utf-8 -*-
import subprocess
from datetime import datetime
import os

# 配置日志文件的绝对路径（请根据需要修改）
LOG_FILE = r"C:\disable_usb_wake.log"

def run_command(command):
    """执行系统命令并返回输出"""
    result = subprocess.run(command, capture_output=True, text=True, encoding='gbk')
    return result.stdout.strip().splitlines()

def disable_wake_devices():
    # 获取可唤醒设备列表
    devices = run_command(["powercfg", "/devicequery", "wake_armed"])
    
    # 过滤无效输出（处理不同系统版本的输出差异）
    filtered_devices = []
    for device in devices:
        stripped = device.strip()
        if stripped and stripped != "无":
            filtered_devices.append(stripped)
    
    # 处理无设备情况
    if not filtered_devices:
        print("未检测到可唤醒设备")
        return

    # 创建日志文件所在目录（如果不存在）
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    
    # 禁用每个设备的唤醒功能
    with open(LOG_FILE, "a", encoding="utf-8") as log:
        for device in filtered_devices:
            # 执行禁用命令（静默执行）
            subprocess.run(["powercfg", "/devicedisablewake", device], 
                          stdout=subprocess.DEVNULL, 
                          stderr=subprocess.DEVNULL)
            
            # 记录日志
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"设备名: {device} | 禁用时间: {timestamp}\n"
            log.write(log_entry)
            print(f"已禁用: {device}")

    print(f"\n操作完成，日志已保存至：{LOG_FILE}")

if __name__ == "__main__":
    disable_wake_devices()
