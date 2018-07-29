import pickle
import numpy as np
from sklearn import preprocessing
from scipy.cluster.vq import vq

from IRS.bow.utils import SIFT_Extractor


class Retrieval(object):
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
