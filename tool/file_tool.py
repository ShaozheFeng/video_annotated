import gzip
import cPickle as pickle


def load_gzip_pickle(file_path):
    with gzip.open(file_path + '.pkl.gz', 'r') as f:
        data = pickle.load(f)
        return data


def write_gzip_pickle_file(file_path, data):
    with gzip.open(file_path + '.pkl.gz', 'w') as f:
        pickle.dump(data, f)


def load_pickle(file_path):
    with open(file_path, 'r') as f:
        data = pickle.load(f)
        return data


def write_pickle(file_path, data):
    with open(file_path, 'w')as f:
        pickle.dump(data, f)
