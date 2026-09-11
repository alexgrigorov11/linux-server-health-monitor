import subprocess
import re
import json
import os
import argparse
from datetime import datetime



def parse_args():
    parser = argparse.ArgumentParser(description="Linux server health monitoring tool")
    parser.add_argument("--no-save", action="store_true", help="Do not save report file")
    parser.add_argument("--no-log", action="store_true", help="Do not update CSV log")
    parser.add_argument("-o", "--output-dir", default="reports", help="Directory for generated report files")    
    return parser.parse_args()


def run_command(command):
   result = subprocess.run(command, capture_output=True, text=True)
   return result.stdout

def get_uptime():
   uptime_output = run_command(["uptime"])
   return uptime_output.strip()

def get_load_average(uptime_text):
   load_1 = 0.0
   load_5 = 0.0
   load_15 = 0.0

   load_match = re.search(r"load average: ([0-9.]+), ([0-9.]+), ([0-9.]+)", uptime_text)

   if load_match:
      load_1 = float(load_match.group(1))
      load_5 = float(load_match.group(2))
      load_15 = float(load_match.group(3))

   return load_1, load_5, load_15

def get_cpu_usage():
   cpu_output = run_command(["top", "-bn1"])
   cpu_idle = 0

   for line in cpu_output.splitlines():
      if "Cpu(s)" in line:
         parts = line.replace(",", "").split()
         for i in range(len(parts)):
            if parts[i] == "id":
               cpu_idle = float(parts[i - 1])

   return int(100 - cpu_idle)

def get_disk_usage():
   disk_output = run_command(["df", "-h"])
   disk_usage_percent = 0

   for line in disk_output.splitlines():
      parts = line.split()
      if len(parts) >= 6 and parts[-1] == "/":
         disk_usage_percent = int(parts[4].replace("%", ""))


   return disk_usage_percent

def get_memory_usage():
   memory_output = run_command(["free", "-h"])
   mem_lines = memory_output.splitlines()
   mem_parts = mem_lines[1].split()

   mem_total = float(mem_parts[1].replace("Gi", ""))
   mem_used = float(mem_parts[2].replace("Gi", ""))
   memory_usage_percent = int((mem_used / mem_total) * 100)

   return memory_usage_percent

def get_swap_usage():
   memory_output = run_command(["free", "-h"])
   mem_lines = memory_output.splitlines()
   swap_parts = mem_lines[2].split()

   swap_used = swap_parts[2] != "0B"

   return swap_used

def save_report(timestamp, uptime, cpu_usage_percent, load_1, load_5, load_15, disk_usage_percent, memory_usage_percent, swap_used, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    report_filename = "server_health_report_" + timestamp + ".txt"
    report_path = os.path.join(output_dir, report_filename)

    with open(report_path, "w") as file:
      file.write("==== SERVER HEALTH REPORT ====\n")
      file.write("Uptime: " + uptime + "\n")
      file.write("Load Average (1/5/15min): " + str(load_1) + " / " + str(load_5) + " / " + str(load_15) + "\n")
      file.write("CPU Usage: " + str(cpu_usage_percent) + "%\n")
      file.write("Disk Usage (/): " + str(disk_usage_percent) + "%\n")
      file.write("Memory Usage: " + str(memory_usage_percent) + "%\n")
      file.write("Swap Usage: " + ("USED" if swap_used else "NOT USED") + "\n")

    return report_path

def update_log(timestamp, cpu_usage_percent, load_1, load_5, load_15, disk_usage_percent, memory_usage_percent, swap_used):
    log_file = "server_health_log.csv"

    log_line = (
        timestamp + ","
        + str(cpu_usage_percent) + ","
        + str(load_1) + ","
        + str(load_5) + ","
        + str(load_15) + ","
        + str(disk_usage_percent) + ","
        + str(memory_usage_percent) + ","
        + ("1" if swap_used else "0")
        + "\n"
    )

    log_header = "timestamp,cpu,load_1,load_5,load_15,disk,memory,swap\n"

    write_header = not os.path.exists(log_file) or os.path.getsize(log_file) == 0

    with open(log_file, "a") as log:
        if write_header:
            log.write(log_header)
        log.write(log_line)

    return log_file

def load_config():
    default_config = {
        "cpu_warning": 80,
        "disk_warning": 80,
        "memory_warning": 80,
        "load_15_warning": 2.0,
        "warn_on_swap": True
    }

    try:
        with open("config.json", "r") as config_file:
            return json.load(config_file)
    except FileNotFoundError:
        print("[WARNING] config.json not found. Using default config.")
        return default_config
    except json.JSONDecodeError:
        print("[WARNING] config.json is invalid. Using default config.")
        return default_config

def main():
    args = parse_args()
    config = load_config()

    uptime = get_uptime()
    load_1, load_5, load_15 = get_load_average(uptime)

    cpu_usage_percent = get_cpu_usage()
    disk_usage_percent = get_disk_usage()
    memory_usage_percent = get_memory_usage()
    swap_used = get_swap_usage()

    print("=== SERVER HEALTH REPORT ===")
    print("Uptime:", uptime)

    print("CPU Usage:", str(cpu_usage_percent) + "%", end=" ")
    if cpu_usage_percent > config["cpu_warning"]:
        print("- WARNING")
    else:
        print("- OK")

    print("Load Average (1/5/15min):", str(load_1), "/", str(load_5), "/", str(load_15), end=" ")
    if load_15 > config["load_15_warning"]:
        print("- WARNING")
    else:
        print("- OK")

    print("Disk Usage (/):", str(disk_usage_percent) + "%", end=" ")
    if disk_usage_percent > config["disk_warning"]:
        print("- WARNING")
    else:
        print("- OK")

    print("Memory Usage:", str(memory_usage_percent) + "%", end=" ")
    if memory_usage_percent > config["memory_warning"]:
        print("- WARNING")
    else:
        print("- OK")

    print("Swap Usage:", "USED" if swap_used else "NOT USED", end=" ")
    if swap_used and config["warn_on_swap"]:
        print("- WARNING")
    else:
        print("- OK")

    print("============================")

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    if not args.no_save:
        report_filename = save_report(timestamp, uptime, cpu_usage_percent, load_1, load_5, load_15, disk_usage_percent, memory_usage_percent, swap_used, args.output_dir)
        print("Report saved to", report_filename)
    else:
        print("Report saving skipped")

    if not args.no_log:
        log_file = update_log(timestamp, cpu_usage_percent, load_1, load_5, load_15, disk_usage_percent, memory_usage_percent, swap_used)
        print("Log updated:", log_file)
    else:
        print("Log update skipped")

if __name__ == "__main__":
   main()
