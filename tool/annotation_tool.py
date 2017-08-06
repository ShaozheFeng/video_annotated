import numpy as np
import cv2


class Annotator(object):
    def __init__(self, segment_name):
        self.segment_name = segment_name
        pass

    # label the video
    def label_video(self, frame):
        frame_label = np.zeros(frame.shape[0])
        i = 0
        is_play = False
        while True and i < len(frame):
            # font = cv2.FONT_HERSHEY_SIMPLEX
            # cv2.putText(frame, 'OpenCV', (0, 0), font, 1, (255, 255, 255), 2, cv2.LINE_AA)

            cv2.imshow(self.segment_name, frame[i])

            if is_play is True:
                c = cv2.waitKey(10)
            else:
                c = cv2.waitKey(0)

            if c == 27:
                cv2.destroyAllWindows()
                break
            # left
            elif c == ord('j'):
                if i != 0:
                    i -= 1
            # right
            elif c == ord('l'):
                i += 1
            elif c == ord('a'):
                frame_label[i] = 1
                print str(i) + '---added'
            elif c == ord('r'):
                frame_label[i] = 0
                print str(i) + '---removed'
            # space
            elif c == 32:
                is_play = not is_play
                print is_play
            if is_play is True:
                i += 1

        return frame_label
