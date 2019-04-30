from yolo import YOLO
from PIL import Image,ImageOps
import os
import cv2
import datetime as dt
import csv
from pathlib import Path
import pytesseract
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
def parser_date(f):
    i = f.find('_') + 1
    j = len(f)
    idplace=f[0:i:1]
    data = f[i:j:1]
    year=data[0:4:1]
    month=data[5:7:1]
    day=data[8:10:1]
    d = dt.date(int(year),int(month),int(day))
    return idplace,d,data
def get_client (pred):
    count=0
    i=0
    while (i<len(pred) and count<2 ):
       if(pred[i][1] == 0.0) : # 0 - идентификатор класса person (человек)
           count+=1
       i+=1
    if count>=2 :
        return True #клиент/клиенты есть в кадре
    else :
        return False # в кадре только оператор или нет людей
def get_datetime (img):
    im = img
    im = ImageOps.invert(im)
    im = im.convert("P")
    im2 = Image.new("P", im.size, 255)

    im = im.convert("P")

    temp = {}

    for x in range(im.size[1]):
        for y in range(im.size[0]):
            pix = im.getpixel((y, x))
            temp[pix] = pix
            if pix == 0:  # these are the numbers to get
                im2.putpixel((y, x), 0)

    text = pytesseract.image_to_string(im2)
    print(text)
    text = text.replace('\n', '_')
    text = text.replace(':', '.')
    text = text.replace(' ', '_')
    remove = text[0:text.find('_') + 1:1]
    text = text.replace(remove, '')
    remove = text[0:text.find('_') + 1:1]
    text = text.replace(remove, '')
    if (text.find('.') == 1):
        text = '0' + text
    return text
place="9013-423(1)"
directory = Path.cwd()
files = os.listdir(directory)
pictures = filter(lambda x: x.startswith('frames.'+place), files)
count=0
for file in pictures:
    if count==0 :
        first=file
        break
print(first)
idplace,date_old,num_file=parser_date(first)
FILENAME = "{id}.csv".format(id=first)
PredictSet=list()
model = YOLO()
p = (str(directory) + '/' + file)
p = Path(p)
print(p)
for f in p.glob('*.jpg'):


        try:
            imgs = cv2.imread(str(f))
            img=Image.fromarray(imgs)
            date=get_datetime(img)
        except AttributeError:
                happy=False
                break
        out = model.detect_image(img)
        detect=get_client(out)
        print(detect)
        idplace = idplace.replace(idplace[0:idplace.find('.') + 1:1], '')
        idplace = idplace.replace('_', '')

        PredictSet.append([idplace, date, detect])
model.close_session()
with open(FILENAME, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(PredictSet)
    print("Created csv file")
