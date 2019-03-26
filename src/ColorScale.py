from PySide.QtGui import *
from PySide.QtCore import *


#Settings window for color scale
class ColorScale(QDialog):

	#constructor
	def __init__(self, mainw, parent=None):

		super(ColorScale, self).__init__()
		self.setWindowTitle("Scale settings")
		self.minScale=-250
		self.maxScale=250
		self.methods = []
		self.resize(500,400)
			
		#layout
		v1 = QVBoxLayout()
		v2 = QVBoxLayout()
		v3 = QVBoxLayout()
		h1 = QHBoxLayout()
		minlab = QLabel("Minimum scale ")
		maxlab = QLabel(" Maximum scale")
		self.minsb = QSpinBox()
		self.maxsb = QSpinBox()
      	
      	#Widgets
		v1.addWidget(minlab)
		v1.addWidget(self.minsb)
		v2.addWidget(maxlab)
		v2.addWidget(self.maxsb)
		h1.addLayout(v1)
		h1.addLayout(v2)
		v3.addLayout(h1)
		
		self.minsb.setMaximum(500)
		self.minsb.setMinimum(-1000)
		self.maxsb.setMaximum(1000)
		self.maxsb.setMinimum(-500)
		self.resetSB()
		
		#Creation of the list of methods
		self.methodList = QListView();
		self.model = QStandardItemModel(self.methodList)
		self.methodList.setModel(self.model)
		
		#Creation of the Form
		v3.addWidget(QLabel("Choose the method to use :"))
		v3.addWidget(self.methodList)
		
		buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
		buttonBox.accepted.connect(self.accept)
		buttonBox.rejected.connect(self.reject)
		v3.addWidget(buttonBox)
		self.setLayout(v3)
		
		gsls = mainw.locCharac.gsls
		if(gsls==None):
			self.indexmethod = -1
		else:
			#Add  methods names to Colorscale
			for gsl in gsls:
				name = "- " + gsl.method + " - " + gsl.method_name
				self.addmethod(name)
			self.indexmethod = 0
		
     	
	#add method to the list of method
	def addmethod(self, m):
		self.methods.append(m)
		item = QStandardItem(m)
		self.model.appendRow(item)
	
	#Reset spin box at their value when the user cancel the window
	def resetSB(self):
		self.maxsb.setProperty("value", self.maxScale)
		self.minsb.setProperty("value", self.minScale)
		
	#Update the current min and max scale
	def majSB(self):
		self.minScale=self.minsb.value()
		self.maxScale=self.maxsb.value()
		if(self.indexmethod!=-1):
			self.indexmethod = max(0,self.methodList.currentIndex().row())
		
		
