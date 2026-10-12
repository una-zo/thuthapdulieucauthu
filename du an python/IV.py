import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA  
from sklearn.metrics import silhouette_score

def load_and_preprocess_data(db_name="football_data.db"):
    with sqlite3.connect(db_name) as conn:
        #lấy data
        df_stats = pd.read_sql("SELECT * FROM fbref_player_stats", conn)
    
    #tìm cột chứa tên cầu thủ và vị trí
    player_col = [c for c in df_stats.columns if 'Player' in c][0]
    pos_col = [c for c in df_stats.columns if 'Pos' in c][0]
    
    #giữ lại thông tin định danh để vẽ biểu đồ
    df_info = df_stats[[player_col, pos_col]].copy()
    
    #lọc ra các cột là dữ liệu số để đưa vào model
    cols_to_drop = [col for col in df_stats.columns if any(x in col for x in ['Player', 'Nation', 'Pos', 'Squad', 'Comp', 'Age', 'Born', 'Matches'])]
    df_features = df_stats.drop(columns=cols_to_drop)
    
    #ép kiểu về dạng số, sau đó điền cột N/a thành 0
    df_features = df_features.apply(pd.to_numeric, errors='coerce').fillna(0)
    
    #chuẩn hóa dữ liệu 
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(df_features)
    
    #trả về thêm player_col để hàm vẽ biểu đồ biết cột nào chứa tên
    return df_info, scaled_data, player_col 

def find_optimal_k(data, max_k=10):
    inertias = []
    sil_scores = []
    k_values = range(2, max_k + 1)
    
    for k in k_values:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans.fit(data)
        inertias.append(kmeans.inertia_)
        sil_scores.append(silhouette_score(data, kmeans.labels_))
        
    #elbow và silhouette
    fig, ax1 = plt.subplots(figsize=(10, 5))

    color = 'tab:blue'
    ax1.set_xlabel('Số lượng cụm (k)')
    ax1.set_ylabel('Inertia (WSSE)', color=color)
    ax1.plot(k_values, inertias, marker='o', color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  
    color = 'tab:red'
    ax2.set_ylabel('Silhouette Score', color=color)
    ax2.plot(k_values, sil_scores, marker='s', color=color, linestyle='--')
    ax2.tick_params(axis='y', labelcolor=color)

    plt.title('Biểu đồ Elbow và Silhouette để chọn K tối ưu')
    fig.tight_layout()
    plt.grid(True)
    plt.show()

def perform_clustering_and_visualization(df_info, scaled_data, optimal_k, player_col):
    kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(scaled_data)
    df_info['Cluster'] = clusters
    
    #pca 2 chiều
    pca_2d = PCA(n_components=2)
    components_2d = pca_2d.fit_transform(scaled_data)
    df_info['PCA1'] = components_2d[:, 0]
    df_info['PCA2'] = components_2d[:, 1]

    #lấy ngẫu nhiên 20 cầu thủ
    sample_df = df_info.sample(n=20, random_state=42)
    
    plt.figure(figsize=(12, 8))
    sns.scatterplot(x='PCA1', y='PCA2', hue='Cluster', palette='tab10', data=df_info, alpha=0.7)
     
    #gắn nhãn tên cầu thủ cho pca
    for _, row in sample_df.iterrows():
        plt.text(row['PCA1'] + 0.1, row['PCA2'], row[player_col], 
                 horizontalalignment='left', size='small', color='black', weight='semibold')
                 
    plt.title('Phân cụm cầu thủ (K-means) trên không gian PCA 2D')
    plt.show()

    #pca 3 chiều
    pca_3d = PCA(n_components=3)
    components_3d = pca_3d.fit_transform(scaled_data)
    
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    scatter = ax.scatter(components_3d[:, 0], components_3d[:, 1], components_3d[:, 2], 
                         c=clusters, cmap='tab10', alpha=0.7)
    
    ax.set_xlabel('PCA 1')
    ax.set_ylabel('PCA 2')
    ax.set_zlabel('PCA 3')
    plt.title('Phân cụm cầu thủ (K-means) trên không gian PCA 3D')
    
    legend1 = ax.legend(*scatter.legend_elements(), title="Clusters")
    ax.add_artist(legend1)
    plt.show()

if __name__ == "__main__":
    #1. data preprocessing
    df_info, scaled_data, player_col = load_and_preprocess_data()
    
    #2. xem biểu đồ và phân tích để chọn k
    find_optimal_k(scaled_data, max_k=10)
    
    #3. chọn k tối ưu
    CHOSEN_K = 4
    
    #4. phân cụm và vẽ pca
    perform_clustering_and_visualization(df_info, scaled_data, CHOSEN_K, player_col)
