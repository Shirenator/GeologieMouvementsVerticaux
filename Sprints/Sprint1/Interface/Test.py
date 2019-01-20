import sys

from PySide.QtGui import *
from PySide.QtCore import *
from geomove import Ui_Geomove


class MainWindow(QMainWindow, Ui_Geomove):

   def __init__(self):

       super(MainWindow, self).__init__()
       self.setupUi(self)
       self.show()

   

if __name__ == '__main__':

   app = QApplication(sys.argv)
   mainWin = MainWindow()
   ret = app.exec_()
   sys.exit( ret )
