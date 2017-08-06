import os
from tool.annotation_tool import Annotator
from tool.split_tool import *
from tool import file_tool


def get_split_video(video_dir):
    for video_name in os.listdir(video_dir):
        video_path = os.path.join(video_dir, video_name)

        coordinate, _ = get_coordinate(video_path)
        split_video(video_path, coordinate, './')


if __name__ == '__main__':
    # get_split_video('/Users/fengshaozhe/Desktop/videos')

    crop_dir = './data'
    for crop_file in os.listdir(crop_dir):
        file_extension = os.path.splitext(crop_file)[1]
        file_name = os.path.splitext(crop_file)[0]
        if file_extension == '.pkl':
            crop_path = os.path.join(crop_dir, crop_file)
            frame = file_tool.load_pickle(crop_path)
            annotator = Annotator(file_name)
            frame_label = annotator.label_video(frame)

            label_name = 'label' + os.path.splitext(crop_file)[0]
            file_tool.write_pickle(label_name, frame_label)
