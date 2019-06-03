from PIL import Image,ImageOps
import pytesseract
#import tesserocr
def get_datetime (img): # принимает картинку делает предсказание времени и даты с помощью tesseract

    from tempfile import mkdtemp,tempdir
    from os import rmdir
    im = img
    #im=im.filter(ImageFilter.UnsharpMask(radius=2,percent=150,threshold=3))
    im = im.resize((int(im.size[0]*0.8),int(im.size[1]*0.8))) #0.8 оставляет 80% пикселей картинке значительно ускоряет распознавание
                                                                # можно ставить и 0,7, но уже при 0,5 сильно проигрываем в точности
   # print("Size -",int(im.size[0]*0.8),' * ',int(im.size[1]*0.8))
    im = ImageOps.invert(im)
    im = im.convert("P")
    im2 = Image.new("L", im.size, 255)

    im = im.convert("P")

    temp = {}

    for x in range(im.size[1]): # получаем черно белую картинку, где черные пиксели, это все Белые пиксели в ИСХОДНОЙ картинке
        for y in range(im.size[0]):
            pix = im.getpixel((y, x))
            temp[pix] = pix
            if pix == 0:  # these are the numbers to get
                im2.putpixel((y, x), 0)

    td = mkdtemp()
    tempdir = td
    try: # удаляет временные файлы, немного ускоряет tesseract

    #api.SetImage(im2)
    #text=api.GetUTF8Text()
        #text = pytesseract.image_to_string(im2,lang=None,config='-c tessedit_char_whitelist=0123456789')
        text = pytesseract.image_to_string(im2, lang=None, config='digits')
    finally:
       rmdir(td)
       tempdir = None
    #print(text)
    remove = text[0:text.find('\n') + 1:1] # парсинг строки с предиктом, замена символов
    text=text.replace(remove,'')
    text = text.replace(':', '.')
    text=text.replace(' ','_')
    if (text.find('.') == 1): # на камере время в формате 9.00.00, превратит его в 09.00.00 для универсальности
        text = '0' + text
    text=text.replace(',','.') #для грязных предиктов
    text=text[0:19:1]
    print(text)
    return text # возвращаем готовый предикт с датой и временем
def parser_time(f): # выделяет из строки время в формате 09:00:00
    from datetime import time
    i=f.find('_')+1
    j=len(f)
    data=f[i:j:1]
    hour=data[0:2:1]
    minute=data[3:5:1]
    second=data[6:8:1]
    d=time(int(hour),int(minute),int(second))
    return d
def parser_date(f): # выделяет из строки дату в формате день/месяц/год(четыре цифры)
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
def filter_time(f): # возвращает True если возможно преобразовать строку во время
  from datetime import time
  b=True
  if ( (not f[2]=='.') or (not f[5]=='.')):
      b=False
  hour = f[0:2:1]
  minute = f[3:5:1]
  second = f[6:8:1]
  try:
    d = time(int(hour), int(minute), int(second))
  except ValueError:
    b=False
  return b
def filter_date(f):# возвращает True если возможно преобразовать строку в дату
  from datetime import date
  b=True
  day = f[9:11:1]
  month = f[12:14:1]
  #year = f[15:len(f):1]
  year = f[15:19:1]
  try:
    d = date(int(year), int(month), int(day))
  except ValueError:
    b=False
  return b
def nn_filter (n_file): # проверка предикта нейросети на корректность по дате и времени, чтобы записать картинку
    b=False
    try:
        #if (len(n_file) == 19 and filter_date(n_file) and filter_time(n_file)):
        if(filter_time(n_file)):
        #if (filter_date(n_file) and filter_time(n_file)):
            b=True
    except IndexError:
        b=False
    return b
def cutPred(pathFile=None): # нарезает видео на картинки по одному кадру в секунду, сохраняет их в названии используя предсказание
                            #нейросети с временем и датой, если оно некорректно картинка не сохраняется
    from cv2 import VideoCapture,CAP_PROP_FPS,CAP_PROP_POS_FRAMES,imwrite
    from pathlib import Path
    from os import listdir,mkdir,path
    pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe' # путь до тессеракта, может быть другим (:-
    #api = tesserocr.PyTessBaseAPI(path='C:\\Program Files\\Tesseract-OCR\\tessdata')
    if pathFile is None: #получает путь к файлу из проводника, если проводник не использовался
                        # выполняется поиск всех .avi файлов лежащих в каталоге с проектом
        directory = Path.cwd()
        files = listdir(directory)
        videos = filter(lambda x: x.endswith('.avi'), files)
    else:
        files = path.basename(pathFile)
        print(files)
        #videos = filter(lambda x: x.endswith('.avi'), files)
        videos=[files]
        print(videos)
    num_file = 0
    for file in videos: # для каждого найденного файла открываем его как видео и нарезаем на кадры
        i = 0
        print(file)
        idplace, date, num_file = parser_date(file)
        #print(idplace + str(date))
        num_dir = num_file = parser_time(num_file)
        num_dir = str(num_dir)
        num_dir = num_dir.replace(':', '.')
        if pathFile is None:
            vidcap = VideoCapture(file)
        else:
            vidcap=VideoCapture(pathFile)
        success, image = vidcap.read()
        fps = int(vidcap.get(CAP_PROP_FPS))
        #print(fps)
        success = True
        # определим имя директории, которую создаём
        path = 'pictures{id}'.format(id='.' + idplace + str(date) + '_' + str(num_dir))

        try:
            mkdir(path)
        except OSError:
            #print("Создать директорию %s не удалось" % path)
            printed="Создать директорию %s не удалось" % path
            print(printed)
        else:
            #print("Успешно создана директория %s " % path)
            printed="Успешно создана директория %s " % path
            print(printed)
        while success:
            vidcap.set(CAP_PROP_POS_FRAMES, i * fps) # переходим по кадрам умножаяя текущий кадр на количество кадров в секунду
                                                    # то есть берем один кадр в секунду
            success, image = vidcap.read()
            try:
                n_file = get_datetime(Image.fromarray(image))
            except AttributeError:
                break

            print('Read a new frame: ', success)
            if (nn_filter(n_file)):
                #n_file=n_file[0:19:1]
                #print(n_file)
                imwrite('pictures{id}/frame{time}.jpg'.format(id='.' + idplace + str(date) + '_' + str(num_dir),
                                                                  time='.' + idplace + str(n_file)), image)
            i += 1
def main(pathFile=None): # аналогично предыдущий функции, но сработает при запуске скрипта
    from cv2 import VideoCapture,CAP_PROP_FPS,CAP_PROP_POS_FRAMES,imwrite
    from pathlib import Path
    from os import listdir,mkdir
    pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
    #api = tesserocr.PyTessBaseAPI(path='C:\\Program Files\\Tesseract-OCR\\tessdata')
    if pathFile is None:
        directory = Path.cwd()
        files = listdir(directory)
        videos = filter(lambda x: x.endswith('.avi'), files)
    else:
        directory=pathFile
        files = listdir(directory)
        videos = filter(lambda x: x.endswith('.avi'), files)
    num_file = 0
    for file in videos:
        i = 0
        print(file)
        idplace, date, num_file = parser_date(file)
        #print(idplace + str(date))
        num_dir = num_file = parser_time(num_file)
        num_dir = str(num_dir)
        num_dir = num_dir.replace(':', '.')
        vidcap = VideoCapture(file)
        success, image = vidcap.read()
        fps = int(vidcap.get(CAP_PROP_FPS))
        #print(fps)
        success = True
        # определим имя директории, которую создаём
        path = 'pictures{id}'.format(id='.' + idplace + str(date) + '_' + str(num_dir))

        try:
            mkdir(path)
        except OSError:
            #print("Создать директорию %s не удалось" % path)
            printed="Создать директорию %s не удалось" % path
            print(printed)
        else:
            #print("Успешно создана директория %s " % path)
            printed="Успешно создана директория %s " % path
            print(printed)
        while success:
            vidcap.set(CAP_PROP_POS_FRAMES, i * fps)
            success, image = vidcap.read()
            try:
                n_file = get_datetime(Image.fromarray(image))
            except AttributeError:
                break

            print('Read a new frame: ', success)
            if (nn_filter(n_file)):
                #n_file=n_file[0:19:1]
                #print(n_file)
                imwrite('pictures{id}/frame{time}.jpg'.format(id='.' + idplace + str(date) + '_' + str(num_dir),
                                                                  time='.' + idplace + str(n_file)), image)
            i += 1
    #api.End()
    return 0
if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()