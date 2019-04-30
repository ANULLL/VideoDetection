import cv2
import matplotlib.pyplot as plt
import os
import datetime as dt
from pathlib import Path
def correct_time(time): # добавляем секунду каждому кадру и корректируем остальное время
    h =time.hour
    m=time.minute
    s=time.second
    s+=1
    if s>=60:
        m+= 1
        s= s % 60
    if m>=60:
        h+= 1
        m= m % 60
    if h>=24:
        h=0
        m=0
        s=0
    time=time.replace(hour=h,minute=m,second=s)
    return time
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
    day = data[0:2:1]
    month = data[3:5:1]
    year = data[6:10:1]
    d = dt.date(int(year),int(month),int(day))
    return idplace,d,data
# path to video files
directory=Path.cwd()
files = os.listdir(directory)
videos = filter(lambda x: x.endswith('.mp4'), files)
num_file=0
for file in videos:
    i=0
    print(file)
    idplace,date,num_file=parser_date(file)
    print(idplace+str(date))
    num_dir=num_file=parser_time(num_file)
    num_dir=str(num_dir)
    num_dir=num_dir.replace(':','.')
    vidcap = cv2.VideoCapture(file)
    success, image = vidcap.read()
    fps=int(vidcap.get(cv2.CAP_PROP_FPS))
    print(fps)
    success = True
    # определим имя директории, которую создаём
    path = 'frames{id}'.format(id='.'+idplace+str(date)+'_'+str(num_dir))

    try:
        os.mkdir(path)
    except OSError:
        print("Создать директорию %s не удалось" % path)
    else:
        print("Успешно создана директория %s " % path)
    while success:
        vidcap.set(cv2.CAP_PROP_POS_FRAMES, i*fps)
        success, image = vidcap.read()
        print('Read a new frame: ', success)
          # save frame as JPEG file
        n_file = str(num_file)
        n_file = n_file.replace(':', '.')
        cv2.imwrite('frames{id}/frame{time}.jpg'.format(id='.'+idplace+str(date)+'_'+str(num_dir),time='_'+idplace+str(date)+'_'+str(n_file)), image)
        i+=1
        num_file = correct_time(num_file)

    #num_file+=1