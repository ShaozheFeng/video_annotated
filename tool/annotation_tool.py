import numpy as np
import cv2


class Annotator(object):
    def __init__(self):
        pass

    # label the video
    def label_video(self, frame):
        frame_label = np.zeros(frame.shape[0])
        i = 0
        is_play = True
        while True and i < len(frame):
            cv2.imshow('sample', frame[i])
            if is_play is True:
                c = cv2.waitKey(10)
            else:
                c = cv2.waitKey(0)

            if c == 27:
                cv2.destroyAllWindows()
                break
            # left
            elif c == ord('j'):
                i -= 1
            # right
            elif c == ord('l'):
                i += 1
            elif c == ord('a'):
                frame_label[i] = 1
                print "goal!!!____", i
            elif c == ord('r'):
                frame_label[i] = 0
                print "remove succeed~~~~", i
            # space
            elif c == 32:
                is_play = not is_play
                print is_play
            if is_play is True:
                i += 1

        return frame_label
