def parser_date(f):
    from datetime import date
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
    d = date(int(year),int(month),int(day))
    return idplace,d,data
def parser_time(f):
    from datetime import time
    #i=f.find('_')+1
    #j=len(f)
    #data=f[i:j:1]
    hour=f[0:2:1]
    minute=f[3:5:1]
    second=f[6:8:1]
    d=time(int(hour),int(minute),int(second))
    return d
def main():
    from pathlib import Path
    from os import listdir
    from csv import writer,reader
    directory = Path.cwd()
    files = listdir(directory)
    TextFiles = filter(lambda x: x.startswith('frames.'), files)
    textFiles = list(filter(lambda x: x.endswith('.csv'), TextFiles))
    print(textFiles)

    for i in range(0, len(textFiles)):
        file_first = textFiles[i]
        FILENAME = textFiles[i]
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
            begin_time = parser_time(row[2])
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
                    DataSet.append([row[0], row[1], str(time.hour) + ':' + str(time.minute), pred])
                    minute = time.minute
                    countT = 0
                    countF = 0
        idplace, date, num_file = parser_date(file_first)
        idplace = idplace.replace(idplace[0:idplace.find('.') + 1:1], '')
        idplace = idplace.replace('_', '')
        FILENAME = "{id}.csv".format(id=idplace + str(date) + '_' + str(begin_time.hour) + '.' + str(begin_time.minute))
        with open(FILENAME, "w", newline="") as file:
            writ = writer(file)
            writ.writerows(DataSet)
            print("Created csv file")
    return 0
main()