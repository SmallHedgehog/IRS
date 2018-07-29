from __future__ import print_function

import pickle
import os
import numpy as np
from scipy.cluster.vq import *
from sklearn import preprocessing

from IRS.bow.utils import SIFT_Extractor


# Extract SIFT FEATURES
dataset_path = 'E:\\workplace\\Pytorch\\IRS\\data'
features = []
images = []
sift_extractor = SIFT_Extractor()
count = 0
for image in os.listdir(dataset_path):
    ab_image = os.path.join(dataset_path, image)
    print(count, ab_image)
    try:
        des = sift_extractor.detect(ab_image)
        features.append((image, des))
        images.append(image)
    except:
        pass
    count += 1
descriptors = features[0][1]
for _, descriptor in features:
    descriptors = np.vstack((descriptors, descriptor))

# CLUSTER
codes = 1000
codebook, var = kmeans(obs=descriptors, k_or_guess=codes)

# THE HISTOGRAM OF FEATURES
im_features = np.zeros((len(features), codes))
for idx in range(len(features)):
    words, dis = vq(features[idx][1], code_book=codebook)
    for w in words:
        im_features[idx][w] += 1

# TF-IDF
occur = np.sum((im_features > 0) * 1, axis=0)
idf = np.array(np.log(1 + (1.0*occur+1) / (1.0*len(features) + 1)))

# L2-NORMALIZATION
im_features = im_features * idf
im_features = preprocessing.normalize(im_features, norm='l2')

infos = {
    'images': images,
    'idf': idf,
    'im_features': im_features,
    'codes': codes,
    'codebook': codebook
}
pickle.dump(infos, open('infos.pk', 'wb'))
