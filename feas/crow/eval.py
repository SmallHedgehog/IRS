import numpy as np
import os
import pickle

from .crow import normalize_


def get_nn(query, data, k=None):
    if k is None:
        k = len(data)
    dists = ((query-data)**2).sum(axis=1)
    idx = np.argsort(dists)
    dists = dists[idx]
    return idx[:k], dists[:k]

def query_expansion(query, data, idx, k_top=10):
    query += data[idx[:k_top], :].sum(axis=0)
    return normalize_(query)

def eval(query, data, qe=None, k=None, k_top=10):
    idx, dists = get_nn(query, data, k)
    if not qe:
        query = qe(query, data, idx, k_top)
        idx, dists = get_nn(query, data, k)
    return idx, dists
