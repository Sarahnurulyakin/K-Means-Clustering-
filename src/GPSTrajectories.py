import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import accuracy_score, classification_report, f1_score

# Load dataset
baca = pd.read_csv("../dataset/go_track_tracks.csv")

print(baca.head())

# Informasi dataset
print(baca.info())

# Menghapus kolom yang tidak digunakan
baca = baca.drop(["linha"], axis=1)

print(baca.head())

# Menentukan variabel clustering
baca_x = baca.iloc[:, 1:3]

print(baca_x.head())

# Visualisasi persebaran data
plt.scatter(
    baca.distance,
    baca.speed,
    s=10,
    c="red",
    marker="o",
    alpha=0.5
)

plt.xlabel("Distance")
plt.ylabel("Speed")
plt.title("Persebaran Data GPS")

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
    baca['id_android'],
    baca['speed'],
    c=baca['kluster'],
    cmap='viridis'
)

plt.scatter(
    kmeans.cluster_centers_[:, 0],
    kmeans.cluster_centers_[:, 1],
    s=200,
    c='red',
    marker='X',
    label='Centroid'
)

plt.xlabel('ID Android')
plt.ylabel('Speed')

plt.title('K-Means Clustering GPS Trajectories')

plt.legend()

plt.savefig("../hasil/visualisasi_cluster_gps.png", bbox_inches='tight')

plt.show()

# Menyimpan hasil clustering
baca.to_csv("../hasil/hasil_cluster_gps.csv", index=False)

print("Hasil clustering berhasil disimpan.")

# Menyimpan ringkasan cluster
ringkasan_cluster = baca.groupby("kluster")[["distance", "speed"]].mean()

print(ringkasan_cluster)

ringkasan_cluster.to_csv("../hasil/ringkasan_cluster_gps.csv")

print("Ringkasan cluster berhasil disimpan.")