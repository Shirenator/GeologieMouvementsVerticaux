import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import Back
import pickle
import Map
import Sheetchoice
import Coordinates
import ColorScale
import DisplayScale
import LocationRectangle
import re
import os
import PrintLocationCharacteristics
import CreateLocationWindow
from PySide.QtGui import *
from PySide.QtCore import *
from geomove import Ui_Geomove
from random import *

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
		self.readsave()
		self.colorScale = ColorScale.ColorScale(self)
		self.connectActions()


	#Connect items of the interface and fonctions
	def connectActions(self):
		#Menu
		self.actionQuit.triggered.connect(qApp.quit)
		self.actionNew_Map.triggered.connect(self.action_addMap)
		self.actionImport_locations.triggered.connect(self.action_addLocationExcel)
		self.actionImport_GSL.triggered.connect(self.action_GSL)
		self.actionDelete_Selected_Location.triggered.connect(self.action_deleteLocation)
		self.actionTuto.triggered.connect(self.action_tuto)
		self.actionExportMapPng.triggered.connect(self.action_ExportPng)
		self.action_ExportMaptxt.triggered.connect(self.action_ExportTxt)
		self.actionMVMScale.triggered.connect(self.action_scale)
		self.actionDisplay_scale.triggered.connect(self.action_displayScale)
		self.actionExport_scale.triggered.connect(self.action_ExportScale)
		self.actionAdd_coordinates.triggered.connect(self.action_AddCoordinates)
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
		self.action_confirmFilter()

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
			self.action_confirmFilter()

	#reset the scene for update
	def resetscene(self):
		ind = self.listMaps.currentIndex().row()
		scene = QGraphicsScene()
		mapsize = self.map.frameSize()
		mWid = mapsize.width()
		mHei = mapsize.height()
		pixmap = QPixmap.fromImage(self.mapsList[ind].im.scaled(mWid*self.mapsList[ind].zoom, mHei*self.mapsList[ind].zoom, Qt.KeepAspectRatio, Qt.SmoothTransformation))
		scene.addPixmap(pixmap)
		self.mapsList[ind].scene = scene
		self.map.setScene(self.mapsList[ind].scene)



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
						if(self.locCharac.gsls!=None and self.mapsList[index].coord()):
							self.printRect(self.mapsList[index], loc)
				except Exception as e:
					print(e)
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
								#print on the map
								if(self.locCharac.gsls!=None and self.mapsList[index].coord()):
									self.printRect(self.mapsList[index], loc)
				except Exception as e:
					print(e)
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
				#Add  methods names to Colorscale
				for gsl in gsls:
					name = "- " + gsl.method + " - " + gsl.method_name
					self.colorScale.addmethod(name)
				self.colorScale.indexmethod = 0
				#Update characteristics of the location
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
		msg.setInformativeText("Vertical movement results are now available for each point in the period corresponding to the imported file")
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
		self.resetscene()
		ind = self.listMaps.currentIndex().row()
		del self.mapsList[ind].locListFiltered [:]
		locations = self.mapsList[ind].locList
		for loc in locations:
			if(loc.age_min >= self.agemin.value() and loc.age_max <= self.agemax.value()):
				self.mapsList[ind].addlocFiltered(loc)
				item = QStandardItem(loc.name)
				self.modelloc.appendRow(item)
				if(self.locCharac.gsls!=None and self.mapsList[ind].coord()):
					self.printRect(self.mapsList[ind], loc)
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

	#Print the tutorial
	def action_tuto(self):
		qd = QDialog()
		qd.setWindowTitle("Tutorial")
		label = QLabel(qd)
   		pixmap = QPixmap("src/tuto.jpg")
   		label.setPixmap(pixmap)
   		hbox = QHBoxLayout()
		hbox.addWidget(label)
		qd.setLayout(hbox)
		qd.exec_()


	#Export the map with locations in png format
	def action_ExportPng(self):

		msg = QMessageBox()
		msg.setStandardButtons(QMessageBox.Ok)
		try:
			ind = self.listMaps.currentIndex().row()
			scene = self.mapsList[ind].scene
			img = QImage(scene.width(),scene.height(),QImage.Format_ARGB32_Premultiplied);
			p = QPainter(img);
			scene.render(p);
			p.end();
			img.save("Ressources\MapSave.png");
			#info message
			msg.setIcon(QMessageBox.Information)
			msg.setText("     Map exported !         ")
			msg.setWindowTitle("Exportation successfull")
			msg.setInformativeText("It has been saved in the Ressources Folder")
		except:
			#warning message
			msg.setIcon(QMessageBox.Warning)
			msg.setText("     No map to save !         ")
			msg.setWindowTitle("Export error")
			msg.setInformativeText("Please, select or create a map to export it")
		finally:
			msg.exec_()


	#Export the scale as png file
	def action_ExportScale(self):

		ds = DisplayScale.DisplayScale(self)
		scene = ds.scene
		scene.setBackgroundBrush(QBrush(Qt.white))
		img = QImage(scene.width(),scene.height(),QImage.Format_ARGB32_Premultiplied);
		p = QPainter(img);
		scene.render(p);
		p.end();
		img.save("Ressources\ScaleSave.png");
		#info message
		msg = QMessageBox()
		msg.setStandardButtons(QMessageBox.Ok)
		msg.setIcon(QMessageBox.Information)
		msg.setText("     Scale exported !         ")
		msg.setWindowTitle("Exportation successfull")
		msg.setInformativeText("It has been saved in the Ressources Folder")
		msg.exec_()


	#Window where the user can modify the color scale
	def action_scale(self):
		cs = self.colorScale.exec_()
		if (cs == QDialog.Accepted):
			self.colorScale.majSB()
			if(len(self.mapsList)>0):
				self.action_confirmFilter()
		else:
			self.colorScale.resetSB()

	#Print the scale
	def action_displayScale(self):
		ds = DisplayScale.DisplayScale(self)
		scale = ds.exec_()


	#Convert longitude / latitude in coordonate on the scene
	def getcoordonate(self, longi, lat, taille):

		ind = self.listMaps.currentIndex().row()
		longi = float(longi)
		lat = float(lat)
		coordXTopL = float(self.mapsList[ind].tlclon)
		coordYTopL = float(self.mapsList[ind].tlclat)
		coordXBotR = float(self.mapsList[ind].brclon)
		coordYBotR = float(self.mapsList[ind].brclat)

		x= abs(coordXTopL-longi)*(1.0*float(self.mapsList[ind].scene.width())/abs(coordXTopL-coordXBotR))
		y= abs(coordYTopL-lat)*(1.0*float(self.mapsList[ind].scene.height())/abs(coordYTopL-coordYBotR))
		x -= (taille/2)+(taille/4)
		y -= taille/4
		return [x,y]


	#Display location in parameter on the map according to its vertical movement
	def printRect(self, currentmap, loc):

		smin = self.colorScale.minScale
		smax = self.colorScale.maxScale
		taille = 40
		indexmethod = self.colorScale.indexmethod  + 1

		#get vertical movement values
		fvm = loc.vertical_movement(self.locCharac.gsls) #method, method_name, min, mean, max

		if(fvm[indexmethod][2]==None):	#No result
			mini = 99999
			mean = 99999
			maxi = 99999
		else:		#Results : min, mean, max
			mini = round(fvm[indexmethod][2],1)
			mean = round(fvm[indexmethod][3],1)
			maxi = round(fvm[indexmethod][4],1)

		#position in the scene of rectangles
		coord = self.getcoordonate(loc.longitude, loc.latitude, taille)
		x = coord[0]
		y = coord[1]

		itemmin = LocationRectangle.LocationRectangle(x,y,taille/2,taille/2, loc, self)
		item = LocationRectangle.LocationRectangle(x+taille/2,y,taille/2,taille/2, loc, self)
		itemmax = LocationRectangle.LocationRectangle(x+taille,y,taille/2,taille/2, loc, self)

		cmin = self.color(smin,smax, mini)
		c = self.color(smin,smax, mean)
		cmax = self.color(smin,smax, maxi)
		itemmin.setBrush(cmin)
		item.setBrush(c)
		itemmax.setBrush(cmax)
		currentmap.scene.addItem(itemmin)
		currentmap.scene.addItem(item)
		currentmap.scene.addItem(itemmax)


	#Return the color according to the vertical movement
	def color(self, scalemin, scalemax, value):

		scale = (scalemax-scalemin)*1.0
		if(value<scalemin+scale/10):
			return QColor(128,0,128,255)
		elif(value<scalemin+(scale/10)*2):
			return QBrush(Qt.darkBlue)
		elif(value<scalemin+(scale/10)*3):
			return QBrush(Qt.blue)
		elif(value<scalemin+(scale/10)*4):
			return QBrush(Qt.cyan)
		elif(value<scalemin+(scale/10)*5):
			return QBrush(Qt.green)
		elif(value<scalemin+(scale/10)*6):
			return QBrush(Qt.yellow)
		elif(value<scalemin+(scale/10)*7):
			return QColor(255,165,0,255)
		elif(value<scalemin+(scale/10)*8):
			return QBrush(Qt.red)
		elif(value<scalemin+(scale/10)*9):
			return QBrush(Qt.darkRed)
		elif(value==99999):
			return QBrush(Qt.darkGray)
		else:
			return QColor(88,41,0,255)


	#Save the data for the next launch of the software
	def save(self):
		#gsl
		savegsl = open("savegsl.txt",'wb')
		pickle.dump(self.locCharac.gsls,savegsl)
		savegsl.close()
		#maps
		savemaps = open("savemaps.txt",'wb')
		tabmapsave = []
		for m in self.mapsList:
			tabmapsave.append([m.fname,m.locList,m.tlclon,m.tlclat,m.brclon,m.brclat])
		pickle.dump(tabmapsave,savemaps)
		savemaps.close()

	#Export data of the current map in a txt file
	def action_ExportTxt(self):
		
		if(self.locCharac.gsls!=None and len(self.mapsList)>0):
			ind = self.listMaps.currentIndex().row()
			locs = self.mapsList[ind].locList
			f = open("Ressources\Exportfile.txt","a")
			for location in locs:
				fvms = location.vertical_movement(self.locCharac.gsls)
				
				ret = ""
				loc = fvms[0]
				ret = loc.name+"; "+str(loc.latitude)+"; "+str(loc.longitude)+"; "+str(loc.age_min)+"; "+str(loc.age_max)+"; "+str(loc.min_bathy)+"; "+str(loc.max_bathy)+"; "+str(loc.altitude)+"; "
				for i in range (1,len(fvms)):
					mov = fvms[i]
					for j in range(len(mov)):
						ret = ret+"; "+str(mov[j]).replace("\n"," ")
				f.write(ret)
				f.write("\n")
			f.close()
			#info message
			msg = QMessageBox()
			msg.setStandardButtons(QMessageBox.Ok)
			msg.setIcon(QMessageBox.Information)
			msg.setText("     Data exported !         ")
			msg.setWindowTitle("Exportation successfull")
			msg.setInformativeText("It has been saved in the Ressources Folder")
			msg.exec_()




	#Update the data with backup files
	def readsave(self):
		#gsl
		try:
			savegsl = open("savegsl.txt",'r')
			gsls = pickle.load(savegsl)
			savegsl.close()
			self.locCharac.gsls = gsls
		except:
			print("")

		#maps
		try:
			savemaps = open("savemaps.txt",'r')
			maps = pickle.load(savemaps)
			savemaps.close()
			for m in maps:

				ma = Map.Map(m[0], self.map)
				ma.locList += m[1]
				ma.tlclon = m[2]
				ma.tlclat = m[3]
				ma.brclon = m[4]
				ma.brclat = m[5]
				#Add to map list
				self.mapsList.append(ma)
				item = QStandardItem(ma.name)
				self.modelmaps.appendRow(item)
		except:
			print("")


	#Add longitude/latitude coordinate to the current map
	def action_AddCoordinates(self):
		coord = Coordinates.Coordinates(self)
		check = coord.exec_()
		if(check==QDialog.Accepted):
			ind = self.listMaps.currentIndex().row()
			self.mapsList[ind].tlclon = coord.tlclon.text()
			self.mapsList[ind].tlclat = coord.tlclat.text()
			self.mapsList[ind].brclon = coord.brclon.text()
			self.mapsList[ind].brclat = coord.brclat.text()


	#Show the interface
	def main(self):
		self.showMaximized()


#Main
if __name__ == '__main__':

	app = QApplication(sys.argv)
	mainWin = MainWindow()
	mainWin.main()
	ret = app.exec_()
	mainWin.save()
	sys.exit( ret )
