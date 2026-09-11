import argparse
import csv
import json
import os
import re
import subprocess
from datetime import datetime
from pathlib import Path


DEFAULT_CONFIG = {
    "cpu_warning": 80,
    "disk_warning": 80,
    "memory_warning": 80,
    "load_15_warning": 2.0,
    "warn_on_swap": True,
    "command_timeout": 5,
}


def parse_args():
    parser = argparse.ArgumentParser(description="Linux server health monitoring tool")
    parser.add_argument("--no-save", action="store_true", help="Do not save report file")
    parser.add_argument("--no-log", action="store_true", help="Do not update CSV log")
    parser.add_argument("-o", "--output-dir", default="reports", help="Directory for generated report files")
    parser.add_argument("-l", "--log-dir", default="logs", help="Directory for CSV log files")
    return parser.parse_args()


def run_command(command, timeout=5):
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except FileNotFoundError:
        return "ERROR: command not found: " + command[0]
    except subprocess.TimeoutExpired:
        return "ERROR: command timed out: " + " ".join(command)
    except Exception as error:
        return "ERROR: " + str(error)

    if result.returncode != 0:
        error_text = result.stderr.strip()
        if error_text:
            return "ERROR: " + error_text
        return "ERROR: command failed: " + " ".join(command)

    return result.stdout.strip()


def load_config():
    try:
        with open("config.json", "r") as config_file:
            user_config = json.load(config_file)
    except FileNotFoundError:
        print("[WARNING] config.json not found. Using default config.")
        return DEFAULT_CONFIG.copy()
    except json.JSONDecodeError:
        print("[WARNING] config.json is invalid. Using default config.")
        return DEFAULT_CONFIG.copy()

    if not isinstance(user_config, dict):
        print("[WARNING] config.json should contain a JSON object. Using default config.")
        return DEFAULT_CONFIG.copy()

    config = DEFAULT_CONFIG.copy()
    config.update(user_config)
    return config


def get_uptime(timeout):
    return run_command(["uptime"], timeout)


def get_load_average(uptime_text):
    load_1 = None
    load_5 = None
    load_15 = None

    load_match = re.search(r"load average: ([0-9.]+), ([0-9.]+), ([0-9.]+)", uptime_text)

    if load_match:
        load_1 = float(load_match.group(1))
        load_5 = float(load_match.group(2))
        load_15 = float(load_match.group(3))

    return load_1, load_5, load_15


def get_cpu_usage(timeout):
    cpu_output = run_command(["top", "-bn1"], timeout)

    if cpu_output.startswith("ERROR:"):
        return None

    for line in cpu_output.splitlines():
        if "%Cpu(s)" in line or "%Cpu" in line:
            parts = line.replace(",", "").split()
            for i in range(len(parts)):
                if parts[i] == "id" and i > 0:
                    cpu_idle = float(parts[i - 1])
                    return int(100 - cpu_idle)

    return None


def get_disk_usage(timeout):
    disk_output = run_command(["df", "-h", "/"], timeout)

    if disk_output.startswith("ERROR:"):
        return None

    lines = disk_output.splitlines()

    if len(lines) < 2:
        return None

    parts = lines[1].split()

    if len(parts) < 5:
        return None

    return int(parts[4].replace("%", ""))


def get_memory_usage(timeout):
    memory_output = run_command(["free"], timeout)

    if memory_output.startswith("ERROR:"):
        return None

    lines = memory_output.splitlines()

    for line in lines:
        if line.startswith("Mem:"):
            parts = line.split()
            if len(parts) >= 3:
                mem_total = int(parts[1])
                mem_used = int(parts[2])
                if mem_total == 0:
                    return None
                return int((mem_used / mem_total) * 100)

    return None


def get_swap_usage(timeout):
    memory_output = run_command(["free"], timeout)

    if memory_output.startswith("ERROR:"):
        return None

    lines = memory_output.splitlines()

    for line in lines:
        if line.startswith("Swap:"):
            parts = line.split()
            if len(parts) >= 3:
                swap_used = int(parts[2])
                return swap_used > 0

    return None


def status_from_threshold(value, warning_threshold):
    if value is None:
        return "UNKNOWN"

    if value > warning_threshold:
        return "WARNING"

    return "OK"


def swap_status(swap_used, warn_on_swap):
    if swap_used is None:
        return "UNKNOWN"

    if swap_used and warn_on_swap:
        return "WARNING"

    return "OK"


def value_or_na(value, suffix=""):
    if value is None:
        return "N/A"

    return str(value) + suffix


def build_report(uptime, cpu_usage_percent, load_1, load_5, load_15, disk_usage_percent, memory_usage_percent, swap_used, config):
    cpu_status = status_from_threshold(cpu_usage_percent, config["cpu_warning"])
    load_status = status_from_threshold(load_15, config["load_15_warning"])
    disk_status = status_from_threshold(disk_usage_percent, config["disk_warning"])
    memory_status = status_from_threshold(memory_usage_percent, config["memory_warning"])
    current_swap_status = swap_status(swap_used, config["warn_on_swap"])

    if swap_used is None:
        swap_text = "N/A"
    elif swap_used:
        swap_text = "USED"
    else:
        swap_text = "NOT USED"

    report_lines = [
        "=== SERVER HEALTH REPORT ===",
        "Uptime: " + uptime,
        "CPU Usage: " + value_or_na(cpu_usage_percent, "%") + " - " + cpu_status,
        "Load Average (1/5/15min): "
        + value_or_na(load_1)
        + " / "
        + value_or_na(load_5)
        + " / "
        + value_or_na(load_15)
        + " - "
        + load_status,
        "Disk Usage (/): " + value_or_na(disk_usage_percent, "%") + " - " + disk_status,
        "Memory Usage: " + value_or_na(memory_usage_percent, "%") + " - " + memory_status,
        "Swap Usage: " + swap_text + " - " + current_swap_status,
        "============================",
    ]

    return "\n".join(report_lines)


def save_report(report_text, timestamp, output_dir):
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    report_filename = "server_health_report_" + timestamp + ".txt"
    report_path = output_path / report_filename

    with open(report_path, "w") as file:
        file.write(report_text + "\n")

    return str(report_path)


def update_log(timestamp, cpu_usage_percent, load_1, load_5, load_15, disk_usage_percent, memory_usage_percent, swap_used, log_dir):
    log_path = Path(log_dir)
    log_path.mkdir(parents=True, exist_ok=True)

    log_file = log_path / "server_health_log.csv"
    write_header = not log_file.exists() or log_file.stat().st_size == 0

    if swap_used is None:
        swap_value = "N/A"
    elif swap_used:
        swap_value = "1"
    else:
        swap_value = "0"

    with open(log_file, "a", newline="") as file:
        writer = csv.writer(file)

        if write_header:
            writer.writerow(["timestamp", "cpu", "load_1", "load_5", "load_15", "disk", "memory", "swap"])

        writer.writerow([
            timestamp,
            value_or_na(cpu_usage_percent),
            value_or_na(load_1),
            value_or_na(load_5),
            value_or_na(load_15),
            value_or_na(disk_usage_percent),
            value_or_na(memory_usage_percent),
            swap_value,
        ])

    return str(log_file)


def main():
    args = parse_args()
    config = load_config()
    timeout = int(config["command_timeout"])

    uptime = get_uptime(timeout)
    load_1, load_5, load_15 = get_load_average(uptime)
    cpu_usage_percent = get_cpu_usage(timeout)
    disk_usage_percent = get_disk_usage(timeout)
    memory_usage_percent = get_memory_usage(timeout)
    swap_used = get_swap_usage(timeout)

    report_text = build_report(
        uptime,
        cpu_usage_percent,
        load_1,
        load_5,
        load_15,
        disk_usage_percent,
        memory_usage_percent,
        swap_used,
        config,
    )

    print(report_text)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    if not args.no_save:
        report_filename = save_report(report_text, timestamp, args.output_dir)
        print("Report saved to", report_filename)
    else:
        print("Report saving skipped")

    if not args.no_log:
        log_file = update_log(
            timestamp,
            cpu_usage_percent,
            load_1,
            load_5,
            load_15,
            disk_usage_percent,
            memory_usage_percent,
            swap_used,
            args.log_dir,
        )
        print("Log updated:", log_file)
    else:
        print("Log update skipped")


if __name__ == "__main__":
    main()
