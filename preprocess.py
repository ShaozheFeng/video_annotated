import os
from tool.annotation_tool import Annotator
from tool.split_tool import *
from tool import file_tool

sep = os.path.sep


def get_split_video(video_dir):
    cor_list = [(639, 150, 798, 346),
                (370, 55, 503, 195),
                (820, 324, 962, 500),
                (653, 165, 768, 330),
                (364, 33, 501, 195),
                (531, 16, 668, 204),
                (679, 27, 833, 222),
                (700, 29, 829, 188),
                (532, 8, 668, 155),
                (682, 91, 833, 261)
                ]
    for video_name, coordinate in zip(os.listdir(video_dir), cor_list):
        video_path = os.path.join(video_dir, video_name)

        # coordinate, _ = get_coordinate(video_path)

        split_video(video_path, coordinate, '.' + sep + 'data' + sep + 'split_videos')


if __name__ == '__main__':
    # get_split_video('.' + sep + 'data' + sep + 'videos')

    crop_dir =  '.' + sep + 'data' + sep + 'split_videos'
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
