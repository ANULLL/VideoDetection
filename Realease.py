import time
import SortVideoCut
import PredWithTime
import CreateNewCsv
from easygui import fileopenbox
def main():
    start_time = time.time()
    pathFile = fileopenbox(msg='Please choose a AVI file', default='', filetypes=['*.avi'], multiple=False)
    SortVideoCut.cutPred(pathFile)
    PredWithTime.timePred()
    CreateNewCsv.csvPred()
    out = "--- %s seconds ---" % (time.time() - start_time)
    my_file = open("result.txt", "w")
    my_file.write(out)
    my_file.close()
    print("--- %s seconds ---" % (time.time() - start_time))
    return 0
def prediction (pathFile=None):
    start_time = time.time()
    SortVideoCut.cutPred(pathFile)
    PredWithTime.timePred()
    CreateNewCsv.csvPred()
    out="--- %s seconds ---" % (time.time() - start_time)
    my_file = open("result.txt", "w")
    my_file.write(out)
    my_file.close()
    print("--- %s seconds ---" % (time.time() - start_time))
    return out
if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()