#!/usr/bin/env python3
"""
Comprehensive Python Monitoring System
Supports: System, Servers, Database, Logs, Files, and Network monitoring
"""

import os
import sys
import time
import subprocess
from datetime import datetime

# Import monitoring modules
from monitors.system_monitor import SystemMonitor
from monitors.server_monitor import ServerMonitor
from monitors.database_monitor import DatabaseMonitor
from monitors.log_monitor import LogMonitor
from monitors.file_monitor import FileMonitor
from monitors.network_monitor import NetworkMonitor


class MonitoringSystem:
    def __init__(self):
        self.system_monitor = SystemMonitor()
        self.server_monitor = ServerMonitor()
        self.database_monitor = DatabaseMonitor()
        self.log_monitor = LogMonitor()
        self.file_monitor = FileMonitor()
        self.network_monitor = NetworkMonitor()
        
    def clear_screen(self):
        """Clear terminal screen"""
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def print_header(self):
        """Print main menu header"""
        self.clear_screen()
        print("\n" + "="*60)
        print("     COMPREHENSIVE PYTHON MONITORING SYSTEM")
        print("="*60 + "\n")
    
    def print_menu(self):
        """Display main menu"""
        self.print_header()
        print("Select monitoring module:")
        print("  1. System Monitoring (CPU, RAM, Disk, Processes)")
        print("  2. Server Monitoring (HTTP, Status, Performance)")
        print("  3. Database Monitoring (Connections, Queries, Health)")
        print("  4. Log Monitoring (Error tracking, Alerts)")
        print("  5. File Monitoring (Changes, New files, Permissions)")
        print("  6. Network Monitoring (Ping, Latency, Connectivity)")
        print("  7. All Monitoring (Run all modules)")
        print("  0. Exit")
        print("\n" + "-"*60)
    
    def run_system_monitoring(self):
        """Run system monitoring"""
        self.clear_screen()
        print("\n=== SYSTEM MONITORING ===\n")
        
        try:
            while True:
                print(f"\n[{datetime.now().strftime('%H:%M:%S')}] System Status:")
                print("-" * 50)
                
                # CPU
                cpu_percent = self.system_monitor.get_cpu_usage()
                print(f"CPU Usage: {cpu_percent}%")
                
                # Memory
                memory = self.system_monitor.get_memory_info()
                print(f"Memory: {memory['percent']}% ({memory['used']}MB / {memory['total']}MB)")
                
                # Disk
                disk = self.system_monitor.get_disk_info()
                print(f"Disk: {disk['percent']}% ({disk['used']}GB / {disk['total']}GB)")
                
                # Top processes
                print("\nTop 5 Processes by CPU:")
                processes = self.system_monitor.get_top_processes()
                for proc in processes[:5]:
                    print(f"  {proc['name']}: {proc['cpu']}% CPU, {proc['memory']}MB RAM")
                
                print("\nPress Ctrl+C to go back to menu...")
                time.sleep(5)
                
        except KeyboardInterrupt:
            print("\n\nReturning to menu...")
            time.sleep(1)
    
    def run_server_monitoring(self):
        """Run server monitoring"""
        self.clear_screen()
        print("\n=== SERVER MONITORING ===\n")
        
        url = input("Enter server URL (e.g., http://localhost:8000): ").strip()
        if not url:
            url = "http://localhost:8000"
        
        try:
            while True:
                print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Server Status:")
                print("-" * 50)
                
                status = self.server_monitor.check_server_health(url)
                print(f"URL: {url}")
                print(f"Status: {'✓ Online' if status['online'] else '✗ Offline'}")
                print(f"Response Code: {status.get('status_code', 'N/A')}")
                print(f"Response Time: {status.get('response_time', 0):.2f}ms")
                
                if status['online']:
                    print(f"Content Length: {status.get('content_length', 0)} bytes")
                
                print("\nPress Ctrl+C to go back to menu...")
                time.sleep(5)
                
        except KeyboardInterrupt:
            print("\n\nReturning to menu...")
            time.sleep(1)
    
    def run_database_monitoring(self):
        """Run database monitoring"""
        self.clear_screen()
        print("\n=== DATABASE MONITORING ===\n")
        
        print("Database Type:")
        print("  1. MySQL")
        print("  2. PostgreSQL")
        print("  3. SQLite")
        
        db_type = input("\nSelect database type (1-3): ").strip()
        
        if db_type == "1":
            host = input("Enter MySQL host (default: localhost): ").strip() or "localhost"
            user = input("Enter username (default: root): ").strip() or "root"
            password = input("Enter password: ").strip()
            database = input("Enter database name: ").strip()
            
            self.database_monitor.connect_mysql(host, user, password, database)
            
        elif db_type == "2":
            host = input("Enter PostgreSQL host (default: localhost): ").strip() or "localhost"
            user = input("Enter username (default: postgres): ").strip() or "postgres"
            password = input("Enter password: ").strip()
            database = input("Enter database name: ").strip()
            
            self.database_monitor.connect_postgres(host, user, password, database)
            
        elif db_type == "3":
            db_path = input("Enter SQLite database path: ").strip()
            self.database_monitor.connect_sqlite(db_path)
        
        try:
            while True:
                print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Database Status:")
                print("-" * 50)
                
                status = self.database_monitor.get_database_status()
                if status:
                    for key, value in status.items():
                        print(f"{key}: {value}")
                else:
                    print("Failed to connect to database")
                    break
                
                print("\nPress Ctrl+C to go back to menu...")
                time.sleep(5)
                
        except KeyboardInterrupt:
            print("\n\nReturning to menu...")
            time.sleep(1)
    
    def run_log_monitoring(self):
        """Run log monitoring"""
        self.clear_screen()
        print("\n=== LOG MONITORING ===\n")
        
        log_path = input("Enter log file path (e.g., /var/log/app.log): ").strip()
        if not log_path:
            log_path = "./app.log"
        
        keywords = input("Enter keywords to monitor (comma-separated, e.g., ERROR,WARN): ").strip()
        keywords = [k.strip() for k in keywords.split(",")] if keywords else ["ERROR", "WARN"]
        
        try:
            while True:
                print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Log Analysis:")
                print("-" * 50)
                
                analysis = self.log_monitor.analyze_log(log_path, keywords)
                
                if analysis:
                    for key, value in analysis.items():
                        if isinstance(value, list):
                            print(f"\n{key}:")
                            for item in value[-5:]:  # Show last 5
                                print(f"  - {item}")
                        else:
                            print(f"{key}: {value}")
                else:
                    print("Failed to read log file")
                    break
                
                print("\nPress Ctrl+C to go back to menu...")
                time.sleep(5)
                
        except KeyboardInterrupt:
            print("\n\nReturning to menu...")
            time.sleep(1)
    
    def run_file_monitoring(self):
        """Run file monitoring"""
        self.clear_screen()
        print("\n=== FILE MONITORING ===\n")
        
        directory = input("Enter directory path to monitor (e.g., ./): ").strip()
        if not directory:
            directory = "./"
        
        try:
            while True:
                print(f"\n[{datetime.now().strftime('%H:%M:%S')}] File System Changes:")
                print("-" * 50)
                
                changes = self.file_monitor.monitor_directory(directory)
                
                if changes:
                    for change_type, files in changes.items():
                        print(f"\n{change_type}:")
                        for file in files[-10:]:  # Show last 10
                            print(f"  - {file}")
                else:
                    print("No changes detected")
                
                print("\nPress Ctrl+C to go back to menu...")
                time.sleep(5)
                
        except KeyboardInterrupt:
            print("\n\nReturning to menu...")
            time.sleep(1)
    
    def run_network_monitoring(self):
        """Run network monitoring"""
        self.clear_screen()
        print("\n=== NETWORK MONITORING ===\n")
        
        hosts = input("Enter hosts to ping (comma-separated, e.g., 8.8.8.8,google.com): ").strip()
        hosts = [h.strip() for h in hosts.split(",")] if hosts else ["8.8.8.8", "google.com"]
        
        try:
            while True:
                print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Network Status:")
                print("-" * 50)
                
                for host in hosts:
                    ping_result = self.network_monitor.ping_host(host)
                    print(f"\n{host}:")
                    print(f"  Status: {'✓ Reachable' if ping_result['reachable'] else '✗ Unreachable'}")
                    if ping_result['reachable']:
                        print(f"  Response Time: {ping_result['response_time']:.2f}ms")
                
                # Network interfaces
                print("\n\nNetwork Interfaces:")
                interfaces = self.network_monitor.get_network_interfaces()
                for iface, info in list(interfaces.items())[:5]:
                    print(f"\n  {iface}:")
                    print(f"    IP: {info.get('ip', 'N/A')}")
                    print(f"    Sent: {info.get('bytes_sent', 0)} bytes")
                    print(f"    Recv: {info.get('bytes_recv', 0)} bytes")
                
                print("\nPress Ctrl+C to go back to menu...")
                time.sleep(5)
                
        except KeyboardInterrupt:
            print("\n\nReturning to menu...")
            time.sleep(1)
    
    def run_all_monitoring(self):
        """Run all monitoring modules"""
        self.clear_screen()
        print("\n=== RUNNING ALL MONITORS ===\n")
        
        try:
            while True:
                self.clear_screen()
                print(f"\n[{datetime.now().strftime('%H:%M:%S')}] FULL SYSTEM REPORT\n")
                print("="*60)
                
                # System
                print("\n[SYSTEM MONITORING]")
                print("-" * 60)
                cpu = self.system_monitor.get_cpu_usage()
                memory = self.system_monitor.get_memory_info()
                disk = self.system_monitor.get_disk_info()
                print(f"CPU: {cpu}% | Memory: {memory['percent']}% | Disk: {disk['percent']}%")
                
                # Network
                print("\n[NETWORK MONITORING]")
                print("-" * 60)
                ping = self.network_monitor.ping_host("8.8.8.8")
                print(f"Internet: {'✓ Connected' if ping['reachable'] else '✗ Disconnected'}")
                if ping['reachable']:
                    print(f"Latency: {ping['response_time']:.2f}ms")
                
                # File
                print("\n[FILE MONITORING]")
                print("-" * 60)
                changes = self.file_monitor.monitor_directory("./")
                total_changes = sum(len(v) for v in changes.values())
                print(f"Changes detected: {total_changes}")
                
                print("\n" + "="*60)
                print("Press Ctrl+C to go back to menu...")
                time.sleep(5)
                
        except KeyboardInterrupt:
            print("\n\nReturning to menu...")
            time.sleep(1)
    
    def run(self):
        """Main application loop"""
        while True:
            self.print_menu()
            choice = input("Enter your choice (0-7): ").strip()
            
            if choice == "1":
                self.run_system_monitoring()
            elif choice == "2":
                self.run_server_monitoring()
            elif choice == "3":
                self.run_database_monitoring()
            elif choice == "4":
                self.run_log_monitoring()
            elif choice == "5":
                self.run_file_monitoring()
            elif choice == "6":
                self.run_network_monitoring()
            elif choice == "7":
                self.run_all_monitoring()
            elif choice == "0":
                self.clear_screen()
                print("Thank you for using Monitoring System. Goodbye!\n")
                sys.exit(0)
            else:
                print("Invalid choice. Please try again.")
                time.sleep(1)


if __name__ == "__main__":
    try:
        monitor = MonitoringSystem()
        monitor.run()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
