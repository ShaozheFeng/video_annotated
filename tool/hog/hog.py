import numpy as np
import cv2
from tool import file_tool
import ConfigParser


class HOG:
    def __init__(self, image_size, block_size, stride, cell_size, nbins):
        self.image_size = image_size
        self.block_size = block_size
        self.cell_size = cell_size
        self.stride = stride
        self.nbins = nbins

    def compute_hog(self, image_set):
        num_image = image_set.shape[0]

        hog_dimension = self.get_hog_dimension()
        features = np.zeros((num_image, hog_dimension))

        descriptor = cv2.HOGDescriptor(self.image_size, self.block_size, self.stride, self.cell_size, self.nbins)
        for i in xrange(num_image):
            feature = descriptor.compute(image_set[i])
            feature = feature.T
            features[i] = feature
        return features

    # def compute_gradient(self,image):
    #     descriptor = cv2.HOGDescriptor(self.image_size, self.block_size, self.stride, self.cell_size, self.nbins)
    #     descriptor.computegradient

    def get_hog_dimension(self):
        wins = ((self.image_size[0] - self.block_size[0]) / self.stride[0] + 1) * \
               ((self.image_size[1] - self.block_size[1]) / self.stride[1] + 1)
        cells = (self.block_size[0] / self.cell_size[0]) * (self.block_size[1] / self.cell_size[1])
        return wins * cells * self.nbins

    def merge_feature(self, sample, frame_idx):

        two_frame = []
        two_frame_idx = []
        num_sample = sample.shape[0]
        for i in xrange(num_sample - 1):
            if frame_idx[i] + 1 == frame_idx[i + 1]:
                cur_two_frame = np.concatenate((sample[i], sample[i + 1]))

                two_frame_idx.append(frame_idx[i+1])
                two_frame.append(cur_two_frame)
        return np.array(two_frame),np.array(two_frame_idx)

    def three_feature(self, sample, frame_idx,sub_images):

        two_frame = []
        two_frame_idx = []
        num_sample = sample.shape[0]
        for i in xrange(num_sample - 1):
            if frame_idx[i] + 1 == frame_idx[i + 1]:
                cur_two_frame = np.concatenate((sample[i], sample[i + 1]))
                two_frame_idx.append(frame_idx[i+1])
                two_frame.append(cur_two_frame)
        return np.array(two_frame),np.array(two_frame_idx)


if __name__ == '__main__':
    cf = ConfigParser.ConfigParser()
    cf.read('../config/two_hog.conf')

    image_size = eval(cf.get('descriptor', 'image_size'))
    block_size = eval(cf.get('descriptor', 'block_size'))
    stride = eval(cf.get('descriptor', 'stride'))
    cell_size = eval(cf.get('descriptor', 'cell_size'))
    nbins = cf.getint('descriptor', 'nbins')
    print ''
