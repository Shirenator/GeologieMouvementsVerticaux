from PySide.QtGui import *
from PySide.QtCore import *

#Rectangle which represent location on the map 
class LocationRectangle(QGraphicsRectItem):

	#Constructeur
	def __init__(self, x,y,w,h, loc, mainw):
		QGraphicsRectItem.__init__(self,x,y,w,h)
		self.loc = loc
		self.mainw = mainw

	#When the user click on the rectangle, the location is selected in the location list
	def mousePressEvent(self, event):
	
		ind = self.mainw.listMaps.currentIndex().row()
		select = self.mainw.mapsList[ind].locListFiltered.index(self.loc)
		index = QModelIndex()
		index = self.mainw.modelloc.index(select, 0);
		self.mainw.listLocations.setCurrentIndex(index)
		self.mainw.onlocationSelected(index)
		return QGraphicsRectItem.mousePressEvent(self, event)
