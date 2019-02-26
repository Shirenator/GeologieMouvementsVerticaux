import sys
import Back
import Map
import re
import os
import PrintLocationCharacteristics
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
		self.locCharac = PrintLocationCharacteristics.PrintLocationCharacteristics(self.characteristics)
		self.mapsList = []
		self.connectActions()
		
		
	#Connect items of the interface and fonctions
	def connectActions(self):
		self.actionQuit.triggered.connect(qApp.quit)
		self.actionNew_Map.triggered.connect(self.action_addMap)
		self.actionImport_locations.triggered.connect(self.action_addLocationExcel)
		self.actionImport_GSL.triggered.connect(self.action_GSL)
		self.addMap.clicked.connect(self.action_addMap)
		self.addLocation.clicked.connect(self.action_addLocation)
		self.ConfirmationFilter.clicked.connect(self.action_confirmFilter)
		self.Zoomin.clicked.connect(self.zoomIn)
		self.Zoomout.clicked.connect(self.zoomOut)

		#connect lists
		self.listLocations.clicked.connect(self.onlocationSelected)
		self.listMaps.clicked.connect(self.action_confirmFilter)


	#Add a map on the interface
	def action_addMap(self):
		
		fname = QFileDialog.getOpenFileName(self, 'Open file','c:\\',"geoTIFF files (*.tif *.tiff)")
		if fname[0]:
		
			m = Map.Map(fname, self.map)
			#Add to map list
			self.mapsList.append(m)
			item = QStandardItem(m.name)
			self.modelmaps.appendRow(item)
	
	#Zoom the map	
	def zoomIn(self):

		ind = self.listMaps.currentIndex().row()
		
		self.mapsList[ind].zoom *= 2
		scene = QGraphicsScene()
		mapsize = self.map.frameSize()
		mWid = mapsize.width()
		mHei = mapsize.height()
		w_pix, h_pix = self.mapsList[ind].pixmap.width(), self.mapsList[ind].pixmap.height()
		pixmap = QPixmap.fromImage(self.mapsList[ind].im.scaled(mWid*self.mapsList[ind].zoom, mHei*self.mapsList[ind].zoom, Qt.KeepAspectRatio, Qt.SmoothTransformation))
		scene.setSceneRect(0, 0, w_pix*self.mapsList[ind].zoom, h_pix*self.mapsList[ind].zoom)
		scene.addPixmap(pixmap)
		self.mapsList[ind].scene = scene
		self.map.setScene(self.mapsList[ind].scene)
		self.map.repaint()
		self.map.show()
        	
	#Unzoom the map
	def zoomOut(self):

		ind = self.listMaps.currentIndex().row()
		if self.mapsList[ind].zoom > 1:
			
		
			self.mapsList[ind].zoom *= 0.5
			scene = QGraphicsScene()
			mapsize = self.map.frameSize()
			mWid = mapsize.width()
			mHei = mapsize.height()
			w_pix, h_pix = self.mapsList[ind].pixmap.width(), self.mapsList[ind].pixmap.height()
			pixmap = QPixmap.fromImage(self.mapsList[ind].im.scaled(mWid*self.mapsList[ind].zoom, mHei*self.mapsList[ind].zoom, Qt.KeepAspectRatio, Qt.SmoothTransformation))
			scene.setSceneRect(0, 0, w_pix*self.mapsList[ind].zoom, h_pix*self.mapsList[ind].zoom)
			scene.addPixmap(pixmap)
			self.mapsList[ind].scene = scene
			self.map.setScene(self.mapsList[ind].scene)
			self.map.repaint()
			self.map.show()


	#Add a location on the application
	def action_addLocation(self):

		self.locwindow.clearLineEdit()
		dialogCode = self.locwindow.exec_()
		#If Ok--> new location create
		if (dialogCode == QDialog.Accepted): 
			loc = Back.Location(self.locwindow.name.text(),float(self.locwindow.lat.text()),float(self.locwindow.lon.text()),float(self.locwindow.mina.text()),float(self.locwindow.maxa.text()),float(self.locwindow.minb.text()),float(self.locwindow.maxb.text()),float(self.locwindow.alt.text()))
			index = self.listMaps.currentIndex().row()
			self.mapsList[index].addloc(loc)
			if(loc.age_min >= self.agemin.value() and loc.age_max <= self.agemax.value()):
				self.mapsList[index].addlocFiltered(loc)
				item = QStandardItem(loc.name)
				self.modelloc.appendRow(item)
			
		

	#Add locations on the application from Excel data
	def action_addLocationExcel(self):
		fname = QFileDialog.getOpenFileName(self, 'Open file','c:\\',"Calc files (*.ods *.xls *.xlsx)")
		if fname[0]:		#if user choose file in the window (#fname[0] = absolute path of excel file)
			direc = QDir(QDir.currentPath()) #Test.py path directory
			filedir = direc.relativeFilePath(fname[0])	#filedir = relative path of excel file
			locations = Back.read_locations(filedir,'PIACENZIAN_FVM')		
			#Add to Location list
			index = self.listMaps.currentIndex().row()
			for loc in locations:
				self.mapsList[index].addloc(loc)
				if(loc.age_min >= self.agemin.value() and loc.age_max <= self.agemax.value()):
					self.mapsList[index].addlocFiltered(loc)
					item = QStandardItem(loc.name)
					self.modelloc.appendRow(item)


	#Add Global sea level data from Excel file
	def action_GSL(self):
		fname = QFileDialog.getOpenFileName(self, 'Open file','c:\\',"Calc files (*.ods *.xls *.xlsx)")
		if fname[0]:		#If user choose a file (#fname[0] = absolute path of Excel file)
			direc = QDir(QDir.currentPath()) #path of Test.py
			filedir = direc.relativeFilePath(fname[0])	#filedir = relative path of Excel file
			gsls = Back.read_gsl(filedir,0)
			self.locCharac.updategsl(gsls)

	#Print characteristics of the selected location
	def onlocationSelected(self, index):
		ind = self.listMaps.currentIndex().row()
		loc = self.mapsList[ind].locListFiltered[index.row()]	
		self.locCharac.updateloc(loc)

		
	#Confirmation of the filter or selection of a map
	def action_confirmFilter(self):
		self.modelloc.clear()
		ind = self.listMaps.currentIndex().row()
		del self.mapsList[ind].locListFiltered [:]
		locations = self.mapsList[ind].locList
		for loc in locations:
			if(loc.age_min >= self.agemin.value() and loc.age_max <= self.agemax.value()):
				self.mapsList[ind].addlocFiltered(loc)
				item = QStandardItem(loc.name)
				self.modelloc.appendRow(item)
		#Map View
		self.map.setScene(self.mapsList[ind].scene)


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

