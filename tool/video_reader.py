import cv2
import os
import ConfigParser

_PROP_FRAME_COUNT = cv2.CAP_PROP_FRAME_COUNT


class VideoReader:
    def __init__(self, video_path):
        self._capture = cv2.VideoCapture(video_path)
        self._video_file = video_path
        self._index = 0
        self._last_frame = None
        self._index = 0

    def read(self):
        self._index += 1
        ret_code, self._last_frame = self._capture.read()
        return self._last_frame

    def get_frame_count(self):
        return int(self._capture.get(_PROP_FRAME_COUNT))

    def get_submat(self, img, x, y, height, width):
        crop_img = img[x:x + width, y:y + height]
        return crop_img

    def get_specific_frame(self, frame_index):
        self._capture.set(1, frame_index)
        ret_code, specific_frame = self._capture.read()
        return specific_frame

    def get_time(self):
        return self._capture.get(cv2.CAP_PROP_POS_MSEC) / 1000


if __name__ == "__main__":

    cf = ConfigParser.ConfigParser()
    cf.read('../config/video.conf')

    video_path = cf.get('video', 'video_path')
    dpm_neg_dir = cf.get('video', 'dpm_neg_dir')

    video_reader = VideoReader(video_path)
    for img_name in os.listdir(dpm_neg_dir):
        extension_name = os.path.splitext(img_name)[1]
        if extension_name == '.png':
            image_idx = float(os.path.splitext(img_name)[0].strip('0'))
            huge_img = video_reader.get_specific_frame(image_idx)
            cv2.imwrite('/Volumes/Bingbong/hoop_data/dpm_hard_neg_huge/' + str(image_idx) + '.png', huge_img)
