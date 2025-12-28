"""
Module UI Components
Chứa các thành phần giao diện người dùng
"""

import tkinter as tk
from tkinter import ttk


class UIComponents:
    """Lớp quản lý các thành phần UI"""
    
    def __init__(self, root):
        self.root = root
        self.entry_widgets = {}
        
        # KHUNG ĐIỀU KHIỂN TRÊN CÙNG
        self.top_frame = None
        self.lbl_status = None
        
        # KHUNG NHẬP LIỆU
        self.input_frame = None
        
        # KHUNG CHỨC NĂNG
        self.btn_frame = None
        
        # BẢNG DỮ LIỆU
        self.tree = None
        
    def create_top_frame(self, import_command):
        """Tạo khung điều khiển trên cùng"""
        self.top_frame = tk.Frame(self.root, pady=10)
        self.top_frame.pack(fill="x")
        
        # Nút load file
        btn_import = tk.Button(
            self.top_frame, 
            text="📂 Mở File (CSV/Excel)", 
            bg="#2196F3", 
            fg="white",
            font=("Arial", 10, "bold"), 
            command=import_command
        )
        btn_import.pack(side="left", padx=20)
        
        # Label trạng thái
        self.lbl_status = tk.Label(self.top_frame, text="Chưa có dữ liệu", fg="red")
        self.lbl_status.pack(side="left")
        
        return self.top_frame
    
    def create_input_frame(self):
        """Tạo khung nhập liệu"""
        self.input_frame = tk.LabelFrame(self.root, text="Thông tin chi tiết / Chỉnh sửa")
        self.input_frame.pack(fill="x", padx=10, pady=5)
        return self.input_frame
    
    def create_button_frame(self, add_cmd, update_cmd, delete_cmd, clean_cmd, plot_cmd):
        """Tạo khung chứa các nút chức năng"""
        self.btn_frame = tk.Frame(self.root)
        self.btn_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Button(
            self.btn_frame, 
            text="Thêm Dòng Mới", 
            bg="#4CAF50", 
            fg="white", 
            command=add_cmd
        ).pack(side="left", padx=5)
        
        tk.Button(
            self.btn_frame, 
            text="Cập nhật Dòng đang chọn", 
            bg="#FF9800", 
            fg="white", 
            command=update_cmd
        ).pack(side="left", padx=5)
        
        tk.Button(
            self.btn_frame, 
            text="Xóa Dòng", 
            bg="#F44336", 
            fg="white", 
            command=delete_cmd
        ).pack(side="left", padx=5)
        
        tk.Button(
            self.btn_frame, 
            text="🧹 Làm sạch (Fill Null)", 
            command=clean_cmd
        ).pack(side="right", padx=5)
        
        tk.Button(
            self.btn_frame, 
            text="📊 Vẽ Biểu Đồ", 
            command=plot_cmd
        ).pack(side="right", padx=5)
        
        return self.btn_frame
    
    def create_tree_view(self, select_callback):
        """Tạo bảng dữ liệu (TreeView)"""
        tree_frame = tk.Frame(self.root)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Scrollbar dọc
        scrolly = ttk.Scrollbar(tree_frame, orient="vertical")
        scrolly.pack(side="right", fill="y")
        
        # Scrollbar ngang
        scrollx = ttk.Scrollbar(tree_frame, orient="horizontal")
        scrollx.pack(side="bottom", fill="x")
        
        # TreeView
        self.tree = ttk.Treeview(
            tree_frame, 
            yscrollcommand=scrolly.set, 
            xscrollcommand=scrollx.set, 
            show="headings"
        )
        self.tree.pack(side="left", fill="both", expand=True)
        
        scrolly.config(command=self.tree.yview)
        scrollx.config(command=self.tree.xview)
        
        # Sự kiện chọn dòng
        self.tree.bind("<<TreeviewSelect>>", select_callback)
        
        return self.tree
    
    def refresh_input_widgets(self, columns):
        """Tạo lại các ô nhập liệu dựa trên danh sách cột"""
        # Xóa widget cũ
        for widget in self.input_frame.winfo_children():
            widget.destroy()
        
        self.entry_widgets = {}
        for i, col in enumerate(columns):
            # Sắp xếp input thành lưới (grid), mỗi hàng 4 ô
            row = i // 4
            col_pos = (i % 4) * 2
            
            tk.Label(self.input_frame, text=col + ":").grid(
                row=row, column=col_pos, padx=5, pady=5, sticky="e"
            )
            entry = tk.Entry(self.input_frame)
            entry.grid(row=row, column=col_pos + 1, padx=5, pady=5, sticky="w")
            self.entry_widgets[col] = entry
    
    def refresh_tree_columns(self, columns):
        """Cấu hình lại cột cho TreeView"""
        self.tree["columns"] = columns
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
    
    def populate_tree(self, df):
        """Đổ dữ liệu vào TreeView"""
        # Xóa dữ liệu cũ
        self.tree.delete(*self.tree.get_children())
        
        # Thay NaN bằng chuỗi rỗng để hiển thị đẹp
        display_df = df.fillna("")
        for index, row in display_df.iterrows():
            self.tree.insert("", "end", iid=index, values=list(row))
    
    def get_entry_values(self):
        """Lấy giá trị từ các ô nhập liệu"""
        return {col: entry.get() for col, entry in self.entry_widgets.items()}
    
    def fill_entry_values(self, row_data):
        """Điền dữ liệu vào các ô nhập liệu"""
        for col, entry in self.entry_widgets.items():
            entry.delete(0, tk.END)
            if col in row_data.index:
                val = row_data[col]
                if pd.notna(val):
                    entry.insert(0, str(val))
    
    def get_selected_item(self):
        """Lấy item đang được chọn trong TreeView"""
        selected_item = self.tree.selection()
        if selected_item:
            return int(selected_item[0])
        return None
    
    def update_status_label(self, text, color):
        """Cập nhật label trạng thái"""
        if self.lbl_status:
            self.lbl_status.config(text=text, fg=color)


import pandas as pd