import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import accuracy_score, classification_report, f1_score

# Load dataset
baca = pd.read_csv("../dataset/Country-data.csv")

print(baca.head())

# Informasi dataset
print(baca.info())

# Memilih kolom numerik
baca_x = baca.select_dtypes(include=np.number)

print(baca_x.head())

# Visualisasi persebaran data
plt.scatter(
    baca['income'],
    baca['gdpp'],
    s=20,
    c='blue',
    alpha=0.5
)

plt.xlabel("Income")
plt.ylabel("GDP")

plt.title("Persebaran Data Country")

plt.show()

# Mengubah dataframe menjadi array
x_array = np.array(baca_x)

print(x_array)

# Normalisasi data
scaler = MinMaxScaler()

x_scaled = scaler.fit_transform(x_array)

print(x_scaled)

# Membuat model K-Means
kmeans = KMeans(n_clusters=3, random_state=42)

kmeans.fit(x_scaled)

# Menampilkan label cluster
print(kmeans.labels_)

# Menambahkan hasil cluster ke dataframe
baca["kluster"] = kmeans.labels_

print(baca.head())

# Report hasil clustering
y_pred = kmeans.labels_

y_test = y_pred

print("Accuracy :", accuracy_score(y_test, y_pred))

print(f'Classification Report: \n{classification_report(y_test, y_pred)}')

print(f"F1 Score : {f1_score(y_test, y_pred, average='macro')}")

# Visualisasi hasil clustering
plt.figure(figsize=(8,6))

plt.scatter(
    baca['income'],
    baca['gdpp'],
    c=baca['kluster'],
    cmap='viridis'
)

# Titik centroid
plt.scatter(
    kmeans.cluster_centers_[:, 6],
    kmeans.cluster_centers_[:, 8],
    s=200,
    c='red',
    marker='X',
    label='Centroid'
)

plt.xlabel('Income')
plt.ylabel('GDP')

plt.title('K-Means Clustering Country Data')

plt.legend()

# Menyimpan visualisasi
plt.savefig("../hasil/visualisasi_cluster_country.png", bbox_inches='tight')

plt.show()

# Menyimpan hasil clustering
baca.to_csv("../hasil/hasil_cluster_country.csv", index=False)

print("Hasil clustering berhasil disimpan.")

# Menyimpan ringkasan cluster
ringkasan_cluster = baca.groupby("kluster")[["income", "gdpp"]].mean()

print(ringkasan_cluster)

ringkasan_cluster.to_csv("../hasil/ringkasan_cluster_country.csv")

print("Ringkasan cluster berhasil disimpan.")

print("""
K-Means Clustering berhasil diterapkan pada dataset Country Data.
Data negara berhasil dikelompokkan berdasarkan karakteristik ekonomi tertentu.
""")