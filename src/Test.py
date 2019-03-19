import sys
import Back
import Map
import Sheetchoice
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
		#Menu
		self.actionQuit.triggered.connect(qApp.quit)
		self.actionNew_Map.triggered.connect(self.action_addMap)
		self.actionSave.triggered.connect(self.action_save)
		self.actionImport_locations.triggered.connect(self.action_addLocationExcel)
		self.actionImport_GSL.triggered.connect(self.action_GSL)
		self.actionDelete_Selected_Location.triggered.connect(self.action_deleteLocation)
		self.actionTuto.triggered.connect(self.action_tuto)
		self.actionExportMapPng.triggered.connect(self.action_ExportPng)
		self.action_ExportMaptxt.triggered.connect(self.action_ExportTxt)
		self.actionExportMapExcel.triggered.connect(self.action_ExportExcel)
		#Buttons
		self.addMap.clicked.connect(self.action_addMap)
		self.addLocation.clicked.connect(self.action_addLocation)
		self.ConfirmationFilter.clicked.connect(self.action_confirmFilter)
		self.Zoomin.clicked.connect(self.zoomIn)
		self.Zoomout.clicked.connect(self.zoomOut)

		#Lists
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
			
			
			
	def ajouterPoint(self):

		print "ajoutPoint"

		ind = self.listMaps.currentIndex().row()
		pix = self.mapsList[ind].im
		w_pix, h_pix = self.mapsList[ind].pixmap.width(), self.mapsList[ind].pixmap.height()

		mapsize = self.map.frameSize()
		mWid = mapsize.width()
		mHei = mapsize.height()
		x,y,w_scene,h_scene = self.map.geometry().getRect()

		oSceneX = x-1
		oSceneY = y-25-2

		margeX = (w_scene-w_pix)/2
		margeY = (h_scene-h_pix)/2

		oMapX = oSceneX - margeX
		oMapY = oSceneY - margeY

		################################### TEST #################################
		####### a tester avec de coordonnées ca marche surement pas mais bon #####

		# me faut les coordonnées de l'angle en haut a gauche et en bas a droite
		
		coorXdTopL = 52000
		coorYdTopL = 52000

		coordXBotR = 92000
		coordYBotR = 92000

		# coordonnées du points en question
		
		coordXPoint = 70000
		coordYPoint = 70000
		
		lon = w_pix - (w_pix*((coordXBotR-coordXPoint)/(coordXBotR-coorXdTopL)))
		lar = h_pix - (h_pix*((coordYBotR-coordYPoint)/(coordYBotR-coorYdTopL)))

		posPointX = oSceneX + lon
		posPointY = oSceneY + lar

		print(lon)
		print(lar)
		
		# dessiner le rectangle ici,
		# utiliser lon et lar
		
		item = QGraphicsRectItem(lar,lon,25,25)
		item.setBrush(QBrush(Qt.Red))
		currentmap.scene.addItem(item)

		###########################################################################



	#Add a location on the application
	def action_addLocation(self):

		if not self.mapsList:
			self.ErrorNoMap()
		else:
			self.locwindow.clearLineEdit()
			dialogCode = self.locwindow.exec_()
			#If Ok--> new location create
			if (dialogCode == QDialog.Accepted):
				try: 
					loc = Back.Location(self.locwindow.name.text(),float(self.locwindow.lat.text()),float(self.locwindow.lon.text()),float(self.locwindow.mina.text()),float(self.locwindow.maxa.text()),float(self.locwindow.minb.text()),float(self.locwindow.maxb.text()),float(self.locwindow.alt.text()))
					index = self.listMaps.currentIndex().row()
					self.mapsList[index].addloc(loc)
					if(loc.age_min >= self.agemin.value() and loc.age_max <= self.agemax.value()):
						self.mapsList[index].addlocFiltered(loc)
						item = QStandardItem(loc.name)
						self.modelloc.appendRow(item)
				except:
					self.ErrorCreationLocation()
			
		
	#Add locations on the application from Excel data
	def action_addLocationExcel(self):
	
		if not self.mapsList:
			self.ErrorNoMap()
		else:
			fname = QFileDialog.getOpenFileName(self, 'Open file','c:\\',"Calc files (*.ods *.xls *.xlsx)")
			if fname[0]:		#if user choose file in the window (#fname[0] = absolute path of excel file)
				try:
					direc = QDir(QDir.currentPath()) #Test.py path directory
					filedir = direc.relativeFilePath(fname[0])	#filedir = relative path of excel file
					sheet = self.sheetChoice(filedir)
					if(sheet!="cancel"):
						locations = Back.read_locations(filedir,sheet)		
						#Add to Location list
						index = self.listMaps.currentIndex().row()
						for loc in locations:
							self.mapsList[index].addloc(loc)
							if(loc.age_min >= self.agemin.value() and loc.age_max <= self.agemax.value()):
								self.mapsList[index].addlocFiltered(loc)
								item = QStandardItem(loc.name)
								self.modelloc.appendRow(item)
				except:
					self.ErrorImportation()


	#Message when user try to create locations before creation of map
	def ErrorNoMap(self):
		msg = QMessageBox()
		msg.setIcon(QMessageBox.Warning)
		msg.setText("     No map available !         ")
		msg.setInformativeText("Please, create a map before create locations")
		msg.setWindowTitle("No map error")
		msg.setStandardButtons(QMessageBox.Ok)
		msg.exec_()
		
	#Message when user try to create location with wrong format
	def ErrorCreationLocation(self):
		msg = QMessageBox()
		msg.setIcon(QMessageBox.Warning)
		msg.setText("     Incorrect information entered !         ")
		msg.setInformativeText("Please, create a location with this format :\n\nName : String \n\t-Example : foo\n\nOther informations : Float or int \n\t-Example 1 : 52.16\n\t-Example 2 : 64")
		msg.setWindowTitle("Creation error")
		msg.setStandardButtons(QMessageBox.Ok)
		msg.exec_()


	#Add Global sea level data from Excel file
	def action_GSL(self):
		fname = QFileDialog.getOpenFileName(self, 'Open file','c:\\',"Calc files (*.ods *.xls *.xlsx)")
		if fname[0]:		#If user choose a file (#fname[0] = absolute path of Excel file)
			try:
				direc = QDir(QDir.currentPath()) #path of Test.py
				filedir = direc.relativeFilePath(fname[0])	#filedir = relative path of Excel file
				gsls = Back.read_gsl(filedir,0)
				self.locCharac.updategsl(gsls)
				self.GSLFileMessage()
			except:
				self.ErrorImportation()

	#Message when user import a Excel file with wronf format
	def ErrorImportation(self):
		msg = QMessageBox()
		msg.setIcon(QMessageBox.Warning)
		msg.setText("     Wrong Excel file format !         ")
		msg.setInformativeText("Please, refer to the Excel examples provided with the software to create an Excel file to be imported into the software")
		msg.setWindowTitle("Wrong Excel file")
		msg.setStandardButtons(QMessageBox.Ok)
		msg.exec_()
		
	
	#Message when user import GSL File with good format
	def GSLFileMessage(self):
		msg = QMessageBox()
		msg.setIcon(QMessageBox.Information)
		msg.setText("     GSL File imported !         ")
		msg.setInformativeText("Vertical motion results are now available for each point in the period corresponding to the imported file")
		msg.setWindowTitle("Importation successfull")
		msg.setStandardButtons(QMessageBox.Ok)
		msg.exec_()
	

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

	#Delete the selected location
	def action_deleteLocation(self):
		try:
			indmap = self.listMaps.currentIndex().row()
			indloc = self.listLocations.currentIndex().row()
			self.mapsList[indmap].deleteLoc(indloc)
			self.action_confirmFilter()
		except:
			msg = QMessageBox()
			msg.setIcon(QMessageBox.Warning)
			msg.setText("     No location found !         ")
			msg.setInformativeText("Please, select a location to delete")
			msg.setWindowTitle("No location")
			msg.setStandardButtons(QMessageBox.Ok)
			msg.exec_()
	
	#Choice of the sheet of the import Excel file	
	def sheetChoice(self, filepath):
		sc = Sheetchoice.Sheetchoice(self, filepath)
		dc = sc.exec_()
		if (dc == QDialog.Accepted):
			ind = sc.sheetList.currentIndex().row()
			sheetname = sc.sl[ind]
			return sheetname
		else:
			return("cancel")
	
	#Save of data
	def action_save(self):
		print("save")

	#Print the tutorial
	def action_tuto(self):
		qd = QDialog()
		qd.setWindowTitle("Tutorial")
		label = QLabel(qd)
   		pixmap = QPixmap("tuto.jpg")
   		label.setPixmap(pixmap)
   		hbox = QHBoxLayout()
		hbox.addWidget(label)
		qd.setLayout(hbox)
		qd.exec_()
		
		
		
	#Export the map in png format
	def action_ExportPng(self):
		print("PNG")
		
	#Export the data of the selected map in a txt file
	def action_ExportTxt(self):
		print("txt")

	#Export the data of the selected map in a Excel file
	def action_ExportExcel(self):
		print("Excel")


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

