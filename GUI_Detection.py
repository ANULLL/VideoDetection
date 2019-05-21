import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets,QtGui,QtCore
import design1  # Это наш конвертированный файл дизайна
import threading
import Realease
import multiprocessing
import os
import easygui

def predictScript(pathFile=None):
   # global out
    out=Realease.prediction(pathFile)
    print(out)



class ExampleApp(QtWidgets.QMainWindow, design1.Ui_MainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.StartBut.clicked.connect(self.thPredict) # обработчик нажатия на кнопку
        self.ExitBut.clicked.connect(self.exitScript)
        self.setWindowIcon(QtGui.QIcon('sber.jpg'))


    def thPredict(self):
        self.StartBut.setEnabled(False)
        t=threading.Thread(target=predictScript)
        #t=multiprocessing.Process(target=predictScript)
        t.setDaemon(True)
        #t.run()
        t.start()
        #t.join()
        #res=t.join()
        #self.listWidget.addItem(res)
       # while t.is_alive():
               #res=t.join()
               #if (res is not None):
        #        self.StartBut.setEnabled(True)
                #self.listWidget.addItem(res)
         #      t.kill()

    def exitScript(self):
        #sys.exit()
        file = easygui.fileopenbox(filetypes=["*.avi","*.mp4"])
        print(file)
        t = threading.Thread(target=predictScript(file))
        # t=multiprocessing.Process(target=predictScript)
        t.setDaemon(True)
        # t.run()
        t.start()
        #exit()
def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение
    #mainThread=threading.Thread(target=app.exec())
    #mainThread.setDaemon(True)
    #mainThread.start()
if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()