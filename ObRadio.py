#!/bin/python 

import sys, subprocess, os, requests
import xml.etree.ElementTree as ET
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *

class AnotherWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Add Url')
        self.setGeometry(10, 10, 300, 220)

        layout = QVBoxLayout()
        self.frm1 = QFrame()
        self.label = QLabel("Name")
        self.label2 = QLabel("Url")
        self.streamName = QLineEdit()
        self.streamUrl = QLineEdit()
        self.addBtn = QPushButton("Add")
        self.addBtn.clicked.connect(self.addtoXML)
        self.cancelBtn = QPushButton("Cancel")
        self.cancelBtn.clicked.connect(self.close)
        layout.addWidget(self.label)
        layout.addWidget(self.streamName)
        layout.addWidget(self.label2)
        layout.addWidget(self.streamUrl)
        layout.addWidget(self.addBtn)
        layout.addWidget(self.cancelBtn)
        self.setLayout(layout)
        directory_path = os.getcwd()

    def addtoXML(self):
        directory_path = os.getcwd()
        mytree = ET.parse(directory_path + '/stations.xml')
        myroot = mytree.getroot()
        subroot = ET.SubElement(myroot, 'Station')
        child1 = ET.SubElement(subroot, 'Name')
        child1.text = self.streamName.text()
        child2 = ET.SubElement(subroot, 'Url')
        child2.text = self.streamUrl.text()
        mytree.write(directory_path + '/stations.xml')
        MainWindow.parseXML(self, directory_path + '/stations.xml')

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('OB Radio Player')
        self.setGeometry(0, 0, 350, 250)
        self.move(60, 45)
        self.selfUI()
        
    def selfUI(self):
        self.hbox = QHBoxLayout()
        self.frm1 = QFrame()
        global listWidget 
        listWidget = QListWidget(self.frm1)
        listWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        listWidget.setGeometry(0, 0, 320, 180)
        self.btn1 = QPushButton(self.frm1)
        self.btn1.setText('Play')
        self.btn1.setGeometry(0, 200, 50, 24)
        self.btn1.clicked.connect(self.playStream)
        self.btn2 = QPushButton(self.frm1)
        self.btn2.setText('Stop')
        self.btn2.setGeometry(60, 200, 50, 24)
        self.btn2.clicked.connect(self.stopStream)
        self.btn3 = QPushButton(self.frm1)
        self.btn3.setText('Add')
        self.btn3.setGeometry(120, 200, 50, 24)
        self.btn3.clicked.connect(self.add2List)
        self.btn4 = QPushButton(self.frm1)
        self.btn4.setText('Edit')
        self.btn4.setGeometry(180, 200, 50, 24)
        self.btn4.clicked.connect(self.editEntry)
        self.btn5 = QPushButton(self.frm1)
        self.btn5.setText('Quit')
        self.btn5.setGeometry(240, 200, 50, 24)
        self.btn5.clicked.connect(self.closeApp)
        listWidget.clicked.connect(self.playStream)
        self.hbox.addWidget(self.frm1)
        self.setLayout(self.hbox)
        directory_path = os.getcwd()
        self.parseXML(directory_path + '/stations.xml')

        # SysTray
        self.tray = QSystemTrayIcon()
        icon = QIcon("icon.png")
        self.tray.setIcon(icon)
        self.tray.setToolTip('OB Radio Player - Dev')
        self.menu = QMenu()
        showAction = QAction("Show",self) 
        showAction.triggered.connect(self.show)
        self.menu.addAction(showAction)
        playAction = QAction("Play",self) 
        playAction.triggered.connect(self.playStream)
        self.menu.addAction(playAction)
        stopAction = QAction("Stop",self) 
        stopAction.triggered.connect(self.stopStream)
        self.menu.addAction(stopAction)
        quitAction = QAction("Quit",self) 
        quitAction.triggered.connect(self.closeApp)
        self.menu.addAction(quitAction)
        self.tray.setContextMenu(self.menu)
        self.tray.show()
        self.show()
        

    def playStream(self):
        self.player = QMediaPlayer()
        selectedUrl = self.nameToUrl(listWidget.currentItem().text())
        self.player.setMedia(QMediaContent(QUrl(selectedUrl)))
        self.player.play()
    
    def stopStream(self):
        self.player = QMediaPlayer()
        self.player.stop()

    def editEntry(self):
        selectedUrl = self.nameToUrl(listWidget.currentItem().text())
        directory_path = os.getcwd()
        tree = ET.ElementTree(file=directory_path + '/stations.xml')
        root = tree.getroot()
        urls = root.findall('.//Url') 



    def nameToUrl(self, selectedName):
        directory_path = os.getcwd()
        mytree = ET.parse(directory_path + '/stations.xml').getroot()
        for child in mytree:
            if child.find('Name').text == selectedName:
                urlToPass =  child.find('Url').text
        return urlToPass


    def add2List(self):
        self.w = AnotherWindow()
        self.w.show()

    def createRadioList(self):
        directory_path = os.getcwd()
        root = ET.Element("Stations")
        children1 = ET.Element("Station")
        root.append(children1)
        userId1 = ET.SubElement(children1, "Name")
        userId1.text = "BBC Radio 1"
        userName1 = ET.SubElement(children1, "Url")
        userName1.text = "http://stream.live.vc.bbcmedia.co.uk/bbc_radio_one"
        tree = ET.ElementTree(root)
        with open(directory_path + '/stations.xml', "wb") as fh:
            tree.write(fh)
    
    def parseXML(self,file_name):
        # Parse XML with ElementTree
        listWidget.clear()
        tree = ET.ElementTree(file=file_name)
        root = tree.getroot()
        for country in root.findall('Station'):
            name = country.find('Name').text
            streamUrl = country.find('Url').text
            listWidget.addItem(name)

    def closeApp(self):
        quit()
    
    def closeEvent(self, event):
        event.ignore()
        self.hide()



# Initialize App
app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.setWindowIcon(QIcon('icon.png'))
app.exec_()
