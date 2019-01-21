import sys
import Back
import CreateLocationWindow
from PySide.QtGui import *
from PySide.QtCore import *
from geomove import Ui_Geomove

#Main window
class MainWindow(QMainWindow, Ui_Geomove):

	#Constructor
	def __init__(self):

		super(MainWindow, self).__init__()
		self.setupUi(self)
		self.modelmaps = QStandardItemModel(self.listMaps)
		self.listMaps.setModel(self.modelmaps)
		self.modelloc = QStandardItemModel(self.listLocations)
		self.listLocations.setModel(self.modelloc)
		self.locwindow = CreateLocationWindow.CreateLocationWindow(self)
		self.connectActions()
		
	#Connect items of the interface and fonctions
	def connectActions(self):
		self.actionQuit.triggered.connect(qApp.quit)
		self.actionNew_Map.triggered.connect(self.action_addMap)
		self.addMap.clicked.connect(self.action_addMap)
		self.addLocation.clicked.connect(self.action_addLocation)

	#####Sprint2
	#Add a map on the interface
	def action_addMap(self):
		
		item = QStandardItem("MapExample")
		self.modelmaps.appendRow(item)
	#####

	#Add a location on the application
	def action_addLocation(self):

		self.locwindow.clearLineEdit()
		dialogCode = self.locwindow.exec_()
		#If Ok--> new location create
		if (dialogCode == QDialog.Accepted): 
			loc = Back.Location(self.locwindow.name.text(),self.locwindow.lat.text(),self.locwindow.lon.text(),self.locwindow.mina.text(),self.locwindow.maxa.text(),self.locwindow.minb.text(),self.locwindow.maxb.text(),self.locwindow.alt.text())
			item = QStandardItem(loc.name)
			self.modelloc.appendRow(item)

	#Show the interface
	def main(self):
		self.show()

   
#Main
if __name__ == '__main__':

	app = QApplication(sys.argv)
	mainWin = MainWindow()
	mainWin.main()
	ret = app.exec_()
	sys.exit( ret )




