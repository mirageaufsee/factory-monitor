import requests
import random
import time
import os

API_URL = os.getenv("API_URL", "http://backend:8000")

DEVICES = [
    {"name": "机床 A1", "location": "车间一", "device_type": "CNC Machine"},
    {"name": "机床 B2", "location": "车间二", "device_type": "CNC Machine"},
    {"name": "压缩机 C1", "location": "车间一", "device_type": "Compressor"},
]

def wait_for_backend():
    print("等待后端启动...")
    while True:
        try:
            r = requests.get(f"{API_URL}/")
            if r.status_code == 200:
                print("后端已就绪！")
                return
        except Exception:
            pass
        time.sleep(3)

def register_devices():
    print("注册设备...")
    device_ids = []
    for device in DEVICES:
        try:
            r = requests.post(f"{API_URL}/devices/", json=device)
            if r.status_code == 200:
                device_id = r.json()["id"]
                device_ids.append(device_id)
                print(f"  已注册：{device['name']} (id={device_id})")
        except Exception as e:
            print(f"  注册失败：{e}")
    return device_ids

def generate_reading(device_id):
    # 90% 正常范围，10% 触发报警
    is_anomaly = random.random() < 0.1

    if is_anomaly:
        temperature = random.uniform(80, 95)
        pressure = random.uniform(9, 11)
        rpm = random.uniform(3200, 3800)
    else:
        temperature = random.uniform(55, 74)
        pressure = random.uniform(5, 7.9)
        rpm = random.uniform(1500, 2900)

    return {
        "device_id": device_id,
        "temperature": round(temperature, 2),
        "pressure": round(pressure, 2),
        "rpm": round(rpm, 2),
    }

def run():
    wait_for_backend()
    device_ids = register_devices()

    if not device_ids:
        print("没有设备可以模拟，退出。")
        return

    print(f"\n开始发送数据，每5秒一次...\n")
    while True:
        for device_id in device_ids:
            data = generate_reading(device_id)
            try:
                r = requests.post(f"{API_URL}/sensor-data/", json=data)
                status = "⚠️ 异常" if (
                    data["temperature"] > 75 or
                    data["pressure"] > 8 or
                    data["rpm"] > 3000
                ) else "✅ 正常"
                print(f"Device {device_id} | 温度 {data['temperature']}°C | "
                      f"压力 {data['pressure']} bar | "
                      f"转速 {data['rpm']} rpm | {status}")
            except Exception as e:
                print(f"发送失败：{e}")
        time.sleep(5)

if __name__ == "__main__":
    run()