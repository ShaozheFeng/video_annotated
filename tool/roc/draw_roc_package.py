import numpy as np
from matplotlib import pyplot as plt
class DrawRoc(object):
    line_style = ['r-', 'b-', 'g-', 'k-', 'm-', 'c-', 'y-', 'r--', 'b--', 'g--', 'k--']
    style_number = len(line_style)
    def __init__(self, fpr, tpr, file_name, line_names):
        self.fpr = fpr
        self.tpr = tpr
        self.file_name = file_name
        self.line_names = line_names
    def draw_roc(self):
        roc_order = 0
        plt.figure(figsize=(15, 8))
        for i in xrange(len(self.line_names)):
            cur_fpr = self.fpr[i] + 0.00001
            cur_fpr = np.log10(cur_fpr)
            cur_tpr = self.tpr[i]
            plt.plot(cur_fpr, cur_tpr, self.line_style[(roc_order % self.style_number)], linewidth=2)
            roc_order += 1
        plt.title('roc curve')
        plt.xlabel('log10 false alarm rate')
        plt.ylabel('true positive rate')
        plt.xlim(-5, 0)
        plt.grid(True)
        plt.legend(self.line_names, loc=4)
        plt.savefig(self.file_name)