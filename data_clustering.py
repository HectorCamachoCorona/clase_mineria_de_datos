# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1fCYZ67_8ABMFTDudJR9vdMMmjjT1bfBm

# New Section
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import List
import os

def scatter_group_by(file_path: str, df: pd.DataFrame, centroids: np.array, x_column: str, y_column: str, label_column: str):
    fig, ax = plt.subplots()
    labels = pd.unique(df[label_column])
    cmap = plt.cm.get_cmap("tab10", len(labels))

    for i, label in enumerate(labels):
        filtered = df[df[label_column] == label]
        ax.scatter(filtered[x_column], filtered[y_column], label=f"Cluster {label}", cmap=cmap)

    if centroids is not None and len(centroids) > 0:
        centroids = np.array(centroids)
        ax.scatter(centroids[:, 0], centroids[:, 1], marker='x', s=150, c='black', label="Centroides")

    ax.set_xlabel(x_column)
    ax.set_ylabel(y_column)
    ax.legend()
    plt.savefig(file_path)
    plt.close()

def euclidean_distance(p1: np.array, p2: np.array) -> float:
    return np.sqrt(np.sum((p2 - p1) ** 2))

def calculate_means(points: np.array, labels: np.array, clusters: int) -> np.array:
    return [np.mean(points[labels == k], axis=0) for k in range(clusters)]

def calculate_nearest_k(point: np.array, means: List[np.array]):
    distances = [euclidean_distance(mean, point) for mean in means]
    return np.argmin(distances)

def k_means(points: List[np.array], k: int, output_dir="kmeans_imgs"):
    os.makedirs(output_dir, exist_ok=True)
    points = np.array(points)
    labels = np.random.randint(0, k, len(points))
    mean = np.zeros((k, points.shape[1]))

    for t in range(15):
        new_means = calculate_means(points, labels, k)
        new_labels = np.array([calculate_nearest_k(p, new_means) for p in points])

        df_points = pd.DataFrame(points, columns=["year", "selling_price"])
        df_points["label"] = new_labels.astype(str)
        scatter_group_by(f"{output_dir}/kmeans_{t}.png", df_points, new_means, "year", "selling_price", "label")

        if np.array_equal(mean, new_means):
            break
        mean = new_means.copy()
        labels = new_labels

    return mean


df = pd.read_csv("datos_limpios.csv")
df['year'] = pd.to_datetime(df['year'], errors='coerce')
df = df.dropna(subset=['year', 'selling_price'])
df['year'] = df['year'].dt.year
df = df[df['selling_price'] < 5000000]

points = df[['year', 'selling_price']].values.tolist()

centroids = k_means(points, k=3)
print("Centroides finales:", centroids)