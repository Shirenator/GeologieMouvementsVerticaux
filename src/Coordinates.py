from PySide.QtGui import *
from PySide.QtCore import *

#Window for the user-entered location creation
class Coordinates(QDialog):

	#constructor
	def __init__(self, mainw, parent=None):

		super(Coordinates, self).__init__(parent)

		self.mainw = mainw
		self.setWindowTitle("Add Coordinates")
		mainLayout = QVBoxLayout()
		h1 = QHBoxLayout()
		h2 = QHBoxLayout()
		
		lab1 = QLabel("Top left corner of the map (decimal) :")
		lab1.setAlignment(Qt.AlignCenter)
		lab2 = QLabel("Bottom right corner of the map (decimal) :")
		lab2.setAlignment(Qt.AlignCenter)
		lab3 = QLabel("Longitude :")
		lab4 = QLabel("Latitude :")
		lab5 = QLabel("Longitude :")
		lab6 = QLabel("Latitude :")

		self.tlclon = QLineEdit()
		self.tlclat = QLineEdit()
		self.brclon = QLineEdit()
		self.brclat = QLineEdit()
		
		h1.addWidget(lab3)
		h1.addWidget(self.tlclon)
		h1.addWidget(lab4)
		h1.addWidget(self.tlclat)
		
		h2.addWidget(lab5)
		h2.addWidget(self.brclon)
		h2.addWidget(lab6)
		h2.addWidget(self.brclat)
		
		mainLayout.addWidget(lab1)
		mainLayout.addLayout(h1)
		mainLayout.addWidget(lab2)
		mainLayout.addLayout(h2)
		
		self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
		self.buttonBox.accepted.connect(self.accept)
		self.buttonBox.rejected.connect(self.reject)
		mainLayout.addWidget(self.buttonBox)
		self.setLayout(mainLayout)
		
		#Connection check
		self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
		self.tlclon.textChanged.connect(self.checkEmpty)
		self.tlclat.textChanged.connect(self.checkEmpty)
		self.brclon.textChanged.connect(self.checkEmpty)
		self.brclat.textChanged.connect(self.checkEmpty)
		
		
		#Check if a lineEdit is empty
	def checkEmpty(self):
		if(self.tlclon.text()=="" or self.tlclat.text()=="" or self.brclon.text()=="" or self.brclat.text()==""):
			flag = False
		else:
			flag = True
		self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(flag)
		
		
		
		
