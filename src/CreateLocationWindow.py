
from PySide.QtGui import *
from PySide.QtCore import *
import Back

#Window for the user-entered location creation
class CreateLocationWindow(QDialog):

	#constructor
	def __init__(self, mainw, parent=None):

		super(CreateLocationWindow, self).__init__(parent)

		self.mainw = mainw
		self.setWindowTitle("Add Location")
		self.resize(500,400);
		self.formGroupBox = QGroupBox("Location characteristics")

		self.name = QLineEdit()
		self.lat = QLineEdit()
		self.lon = QLineEdit()
		self.mina = QLineEdit()
		self.maxa = QLineEdit()
		self.minb = QLineEdit()
		self.maxb = QLineEdit()
		self.alt = QLineEdit()

		#Creation of the Form
		layout = QFormLayout()
		layout.addRow(QLabel("Name:"), self.name)
		layout.addRow(QLabel("Latitude:"), self.lat)
		layout.addRow(QLabel("Longitude:"), self.lon)
		layout.addRow(QLabel("Minimum age:"), self.mina)
		layout.addRow(QLabel("Maximum age:"), self.maxa)
		layout.addRow(QLabel("Minimum bathymetry:"), self.minb)
		layout.addRow(QLabel("Maximum bathymetry:"), self.maxb)
		layout.addRow(QLabel("Altitude:"), self.alt)

		self.formGroupBox.setLayout(layout)
		buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
		buttonBox.accepted.connect(self.accept)
		buttonBox.rejected.connect(self.reject)
		mainLayout = QVBoxLayout()
		mainLayout.addWidget(self.formGroupBox)
		mainLayout.addWidget(buttonBox)
		self.setLayout(mainLayout)
		

	#Clear all LineEdits
	def clearLineEdit(self):
		self.name.clear()
		self.lat.clear()
		self.lon.clear()
		self.mina.clear()
		self.maxa.clear()
		self.minb.clear()
		self.maxb.clear()
		self.alt.clear()


		
