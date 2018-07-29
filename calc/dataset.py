import os


class Dataset(object):
    pic_surfix = ('jpg', 'JPG', 'jpeg', 'JPEG', 'png', 'PNG',
            'bmp', 'BMP')
    def __init__(self, _dataset):
        super(Dataset, self).__init__()
        self.dataset = _dataset
        self.images = []
        self._load_images()

    def _load_images(self):
        for item in os.listdir(self.dataset):
            for surfix in Dataset.pic_surfix:
                if item.endswith(surfix):
                    self.images.append(item)

    def __len__(self):
        return len(self.images)

    def __getitem__(self, index):
        assert index >= 0 and index < len(self.images)
        return self.images[index]

    def absolute(self, image):
        return os.path.join(self.dataset, image)
