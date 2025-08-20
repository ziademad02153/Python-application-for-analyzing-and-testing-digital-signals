import sys
import csv
import time
import os
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QLabel, QPushButton, QHBoxLayout
)
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QColor
import nidaqmx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import pandas as pd

DEVICE_NAME = "cDAQ1Mod1"

CHANNELS = {
    'Heat': 'ai0',
    'Ready': 'ai1',
    'Eco': 'ai2',
    'Clean': 'ai3',
    'Heater1': 'ai4',
    'Heater2': 'ai5'
}

COLORS = {
    'Heat': QColor(255, 165, 0),    # برتقالي
    'Ready': QColor(255, 0, 0),     # أحمر
    'Eco': QColor(0, 255, 0),       # أخضر
    'Clean': QColor(169, 169, 169)  # رمادي
}

THRESHOLD = 1.0

class HeaterTestSystem(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Heater Test System")
        self.resize(1200, 750)

        self.task = nidaqmx.Task()
        for ch in CHANNELS.values():
            self.task.ai_channels.add_ai_voltage_chan(f"{DEVICE_NAME}/{ch}")
        self.task.start()

        self.layout = QVBoxLayout()
        self.status_label = QLabel("Current State: None | Previous State: None")
        self.duration_label = QLabel("Duration: 0 sec")
        self.table = QTableWidget(0, 10)
        self.table.setHorizontalHeaderLabels([
            "Time", "Heat", "Ready", "Eco", "Clean",
            "Heater1", "Heater2", "Current State", "Previous State", "Duration"
        ])
        self.save_button = QPushButton("save")
        self.stop_button = QPushButton("stop")
        self.reset_button = QPushButton("Reset")
        self.save_button.clicked.connect(self.save_direct)
        self.stop_button.clicked.connect(self.stop_acquisition)
        self.reset_button.clicked.connect(self.reset_data)

        self.canvas = FigureCanvas(plt.Figure())
        self.ax = self.canvas.figure.add_subplot(111)
        self.timestamps = []
        self.heater1_data = []
        self.heater2_data = []

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.save_button)
        btn_layout.addWidget(self.stop_button)
        btn_layout.addWidget(self.reset_button)
        self.layout.addWidget(self.status_label)
        self.layout.addWidget(self.duration_label)
        self.layout.addWidget(self.table)
        self.layout.addWidget(self.canvas)
        self.layout.addLayout(btn_layout)
        self.setLayout(self.layout)

        self.last_state = "None"
        self.current_state = "None"
        self.state_start_time = time.time()
        self.data_log = []

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(1000)

    def read_signals(self):
        return self.task.read()

    def update_data(self):
        values = self.read_signals()
        timestamp = datetime.now().strftime("%H:%M:%S")
        heat, ready, eco, clean, heater1, heater2 = values

        active_signals = []
        for name, val in zip(CHANNELS.keys(), values):
            if name in COLORS and val > THRESHOLD:
                active_signals.append(name)

        self.last_state = self.current_state
        self.current_state = ' + '.join(active_signals) if active_signals else "None"

        duration = int(time.time() - self.state_start_time)
        self.status_label.setText(f"Current State: {self.current_state} | Previous State: {self.last_state}")
        self.duration_label.setText(f"Duration: {duration} sec")
        if self.current_state != self.last_state:
            self.state_start_time = time.time()
            duration = 0

        row = self.table.rowCount()
        self.table.insertRow(row)
        items = [
            timestamp, f"{heat:.2f}", f"{ready:.2f}", f"{eco:.2f}", f"{clean:.2f}",
            f"{heater1:.2f}", f"{heater2:.2f}", self.current_state, self.last_state, str(duration)
        ]
        for i, val in enumerate(items):
            item = QTableWidgetItem(val)
            if i in [1, 2, 3, 4]:
                signal_name = list(CHANNELS.keys())[i - 1]
                if float(val) > THRESHOLD:
                    item.setBackground(COLORS[signal_name])
                    item.setForeground(QColor(255, 255, 255))
            self.table.setItem(row, i, item)

        self.data_log.append(items)

        self.timestamps.append(timestamp)
        self.heater1_data.append(heater1)
        self.heater2_data.append(heater2)
        self.ax.clear()
        self.ax.plot(self.timestamps[-30:], self.heater1_data[-30:], label="Heater1")
        self.ax.plot(self.timestamps[-30:], self.heater2_data[-30:], label="Heater2")
        self.ax.set_title("Live Voltage")
        self.ax.set_ylabel("Voltage (V)")
        self.ax.set_xlabel("Time")
        self.ax.legend()
        self.canvas.draw()

    def reset_data(self):
        self.table.setRowCount(0)
        self.data_log.clear()
        self.timestamps.clear()
        self.heater1_data.clear()
        self.heater2_data.clear()
        self.last_state = "None"
        self.current_state = "None"
        self.state_start_time = time.time()
        self.status_label.setText("Current State: None | Previous State: None")
        self.duration_label.setText("Duration: 0 sec")
        self.ax.clear()
        self.canvas.draw()

    def save_direct(self):
        df = pd.DataFrame(self.data_log, columns=[
            "Time", "Heat", "Ready", "Eco", "Clean",
            "Heater1", "Heater2", "Current State", "Previous State", "Duration"
        ])
        logs_dir = r"D:\logs"
        os.makedirs(logs_dir, exist_ok=True)
        filename = f"heater_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        path = os.path.join(logs_dir, filename)
        df.to_excel(path, index=False)

    def stop_acquisition(self):
        self.timer.stop()
        self.task.stop()
        self.status_label.setText("تم إيقاف القراءة من DAQ")

    def closeEvent(self, event):
        with open("heater_log.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                "Time", "Heat", "Ready", "Eco", "Clean",
                "Heater1", "Heater2", "Current State", "Previous State", "Duration"
            ])
            writer.writerows(self.data_log)
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HeaterTestSystem()
    window.show()
    sys.exit(app.exec_())
