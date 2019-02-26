from PySide.QtGui import *
from PySide.QtCore import *


#Map imported by user and which contain a list of Locations
class Map:

	#constructor
	def __init__(self, fname, wmap):

		# on recupere le chemin, le passe en str, et on nomme la map
		fulldir=fname[0]
		#fulldir.type()
		fulldir.encode('ascii','ignore')
		fulldir.encode('ascii','replace')
		#fulldir.decode()
		fulldirsplit=fulldir.split('/')
		self.name = fulldirsplit[-1]
		
		mapsize = wmap.frameSize()
		mWid = mapsize.width()
		mHei = mapsize.height()
		self.im = QImage(fname[0])
		self.zoom = 1
		self.pixmap = pixmap = QPixmap.fromImage(self.im.scaled(mWid, mHei, Qt.KeepAspectRatio, Qt.SmoothTransformation))
		self.scene = QGraphicsScene()
		w_pix, h_pix = self.pixmap.width(), self.pixmap.height()
		self.scene.setSceneRect(0, 0, w_pix, h_pix)
		self.scene.addPixmap(self.pixmap)
		self.locList = []			#All locations of the map
		self.locListFiltered = []		#All locations displayed with the filter
		#importation fichier geotif
		
	def addloc(self, loc):
		self.locList.append(loc)
		
	def addlocFiltered(self, loc):
		self.locListFiltered.append(loc)
