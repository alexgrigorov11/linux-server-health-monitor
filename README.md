# Linux Server Health Monitoring Tool

A Python-based Linux monitoring tool that checks basic system health and generates reports.

Generated reports are saved inside the `reports/` directory.

Example:

```text
reports/server_health_report_2026-09-08_18-48-53.txt
```

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
- Saves timestamped report files inside the `reports/` directory
- Updates a CSV history log
- Supports command line options:
  - `--no-save`
  - `--no-log`
- Uses a clean `main()` structure
- Includes basic error handling for missing or invalid config files

## Example usage

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

Show help:

```bash
python system_report.py --help
```

## Project files

- `system_report.py` — main Python monitoring script
- `config.json` — warning thresholds
- `README.md` — project documentation
- `SECURITY.md` — security notes
- `PROJECT_PLAN.md` — project plan
- `.gitignore` — ignored generated files

## Generated files

The script can create generated files such as:

- timestamped reports inside `reports/`
- `server_health_log.csv`

These files should not be committed to GitHub.

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

## Project status

Completed as part of my Platform Engineering / SRE / Infrastructure Automation learning path.
