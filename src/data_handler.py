"""
Module xử lý dữ liệu - Data Handler
Chứa các hàm xử lý, validate, clean dữ liệu
"""

import pandas as pd
import os


class DataHandler:
    """Lớp xử lý dữ liệu"""
    
    def __init__(self):
        self.df = pd.DataFrame()
        self.data_dir = "data"
        self.csv_filename = "titanic.csv"
        
        # Tạo thư mục data nếu chưa tồn tại
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    @staticmethod
    def parse_value(val):
        """Ép kiểu dữ liệu an toàn"""
        val = val.strip()  # Xóa khoảng trắng
        if val == "":
            return None
        
        # Thử ép sang số nguyên
        try:
            return int(val)
        except ValueError:
            # Nếu không phải số nguyên, thử ép sang số thực
            try:
                return float(val)
            except ValueError:
                # Nếu không phải số thì giữ nguyên chuỗi
                return val
    
    @staticmethod
    def validate_data(row_data):
        """
        Kiểm tra tính hợp lệ của dữ liệu trước khi Thêm hoặc Update.
        Trả về: (True, "") nếu hợp lệ, (False, "Lỗi...") nếu không hợp lệ.
        """
        
        # 1. Kiểm tra Survived (0 hoặc 1)
        if 'Survived' in row_data:
            val = row_data['Survived']
            # Chấp nhận số 0, 1 hoặc chuỗi "0", "1"
            if str(val) not in ['0', '1']:
                return False, "Cột 'Survived' chỉ được nhập 0 hoặc 1."

        # 2. Kiểm tra Pclass (1, 2, 3)
        if 'Pclass' in row_data:
            val = row_data['Pclass']
            if str(val) not in ['1', '2', '3']:
                return False, "Cột 'Pclass' chỉ được nhập 1, 2 hoặc 3."

        # 3. Kiểm tra Sex (male hoặc female)
        if 'Sex' in row_data:
            val = str(row_data['Sex']).lower().strip()
            if val not in ['male', 'female']:
                return False, "Cột 'Sex' chỉ được nhập 'male' hoặc 'female'."

        # 4. Kiểm tra Age (>0 và <=146)
        if 'Age' in row_data:
            val = row_data['Age']
            # Kiểm tra xem có phải số không (int hoặc float)
            if not isinstance(val, (int, float)):
                return False, "Cột 'Age' phải là số."
            if not (0 < val <= 146):
                return False, "Cột 'Age' phải lớn hơn 0 và nhỏ hơn hoặc bằng 146."

        # 5. Các cột bắt buộc là số: SibSp, Parch, Fare
        numeric_cols = ['SibSp', 'Parch', 'Fare']
        for col in numeric_cols:
            if col in row_data:
                val = row_data[col]
                if not isinstance(val, (int, float)):
                    return False, f"Cột '{col}' bắt buộc phải nhập số."
                if val < 0:
                    return False, f"Cột '{col}' không được là số âm."

        return True, ""
    
    def load_file(self, file_path):
        """Load file CSV hoặc Excel"""
        if file_path.endswith('.csv'):
            self.df = pd.read_csv(file_path)
        else:
            self.df = pd.read_excel(file_path)
        return self.df
    
    def add_row(self, new_row):
        """Thêm dòng mới vào DataFrame"""
        self.df.loc[len(self.df)] = new_row
        return self.df
    
    def update_row(self, index, updated_row):
        """Cập nhật dòng tại index"""
        for col, val in updated_row.items():
            self.df.at[index, col] = val
        return self.df
    
    def delete_row(self, index):
        """Xóa dòng tại index"""
        self.df = self.df.drop(index).reset_index(drop=True)
        return self.df
    
    def save_to_csv(self, filename=None):
        """Lưu DataFrame ra file CSV trong thư mục data"""
        if filename is None:
            filename = self.csv_filename
        
        # Đường dẫn đầy đủ đến file
        filepath = os.path.join(self.data_dir, filename)
        self.df.to_csv(filepath, index=False)
        return filepath
    
    def clean_data(self):
        """Làm sạch dữ liệu"""
        data = self.df
        
        # Loại bỏ các dòng có giá trị null tại cột PassengerId
        data = data.dropna(subset=['PassengerId'])
        
        # Danh sách các cột số nguyên (Int) cần điền 0
        columns_int = ['Survived', 'SibSp', 'Parch']
        
        for col in columns_int:
            if col in data.columns:
                # Điền giá trị thiếu bằng 0
                data[col] = data[col].fillna(0)
        
        # Fill các dữ liệu trống bằng dữ liệu Pclass phổ biến nhất
        if 'Pclass' in data.columns:
            data['Pclass'] = data['Pclass'].fillna(data['Pclass'].mode()[0])
        
        # Tính trung bình của cột Age và Fare
        columns_mean = ['Age', 'Fare']
        for col in columns_mean:
            if col in data.columns:
                data[col] = data[col].fillna(data[col].mean())
        
        # Danh sách cột chuỗi thiếu dữ liệu
        string_cols = ['Name', 'Sex', 'Cabin', 'Embarked', 'Ticket']
        
        for col in string_cols:
            if col in data.columns:
                # Điền chuỗi "No info" vào các ô trống
                data[col].fillna("No info", inplace=True)
                # Ép kiểu chuỗi -> Chuyển chữ thường -> Cắt khoảng trắng thừa
                data[col] = data[col].astype(str).str.lower().str.strip()
        
        # Loại bỏ các bản ghi trùng lặp dựa PassengerId
        data = data.drop_duplicates(subset=['PassengerId'], keep='first')
        
        # Chuyển đổi cột Age sang kiểu số nguyên
        if 'Age' in data.columns:
            data['Age'] = data['Age'].astype(int)
        
        # Chuyển đổi PassengerId sang kiểu chuỗi
        if 'PassengerId' in data.columns:
            data['PassengerId'] = data['PassengerId'].astype(str)
        
        # Danh sách các cột số lượng bắt buộc phải dương
        cols_pos = ['Fare', 'SibSp', 'Parch']
        
        for col in cols_pos:
            if col in data.columns:
                # Lấy trị tuyệt đối cho toàn bộ cột
                data[col] = data[col].abs()
        
        self.df = data
        
        # Lưu file sau khi clean
        self.save_to_csv()
        
        return self.df
    
    def get_numeric_columns(self):
        """Lấy danh sách các cột số"""
        return self.df.select_dtypes(include=['number']).columns.tolist()
    
    def get_grouped_data(self, x_col, y_col):
        """Gom nhóm dữ liệu theo cột x và tổng cột y"""
        return self.df.groupby(x_col)[y_col].sum().reset_index()