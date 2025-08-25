#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

setup(
    name="heater-monitor-system",
    version="2.0.0",
    description="Professional Heater Monitor System with DAQ and TTL support",
    author="Heater Monitor Team",
    author_email="support@heatermonitor.com",
    packages=find_packages(),
    install_requires=[
        "PyQt6>=6.0.0",
        "nidaqmx>=1.0.0",
        "matplotlib>=3.5.0",
        "pandas>=1.3.0",
        "pyserial>=3.5",
        "psutil>=5.0.0",
        "openpyxl>=3.0.0"
    ],
    python_requires=">=3.8",
    include_package_data=True,
    package_data={
        "": ["*.json", "*.md", "*.txt", "*.bat"]
    },
    entry_points={
        "console_scripts": [
            "heater-monitor=heater_monitor:main",
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Manufacturing",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: System :: Hardware",
        "Topic :: System :: Monitoring",
    ],
    keywords="heater monitor daq ttl serial communication",
    project_urls={
        "Bug Reports": "https://github.com/heater-monitor/issues",
        "Source": "https://github.com/heater-monitor/heater-monitor-system",
        "Documentation": "https://heater-monitor.readthedocs.io/",
    },
)
