#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
User Account Report
- Reads a CSV with columns: userPrincipalName, status, department, isAdmin, lastLogin(YYYY-MM-DD)
- Computes active/disabled/inactive(>90d), missing department, admin accounts
- Exports summary + detailed CSV to ./reports/
- Logs to ./logs/
- If no --input provided, uses demo dataset
"""

import argparse
import csv
import logging
from datetime import datetime, timedelta
from pathlib import Path

LOG_DIR = Path("logs")
REPORT_DIR = Path("reports")
LOG_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=LOG_DIR.joinpath(f"{datetime.now():%Y-%m-%d}.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - user_account_report - %(message)s",
)

def load_rows(path: Path | None):
    if path is None:
        # Demo data
        return [
            {"userPrincipalName":"alice.wang@contoso.com", "status":"Active", "department":"IT", "isAdmin":"False", "lastLogin":"2025-10-20"},
            {"userPrincipalName":"bob.chen@contoso.com",   "status":"Disabled", "department":"IT", "isAdmin":"False", "lastLogin":"2025-07-01"},
            {"userPrincipalName":"carol.li@contoso.com",   "status":"Active", "department":"", "isAdmin":"True", "lastLogin":"2025-05-10"},
            {"userPrincipalName":"david.z@contoso.com",    "status":"Active", "department":"HR", "isAdmin":"False", "lastLogin":"2024-12-01"},
        ]
    rows = []
    with path.open(newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            rows.append(row)
    return rows

def parse_date(s: str | None):
    if not s:
        return None
    try:
        return datetime.strptime(s.strip(), "%Y-%m-%d")
    except ValueError:
        return None

def analyze(rows):
    today = datetime.now()
    inactive_cutoff = today - timedelta(days=90)
    stats = {
        "total": 0, "active": 0, "disabled": 0,
        "inactive_gt_90d": 0, "missing_dept": 0, "admin_count": 0
    }
    detail = []
    for r in rows:
        stats["total"] += 1
        status = (r.get("status","") or "").strip().lower()
        dept   = (r.get("department","") or "").strip()
        admin  = (r.get("isAdmin","False") or "False").strip().lower() in ("true","1","yes")
        last_login = parse_date(r.get("lastLogin"))

        if status == "active":
            stats["active"] += 1
        elif status == "disabled":
            stats["disabled"] += 1

        if not dept:
            stats["missing_dept"] += 1
        if admin:
            stats["admin_count"] += 1
        if last_login and last_login < inactive_cutoff and status != "disabled":
            stats["inactive_gt_90d"] += 1

        detail.append({
            "userPrincipalName": r.get("userPrincipalName",""),
            "status": r.get("status",""),
            "department": dept or "(missing)",
            "isAdmin": admin,
            "lastLogin": r.get("lastLogin",""),
            "flag_inactive_gt_90d": bool(last_login and last_login < inactive_cutoff and status != "disabled"),
            "flag_missing_dept": not bool(dept),
        })
    return stats, detail

def export_summary(stats, out_path: Path):
    with out_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Metric", "Value"])
        for k, v in stats.items():
            w.writerow([k, v])

def export_detail(detail, out_path: Path):
    if not detail:
        out_path.write_text("", encoding="utf-8"); return
    keys = list(detail[0].keys())
    with out_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        w.writerows(detail)

def main():
    ap = argparse.ArgumentParser(description="User Account Report")
    ap.add_argument("--input", help="Path to CSV (optional). If omitted, demo data is used.")
    args = ap.parse_args()

    logging.info("Start user account report")
    rows = load_rows(Path(args.input)) if args.input else load_rows(None)
    stats, detail = analyze(rows)

    ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    summary_path = REPORT_DIR.joinpath(f"user_audit_summary_{ts}.csv")
    detail_path  = REPORT_DIR.joinpath(f"user_audit_detail_{ts}.csv")
    export_summary(stats, summary_path)
    export_detail(detail, detail_path)

    print("User Account Report")
    print("-" * 35)
    for k, v in stats.items():
        print(f"{k:>18}: {v}")
    print(f"\n✅ Summary -> {summary_path}\n✅ Detail  -> {detail_path}")
    logging.info(f"Reports exported -> {summary_path}, {detail_path}")

if __name__ == "__main__":
    main()
