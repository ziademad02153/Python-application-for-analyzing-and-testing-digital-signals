"""
Comprehensive System Diagnostic - Identify All 12 Problems
This script systematically checks all components and identifies issues
"""

import sys
import os
import traceback
from datetime import datetime

def print_header(title):
    """Print diagnostic section header"""
    print(f"\n{'='*60}")
    print(f"🔍 {title}")
    print(f"{'='*60}")

def test_imports():
    """Test 1-4: Module Import Issues"""
    print_header("TESTING MODULE IMPORTS")
    
    import_tests = [
        ("PyQt6.QtWidgets", "QApplication, QMainWindow"),
        ("PyQt6.QtCore", "QTimer, QThread"),
        ("matplotlib.pyplot", "pyplot"),
        ("pandas", "pandas"),
        ("psutil", "psutil"),
        ("openpyxl", "openpyxl"),
        ("nidaqmx", "nidaqmx"),
        ("serial", "pyserial"),
        ("performance_optimization", "PerformanceOptimizer"),
        ("heater_monitor", "HeaterTestSystem")
    ]
    
    problems = []
    for i, (module_name, description) in enumerate(import_tests, 1):
        try:
            __import__(module_name)
            print(f"✅ Problem {i}: {module_name} ({description}) - OK")
        except ImportError as e:
            error_msg = f"❌ Problem {i}: {module_name} - FAILED: {e}"
            print(error_msg)
            problems.append(error_msg)
    
    return problems

def test_performance_optimization():
    """Test 5-8: Performance Optimization Issues"""
    print_header("TESTING PERFORMANCE OPTIMIZATION")
    
    problems = []
    
    # Define MockApp class for all tests
    class MockApp:
        def __init__(self):
            self.timestamps = list(range(1000))  # 1000 data points
            self.heater1_data = [25.0] * 1000
            self.heater2_data = [30.0] * 1000
    
    mock_app = MockApp()
    
    try:
        # Test 5: Chart Optimizer Data Point Limiting
        print("🧪 Test 5: Chart Data Point Limiting")
        from performance_optimization import ChartOptimizer
        optimizer = ChartOptimizer(mock_app)
        
        plot_timestamps, plot_heater1, plot_heater2 = optimizer.get_optimized_data_points()
        
        if len(plot_timestamps) <= optimizer.data_points_limit:
            print(f"✅ Problem 5: Data point limiting works ({len(plot_timestamps)}/{optimizer.data_points_limit})")
        else:
            error_msg = f"❌ Problem 5: Data points exceed limit ({len(plot_timestamps)}/{optimizer.data_points_limit})"
            print(error_msg)
            problems.append(error_msg)
            
    except Exception as e:
        error_msg = f"❌ Problem 5: Chart optimizer error: {e}"
        print(error_msg)
        problems.append(error_msg)
    
    try:
        # Test 6: Memory Monitoring
        print("🧪 Test 6: Memory Monitoring")
        from performance_optimization import PerformanceOptimizer
        
        mock_app = MockApp()
        perf_optimizer = PerformanceOptimizer(mock_app)
        memory_usage = perf_optimizer.get_memory_usage()
        
        if memory_usage > 0:
            print(f"✅ Problem 6: Memory monitoring works ({memory_usage:.1f} MB)")
        else:
            error_msg = "❌ Problem 6: Memory monitoring failed"
            print(error_msg)
            problems.append(error_msg)
            
    except Exception as e:
        error_msg = f"❌ Problem 6: Performance optimizer error: {e}"
        print(error_msg)
        problems.append(error_msg)
    
    try:
        # Test 7: Auto-Save Manager
        print("🧪 Test 7: Auto-Save Manager")
        from performance_optimization import AutoSaveManager
        
        auto_save = AutoSaveManager(mock_app)
        if hasattr(auto_save, 'auto_save_timer'):
            print("✅ Problem 7: Auto-save manager initialized")
        else:
            error_msg = "❌ Problem 7: Auto-save timer not initialized"
            print(error_msg)
            problems.append(error_msg)
            
    except Exception as e:
        error_msg = f"❌ Problem 7: Auto-save manager error: {e}"
        print(error_msg)
        problems.append(error_msg)
    
    try:
        # Test 8: Chart Redraw Logic
        print("🧪 Test 8: Chart Redraw Logic")
        from performance_optimization import ChartOptimizer
        optimizer = ChartOptimizer(mock_app)
        
        # Test redraw decision
        should_redraw_1 = optimizer.should_full_redraw()
        should_redraw_2 = optimizer.should_full_redraw()  # Immediate second call
        
        # Should skip frequent redraws
        if should_redraw_1 != should_redraw_2 or not should_redraw_2:
            print("✅ Problem 8: Intelligent redraw skipping works")
        else:
            error_msg = "❌ Problem 8: Redraw skipping logic failed"
            print(error_msg)
            problems.append(error_msg)
            
    except Exception as e:
        error_msg = f"❌ Problem 8: Redraw logic error: {e}"
        print(error_msg)
        problems.append(error_msg)
    
    return problems

def test_main_application():
    """Test 9-10: Main Application Issues"""
    print_header("TESTING MAIN APPLICATION")
    
    problems = []
    
    try:
        # Test 9: Main App Import and Initialization
        print("🧪 Test 9: Main Application Import")
        from heater_monitor import HeaterTestSystem
        print("✅ Problem 9: HeaterTestSystem import successful")
        
    except Exception as e:
        error_msg = f"❌ Problem 9: Main application import failed: {e}"
        print(error_msg)
        problems.append(error_msg)
    
    try:
        # Test 10: Performance Integration
        print("🧪 Test 10: Performance Integration Check")
        from heater_monitor import HAS_PERFORMANCE_OPT
        if HAS_PERFORMANCE_OPT:
            print("✅ Problem 10: Performance optimization integration enabled")
        else:
            error_msg = "❌ Problem 10: Performance optimization not integrated"
            print(error_msg)
            problems.append(error_msg)
            
    except Exception as e:
        error_msg = f"❌ Problem 10: Performance integration check failed: {e}"
        print(error_msg)
        problems.append(error_msg)
    
    return problems

def test_comprehensive_suite():
    """Test 11-12: Comprehensive Test Suite Issues"""
    print_header("TESTING COMPREHENSIVE TEST SUITE")
    
    problems = []
    
    try:
        # Test 11: Comprehensive Tests Import
        print("🧪 Test 11: Comprehensive Tests Import")
        from comprehensive_tests import TestHeaterMonitorSystem
        print("✅ Problem 11: Comprehensive tests import successful")
        
    except Exception as e:
        error_msg = f"❌ Problem 11: Comprehensive tests import failed: {e}"
        print(error_msg)
        problems.append(error_msg)
    
    try:
        # Test 12: Chart Performance Test
        print("🧪 Test 12: Chart Performance Test Suite")
        
        # Check if file exists and is readable
        if os.path.exists("chart_performance_test_fixed.py"):
            with open("chart_performance_test_fixed.py", 'r') as f:
                content = f.read()
                if "ChartPerformanceTest" in content:
                    print("✅ Problem 12: Chart performance test suite available")
                else:
                    error_msg = "❌ Problem 12: Chart performance test class not found"
                    print(error_msg)
                    problems.append(error_msg)
        else:
            error_msg = "❌ Problem 12: Chart performance test file missing"
            print(error_msg)
            problems.append(error_msg)
            
    except Exception as e:
        error_msg = f"❌ Problem 12: Chart performance test check failed: {e}"
        print(error_msg)
        problems.append(error_msg)
    
    return problems

def main():
    """Main diagnostic function"""
    print("🚀 COMPREHENSIVE SYSTEM DIAGNOSTIC")
    print(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🐍 Python: {sys.version}")
    print(f"📁 Working Directory: {os.getcwd()}")
    
    all_problems = []
    
    # Run all diagnostic tests
    all_problems.extend(test_imports())
    all_problems.extend(test_performance_optimization())
    all_problems.extend(test_main_application())
    all_problems.extend(test_comprehensive_suite())
    
    # Final summary
    print_header("DIAGNOSTIC SUMMARY")
    
    total_tests = 12
    failed_tests = len(all_problems)
    passed_tests = total_tests - failed_tests
    
    print(f"📊 RESULTS:")
    print(f"  Total Tests: {total_tests}")
    print(f"  ✅ Passed: {passed_tests}")
    print(f"  ❌ Failed: {failed_tests}")
    print(f"  📈 Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    
    if all_problems:
        print(f"\n🚨 PROBLEMS IDENTIFIED ({len(all_problems)}):")
        for i, problem in enumerate(all_problems, 1):
            print(f"  {i}. {problem}")
            
        print(f"\n💡 RECOMMENDED ACTIONS:")
        if any("import" in p.lower() for p in all_problems):
            print("  - Install missing dependencies: pip install -r requirements.txt")
        if any("chart" in p.lower() for p in all_problems):
            print("  - Fix chart optimization data point limiting")
        if any("performance" in p.lower() for p in all_problems):
            print("  - Review performance optimization integration")
        if any("test" in p.lower() for p in all_problems):
            print("  - Fix test suite import/execution issues")
    else:
        print(f"\n🎉 ALL TESTS PASSED - SYSTEM IS STABLE!")
        print(f"✅ Chart performance issues resolved")
        print(f"✅ All dependencies available")
        print(f"✅ Performance optimization working")
        print(f"✅ Test suites functional")
    
    return len(all_problems) == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)