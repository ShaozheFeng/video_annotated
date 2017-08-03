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

    frame = file_tool.load_pickle('/Users/fengshaozhe/Projects/pycharm/video_annotated/data/12_0-4999.pkl')
    annotator = Annotator()
    annotator.label_video(frame)
