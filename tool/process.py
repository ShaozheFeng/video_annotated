import numpy as np
from tool import file_tool
import cv2
from tool.hog.hog import HOG
import ConfigParser
from tool import shuffle_tool
from tool.roc.draw_roc_package import DrawRoc
from sklearn import metrics
import os


def get_total_image(image_dir, label_dir, number):
    total_image = []
    total_label = []

    lable_list = ['27', '28', '29', '30']
    for image_name, label_name in zip(os.listdir(image_dir), os.listdir(label_dir)):
        if image_name != '.DS_Store':
            _, img_v_num, img_seg_num = image_name.split('_')
            _, label_v_num, label_seg_num = label_name.split('_')
            if img_v_num == label_v_num and img_seg_num == label_seg_num:
                if label_v_num in lable_list:
                    image = file_tool.load_pickle(os.path.join(image_dir, image_name))
                    label = file_tool.load_pickle(os.path.join(label_dir, label_name))

                    total_image.extend(image)
                    total_label.extend(label)
            else:
                raise AssertionError()

    total_image = np.array(total_image)
    total_label = np.array(total_label)

    pos_idx = np.where(total_label == 1)
    neg_idx = np.where(total_label == 0)

    pos_img = total_image[pos_idx]
    neg_img = total_image[neg_idx]

    pos_data = (pos_img, pos_idx[0])
    neg_data = (neg_img, neg_idx[0])

    file_tool.write_pickle('../data/total_image/' + number + '_pos_sample.pkl', (pos_img, pos_idx[0]))
    file_tool.write_pickle('../data/total_image/' + number + '_neg_sample.pkl', (neg_img, neg_idx[0]))
    return pos_data, neg_data


def get_hog_feature(total_img_dir, number):
    cf = ConfigParser.ConfigParser()
    cf.read('../config/hog.conf')

    image_size = eval(cf.get('descriptor', 'image_size'))
    block_size = eval(cf.get('descriptor', 'block_size'))
    stride = eval(cf.get('descriptor', 'stride'))
    cell_size = eval(cf.get('descriptor', 'cell_size'))
    nbins = cf.getint('descriptor', 'nbins')
    hog = HOG(image_size, block_size, stride, cell_size, nbins)

    pos_samples = []
    pos_sample_idx = []
    neg_samples = []
    neg_sample_idx = []
    for file_name in os.listdir(total_img_dir):
        norp = file_name.split('_')[1]
        file_path = os.path.join(total_img_dir, file_name)
        data = file_tool.load_pickle(file_path)
        if norp == 'neg':
            neg_samples.extend(data[0])
            neg_sample_idx.extend(data[1])
        elif norp == 'pos':
            pos_samples.extend(data[0])
            pos_sample_idx.extend(data[1])

    pos_samples = np.array(pos_samples)
    pos_sample_idx = np.array(pos_sample_idx)
    neg_samples = np.array(neg_samples)
    neg_sample_idx = np.array(neg_sample_idx)
    # pos_samples = pos_data[0]
    # pos_sample_idx = pos_data[1]
    pos_hog = hog.compute_hog(pos_samples)

    two_pos, two_pos_idx = hog.merge_feature(pos_hog, pos_sample_idx)

    two_pos, two_pos_idx = shuffle_tool.shuffle_two_array(two_pos, two_pos_idx)

    file_tool.write_pickle('../data/two_hog/' + 'two_' + number + '_pos.pkl', (two_pos, two_pos_idx))

    # neg_samples = neg_data[0]
    # neg_sample_idx = neg_data[1]
    neg_hog = hog.compute_hog(neg_samples)

    two_neg, two_neg_idx = hog.merge_feature(neg_hog, neg_sample_idx)

    two_neg, two_neg_idx = shuffle_tool.shuffle_two_array(two_neg, two_neg_idx)
    two_neg = two_neg[0:13000]

    file_tool.write_pickle('../data/two_hog/' + 'two_' + number + '_neg.pkl', (two_neg, two_neg_idx))


def save_pos_img(pos_path, des_path):
    pos_data = file_tool.load_pickle(pos_path)
    for i in xrange(pos_data[0].shape[0]):
        cv2.imwrite('./pos_img/' + str(i) + '.png', pos_data[0][i])


def get_training_test_set(two_hog_dir, number):
    total_pos = []
    total_neg = []
    num_set = 50000
    for two_hog_name in (os.listdir(two_hog_dir)):
        if two_hog_name[-7:] == 'neg.pkl':
            print two_hog_name[-7:]
            data = file_tool.load_pickle(os.path.join(two_hog_dir, two_hog_name))
            # neg_label = np.zeros(data[0].shape[0])
            # total_label.extend(neg_label)
            total_neg.extend(data[0])
        elif two_hog_name[-7:] == 'pos.pkl':
            print two_hog_name[-7:]
            data = file_tool.load_pickle(os.path.join(two_hog_dir, two_hog_name))
            # pos_label = np.ones(data[0].shape[0])
            # total_label.extend(pos_label)
            total_pos.extend(data[0])

    total_neg = np.array(total_neg)
    total_neg = shuffle_tool.shuffle_array(total_neg)
    total_pos = np.array(total_pos)

    total_feature = np.concatenate((total_pos, total_neg))
    total_label = np.concatenate((np.ones(total_pos.shape[0]), np.zeros(total_neg.shape[0])))

    total_feature, total_label = shuffle_tool.shuffle_two_array(total_feature, total_label)
    print total_feature.shape, total_label.shape

    num_train = 40000
    train_feature = total_feature[0:num_train]
    train_label = total_label[0:num_train]
    test_feature = total_feature[num_train:]
    test_label = total_label[num_train:]

    print train_feature.shape, train_label.shape
    print test_feature.shape, test_label.shape

    file_tool.write_pickle('../data/set/' + '/training_' + number + '_.pkl', (train_feature, train_label))
    file_tool.write_pickle('../data/set/' + '/test_' + number + '_.pkl', (test_feature, test_label))


def show_roc(roc_name, directory):
    data = file_tool.load_pickle('../data/two_hog/1213_test_set.pkl.gz')
    y_true = data[1]

    fpr = []
    tpr = []
    line_name = []

    for file_name in os.listdir(directory):
        extension = os.path.splitext(file_name)[1]
        if extension == '.gz':
            val = file_tool.load_pickle(os.path.join(directory, file_name))
            val = np.array(val) * -1
            cur_fpr, cur_tpr, _ = metrics.roc_curve(y_true, val)

            fpr.append(cur_fpr)
            tpr.append(cur_tpr)
            file_name = file_name[:-7]
            line_name.append(file_name)

    draw_roc = DrawRoc(fpr, tpr, roc_name, line_name)
    draw_roc.draw_roc()


if __name__ == '__main__':
    # image_dir = '../data/hoop'
    # label_dir = '../data/label'
    # get_total_image(image_dir, label_dir, '27-28-29-30')

    # get_hog_feature('../data/total_image', '27-28-29-30')

    get_training_test_set('../data/two_hog', '1130')

    # save_pos_img('../data/total_image/27-28-29-30_pos_sample.pkl', '')
