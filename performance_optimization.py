"""
Performance Optimization Module for Heater Monitor System
Addresses memory leaks, stability issues, and continuous operation requirements
"""

import gc
import psutil
import threading
import time
from datetime import datetime, timedelta
from PyQt6.QtCore import QTimer, pyqtSignal, QObject
from PyQt6.QtWidgets import QMessageBox

class PerformanceOptimizer(QObject):
    """Performance optimization and memory management system"""
    
    # Signals for performance monitoring
    memory_usage_updated = pyqtSignal(float)  # MB
    cleanup_performed = pyqtSignal(str)       # cleanup type
    performance_alert = pyqtSignal(str)       # alert message
    
    def __init__(self, parent_app):
        super().__init__()
        self.app = parent_app
        self.process = psutil.Process()
        
        # Performance thresholds
        self.MAX_MEMORY_MB = 500  # Maximum memory usage in MB
        self.MAX_DATA_LOG_SIZE = 10000  # Maximum data log entries
        self.MAX_TABLE_ROWS = 5000  # Maximum table rows
        self.MAX_ERROR_LOG_SIZE = 500  # Maximum error log entries
        self.CLEANUP_INTERVAL = 300  # Cleanup every 5 minutes
        
        # Performance monitoring
        self.last_cleanup = time.time()
        self.performance_stats = {
            'startup_time': time.time(),
            'total_cleanups': 0,
            'memory_peaks': [],
            'data_points_processed': 0
        }
        
        # Setup monitoring timer
        self.monitor_timer = QTimer()
        self.monitor_timer.timeout.connect(self.monitor_performance)
        self.monitor_timer.start(30000)  # Monitor every 30 seconds
        
        # Setup cleanup timer
        self.cleanup_timer = QTimer()
        self.cleanup_timer.timeout.connect(self.perform_periodic_cleanup)
        self.cleanup_timer.start(self.CLEANUP_INTERVAL * 1000)  # Convert to ms
        
        print("🚀 Performance Optimizer initialized")
    
    def get_memory_usage(self):
        """Get current memory usage in MB"""
        try:
            memory_info = self.process.memory_info()
            return memory_info.rss / 1024 / 1024  # Convert to MB
        except Exception:
            return 0.0
    
    def monitor_performance(self):
        """Monitor system performance and trigger alerts if needed"""
        try:
            memory_mb = self.get_memory_usage()
            self.memory_usage_updated.emit(memory_mb)
            
            # Track memory peaks
            self.performance_stats['memory_peaks'].append({
                'timestamp': datetime.now(),
                'memory_mb': memory_mb
            })
            
            # Keep only last 100 memory readings
            if len(self.performance_stats['memory_peaks']) > 100:
                self.performance_stats['memory_peaks'] = self.performance_stats['memory_peaks'][-100:]
            
            # Check for memory threshold
            if memory_mb > self.MAX_MEMORY_MB:
                self.performance_alert.emit(f"High memory usage: {memory_mb:.1f} MB")
                self.force_cleanup()
            
            # Check data log size
            if hasattr(self.app, 'data_log') and len(self.app.data_log) > self.MAX_DATA_LOG_SIZE:
                self.performance_alert.emit(f"Large data log: {len(self.app.data_log)} entries")
                self.cleanup_data_log()
            
            # Check table sizes
            if hasattr(self.app, 'table') and self.app.table.rowCount() > self.MAX_TABLE_ROWS:
                self.performance_alert.emit(f"Large table: {self.app.table.rowCount()} rows")
                self.cleanup_tables()
                
        except Exception as e:
            print(f"Performance monitoring error: {e}")
    
    def perform_periodic_cleanup(self):
        """Perform periodic cleanup to maintain performance"""
        try:
            cleanup_actions = []
            
            # Clean data log
            if hasattr(self.app, 'data_log') and len(self.app.data_log) > self.MAX_DATA_LOG_SIZE // 2:
                self.cleanup_data_log()
                cleanup_actions.append("data_log")
            
            # Clean tables
            if hasattr(self.app, 'table') and self.app.table.rowCount() > self.MAX_TABLE_ROWS // 2:
                self.cleanup_tables()
                cleanup_actions.append("tables")
            
            # Clean error logs
            if hasattr(self.app, 'error_log') and len(self.app.error_log) > self.MAX_ERROR_LOG_SIZE:
                self.cleanup_error_logs()
                cleanup_actions.append("error_logs")
            
            # Force garbage collection
            gc.collect()
            cleanup_actions.append("garbage_collection")
            
            if cleanup_actions:
                self.performance_stats['total_cleanups'] += 1
                self.cleanup_performed.emit(", ".join(cleanup_actions))
                print(f"🧹 Periodic cleanup performed: {', '.join(cleanup_actions)}")
            
            self.last_cleanup = time.time()
            
        except Exception as e:
            print(f"Periodic cleanup error: {e}")
    
    def cleanup_data_log(self):
        """Clean up data log to prevent memory bloat"""
        try:
            if hasattr(self.app, 'data_log') and len(self.app.data_log) > 1000:
                # Keep only last 70% of data
                keep_size = int(len(self.app.data_log) * 0.7)
                removed_count = len(self.app.data_log) - keep_size
                self.app.data_log = self.app.data_log[-keep_size:]
                print(f"🗑️ Cleaned data log: removed {removed_count} entries, kept {keep_size}")
                
        except Exception as e:
            print(f"Data log cleanup error: {e}")
    
    def cleanup_tables(self):
        """Clean up table rows to improve performance"""
        try:
            # Clean main table
            if hasattr(self.app, 'table') and self.app.table.rowCount() > 1000:
                keep_rows = 1000
                total_rows = self.app.table.rowCount()
                remove_rows = total_rows - keep_rows
                
                # Remove oldest rows (from top)
                for i in range(remove_rows):
                    self.app.table.removeRow(0)
                
                print(f"🗑️ Cleaned main table: removed {remove_rows} rows, kept {keep_rows}")
            
            # Clean TTL table
            if hasattr(self.app, 'ttl_table') and self.app.ttl_table.rowCount() > 1000:
                keep_rows = 1000
                total_rows = self.app.ttl_table.rowCount()
                remove_rows = total_rows - keep_rows
                
                # Remove oldest rows (from top)
                for i in range(remove_rows):
                    self.app.ttl_table.removeRow(0)
                
                print(f"🗑️ Cleaned TTL table: removed {remove_rows} rows, kept {keep_rows}")
                
        except Exception as e:
            print(f"Table cleanup error: {e}")
    
    def cleanup_error_logs(self):
        """Clean up error logs to prevent memory bloat"""
        try:
            if hasattr(self.app, 'error_log') and len(self.app.error_log) > self.MAX_ERROR_LOG_SIZE:
                # Keep only last 50% of errors
                keep_size = self.MAX_ERROR_LOG_SIZE // 2
                removed_count = len(self.app.error_log) - keep_size
                self.app.error_log = self.app.error_log[-keep_size:]
                print(f"🗑️ Cleaned error log: removed {removed_count} entries, kept {keep_size}")
                
        except Exception as e:
            print(f"Error log cleanup error: {e}")
    
    def force_cleanup(self):
        """Force immediate cleanup when memory is high"""
        try:
            print("🚨 Force cleanup triggered due to high memory usage")
            
            # Aggressive data log cleanup
            if hasattr(self.app, 'data_log') and len(self.app.data_log) > 500:
                keep_size = 500
                self.app.data_log = self.app.data_log[-keep_size:]
                print(f"🗑️ Force cleaned data log: kept only {keep_size} entries")
            
            # Aggressive table cleanup
            if hasattr(self.app, 'table') and self.app.table.rowCount() > 500:
                # Remove older rows
                current_rows = self.app.table.rowCount()
                keep_rows = 500
                remove_rows = current_rows - keep_rows
                for i in range(remove_rows):
                    self.app.table.removeRow(0)
                print(f"🗑️ Force cleaned main table: removed {remove_rows} rows")
            
            if hasattr(self.app, 'ttl_table') and self.app.ttl_table.rowCount() > 500:
                # Remove older rows
                current_rows = self.app.ttl_table.rowCount()
                keep_rows = 500
                remove_rows = current_rows - keep_rows
                for i in range(remove_rows):
                    self.app.ttl_table.removeRow(0)
                print(f"🗑️ Force cleaned TTL table: removed {remove_rows} rows")
            
            # Clear chart data if too large
            if hasattr(self.app, 'timestamps') and len(self.app.timestamps) > 200:
                keep_size = 200
                self.app.timestamps = self.app.timestamps[-keep_size:]
                self.app.heater1_data = self.app.heater1_data[-keep_size:]
                self.app.heater2_data = self.app.heater2_data[-keep_size:]
                print(f"🗑️ Force cleaned chart data: kept only {keep_size} points")
            
            # Force garbage collection
            gc.collect()
            
        except Exception as e:
            print(f"Force cleanup error: {e}")
    
    def get_performance_report(self):
        """Generate performance report"""
        try:
            uptime = time.time() - self.performance_stats['startup_time']
            uptime_hours = uptime / 3600
            
            memory_mb = self.get_memory_usage()
            
            # Calculate average memory usage
            if self.performance_stats['memory_peaks']:
                avg_memory = sum(p['memory_mb'] for p in self.performance_stats['memory_peaks']) / len(self.performance_stats['memory_peaks'])
                max_memory = max(p['memory_mb'] for p in self.performance_stats['memory_peaks'])
            else:
                avg_memory = memory_mb
                max_memory = memory_mb
            
            report = f"""
📊 PERFORMANCE REPORT
{'='*50}

🕐 System Uptime: {uptime_hours:.1f} hours
💾 Current Memory: {memory_mb:.1f} MB
📈 Average Memory: {avg_memory:.1f} MB
🔝 Peak Memory: {max_memory:.1f} MB

🧹 Total Cleanups: {self.performance_stats['total_cleanups']}
📊 Data Log Size: {len(getattr(self.app, 'data_log', []))} entries
📋 Main Table Rows: {getattr(self.app.table, 'rowCount', lambda: 0)() if hasattr(self.app, 'table') else 0}
📋 TTL Table Rows: {getattr(self.app.ttl_table, 'rowCount', lambda: 0)() if hasattr(self.app, 'ttl_table') else 0}
🔢 Chart Points: {len(getattr(self.app, 'timestamps', []))}

🎯 Memory Efficiency: {((self.MAX_MEMORY_MB - memory_mb) / self.MAX_MEMORY_MB * 100):.1f}%
✅ System Status: {'OPTIMAL' if memory_mb < self.MAX_MEMORY_MB * 0.7 else 'WARNING' if memory_mb < self.MAX_MEMORY_MB else 'CRITICAL'}

📝 Recommendations:
- Keep system running with automatic cleanup
- Monitor memory usage regularly
- Use reset data function periodically
- Consider reducing update rate if needed
"""
            return report
            
        except Exception as e:
            return f"Error generating performance report: {e}"


class ChartOptimizer:
    """Optimized chart rendering for better performance"""
    
    def __init__(self, app):
        self.app = app
        self.last_redraw = 0
        self.redraw_interval = 2.0  # Minimum 2 seconds between full redraws
        self.partial_update_count = 0
        self.last_data_hash = None  # Track data changes
        self.skip_count = 0
        self.max_skips = 3  # Skip 3 updates before forcing redraw
        self.chart_dirty = False
        self.data_points_limit = 200  # Reduced from 300 for better performance
        
    def should_full_redraw(self):
        """Determine if full chart redraw is needed with intelligent skipping"""
        current_time = time.time()
        
        # Check if enough time has passed
        time_passed = current_time - self.last_redraw > self.redraw_interval
        
        # Check if data has actually changed
        data_changed = self.has_data_changed()
        
        # Force redraw if we've skipped too many updates
        force_redraw = self.skip_count >= self.max_skips
        
        if (time_passed and data_changed) or force_redraw:
            self.last_redraw = current_time
            self.partial_update_count = 0
            self.skip_count = 0
            self.chart_dirty = False
            return True
        elif not data_changed:
            # Data hasn't changed, skip this update
            return False
        else:
            # Data changed but not enough time passed, count as skip
            self.skip_count += 1
            return False
    
    def has_data_changed(self):
        """Check if chart data has actually changed"""
        try:
            if not hasattr(self.app, 'timestamps') or not self.app.timestamps:
                return False
            
            # Create a simple hash of the last few data points
            if len(self.app.timestamps) > 0:
                last_timestamp = self.app.timestamps[-1]
                last_temp1 = self.app.heater1_data[-1] if self.app.heater1_data else 0
                last_temp2 = self.app.heater2_data[-1] if self.app.heater2_data else 0
                
                # Simple hash of recent data
                current_hash = hash((str(last_timestamp), last_temp1, last_temp2))
                
                if self.last_data_hash != current_hash:
                    self.last_data_hash = current_hash
                    return True
            
            return False
        except Exception:
            return True  # If error, assume data changed
    
    def get_optimized_data_points(self):
        """Get optimized data points for plotting"""
        try:
            if not hasattr(self.app, 'timestamps') or len(self.app.timestamps) == 0:
                return [], [], []
            
            timestamps = self.app.timestamps
            heater1_data = self.app.heater1_data
            heater2_data = self.app.heater2_data
            
            # If data is within limit, return as is
            if len(timestamps) <= self.data_points_limit:
                return timestamps, heater1_data, heater2_data
            
            # Intelligent downsampling - keep recent data dense, older data sparse
            total_points = len(timestamps)
            keep_recent = self.data_points_limit // 2  # Keep half as recent data
            keep_older = self.data_points_limit - keep_recent  # Downsample the rest
            
            # Recent data (keep all)
            recent_timestamps = timestamps[-keep_recent:]
            recent_heater1 = heater1_data[-keep_recent:]
            recent_heater2 = heater2_data[-keep_recent:]
            
            # Older data (downsample)
            if total_points > keep_recent:
                older_data_size = total_points - keep_recent
                step = max(1, older_data_size // keep_older)
                
                older_timestamps = timestamps[:-keep_recent:step]
                older_heater1 = heater1_data[:-keep_recent:step]
                older_heater2 = heater2_data[:-keep_recent:step]
                
                # Ensure older data doesn't exceed limit
                if len(older_timestamps) > keep_older:
                    older_timestamps = older_timestamps[-keep_older:]
                    older_heater1 = older_heater1[-keep_older:]
                    older_heater2 = older_heater2[-keep_older:]
                
                # Combine older and recent data
                plot_timestamps = older_timestamps + recent_timestamps
                plot_heater1 = older_heater1 + recent_heater1
                plot_heater2 = older_heater2 + recent_heater2
                
                # Final safety check - ensure we don't exceed limit
                if len(plot_timestamps) > self.data_points_limit:
                    excess = len(plot_timestamps) - self.data_points_limit
                    plot_timestamps = plot_timestamps[excess:]
                    plot_heater1 = plot_heater1[excess:]
                    plot_heater2 = plot_heater2[excess:]
            else:
                plot_timestamps = recent_timestamps
                plot_heater1 = recent_heater1
                plot_heater2 = recent_heater2
            
            return plot_timestamps, plot_heater1, plot_heater2
            
        except Exception as e:
            print(f"Data optimization error: {e}")
            return self.app.timestamps, self.app.heater1_data, self.app.heater2_data
    
    def optimized_chart_update(self):
        """Highly optimized chart update with aggressive performance improvements"""
        try:
            # Quick exit if no data
            if not hasattr(self.app, 'timestamps') or len(self.app.timestamps) == 0:
                return
            
            # Check if we need to redraw
            if not self.should_full_redraw():
                # Skip this update - no changes or too frequent
                return
            
            # Get optimized data points
            plot_timestamps, plot_heater1, plot_heater2 = self.get_optimized_data_points()
            
            if len(plot_timestamps) == 0:
                return
            
            # Clear and redraw with optimized settings
            self.app.ax.clear()
            
            # Use faster plotting methods
            # Plot with minimal styling for performance
            line1 = self.app.ax.plot(plot_timestamps, plot_heater1, 
                           label="Water Temp", color="#0066CC", 
                           linewidth=1.5, alpha=0.9,
                           rasterized=True)  # Rasterize for performance
            
            line2 = self.app.ax.plot(plot_timestamps, plot_heater2, 
                           label="Target Temp", color="#FF6600", 
                           linewidth=1.5, alpha=0.9, linestyle='--',
                           rasterized=True)  # Rasterize for performance
            
            # Minimal essential styling only
            self.app.ax.set_title("Live Temperature Monitoring", 
                                color="#FFFFFF", fontsize=10, pad=5)
            self.app.ax.set_ylabel("Temperature (°C)", color="#FFFFFF", fontsize=9)
            self.app.ax.set_xlabel("Time", color="#FFFFFF", fontsize=9)
            
            # Optimized grid
            self.app.ax.grid(True, alpha=0.3, linewidth=0.5, color='#666666')
            self.app.ax.set_facecolor('#1a1a1a')
            self.app.ax.set_ylim(0, 100)
            
            # Simplified legend
            legend = self.app.ax.legend(fontsize=8, loc='upper right', 
                                       framealpha=0.8, fancybox=False, shadow=False)
            legend.get_frame().set_facecolor('#2a2a2a')
            for text in legend.get_texts():
                text.set_color('#FFFFFF')
            
            # Optimized time formatting - less frequent updates
            if len(plot_timestamps) > 5:
                import matplotlib.dates as mdates
                self.app.ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
                self.app.ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=5))
            
            # Optimized tick parameters
            self.app.ax.tick_params(axis='x', rotation=15, colors='#FFFFFF', 
                                   labelsize=7, width=0.5, length=2)
            self.app.ax.tick_params(axis='y', colors='#FFFFFF', 
                                   labelsize=7, width=0.5, length=2)
            
            # Remove expensive elements for performance
            # No fill_between, no annotations, no reference lines
            
            # Optimized layout
            self.app.canvas.figure.tight_layout(pad=0.5)
            
            # Set spine styling efficiently
            for spine in self.app.ax.spines.values():
                spine.set_color('#555555')
                spine.set_linewidth(0.5)
            
            # Use efficient draw method
            self.app.canvas.draw_idle()  # More efficient than draw()
            
            print(f"Chart updated with {len(plot_timestamps)} points (optimized from {len(self.app.timestamps)})")
            
        except Exception as e:
            print(f"Optimized chart update error: {e}")
            # Fallback to basic update
            self.basic_chart_update()
    
    def basic_chart_update(self):
        """Basic fallback chart update method"""
        try:
            self.app.ax.clear()
            
            if len(self.app.timestamps) > 0:
                # Use only last 50 points for emergency fallback
                recent_timestamps = self.app.timestamps[-50:]
                recent_heater1 = self.app.heater1_data[-50:]
                recent_heater2 = self.app.heater2_data[-50:]
                
                self.app.ax.plot(recent_timestamps, recent_heater1, 'b-', linewidth=1)
                self.app.ax.plot(recent_timestamps, recent_heater2, 'r--', linewidth=1)
                
                self.app.ax.set_title("Temperature (Emergency Mode)", color="#FFFFFF")
                self.app.ax.set_facecolor('#1a1a1a')
                self.app.ax.grid(True, alpha=0.3)
            
            self.app.canvas.draw_idle()
            
        except Exception as e:
            print(f"Basic chart update error: {e}")


class AutoSaveManager:
    """Automatic data saving for reliability"""
    
    def __init__(self, app):
        self.app = app
        self.auto_save_interval = 600  # Auto-save every 10 minutes
        
        # Setup auto-save timer
        self.auto_save_timer = QTimer()
        self.auto_save_timer.timeout.connect(self.auto_save_data)
        self.auto_save_timer.start(self.auto_save_interval * 1000)
        
        print("💾 Auto-save manager initialized")
    
    def auto_save_data(self):
        """Automatically save data to prevent loss"""
        try:
            if hasattr(self.app, 'data_log') and len(self.app.data_log) > 0:
                # Save to auto-save file
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                auto_save_path = f"logs/auto_save_{timestamp}.xlsx"
                
<<<<<<< HEAD
                # Create logs directory if it doesn't exist
                import os
                os.makedirs("logs", exist_ok=True)
                
                # Save data directly to auto-save file
                import pandas as pd
                
                # Create enhanced data for export
                export_data = []
                for row_data in self.app.data_log:
                    enhanced_row = list(row_data)
                    
                    # Convert lamp status to readable text
                    if len(enhanced_row) >= 15:
                        if hasattr(self.app, 'convert_lamp_status_to_text'):
                            enhanced_row[13] = self.app.convert_lamp_status_to_text(enhanced_row[13])
                            enhanced_row[14] = self.app.convert_lamp_status_to_text(enhanced_row[14])
                    
                    export_data.append(enhanced_row)
                
                # Create DataFrame
                columns = [
                    "Time", "Mode", "Heater", "Water Temp", "Target Temp", "Clean Mode", "Clean Hours", "Clean 3Min",
                    "Eco Mode", "Heat LED", "Ready LED", "Eco LED", "Clean LED", "Current State", "Previous State", "Duration",
                    "Heater State", "Heater Cmd", "Clean Mode Automation"
                ]
                df = pd.DataFrame(export_data)
                if len(df.columns) == len(columns):
                    df.columns = columns
                
                # Save to Excel
                df.to_excel(auto_save_path, index=False, engine='openpyxl')
                
                print(f"💾 Auto-save completed: {auto_save_path}")
                return auto_save_path
                
        except Exception as e:
            print(f"Auto-save error: {e}")
            return None
=======
                saved_path = self.app.save_direct()
                if saved_path:
                    print(f"💾 Auto-save completed: {saved_path}")
                
        except Exception as e:
            print(f"Auto-save error: {e}")
>>>>>>> 24a22cb66b502c59f5581b1d6de7b48f98ae3756


# Performance monitoring functions
def get_system_info():
    """Get comprehensive system information"""
    try:
        import platform
        
        info = {
            'os': platform.system(),
            'os_version': platform.version(),
            'python_version': platform.python_version(),
            'cpu_count': psutil.cpu_count(),
            'total_memory_gb': psutil.virtual_memory().total / (1024**3),
            'available_memory_gb': psutil.virtual_memory().available / (1024**3),
            'cpu_percent': psutil.cpu_percent(interval=1),
        }
        
        return info
    except Exception as e:
        return {'error': str(e)}

def optimize_matplotlib():
    """Optimize matplotlib for better performance"""
    try:
        import matplotlib
        matplotlib.use('Qt5Agg')  # Use Qt5Agg backend for compatibility
        
        # Optimize matplotlib settings
        import matplotlib.pyplot as plt
        plt.ioff()  # Turn off interactive mode
        
        # Reduce memory usage
        matplotlib.rcParams['figure.max_open_warning'] = 1
        matplotlib.rcParams['agg.path.chunksize'] = 1000
        
        print("📈 Matplotlib optimized for performance")
        
    except Exception as e:
        print(f"Matplotlib optimization error: {e}")

def check_dependencies():
    """Check if all dependencies are properly installed"""
    try:
        dependencies = {
            'PyQt6': 'PyQt6',
            'matplotlib': 'matplotlib', 
            'pandas': 'pandas',
            'psutil': 'psutil',
            'openpyxl': 'openpyxl',
            'serial': 'pyserial'
        }
        
        results = {}
        for name, package in dependencies.items():
            try:
                __import__(name)
                results[package] = "✅ OK"
            except ImportError:
                results[package] = "❌ Missing"
        
        return results
        
    except Exception as e:
        return {'error': str(e)}