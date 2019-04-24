import cv2
import matplotlib.pyplot as plt
import os
try:
    from pathlib import Path
except ImportError:             # Python 2
    from pathlib2 import Path
# path to video files
directory=Path.cwd()
files = os.listdir(directory)
videos = filter(lambda x: x.endswith('.mp4'), files)
num_file=0
for file in videos:
    print(file)
    vidcap = cv2.VideoCapture(file)
    success, image = vidcap.read()
    count = 0
    success = True
    # определим имя директории, которую создаём
    path = 'frames{id}'.format(id=num_file)

    try:
        os.mkdir(path)
    except OSError:
        print("Создать директорию %s не удалось" % path)
    else:
        print("Успешно создана директория %s " % path)
    while success:
        vidcap.set(cv2.CAP_PROP_POS_MSEC, count*1000)
        success, image = vidcap.read()
        print('Read a new frame: ', success)
        cv2.imwrite('frames{id}/frame%d.jpg'.format(id=num_file) % count, image)  # save frame as JPEG file
        count += 1
            #plt.imshow(image)
            #plt.show()
    num_file+=1