import sys
import csv
import time
import os
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QLabel, QPushButton, QHBoxLayout, QHeaderView, QSplitter, QStyleFactory, QAbstractItemView
)
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QColor, QBrush, QPalette, QFont
import nidaqmx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib import dates as mdates
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
LOGS_DIR = os.path.join(os.path.dirname(__file__), "logs")
SYNC_COLUMNS = ['Heat', 'Ready', 'Eco', 'Clean', 'Heater1', 'Heater2']
ALL_FIVE_MIN = 4.5
ALL_FIVE_MAX = 5.0
ALL_ZERO_MIN = 0.0
ALL_ZERO_MAX = 0.44

class HeaterTestSystem(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Heater Test System")
        self.resize(1200, 750)

        # Theme: Fusion dark
        QApplication.setStyle(QStyleFactory.create("Fusion"))
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Base, QColor(35, 35, 35))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
        palette.setColor(QPalette.ColorRole.Highlight, QColor(142, 45, 197).lighter())
        palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.black)
        self.setPalette(palette)
        self.setFont(QFont("Segoe UI", 10))

        self.task = nidaqmx.Task()
        for ch in CHANNELS.values():
            self.task.ai_channels.add_ai_voltage_chan(f"{DEVICE_NAME}/{ch}")
        self.task.start()

        self.layout = QVBoxLayout()
        self.status_label = QLabel("Current State: None | Previous State: None")
        self.duration_label = QLabel("Duration: 0 sec")
        self.table = QTableWidget(0, 12)
        self.table.setHorizontalHeaderLabels([
            "Time", "Heat", "Ready", "Eco", "Clean",
            "Heater1", "Heater2", "Current State", "Previous State", "Duration",
            "All5 Count", "All0 Count"
        ])
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        header.setHighlightSections(False)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.table.setFont(QFont("Segoe UI", 10))
        self.table.setStyleSheet("QTableWidget{gridline-color:#666;} QHeaderView::section{background:#1f1f1f;color:white;padding:6px;border:0;} QTableWidget{color:white;} ")

        # Buttons
        self.save_button = QPushButton("Save")
        self.stop_button = QPushButton("Stop")
        self.reset_button = QPushButton("Reset")
        self.save_button.clicked.connect(self.save_direct)
        self.stop_button.clicked.connect(self.stop_acquisition)
        self.reset_button.clicked.connect(self.reset_data)

        # Chart canvas and data holders
        self.canvas = FigureCanvas(plt.Figure(facecolor="#2b2b2b"))
        self.ax = self.canvas.figure.add_subplot(111)
        self.timestamps = []
        self.heater1_data = []
        self.heater2_data = []

        # Top labels
        self.layout.addWidget(self.status_label)
        self.layout.addWidget(self.duration_label)

        # Splitter with table and chart (chart larger)
        splitter = QSplitter(Qt.Orientation.Vertical)
        splitter.addWidget(self.table)
        splitter.addWidget(self.canvas)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)
        splitter.setSizes([500, 700])
        self.layout.addWidget(splitter)

        # Buttons row
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.save_button)
        btn_layout.addWidget(self.stop_button)
        btn_layout.addWidget(self.reset_button)
        self.layout.addLayout(btn_layout)
        self.setLayout(self.layout)

        self.last_state = "None"
        self.current_state = "None"
        self.state_start_time = time.time()
        self.data_log = []
        self.all_five_count = 0
        self.all_zero_count = 0
        os.makedirs(LOGS_DIR, exist_ok=True)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(1000)

    def read_signals(self):
        try:
            return self.task.read()
        except Exception as e:
            print(f"DAQ read error: {e}")
            return [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

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

        if self.current_state != self.last_state:
            self.state_start_time = time.time()
        duration = int(time.time() - self.state_start_time)
        self.status_label.setText(f"Current State: {self.current_state} | Previous State: {self.last_state}")
        self.duration_label.setText(f"Duration: {duration} sec")

        # تحقق من تزامن قراءات 5V و0V لجميع الأعمدة المحددة
        channel_names = list(CHANNELS.keys())
        selected_values = [val for name, val in zip(channel_names, values) if name in SYNC_COLUMNS]
        if selected_values:
            if all(ALL_FIVE_MIN <= v <= ALL_FIVE_MAX for v in selected_values):
                self.all_five_count += 1
            if all(ALL_ZERO_MIN <= v <= ALL_ZERO_MAX for v in selected_values):
                self.all_zero_count += 1

        row = self.table.rowCount()
        self.table.insertRow(row)
        items = [
            timestamp, f"{heat:.2f}", f"{ready:.2f}", f"{eco:.2f}", f"{clean:.2f}",
            f"{heater1:.2f}", f"{heater2:.2f}", self.current_state, self.last_state, str(duration),
            str(self.all_five_count), str(self.all_zero_count)
        ]
        for i, val in enumerate(items):
            item = QTableWidgetItem(val)
            if i in [1, 2, 3, 4]:
                signal_name = list(CHANNELS.keys())[i - 1]
                if float(val) > THRESHOLD:
                    item.setBackground(QBrush(COLORS[signal_name]))
                    item.setForeground(QBrush(QColor(255, 255, 255)))
            self.table.setItem(row, i, item)
        # auto-scroll to bottom
        self.table.scrollToBottom()

        self.data_log.append(items)

        self.timestamps.append(datetime.now())
        self.heater1_data.append(heater1)
        self.heater2_data.append(heater2)
        # keep last 200 points for smooth plotting
        self.timestamps = self.timestamps[-200:]
        self.heater1_data = self.heater1_data[-200:]
        self.heater2_data = self.heater2_data[-200:]
        self.ax.clear()
        self.ax.plot(self.timestamps, self.heater1_data, label="Heater1", color="#4FC3F7", linewidth=2.2)
        self.ax.plot(self.timestamps, self.heater2_data, label="Heater2", color="#FFB74D", linewidth=2.2)
        self.ax.fill_between(self.timestamps, self.heater1_data, color="#4FC3F7", alpha=0.10)
        self.ax.fill_between(self.timestamps, self.heater2_data, color="#FFB74D", alpha=0.10)
        self.ax.set_title("Live Voltage", color="w", fontsize=12, pad=12)
        self.ax.set_ylabel("Voltage (V)", color="w")
        self.ax.set_xlabel("Time", color="w")
        self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
        self.ax.xaxis.set_major_locator(mdates.AutoDateLocator(minticks=4, maxticks=8))
        self.ax.tick_params(axis='x', rotation=20, colors='w')
        self.ax.tick_params(axis='y', colors='w')
        self.ax.grid(True, color="#444", linestyle=":", linewidth=0.7)
        leg = self.ax.legend(facecolor="#232323", edgecolor="#555")
        for text in leg.get_texts():
            text.set_color('w')
        self.canvas.figure.tight_layout()
        self.canvas.draw()

    def reset_data(self):
        self.table.setRowCount(0)
        self.data_log.clear()
        self.timestamps.clear()
        self.heater1_data.clear()
        self.heater2_data.clear()
        self.all_five_count = 0
        self.all_zero_count = 0
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
            "Heater1", "Heater2", "Current State", "Previous State", "Duration",
            "All5 Count", "All0 Count"
        ])
        os.makedirs(LOGS_DIR, exist_ok=True)
        filename = f"heater_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        path = os.path.join(LOGS_DIR, filename)
        df.to_excel(path, index=False)
        return path

    def stop_acquisition(self):
        self.timer.stop()
        try:
            self.task.stop()
        except Exception:
            pass
        try:
            self.task.close()
        except Exception:
            pass
        try:
            saved_path = self.save_direct()
            self.status_label.setText(f"تم الإيقاف وتم حفظ الملف: {saved_path}")
        except Exception as e:
            self.status_label.setText(f"تم الإيقاف ولكن حدث خطأ أثناء الحفظ: {e}")

    def closeEvent(self, event):
        os.makedirs(LOGS_DIR, exist_ok=True)
        csv_path = os.path.join(LOGS_DIR, "heater_log.csv")
        with open(csv_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                "Time", "Heat", "Ready", "Eco", "Clean",
                "Heater1", "Heater2", "Current State", "Previous State", "Duration",
                "All5 Count", "All0 Count"
            ])
            writer.writerows(self.data_log)
        try:
            self.task.close()
        except Exception:
            pass
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HeaterTestSystem()
    window.show()
    sys.exit(app.exec())
