# Heater Test System

A professional Python application for monitoring and testing heater signals using National Instruments DAQ devices.

## Description

The Heater Test System is a real-time monitoring application that reads analog voltage signals from a cDAQ device and provides a comprehensive interface for real-time signal monitoring, state tracking with duration calculation, data visualization in a professional table format, and data export to Excel and CSV formats.

## Features

- 6-Channel Monitoring: Heat, Ready, Eco, Clean, Heater1, Heater2
- Real-time Updates with 1-second refresh rate
- State Detection with automatic state change detection and threshold-based logic
- Duration Tracking with real-time duration calculation for each state
- Professional GUI built with PyQt5
- Color-coded Signals with visual indicators for active signals
- Data Export to Excel and CSV formats
- Data Reset functionality to clear all data and restart monitoring

## Requirements

- Operating System: Windows 10/11
- Python: 3.8 - 3.11 (PyQt5 compatibility)
- Hardware: National Instruments cDAQ device with analog input module

## Dependencies

- PyQt5
- nidaqmx
- matplotlib
- pandas
- openpyxl

## Configuration

The application is configured for a cDAQ1Mod1 device with 6 analog input channels:
- Heat (ai0): Heating signal indicator
- Ready (ai1): Ready state indicator
- Eco (ai2): Eco mode indicator
- Clean (ai3): Cleaning mode indicator
- Heater1 (ai4): Primary heater voltage
- Heater2 (ai5): Secondary heater voltage

Signal threshold is set to 1.0V with 1000ms update rate.

## Author

- GitHub: ziademad02153
- Email: ziademadbts@gmail.com