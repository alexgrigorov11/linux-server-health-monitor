# Project Plan

## Project name

Linux Server Health Monitoring Tool

## Project goal

Build a simple Linux system monitoring tool for infrastructure automation practice.

The tool collects system health data, prints a terminal report, saves timestamped reports, and keeps a CSV history log.

## Real-world use case

A small IT team, system administrator, or infrastructure engineer can use this type of tool to quickly check basic Linux server health.

It can help identify:

- high CPU usage
- high memory usage
- high disk usage
- swap usage
- abnormal load average
- system uptime

## Sasha's role

Sasha is responsible for the infrastructure automation part:

- Linux commands
- Python scripting
- system metrics collection
- parsing command output
- report generation
- CSV logging
- JSON configuration
- command line options
- Git repository setup
- README documentation

## Zheka's role

Zheka is responsible for the security and DevSecOps review:

- check file permissions
- check that no secrets are stored
- review generated logs and reports
- review `.gitignore`
- check that commands are read-only
- write security recommendations
- suggest future security improvements

## Current features

- CPU usage check
- load average parsing
- disk usage check
- memory usage check
- swap usage check
- uptime collection
- OK/WARNING logic
- configurable thresholds using `config.json`
- timestamped text reports
- CSV log history
- CSV header
- basic error handling
- command line options:
  - `--no-save`
  - `--no-log`
- clean `main()` function
- reusable Python functions

## Project files

- `system_report.py` — main Python monitoring script
- `config.json` — warning thresholds
- `README.md` — project documentation
- `SECURITY.md` — security notes and review tasks
- `.gitignore` — ignored generated files
- `PROJECT_PLAN.md` — project plan and roles

## What should not be committed

Generated files should not be committed:

- `server_health_report*.txt`
- `server_health_log.csv`
- backup files
- test scripts
- Python cache files

## Future improvements

- add output directory for reports
- add log rotation
- add better command error handling
- add tests
- add GitHub Actions
- add shell script installer
- add Docker version
- add monitoring dashboard later
- add security scanning in CI/CD
- add remote server checks over SSH

## Definition of done

This project is considered complete when:

- the script runs successfully
- reports are generated correctly
- CSV log is updated correctly
- config thresholds work
- command line options work
- README is written
- security notes are written
- project plan is written
- Git commits are clean
- the project is ready to upload to GitHub
