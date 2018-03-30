import os
import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sio

def modify_line(scr_path, dst_path, line_idx, target_content):
    with open(scr_path, 'r') as f:
        data = f.readlines()
        data[line_idx] = target_content

    with open(dst_path, 'w') as f:
        f.writelines(data)


def modify_qj():
    scr_path = 'QJ_demo.cpp'
    num_files = 10

    video_name_list = ['changchun', 'dongdan']
    corr_list = [(1, 2, 3, 4), (5, 6, 7, 8)]
    for i, (video_name, cor_tuple) in enumerate(zip(video_name_list, corr_list)):
        dst_path = 'QJ_demo_' + str(i) + '.cpp'

        # modify video name
        name_content = '    string video_name = ' + '"' + video_name + '";\r\n'
        modify_line(scr_path, dst_path, 16, name_content)

        # modify coordinate
        # from the second one, the scr_path must be the dst path
        cor_x, cor_y, width, height = cor_tuple
        cor_content = "    int left = %s, top = %s, right = %s, bottom = %s;\r\n" % (
            str(cor_x), str(cor_y), str(width), str(height))
        modify_line(dst_path, dst_path, 38, cor_content)


if __name__ == '__main__':
    pass
