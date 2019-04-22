import cv2
import matplotlib.pyplot as plt
vidcap = cv2.VideoCapture('video.mp4')
success, image = vidcap.read()
count = 0
success = True
while success:
    vidcap.set(cv2.CAP_PROP_POS_MSEC, count*1000)
    success, image = vidcap.read()
    print('Read a new frame: ', success)
    cv2.imwrite('/Users/maksimpolakov/PycharmProjects/untitled/venv/frames/frame%d.jpg' % count, image)  # save frame as JPEG file
    count += 1
    #plt.imshow(image)
    #plt.show()
