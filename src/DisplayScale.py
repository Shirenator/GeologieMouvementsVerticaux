from PySide.QtGui import *
from PySide.QtCore import *


#Scale of vertical movements colors
class DisplayScale(QDialog):

	#constructor
	def __init__(self, main, parent=None):

		super(DisplayScale, self).__init__()
		self.setWindowTitle("Scale")
		self.view = QGraphicsView(self)
		self.main = main
		self.scene = QGraphicsScene()
		self.updateScale()
		
		
	#Update the scale when the scale settings are modified
	def updateScale(self):
	
		scene = QGraphicsScene()
		smin = self.main.colorScale.minScale
		smax = self.main.colorScale.maxScale
		val = smax*1.0
		y = 10
		#Color scale
		while(val>smin+1):
			
			item = QGraphicsRectItem(0,y,40,40)
			item.setBrush(self.main.color(smin,smax,val-1))
			scene.addItem(item)
			lab = QGraphicsTextItem()
			lab = scene.addText(str(val))
			lab.setPos(45,y-12)
			val -= (smax-smin)/10.0
			y += 40
			
		lab = QGraphicsTextItem()
		lab = scene.addText(str(val))
		lab.setPos(45,y-12)
		self.view.setScene(scene)
		self.scene = scene
		self.resize(scene.width(),scene.height())
