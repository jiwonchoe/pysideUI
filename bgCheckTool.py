"""
-----------------------------------------------------------------------------------------------------------------------------------------------------
Written by jiwon choe
Copyright : jiwon choe
E-mail : jiwonkun@gmail.com
Version : 1
-----------------------------------------------------------------------------------------------------------------------------------------------------
"""

from PyQt4 import QtGui, QtCore
import maya.OpenMayaUI as OpenMayaUI  
import sip
import pymel.core as pm

def getPyQtMayaWindow():  
    accessMainWindow = OpenMayaUI.MQtUtil.mainWindow()
    return sip.wrapinstance(long(accessMainWindow), QtCore.QObject)  

class bgCheckTool(QtGui.QWidget):
    def __init__(self, parent=getPyQtMayaWindow()):

        super(bgCheckTool, self).__init__(parent)
        
        mainLayout = QtGui.QVBoxLayout()
        buttonVLayout = QtGui.QVBoxLayout()
        buttonLayout01 = QtGui.QHBoxLayout()
        buttonLayout02 = QtGui.QHBoxLayout()
        buttonLayout03 = QtGui.QHBoxLayout()

        # layout main add
        self.listWg = QtGui.QListWidget()
        self.outPathLineEditer = QtGui.QLineEdit('d:/attrTest.mel')

        # layout 1 add
        runButton = QtGui.QPushButton('select Check')
        self.lineEditer = QtGui.QLineEdit()
        filterButton = QtGui.QPushButton('filter')

        # layout 2 add
        exportButton = QtGui.QPushButton('all OutputFile')
        selectExportButton = QtGui.QPushButton('select OutputFile')

        # layout 3 add
        self.radioButton01 = QtGui.QRadioButton('translate', self)
        self.radioButton02 = QtGui.QRadioButton('rotate', self)
        self.radioButton03 = QtGui.QRadioButton('scale', self)
        self.radioButton04 = QtGui.QRadioButton('visibility', self)

        # radioButton set
        self.radioButton01.setAutoExclusive(0)
        self.radioButton02.setAutoExclusive(0)
        self.radioButton03.setAutoExclusive(0)
        self.radioButton04.setAutoExclusive(0)
        self.radioButton01.setChecked(1)
        self.radioButton02.setChecked(1)
        self.radioButton03.setChecked(1)
        self.radioButton04.setChecked(1)

        ###### button connect ######
        runButton.clicked.connect(self.additem)
        filterButton.clicked.connect(self.filterItem)
        exportButton.clicked.connect(self.allOutFile)
        selectExportButton.clicked.connect(self.selectOutFile)

        # listWg set
        self.listWg.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)

        buttonLayout01.addWidget(runButton)
        buttonLayout01.addWidget(self.lineEditer)
        buttonLayout01.addWidget(filterButton)

        buttonLayout02.addWidget(exportButton)
        buttonLayout02.addWidget(selectExportButton)

        buttonLayout03.addWidget(self.radioButton01)
        buttonLayout03.addWidget(self.radioButton02)
        buttonLayout03.addWidget(self.radioButton03)
        buttonLayout03.addWidget(self.radioButton04)

        mainLayout.addWidget(self.listWg)
        mainLayout.addWidget(self.outPathLineEditer)

        buttonVLayout.addLayout(buttonLayout01)
        buttonVLayout.addLayout(buttonLayout02)
        buttonVLayout.addLayout(buttonLayout03)

        mainLayout.addLayout(buttonVLayout)

        self.setLayout(mainLayout)
        self.setWindowTitle('BG CheckTool')

        self.setGeometry(300, 300, 200, 500)

        styleFile = open('w:/BBM/Assets/Rig/Set/Rigging/set/darkorange.stylesheet', 'r')
        self.setStyleData = styleFile.read()
        styleFile.close()
        self.setStyleSheet(self.setStyleData)
        
        self.setWindowFlags(QtCore.Qt.Window)

    def selectOut(self):
        getList = self.listWg.selectedItems()
        getListText = []
        for x in getList:
            getListText.append(str(x.text()))
        return getListText

    def allOut(self):
        getList = []
        getListText = [] 
        for x in xrange(self.listWg.count()):
            getList.append(self.listWg.item(x))
        for y in getList:
            getListText.append(str(y.text()))
        return getListText

    def selectOutFile(self):
        outList = self.selectOut()
        outPath = str(self.outPathLineEditer.text())
        with open(outPath,'w') as outFile:
            for x in outList:
                outFile.write(x + ';\n')
            outFile.close()

    def allOutFile(self):
        outList = self.allOut()
        outPath = str(self.outPathLineEditer.text())
        with open(outPath,'w') as outFile:
            for x in outList:
                outFile.write(x + ';\n')
            outFile.close()

    def additem(self):
        selectNode = pm.ls(sl=1)[0]
        referenceAttrList = selectNode.referenceFile().getReferenceEdits()
        referenceAttrListFilter =[]
        
        if self.radioButton01.isChecked():
            referenceAttrListFilter = self.filterStringList(referenceAttrList,'.translate')
        if self.radioButton02.isChecked():
            referenceAttrListFilter = referenceAttrListFilter + self.filterStringList(referenceAttrList,'.rotate')
        if self.radioButton03.isChecked():
            referenceAttrListFilter = referenceAttrListFilter + self.filterStringList(referenceAttrList,'.scale')
        if self.radioButton04.isChecked():
            referenceAttrListFilter = referenceAttrListFilter + self.filterStringList(referenceAttrList,'.visibility')
        
        if self.listWg.count() >= 0:
            self.listWg.clear()
            self.listWg.addItems(referenceAttrListFilter)


    def filterItem(self):
        findString = str(self.lineEditer.text())
        getListText = self.allOut()
        newList = self.filterStringList(getListText, findString)
        self.listWg.clear()
        self.listWg.addItems(newList)

    def filterStringList(self,inputList,filterString):
        returnList =[]
        
        for x in inputList:
            if x.find(filterString) != -1:
                returnList.append(x)
        
        return returnList
    
    def replaceNameList(self,inputList,oldName,newName):
        returnList = []
    
        for x in inputList:
            returnList.append(x.replace(oldName,newName))
    
        return returnList
    
    def filterNameList(self,inputList,name,value):
        returnListP = []
        returnListA = []
    
        for x in inputList:
            if x.find(name) != -1:
                returnListP.append(x)
            else:
                returnListA.append(x)
        if value:
            return returnListP
        else:
            return returnListA
