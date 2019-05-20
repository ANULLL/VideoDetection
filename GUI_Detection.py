import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets
import design1  # Это наш конвертированный файл дизайна
import threading
import Realease

def predictScript():
   # global out
    out=Realease.prediction()
    print(out)
class ExampleApp(QtWidgets.QMainWindow, design1.Ui_MainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.StartBut.clicked.connect(self.thPredict) # обработчик нажатия на кнопку
        self.ExitBut.clicked.connect(self.exitScript)



    def thPredict(self):
        self.StartBut.setEnabled(False)
        t=threading.Thread(target=predictScript)
        t.setDaemon(True)
        t.start()
        #t.join()
        self.listWidget.addItem('Hell')
        if not t.isAlive():
               self.StartBut.setEnabled(True)

    def exitScript(self):
        sys.exit()
def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()