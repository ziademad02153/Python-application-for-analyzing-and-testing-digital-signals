# Heater Test System

A professional Python application for monitoring and testing heater signals using National Instruments DAQ devices.

## Description

The Heater Test System is a real-time monitoring application that reads analog voltage signals from a cDAQ device and provides a comprehensive interface for real-time signal monitoring, state tracking with duration calculation, data visualization in a professional table format, and data export to Excel and CSV formats.

## Features

- 6-Channel Monitoring: Heat, Ready, Eco, Clean, Heater1, Heater2
- Real-time Updates with 1-second refresh rate
- State Detection with automatic state change detection and threshold-based logic
- Duration Tracking with real-time duration calculation for each state
- Professional GUI built with PyQt6 (modern dark theme)
- Color-coded Signals with visual indicators for active signals
- Data Export to Excel and CSV formats
- Data Reset functionality to clear all data and restart monitoring
- Resizable layout with splitter: larger live chart and data table
- Time-based chart with auto time-axis formatting, grid, and smooth visuals (last 200 points)
- Auto-scroll table to keep the latest reading visible every second
- All5 Count and All0 Count columns with voltage ranges:
  - All5 Count: all selected channels in 4.50–5.00 V
  - All0 Count: all selected channels in 0.00–0.44 V
- Safe stop behavior: on Stop, data exported to Excel automatically to `logs/`; on window close, CSV saved to `logs/heater_log.csv`
- Robust DAQ handling: read error resilience and clean task close
- Automated heater testing (~87% automation): start/monitor/log/export with minimal user interaction

## Requirements

- Operating System: Windows 10/11
- Python: 3.8 - 3.13 (PyQt6 compatibility)
- Hardware: National Instruments cDAQ device with analog input module
- Software: NI-DAQmx driver installed for `nidaqmx` to communicate with hardware

## Dependencies

- PyQt6
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

Logs are written under the project `logs/` directory (configurable via `LOGS_DIR`).

## Automation

- Roughly 87% of the heater testing workflow is automated:
  - App launches, starts periodic acquisition (1s), updates UI, and logs without manual steps.
  - Auto-save to Excel on Stop and CSV on window close.
  - Error-tolerant acquisition and safe resource cleanup (task stop/close).

## Data Columns

- Time: timestamp HH:MM:SS per sample.
- Heat, Ready, Eco, Clean: digital-like voltages (colored when active above threshold).
- Heater1, Heater2: analog voltage channels plotted live.
- Current State / Previous State: active signal names joined, with automatic transitions.
- Duration: seconds since last state change.
- All5 Count: increments when all of [Heat, Ready, Eco, Clean, Heater1, Heater2] are within 4.50–5.00 V simultaneously.
- All0 Count: increments when all of the same set are within 0.00–0.44 V simultaneously.

## Live Chart

- Time-based X-axis with automatic formatting (HH:MM:SS), dark theme.
- Smooth lines with subtle area fill; grid for readability.
- Shows latest 200 points for responsiveness; size prioritized via resizable splitter.
- Distinct colors for Heater1/Heater2 and clear legend.

## Author

- GitHub: ziademad02153
- Email: ziademadbts@gmail.com