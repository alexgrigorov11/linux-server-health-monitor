# Linux Server Health Monitoring Tool

A Python-based Linux monitoring tool that checks basic system health and generates reports.

Generated reports are saved inside the `reports/` directory by default.

The output directory can also be changed with the `--output-dir` option.

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
- Supports custom output directories with `--output-dir` or `-o`
- Updates a CSV history log
- Supports command line options:
  - `--no-save`
  - `--no-log`
  - `--output-dir`
  - `-o`
- Uses a clean `main()` structure
- Includes basic error handling for missing or invalid config files

## Example usage

Run the script:

```bash
python system_report.py
```

Run without saving a report:

```bash
python system_report.py --no-save
```

Run without updating the CSV log:

```bash
python system_report.py --no-log
```

Run with a custom output directory:

```bash
python system_report.py --output-dir reports
```

Short version:

```bash
python system_report.py -o reports
```

Show help:

```bash
python system_report.py --help
```

## Example output

```text
=== SERVER HEALTH REPORT ===
Uptime: 15:49:21 up 5:54, 1 user, load average: 0.34, 0.57, 0.62
CPU Usage: 7% - OK
Load Average (1/5/15min): 0.34 / 0.57 / 0.62 - OK
Disk Usage (/): 26% - OK
Memory Usage: 35% - OK
Swap Usage: NOT USED - OK
============================
Report saved to reports/server_health_report_2026-09-11_15-49-22.txt
Log updated: server_health_log.csv
```

## Project files

- `system_report.py` — main Python monitoring script
- `config.json` — warning thresholds
- `README.md` — project documentation
- `SECURITY.md` — security notes
- `PROJECT_PLAN.md` — project plan
- `.gitignore` — ignored generated files
- `.github/workflows/python-check.yml` — GitHub Actions workflow

## Generated files

The script can create generated files such as:

- timestamped reports inside `reports/`
- reports inside a custom output directory
- `server_health_log.csv`

These files should not be committed to GitHub.

## Configuration

Warning thresholds are stored in `config.json`.

Example:

```json
{
    "cpu_warning": 80,
    "disk_warning": 80,
    "memory_warning": 80,
    "load_15_warning": 2.0,
    "warn_on_swap": true
}
```

## GitHub Actions

This project uses GitHub Actions to automatically check the Python script.

The workflow runs on:

- push
- pull request

The workflow checks:

- Python syntax
- help command execution

## Skills demonstrated

- Linux basics
- Python scripting
- Infrastructure automation
- Monitoring basics
- Log parsing
- CSV logging
- JSON configuration
- Error handling
- Command line arguments
- Git and GitHub workflow
- GitHub Issues
- Pull Requests
- GitHub Actions CI

## Project status

Completed as part of my Platform Engineering / SRE / Infrastructure Automation learning path.
