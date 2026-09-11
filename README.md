# Linux Server Health Monitoring Tool

A Python-based Linux monitoring tool that checks basic system health and generates reports.

This project is built as a portfolio-ready infrastructure automation project for Platform Engineering / SRE practice.

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
- Saves reports inside the `reports/` directory by default
- Supports custom report output directories with `--output-dir` or `-o`
- Saves CSV logs inside the `logs/` directory by default
- Supports custom CSV log directories with `--log-dir` or `-l`
- Supports command line options:
  - `--no-save`
  - `--no-log`
  - `--output-dir`
  - `-o`
  - `--log-dir`
  - `-l`
- Includes safer Linux command execution
- Includes command timeout handling
- Uses a clean `main()` structure
- Uses reusable Python functions
- Includes GitHub Actions CI checks

## Example usage

Run the script:

```bash
python system_report.py
