import json

from system_report import (
    DEFAULT_CONFIG,
    build_report,
    load_config,
    status_from_threshold,
    swap_status,
)


def test_status_from_threshold():
    assert status_from_threshold(50, 80) == "OK"
    assert status_from_threshold(81, 80) == "WARNING"
    assert status_from_threshold(None, 80) == "UNKNOWN"


def test_swap_status():
    assert swap_status(False, True) == "OK"
    assert swap_status(True, True) == "WARNING"
    assert swap_status(True, False) == "OK"
    assert swap_status(None, True) == "UNKNOWN"


def test_load_config_merges_defaults(tmp_path):
    path = tmp_path / "config.json"
    path.write_text(json.dumps({"cpu_warning": 70}), encoding="utf-8")
    config = load_config(path)
    assert config["cpu_warning"] == 70
    assert config["disk_warning"] == DEFAULT_CONFIG["disk_warning"]


def test_build_report_marks_high_cpu():
    config = DEFAULT_CONFIG.copy()
    report = build_report("1 hour", 90, 1.0, 1.0, 1.0, 20, 30, False, config)
    assert "CPU Usage: 90% - WARNING" in report
    assert "Swap Usage: NOT USED - OK" in report
