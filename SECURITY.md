# Security Notes

This project is a local Linux system monitoring tool created for infrastructure automation practice.

## Security scope

The script collects basic local system information:

- CPU usage
- load average
- disk usage
- memory usage
- swap usage
- uptime

The script does not collect passwords, tokens, SSH keys, API keys, personal files, or application secrets.

## Files created by the script

The script can create:

- timestamped text reports
- a CSV history log

Generated reports and logs are ignored by Git using `.gitignore`.

## Configuration

Warning thresholds are stored in `config.json`.

The config file should not contain secrets.

## Permissions

Recommended file permissions:

```bash
chmod 644 config.json
chmod 644 README.md
chmod 644 SECURITY.md
chmod 755 system_report.py
