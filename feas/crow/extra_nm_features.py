"""
Get aggregation features by Crow.
"""

import pickle
import os

import torch
import numpy as np

from crow import apply_crow_aggregation, apply_process_normalize


def load_features(features_path):
    for np_file in os.listdir(features_path):
        X = np.load(os.path.join(features_path, np_file))
        yield X, np_file.split('.npy')[0]

def squeeze_0(X):
    X = torch.Tensor(X)
    X.squeeze_(0)
    return X.numpy()


if __name__ == '__main__':
    net_features = '/data8T/ycf/project/IRS/feas/crow/features'
    query_features = '/data8T/ycf/project/IRS/feas/crow/query_features'
    norm_features = '/data8T/ycf/project/IRS/feas/crow/norm_features'
    query_norm_features = '/data8T/ycf/project/IRS/feas/crow/query_norm_features'
    
    features, N = [], []
    for X, n in load_features(net_features):
        X = squeeze_0(X)
        X = list(apply_crow_aggregation(X))
        features.append(X)
        N.append(n)

    features = np.array(features)
    features, paras = apply_process_normalize(features)
    infos = {
        'norm_features': features,
        'paras': paras,
        'images': N
    }
    pickle.dump(infos, open(os.path.join(norm_features, 'infos.plk'), 'wb'))

    features, N = [], []
    for X, n in load_features(query_features):
        X = squeeze_0(X)
        X = list(apply_crow_aggregation(X))
        features.append(X)
        N.append(n)
    features = np.array(features)
    features, _ = apply_process_normalize(features, paras=paras)
    infos = {
        'norm_features': features,
        'images': N
    }
    pickle.dump(infos, open(os.path.join(query_norm_features, 'infos.plk'), 'wb'))

