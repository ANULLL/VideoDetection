import cv2
import matplotlib.pyplot as plt
import os
import datetime as dt
try:
    from pathlib import Path
except ImportError:             # Python 2
    from pathlib2 import Path
def parser(f):
    i=f.find('_')+1
    j=len(f)
    data=f[i:j:1]
    hour=data[0:2:1]
    minute=data[3:5:1]
    second=data[6:8:1]
    d=dt.time(int(hour),int(minute),int(second))
    return d
# path to video files
directory=Path.cwd()
files = os.listdir(directory)
videos = filter(lambda x: x.endswith('.mp4'), files)
num_file=0
for file in videos:
    print(file)
    num_file=parser(file)
    vidcap = cv2.VideoCapture(file)
    success, image = vidcap.read()
    count = num_file.second
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

    #num_file+=1