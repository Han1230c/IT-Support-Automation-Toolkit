
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse, socket, time, sys, os
from pathlib import Path
from datetime import datetime

DEFAULT_TARGET = "8.8.8.8"
DEFAULT_PORTS = [80, 443, 22, 3389, 445]

def check_dns():
    results = []
    for dns in ["8.8.8.8","1.1.1.1"]:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1.0)
            s.connect((dns, 53))
            results.append((dns, True))
            s.close()
        except Exception:
            results.append((dns, False))
    return results

def resolve_host(host):
    try:
        ip = socket.gethostbyname(host)
        return ip, True
    except Exception:
        return None, False

def ping_like(host, timeout=1.0):
    # Simple TCP connect to 443 as a ping-like test
    try:
        s = socket.create_connection((host, 443), timeout=timeout)
        s.close()
        return True
    except Exception:
        return False

def check_ports(host, ports, timeout):
    results = []
    for p in ports:
        try:
            s = socket.create_connection((host, p), timeout=timeout)
            s.close()
            results.append((p, True))
        except Exception:
            results.append((p, False))
    return results

def write_reports(outdir, target, dns_ok, ping_ok, resolved_ip, ports_results):
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    txt = outdir / f"network_report_{ts}.txt"
    csv = outdir / f"network_report_{ts}.csv"

    # TXT
    with open(txt,"w",encoding="utf-8") as f:
        f.write("INTERNET CONNECTIVITY CHECK\n")
        f.write("------------------------------------------\n")
        f.write(f"Target Host: {target}\n")
        for ip, ok in dns_ok:
            f.write(f"DNS {ip}:53 -> {'OK' if ok else 'FAILED'}\n")
        f.write(f"Ping {target}   -> {'OK' if ping_ok else 'FAILED'}\n")
        if resolved_ip:
            f.write(f"Resolve {target} -> {resolved_ip}\n")
        else:
            f.write(f"Resolve {target} -> FAILED\n")
        f.write("\nPort Checks:\n")
        for p, ok in ports_results:
            f.write(f"  {target}:{p} -> {'OPEN' if ok else 'CLOSED/NO RESPONSE'}\n")
        f.write("\nDiagnosis:\n")
        if ping_ok and any(ok for _,ok in ports_results):
            f.write("  ✓ Internet connection seems stable.\n")
        elif any(ok for _,ok in dns_ok):
            f.write("  ! DNS reachable but target ports closed.\n")
        else:
            f.write("  ✗ Suspect DNS or outbound connectivity issue.\n")

    # CSV
    import csv as _csv
    with open(csv,"w",newline="",encoding="utf-8") as f:
        w = _csv.writer(f)
        w.writerow(["metric","value"])
        w.writerow(["target", target])
        for ip, ok in dns_ok:
            w.writerow([f"dns_{ip}_53", "OK" if ok else "FAILED"])
        w.writerow(["ping_like_443", "OK" if ping_ok else "FAILED"])
        w.writerow(["resolved_ip", resolved_ip or "FAILED"])
        for p, ok in ports_results:
            w.writerow([f"port_{p}", "OPEN" if ok else "CLOSED"])

    return str(txt), str(csv)

def parse_ports(s):
    ports = []
    for part in s.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            a,b = part.split("-",1)
            a=int(a); b=int(b)
            ports.extend(list(range(min(a,b), max(a,b)+1)))
        else:
            ports.append(int(part))
    return sorted(set(ports))

def main():
    ap = argparse.ArgumentParser(description="Network Connectivity Checker")
    ap.add_argument("--target", default=DEFAULT_TARGET, help="Target host or IP (default: 8.8.8.8)")
    ap.add_argument("--ports", default=",".join(str(p) for p in DEFAULT_PORTS), help="Ports to check, e.g. '443' or '80,443' or '20-25'")
    ap.add_argument("--timeout", type=float, default=2.0, help="Per-port timeout in seconds (default: 2.0)")
    ap.add_argument("--fast", action="store_true", help="Fast mode: ports=443, timeout=1.0")
    ap.add_argument("--out", default="reports", help="Output directory for reports")
    args = ap.parse_args()

    if args.fast:
        args.ports = "443"
        args.timeout = min(args.timeout, 1.0) if args.timeout else 1.0

    ports = parse_ports(args.ports)

    # checks
    dns = check_dns()
    resolved_ip, _ = resolve_host(args.target)
    ping_ok = ping_like(args.target, timeout=args.timeout)
    ports_results = check_ports(args.target, ports, timeout=args.timeout)

    txt, csv = write_reports(args.out, args.target, dns, ping_ok, resolved_ip, ports_results)
    # stdout minimal message
    print(f"Reports exported -> {txt}, {csv}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
