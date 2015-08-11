import pymel.api as api
import pymel.core as pm
from PySide import QtGui, QtCore
import shiboken, os

# core


commonPath = 'F:/prj.palrilla/assets/'


assetType = ['ch/', 'pr/', 'bg/']

def isDir(inPath, asset):
    
    path = inPath + asset

    dirList = os.listdir(path)
    
    itemList = []

    for x in dirList:
        if os.path.isdir(path + x + '/rig' ):
            itemList.append(x)

    return itemList

class makeRef():
    
    def __init__(self):
        
        self.assetType = ''

    def makeRN(self, name):
        
        print '?'
        
        objName = name
        assetType = self.assetType
    
        mbPath = commonPath + assetType
    
        mbFile = mbPath + objName + '/rig/' + assetType[:2] + '_' + objName + '_rig_v000.ma'
        
        if os.path.isfile(mbFile):
            pm.createReference(mbFile, groupLocator=1, loadReferenceDepth='all' ,namespace=objName + '0' ,rfn=assetType.replace('/', '_') + objName + '_RN0')
    

def errorFileMessage(fileName):
    
    message = QtGui.QMessageBox()
    message.setWindowTitle('ERROR')
    message.setInformativeText('Missing File\n %s' % fileName)
    message.exec_()

# UI

def getMayaWindow():  
    accessMainWindow = api.MQtUtil.mainWindow()  
    return shiboken.wrapInstance(long(accessMainWindow), QtGui.QWidget)

class chTab(QtGui.QWidget):

    def __init__(self, parent=None):

        super(chTab, self).__init__(parent)

        self.mainLayout = QtGui.QVBoxLayout()
        self.mainLayout.setSpacing(0)
        
        self.addButton()
        
        self.setLayout(self.mainLayout)
        
    def addButton(self):
        
        itemList = (isDir(commonPath, assetType[0]))
        buttonList = {}
        ref = makeRef()
        ref.assetType = assetType[0]   

        for x in itemList:
            
            buttonList[x] = QtGui.QPushButton(x)
            buttonList[x].clicked.connect(lambda xa = x: ref.makeRN(xa))
            self.mainLayout.addWidget(buttonList[x])

class bgTab(QtGui.QWidget):

    def __init__(self, parent=None):

        super(bgTab, self).__init__(parent)
        self.mainLayout = QtGui.QVBoxLayout()
        self.mainLayout.setSpacing(0)
        
        self.addButton()
        
        self.setLayout(self.mainLayout)
        
    def addButton(self):
        
        itemList = (isDir(commonPath, assetType[2]))
        buttonList = {}
        ref = makeRef()
        ref.assetType = assetType[2]   

        for x in itemList:
            
            buttonList[x] = QtGui.QPushButton(x)
            buttonList[x].clicked.connect(lambda xa = x: ref.makeRN(xa))
            self.mainLayout.addWidget(buttonList[x])

class propTab(QtGui.QWidget):

    def __init__(self, parent=None):

        super(propTab, self).__init__(parent)
        
        self.mainLayout = QtGui.QVBoxLayout()
        self.mainLayout.setSpacing(0)
        
        self.addButton()
        
        self.setLayout(self.mainLayout)
        
    def addButton(self):
        
        itemList = (isDir(commonPath, assetType[1]))
        buttonList = {}
        ref = makeRef()
        ref.assetType = assetType[1]   

        for x in itemList:
            
            buttonList[x] = QtGui.QPushButton(x)
            buttonList[x].clicked.connect(lambda xa = x: ref.makeRN(xa))
            self.mainLayout.addWidget(buttonList[x])


class toolTab(QtGui.QWidget):

    def __init__(self, parent=None):

        super(toolTab, self).__init__(parent)
        
        mainLayout = QtGui.QVBoxLayout()
        mainLayout.setSpacing(0)
        
        iconSizePolicy = QtGui.QSizePolicy()
        iconSizePolicy.setHorizontalPolicy(QtGui.QSizePolicy.Preferred)
        iconSizePolicy.setVerticalPolicy(QtGui.QSizePolicy.Preferred)        
        
        #unitButton = QtGui.QPushButton('Unit "cm"')
        #gridButton = QtGui.QPushButton('Grid 12 * 5')
        bakeButton = QtGui.QPushButton('Bake')
        
        #unitButton.clicked.connect(self.unitCovert)
        #gridButton.clicked.connect(self.gridSet)
        bakeButton.clicked.connect(self.bake)
        
        #unitButton.setSizePolicy(iconSizePolicy)
        #gridButton.setSizePolicy(iconSizePolicy)
        bakeButton.setSizePolicy(iconSizePolicy)
        
        #mainLayout.addWidget(unitButton)
        #mainLayout.addWidget(gridButton)
        mainLayout.addWidget(bakeButton)

        self.setLayout(mainLayout)

    def unitCovert(self):

        pm.currentUnit(l='cm')
    
    def gridSet(self):

        pm.grid(r=1)
        pm.grid(s=12,d=5)
        pm.grid(r=1)

    def bake(self):

        minFrame = int(pm.playbackOptions(q=1,min=1))
        maxFrame = int(pm.playbackOptions(q=1,max=1))
        selectSet = pm.ls('*:bake_set*',typ='objectSet')
        if selectSet == []:
            pm.headsUpMessage( '???' )
        else:
            bakeList = []
            for x in selectSet:
                for y in x.flattened():
                    bakeList.append(y)
            pm.bakeResults(bakeList, sm=1, t=(minFrame, maxFrame), sb=1, pok=1, sac=0, bol=0, at=['tx','ty','tz','rx','ry','rz','sx','sy','sz'])

class aboutTab(QtGui.QWidget):

    def __init__(self, parent=None):

        super(aboutTab, self).__init__(parent)

        mainLayout = QtGui.QVBoxLayout()
        inLayout = QtGui.QVBoxLayout()
              
        #aboutIcon = QtGui.QPixmap('W:/Kyowon/Doyose/Assets/Rig/icon/about.png')
        #aboutLabel = QtGui.QLabel()
        #aboutLabel.setPixmap(aboutIcon)
        
        textLabel = QtGui.QLabel('project 8\n\nWritten by jiwon choe\n\njiwonkun@gmail.com')
        textLabel.setAlignment(QtCore.Qt.AlignHCenter)
        
        #inLayout.addWidget(aboutLabel)
        inLayout.addWidget(textLabel)
        
        mainLayout.addLayout(inLayout)
        
        mainLayout.setAlignment(QtCore.Qt.AlignHCenter)

        self.setLayout(mainLayout)
  

class palrillaLayoutTool(QtGui.QWidget):

    def __init__(self, parent=getMayaWindow()):

        super(palrillaLayoutTool, self).__init__(parent)
        
        self.closeCheck()

        mainLayout = QtGui.QVBoxLayout()

        tab = QtGui.QTabWidget()
        tab.addTab(chTab(), 'ch')
        tab.addTab(propTab(), 'pr')
        tab.addTab(bgTab(), 'bg')
        tab.addTab(toolTab(), 'tool')
        tab.addTab(aboutTab(), 'about')

        mainLayout.addWidget(tab)

        self.setWindowTitle('simple layout tool')
        self.setLayout(mainLayout)
        
        '''
        styleFile = open('W:/Kyowon/Doyose/Assets/Rig/script/darkorange.stylesheet', 'r')
        self.setStyleData = styleFile.read()
        styleFile.close()
        self.setStyleSheet(self.setStyleData)
        '''
        
        self.setWindowFlags(QtCore.Qt.Window)
        self.setObjectName('palrillaLT')
        
        self.show()
        

    def errorMessage(self, unit):
        
        message = QtGui.QMessageBox()
        message.setWindowTitle('ERROR')
        message.setInformativeText('Unit "%s"' % unit)
        message.exec_()

    def closeCheck(self):

        for x in QtGui.QApplication.topLevelWidgets():
            try:
                if x.objectName() == 'palrillaLT':
                    x.deleteLater()
            except:
                pass

#

testUI = palrillaLayoutTool()

print '*' * 400
print '*' * 400
print '*' * 400

#
