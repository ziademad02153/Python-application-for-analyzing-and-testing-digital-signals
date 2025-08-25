#!/usr/bin/env python3
"""
Test script to demonstrate the Error Number Detection System
This script shows how TTL frame errors are detected and numbered.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from heater_monitor import SerialManager, DEFAULT_CONFIG

def test_error_detection():
    """Test the error number detection system"""
    print("🧪 TESTING ERROR NUMBER DETECTION SYSTEM")
    print("=" * 60)
    
    # Initialize serial manager
    serial_manager = SerialManager(DEFAULT_CONFIG)
    
    # Test data with various error patterns
    test_cases = [
        # Display errors (Error #1-6)
        ("M1,H0,T25,TT30,/iv,CM0,CH0,C3M0,ECO0,HL0,RL1,EL0,CL0", "Display Error #1: /iv pattern"),
        ("M1,H0,T25,TT30,CM0,CH0,vrl,C3M0,ECO0,HL0,RL1,EL0,CL0", "Display Error #2: vrl pattern"),
        ("M1,H0,T25,TT30,CM0,CH0,err,C3M0,ECO0,HL0,RL1,EL0,CL0", "Display Error #3: err pattern"),
        ("M1,H0,T25,TT30,CM0,CH0,Er,C3M0,ECO0,HL0,RL1,EL0,CL0", "Display Error #4: Er pattern"),
        ("M1,H0,T25,TT30,CM0,CH0,E-,C3M0,ECO0,HL0,RL1,EL0,CL0", "Display Error #5: E- pattern"),
        ("M1,H0,T25,TT30,CM0,CH0,-E,C3M0,ECO0,HL0,RL1,EL0,CL0", "Display Error #6: -E pattern"),
        
        # Valid data for comparison
        ("M1,H0,T25,TT30,CM0,CH0,C3M0,ECO0,HL0,RL1,EL0,CL0", "Valid TTL frame"),
        
        # Validation errors will be tested separately
        ("M9,H0,T25,TT30,CM0,CH0,C3M0,ECO0,HL0,RL1,EL0,CL0", "Invalid mode (Error #11)"),
        ("M1,H0,T150,TT30,CM0,CH0,C3M0,ECO0,HL0,RL1,EL0,CL0", "Invalid water temp (Error #12)"),
        ("M1,H0,T25,TT150,CM0,CH0,C3M0,ECO0,HL0,RL1,EL0,CL0", "Invalid target temp (Error #13)"),
        ("M1,H0,T25,TT30,CM0,CH0,C3M0,ECO0,HL3,RL1,EL0,CL0", "Invalid Heat LED voltage (Error #14)"),
    ]
    
    print("🔍 Testing Display Error Detection:")
    print("-" * 40)
    
    for i, (ttl_data, description) in enumerate(test_cases, 1):
        print(f"\nTest {i}: {description}")
        print(f"TTL Data: {ttl_data}")
        
        # Test display error detection
        error_number = serial_manager.detect_display_errors(ttl_data)
        if error_number > 0:
            print(f"✅ Display Error #{error_number} detected!")
        else:
            print("✅ No display error detected")
        
        # Test TTL parsing and validation
        parsed_data = serial_manager.parse_ttl_data(ttl_data)
        validation_result = serial_manager.validate_ttl_frame(parsed_data, ttl_data)
        
        if not validation_result['valid']:
            validation_error_number = validation_result.get('error_number', 0)
            print(f"⚠️ Validation Error #{validation_error_number}: {validation_result['error']}")
        else:
            print("✅ TTL frame validation passed")
        
        print(f"Parsed Values: {parsed_data}")
    
    print("\n" + "=" * 60)
    print("🎯 ERROR NUMBER SUMMARY:")
    print("  Display Errors: #1-6 (7-segment display issues)")
    print("  Frame Errors: #10-20 (TTL validation issues)")
    print("  Parsing Errors: #30 (Communication issues)")
    print("=" * 60)

if __name__ == "__main__":
    test_error_detection()