def parser_date(f): # возвращает дату из формата год(четыре цифры)/месяц/лень
    from datetime import date
    i = f.find('_') + 1
    j = len(f)
    idplace=f[0:i:1]
    data = f[i:j:1]
    year=data[0:4:1]
    month=data[5:7:1]
    day=data[8:10:1]
    d = date(int(year),int(month),int(day))
    return idplace,d,data
def parser_time(f):#возвращает время из строки
    from datetime import time
    hour=f[0:2:1]
    minute=f[3:5:1]
    second=f[6:8:1]
    try:
        d=time(int(hour),int(minute),int(second))
    except ValueError:
        d=time(0,0,0)
    return d
def splitter (idplace):
    id1,id2=idplace.split('-')
    id2=id2.replace('_','')
    print(id1+ '  ' + id2)
    return id1,id2
def split_time(t):
    res = t.split('_')
    print(res[2])
    r = res[2].split('.')
    temp=r[0] + '.' + r[1]
    print(temp)
    return temp
def csvPred():# из посекундного файла формирует файл по минутам с предсказаниями
    from pathlib import Path
    from os import listdir
    from csv import writer,reader
    directory = Path.cwd()
    files = listdir(directory)
    TextFiles = filter(lambda x: x.startswith('frames.'), files)
    textFiles = list(filter(lambda x: x.endswith('.csv'), TextFiles))
    print(textFiles) # получаем список всех посекундных csv файлов

    for i in range(0, len(textFiles)):
        file_first = textFiles[i]
        FILENAME = textFiles[i]
        #print('File Name - ' + FILENAME)
        reg_time = split_time(FILENAME)
        idplace, date, num_file = parser_date(file_first)
        idplace = idplace.replace(idplace[0:idplace.find('.') + 1:1], '')
        id1, id2 = splitter(idplace)
        DataSet = list()
        with open(FILENAME, "r", newline="") as file:  ### жесткий костыль
            read = reader(file)
            for row in read:
                time = parser_time(row[2])
                minute = time.minute
                break
        countT = 0
        countF = 0
        with open(FILENAME, "r", newline="") as file:
            read = reader(file)
            try:
                begin_time = parser_time(row[2])
            except UnboundLocalError:
                break
            for row in read:
                # print(row[2], " - ", row[3])
                time = parser_time(row[2])
                # print(time.minute)
                if (minute == time.minute):
                    # print(row[3])
                    if ((row[3]) == "True"):
                        countT += 1
                    else:
                        countF += 1
                else:
                    # print("All ",int((countF+countT)*20/100)+1)
                    # print("true ",countT)
                    if (int((countF + countT) * 10 / 100) + 1 < countT):
                        pred = True
                    else:
                        pred = False
                    # print(countF, " + ", countT)
                    DataSet.append([id1,id2, row[1], str(time.hour) + ':' + str(time.minute), pred])
                    minute = time.minute
                    countT = 0
                    countF = 0
        #FILENAME = "{id}.csv".format(id=idplace + str(date) + '_' + str(begin_time.hour) + '.' + str(begin_time.minute))
        FILENAME = "{id}.csv".format(id=idplace + str(date) + '_' + reg_time)
        with open(FILENAME, "w", newline="") as file:
            writ = writer(file)
            writ.writerows(DataSet)
            print("Created csv file")
def main(): # аналогично предыдущей функции
    from pathlib import Path
    from os import listdir
    from csv import writer,reader
    directory = Path.cwd()
    files = listdir(directory)
    TextFiles = filter(lambda x: x.startswith('frames.'), files)
    textFiles = list(filter(lambda x: x.endswith('.csv'), TextFiles))
    print(textFiles) # получаем список всех посекундных csv файлов

    for i in range(0, len(textFiles)):
        file_first = textFiles[i]
        FILENAME = textFiles[i]
        #print('File Name - ' + FILENAME)
        reg_time=split_time(FILENAME)
        idplace, date, num_file = parser_date(file_first)
        idplace = idplace.replace(idplace[0:idplace.find('.') + 1:1], '')
        id1, id2 = splitter(idplace)
        DataSet = list()
        with open(FILENAME, "r", newline="") as file:  ### жесткий костыль
            read = reader(file)
            for row in read:
                time = parser_time(row[2])
                minute = time.minute
                break
        countT = 0
        countF = 0
        with open(FILENAME, "r", newline="") as file:
            read = reader(file)
            try:
                begin_time = parser_time(row[2])
            except UnboundLocalError:
                break
            for row in read:
                # print(row[2], " - ", row[3])
                time = parser_time(row[2])
                # print(time.minute)
                if (minute == time.minute):
                    # print(row[3])
                    if ((row[3]) == "True"):
                        countT += 1
                    else:
                        countF += 1
                else:
                    # print("All ",int((countF+countT)*20/100)+1)
                    # print("true ",countT)
                    if (int((countF + countT) * 10 / 100) + 1 < countT):
                        pred = True
                    else:
                        pred = False
                    # print(countF, " + ", countT)
                    DataSet.append([id1,id2, row[1], str(time.hour) + ':' + str(time.minute), pred])
                    minute = time.minute
                    countT = 0
                    countF = 0
        FILENAME = "{id}.csv".format(id=idplace + str(date) + '_' + reg_time)
        with open(FILENAME, "w", newline="") as file:
            writ = writer(file)
            writ.writerows(DataSet)
            print("Created csv file")
    return 0
#main()
if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()