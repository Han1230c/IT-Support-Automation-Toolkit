#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
System Health Check
- CPU / Memory / Disk summary
- Basic network reachability
- CSV report export to ./reports/
- Daily rolling logs to ./logs/YYYY-MM-DD.log
"""

import argparse
import csv
import logging
import os
import platform
import socket
import subprocess
from datetime import datetime
from pathlib import Path

try:
    import psutil
except ImportError:
    raise SystemExit("Missing dependency: psutil. Install with: pip install psutil")

LOG_DIR = Path("logs")
REPORT_DIR = Path("reports")
LOG_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=LOG_DIR.joinpath(f"{datetime.now():%Y-%m-%d}.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - system_health_check - %(message)s",
)

def check_network(host="8.8.8.8", port=53, timeout=2.0) -> bool:
    """TCP connect to DNS server to infer internet reachability."""
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False

def ping(host="8.8.8.8") -> bool:
    """Best-effort ping (works on macOS/Linux/Windows)."""
    try:
        count_flag = "-n" if platform.system().lower().startswith("win") else "-c"
        result = subprocess.run(
            ["ping", count_flag, "1", host],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=3
        )
        return result.returncode == 0
    except Exception:
        return False

def gather_metrics():
    cpu_percent = psutil.cpu_percent(interval=1)
    vm = psutil.virtual_memory()
    mem_total_gb = round(vm.total / (1024**3), 2)
    mem_used_gb = round(vm.used / (1024**3), 2)
    mem_pct = vm.percent

    disk_rows = []
    for part in psutil.disk_partitions(all=False):
        try:
            usage = psutil.disk_usage(part.mountpoint)
        except PermissionError:
            continue
        disk_rows.append({
            "device": part.device,
            "mountpoint": part.mountpoint,
            "total_gb": round(usage.total / (1024**3), 2),
            "used_gb": round(usage.used / (1024**3), 2),
            "free_gb": round(usage.free / (1024**3), 2),
            "percent": usage.percent,
        })

    net_ok_dns = check_network()
    net_ok_ping = ping()

    return {
        "hostname": socket.gethostname(),
        "os": f"{platform.system()} {platform.release()}",
        "cpu_percent": cpu_percent,
        "mem_total_gb": mem_total_gb,
        "mem_used_gb": mem_used_gb,
        "mem_percent": mem_pct,
        "disk_rows": disk_rows,
        "net_ok_dns": net_ok_dns,
        "net_ok_ping": net_ok_ping,
    }

def recommend(metrics, cpu_threshold=85, mem_threshold=85, disk_threshold=90):
    recs = []
    if metrics["cpu_percent"] >= cpu_threshold:
        recs.append(f"High CPU usage: {metrics['cpu_percent']}% (>{cpu_threshold}%)")
    if metrics["mem_percent"] >= mem_threshold:
        recs.append(f"High memory usage: {metrics['mem_percent']}% (>{mem_threshold}%)")
    for d in metrics["disk_rows"]:
        if d["percent"] >= disk_threshold:
            recs.append(f"Low disk space on {d['mountpoint']}: {d['percent']}% used")
    if not metrics["net_ok_dns"] or not metrics["net_ok_ping"]:
        recs.append("Network connectivity check failed (DNS or ping).")
    if not recs:
        recs.append("System is running normally.")
    return recs

def export_csv(metrics, out_path: Path):
    with out_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Section", "Metric", "Value"])
        w.writerow(["Meta", "Hostname", metrics["hostname"]])
        w.writerow(["Meta", "OS", metrics["os"]])
        w.writerow(["CPU", "CPU Usage %", metrics["cpu_percent"]])
        w.writerow(["Memory", "Total (GB)", metrics["mem_total_gb"]])
        w.writerow(["Memory", "Used (GB)", metrics["mem_used_gb"]])
        w.writerow(["Memory", "Used %", metrics["mem_percent"]])
        for d in metrics["disk_rows"]:
            w.writerow(["Disk", f"{d['mountpoint']} used %", d["percent"]])
            w.writerow(["Disk", f"{d['mountpoint']} free (GB)", d["free_gb"]])
        w.writerow(["Network", "DNS TCP 8.8.8.8:53", metrics["net_ok_dns"]])
        w.writerow(["Network", "Ping 8.8.8.8", metrics["net_ok_ping"]])

def main():
    ap = argparse.ArgumentParser(description="System Health Check")
    ap.add_argument("--cpu-threshold", type=int, default=85)
    ap.add_argument("--mem-threshold", type=int, default=85)
    ap.add_argument("--disk-threshold", type=int, default=90)
    ap.add_argument("--report-name", default=None, help="Custom report filename")
    args = ap.parse_args()

    logging.info("Start system health check")
    metrics = gather_metrics()
    recs = recommend(metrics, args.cpu_threshold, args.mem_threshold, args.disk_threshold)

    # Console pretty print
    print("=" * 50)
    print("SYSTEM HEALTH CHECK REPORT")
    print("=" * 50)
    print(f"Hostname: {metrics['hostname']}")
    print(f"OS: {metrics['os']}\n")
    print(f"CPU Usage: {metrics['cpu_percent']}%")
    print(f"Memory Used: {metrics['mem_used_gb']}/{metrics['mem_total_gb']} GB ({metrics['mem_percent']}%)\n")
    print("Disk:")
    for d in metrics["disk_rows"]:
        print(f"  {d['mountpoint']}: used {d['percent']}% | free {d['free_gb']} GB")
    print("\nNetwork:")
    print(f"  DNS TCP 8.8.8.8:53 -> {'OK' if metrics['net_ok_dns'] else 'FAIL'}")
    print(f"  Ping 8.8.8.8       -> {'OK' if metrics['net_ok_ping'] else 'FAIL'}")
    print("\nRecommendations:")
    for r in recs:
        print(f"  - {r}")

    # Export CSV
    ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    name = args.report_name or f"system_report_{ts}.csv"
    out_path = REPORT_DIR.joinpath(name)
    export_csv(metrics, out_path)
    logging.info(f"Report exported -> {out_path}")
    print(f"\n✅ Report saved: {out_path}")

if __name__ == "__main__":
    main()
