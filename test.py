from yolo import YOLO, detect_video
from PIL import Image
import os
import cv2
import datetime as dt
import matplotlib.pylab as plt
import csv
#import VideoCut
try:
    from pathlib import Path
except ImportError:             # Python 2
    from pathlib2 import Path
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
    year=data[0:4:1]
    month=data[5:7:1]
    day=data[8:10:1]
    #day = data[0:2:1]
    #month = data[3:5:1]
    #year = data[6:10:1]
    d = dt.date(int(year),int(month),int(day))
    return idplace,d,data
def get_client (pred):
    count=0
    i=0
    while (i<len(pred) and count<2 ):
       if(pred[i][1] == 0.0) : # 0 - идентификатор класса person (человек)
           count+=1
           #print(pred[i])
       #print(pred[i][1])
       i+=1
    #print(count)
    if count>=2 :
        return True #клиент/клиенты есть в кадре
    else :
        return False # в кадре только оператор или нет людей
def get_images(place):
    directory = Path.cwd()
    files = os.listdir(directory)
    pictures = filter(lambda x: x.startswith('frames.'+place), files)
    count=0
    for file in pictures:
        if count==0 :
            file_first=file
        # print(file)
        # count=parser(file)
        #idplace, date, num_file = parser_date(file)
        #print(idplace + '_' + str(date))
        #num_dir = num_file = parser_time(num_file)
        # print(count)
        # читаем кадры
        p = (str(directory) + '/' + file)
        p = Path(p)
        print(p)
        count+=1
        imgs = [cv2.imread(str(f)) for f in p.glob('*.jpg')]
    return imgs,file_first

model = YOLO()
#img = Image.open("/Users/maksimpolakov/PycharmProjects/untitled/venv/VideoDetection-master/frame_placeid_2019-04-05_09:25:17.jpg")
##изображение
place="placeid2"
images,first=get_images(place)
idplace,date,num_file=parser_date(first)
num_dir=num_file=parser_time(num_file)
FILENAME = "{id}.csv".format(id=first)
PredictSet=list()
for i in range(0,len(images)):
    try:
        img=Image.fromarray(images[i])
    except AttributeError:
        break
    out = model.detect_image(img)
    detect=get_client(out)
    print(detect)
    idplace = idplace.replace(idplace[0:idplace.find('.') + 1:1], '')
    idplace = idplace.replace('_', '')
    PredictSet.append([idplace,date,num_file,detect])
    num_file = correct_time(num_file)
model.close_session()
with open(FILENAME, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(PredictSet)
    print("Created csv file")

#print(first)['{id}'.format(id=idplace+str(date)+'_'+str(num_dir)),detect]
#idplace,date,num_file=parser_date(first)
#num_file=parser_time(num_file)
#last = correct_time(num_file,count)
#last=idplace+str(date)+'_'+str(last)
#print(last)


##видос(массив в строку весь возвращается - я поправлю)

#res = detect_video(model,"frames.placeid_2019-04-05_08:42:51.avi")
