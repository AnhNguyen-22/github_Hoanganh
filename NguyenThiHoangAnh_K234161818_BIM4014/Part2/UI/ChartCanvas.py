# UI/ChartCanvas.py
try:
    from matplotlib.backends.backend_qt6agg import FigureCanvasQTAgg as FigureCanvas
except ImportError:
    # Fallback cho PyQt5 hoặc các phiên bản cũ
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import pandas as pd
from datetime import datetime, date

class ChartCanvas(FigureCanvas):
    """Canvas để nhúng biểu đồ matplotlib vào PyQt."""

    def __init__(self, parent=None, width=6, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax = self.fig.add_subplot(111)
        super().__init__(self.fig)
        self.setParent(parent)
        # Ẩn axes khi khởi tạo
        self.ax.axis('off')
        self.ax.text(0.5, 0.5, 'Chọn một chức năng để xem biểu đồ', 
                     ha='center', va='center', fontsize=14, 
                     color='gray', transform=self.ax.transAxes)
        self.draw()

    def clear(self):
        """Xoá nội dung biểu đồ và hiển thị message placeholder."""
        self.ax.clear()
        self.ax.axis('off')
        self.ax.text(0.5, 0.5, 'Chọn một chức năng để xem biểu đồ', 
                     ha='center', va='center', fontsize=14, 
                     color='gray', transform=self.ax.transAxes)
        self.draw()

    def plot_bar(self, x, y, title="", color="#D6A99D", rotation=0, ha="center"):
        """Vẽ biểu đồ cột."""
        self.ax.clear()
        self.ax.axis('on')  # Bật lại axes khi vẽ biểu đồ
        labels = list(x)
        values = list(y)
        indices = range(len(labels))
        self.ax.bar(indices, values, color=color)
        self.ax.set_title(title)
        self.ax.set_xlabel(x.name if hasattr(x, "name") else "X")
        self.ax.set_ylabel(y.name if hasattr(y, "name") else "Y")
        self.ax.set_xticks(indices)
        self.ax.set_xticklabels(labels, rotation=rotation, ha=ha)
        self.ax.margins(x=0.01)
        self.ax.grid(axis="y", alpha=0.2)
        self.fig.tight_layout()
        self.draw()

    def plot_line(self, x, y, title="", color="#9CAFAA", marker="o", rotation=0):
        """Vẽ biểu đồ đường."""
        self.ax.clear()
        self.ax.axis('on')  # Bật lại axes khi vẽ biểu đồ
        labels = list(x)
        values = list(y)
        series_name = y.name if hasattr(y, "name") else "Y"
        is_datetime = False
        if hasattr(x, "dtype") and getattr(x.dtype, "kind", "") == "M":
            is_datetime = True
        elif isinstance(x, pd.DatetimeIndex):
            is_datetime = True
        elif labels and isinstance(labels[0], (pd.Timestamp, datetime, date)):
            is_datetime = True

        if is_datetime:
            idx = pd.to_datetime(labels)
            self.ax.plot(idx, values, color=color, marker=marker)
            self.fig.autofmt_xdate(rotation if rotation else 30)
        else:
            indices = range(len(labels))
            self.ax.plot(indices, values, color=color, marker=marker)
            self.ax.set_xticks(indices)
            self.ax.set_xticklabels(labels, rotation=rotation or 45, ha="right")
        self.ax.set_title(title)
        self.ax.set_xlabel(x.name if hasattr(x, "name") else "X")
        self.ax.set_ylabel(series_name)
        self.ax.grid(alpha=0.3)
        self.fig.tight_layout()
        self.draw()

    def plot_multi_line(self, df, title=""):
        """
        Vẽ nhiều đường (mỗi cột là một series).
        df: DataFrame với index làm trục X (datetime hoặc số), mỗi cột là category.
        """
        self.ax.clear()
        self.ax.axis('on')  # Bật lại axes khi vẽ biểu đồ
        for col in df.columns:
            self.ax.plot(df.index, df[col], marker="o", label=col)
        self.ax.set_title(title)
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Revenue")
        if df.index.dtype.kind == "M":
            self.fig.autofmt_xdate()
        else:
            self.ax.tick_params(axis="x", rotation=45)
        self.ax.grid(alpha=0.3)
        self.ax.legend()
        self.fig.tight_layout()
        self.draw()

    def plot_elbow(self, k_values, inertias, title="Elbow Method"):
        """Vẽ biểu đồ elbow method để chọn số cluster K."""
        self.ax.clear()
        self.ax.axis('on')
        self.ax.plot(k_values, inertias, "o", color="#9CAFAA", markersize=8)
        self.ax.plot(k_values, inertias, "-", color="#9CAFAA", alpha=0.6, linewidth=2)
        self.ax.set_xlabel("Number of Clusters (k)")
        self.ax.set_ylabel("Cluster Sum of Squared Distances (Inertia)")
        self.ax.set_title(title)
        self.ax.grid(alpha=0.3)
        self.ax.set_xticks(k_values)
        self.fig.tight_layout()
        self.draw()

    def plot_cluster_2d(self, df, x_col, y_col, cluster_col="Cluster", title="Customer Clusters", palette=None):
        """
        Vẽ biểu đồ scatter 2D với màu theo cluster.
        df: DataFrame chứa dữ liệu
        x_col, y_col: tên cột cho trục X và Y
        cluster_col: tên cột chứa cluster ID
        palette: danh sách màu cho các cluster
        """
        import numpy as np
        
        if palette is None:
            palette = ["#D6A99D", "#9CAFAA", "#D6DAC8", "#FBF3D5", "#8aa0a0", "#d9b8b0", "#c6d1c6"]
        
        self.ax.clear()
        self.ax.axis('on')
        
        # Lấy danh sách các cluster unique
        clusters = sorted(df[cluster_col].unique())
        
        # Vẽ từng cluster với màu riêng
        for i, cluster_id in enumerate(clusters):
            cluster_data = df[df[cluster_col] == cluster_id]
            color = palette[i % len(palette)]
            self.ax.scatter(
                cluster_data[x_col],
                cluster_data[y_col],
                c=color,
                label=f'Cluster {cluster_id}',
                s=80,
                edgecolors='white',
                linewidths=0.4,
                alpha=0.8
            )
        
        self.ax.set_xlabel(x_col)
        self.ax.set_ylabel(y_col)
        self.ax.set_title(title)
        self.ax.grid(alpha=0.3)
        self.ax.legend(loc='best')
        self.fig.tight_layout()
        self.draw()

    def plot_forecast(self, df, time_col="TimeIndex", actual_col="Revenue", pred_col="Predicted", title="Revenue Trend Forecast"):
        """
        Vẽ biểu đồ forecast: Actual vs Predicted
        df: DataFrame chứa dữ liệu với các cột time_col, actual_col, pred_col
        """
        self.ax.clear()
        self.ax.axis('on')
        
        # Vẽ Actual
        self.ax.plot(df[time_col], df[actual_col], 
                    label="Actual", color="#D6A99D", marker="o", linewidth=2, markersize=6)
        
        # Vẽ Predicted
        self.ax.plot(df[time_col], df[pred_col], 
                    label="Predicted", color="#9CAFAA", marker="o", linewidth=2, markersize=6)
        
        self.ax.set_xlabel("Time (months)")
        self.ax.set_ylabel("Revenue")
        self.ax.set_title(title)
        self.ax.grid(alpha=0.3)
        self.ax.legend(loc='best')
        self.fig.tight_layout()
        self.draw()

    def plot_forecast_future(self, df_actual, df_future, time_col="TimeIndex", revenue_col="Revenue", 
                            forecast_col="Forecast", title="Next Months Forecast"):
        """
        Vẽ biểu đồ forecast với dữ liệu tương lai
        df_actual: DataFrame chứa dữ liệu thực tế (có cột time_col, revenue_col)
        df_future: DataFrame chứa dự báo tương lai (có cột time_col, forecast_col)
        """
        self.ax.clear()
        self.ax.axis('on')
        
        # Vẽ Actual
        self.ax.plot(df_actual[time_col], df_actual[revenue_col], 
                    label="Actual", color="#D6A99D", marker="o", linewidth=2, markersize=6)
        
        # Vẽ Forecast
        self.ax.plot(df_future[time_col], df_future[forecast_col], 
                    label="Forecast", color="#9CAFAA", marker="o", linewidth=2, markersize=6, linestyle='--')
        
        # Vẽ đường nối giữa actual và forecast
        if len(df_actual) > 0 and len(df_future) > 0:
            last_actual_time = df_actual[time_col].iloc[-1]
            last_actual_revenue = df_actual[revenue_col].iloc[-1]
            first_future_time = df_future[time_col].iloc[0]
            first_future_forecast = df_future[forecast_col].iloc[0]
            
            # Vẽ đường nối
            self.ax.plot([last_actual_time, first_future_time], 
                        [last_actual_revenue, first_future_forecast],
                        color="#9CAFAA", linestyle='--', alpha=0.5, linewidth=1)
        
        self.ax.set_xlabel("Time (months)")
        self.ax.set_ylabel("Revenue")
        self.ax.set_title(title)
        self.ax.grid(alpha=0.3)
        self.ax.legend(loc='best')
        self.fig.tight_layout()
        self.draw()
