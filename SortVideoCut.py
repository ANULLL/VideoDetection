import cv2
import os
import datetime as dt
from pathlib import Path
from PIL import Image,ImageOps
import pytesseract
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
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
directory=Path.cwd()
files = os.listdir(directory)
videos = filter(lambda x: x.endswith('.avi'), files)
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
        n_file=get_datetime(Image.fromarray(image))
        print('Read a new frame: ', success)
        if(n_file[0]=='0'):

          # save frame as JPEG file
        #n_file = str(num_file)
        #n_file = n_file.replace(':', '.')
            cv2.imwrite('frames{id}/frame{time}.jpg'.format(id='.'+idplace+str(date)+'_'+str(num_dir),time='_'+idplace+str(n_file)), image)
        i+=1
        #num_file = correct_time(num_file)