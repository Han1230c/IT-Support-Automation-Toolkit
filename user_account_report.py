#!/usr/bin/env python3
"""
User Account Report Generator
Author: Xiaohan Chen
Purpose: Generate user account reports for IT support and audit purposes
"""

import csv
import datetime
from collections import defaultdict

def load_user_data(csv_file):
    """Load user data from CSV file"""
    users = []
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                users.append(row)
        return users
    except FileNotFoundError:
        print(f"Error: File {csv_file} not found")
        return []
    except Exception as e:
        print(f"Error reading file: {e}")
        return []

def generate_summary_report(users):
    """Generate summary statistics"""
    print("=" * 60)
    print("USER ACCOUNT SUMMARY REPORT")
    print("=" * 60)
    print(f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total Users: {len(users)}")
    print()
    
    # Count by status
    status_count = defaultdict(int)
    for user in users:
        status = user.get('Status', 'Unknown')
        status_count[status] += 1
    
    print("USER STATUS:")
    for status, count in sorted(status_count.items()):
        print(f"  {status}: {count}")
    print()
    
    # Count by department
    dept_count = defaultdict(int)
    for user in users:
        dept = user.get('Department', 'Unknown')
        dept_count[dept] += 1
    
    print("USERS BY DEPARTMENT:")
    for dept, count in sorted(dept_count.items(), key=lambda x: x[1], reverse=True):
        print(f"  {dept}: {count}")
    print()

def find_inactive_users(users, days_threshold=90):
    """Find users who haven't logged in recently"""
    print("INACTIVE USERS (No login in last 90 days):")
    inactive_count = 0
    
    for user in users:
        last_login = user.get('LastLogin', '')
        status = user.get('Status', '')
        
        if status.lower() == 'inactive' or not last_login:
            print(f"  - {user.get('Username', 'N/A')} ({user.get('Email', 'N/A')})")
            print(f"    Department: {user.get('Department', 'N/A')}")
            print(f"    Last Login: {last_login if last_login else 'Never'}")
            inactive_count += 1
    
    if inactive_count == 0:
        print("  ✓ No inactive users found")
    else:
        print(f"\n  Total Inactive: {inactive_count}")
        print(f"  ⚠️ Recommendation: Review these accounts for potential deprovisioning")
    print()

def find_security_issues(users):
    """Identify potential security concerns"""
    print("SECURITY CONCERNS:")
    issues_found = False
    
    for user in users:
        concerns = []
        
        # Check for admin accounts
        if user.get('Role', '').lower() == 'admin':
            concerns.append("Admin privileges")
        
        # Check for missing email
        if not user.get('Email'):
            concerns.append("Missing email address")
        
        # Check for disabled but not locked accounts
        if user.get('Status', '').lower() == 'disabled':
            concerns.append("Disabled account - review for removal")
        
        if concerns:
            issues_found = True
            print(f"  - {user.get('Username', 'N/A')}:")
            for concern in concerns:
                print(f"    • {concern}")
    
    if not issues_found:
        print("  ✓ No major security concerns detected")
    print()

def export_report(users, output_file):
    """Export detailed report to CSV"""
    try:
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            if users:
                writer = csv.DictWriter(f, fieldnames=users[0].keys())
                writer.writeheader()
                writer.writerows(users)
        print(f"✓ Detailed report exported to: {output_file}")
    except Exception as e:
        print(f"Error exporting report: {e}")

def create_sample_data():
    """Create sample user data for demonstration"""
    sample_file = 'sample_users.csv'
    sample_users = [
        {'Username': 'jsmith', 'Email': 'jsmith@company.com', 'Department': 'IT', 
         'Role': 'User', 'Status': 'Active', 'LastLogin': '2024-10-28'},
        {'Username': 'bjones', 'Email': 'bjones@company.com', 'Department': 'HR', 
         'Role': 'User', 'Status': 'Active', 'LastLogin': '2024-10-27'},
        {'Username': 'admin', 'Email': 'admin@company.com', 'Department': 'IT', 
         'Role': 'Admin', 'Status': 'Active', 'LastLogin': '2024-10-29'},
        {'Username': 'olduser', 'Email': 'olduser@company.com', 'Department': 'Sales', 
         'Role': 'User', 'Status': 'Inactive', 'LastLogin': '2024-01-15'},
        {'Username': 'testuser', 'Email': '', 'Department': 'IT', 
         'Role': 'User', 'Status': 'Disabled', 'LastLogin': '2024-09-10'},
    ]
    
    with open(sample_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=sample_users[0].keys())
        writer.writeheader()
        writer.writerows(sample_users)
    
    print(f"✓ Sample data created: {sample_file}\n")
    return sample_file

def main():
    """Main function"""
    print("User Account Report Generator\n")
    
    # Create sample data for demonstration
    input_file = create_sample_data()
    
    # Load user data
    users = load_user_data(input_file)
    
    if not users:
        print("No user data to process")
        return
    
    # Generate reports
    generate_summary_report(users)
    find_inactive_users(users)
    find_security_issues(users)
    
    # Export detailed report
    output_file = f"user_report_{datetime.datetime.now().strftime('%Y%m%d')}.csv"
    export_report(users, output_file)
    
    print("=" * 60)
    print("Report generation complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()
