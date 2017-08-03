import cv2


class Drawer:
    def __init__(self, img=None, image_path=''):

        self.drawing = False
        self.mode = True
        self.ix = -1
        self.iy = -1
        if img is None:
            self.img = cv2.imread(image_path)
        else:
            self.img = img
        # self.xmin = -1
        # self.ymin = -1
        self.length = -1
        self.xmax = -1
        self.xmax = -1

    def draw_rect(self, event, x, y, flags, param):

        if event == cv2.EVENT_LBUTTONDOWN:
            self.drawing = True
            self.ix, self.iy = x, y
        elif event == cv2.EVENT_MOUSEMOVE:
            if self.drawing:
                copy_img = self.img.copy()
                cv2.rectangle(copy_img, (self.ix, self.iy), (x, y), (0, 255, 0), 1)
                cv2.imshow('image', copy_img)
        elif event == cv2.EVENT_LBUTTONUP:
            self.drawing = False
            copy_img = self.img.copy()
            cv2.rectangle(copy_img, (self.ix, self.iy), (x, y), (0, 255, 0), 1)
            print 'final coordinate: xmin: ymin: xmax: ymax %d %d %d %d' % (self.ix, self.iy, x, y)
            cv2.imshow('image', copy_img)
            self.xmax = x
            self.ymax = y

    def show_res(self):
        # image_size
        cv2.namedWindow('image')
        # cv2.namedWindow('image', cv2.WINDOW_NORMAL)
        cv2.setMouseCallback('image', self.draw_rect)
        # cv2.resizeWindow('image', 70, 60)

        cv2.imshow('image', self.img)
        cv2.waitKey(0)

        cv2.destroyAllWindows()
        return (self.ix, self.iy, self.xmax, self.ymax), self.img.shape


if __name__ == '__main__':
    drawer = Drawer('../data/test_gray.png')
    print drawer.show_res()
