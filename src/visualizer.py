"""
Module Visualizer
Chứa các hàm vẽ biểu đồ
"""

import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt


class Visualizer:
    """Lớp xử lý vẽ biểu đồ"""
    
    def __init__(self, parent_window):
        self.parent = parent_window
    
    def show_visualization_popup(self, df):
        """Hiển thị popup chọn cột để vẽ biểu đồ"""
        if df.empty:
            return
        
        popup = tk.Toplevel(self.parent)
        popup.title("Cấu hình Biểu đồ")
        popup.geometry("300x200")
        
        tk.Label(popup, text="Chọn cột Trục X (Tên/Danh mục):").pack(pady=5)
        col_x = ttk.Combobox(popup, values=list(df.columns))
        col_x.pack()
        
        tk.Label(popup, text="Chọn cột Trục Y (Giá trị số):").pack(pady=5)
        # Chỉ lấy các cột số
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        col_y = ttk.Combobox(popup, values=numeric_cols)
        col_y.pack()
        
        def plot():
            x_val = col_x.get()
            y_val = col_y.get()
            if x_val and y_val:
                self.plot_chart(df, x_val, y_val)
                popup.destroy()
        
        tk.Button(
            popup, 
            text="Vẽ ngay", 
            bg="purple", 
            fg="white", 
            command=plot
        ).pack(pady=15)
    
    @staticmethod
    def plot_chart(df, x_col, y_col):
        """Vẽ biểu đồ Bar Chart"""
        # Gom nhóm dữ liệu nếu trục X bị trùng lặp
        chart_data = df.groupby(x_col)[y_col].sum().reset_index()
        
        plt.figure(figsize=(8, 5))
        plt.bar(chart_data[x_col].astype(str), chart_data[y_col], color='#4CAF50')
        plt.xlabel(x_col)
        plt.ylabel(y_col)
        plt.title(f"Biểu đồ {y_col} theo {x_col}")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()