"""Crow.

Reference:
[1] Yannis Kalantidis, Clayton Mellina, Simon Osindero. ECCV 2016.
    Cross-dimensional Weighting for Aggregated Deep Convolutional Features
"""


import numpy as np
import torch
from sklearn.preprocessing import normalize
from sklearn.decomposition import PCA


def spatial_weight(X, a=2, b=2):
    S = np.sum(X, axis=0) * 1.0
    return np.power(S / np.power(np.sum(np.power(S, a)), 1.0/a), 1.0/b)

def channel_weight(X):
    c, w, h = X.shape
    area = float(w*h)
    nonzero = np.zeros(c, dtype=np.float32)
    for idx, x in enumerate(X):
        nonzero[idx] = np.count_nonzero(x) / area
    nonzero_sum = nonzero.sum()
    for idx, nzero in enumerate(nonzero):
        nonzero[idx] = np.log(nonzero_sum / nzero) if nzero > 0. else 0.
    return nonzero

def apply_crow_aggregation(X, a=2, b=2):
    S = spatial_weight(X, a=a, b=b)
    C = channel_weight(X)
    X = X * S
    X = np.sum(X, axis=(1, 2))
    return X * C

def normalize_(X):
    if type(X) == np.ndarray and len(X.shape) == 1:
        X = X.reshape(1, -1)
    return normalize(X)

def apply_process_normalize(X, dim=512, whiten=True, paras=None, copy=False):
    # def normalize_(X):
    #    if type(X) == np.ndarray and len(X.shape) == 1:
    #        X = X.reshape(1, -1)
    #    return normalize(X)

    X = normalize_(X)

    # PCA and Whiten
    if paras is not None:
        pca = paras['pca']
        features = pca.transform(X)
    else:
        pca = PCA(n_components=dim, whiten=whiten, copy=copy)
        features = pca.fit_transform(X)
        paras = {'pca': pca}

    features = normalize_(features)
    return features, paras
