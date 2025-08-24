#!/usr/bin/env python3
"""
Test script to verify all required modules can be imported
"""

print("Testing module imports...")

try:
    import sys
    print(f"✅ Python version: {sys.version}")
except Exception as e:
    print(f"❌ Python import failed: {e}")

try:
    from PyQt6.QtWidgets import QApplication
    print("✅ PyQt6 imported successfully")
except Exception as e:
    print(f"❌ PyQt6 import failed: {e}")

try:
    import numpy as np
    print(f"✅ NumPy {np.__version__} imported successfully")
except Exception as e:
    print(f"❌ NumPy import failed: {e}")

try:
    import matplotlib
    print(f"✅ Matplotlib {matplotlib.__version__} imported successfully")
except Exception as e:
    print(f"❌ Matplotlib import failed: {e}")

try:
    import pandas as pd
    print(f"✅ Pandas {pd.__version__} imported successfully")
except Exception as e:
    print(f"❌ Pandas import failed: {e}")

try:
    import nidaqmx
    print("✅ NI DAQmx imported successfully")
except Exception as e:
    print(f"❌ NI DAQmx import failed: {e}")

try:
    import openpyxl
    print(f"✅ OpenPyXL {openpyxl.__version__} imported successfully")
except Exception as e:
    print(f"❌ OpenPyXL import failed: {e}")

try:
    import serial
    print("✅ PySerial imported successfully")
except Exception as e:
    print(f"❌ PySerial import failed: {e}")

print("\n" + "="*50)
print("Import test completed!")
print("If all modules show ✅, you can run the main application.")
print("If any module shows ❌, please fix that dependency first.")