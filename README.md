# Linux Server Health Monitoring Tool

A Python-based Linux monitoring tool that checks basic system health and generates reports.

## What it checks

- CPU usage
- Load average
- Disk usage
- Memory usage
- Swap usage
- System uptime

## Features

- Runs Linux commands from Python
- Parses command output
- Uses configurable warning thresholds from `config.json`
- Saves timestamped report files
- Updates a CSV history log
- Supports command line options:
  - `--no-save`
  - `--no-log`
- Uses a clean `main()` structure
- Includes basic error handling for missing or invalid config files

## Example usage

```bash
python system_report.py
