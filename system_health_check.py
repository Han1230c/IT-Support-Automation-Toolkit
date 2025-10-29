#!/usr/bin/env python3
"""
System Health Check Script
Author: Xiaohan Chen
Purpose: Automated system health monitoring for IT support
"""

import platform
import psutil
import datetime
import socket

def check_system_info():
    """Gather basic system information"""
    print("=" * 50)
    print("SYSTEM HEALTH CHECK REPORT")
    print("=" * 50)
    print(f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Hostname: {socket.gethostname()}")
    print(f"OS: {platform.system()} {platform.release()}")
    print(f"Architecture: {platform.machine()}")
    print()

def check_cpu():
    """Check CPU usage"""
    print("CPU INFORMATION:")
    print(f"  Physical Cores: {psutil.cpu_count(logical=False)}")
    print(f"  Total Cores: {psutil.cpu_count(logical=True)}")
    print(f"  Current Usage: {psutil.cpu_percent(interval=1)}%")
    
    # Alert if CPU usage is high
    cpu_usage = psutil.cpu_percent(interval=1)
    if cpu_usage > 80:
        print(f"  ⚠️ WARNING: High CPU usage detected!")
    print()

def check_memory():
    """Check memory usage"""
    memory = psutil.virtual_memory()
    print("MEMORY INFORMATION:")
    print(f"  Total: {memory.total / (1024**3):.2f} GB")
    print(f"  Available: {memory.available / (1024**3):.2f} GB")
    print(f"  Used: {memory.used / (1024**3):.2f} GB ({memory.percent}%)")
    
    # Alert if memory usage is high
    if memory.percent > 85:
        print(f"  ⚠️ WARNING: High memory usage detected!")
    print()

def check_disk():
    """Check disk usage"""
    print("DISK INFORMATION:")
    partitions = psutil.disk_partitions()
    for partition in partitions:
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            print(f"  Drive {partition.device}:")
            print(f"    Total: {usage.total / (1024**3):.2f} GB")
            print(f"    Used: {usage.used / (1024**3):.2f} GB ({usage.percent}%)")
            print(f"    Free: {usage.free / (1024**3):.2f} GB")
            
            # Alert if disk usage is high
            if usage.percent > 90:
                print(f"    ⚠️ WARNING: Low disk space!")
        except PermissionError:
            print(f"    ⚠️ Access denied to {partition.device}")
        print()

def check_network():
    """Check network connectivity"""
    print("NETWORK INFORMATION:")
    print(f"  Hostname: {socket.gethostname()}")
    try:
        print(f"  IP Address: {socket.gethostbyname(socket.gethostname())}")
    except:
        print(f"  IP Address: Unable to retrieve")
    
    # Check internet connectivity
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        print(f"  Internet: ✓ Connected")
    except OSError:
        print(f"  Internet: ✗ Disconnected")
    print()

def generate_summary():
    """Generate summary and recommendations"""
    print("=" * 50)
    print("RECOMMENDATIONS:")
    
    memory = psutil.virtual_memory()
    cpu_usage = psutil.cpu_percent(interval=1)
    
    issues = []
    if cpu_usage > 80:
        issues.append("- Investigate high CPU usage processes")
    if memory.percent > 85:
        issues.append("- Close unnecessary applications to free memory")
    
    for partition in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            if usage.percent > 90:
                issues.append(f"- Clean up disk space on {partition.device}")
        except:
            pass
    
    if not issues:
        print("✓ System is running normally")
    else:
        for issue in issues:
            print(issue)
    
    print("=" * 50)

def main():
    """Main function to run all checks"""
    try:
        check_system_info()
        check_cpu()
        check_memory()
        check_disk()
        check_network()
        generate_summary()
    except Exception as e:
        print(f"Error running health check: {e}")

if __name__ == "__main__":
    main()
