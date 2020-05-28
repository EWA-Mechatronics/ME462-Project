#!/usr/bin/env python3

'''
ME 462 TERM PROJECT - 2020 Spring

Created by Engineers with Attitude:
    
    Ege Uğur Aguş
    İsmail Melih Canbolat
    Koral Özbey 

This is the Mode Selection GUI. Created to provide selection for the Mode.   
'''

import sandbox_gui as sg
import competitive_gui as cg
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QGridLayout, QLabel
from PyQt5.QtWidgets import QStatusBar, QToolBar
from PyQt5.QtWidgets import QPushButton, QGroupBox
from PyQt5.QtCore import pyqtSignal

class SelectionGUI(QMainWindow):
    """
    Main Gui Set-up
    """
    switch_window_to_sand = pyqtSignal() #Define signals to open selected GUI
    switch_window_to_comp = pyqtSignal() 

    def __init__(self):
        super().__init__()

        # Set some main window's properties
        self.setGeometry(700,450,450,150) # 3th parameter width, 4th is height
        self.setWindowTitle(" Robot Areana Mode Selection")
        
        self._createMenu()
        self._createToolBar()
        self._createStatusBar()

        # Set the central widget and general Layout
        self.generalLayout = QGridLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)

        #Create Led Pins, Pot-Bar & Button Pins
        self.generalLayout.addWidget(self._createButton(),0,0)

    def _createButton(self):
        """
        This function creates Mode Selection Buttons.
        """
        groupBox = QGroupBox("Please Select Game Mode")  #Create 'Please Select Game Mode' group box
        buttonLayout = QGridLayout()                     #The instance of a QGridLayout is created

        button1 = QPushButton("Sandbox")        
        button1.clicked.connect(self.change_sand)
        buttonLayout.addWidget(button1,1,1)
        
        button2 = QPushButton("Competetive")
        button2.clicked.connect(self.change_comp)
        buttonLayout.addWidget(button2,0,1)

        groupBox.setLayout(buttonLayout)             #Set the Layout of group box as radiolayout
    
        return groupBox    

    def change_comp(self):
        self.switch_window_to_comp.emit()

    def change_sand(self):
        self.switch_window_to_sand.emit()  

    def _createMenu(self):
        '''
        Create basic menu bar with )an exit option.
        '''
        self.menu = self.menuBar().addMenu("&Menu")
        self.menu.addAction('&Exit', self.close)

    def _createToolBar(self):
        '''
        Create a tool bar with an exit option.
        '''
        tools = QToolBar()
        self.addToolBar(tools)
        tools.addAction('Exit', self.close)

    def _createStatusBar(self):
        '''
        Create a status bar with polite massages to the user.
        '''
        status = QStatusBar()
        status.showMessage("This is the Status Bar.")
        self.setStatusBar(status)      

class Controller:
    """
        This class is to control the switching between GUIs.
    """
    def __init__(self):
        pass

    def show_selection(self):
        self.show_selection = SelectionGUI()
        self.show_selection.switch_window_to_comp.connect(self.show_comp)
        self.show_selection.switch_window_to_sand.connect(self.show_sand)
        self.show_selection.show()

    def show_comp(self):
        self.show_selection.close()
        self.window = cg.MainGui()
        self.window.show()

    def show_sand(self):
        self.show_selection.close()
        self.window = sg.sandController()
        self.window.show_MainGui()

def main():
    app = QApplication(sys.argv)
    controller = Controller()
    controller.show_selection()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
