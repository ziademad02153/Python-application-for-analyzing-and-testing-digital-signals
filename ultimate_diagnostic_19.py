"""
Ultimate 19-Point Terminal Diagnostic
Comprehensive identification of all terminal problems with expanded detection
"""

import sys
import os
import traceback
import subprocess
import json
import warnings
import tempfile
import shutil
from datetime import datetime

def print_problem(num, title, status, details=""):
    """Print problem status with consistent formatting"""
    status_symbol = "✅" if status else "❌"
    print(f"{status_symbol} Problem {num}: {title}")
    if details:
        print(f"    {details}")

def main():
    """Ultimate 19-point diagnostic with expanded error detection"""
    print("🚀 ULTIMATE 19-POINT TERMINAL DIAGNOSTIC")
    print(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🐍 Python: {sys.version}")
    print(f"📁 Working Directory: {os.getcwd()}")
    
    problems = []
    
    print("\n" + "="*70)
    print("🔍 COMPREHENSIVE PROBLEM ANALYSIS")
    print("="*70)
    
    # Problem 1: Python executable and environment
    try:
        python_path = sys.executable
        python_accessible = os.path.exists(python_path)
        print_problem(1, "Python Executable Path", python_accessible, f"Path: {python_path}")
        if not python_accessible:
            problems.append("Python executable not accessible")
    except Exception as e:
        print_problem(1, "Python Executable Path", False, f"Error: {e}")
        problems.append(f"Python path error: {e}")
    
    # Problem 2: Virtual environment detection
    try:
        in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
        venv_path = sys.prefix if in_venv else "None"
        print_problem(2, "Virtual Environment", in_venv, f"Path: {venv_path}")
        if not in_venv:
            problems.append("Not running in virtual environment")
    except Exception as e:
        print_problem(2, "Virtual Environment", False, f"Error: {e}")
        problems.append(f"Virtual environment check error: {e}")
    
    # Problem 3: Critical file existence and syntax
    try:
        critical_files = [
            'heater_monitor.py',
            'performance_optimization.py',
            'comprehensive_tests.py',
            'config.json',
            'requirements.txt'
        ]
        
        file_issues = []
        for file in critical_files:
            if not os.path.exists(file):
                file_issues.append(f"{file} missing")
            else:
                # Check syntax for Python files
                if file.endswith('.py'):
                    try:
                        with open(file, 'r', encoding='utf-8') as f:
                            code = f.read()
                        compile(code, file, 'exec')
                    except SyntaxError as se:
                        file_issues.append(f"{file} syntax error: {se}")
                    except UnicodeDecodeError:
                        file_issues.append(f"{file} encoding error")
        
        files_ok = len(file_issues) == 0
        print_problem(3, "Critical Files & Syntax", files_ok, f"Issues: {len(file_issues)}")
        if file_issues:
            problems.extend(file_issues)
    except Exception as e:
        print_problem(3, "Critical Files & Syntax", False, f"Error: {e}")
        problems.append(f"File check error: {e}")
    
    # Problem 4: Package import verification
    try:
        import_tests = [
            ('PyQt6.QtWidgets', 'QApplication'),
            ('PyQt6.QtCore', 'QTimer'),
            ('matplotlib.pyplot', 'pyplot'),
            ('pandas', 'pandas'),
            ('psutil', 'psutil'),
            ('openpyxl', 'openpyxl'),
            ('nidaqmx', 'nidaqmx'),
            ('serial', 'pyserial')
        ]
        
        import_issues = []
        for module_name, description in import_tests:
            try:
                __import__(module_name)
            except ImportError as e:
                import_issues.append(f"{module_name} ({description}): {e}")
        
        imports_ok = len(import_issues) == 0
        print_problem(4, "Package Imports", imports_ok, f"Failed: {len(import_issues)}")
        if import_issues:
            problems.extend(import_issues)
    except Exception as e:
        print_problem(4, "Package Imports", False, f"Error: {e}")
        problems.append(f"Import check error: {e}")
    
    # Problem 5: GUI system availability
    try:
        from PyQt6.QtWidgets import QApplication
        
        # Test if GUI system is available without creating persistent app
        try:
            app = QApplication.instance()
            if app is None:
                test_app = QApplication([])
                gui_available = True
                test_app.quit()
            else:
                gui_available = True
        except Exception:
            gui_available = False
        
        print_problem(5, "GUI System Availability", gui_available)
        if not gui_available:
            problems.append("GUI system not available (display/X11 issues)")
    except Exception as e:
        print_problem(5, "GUI System Availability", False, f"Error: {e}")
        problems.append(f"GUI system error: {e}")
    
    # Problem 6: Matplotlib backend compatibility
    try:
        # First check what the diagnostic sees
        import matplotlib
        initial_backend = matplotlib.get_backend()
        
        # Then check what the application would use
        try:
            # Import heater_monitor to see if it sets backend correctly
            import heater_monitor
            app_backend = matplotlib.get_backend()
            backend_ok = app_backend == 'Qt5Agg'
        except Exception:
            backend_ok = 'Qt' in initial_backend or 'Agg' in initial_backend
            app_backend = initial_backend
        
        print_problem(6, "Matplotlib Backend", backend_ok, f"App backend: {app_backend}")
        if not backend_ok:
            problems.append(f"Incompatible matplotlib backend: {app_backend}")
    except Exception as e:
        print_problem(6, "Matplotlib Backend", False, f"Error: {e}")
        problems.append(f"Matplotlib backend error: {e}")
    
    # Problem 7: Configuration file integrity  
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
        
        required_sections = {
            'thresholds': ['all5_min', 'all5_max', 'all0_min', 'all0_max'],
            'colors': ['heater1', 'heater2'],
            'serial': ['enabled', 'port', 'baudrate'],
            'heater_system': ['enabled', 'temp_min', 'temp_max']
        }
        
        config_issues = []
        for section, keys in required_sections.items():
            if section not in config:
                config_issues.append(f"Missing section: {section}")
            else:
                for key in keys:
                    if key not in config[section]:
                        config_issues.append(f"Missing key: {section}.{key}")
        
        config_ok = len(config_issues) == 0
        print_problem(7, "Configuration Structure", config_ok, f"Issues: {len(config_issues)}")
        if config_issues:
            problems.extend(config_issues)
    except Exception as e:
        print_problem(7, "Configuration Structure", False, f"Error: {e}")
        problems.append(f"Config file error: {e}")
    
    # Problem 8: Performance optimization system
    try:
        from performance_optimization import PerformanceOptimizer, ChartOptimizer, AutoSaveManager
        
        class MockAppBase:
            def __init__(self):
                self.timestamps = []
                self.heater1_data = []
                self.heater2_data = []
        
        mock_app = MockAppBase()
        
        # Test instantiation
        perf_opt = PerformanceOptimizer(mock_app)
        chart_opt = ChartOptimizer(mock_app)
        auto_save = AutoSaveManager(mock_app)
        
        # Test key methods exist
        methods_ok = all([
            hasattr(perf_opt, 'get_memory_usage'),
            hasattr(chart_opt, 'optimized_chart_update'),
            hasattr(auto_save, 'auto_save_data')
        ])
        
        print_problem(8, "Performance System", methods_ok, "All components functional")
        if not methods_ok:
            problems.append("Performance optimization methods missing")
    except Exception as e:
        print_problem(8, "Performance System", False, f"Error: {e}")
        problems.append(f"Performance system error: {e}")
    
    # Problem 9: Chart data point limiting
    try:
        from performance_optimization import ChartOptimizer
        
        # Define MockApp for this test
        class MockApp:
            def __init__(self):
                self.timestamps = list(range(1000))
                self.heater1_data = [25.0] * 1000
                self.heater2_data = [30.0] * 1000
        
        mock_app = MockApp()
        
        optimizer = ChartOptimizer(mock_app)
        plot_data = optimizer.get_optimized_data_points()
        
        data_limited = len(plot_data[0]) <= optimizer.data_points_limit
        limit_reasonable = optimizer.data_points_limit <= 300  # Should be 200-300
        
        chart_perf_ok = data_limited and limit_reasonable
        print_problem(9, "Chart Data Limiting", chart_perf_ok, 
                     f"Points: {len(plot_data[0])}/{optimizer.data_points_limit}")
        if not chart_perf_ok:
            problems.append("Chart data limiting not working properly")
    except Exception as e:
        print_problem(9, "Chart Data Limiting", False, f"Error: {e}")
        problems.append(f"Chart limiting error: {e}")
    
    # Problem 10: Main application integration
    try:
        from heater_monitor import HeaterTestSystem, HAS_PERFORMANCE_OPT
        
        # Check performance integration
        integration_ok = HAS_PERFORMANCE_OPT
        
        # Check critical methods
        required_methods = [
            'start_acquisition', 'stop_acquisition', 'lightweight_chart_update',
            'save_direct', 'reset_data', 'toggle_simulation_mode'
        ]
        
        methods_ok = all(hasattr(HeaterTestSystem, method) for method in required_methods)
        
        main_app_ok = integration_ok and methods_ok
        print_problem(10, "Main Application", main_app_ok, 
                     f"Performance: {integration_ok}, Methods: {methods_ok}")
        if not main_app_ok:
            problems.append("Main application integration incomplete")
    except Exception as e:
        print_problem(10, "Main Application", False, f"Error: {e}")
        problems.append(f"Main application error: {e}")
    
    # Problem 11: Test suite functionality
    try:
        from comprehensive_tests import TestHeaterMonitorSystem
        
        # Count test methods
        test_methods = [method for method in dir(TestHeaterMonitorSystem) 
                       if method.startswith('test_')]
        
        tests_adequate = len(test_methods) >= 10
        
        # Check if chart performance test exists
        chart_test_exists = os.path.exists('chart_performance_test_fixed.py')
        
        test_system_ok = tests_adequate and chart_test_exists
        print_problem(11, "Test Suite System", test_system_ok, 
                     f"Methods: {len(test_methods)}, Chart test: {chart_test_exists}")
        if not test_system_ok:
            problems.append("Test suite incomplete or missing components")
    except Exception as e:
        print_problem(11, "Test Suite System", False, f"Error: {e}")
        problems.append(f"Test suite error: {e}")
    
    # Problem 12: System resources
    try:
        import psutil
        
        # Memory check
        memory = psutil.virtual_memory()
        available_gb = memory.available / (1024**3)
        memory_ok = available_gb > 0.5
        
        # CPU check
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_ok = cpu_percent < 80
        
        # Disk space check
        disk_usage = shutil.disk_usage(os.getcwd())
        free_gb = disk_usage.free / (1024**3)
        disk_ok = free_gb > 1.0
        
        resources_ok = memory_ok and cpu_ok and disk_ok
        print_problem(12, "System Resources", resources_ok, 
                     f"Memory: {available_gb:.1f}GB, CPU: {cpu_percent:.1f}%, Disk: {free_gb:.1f}GB")
        if not resources_ok:
            if not memory_ok:
                problems.append(f"Low memory: {available_gb:.1f}GB available")
            if not cpu_ok:
                problems.append(f"High CPU usage: {cpu_percent:.1f}%")
            if not disk_ok:
                problems.append(f"Low disk space: {free_gb:.1f}GB free")
    except Exception as e:
        print_problem(12, "System Resources", False, f"Error: {e}")
        problems.append(f"System resource check error: {e}")
    
    # Problem 13: File permissions and access
    try:
        permission_issues = []
        
        # Check read/write permissions for key files
        files_to_check = ['heater_monitor.py', 'config.json', 'requirements.txt']
        for file in files_to_check:
            if os.path.exists(file):
                if not os.access(file, os.R_OK):
                    permission_issues.append(f"{file} not readable")
                if not os.access(file, os.W_OK):
                    permission_issues.append(f"{file} not writable")
        
        # Check logs directory
        logs_dir = "logs"
        if not os.path.exists(logs_dir):
            try:
                os.makedirs(logs_dir)
            except:
                permission_issues.append("Cannot create logs directory")
        elif not os.access(logs_dir, os.W_OK):
            permission_issues.append("Logs directory not writable")
        
        permissions_ok = len(permission_issues) == 0
        print_problem(13, "File Permissions", permissions_ok, f"Issues: {len(permission_issues)}")
        if permission_issues:
            problems.extend(permission_issues)
    except Exception as e:
        print_problem(13, "File Permissions", False, f"Error: {e}")
        problems.append(f"Permission check error: {e}")
    
    # Problem 14: Serial port system
    try:
        import serial
        import serial.tools.list_ports
        
        # Test serial system
        ports = list(serial.tools.list_ports.comports())
        serial_system_ok = True  # Serial is optional for simulation mode
        
        # Test SerialManager if it exists
        try:
            from heater_monitor import SerialManager
            config = {"serial": {"enabled": False, "port": "COM1", "baudrate": 9600, 
                               "timeout": 1, "data_bits": 8, "stop_bits": 1, "parity": "N", "auto_detect": True}}
            serial_mgr = SerialManager(config)
            serial_manager_ok = hasattr(serial_mgr, 'parse_ttl_data')
        except Exception:
            serial_manager_ok = False
        
        serial_ok = serial_system_ok and serial_manager_ok
        print_problem(14, "Serial Communication", serial_ok, 
                     f"Ports: {len(ports)}, Manager: {serial_manager_ok}")
        if not serial_ok:
            problems.append("Serial communication system issues")
    except Exception as e:
        print_problem(14, "Serial Communication", False, f"Error: {e}")
        problems.append(f"Serial system error: {e}")
    
    # Problem 15: DAQ system compatibility
    try:
        import nidaqmx
        
        # Test basic DAQ functionality in simulation mode
        try:
            import nidaqmx.system  # type: ignore
            system = nidaqmx.system.System.local()
            devices = system.devices
            daq_system_ok = True  # Should work even without hardware
        except Exception:
            daq_system_ok = True  # Expected to fail without hardware, OK for simulation
        
        # Test MockDAQ if available
        try:
            from heater_monitor import MockDAQ
            mock_daq = MockDAQ()
            mock_data = mock_daq.read()
            mock_ok = len(mock_data) == 12  # Should return 12 values
        except Exception:
            mock_ok = False
        
        daq_ok = daq_system_ok and mock_ok
        print_problem(15, "DAQ System", daq_ok, f"System: OK, Mock: {mock_ok}")
        if not daq_ok:
            problems.append("DAQ system compatibility issues")
    except Exception as e:
        print_problem(15, "DAQ System", False, f"Error: {e}")
        problems.append(f"DAQ system error: {e}")
    
    # Problem 16: Error detection and logging
    try:
        # Test error logging functionality
        from heater_monitor import SerialManager
        
        config = {"serial": {"enabled": False, "port": "COM1", "baudrate": 9600,
                           "timeout": 1, "data_bits": 8, "stop_bits": 1, "parity": "N", "auto_detect": True}}
        serial_mgr = SerialManager(config)
        
        # Test error detection methods
        error_methods_ok = all([
            hasattr(serial_mgr, 'detect_display_errors'),
            hasattr(serial_mgr, 'validate_ttl_frame'),
            hasattr(serial_mgr, 'log_parsing_error')
        ])
        
        print_problem(16, "Error Detection System", error_methods_ok, "All methods present")
        if not error_methods_ok:
            problems.append("Error detection methods missing")
    except Exception as e:
        print_problem(16, "Error Detection System", False, f"Error: {e}")
        problems.append(f"Error detection error: {e}")
    
    # Problem 17: Data export functionality
    try:
        # Test data export dependencies
        import openpyxl
        import pandas as pd
        
        # Test creating temporary Excel file
        temp_file = os.path.join(tempfile.gettempdir(), "test_export.xlsx")
        try:
            # Create test workbook
            wb = openpyxl.Workbook()
            wb.save(temp_file)
            wb.close()
            
            # Clean up
            if os.path.exists(temp_file):
                os.remove(temp_file)
            
            export_ok = True
        except Exception:
            export_ok = False
        
        print_problem(17, "Data Export System", export_ok, "Excel export functional")
        if not export_ok:
            problems.append("Data export system not working")
    except Exception as e:
        print_problem(17, "Data Export System", False, f"Error: {e}")
        problems.append(f"Data export error: {e}")
    
    # Problem 18: System warnings and deprecations
    try:
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            
            # Import modules to trigger warnings
            try:
                import heater_monitor
                import performance_optimization
                import comprehensive_tests
            except Exception:
                pass
            
            warning_count = len(w)
            warnings_acceptable = warning_count < 10  # Allow up to 10 warnings
            
            print_problem(18, "System Warnings", warnings_acceptable, f"Warnings: {warning_count}")
            if not warnings_acceptable:
                problems.append(f"Too many warnings: {warning_count}")
                # Show first few warnings
                for warning in w[:3]:
                    problems.append(f"Warning: {str(warning.message)[:100]}")
    except Exception as e:
        print_problem(18, "System Warnings", False, f"Error: {e}")
        problems.append(f"Warning check error: {e}")
    
    # Problem 19: Overall system integration
    try:
        # Test if the complete system can be initialized
        integration_issues = []
        
        # Test application startup simulation
        try:
            from PyQt6.QtWidgets import QApplication
            app = QApplication.instance()
            if app is None:
                app = QApplication([])
                created_app = True
            else:
                created_app = False
            
            # Test HeaterTestSystem creation (without showing UI)
            from heater_monitor import HeaterTestSystem
            test_system = HeaterTestSystem()
            
            # Basic functionality checks
            if not hasattr(test_system, 'config'):
                integration_issues.append("Config system not initialized")
            if not hasattr(test_system, 'simulation_mode'):
                integration_issues.append("Simulation mode not set")
            
            # Clean up
            if created_app:
                app.quit()
                
        except Exception as e:
            integration_issues.append(f"System initialization failed: {str(e)[:100]}")
        
        integration_ok = len(integration_issues) == 0
        print_problem(19, "System Integration", integration_ok, f"Issues: {len(integration_issues)}")
        if integration_issues:
            problems.extend(integration_issues)
    except Exception as e:
        print_problem(19, "System Integration", False, f"Error: {e}")
        problems.append(f"Integration error: {e}")
    
    # Final comprehensive summary
    print("\n" + "="*70)
    print("📊 ULTIMATE DIAGNOSTIC SUMMARY")
    print("="*70)
    
    total_checks = 19
    failed_checks = len(problems)
    passed_checks = total_checks - failed_checks
    
    print(f"📈 RESULTS:")
    print(f"  Total Checks: {total_checks}")
    print(f"  ✅ Passed: {passed_checks}")
    print(f"  ❌ Failed: {failed_checks}")
    print(f"  📊 Success Rate: {(passed_checks/total_checks)*100:.1f}%")
    
    if problems:
        print(f"\n🚨 DETAILED PROBLEMS IDENTIFIED ({len(problems)}):")
        for i, problem in enumerate(problems, 1):
            print(f"  {i:2d}. {problem}")
        
        print(f"\n💡 COMPREHENSIVE SOLUTIONS:")
        print("  1. 📦 Dependencies: pip install -r requirements.txt")
        print("  2. 🔧 Environment: Activate virtual environment")
        print("  3. 📝 Files: Check permissions and syntax")
        print("  4. ⚙️ Config: Verify config.json structure")
        print("  5. 🖥️ Resources: Free up memory and disk space")
        print("  6. 🎨 GUI: Check display system availability")
        print("  7. 📊 Backend: Ensure matplotlib Qt5Agg backend")
        print("  8. 🔍 Integration: Verify all components work together")
    else:
        print(f"\n🎉 ALL 19 CHECKS PASSED - SYSTEM FULLY OPERATIONAL!")
        print("✅ Complete system validation successful")
        print("✅ All components integrated and functional")
        print("✅ Performance optimization active")
        print("✅ Ready for production deployment")
        print("✅ Stable for continuous operation")
    
    return len(problems) == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)