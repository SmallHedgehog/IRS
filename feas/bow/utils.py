import cv2

class SIFT_Extractor(object):
	def __init__(self, use_sift=True):
		super(SIFT_Extractor, self).__init__()
		self.im = None
		self.kp = None
		self.dp = None
		self.use_sift = use_sift
		if use_sift:
			self.sift = cv2.xfeatures2d.SIFT_create()
		else:
			self.surf = cv2.xfeatures2d.SURF_create()

	def detect(self, image):
		self.clear()
		if self.use_sift:
			self._sift(image)
		else:
			self._surf(image)
		return self.dp

	def clear(self):
		self.im, self.kp, self.dp = None, None, None

	def descriptors(self):
		return self.dp

	def _sift(self, image):
		self.im = cv2.imread(image)
		self.im = cv2.cvtColor(self.im, cv2.COLOR_BGR2RGB)
		self.kp = self.sift.detect(self.im)
		self.kp, self.dp = self.sift.compute(self.im, self.kp)

	def _surf(self, image):
		self.im = cv2.imread(image)
		self.im = cv2.cvtColor(self.im, cv2.COLOR_BGR2RGB)
		self.kp = self.surf.detect(self.im)
		self.kp, self.dp = self.surf.compute(self.im, self.kp)
