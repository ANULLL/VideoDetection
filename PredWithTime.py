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
def parser_csv (f):
    i = f.find('_') + 1
    j = len(f)
    idplace = f[0:i-1:1]
    data = f[i:j:1]
    time=data[0:8:1]
    data=data[9:len(data):1]
    return idplace,data,time
def main():
    from cv2 import imread
    from yolo import YOLO
    from os import listdir
    from pathlib import Path
    from csv import writer
    from PIL import Image
    model = YOLO()
    # place="9013-423"
    directory = Path.cwd()
    files = listdir(directory)
    pictures = filter(lambda x: x.startswith('pictures.'), files)
    pictures = list(pictures)
    print(pictures)
    # print(first)
    for i in range(0, len(pictures)):
        first = pictures[i]
        p = (str(directory) + '/' + first)
        p = Path(p)
        print(p)
        files = listdir(p)
        name = pictures[i].replace('pictures.', 'frames.')
        print(name)
        FILENAME = "{id}.csv".format(id=name)
        PredictSet = list()

        count = 1
        for f in p.glob('*.jpg'):

            try:
                imgs = imread(str(f))
                date = files[count]
                date = date.replace('frame.', '')
                date = date.replace('.jpg', '')
                idplace, date, time = parser_csv(date)
                img = Image.fromarray(imgs)
                count += 1
            except AttributeError:
                break
            except IndexError:
                break
            out = model.detect_image(img)
            detect = get_client(out)
            print(detect)
            PredictSet.append([idplace, date, time, detect])

        with open(FILENAME, "w", newline="") as file:
            writ = writer(file)
            writ.writerows(PredictSet)
            print("Created csv file")
    model.close_session()
    return 0
main()