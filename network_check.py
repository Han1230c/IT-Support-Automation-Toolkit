#!/usr/bin/env python3
"""
Network Connectivity Checker
Author: Xiaohan Chen
Purpose: Automated network troubleshooting tool for IT support
"""

import socket
import platform
import subprocess
import time
from datetime import datetime

def print_header(title):
    """Print formatted section header"""
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)

def check_dns_resolution(hostname):
    """Check if DNS resolution is working"""
    try:
        ip = socket.gethostbyname(hostname)
        return True, ip
    except socket.gaierror:
        return False, None

def check_port_connectivity(host, port, timeout=3):
    """Check if a specific port is reachable"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except Exception as e:
        return False

def ping_host(host, count=4):
    """Ping a host and return success status"""
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, str(count), host]
    
    try:
        output = subprocess.run(command, capture_output=True, text=True, timeout=10)
        return output.returncode == 0, output.stdout
    except Exception as e:
        return False, str(e)

def check_internet_connectivity():
    """Check internet connectivity using multiple methods"""
    print_header("INTERNET CONNECTIVITY CHECK")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Test DNS servers
    dns_servers = [
        ("Google DNS", "8.8.8.8"),
        ("Cloudflare DNS", "1.1.1.1"),
        ("Quad9 DNS", "9.9.9.9")
    ]
    
    print("Testing DNS Servers:")
    dns_working = False
    for name, ip in dns_servers:
        reachable = check_port_connectivity(ip, 53)
        status = "✓ Reachable" if reachable else "✗ Unreachable"
        print(f"  {name} ({ip}): {status}")
        if reachable:
            dns_working = True
    print()
    
    # Test common websites
    websites = [
        "google.com",
        "cloudflare.com",
        "microsoft.com"
    ]
    
    print("Testing DNS Resolution:")
    dns_resolving = False
    for site in websites:
        success, ip = check_dns_resolution(site)
        if success:
            print(f"  {site}: ✓ Resolved to {ip}")
            dns_resolving = True
        else:
            print(f"  {site}: ✗ Failed to resolve")
    print()
    
    # Test HTTP/HTTPS connectivity
    print("Testing HTTP/HTTPS Connectivity:")
    web_servers = [
        ("google.com", 443),
        ("cloudflare.com", 443),
        ("microsoft.com", 80)
    ]
    
    http_working = False
    for host, port in web_servers:
        reachable = check_port_connectivity(host, port)
        protocol = "HTTPS" if port == 443 else "HTTP"
        status = "✓ Connected" if reachable else "✗ Failed"
        print(f"  {host}:{port} ({protocol}): {status}")
        if reachable:
            http_working = True
    print()
    
    # Overall status
    print("DIAGNOSIS:")
    if dns_working and dns_resolving and http_working:
        print("  ✓ Internet connection is working normally")
    elif not dns_working:
        print("  ✗ DNS servers unreachable - Check network connection")
        print("  Recommendation: Verify physical connection and IP configuration")
    elif not dns_resolving:
        print("  ✗ DNS resolution failing - DNS configuration issue")
        print("  Recommendation: Check DNS settings, try flushing DNS cache")
    elif not http_working:
        print("  ✗ HTTP/HTTPS blocked - Possible firewall issue")
        print("  Recommendation: Check firewall and proxy settings")

def check_local_network():
    """Check local network configuration"""
    print_header("LOCAL NETWORK CONFIGURATION")
    
    # Get hostname
    hostname = socket.gethostname()
    print(f"Hostname: {hostname}")
    
    # Get local IP
    try:
        local_ip = socket.gethostbyname(hostname)
        print(f"Local IP: {local_ip}")
    except:
        print(f"Local IP: Unable to retrieve")
    
    # Check default gateway (simplified)
    print(f"Operating System: {platform.system()} {platform.release()}")
    print()

def test_specific_host(host):
    """Test connectivity to a specific host"""
    print_header(f"TESTING CONNECTIVITY TO: {host}")
    
    # DNS resolution
    print("1. DNS Resolution:")
    success, ip = check_dns_resolution(host)
    if success:
        print(f"   ✓ Resolved to: {ip}\n")
    else:
        print(f"   ✗ Failed to resolve hostname\n")
        print("RECOMMENDATION: Check DNS settings or hostname spelling")
        return
    
    # Ping test
    print("2. Ping Test:")
    success, output = ping_host(host)
    if success:
        print(f"   ✓ Host is reachable")
    else:
        print(f"   ✗ Host is unreachable")
    print()
    
    # Common port tests
    print("3. Common Port Tests:")
    common_ports = {
        80: "HTTP",
        443: "HTTPS",
        22: "SSH",
        3389: "RDP",
        445: "SMB"
    }
    
    for port, service in common_ports.items():
        reachable = check_port_connectivity(ip, port, timeout=2)
        status = "✓ Open" if reachable else "✗ Closed/Filtered"
        print(f"   Port {port} ({service}): {status}")
    
    print()

def main():
    """Main function"""
    print("=" * 60)
    print("NETWORK CONNECTIVITY DIAGNOSTIC TOOL")
    print("=" * 60)
    print("This tool helps diagnose common network connectivity issues")
    
    # Run general internet connectivity check
    check_internet_connectivity()
    
    # Check local network
    check_local_network()
    
    # Optional: Test specific host
    print("\n" + "=" * 60)
    print("To test a specific host, run:")
    print("  python network_check.py <hostname>")
    print("Example: python network_check.py example.com")
    print("=" * 60)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        test_specific_host(sys.argv[1])
    else:
        main()
