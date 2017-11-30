import numpy as np
import random


def shuffle_two_array(array1, array2):
    original_order = np.arange(array1.shape[0])
    order = np.arange(array1.shape[0])
    random.shuffle(order)
    array1[order] = array1[original_order]
    array2[order] = array2[original_order]
    return array1, array2


def shuffle_array(array):
    original_order = np.arange(array.shape[0])
    order = np.arange(array.shape[0])
    random.shuffle(order)
    array[order] = array[original_order]
    return array
