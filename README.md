
# 🧰 IT Support Automation Toolkit

A Python-based automation suite that streamlines IT Support daily operations — including system health checks, network diagnostics, and user account audits.  
Designed for internal IT teams to improve consistency, reduce manual work, and produce standardized reports with one command.

---

## 🚀 Overview

This toolkit provides three fully automated diagnostic modules integrated through a single command-line interface (CLI):

| Module | Description | Output |
|---------|--------------|--------|
| 🖥️ **System Health Check** | Collects system metrics (CPU, RAM, disk, OS info) | CSV report |
| 🌐 **Network Connectivity Check** | Tests DNS, Ping, and port reachability | TXT + CSV report |
| 👤 **User Account Report** | Audits active/disabled users, inactive accounts, and admin counts | Summary + Detail CSV |

After execution, all results are summarized into an **HTML dashboard**, ready for review or archival.

---

## ⚙️ Key Features

- 🧩 **Modular architecture** – Each module runs independently or through unified CLI  
- ⚡ **One-command automation** – Run all checks with `--all`  
- 🧹 **Smart cleanup** – Remove old logs/reports with `--clean` or `--clean-only`  
- 📊 **Comprehensive summary** – Auto-generated HTML report consolidating all results  
- 🕒 **Performance tracking** – Execution time and line count per module  
- 🧾 **Structured logging** – Daily logs with INFO/WARN/ERROR levels  
- ⚙️ **Cross-platform** – Works on macOS, Linux, and Windows (Python 3.9+)  
- 🔄 **Configurable** – Supports external JSON or key=value config files  

---

## 🖥️ Example Usage

```bash
# Run all modules
python3 toolkit_cli.py --all

# Clean old logs/reports before running
python3 toolkit_cli.py --clean --all

# Only clean and exit
python3 toolkit_cli.py --clean-only

# Run only system health check
python3 toolkit_cli.py --system

# Network check for a custom target
python3 toolkit_cli.py --network --target example.com
```

---

## 📁 Output Structure

```
IT-Support-Automation-Toolkit/
├─ reports/
│   ├─ system_report_*.csv
│   ├─ network_report_*.txt
│   ├─ user_audit_summary_*.csv
│   ├─ user_audit_detail_*.csv
│   └─ summary_*.html
│
├─ logs/
│   └─ daily.log
│
├─ toolkit_cli.py
├─ system_health_check.py
├─ network_check.py
├─ user_account_report.py
└─ config.example.json
```

> Each module writes time-stamped CSV/TXT files for traceability.  
> `summary_*.html` provides a unified overview with warnings, durations, and line counts.

---

## 🧠 Internal Workflow

### 1. `toolkit_cli.py` (Main Orchestrator)
- Parses CLI arguments  
- Handles cleaning, logging, and configuration  
- Calls each sub-module (`subprocess.run`)  
- Merges results into one HTML summary  

### 2. `system_health_check.py`
- Uses **psutil** to gather system information  
- Detects low disk space and outputs recommendations  

### 3. `network_check.py`
- Tests DNS, Ping, and port connectivity (default: 443)  
- Generates both `.txt` and `.csv` reports  

### 4. `user_account_report.py`
- Generates demo user statistics (active, disabled, inactive)  
- Produces summary + detailed reports  

---

## 🧩 Tech Stack

| Library | Purpose |
|----------|----------|
| **Python 3.9+** | Core language |
| **psutil** | System metrics |
| **argparse / subprocess** | CLI orchestration |
| **csv / html / json** | Reporting and configuration |
| **datetime / logging** | Logs and timestamps |

---

## 🧰 Installation

```bash
git clone https://github.com/Han1230c/IT-Support-Automation-Toolkit.git
cd IT-Support-Automation-Toolkit
pip install psutil
python3 toolkit_cli.py --all
```

*(No external dependencies beyond psutil.)*

---

## 🧱 Design Goals

- Reduce manual diagnostic effort for IT teams  
- Standardize health and network audit processes  
- Generate reliable, traceable reports  
- Serve as a reusable base for larger monitoring systems  

---

## 🔮 Future Enhancements

- Slack / Email notifications  
- Remote system checks via SSH or WinRM  
- Integration with Active Directory (LDAP queries)  
- Web dashboard with Flask or Streamlit  

---

## 📄 License

MIT License © 2025  
For educational and professional demonstration of IT automation.
