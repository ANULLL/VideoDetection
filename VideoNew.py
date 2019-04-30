import cv2
import matplotlib.pyplot as plt
import numpy as np
import os
import datetime as dt

from pathlib import Path

def parser_time(f):
    i=f.find('_')+1
    j=len(f)
    data=f[i:j:1]
    hour=data[0:2:1]
    minute=data[3:5:1]
    second=data[6:8:1]
    d=dt.time(int(hour),int(minute),int(second))
    return d
def parser_date(f):
    i = f.find('_') + 1
    j = len(f)
    idplace=f[0:i:1]
    data = f[i:j:1]
    year=data[0:4:1]
    month=data[5:7:1]
    day=data[8:10:1]
    #day = data[0:2:1]
    #month = data[3:5:1]
    #year = data[6:10:1]
    d = dt.date(int(year),int(month),int(day))
    return idplace,d,data
directory=Path.cwd()
files = os.listdir(directory)
pictures = filter(lambda x: x.startswith('frames'), files)
#count=1
for file in pictures:
    #print(file)
    #count=parser(file)
    idplace, date, num_file = parser_date(file)
    print(idplace + '_' + str(date))
    num_dir = num_file = parser_time(num_file)
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
    num_dir = str(num_dir)
    num_dir = num_dir.replace(':', '.')
    success = vout.open('{id}.avi'.format(id=idplace+str(date)+'_'+str(num_dir)),fourcc,fps,capSize,True)
    _=[vout.write(i) for i in imgs]
    print("Видео файл успешно создан")
    cv2.destroyAllWindows()
    vout.release()
    #count+=1