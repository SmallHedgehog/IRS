import pickle
import os

import numpy as np
from scipy.cluster.vq import vq
from sklearn import preprocessing

from IRS.feas.bow.utils import SIFT_Extractor
from IRS.feas.crow.eval import eval, query_expansion

class baseRetrieval(object):
    def __init__(self):
        super(baseRetrieval, self).__init__()

    def _setup(self):
        raise NotImplementedError

    def metric(self, rimage):
        raise NotImplementedError


class Retrieval(baseRetrieval):
    def __init__(self, _args):
        super(Retrieval, self).__init__()
        self.args = _args
        self._setup()

    def _setup(self):
        self.infos = pickle.load(open(self.args.features, 'rb'))

    def metric(self, rimage):
        feature = self._calc_feature(rimage)
        return self._calc_metric(feature)

    def _calc_feature(self, rimage):
        des = SIFT_Extractor().detect(rimage)
        feature = np.zeros((1, self.infos['codes']))
        words, dis = vq(des, self.infos['codebook'])
        for w in words:
            feature[0][w] += 1
        feature = feature * self.infos['idf']
        feature = preprocessing.normalize(feature, 'l2')
        return feature

    def _calc_metric(self, feature):
        score = np.dot(feature, self.infos['im_features'].T)
        idx = np.argsort(-score)
        images = []
        for index in idx[0]:
            images.append(self.infos['images'][index])
        return images


class ParisRetrieval(baseRetrieval):
    def __init__(self, _args):
        super(ParisRetrieval, self).__init__()
        self.args = _args
        self._setup()

    def _setup(self):
        self.data_infos = pickle.load(
            open(self.args.features, 'rb'), encoding='bytes'
        )
        self.query_infos = pickle.load(
            open(self.args.query_features, 'rb'), encoding='bytes'
        )

    def _data(self, rimage, data):
        for idx, image in enumerate(data):
            image = bytes.decode(image)
            if os.path.basename(rimage) == image:
                return True, idx
        return False, -1

    def metric(self, rimage):
        res, index = self._data(rimage, self.data_infos[b'images'])
        database = 'data'
        if not res:
            res, index = self._data(rimage, self.query_infos[b'images'])
            if not res:
                return None
            database = 'query'

        idx, dists = eval(
            self.data_infos[b'norm_features'][index] if database == 'data' else self.query_infos[b'norm_features'][index],
            self.data_infos[b'norm_features'],
            query_expansion
        )
        images = []
        for index in list(idx):
            images.append(bytes.decode(self.data_infos[b'images'][index]))
        return images
