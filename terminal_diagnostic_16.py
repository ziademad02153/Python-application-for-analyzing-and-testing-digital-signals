"""
Comprehensive 16-Point Terminal Diagnostic
Systematic identification of all terminal problems
"""

import sys
import os
import traceback
import subprocess
import json
from datetime import datetime

def print_header(title, problem_num=None):
    """Print diagnostic section header"""
    if problem_num:
        print(f"\n{'='*60}")
        print(f"🔍 Problem {problem_num}: {title}")
        print(f"{'='*60}")
    else:
        print(f"\n{'='*60}")
        print(f"🔍 {title}")
        print(f"{'='*60}")

def main():
    """Main diagnostic function for 16 problems"""
    print("🚀 COMPREHENSIVE 16-POINT TERMINAL DIAGNOSTIC")
    print(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🐍 Python: {sys.version}")
    print(f"📁 Working Directory: {os.getcwd()}")
    
    problems_found = []
    
    # Problem 1: Python Version Compatibility
    print_header("Python Version Compatibility", 1)
    try:
        version = sys.version_info
        if version.major == 3 and 8 <= version.minor <= 13:
            print(f"✅ Python {version.major}.{version.minor} is compatible")
        else:
            error_msg = f"❌ Python {version.major}.{version.minor} may have compatibility issues"
            print(error_msg)
            problems_found.append(error_msg)
    except Exception as e:
        error_msg = f"❌ Python version check failed: {e}"
        print(error_msg)
        problems_found.append(error_msg)
    
    # Problem 2: Required Files Existence
    print_header("Required Files Existence", 2)
    required_files = [
        'heater_monitor.py',
        'performance_optimization.py', 
        'comprehensive_tests.py',
        'config.json',
        'requirements.txt'
    ]
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file} exists")
        else:
            error_msg = f"❌ Missing required file: {file}"
            print(error_msg)
            problems_found.append(error_msg)
    
    # Problem 3: Config File Validation
    print_header("Config File Validation", 3)
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
        
        required_keys = ['thresholds', 'colors', 'update_rate', 'simulation_mode']
        for key in required_keys:
            if key in config:
                print(f"✅ Config key '{key}' present")
            else:
                error_msg = f"❌ Missing config key: {key}"
                print(error_msg)
                problems_found.append(error_msg)
    except Exception as e:
        error_msg = f"❌ Config file error: {e}"
        print(error_msg)
        problems_found.append(error_msg)
    
    # Problem 4-11: Module Import Tests
    print_header("Module Import Tests", 4)
    modules_to_test = [
        ('PyQt6.QtWidgets', 4),
        ('PyQt6.QtCore', 5),
        ('matplotlib.pyplot', 6),
        ('matplotlib.backends.backend_qt5agg', 7),
        ('pandas', 8),
        ('psutil', 9),
        ('openpyxl', 10),
        ('nidaqmx', 11)
    ]
    
    for module_name, problem_num in modules_to_test:
        try:
            __import__(module_name)
            print(f"✅ Problem {problem_num}: {module_name} - Import OK")
        except ImportError as e:
            error_msg = f"❌ Problem {problem_num}: {module_name} - Import Failed: {e}"
            print(error_msg)
            problems_found.append(error_msg)
    
    # Problem 12: Performance Optimization Integration
    print_header("Performance Optimization Integration", 12)
    try:
        from performance_optimization import PerformanceOptimizer, ChartOptimizer
        
        # Test class instantiation
        class MockApp:
            def __init__(self):
                self.timestamps = []
                self.heater1_data = []
                self.heater2_data = []
        
        mock_app = MockApp()
        perf_opt = PerformanceOptimizer(mock_app)
        chart_opt = ChartOptimizer(mock_app)
        
        print("✅ Performance optimization classes working")
    except Exception as e:
        error_msg = f"❌ Performance optimization error: {e}"
        print(error_msg)
        problems_found.append(error_msg)
    
    # Problem 13: Chart Data Point Limiting
    print_header("Chart Data Point Limiting", 13)
    try:
        from performance_optimization import ChartOptimizer
        
        # Define MockApp for this test
        class MockAppData:
            def __init__(self):
                self.timestamps = list(range(1000))  # 1000 points
                self.heater1_data = [25.0] * 1000
                self.heater2_data = [30.0] * 1000
        
        mock_app = MockAppData()
        
        optimizer = ChartOptimizer(mock_app)
        plot_data = optimizer.get_optimized_data_points()
        
        if len(plot_data[0]) <= optimizer.data_points_limit:
            print(f"✅ Data point limiting works ({len(plot_data[0])}/{optimizer.data_points_limit})")
        else:
            error_msg = f"❌ Data points exceed limit ({len(plot_data[0])}/{optimizer.data_points_limit})"
            print(error_msg)
            problems_found.append(error_msg)
    except Exception as e:
        error_msg = f"❌ Chart data limiting error: {e}"
        print(error_msg)
        problems_found.append(error_msg)
    
    # Problem 14: Main Application Integration
    print_header("Main Application Integration", 14)
    try:
        from heater_monitor import HeaterTestSystem, HAS_PERFORMANCE_OPT
        
        if HAS_PERFORMANCE_OPT:
            print("✅ Performance optimization integrated in main app")
        else:
            error_msg = "❌ Performance optimization not integrated"
            print(error_msg)
            problems_found.append(error_msg)
    except Exception as e:
        error_msg = f"❌ Main application integration error: {e}"
        print(error_msg)
        problems_found.append(error_msg)
    
    # Problem 15: Test Suite Execution
    print_header("Test Suite Execution", 15)
    try:
        # Test if comprehensive_tests can be imported and run
        from comprehensive_tests import TestHeaterMonitorSystem
        print("✅ Comprehensive test suite can be imported")
        
        # Test if chart performance test can be run
        if os.path.exists('chart_performance_test_fixed.py'):
            with open('chart_performance_test_fixed.py', 'r', encoding='utf-8') as f:
                content = f.read()
                if 'ChartPerformanceTest' in content:
                    print("✅ Chart performance test suite available")
                else:
                    error_msg = "❌ Chart performance test class missing"
                    print(error_msg)
                    problems_found.append(error_msg)
        else:
            error_msg = "❌ Chart performance test file missing"
            print(error_msg)
            problems_found.append(error_msg)
    except Exception as e:
        error_msg = f"❌ Test suite error: {e}"
        print(error_msg)
        problems_found.append(error_msg)
    
    # Problem 16: System Memory and Performance
    print_header("System Memory and Performance", 16)
    try:
        import psutil
        
        # Check available memory
        memory = psutil.virtual_memory()
        available_gb = memory.available / (1024**3)
        
        if available_gb > 1.0:
            print(f"✅ Sufficient memory available: {available_gb:.1f} GB")
        else:
            error_msg = f"❌ Low memory warning: {available_gb:.1f} GB available"
            print(error_msg)
            problems_found.append(error_msg)
        
        # Check CPU usage
        cpu_percent = psutil.cpu_percent(interval=1)
        if cpu_percent < 80:
            print(f"✅ CPU usage normal: {cpu_percent:.1f}%")
        else:
            error_msg = f"❌ High CPU usage: {cpu_percent:.1f}%"
            print(error_msg)
            problems_found.append(error_msg)
            
    except Exception as e:
        error_msg = f"❌ System performance check error: {e}"
        print(error_msg)
        problems_found.append(error_msg)
    
    # Final Summary
    print_header("DIAGNOSTIC SUMMARY")
    
    total_checks = 16
    failed_checks = len(problems_found)
    passed_checks = total_checks - failed_checks
    
    print(f"📊 RESULTS:")
    print(f"  Total Checks: {total_checks}")
    print(f"  ✅ Passed: {passed_checks}")
    print(f"  ❌ Failed: {failed_checks}")
    print(f"  📈 Success Rate: {(passed_checks/total_checks)*100:.1f}%")
    
    if problems_found:
        print(f"\n🚨 PROBLEMS IDENTIFIED ({len(problems_found)}):")
        for i, problem in enumerate(problems_found, 1):
            print(f"  {i}. {problem}")
            
        print(f"\n💡 RECOMMENDED ACTIONS:")
        if any("import" in p.lower() for p in problems_found):
            print("  - Install missing dependencies: pip install -r requirements.txt")
        if any("config" in p.lower() for p in problems_found):
            print("  - Fix config.json file structure and content")
        if any("performance" in p.lower() for p in problems_found):
            print("  - Review performance optimization integration")
        if any("test" in p.lower() for p in problems_found):
            print("  - Fix test suite import/execution issues")
        if any("memory" in p.lower() or "cpu" in p.lower() for p in problems_found):
            print("  - Close other applications to free system resources")
    else:
        print(f"\n🎉 ALL 16 CHECKS PASSED - SYSTEM IS FULLY OPERATIONAL!")
        print(f"✅ No terminal problems detected")
        print(f"✅ All modules and dependencies working")
        print(f"✅ Performance optimization active")
        print(f"✅ Test suites functional")
        print(f"✅ System resources adequate")
    
    return len(problems_found) == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)