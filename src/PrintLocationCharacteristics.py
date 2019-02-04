from PySide.QtGui import *
from PySide.QtCore import *
import Back


#Right QListView for print informations of the selected location
class PrintLocationCharacteristics(QWidget):

	#constructor
	def __init__(self, loccar, parent=None):

		super(PrintLocationCharacteristics, self).__init__()
		self.mylist = []
		self.modelcarac = QStandardItemModel(loccar)
		self.gsls = None;
		loccar.setModel(self.modelcarac)
		
	def updategsl(self, gsl):
		self.gsls = gsl	
	

	def updateloc(self, loc):
		self.modelcarac.clear()
		item1 = QStandardItem("Name : " + loc.name)
		item2 = QStandardItem("Latitude : " + str(loc.latitude))
		item3 = QStandardItem("Longitude : " + str(loc.longitude))
		item4 = QStandardItem("Altitude : " + str(loc.altitude))
		item5 = QStandardItem("Minimal Age : " + str(loc.age_min))
		item6 = QStandardItem("Maximal Age : " + str(loc.age_max))
		item7 = QStandardItem("Minimal Bathymetry : " + str(loc.min_bathy))
		item8 = QStandardItem("Maximal Bathymetry : " + str(loc.max_bathy))
		
		self.modelcarac.appendRow(item1)
		self.modelcarac.appendRow(item2)
		self.modelcarac.appendRow(item3)
		self.modelcarac.appendRow(item4)
		self.modelcarac.appendRow(item5)
		self.modelcarac.appendRow(item6)
		self.modelcarac.appendRow(item7)
		self.modelcarac.appendRow(item8)
		
		#Calcul and print movements	
		item = QStandardItem("\nVerticals Movements :")
		self.modelcarac.appendRow(item)	
		
		if(self.gsls==None):		#if no gsl file imported
			item9 = QStandardItem("## No GSL file find ##")
			self.modelcarac.appendRow(item9)
		else:		#if gsl file imported
		
			fvm = loc.vertical_movement(self.gsls) #method, method_name, min, mean, max
			for i in range(1,len(fvm)):
				
				item10 = QStandardItem("\nMethod : "+ fvm[i][0])
				item11 = QStandardItem("Method name : "+ fvm[i][1])
				self.modelcarac.appendRow(item10)
				self.modelcarac.appendRow(item11)
	
				if(fvm[i][2]==None):	#No result
					item12 = QStandardItem("## No valid data for this method ##")
					self.modelcarac.appendRow(item12)
				else:		#Results : min, mean, max
					item12 = QStandardItem("Min : "+ str(fvm[i][2]))
					item13 = QStandardItem("Mean : "+ str(fvm[i][3]))
					item14 = QStandardItem("Max : "+ str(fvm[i][4]))
					self.modelcarac.appendRow(item12)
					self.modelcarac.appendRow(item13)
					self.modelcarac.appendRow(item14)
	
		
		
		
		
		
		
		
		
	
