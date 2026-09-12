#!/usr/bin/env python3
"""
Comprehensive Professional Monitoring System
All-in-one monitoring solution for System, Servers, Database, Logs, Files, and Network
"""

import os
import sys
import time
import json
import sqlite3
import hashlib
import subprocess
import platform
import socket
import re
from datetime import datetime
from collections import defaultdict
from pathlib import Path

try:
    import psutil
    import requests
except ImportError:
    print("Installing required packages...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "psutil", "requests"])
    import psutil
    import requests


class Colors:
    """Terminal colors"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class MonitoringSystem:
    """Professional All-in-One Monitoring System"""
    
    def __init__(self):
        self.os_type = platform.system()
        self.boot_time = datetime.fromtimestamp(psutil.boot_time())
        self.file_hashes = {}
        self.db_connection = None
        self.db_type = None
        self.history = []
        
    def clear_screen(self):
        """Clear terminal"""
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def print_header(self, title):
        """Print formatted header"""
        print(f"\n{Colors.BOLD}{Colors.HEADER}")
        print("=" * 70)
        print(f"  {title}")
        print("=" * 70)
        print(Colors.ENDC)
    
    def print_success(self, msg):
        """Print success message"""
        print(f"{Colors.OKGREEN}✓ {msg}{Colors.ENDC}")
    
    def print_error(self, msg):
        """Print error message"""
        print(f"{Colors.FAIL}✗ {msg}{Colors.ENDC}")
    
    def print_warning(self, msg):
        """Print warning message"""
        print(f"{Colors.WARNING}⚠ {msg}{Colors.ENDC}")
    
    def print_info(self, msg):
        """Print info message"""
        print(f"{Colors.OKBLUE}ℹ {msg}{Colors.ENDC}")
    
    def show_main_menu(self):
        """Display main menu"""
        self.clear_screen()
        self.print_header("PROFESSIONAL MONITORING SYSTEM")
        
        print(f"{Colors.BOLD}Select monitoring module:{Colors.ENDC}\n")
        print("  1. 🖥️  SYSTEM MONITORING (CPU, RAM, Disk, Processes)")
        print("  2. 🌐 SERVER MONITORING (HTTP, Status, Performance)")
        print("  3. 📊 DATABASE MONITORING (MySQL, PostgreSQL, SQLite)")
        print("  4. 📋 LOG MONITORING (Error tracking, Analysis)")
        print("  5. 📁 FILE MONITORING (Changes, New files, Size)")
        print("  6. 🔗 NETWORK MONITORING (Ping, Ports, Bandwidth)")
        print("  7. 📈 FULL REPORT (All modules)")
        print("  8. 💾 EXPORT REPORT (Save results)")
        print("  0. 🚪 EXIT\n")
        print("-" * 70)
        
        choice = input(f"{Colors.BOLD}Enter your choice (0-8): {Colors.ENDC}").strip()
        return choice
    
    # ============== SYSTEM MONITORING ==============
    
    def monitor_system(self):
        """System monitoring module"""
        self.print_header("SYSTEM MONITORING")
        
        try:
            while True:
                self.clear_screen()
                self.print_header("SYSTEM MONITORING")
                print(f"{Colors.BOLD}[{datetime.now().strftime('%H:%M:%S')}] System Status{Colors.ENDC}\n")
                
                # CPU Information
                print(f"{Colors.BOLD}━━━ CPU INFORMATION ━━━{Colors.ENDC}")
                cpu_percent = psutil.cpu_percent(interval=1)
                cpu_count = psutil.cpu_count()
                cpu_freq = psutil.cpu_freq()
                
                print(f"  Usage: {cpu_percent}% ", end="")
                if cpu_percent > 80:
                    print(f"{Colors.FAIL}[CRITICAL]{Colors.ENDC}")
                elif cpu_percent > 60:
                    print(f"{Colors.WARNING}[HIGH]{Colors.ENDC}")
                else:
                    print(f"{Colors.OKGREEN}[NORMAL]{Colors.ENDC}")
                
                print(f"  Cores: {cpu_count} (Physical: {psutil.cpu_count(logical=False)})")
                if cpu_freq:
                    print(f"  Frequency: {cpu_freq.current:.2f} MHz")
                print()
                
                # Memory Information
                print(f"{Colors.BOLD}━━━ MEMORY INFORMATION ━━━{Colors.ENDC}")
                mem = psutil.virtual_memory()
                swap = psutil.swap_memory()
                
                print(f"  RAM: {mem.percent}% ({mem.used // (1024**2)}MB / {mem.total // (1024**2)}MB)", end=" ")
                if mem.percent > 85:
                    print(f"{Colors.FAIL}[CRITICAL]{Colors.ENDC}")
                elif mem.percent > 70:
                    print(f"{Colors.WARNING}[HIGH]{Colors.ENDC}")
                else:
                    print(f"{Colors.OKGREEN}[OK]{Colors.ENDC}")
                
                print(f"  Swap: {swap.percent}% ({swap.used // (1024**2)}MB / {swap.total // (1024**2)}MB)")
                print(f"  Available: {mem.available // (1024**2)}MB")
                print()
                
                # Disk Information
                print(f"{Colors.BOLD}━━━ DISK INFORMATION ━━━{Colors.ENDC}")
                disk = psutil.disk_usage('/')
                print(f"  Root: {disk.percent}% ({disk.used // (1024**3)}GB / {disk.total // (1024**3)}GB)", end=" ")
                if disk.percent > 90:
                    print(f"{Colors.FAIL}[CRITICAL]{Colors.ENDC}")
                elif disk.percent > 75:
                    print(f"{Colors.WARNING}[HIGH]{Colors.ENDC}")
                else:
                    print(f"{Colors.OKGREEN}[OK]{Colors.ENDC}")
                
                io = psutil.disk_io_counters()
                print(f"  Read: {io.read_bytes // (1024**3)}GB | Write: {io.write_bytes // (1024**3)}GB")
                print()
                
                # Network I/O
                print(f"{Colors.BOLD}━━━ NETWORK I/O ━━━{Colors.ENDC}")
                net = psutil.net_io_counters()
                print(f"  Sent: {net.bytes_sent // (1024**2)}MB")
                print(f"  Received: {net.bytes_recv // (1024**2)}MB")
                print()
                
                # Top 10 Processes
                print(f"{Colors.BOLD}━━━ TOP 10 PROCESSES BY CPU ━━━{Colors.ENDC}")
                processes = []
                for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
                    try:
                        pinfo = proc.as_dict(attrs=['pid', 'name', 'cpu_percent', 'memory_info'])
                        processes.append({
                            'pid': pinfo['pid'],
                            'name': pinfo['name'][:30],
                            'cpu': pinfo['cpu_percent'] or 0,
                            'memory': pinfo['memory_info'].rss // (1024**2) if pinfo['memory_info'] else 0
                        })
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        pass
                
                for proc in sorted(processes, key=lambda x: x['cpu'], reverse=True)[:10]:
                    print(f"  {proc['pid']:8} {proc['name']:30} {proc['cpu']:6.1f}% CPU {proc['memory']:6}MB RAM")
                
                print()
                print(f"{Colors.BOLD}System Uptime: {self.get_uptime()}{Colors.ENDC}")
                print("\n" + "-" * 70)
                print("Press Ctrl+C to go back to menu...")
                time.sleep(5)
                
        except KeyboardInterrupt:
            self.print_info("Returning to menu...")
            time.sleep(1)
    
    def get_uptime(self):
        """Get system uptime"""
        uptime_seconds = (datetime.now() - self.boot_time).total_seconds()
        hours = int(uptime_seconds // 3600)
        minutes = int((uptime_seconds % 3600) // 60)
        days = hours // 24
        hours = hours % 24
        return f"{days}d {hours}h {minutes}m"
    
    # ============== SERVER MONITORING ==============
    
    def monitor_server(self):
        """Server monitoring module"""
        self.print_header("SERVER MONITORING")
        
        url = input(f"{Colors.BOLD}Enter server URL (e.g., http://localhost:8000): {Colors.ENDC}").strip()
        if not url:
            url = "http://localhost:8000"
        
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
        
        try:
            while True:
                self.clear_screen()
                self.print_header("SERVER MONITORING")
                print(f"{Colors.BOLD}[{datetime.now().strftime('%H:%M:%S')}] Monitoring: {url}{Colors.ENDC}\n")
                
                print(f"{Colors.BOLD}━━━ SERVER STATUS ━━━{Colors.ENDC}")
                
                try:
                    start_time = time.time()
                    response = requests.get(url, timeout=10, allow_redirects=True)
                    response_time = (time.time() - start_time) * 1000
                    
                    status_code = response.status_code
                    if 200 <= status_code < 300:
                        status_color = Colors.OKGREEN
                        status_text = "ONLINE"
                    elif 300 <= status_code < 400:
                        status_color = Colors.WARNING
                        status_text = "REDIRECT"
                    elif 400 <= status_code < 500:
                        status_color = Colors.WARNING
                        status_text = "CLIENT ERROR"
                    else:
                        status_color = Colors.FAIL
                        status_text = "SERVER ERROR"
                    
                    print(f"  Status: {status_color}[{status_text}]{Colors.ENDC}")
                    print(f"  Status Code: {status_code}")
                    print(f"  Response Time: {response_time:.2f}ms", end=" ")
                    
                    if response_time > 2000:
                        print(f"{Colors.FAIL}[SLOW]{Colors.ENDC}")
                    elif response_time > 1000:
                        print(f"{Colors.WARNING}[MEDIUM]{Colors.ENDC}")
                    else:
                        print(f"{Colors.OKGREEN}[FAST]{Colors.ENDC}")
                    
                    print(f"  Content Length: {len(response.content)} bytes")
                    print(f"  Content Type: {response.headers.get('content-type', 'N/A')}")
                    print(f"  Server: {response.headers.get('server', 'N/A')}")
                    
                    self.history.append({
                        'timestamp': datetime.now(),
                        'url': url,
                        'status': status_code,
                        'response_time': response_time,
                        'online': True
                    })
                    
                except requests.exceptions.Timeout:
                    self.print_error("Request timeout")
                    self.history.append({
                        'timestamp': datetime.now(),
                        'url': url,
                        'status': 'TIMEOUT',
                        'online': False
                    })
                except requests.exceptions.ConnectionError:
                    self.print_error("Connection refused")
                    self.history.append({
                        'timestamp': datetime.now(),
                        'url': url,
                        'status': 'CONNECTION_ERROR',
                        'online': False
                    })
                except Exception as e:
                    self.print_error(f"Error: {str(e)}")
                
                print("\n" + "-" * 70)
                print("Press Ctrl+C to go back to menu...")
                time.sleep(5)
                
        except KeyboardInterrupt:
            self.print_info("Returning to menu...")
            time.sleep(1)
    
    # ============== DATABASE MONITORING ==============
    
    def monitor_database(self):
        """Database monitoring module"""
        self.print_header("DATABASE MONITORING")
        
        print(f"{Colors.BOLD}Select database type:{Colors.ENDC}\n")
        print("  1. MySQL")
        print("  2. PostgreSQL")
        print("  3. SQLite\n")
        
        db_type = input(f"{Colors.BOLD}Enter choice (1-3): {Colors.ENDC}").strip()
        
        if db_type == "1":
            self._connect_mysql()
        elif db_type == "2":
            self._connect_postgres()
        elif db_type == "3":
            self._connect_sqlite()
        else:
            self.print_error("Invalid choice")
            return
        
        if not self.db_connection:
            return
        
        try:
            while True:
                self.clear_screen()
                self.print_header("DATABASE MONITORING")
                print(f"{Colors.BOLD}[{datetime.now().strftime('%H:%M:%S')}] Database: {self.db_type.upper()}{Colors.ENDC}\n")
                
                self._display_database_status()
                
                print("\n" + "-" * 70)
                print("Press Ctrl+C to go back to menu...")
                time.sleep(5)
                
        except KeyboardInterrupt:
            self.print_info("Returning to menu...")
            time.sleep(1)
    
    def _connect_mysql(self):
        """Connect to MySQL"""
        try:
            import mysql.connector
            
            host = input("Enter MySQL host (default: localhost): ").strip() or "localhost"
            user = input("Enter username (default: root): ").strip() or "root"
            password = input("Enter password: ").strip()
            database = input("Enter database name: ").strip()
            
            self.db_connection = mysql.connector.connect(
                host=host, user=user, password=password, database=database
            )
            self.db_type = "mysql"
            self.print_success("Connected to MySQL")
        except Exception as e:
            self.print_error(f"Connection failed: {e}")
    
    def _connect_postgres(self):
        """Connect to PostgreSQL"""
        try:
            import psycopg2
            
            host = input("Enter PostgreSQL host (default: localhost): ").strip() or "localhost"
            user = input("Enter username (default: postgres): ").strip() or "postgres"
            password = input("Enter password: ").strip()
            database = input("Enter database name: ").strip()
            
            self.db_connection = psycopg2.connect(
                host=host, user=user, password=password, database=database
            )
            self.db_type = "postgres"
            self.print_success("Connected to PostgreSQL")
        except Exception as e:
            self.print_error(f"Connection failed: {e}")
    
    def _connect_sqlite(self):
        """Connect to SQLite"""
        try:
            db_path = input("Enter SQLite database path: ").strip()
            self.db_connection = sqlite3.connect(db_path)
            self.db_type = "sqlite"
            self.print_success(f"Connected to SQLite: {db_path}")
        except Exception as e:
            self.print_error(f"Connection failed: {e}")
    
    def _display_database_status(self):
        """Display database status"""
        try:
            cursor = self.db_connection.cursor()
            
            if self.db_type == "sqlite":
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()
                print(f"{Colors.BOLD}━━━ DATABASE INFO ━━━{Colors.ENDC}")
                print(f"  Tables: {len(tables)}")
                if tables:
                    print(f"  Table List: {', '.join([t[0] for t in tables[:5]])}")
                    if len(tables) > 5:
                        print(f"  ... and {len(tables) - 5} more")
            
            elif self.db_type == "mysql":
                cursor.execute("SHOW STATUS;")
                status = dict(cursor.fetchall())
                cursor.execute("SELECT COUNT(*) FROM information_schema.TABLES;")
                table_count = cursor.fetchone()[0]
                
                print(f"{Colors.BOLD}━━━ DATABASE INFO ━━━{Colors.ENDC}")
                print(f"  Tables: {table_count}")
                print(f"  Active Connections: {status.get(b'Threads_connected', 0)}")
                print(f"  Total Queries: {status.get(b'Questions', 0)}")
                print(f"  Uptime: {status.get(b'Uptime', 0)} seconds")
            
            elif self.db_type == "postgres":
                cursor.execute(
                    "SELECT count(*) FROM information_schema.tables WHERE table_schema = 'public';"
                )
                table_count = cursor.fetchone()[0]
                cursor.execute("SELECT datname, numbackends FROM pg_stat_database;")
                db_info = cursor.fetchone()
                
                print(f"{Colors.BOLD}━━━ DATABASE INFO ━━━{Colors.ENDC}")
                print(f"  Tables: {table_count}")
                if db_info:
                    print(f"  Active Connections: {db_info[1]}")
        
        except Exception as e:
            self.print_error(f"Database query error: {e}")
    
    # ============== LOG MONITORING ==============
    
    def monitor_logs(self):
        """Log monitoring module"""
        self.print_header("LOG MONITORING")
        
        log_path = input(f"{Colors.BOLD}Enter log file path (e.g., /var/log/app.log): {Colors.ENDC}").strip()
        if not log_path:
            log_path = "./app.log"
        
        keywords = input(f"{Colors.BOLD}Enter keywords (comma-separated, default: ERROR,WARN): {Colors.ENDC}").strip()
        keywords = [k.strip() for k in keywords.split(",")] if keywords else ["ERROR", "WARN"]
        
        try:
            while True:
                self.clear_screen()
                self.print_header("LOG MONITORING")
                print(f"{Colors.BOLD}[{datetime.now().strftime('%H:%M:%S')}] Log: {log_path}{Colors.ENDC}\n")
                
                if not os.path.exists(log_path):
                    self.print_error(f"Log file not found: {log_path}")
                    time.sleep(2)
                    break
                
                try:
                    with open(log_path, 'r') as f:
                        lines = f.readlines()
                    
                    print(f"{Colors.BOLD}━━━ LOG ANALYSIS ━━━{Colors.ENDC}")
                    print(f"  Total Lines: {len(lines)}")
                    
                    errors = [l for l in lines if 'ERROR' in l or 'CRITICAL' in l]
                    warnings = [l for l in lines if 'WARN' in l and 'ERROR' not in l]
                    infos = [l for l in lines if 'INFO' in l]
                    
                    print(f"  Errors: {len(errors)} {Colors.FAIL if errors else Colors.OKGREEN}[{len(errors)}]{Colors.ENDC}")
                    print(f"  Warnings: {len(warnings)} {Colors.WARNING if warnings else Colors.OKGREEN}[{len(warnings)}]{Colors.ENDC}")
                    print(f"  Info: {len(infos)}")
                    
                    print(f"\n{Colors.BOLD}━━━ LAST 10 ERRORS ━━━{Colors.ENDC}")
                    for line in errors[-10:]:
                        print(f"  {Colors.FAIL}→{Colors.ENDC} {line.strip()[:70]}")
                    
                    print(f"\n{Colors.BOLD}━━━ LAST 10 WARNINGS ━━━{Colors.ENDC}")
                    for line in warnings[-10:]:
                        print(f"  {Colors.WARNING}→{Colors.ENDC} {line.strip()[:70]}")
                
                except Exception as e:
                    self.print_error(f"Error reading log: {e}")
                
                print("\n" + "-" * 70)
                print("Press Ctrl+C to go back to menu...")
                time.sleep(5)
                
        except KeyboardInterrupt:
            self.print_info("Returning to menu...")
            time.sleep(1)
    
    # ============== FILE MONITORING ==============
    
    def monitor_files(self):
        """File monitoring module"""
        self.print_header("FILE MONITORING")
        
        directory = input(f"{Colors.BOLD}Enter directory path (default: ./): {Colors.ENDC}").strip()
        if not directory:
            directory = "./"
        
        if not os.path.exists(directory):
            self.print_error(f"Directory not found: {directory}")
            return
        
        try:
            while True:
                self.clear_screen()
                self.print_header("FILE MONITORING")
                print(f"{Colors.BOLD}[{datetime.now().strftime('%H:%M:%S')}] Directory: {directory}{Colors.ENDC}\n")
                
                changes = self._scan_directory(directory)
                
                print(f"{Colors.BOLD}━━━ DIRECTORY STATUS ━━━{Colors.ENDC}")
                print(f"  Total Files: {changes['total_files']}")
                print(f"  Total Size: {changes['total_size_mb']:.2f} MB")
                print(f"  New Files: {len(changes['new_files'])} {Colors.OKGREEN if not changes['new_files'] else Colors.OKBLUE}[{len(changes['new_files'])}]{Colors.ENDC}")
                print(f"  Modified Files: {len(changes['modified_files'])} {Colors.WARNING if changes['modified_files'] else Colors.OKGREEN}[{len(changes['modified_files'])}]{Colors.ENDC}")
                print(f"  Deleted Files: {len(changes['deleted_files'])} {Colors.FAIL if changes['deleted_files'] else Colors.OKGREEN}[{len(changes['deleted_files'])}]{Colors.ENDC}")
                
                if changes['new_files']:
                    print(f"\n{Colors.BOLD}━━━ NEW FILES (Last 5) ━━━{Colors.ENDC}")
                    for f in changes['new_files'][-5:]:
                        print(f"  {Colors.OKBLUE}+{Colors.ENDC} {f}")
                
                if changes['modified_files']:
                    print(f"\n{Colors.BOLD}━━━ MODIFIED FILES (Last 5) ━━━{Colors.ENDC}")
                    for f in changes['modified_files'][-5:]:
                        print(f"  {Colors.WARNING}~{Colors.ENDC} {f}")
                
                if changes['deleted_files']:
                    print(f"\n{Colors.BOLD}━━━ DELETED FILES (Last 5) ━━━{Colors.ENDC}")
                    for f in changes['deleted_files'][-5:]:
                        print(f"  {Colors.FAIL}-{Colors.ENDC} {f}")
                
                print("\n" + "-" * 70)
                print("Press Ctrl+C to go back to menu...")
                time.sleep(5)
                
        except KeyboardInterrupt:
            self.print_info("Returning to menu...")
            time.sleep(1)
    
    def _scan_directory(self, directory):
        """Scan directory for changes"""
        changes = {
            'new_files': [],
            'modified_files': [],
            'deleted_files': [],
            'total_files': 0,
            'total_size_mb': 0
        }
        
        current_files = {}
        total_size = 0
        
        try:
            for root, dirs, files in os.walk(directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        file_hash = self._get_file_hash(file_path)
                        current_files[file_path] = file_hash
                        total_size += os.path.getsize(file_path)
                    except:
                        pass
            
            # Check for changes
            for file_path, file_hash in current_files.items():
                if file_path not in self.file_hashes:
                    changes['new_files'].append(file_path)
                elif self.file_hashes[file_path] != file_hash:
                    changes['modified_files'].append(file_path)
            
            for file_path in self.file_hashes:
                if file_path not in current_files:
                    changes['deleted_files'].append(file_path)
            
            self.file_hashes = current_files
            changes['total_files'] = len(current_files)
            changes['total_size_mb'] = total_size / (1024**2)
            
        except Exception as e:
            self.print_error(f"Error scanning directory: {e}")
        
        return changes
    
    def _get_file_hash(self, file_path):
        """Get file MD5 hash"""
        try:
            md5 = hashlib.md5()
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b''):
                    md5.update(chunk)
            return md5.hexdigest()
        except:
            return None
    
    # ============== NETWORK MONITORING ==============
    
    def monitor_network(self):
        """Network monitoring module"""
        self.print_header("NETWORK MONITORING")
        
        hosts = input(f"{Colors.BOLD}Enter hosts (comma-separated, default: 8.8.8.8,google.com): {Colors.ENDC}").strip()
        hosts = [h.strip() for h in hosts.split(",")] if hosts else ["8.8.8.8", "google.com"]
        
        try:
            while True:
                self.clear_screen()
                self.print_header("NETWORK MONITORING")
                print(f"{Colors.BOLD}[{datetime.now().strftime('%H:%M:%S')}] Network Status{Colors.ENDC}\n")
                
                print(f"{Colors.BOLD}━━━ HOST STATUS ━━━{Colors.ENDC}")
                for host in hosts:
                    result = self._ping_host(host)
                    status = f"{Colors.OKGREEN}✓ Online{Colors.ENDC}" if result['reachable'] else f"{Colors.FAIL}✗ Offline{Colors.ENDC}"
                    print(f"  {host:30} {status}", end="")
                    if result['reachable']:
                        print(f" ({result['response_time']:.2f}ms)")
                    else:
                        print()
                
                print(f"\n{Colors.BOLD}━━━ NETWORK INTERFACES ━━━{Colors.ENDC}")
                try:
                    interfaces = psutil.net_if_addrs()
                    for iface in list(interfaces.keys())[:5]:
                        addrs = interfaces[iface]
                        for addr in addrs:
                            if addr.family == 2:  # IPv4
                                print(f"  {iface:15} IP: {addr.address}")
                                break
                except:
                    pass
                
                print(f"\n{Colors.BOLD}━━━ NETWORK STATS ━━━{Colors.ENDC}")
                try:
                    net = psutil.net_io_counters()
                    print(f"  Bytes Sent: {net.bytes_sent // (1024**2)}MB")
                    print(f"  Bytes Recv: {net.bytes_recv // (1024**2)}MB")
                    print(f"  Packets Sent: {net.packets_sent}")
                    print(f"  Packets Recv: {net.packets_recv}")
                except:
                    pass
                
                print("\n" + "-" * 70)
                print("Press Ctrl+C to go back to menu...")
                time.sleep(5)
                
        except KeyboardInterrupt:
            self.print_info("Returning to menu...")
            time.sleep(1)
    
    def _ping_host(self, host):
        """Ping a host"""
        try:
            if self.os_type == 'Windows':
                cmd = ['ping', '-n', '1', '-w', '2000', host]
            else:
                cmd = ['ping', '-c', '1', '-W', '2', host]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
            
            if result.returncode == 0:
                lines = result.stdout.split('\n')
                for line in lines:
                    if 'min' in line.lower() or 'avg' in line.lower():
                        parts = line.split('/')
                        if len(parts) >= 2:
                            try:
                                avg = float(parts[-2].split('=')[-1].split()[0])
                                return {'reachable': True, 'response_time': avg}
                            except:
                                pass
                return {'reachable': True, 'response_time': 0}
            else:
                return {'reachable': False, 'response_time': 0}
        except:
            return {'reachable': False, 'response_time': 0}
    
    # ============== FULL REPORT ==============
    
    def full_report(self):
        """Generate full system report"""
        self.clear_screen()
        self.print_header("FULL SYSTEM REPORT")
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'system': self._get_system_info(),
            'cpu': self._get_cpu_info(),
            'memory': self._get_memory_info(),
            'disk': self._get_disk_info(),
            'network': self._get_network_info()
        }
        
        print(f"{Colors.BOLD}━━━ SYSTEM INFO ━━━{Colors.ENDC}")
        for key, value in report['system'].items():
            print(f"  {key}: {value}")
        
        print(f"\n{Colors.BOLD}━━━ CPU ━━━{Colors.ENDC}")
        for key, value in report['cpu'].items():
            print(f"  {key}: {value}")
        
        print(f"\n{Colors.BOLD}━━━ MEMORY ━━━{Colors.ENDC}")
        for key, value in report['memory'].items():
            print(f"  {key}: {value}")
        
        print(f"\n{Colors.BOLD}━━━ DISK ━━━{Colors.ENDC}")
        for key, value in report['disk'].items():
            print(f"  {key}: {value}")
        
        print(f"\n{Colors.BOLD}━━━ NETWORK ━━━{Colors.ENDC}")
        for key, value in report['network'].items():
            print(f"  {key}: {value}")
        
        self.history.append(report)
        
        print("\n" + "-" * 70)
        input("Press Enter to continue...")
    
    def _get_system_info(self):
        """Get system information"""
        return {
            'OS': platform.system(),
            'Version': platform.release(),
            'Hostname': platform.node(),
            'Uptime': self.get_uptime()
        }
    
    def _get_cpu_info(self):
        """Get CPU information"""
        return {
            'Usage': f"{psutil.cpu_percent()}%",
            'Cores': psutil.cpu_count(),
            'Frequency': f"{psutil.cpu_freq().current:.2f} MHz" if psutil.cpu_freq() else "N/A"
        }
    
    def _get_memory_info(self):
        """Get memory information"""
        mem = psutil.virtual_memory()
        return {
            'Usage': f"{mem.percent}%",
            'Used': f"{mem.used // (1024**2)}MB",
            'Total': f"{mem.total // (1024**2)}MB",
            'Available': f"{mem.available // (1024**2)}MB"
        }
    
    def _get_disk_info(self):
        """Get disk information"""
        disk = psutil.disk_usage('/')
        return {
            'Usage': f"{disk.percent}%",
            'Used': f"{disk.used // (1024**3)}GB",
            'Total': f"{disk.total // (1024**3)}GB",
            'Free': f"{disk.free // (1024**3)}GB"
        }
    
    def _get_network_info(self):
        """Get network information"""
        net = psutil.net_io_counters()
        return {
            'Bytes Sent': f"{net.bytes_sent // (1024**2)}MB",
            'Bytes Received': f"{net.bytes_recv // (1024**2)}MB",
            'Packets Sent': net.packets_sent,
            'Packets Received': net.packets_recv
        }
    
    # ============== EXPORT ==============
    
    def export_report(self):
        """Export monitoring report"""
        self.print_header("EXPORT REPORT")
        
        if not self.history:
            self.print_warning("No data to export")
            time.sleep(2)
            return
        
        filename = input(f"{Colors.BOLD}Enter filename (default: report.json): {Colors.ENDC}").strip()
        if not filename:
            filename = "report.json"
        
        try:
            with open(filename, 'w') as f:
                json.dump(self.history, f, indent=2, default=str)
            self.print_success(f"Report exported to {filename}")
            time.sleep(2)
        except Exception as e:
            self.print_error(f"Export failed: {e}")
            time.sleep(2)
    
    # ============== MAIN LOOP ==============
    
    def run(self):
        """Main application loop"""
        while True:
            choice = self.show_main_menu()
            
            if choice == "1":
                self.monitor_system()
            elif choice == "2":
                self.monitor_server()
            elif choice == "3":
                self.monitor_database()
            elif choice == "4":
                self.monitor_logs()
            elif choice == "5":
                self.monitor_files()
            elif choice == "6":
                self.monitor_network()
            elif choice == "7":
                self.full_report()
            elif choice == "8":
                self.export_report()
            elif choice == "0":
                self.clear_screen()
                print(f"\n{Colors.OKGREEN}Thank you for using Professional Monitoring System!{Colors.ENDC}\n")
                sys.exit(0)
            else:
                self.print_error("Invalid choice. Please try again.")
                time.sleep(1)


def main():
    """Application entry point"""
    try:
        monitor = MonitoringSystem()
        monitor.run()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.WARNING}Application interrupted by user{Colors.ENDC}\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.FAIL}Fatal error: {e}{Colors.ENDC}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
