import sys
import Back
import PrintLocationCharacteristics
import CreateLocationWindow
import re
import os
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
		self.locCharac = PrintLocationCharacteristics.PrintLocationCharacteristics(self.characteristics)
		self.locs = []
		self.connectActions()
		self.zoom = 1
		self.scene = QGraphicsScene()
		self.im1 = QImage()
		

		
	#Connect items of the interface and fonctions
	def connectActions(self):
		self.actionQuit.triggered.connect(qApp.quit)
		self.actionNew_Map.triggered.connect(self.action_addMap)
		self.actionImport_locations.triggered.connect(self.action_addLocationExcel)
		self.actionImport_GSL.triggered.connect(self.action_GSL)
		self.addMap.clicked.connect(self.action_addMap)
		self.addLocation.clicked.connect(self.action_addLocation)

		#connect the list of Locations
		self.listLocations.clicked.connect(self.onlocationSelected)



	##########
	#Add a map on the interface
	def action_addMap(self):		
		

		fname = QFileDialog.getOpenFileName(self, 'Open file','c:\\',"TIF Files (*.TIF)")
		if fname[0]:


			mapsize = self.map.frameSize()
			mWid = mapsize.width()
			mHei = mapsize.height()
			im0 = QImage(fname[0])
			self.im1 = QImage(fname[0])			

			pixmap = QPixmap.fromImage(im0.scaled(mWid, mHei, Qt.KeepAspectRatio, Qt.SmoothTransformation))
			w_pix, h_pix = pixmap.width(), pixmap.height()

			self.scene.setSceneRect(0, 0, w_pix, h_pix)
			self.scene.addPixmap(pixmap)
			#self.map.setSceneRect(0, 0, w_pix, h_pix)
			self.map.setScene(self.scene)

			# on recupere le chemin, le passe en str, et l'ajoute dans la liste des maps
			fulldir=fname[0]
			#fulldir.type()
			#fulldir.encode('ascii','ignore')
			#fulldir.encode('ascii','replace')
			fulldir.decode()
			fulldirsplit=fulldir.split('/')

			nameMap = fulldirsplit[-1]
			item = QStandardItem(nameMap)
			self.modelmaps.appendRow(item)


	def zoomIn(self):

		self.scene = QGraphicsScene()
		mapsize = self.map.frameSize()
		mWid = mapsize.width()
		mHei = mapsize.height()
		im0 = self.im1
		pixmap = QPixmap.fromImage(im0.scaled(mWid, mHei, Qt.KeepAspectRatio, Qt.SmoothTransformation))
		w_pix, h_pix = pixmap.width(), pixmap.height()

		self.zoom = self.zoom * 2
		pixmap = QPixmap.fromImage(im0.scaled(mWid*self.zoom, mHei*self.zoom, Qt.KeepAspectRatio, Qt.SmoothTransformation))
		self.scene.setSceneRect(0, 0, w_pix*self.zoom, h_pix*self.zoom)
		self.scene.addPixmap(pixmap)
		self.map.setScene(self.scene)

        	self.map.repaint()
        	self.map.show()

	def zoomOut(self):

		self.scene = QGraphicsScene()
		mapsize = self.map.frameSize()
		mWid = mapsize.width()
		mHei = mapsize.height()
		im0 = self.im1
		pixmap = QPixmap.fromImage(im0.scaled(mWid, mHei, Qt.KeepAspectRatio, Qt.SmoothTransformation))
		w_pix, h_pix = pixmap.width(), pixmap.height()
		
		if self.zoom > 1:
			self.zoom = self.zoom * 0.5

			pixmap = QPixmap.fromImage(im0.scaled(mWid*self.zoom, mHei*self.zoom, Qt.KeepAspectRatio, Qt.SmoothTransformation))
			self.scene.setSceneRect(0, 0, w_pix*self.zoom, h_pix*self.zoom)
			self.scene.addPixmap(pixmap)
			self.map.setScene(self.scene)

			self.map.repaint()
			self.map.show()





	##########

	#Add a location on the application
	def action_addLocation(self):

		self.locwindow.clearLineEdit()
		dialogCode = self.locwindow.exec_()
		#If Ok--> new location create
		if (dialogCode == QDialog.Accepted): 
			loc = Back.Location(self.locwindow.name.text(),float(self.locwindow.lat.text()),float(self.locwindow.lon.text()),float(self.locwindow.mina.text()),float(self.locwindow.maxa.text()),float(self.locwindow.minb.text()),float(self.locwindow.maxb.text()),float(self.locwindow.alt.text()))
			self.locs.append(loc)
			item = QStandardItem(loc.name)
			self.modelloc.appendRow(item)
		

	#Add locations on the application from Excel data
	def action_addLocationExcel(self):
		fname = QFileDialog.getOpenFileName(self, 'Open file','c:\\',"Calc files (*.ods *.xls *.xlsx)")
		if fname[0]:		#si l utilisateur a choisi un fichier dans  explorateur (#fname[0] = chemin absolu du fichier excel)
			direc = QDir(QDir.currentPath()) #chemin de Test.py
			filedir = direc.relativeFilePath(fname[0])	#filedir = chemin relatif du fichier excel
			locations = Back.read_locations(filedir,'PIACENZIAN_FVM')		
			#Ajouter aux points deja presents
			self.locs = self.locs + locations
			for loc in locations:
				item = QStandardItem(loc.name)
				self.modelloc.appendRow(item)


	#Add Global sea level data from Excel file
	def action_GSL(self):
		fname = QFileDialog.getOpenFileName(self, 'Open file','c:\\',"Calc files (*.ods *.xls *.xlsx)")
		if fname[0]:		#si l utilisateur a choisi un fichier dans  explorateur (#fname[0] = chemin absolu du fichier excel)
			direc = QDir(QDir.currentPath()) #chemin de Test.py
			filedir = direc.relativeFilePath(fname[0])	#filedir = chemin relatif du fichier excel
			gsls = Back.read_gsl(filedir,0)
			self.locCharac.updategsl(gsls)

	#print the characteristics of the selected location
	def onlocationSelected(self, index):
		loc = self.locs[index.row()]	
		self.locCharac.updateloc(loc)


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

