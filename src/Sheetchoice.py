from PySide.QtGui import *
from PySide.QtCore import *
import xlrd

#Window for choose the sheet of the imported Excel file
class Sheetchoice(QDialog):

	#constructor
	def __init__(self, mainw, filepath, parent=None):

		super(Sheetchoice, self).__init__(parent)

		self.mainw = mainw
		self.setWindowTitle("Sheet choice")
		self.resize(500,400);

		#Creation of the list of sheet
		self.sheetList = QListView();
		self.model = QStandardItemModel(self.sheetList)
		self.sheetList.setModel(self.model)
		self.sl = []
		
		xls = xlrd.open_workbook(filepath)
		sheets = xls.sheet_names()
		for s in sheets:
		
			item = QStandardItem(s)
			self.model.appendRow(item)
			self.sl.append(s)

		#Creation of the Form
		vbox = QVBoxLayout()
		vbox.addWidget(QLabel("Choose the sheet to import :"))
		vbox.addWidget(self.sheetList)
		
		#Button box
		buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
		buttonBox.accepted.connect(self.accept)
		buttonBox.rejected.connect(self.reject)
		vbox.addWidget(buttonBox)
		self.setLayout(vbox)
		
	


