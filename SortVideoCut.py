from PIL import Image,ImageOps
import pytesseract
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
    remove = text[0:text.find('\n') + 1:1]
    text=text.replace(remove,'')
    text = text.replace(':', '.')
    text=text.replace(' ','_')
    if (text.find('.') == 1):
        text = '0' + text
    print(text)
    return text
def parser_time(f):
    from datetime import time
    i=f.find('_')+1
    j=len(f)
    data=f[i:j:1]
    hour=data[0:2:1]
    minute=data[3:5:1]
    second=data[6:8:1]
    d=time(int(hour),int(minute),int(second))
    return d
def parser_date(f):
    from datetime import date
    i = f.find('_') + 1
    j = len(f)
    idplace=f[0:i:1]
    data = f[i:j:1]
    day = data[0:2:1]
    month = data[3:5:1]
    year = data[6:10:1]
    d = date(int(year),int(month),int(day))
    return idplace,d,data
def filter_time(f):
  from datetime import time
  b=True
  hour = f[0:2:1]
  minute = f[3:5:1]
  second = f[6:8:1]
  try:
    d = time(int(hour), int(minute), int(second))
  except ValueError:
    b=False
  return b
def filter_date(f):
  from datetime import date
  b=True
  day = f[9:11:1]
  month = f[12:14:1]
  year = f[15:len(f):1]
  try:
    d = date(int(year), int(month), int(day))
  except ValueError:
    b=False
  return b
def nn_filter (n_file):
    b=False
    if(n_file[0]=='0' and len(n_file)==19 and filter_date(n_file) and filter_time(n_file)):
        b=True
    return b
def main():
    from cv2 import VideoCapture,CAP_PROP_FPS,CAP_PROP_POS_FRAMES,imwrite
    from pathlib import Path
    from os import listdir,mkdir
    pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
    directory = Path.cwd()
    files = listdir(directory)
    videos = filter(lambda x: x.endswith('.avi'), files)
    num_file = 0
    for file in videos:
        i = 0
        print(file)
        idplace, date, num_file = parser_date(file)
        print(idplace + str(date))
        num_dir = num_file = parser_time(num_file)
        num_dir = str(num_dir)
        num_dir = num_dir.replace(':', '.')
        vidcap = VideoCapture(file)
        success, image = vidcap.read()
        fps = int(vidcap.get(CAP_PROP_FPS))
        print(fps)
        success = True
        # определим имя директории, которую создаём
        path = 'pictures{id}'.format(id='.' + idplace + str(date) + '_' + str(num_dir))

        try:
            mkdir(path)
        except OSError:
            print("Создать директорию %s не удалось" % path)
        else:
            print("Успешно создана директория %s " % path)
        while success:
            vidcap.set(CAP_PROP_POS_FRAMES, i * fps)
            success, image = vidcap.read()
            try:
                n_file = get_datetime(Image.fromarray(image))
            except AttributeError:
                break

            print('Read a new frame: ', success)
            if (nn_filter(n_file)):
                imwrite('pictures{id}/frame{time}.jpg'.format(id='.' + idplace + str(date) + '_' + str(num_dir),
                                                                  time='.' + idplace + str(n_file)), image)
            i += 1
    return 0
main()