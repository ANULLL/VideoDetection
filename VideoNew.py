import cv2
import matplotlib.pyplot as plt
import numpy as np
import os
import datetime as dt
try:
    from pathlib import Path
except ImportError:             # Python 2
    from pathlib2 import Path
def parser(f):
    i=f.find('s')+1
    j=len(f)
    data=f[i:j:1]
    hour=data[0:2:1]
    minute=data[3:5:1]
    second=data[6:8:1]
    d=dt.time(int(hour),int(minute),int(second))
    return d
directory=Path.cwd()
files = os.listdir(directory)
pictures = filter(lambda x: x.startswith('frames'), files)
#count=1
for file in pictures:
    #print(file)
    count=parser(file)
    #print(count)
# читаем кадры
    p=(str(directory)+'/'+file)
    p=Path(p)
    print(p)
    imgs = [cv2.imread(str(f)) for f in p.glob('*.jpg')]
# создаем видео
    width,height, layers = imgs[0].shape
    fps = 1
    capSize = (height,width) # this is the size of my source video
    fourcc = cv2.VideoWriter_fourcc(*'m', 'p', '4', 'v') # note the lower case
    vout = cv2.VideoWriter()
    success = vout.open('out{id}.avi'.format(id='_'+str(count.hour)+'.'+ str(count.minute)+'.'+str(count.second)),fourcc,fps,capSize,True)
    _=[vout.write(i) for i in imgs]
    print("Видео успешно создано")
    cv2.destroyAllWindows()
    vout.release()
    #count+=1