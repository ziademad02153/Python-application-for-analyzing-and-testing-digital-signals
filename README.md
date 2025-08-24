# Heater Test System - Advanced Edition

A professional Python application for analyzing and testing digital signals from heater systems using National Instruments DAQ devices.

## 🚀 **New Advanced Features (Version 2.0)**

### 🎮 **Simulation Mode**
- **Mock DAQ**: Test the application without hardware
- **Real-time Simulation**: Generate realistic test data
- **Toggle Switch**: Easy switching between simulation and real DAQ
- **Development Friendly**: Perfect for testing and demonstrations

### ⚙️ **Configuration Management**
- **Persistent Settings**: Save thresholds, colors, and preferences
- **JSON Config**: Human-readable configuration files
- **Auto-save**: Settings persist between sessions
- **Customizable**: Easy to modify without code changes

### 🔄 **Multi-threaded Architecture**
- **Separate DAQ Thread**: UI never freezes during data acquisition
- **Real-time Updates**: Smooth, responsive interface
- **Error Handling**: Graceful handling of DAQ errors
- **Performance**: Better resource utilization

### 📊 **Advanced Data Analysis**
- **Smart Filtering**: Filter data by date, state, or values
- **Session Comparison**: Compare multiple test sessions
- **Predictive Analytics**: Predict when All5/All0 events will occur
- **Statistical Insights**: Advanced data processing capabilities

### 📈 **Enhanced Export Options**
- **PDF Reports**: Professional reports with charts and data
- **Excel Export**: Enhanced spreadsheet output
- **Multiple Formats**: Support for various export types
- **Report Templates**: Professional report layouts

### 🔔 **Smart Notifications**
- **Audio Alerts**: Sound notifications for important events
- **Visual Indicators**: Clear status displays
- **Event Tracking**: Monitor All5/All0 occurrences
- **Customizable Alerts**: Configure notification preferences

## 🎯 **Core Features**

### **Automation (87%)**
- Continuous data acquisition until manual stop
- Automatic state detection and tracking
- Real-time data logging and analysis
- Intelligent signal processing

### **Data Columns**
- **Time**: Timestamp of each reading
- **Heat, Ready, Eco, Clean**: Status indicators
- **Heater1, Heater2**: Voltage readings
- **Current/Previous State**: State tracking
- **Duration**: Time in current state
- **All5 Count**: Instances of 4.5V-5.0V across all channels
- **All0 Count**: Instances of 0.0V-0.44V across all channels

### **Live Chart**
- Real-time voltage plotting
- Professional dark theme
- Smooth animations
- Fixed time axis (no overlapping labels)
- Large chart display (1/3 to 1/2 screen)
- Auto-scaling and zoom

### **Professional UI**
- Modern dark theme
- English language interface
- Professional header bar with lamp indicators
- Fixed counter displays
- Auto-scrolling table
- Hidden scrollbars for clean appearance

## 🛠️ **Technical Specifications**

### **Requirements**
- Python 3.8 - 3.13
- PyQt6 for modern GUI
- National Instruments DAQ hardware (optional with simulation mode)
- Windows 10/11

### **Dependencies**
```
PyQt6>=6.0.0          # Modern GUI framework
nidaqmx>=0.5.7         # DAQ communication
matplotlib>=3.5.0      # Data visualization
pandas>=1.3.0          # Data manipulation
openpyxl>=3.0.0        # Excel export
reportlab>=3.6.0       # PDF generation
```

### **Architecture**
- **Multi-threaded**: Separate DAQ and UI threads
- **Event-driven**: Signal-based communication
- **Modular**: Easy to extend and maintain
- **Configurable**: JSON-based settings

## 🚀 **Getting Started**

### **Installation**
```bash
# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

### **Running the Application**
```bash
python heater_monitor.py
```

### **Simulation Mode**
1. Check "Simulation Mode" checkbox
2. Application runs without hardware
3. Perfect for testing and development

### **Real DAQ Mode**
1. Connect National Instruments DAQ device
2. Ensure device name matches `DEVICE_NAME` in code
3. Uncheck "Simulation Mode"

## 📁 **File Structure**
```
WH.Python.App/
├── heater_monitor.py      # Main application
├── config.json            # Configuration file
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── logs/                 # Data output directory
│   ├── heater_*.xlsx    # Excel exports
│   └── heater_log.csv   # CSV logs
└── .venv/               # Virtual environment
```

## 🔧 **Configuration**

### **config.json Options**
```json
{
  "thresholds": {
    "all5_min": 4.5,      # Minimum voltage for All5
    "all5_max": 5.0,      # Maximum voltage for All5
    "all0_min": 0.0,      # Minimum voltage for All0
    "all0_max": 0.44      # Maximum voltage for All0
  },
  "colors": {
    "heater1": "#4FC3F7", # Heater1 chart color
    "heater2": "#FFB74D"  # Heater2 chart color
  },
  "update_rate": 500,     # Data update rate (ms)
  "simulation_mode": false # Enable/disable simulation
}
```

## 🎨 **Customization**

### **Adding New Features**
- Extend `HeaterTestSystem` class
- Add new methods for functionality
- Update configuration as needed
- Follow existing code patterns

### **Modifying Thresholds**
- Edit `config.json` file
- Change voltage ranges
- Restart application
- Settings automatically apply

## 📊 **Data Analysis**

### **Filtering Data**
- Use "Filter Data" button
- Select date ranges
- Filter by state changes
- Export filtered results

### **Comparing Sessions**
- Load multiple test sessions
- Side-by-side comparison
- Trend analysis
- Performance tracking

### **Predictions**
- Analyze historical patterns
- Predict future events
- Optimize test timing
- Improve efficiency

## 🔮 **Future Enhancements**

### **Planned Features**
- **Machine Learning**: Advanced pattern recognition
- **Cloud Integration**: Remote monitoring capabilities
- **Mobile App**: Companion mobile application
- **API Support**: REST API for integration
- **Database**: Advanced data storage and querying

### **User Requests**
- **Custom Alerts**: User-defined notification rules
- **Report Templates**: Customizable report layouts
- **Data Export**: Additional export formats
- **Real-time Sharing**: Live data sharing capabilities

## 🤝 **Contributing**

### **Development Setup**
1. Fork the repository
2. Create feature branch
3. Implement changes
4. Test thoroughly
5. Submit pull request

### **Code Standards**
- Follow PEP 8 style guide
- Add docstrings to functions
- Include type hints
- Write unit tests

## 📞 **Support**

### **Common Issues**
- **DAQ Connection**: Check device name and connections
- **Performance**: Use simulation mode for testing
- **Configuration**: Verify `config.json` format
- **Dependencies**: Ensure all packages are installed

### **Getting Help**
- Check configuration settings
- Review error messages
- Test in simulation mode
- Consult documentation

## 📄 **License**

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Version**: 2.0 Advanced Edition  
**Last Updated**: 2025  
**Author**: Python Application Development Team  
**Status**: Active Development