# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'geomove.ui'
#
# Created: Mon Mar 25 13:08:31 2019
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Geomove(object):
    def setupUi(self, Geomove):
        Geomove.setObjectName("Geomove")
        Geomove.resize(1009, 741)
        self.centralwidget = QtGui.QWidget(Geomove)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.MainWindowLayout = QtGui.QHBoxLayout()
        self.MainWindowLayout.setSpacing(6)
        self.MainWindowLayout.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
        self.MainWindowLayout.setObjectName("MainWindowLayout")
        self.Data = QtGui.QVBoxLayout()
        self.Data.setObjectName("Data")
        self.addMap = QtGui.QPushButton(self.centralwidget)
        self.addMap.setObjectName("addMap")
        self.Data.addWidget(self.addMap)
        self.listMaps = QtGui.QListView(self.centralwidget)
        self.listMaps.setEnabled(True)
        self.listMaps.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.listMaps.setObjectName("listMaps")
        self.Data.addWidget(self.listMaps)
        self.addLocation = QtGui.QPushButton(self.centralwidget)
        self.addLocation.setObjectName("addLocation")
        self.Data.addWidget(self.addLocation)
        self.Filter = QtGui.QVBoxLayout()
        self.Filter.setSpacing(0)
        self.Filter.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
        self.Filter.setObjectName("Filter")
        self.Filtervalues = QtGui.QHBoxLayout()
        self.Filtervalues.setSpacing(3)
        self.Filtervalues.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.Filtervalues.setObjectName("Filtervalues")
        self.agemin = QtGui.QDoubleSpinBox(self.centralwidget)
        self.agemin.setMaximumSize(QtCore.QSize(85, 16777215))
        self.agemin.setPrefix("")
        self.agemin.setMaximum(99.99)
        self.agemin.setSingleStep(0.1)
        self.agemin.setObjectName("agemin")
        self.Filtervalues.addWidget(self.agemin)
        self.Tiret = QtGui.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.Tiret.setFont(font)
        self.Tiret.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.Tiret.setTextFormat(QtCore.Qt.AutoText)
        self.Tiret.setWordWrap(False)
        self.Tiret.setMargin(0)
        self.Tiret.setObjectName("Tiret")
        self.Filtervalues.addWidget(self.Tiret)
        self.agemax = QtGui.QDoubleSpinBox(self.centralwidget)
        self.agemax.setMaximumSize(QtCore.QSize(85, 16777215))
        self.agemax.setMaximum(250.0)
        self.agemax.setSingleStep(0.1)
        self.agemax.setProperty("value", 250.0)
        self.agemax.setObjectName("agemax")
        self.Filtervalues.addWidget(self.agemax)
        self.Filtervalues.setStretch(0, 1)
        self.Filtervalues.setStretch(2, 1)
        self.Filter.addLayout(self.Filtervalues)
        self.ConfirmationFilter = QtGui.QPushButton(self.centralwidget)
        self.ConfirmationFilter.setObjectName("ConfirmationFilter")
        self.Filter.addWidget(self.ConfirmationFilter)
        self.Data.addLayout(self.Filter)
        self.listLocations = QtGui.QListView(self.centralwidget)
        self.listLocations.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.listLocations.setObjectName("listLocations")
        self.Data.addWidget(self.listLocations)
        self.Zoom = QtGui.QHBoxLayout()
        self.Zoom.setObjectName("Zoom")
        self.Zoomout = QtGui.QPushButton(self.centralwidget)
        self.Zoomout.setObjectName("Zoomout")
        self.Zoom.addWidget(self.Zoomout)
        self.Zoomin = QtGui.QPushButton(self.centralwidget)
        self.Zoomin.setObjectName("Zoomin")
        self.Zoom.addWidget(self.Zoomin)
        self.Data.addLayout(self.Zoom)
        self.Data.setStretch(1, 1)
        self.Data.setStretch(4, 2)
        self.MainWindowLayout.addLayout(self.Data)
        self.MapScreen = QtGui.QVBoxLayout()
        self.MapScreen.setObjectName("MapScreen")
        self.map = QtGui.QGraphicsView(self.centralwidget)
        self.map.setObjectName("map")
        self.MapScreen.addWidget(self.map)
        self.MainWindowLayout.addLayout(self.MapScreen)
        self.Characteristics = QtGui.QVBoxLayout()
        self.Characteristics.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.Characteristics.setObjectName("Characteristics")
        self.characteristics = QtGui.QListView(self.centralwidget)
        self.characteristics.setLineWidth(1)
        self.characteristics.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.characteristics.setSelectionRectVisible(True)
        self.characteristics.setObjectName("characteristics")
        self.Characteristics.addWidget(self.characteristics)
        self.MainWindowLayout.addLayout(self.Characteristics)
        self.MainWindowLayout.setStretch(0, 1)
        self.MainWindowLayout.setStretch(1, 7)
        self.MainWindowLayout.setStretch(2, 2)
        self.horizontalLayout.addLayout(self.MainWindowLayout)
        Geomove.setCentralWidget(self.centralwidget)
        self.menuBar = QtGui.QMenuBar(Geomove)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1009, 25))
        self.menuBar.setObjectName("menuBar")
        self.menu_File = QtGui.QMenu(self.menuBar)
        self.menu_File.setEnabled(True)
        self.menu_File.setObjectName("menu_File")
        self.menu_Edition = QtGui.QMenu(self.menuBar)
        self.menu_Edition.setObjectName("menu_Edition")
        self.menu_Settings = QtGui.QMenu(self.menuBar)
        self.menu_Settings.setObjectName("menu_Settings")
        self.menu_Help = QtGui.QMenu(self.menuBar)
        self.menu_Help.setObjectName("menu_Help")
        Geomove.setMenuBar(self.menuBar)
        self.actionNew_Map = QtGui.QAction(Geomove)
        self.actionNew_Map.setObjectName("actionNew_Map")
        self.action_Open_Map = QtGui.QAction(Geomove)
        self.action_Open_Map.setEnabled(True)
        self.action_Open_Map.setObjectName("action_Open_Map")
        self.action = QtGui.QAction(Geomove)
        self.action.setObjectName("action")
        self.actionSave = QtGui.QAction(Geomove)
        self.actionSave.setObjectName("actionSave")
        self.actionSave_as = QtGui.QAction(Geomove)
        self.actionSave_as.setObjectName("actionSave_as")
        self.actionQuit = QtGui.QAction(Geomove)
        self.actionQuit.setCheckable(False)
        self.actionQuit.setObjectName("actionQuit")
        self.actionChange_language = QtGui.QAction(Geomove)
        self.actionChange_language.setObjectName("actionChange_language")
        self.actionImport_locations = QtGui.QAction(Geomove)
        self.actionImport_locations.setObjectName("actionImport_locations")
        self.actionChange_scale = QtGui.QAction(Geomove)
        self.actionChange_scale.setObjectName("actionChange_scale")
        self.actionTuto = QtGui.QAction(Geomove)
        self.actionTuto.setObjectName("actionTuto")
        self.actionImport_GSL = QtGui.QAction(Geomove)
        self.actionImport_GSL.setObjectName("actionImport_GSL")
        self.actionDelete_Selected_Location = QtGui.QAction(Geomove)
        self.actionDelete_Selected_Location.setObjectName("actionDelete_Selected_Location")
        self.action_Export_Map_as_PNG = QtGui.QAction(Geomove)
        self.action_Export_Map_as_PNG.setObjectName("action_Export_Map_as_PNG")
        self.actionExportMapPng = QtGui.QAction(Geomove)
        self.actionExportMapPng.setObjectName("actionExportMapPng")
        self.action_ExportMaptxt = QtGui.QAction(Geomove)
        self.action_ExportMaptxt.setObjectName("action_ExportMaptxt")
        self.actionExportMapExcel = QtGui.QAction(Geomove)
        self.actionExportMapExcel.setObjectName("actionExportMapExcel")
        self.actionMVMScale = QtGui.QAction(Geomove)
        self.actionMVMScale.setObjectName("actionMVMScale")
        self.actionDisplay_scale = QtGui.QAction(Geomove)
        self.actionDisplay_scale.setObjectName("actionDisplay_scale")
        self.actionExport_scale = QtGui.QAction(Geomove)
        self.actionExport_scale.setObjectName("actionExport_scale")
        self.actionAdd_coordinates = QtGui.QAction(Geomove)
        self.actionAdd_coordinates.setObjectName("actionAdd_coordinates")
        self.menu_File.addAction(self.actionNew_Map)
        self.menu_File.addAction(self.actionAdd_coordinates)
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.actionQuit)
        self.menu_Edition.addAction(self.actionImport_locations)
        self.menu_Edition.addAction(self.actionImport_GSL)
        self.menu_Edition.addSeparator()
        self.menu_Edition.addAction(self.actionDelete_Selected_Location)
        self.menu_Edition.addSeparator()
        self.menu_Edition.addAction(self.actionExportMapPng)
        self.menu_Edition.addAction(self.action_ExportMaptxt)
        self.menu_Edition.addAction(self.actionExportMapExcel)
        self.menu_Settings.addAction(self.actionMVMScale)
        self.menu_Settings.addAction(self.actionDisplay_scale)
        self.menu_Settings.addAction(self.actionExport_scale)
        self.menu_Help.addAction(self.actionTuto)
        self.menuBar.addAction(self.menu_File.menuAction())
        self.menuBar.addAction(self.menu_Edition.menuAction())
        self.menuBar.addAction(self.menu_Settings.menuAction())
        self.menuBar.addAction(self.menu_Help.menuAction())

        self.retranslateUi(Geomove)
        QtCore.QMetaObject.connectSlotsByName(Geomove)

    def retranslateUi(self, Geomove):
        Geomove.setWindowTitle(QtGui.QApplication.translate("Geomove", "Geomove", None, QtGui.QApplication.UnicodeUTF8))
        self.addMap.setText(QtGui.QApplication.translate("Geomove", "(+)   Add Map", None, QtGui.QApplication.UnicodeUTF8))
        self.addLocation.setText(QtGui.QApplication.translate("Geomove", "(+)   Add Location", None, QtGui.QApplication.UnicodeUTF8))
        self.agemin.setSuffix(QtGui.QApplication.translate("Geomove", "Ma", None, QtGui.QApplication.UnicodeUTF8))
        self.Tiret.setText(QtGui.QApplication.translate("Geomove", " - ", None, QtGui.QApplication.UnicodeUTF8))
        self.agemax.setSuffix(QtGui.QApplication.translate("Geomove", "Ma", None, QtGui.QApplication.UnicodeUTF8))
        self.ConfirmationFilter.setText(QtGui.QApplication.translate("Geomove", "Confirm Locations Filter", None, QtGui.QApplication.UnicodeUTF8))
        self.Zoomout.setText(QtGui.QApplication.translate("Geomove", "Zoom (-)", None, QtGui.QApplication.UnicodeUTF8))
        self.Zoomin.setText(QtGui.QApplication.translate("Geomove", "Zoom (+)", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_File.setTitle(QtGui.QApplication.translate("Geomove", "&File", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_Edition.setTitle(QtGui.QApplication.translate("Geomove", "&Edition", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_Settings.setTitle(QtGui.QApplication.translate("Geomove", "&Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_Help.setTitle(QtGui.QApplication.translate("Geomove", "&Help ?", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNew_Map.setText(QtGui.QApplication.translate("Geomove", "New Map", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Open_Map.setText(QtGui.QApplication.translate("Geomove", "&Open Map", None, QtGui.QApplication.UnicodeUTF8))
        self.action.setText(QtGui.QApplication.translate("Geomove", "Open recent Map", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave.setText(QtGui.QApplication.translate("Geomove", "Save", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave_as.setText(QtGui.QApplication.translate("Geomove", "Save as ...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionQuit.setText(QtGui.QApplication.translate("Geomove", "Quit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionChange_language.setText(QtGui.QApplication.translate("Geomove", "Change language", None, QtGui.QApplication.UnicodeUTF8))
        self.actionImport_locations.setText(QtGui.QApplication.translate("Geomove", "Import Locations from Excel", None, QtGui.QApplication.UnicodeUTF8))
        self.actionChange_scale.setText(QtGui.QApplication.translate("Geomove", "Change scale", None, QtGui.QApplication.UnicodeUTF8))
        self.actionTuto.setText(QtGui.QApplication.translate("Geomove", "Watch didacticiel", None, QtGui.QApplication.UnicodeUTF8))
        self.actionImport_GSL.setText(QtGui.QApplication.translate("Geomove", "Import Global Sea Level from Excel", None, QtGui.QApplication.UnicodeUTF8))
        self.actionDelete_Selected_Location.setText(QtGui.QApplication.translate("Geomove", "Delete Selected Location", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Export_Map_as_PNG.setText(QtGui.QApplication.translate("Geomove", "&Export Map as PNG", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExportMapPng.setText(QtGui.QApplication.translate("Geomove", "Export Map as png", None, QtGui.QApplication.UnicodeUTF8))
        self.action_ExportMaptxt.setText(QtGui.QApplication.translate("Geomove", "Export Map data as txt", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExportMapExcel.setText(QtGui.QApplication.translate("Geomove", "Export Map data as Excel", None, QtGui.QApplication.UnicodeUTF8))
        self.actionMVMScale.setText(QtGui.QApplication.translate("Geomove", "Set scale", None, QtGui.QApplication.UnicodeUTF8))
        self.actionDisplay_scale.setText(QtGui.QApplication.translate("Geomove", "Display scale", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExport_scale.setText(QtGui.QApplication.translate("Geomove", "Export scale as png", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAdd_coordinates.setText(QtGui.QApplication.translate("Geomove", "Add geo. coordinates to this map", None, QtGui.QApplication.UnicodeUTF8))

