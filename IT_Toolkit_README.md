# IT Support Automation Toolkit

A collection of Python scripts developed for automating common IT support tasks and improving troubleshooting efficiency.

**Author:** Xiaohan Chen  
**Purpose:** Practical IT automation tools for help desk and system administration tasks  
**Date:** October 2024 - Present

## 📋 Overview

This toolkit contains scripts I developed to automate repetitive IT support tasks, improve system monitoring, and streamline troubleshooting procedures. These tools demonstrate practical scripting skills applicable to real-world IT support scenarios.

## 🛠️ Tools Included

### 1. System Health Check (`system_health_check.py`)
Automated system monitoring and health reporting tool.

**Features:**
- CPU usage monitoring with threshold alerts
- Memory utilization tracking
- Disk space analysis across all drives
- Network connectivity verification
- Automated recommendations based on system status

**Use Cases:**
- Proactive system monitoring
- Quick health checks during user support calls
- Regular system maintenance reports

**Usage:**
```bash
python system_health_check.py
```

**Sample Output:**
```
==================================================
SYSTEM HEALTH CHECK REPORT
==================================================
Generated: 2024-10-29 14:30:00
Hostname: IT-SUPPORT-01
OS: Windows 10

CPU INFORMATION:
  Physical Cores: 4
  Total Cores: 8
  Current Usage: 23.5%

MEMORY INFORMATION:
  Total: 16.00 GB
  Available: 8.45 GB
  Used: 7.55 GB (47.2%)

RECOMMENDATIONS:
✓ System is running normally
==================================================
```

---

### 2. User Account Report Generator (`user_account_report.py`)
Generates comprehensive user account reports for IT audits and account management.

**Features:**
- User account status tracking (Active/Inactive/Disabled)
- Department-based user distribution
- Inactive user identification
- Security concern detection (missing info, admin accounts)
- CSV export for further analysis

**Use Cases:**
- Regular user account audits
- Identifying accounts for deprovisioning
- Department-based user statistics
- Security compliance reporting

**Usage:**
```bash
python user_account_report.py
```

**Input:** CSV file with user data (sample data auto-generated for demo)  
**Output:** Detailed report and CSV export with timestamp

---

### 3. Network Connectivity Checker (`network_check.py`)
Comprehensive network troubleshooting and diagnostic tool.

**Features:**
- DNS server reachability tests
- DNS resolution verification
- HTTP/HTTPS connectivity checks
- Multi-target ping tests
- Common port scanning (HTTP, HTTPS, SSH, RDP, SMB)
- Automated diagnosis with recommendations

**Use Cases:**
- First-line network troubleshooting
- Diagnosing connectivity issues
- Verifying DNS configuration
- Testing specific host reachability

**Usage:**
```bash
# General internet connectivity check
python network_check.py

# Test specific host
python network_check.py example.com
```

**Sample Diagnosis:**
```
INTERNET CONNECTIVITY CHECK
Testing DNS Servers:
  Google DNS (8.8.8.8): ✓ Reachable
  Cloudflare DNS (1.1.1.1): ✓ Reachable

Testing DNS Resolution:
  google.com: ✓ Resolved to 142.250.80.46

DIAGNOSIS:
  ✓ Internet connection is working normally
```

---

## 💻 Technical Details

**Language:** Python 3.x  
**Dependencies:**
- `psutil` - System and process utilities
- `socket` - Network connectivity
- `csv` - Data export/import
- Built-in libraries: `platform`, `subprocess`, `datetime`

**Installation:**
```bash
pip install psutil
```

## 🎯 Skills Demonstrated

- **Python Scripting:** Clean, maintainable code with proper error handling
- **System Administration:** Understanding of OS-level monitoring and management
- **Network Troubleshooting:** DNS, connectivity, port scanning
- **Automation:** Reducing manual workload through scripting
- **Documentation:** Clear README, code comments, and usage instructions
- **Problem-Solving:** Practical solutions to real IT support scenarios

## 📈 Future Enhancements

Planned improvements:
- [ ] PowerShell versions for Windows environments
- [ ] Active Directory integration for user account management
- [ ] Email alerting for critical system issues
- [ ] Web dashboard for centralized monitoring
- [ ] Log file analysis and parsing tools

## 🔧 Real-World Applications

These scripts can be adapted for:
- **Help Desk:** Quick system diagnostics during user support calls
- **System Administration:** Automated daily health checks
- **IT Audits:** Regular account and security reviews
- **Troubleshooting:** Structured network diagnostic procedures
- **Documentation:** Auto-generated reports for ticket documentation

## 📝 Notes

- All scripts include error handling for production reliability
- Designed for cross-platform compatibility (Windows/Linux/macOS)
- Sample data provided for testing and demonstration
- Can be easily customized for specific organizational needs

---

**Last Updated:** October 2024  
**Contact:** elsie.c03@outlook.com  
**GitHub:** Han1230c
