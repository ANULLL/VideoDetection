import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets,QtGui,QtCore
import design1  # Это наш конвертированный файл дизайна
import threading
import Realease
import multiprocessing
import os
import easygui
import time
import asyncio
def expFunc(pathFile=None):
    #pathFile=easygui.fileopenbox(filetypes=["*.avi"])
    pathFile=easygui.fileopenbox(msg='Please choose a AVI file',default='', filetypes=['*.avi'],multiple=False)
    if pathFile is not None:
        try:
            out= Realease.prediction(pathFile)
            print(out)
        except ValueError:
            print("Wrong file or file name")
    else:
        print("None selected files")
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)

        msg.setText("None selected files")
        #msg.setInformativeText("This is additional information")
        msg.setWindowTitle("Error")
        #msg.setDetailedText("The details are as follows:")
        #msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        #msg.buttonClicked.connect(msgbtn)
        msg.exec_()
def predictScript(pathFile=None):
        # global out
        out = Realease.prediction(pathFile)
        print(out)

class ExampleApp(QtWidgets.QMainWindow, design1.Ui_MainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.StartBut.clicked.connect(self.thPredict) # обработчик нажатия на кнопку
        self.ExitBut.clicked.connect(self.exitScript)
        self.FileBut.clicked.connect(self.explScript)
        self.setWindowIcon(QtGui.QIcon('sber1.jpg'))
        self.listWidget.addItem("Дождитесь выполнения предсказания")



    def thPredict(self):
        self.StartBut.setEnabled(False)
        self.FileBut.setEnabled(False)
        start_time = time.time()
        #t=threading.Thread(target=predictScript)
        t=multiprocessing.Process(target=predictScript)
        #t.setDaemon(True) # Иначе не завершается при нажатии кнопки Exit
        #qeu.put_nowait(t)
        t.start()


        #time.sleep(100)
        b = True
        while (b):
            if (not t.is_alive()):
                b = False
                self.listWidget.addItem("--- %s seconds ---" % (time.time() - start_time))
                self.listWidget.addItem("Для новых предсказаний перезапустите программу")
       # b=True
       # while b:
        #    if qeu.empty():
        #        b=False
        #        self.listWidget.addItem("--- %s seconds ---" % (time.time() - start_time))
        #        self.listWidget.addItem("Для новых предсказаний перезапустите программу")

        #for th in threading.enumerate():  # ожидание всех потоков
         #   if th != threading.currentThread():
         #       th.join()
         #       self.listWidget.addItem("--- %s seconds ---" % (time.time() - start_time))
         #       self.listWidget.addItem("Для новых предсказаний перезапустите программу")
                #self.FileBut.setEnabled(True)
                #self.StartBut.setEnabled(True)


    def explScript(self):
        self.StartBut.setEnabled(False)
        self.FileBut.setEnabled(False)
        start_time = time.time()
        #t = threading.Thread(target=expFunc)

        t=multiprocessing.Process(target=expFunc)

        #t.setDaemon(True) # Иначе не завершается при нажатии кнопки Exit
        t.start()
        #time.sleep(100)
        b=True
        while(b):
            if (not t.is_alive()):
                b=False
                self.listWidget.addItem("--- %s seconds ---" % (time.time() - start_time))
                self.listWidget.addItem("Для новых предсказаний перезапустите программу")
        #for th in threading.enumerate():  # ожидание всех потоков
         #  if th != threading.currentThread():
          #      th.join()
           #     self.listWidget.addItem("--- %s seconds ---" % (time.time() - start_time))
            #    self.listWidget.addItem("Для новых предсказаний перезапустите программу")
                #self.FileBut.setEnabled(True)
                #self.StartBut.setEnabled(True)
    def exitScript(self):
        sys.exit()
        #exit()
def starApp():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение
def main():
    #starApp()
    mainThread=multiprocessing.Process(target=starApp())
    #mainThread=threading.Thread(target=starApp())
    mainThread.daemon=True
    mainThread.start()
    #mainThread.start()
if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()
