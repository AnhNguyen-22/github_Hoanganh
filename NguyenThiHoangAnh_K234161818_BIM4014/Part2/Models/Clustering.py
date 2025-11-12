# Models/Clustering.py
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

PALETTE = ["#D6A99D", "#9CAFAA", "#D6DAC8", "#FBF3D5", "#8aa0a0", "#d9b8b0", "#c6d1c6"]

class Clustering:
    """
    Phân cụm hành vi KH dựa trên um3la.transaction
    - Tạo đặc trưng theo KH (đơn, SP, chi tiêu, v.v.)
    - Elbow method để chọn k
    - Huấn luyện KMeans và trực quan
    - Hàm lấy KH theo cụm
    """

    def __init__(self, connector=None):
        self.connector = connector
        self.df_features = None          # dữ liệu đặc trưng đầu vào
        self.df_clustered = None         # dữ liệu sau khi gán nhãn cụm
        self.scaler = StandardScaler()
        self.kmeans = None

    # -----------------------------
    # 1) Trích xuất đặc trưng theo khách hàng từ bảng transaction
    # -----------------------------
    def load_customer_features(self):
        """Load và preprocess dữ liệu transaction, sau đó tạo features cho mỗi CustomerID"""
        try:
            # Load dữ liệu transaction
            sql = "SELECT * FROM transaction;"
            df = self.connector.queryDataset(sql)
            
            if df is None or df.empty:
                print("⚠️ Không có dữ liệu transaction.")
                return None
            
            # Preprocessing: Loại bỏ duplicate IDs
            if 'Id' in df.columns:
                df = df.drop_duplicates(subset=['Id'], keep='first')
            
            # Loại bỏ các dòng có missing values quan trọng
            required_cols = ['InvoiceNo', 'CustomerID', 'Quantity', 'UnitPrice']
            existing_cols = [col for col in required_cols if col in df.columns]
            
            if existing_cols:
                df = df.dropna(subset=existing_cols)
            
            # Loại bỏ các dòng có Quantity <= 0 hoặc UnitPrice <= 0
            if 'Quantity' in df.columns:
                df = df[df['Quantity'] > 0]
            if 'UnitPrice' in df.columns:
                df = df[df['UnitPrice'] > 0]
            
            # Tính TotalValue trước (Quantity * UnitPrice)
            df['TotalValue'] = df['Quantity'] * df['UnitPrice']
            
            # Tính toán features cho mỗi CustomerID
            df_features = df.groupby('CustomerID').agg({
                'InvoiceNo': 'nunique',      # Số đơn hàng unique
                'StockCode': 'nunique',      # Số sản phẩm unique
                'Quantity': 'sum',           # Tổng số lượng
                'TotalValue': 'sum',         # Tổng chi tiêu
                'UnitPrice': 'mean'          # Giá trung bình
            }).reset_index()
            
            # Đổi tên cột
            df_features.columns = ['CustomerID', 'TotalOrders', 'TotalProducts', 'TotalQuantity', 'TotalSpending', 'AvgUnitPrice']
            
            # Điền các giá trị NaN bằng 0
            df_features = df_features.fillna(0)
            
            # Sắp xếp theo TotalSpending giảm dần
            df_features = df_features.sort_values('TotalSpending', ascending=False)
            
            self.df_features = df_features
            return self.df_features
            
        except Exception as e:
            print(f"Error in load_customer_features: {e}")
            import traceback
            traceback.print_exc()
            return None

    # -----------------------------
    # 2) Khám phá: histogram theo các cột số
    # -----------------------------
    def show_hist(self, columns=None):
        if self.df_features is None or self.df_features.empty:
            print("⚠️ Chưa có dữ liệu đặc trưng. Hãy gọi load_customer_features() trước.")
            return
        cols = columns or ["TotalOrders", "TotalProducts", "TotalQuantity", "TotalSpending", "AvgUnitPrice"]
        n = len(cols)
        plt.figure(figsize=(7, 1 + 2.6*n))
        for i, col in enumerate(cols, 1):
            ax = plt.subplot(n, 1, i)
            plt.subplots_adjust(hspace=0.5)
            sns.histplot(self.df_features[col], bins=32, kde=True, ax=ax)
            ax.set_title(f"Histogram of {col}")
        plt.tight_layout()
        plt.show()

    # -----------------------------
    # 3) Elbow method
    # -----------------------------
    def elbow_method(self, columns, k_max=10, return_data=False):
        """
        columns: list các cột số dùng để gom cụm
        return_data: Nếu True, trả về (k_values, inertias) thay vì vẽ biểu đồ
        """
        if self.df_features is None or self.df_features.empty:
            print("⚠️ Chưa có dữ liệu đặc trưng. Hãy gọi load_customer_features() trước.")
            return None if return_data else None
        X = self.df_features[columns].values
        
        # Áp dụng Log Transform để giảm độ lệch (skewness)
        # Sử dụng np.log1p để xử lý các giá trị bằng 0 (nếu có)
        X = np.log1p(X)
        
        # Giờ mới chuẩn hóa dữ liệu đã biến đổi
        X = self.scaler.fit_transform(X)

        inertias = []
        for k in range(1, k_max+1):
            # Thêm n_init=10 để chạy 10 lần và chọn kết quả tốt nhất
            model = KMeans(n_clusters=k, init="k-means++", max_iter=500, random_state=42, n_init=10) 
            model.fit(X)
            inertias.append(model.inertia_)

        k_values = list(range(1, k_max+1))
        
        if return_data:
            return k_values, inertias
        
        # Vẽ biểu đồ nếu không return_data
        plt.figure(figsize=(9, 4))
        plt.plot(k_values, inertias, "o")
        plt.plot(k_values, inertias, "-", alpha=0.6)
        plt.xlabel("Number of Clusters")
        plt.ylabel("Cluster Sum of Squared Distances (Inertia)")
        plt.title("Elbow Method (after Log Transform)")
        plt.grid(alpha=0.3)
        plt.show()
        return None

    # -----------------------------
    # 4) Train KMeans
    # -----------------------------
    def train_kmeans(self, columns, n_clusters=3):
        if self.df_features is None or self.df_features.empty:
            print("⚠️ Chưa có dữ liệu đặc trưng. Hãy gọi load_customer_features() trước.")
            return None

        X = self.df_features[columns].values
        
        # Áp dụng Log Transform (phải đồng nhất với elbow_method)
        X = np.log1p(X)

        # Chuẩn hóa dữ liệu đã biến đổi
        Xs = self.scaler.fit_transform(X)

        # Thêm n_init=10
        self.kmeans = KMeans(n_clusters=n_clusters, init="k-means++", max_iter=500, random_state=42, n_init=10)
        labels = self.kmeans.fit_predict(Xs)
        
        # Gán nhãn vào dataframe gốc (chưa biến đổi) để trực quan
        self.df_clustered = self.df_features.copy()
        self.df_clustered["Cluster"] = labels
        return self.df_clustered

    # -----------------------------
    # 5) Trực quan 2D (tuỳ chọn cặp trục)
    # -----------------------------
    def visualize_2d(self, x="TotalOrders", y="TotalSpending"):
        if self.df_clustered is None or "Cluster" not in self.df_clustered.columns:
            print("⚠️ Hãy gọi train_kmeans() trước khi vẽ.")
            return
        plt.figure(figsize=(8, 6))
        sns.scatterplot(
            data=self.df_clustered,
            x=x, y=y, hue="Cluster", palette=PALETTE, s=80, edgecolor="white", linewidth=0.4
        )
        plt.title(f"Customer Clusters — {x} vs {y}")
        plt.grid(alpha=0.3)
        plt.tight_layout()
        plt.show()

    # -----------------------------
    # 6) Lấy KH theo cụm
    # -----------------------------
    def get_customers_by_cluster(self, cluster_id):
        if self.df_clustered is None or "Cluster" not in self.df_clustered.columns:
            print("⚠️ Model chưa được train.")
            return pd.DataFrame()
        return self.df_clustered[self.df_clustered["Cluster"] == cluster_id].copy()

