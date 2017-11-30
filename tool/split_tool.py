import cv2
from tool.video_reader import VideoReader
from tool import file_tool
import os
import numpy as np
from tool.drawer import Drawer

sep = os.path.sep
#
# class SplitVideo():
#     def __index__(self, video_path, coordinate, dst_dir, use_crop=True):
#         self._video_path = video_path
#         self.coordinate = coordinate
#         self.dst_dir = dst_dir
#         self.use_crop = use_crop

def get_coordinate(video_path):
    video_reader = VideoReader(video_path)
    first_frame = video_reader.read()
    drawer = Drawer(img=first_frame)
    return drawer.show_res()


def split_video(video_path, coordinate, dst_dir, use_crop=True):  # init the video param
    SEGMENT_LENGTH = 5000

    video_name = os.path.splitext(video_path)[0].split(sep)[-1]
    left, top, right, bottom = coordinate

    video_reader = VideoReader(video_path)
    frame_count = video_reader.get_frame_count()
    seg_list = [x * SEGMENT_LENGTH for x in range(1, frame_count / SEGMENT_LENGTH + 2)]

    # split the video
    start_idx = 0
    for end_idx in seg_list:
        total_frames = []
        for i in range(start_idx, min(end_idx, frame_count)):

            # shape (height,width,channel)
            current_frame = video_reader.read()
            if use_crop:
                current_frame = current_frame[top:bottom, left:right, :]
            gray_frame = cv2.cvtColor(current_frame, cv2.COLOR_RGB2GRAY)
            total_frames.append(gray_frame)

        # save the segment
        segment_name = video_name + '_' + str(start_idx / SEGMENT_LENGTH).rjust(2, '0')
        segment_path = os.path.join(dst_dir, segment_name)
        total_frames = np.array(total_frames)
        file_tool.write_pickle(segment_path, total_frames)

        start_idx = end_idx


def get_hoop_img(big_img_dir, dst_dir):
    coordinate = None
    for big_img_name in os.listdir(big_img_dir):
        big_img_path = os.path.join(big_img_dir, big_img_name)
        big_imgs = file_tool.load_pickle(big_img_path)

        if not coordinate:
            drawer = Drawer(big_imgs[0])
            coordinate, _ = drawer.show_res()
            left, top, right, bottom = coordinate

            cv2.imshow('hoop', big_imgs[0, top:bottom, left:right])
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        crop_imgs = big_imgs[:, top:bottom, left:right]
        resize_imgs = []
        for i in range(crop_imgs.shape[0]):
            resize_imgs.append(cv2.resize(crop_imgs[i], (40, 40)))

        resize_imgs = np.array(resize_imgs)
        dst_path = os.path.join(dst_dir, 'hoop_' + os.path.splitext(big_img_name)[0])
        file_tool.write_pickle(dst_path, resize_imgs)


if __name__ == '__main__':
    big_img_dir = os.path.join('data', 'big_imgs')
    dst_dir = os.path.join('data', 'hoop_imgs')
    get_hoop_img(big_img_dir, dst_dir)
