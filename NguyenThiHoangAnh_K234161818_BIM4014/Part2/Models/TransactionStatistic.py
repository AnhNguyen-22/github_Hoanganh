# Models/TransactionStatistic.py
import pandas as pd
import traceback
from datetime import datetime


class TransactionStatistic:
    """Model cho thống kê từ bảng transaction trong database um3la"""
    
    def __init__(self, connector=None):
        self.connector = connector
        self.df_cleaned = None
    
    def load_and_preprocess(self):
        """Load và preprocess dữ liệu transaction (loại bỏ duplicate, missing cells)"""
        try:
            sql = "SELECT * FROM transaction;"
            df = self.connector.queryDataset(sql)
            
            if df is None or df.empty:
                return None
            
            # Preprocessing: Loại bỏ duplicate IDs
            if 'Id' in df.columns:
                df = df.drop_duplicates(subset=['Id'], keep='first')
            
            # Loại bỏ các dòng có missing values quan trọng
            # Giữ lại các dòng có đầy đủ InvoiceNo, CustomerID, Quantity, UnitPrice
            required_cols = ['InvoiceNo', 'CustomerID', 'Quantity', 'UnitPrice']
            existing_cols = [col for col in required_cols if col in df.columns]
            
            if existing_cols:
                df = df.dropna(subset=existing_cols)
            
            # Loại bỏ các dòng có Quantity <= 0 hoặc UnitPrice <= 0
            if 'Quantity' in df.columns:
                df = df[df['Quantity'] > 0]
            if 'UnitPrice' in df.columns:
                df = df[df['UnitPrice'] > 0]
            
            # Chuyển đổi InvoiceDate sang datetime nếu có
            if 'InvoiceDate' in df.columns:
                try:
                    # Thử nhiều format
                    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], errors='coerce', format='%d/%m/%Y %H:%M')
                    # Nếu không được, thử format khác
                    if df['InvoiceDate'].isna().any():
                        df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], errors='coerce')
                except:
                    pass
            
            self.df_cleaned = df
            return df
            
        except Exception as e:
            print(f"Error in load_and_preprocess: {e}")
            traceback.print_exc()
            return None
    
    def get_max_invoice_no(self):
        """Tìm InvoiceNo có giá trị lớn nhất"""
        try:
            if self.df_cleaned is None:
                self.load_and_preprocess()
            
            if self.df_cleaned is None or self.df_cleaned.empty:
                return None
            
            if 'InvoiceNo' not in self.df_cleaned.columns:
                return None
            
            # Chuyển InvoiceNo sang số nếu có thể
            df = self.df_cleaned.copy()
            try:
                df['InvoiceNo_numeric'] = pd.to_numeric(df['InvoiceNo'], errors='coerce')
                max_invoice = df.loc[df['InvoiceNo_numeric'].idxmax()]
                result = pd.DataFrame([{
                    'InvoiceNo': max_invoice['InvoiceNo'],
                    'Value': max_invoice['InvoiceNo_numeric']
                }])
                return result
            except:
                # Nếu không chuyển được sang số, dùng string
                max_invoice = df.loc[df['InvoiceNo'].str.len().idxmax()] if 'InvoiceNo' in df.columns else None
                if max_invoice is not None:
                    result = pd.DataFrame([{
                        'InvoiceNo': max_invoice['InvoiceNo'],
                        'Value': str(max_invoice['InvoiceNo'])
                    }])
                    return result
                return None
                
        except Exception as e:
            print(f"Error in get_max_invoice_no: {e}")
            traceback.print_exc()
            return None
    
    def get_top_n_customers(self, n, date_from=None, date_to=None):
        """Tìm TOP N CustomerID có giá trị giao dịch lớn nhất trong khoảng thời gian T1-T2"""
        try:
            if self.df_cleaned is None:
                self.load_and_preprocess()
            
            if self.df_cleaned is None or self.df_cleaned.empty:
                return None
            
            df = self.df_cleaned.copy()
            
            # Lọc theo thời gian nếu có
            if date_from and date_to and 'InvoiceDate' in df.columns:
                try:
                    if isinstance(date_from, str):
                        date_from = pd.to_datetime(date_from)
                    if isinstance(date_to, str):
                        date_to = pd.to_datetime(date_to)
                    
                    df = df[(df['InvoiceDate'] >= date_from) & (df['InvoiceDate'] <= date_to)]
                except:
                    pass
            
            # Tính tổng giá trị giao dịch cho mỗi CustomerID
            if 'CustomerID' in df.columns and 'Quantity' in df.columns and 'UnitPrice' in df.columns:
                df['TotalValue'] = df['Quantity'] * df['UnitPrice']
                result = df.groupby('CustomerID')['TotalValue'].sum().reset_index()
                result.columns = ['CustomerID', 'TotalTransactionValue']
                result = result.sort_values('TotalTransactionValue', ascending=False)
                result = result.head(n)
                return result
            else:
                return None
                
        except Exception as e:
            print(f"Error in get_top_n_customers: {e}")
            traceback.print_exc()
            return None
    
    def get_orders_by_year_country(self):
        """Lấy phân bố đơn hàng theo năm và quốc gia"""
        try:
            if self.df_cleaned is None:
                self.load_and_preprocess()
            
            if self.df_cleaned is None or self.df_cleaned.empty:
                return None
            
            df = self.df_cleaned.copy()
            
            # Kiểm tra các cột cần thiết
            if 'InvoiceDate' not in df.columns or 'Country' not in df.columns:
                return None
            
            # Trích xuất năm từ InvoiceDate
            try:
                df['Year'] = pd.to_datetime(df['InvoiceDate']).dt.year
            except:
                return None
            
            # Đếm số đơn hàng (InvoiceNo) theo năm và quốc gia
            # Sử dụng InvoiceNo để đếm đơn hàng (mỗi InvoiceNo là một đơn hàng)
            if 'InvoiceNo' in df.columns:
                result = df.groupby(['Year', 'Country'])['InvoiceNo'].nunique().reset_index()
                result.columns = ['Year', 'Country', 'OrderCount']
                result = result.sort_values(['Year', 'OrderCount'], ascending=[True, False])
                return result
            else:
                return None
                
        except Exception as e:
            print(f"Error in get_orders_by_year_country: {e}")
            traceback.print_exc()
            return None

