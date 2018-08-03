"""
Extract CNN features from VGG16(pre-trained)
"""

from __future__ import print_function

import glob
import os
import numpy as np

import torch
import torchvision.transforms as transforms
from PIL import Image

from vgg import VGG16
from query_lists import load_query_lists


def load_img(path):
    """
    Load the image at the provided path and normalize to RGB.
    """
    try:
        img = Image.open(path)
        rgb_img = Image.new("RGB", img.size)
        rgb_img.paste(img)
        return rgb_img
    except:
        return None

def format_img_for_vgg(img):
    def normalize_mean(tensor, mean):
        for t, m in zip(tensor, mean):
            t.sub_(m)
        return tensor
    """
    Given an Image, convert to ndarray and preprocess for VGG.
    """
    # Get pixel values
    # d = np.array(img, dtype=np.float32)
    # d = d[:,:,::-1]
    # Subtract mean pixel values of VGG training set
    # d -= np.array((104.00698793,116.66876762,122.67891434))
    # return d.transpose((2,0,1))
    t_img = transforms.ToTensor()(img)
    t_img = normalize_mean(
        t_img,
        (104.00698793/255,116.66876762/255,122.67891434/255)
    )
    return t_img


if __name__ == '__main__':
    dataset_dir = '/data8T/ycf/project/data/Paris/paris/*/*'
    out_dir = '/data8T/ycf/project/IRS/feas/crow/features/'
    query_out_dir = '/data8T/ycf/project/IRS/feas/crow/query_features/'

    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    if torch.cuda.is_available():
        print('OK!')

    net = VGG16(pretrained=True)
    net.to(device)
    net.eval()


    query_lists = load_query_lists()
    for img in glob.glob(dataset_dir):
        base_img = os.path.basename(img)
        is_query = False
        if base_img.split('.jpg')[0] in query_lists:
            is_query = True
        image = load_img(img)
        if image is None:
            print('err: ' + img)
            continue
        print(img)
        tensor_image = format_img_for_vgg(image)
        tensor_image = tensor_image.unsqueeze(0)
        cuda_image = tensor_image.to(device)
        with torch.set_grad_enabled(False):
            out = net(cuda_image)
            if not is_query:
                np.save(os.path.join(out_dir, os.path.basename(img)), out.cpu().numpy())
            else:
                np.save(os.path.join(query_out_dir, os.path.basename(img)), out.cpu().numpy())

