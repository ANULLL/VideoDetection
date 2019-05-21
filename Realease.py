import time
import SortVideoCut
import PredWithTime
import CreateNewCsv
def main():
    start_time = time.time()
    SortVideoCut.cutPred()
    PredWithTime.timePred()
    CreateNewCsv.csvPred()
    print("--- %s seconds ---" % (time.time() - start_time))
    return 0
def prediction (pathFile=None):
    start_time = time.time()
    SortVideoCut.cutPred(pathFile)
    PredWithTime.timePred()
    CreateNewCsv.csvPred()
    out="--- %s seconds ---" % (time.time() - start_time)
    print("--- %s seconds ---" % (time.time() - start_time))
    return out
if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()