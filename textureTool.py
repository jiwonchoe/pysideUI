"""
-----------------------------------------------------------------------------------------------------------------------------------------------------
Written by jiwon choe
Copyright : jiwon choe
E-mail : jiwonkun@gmail.com
Version : beta
-----------------------------------------------------------------------------------------------------------------------------------------------------
"""


import pymel.api as pa
import pymel.core as pm
from PyQt4 import QtGui, QtCore
import sip, os, shutil, subprocess

def getPyQtMayaWindow():  

    accessMainWindow = pa.MQtUtil.mainWindow()

    return sip.wrapinstance(long(accessMainWindow), QtCore.QObject)


class texModel(QtCore.QAbstractTableModel):

    def __init__(self, files = [[]], headers = [], nodeName = [], parent=None):

        super(texModel, self).__init__(parent)

        self.files = files
        self.headers = headers
        self.nodeName = nodeName

    def headerData(self, section, orientation, role):

        if role == QtCore.Qt.DisplayRole:

            if orientation == QtCore.Qt.Horizontal:
                if section < len(self.headers):
                    return self.headers[section]
                else:
                    return QtCore.QString('name')
            else:
                if section < len(self.nodeName):
                    return self.nodeName[section]
                else:
                    return QtCore.QString('list %1').arg(section) #'mayaFile %02d' % (section+1)

    def rowCount(self, parent):

        return len(self.files[0])

    def columnCount(self,files):

        return len(self.files)

    def data(self, index, role):

        if role == QtCore.Qt.EditRole:
            return self.files[index.column()][index.row()]

        if role == QtCore.Qt.DisplayRole:

            row = index.row()
            col = index.column()
            value = self.files[col][row]

            return value

    def flags(self, index):

        return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def setData(self, index, value, role = QtCore.Qt.EditRole):

        if role == QtCore.Qt.EditRole:
            row = index.row()
            col =  index.column()
            text = value

            if type(text) == QtCore.QVariant:
                self.files[col][row] = text
                #print self.files[col][row].toString()
                #print self.nodeName[row]
                self.dataChanged.emit(index, index)
                self.run(self.nodeName[row], self.files[col][row].toString())
                return True

        return False

    def run(self, nodeName, rePath):
        pm.setAttr(nodeName + '.ftn', str(rePath))

class texTableView(QtGui.QTableView):
    
    def __init__(self, parent=None):
        
        super(texTableView, self).__init__(parent)
        self.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)

    def contextMenuEvent(self, event):

        menu = QtGui.QMenu(self)
        menu.addAction('Select Node', self.selectNode)
        menu.addAction('View Image', self.texView)
        menu.addAction('Open Folder', self.openFolder)
        menu.exec_(event.globalPos())
    
    def texView(self):
        
        selectList = self.selectedIndexes()
        
        intList = [x.row() for x in selectList]
  
        for x in intList:
            subprocess.Popen(r'fcheck.exe ' + self.data.getListPath[x])

    def selectNode(self):

        selectList = self.selectedIndexes()
        
        intList = [x.row() for x in selectList]
        
        pm.select(cl=1)

        for x in intList:
            pm.select(self.data.getListName[x],add=1)

    def openFolder(self):

        selectList = self.selectedIndexes()
        
        intList = [x.row() for x in selectList]
        
        pathList = list(set(self.data.getListPath[x] for x in intList))
        
        for x in pathList:
            subprocess.Popen(r'explorer.exe ' + os.path.dirname(x).replace('/','\\'))


class textureTool(QtGui.QWidget):

    def __init__(self, parent=getPyQtMayaWindow()):

        super(textureTool, self).__init__(parent)

        mainLayout = QtGui.QVBoxLayout()
        downLayout = QtGui.QHBoxLayout()

        self.view = texTableView()

        self.refreshButton = QtGui.QPushButton('refresh')
        self.refreshButton.clicked.connect(self.refreshList)
        
        self.searchLabel = QtGui.QLabel('search : ')
        self.orgLine = QtGui.QLineEdit()
        
        self.replaceLabel = QtGui.QLabel('replace : ')
        self.replaceLine = QtGui.QLineEdit()
        self.runButton = QtGui.QPushButton('rePath')
        self.runButton.clicked.connect(self.selectReplace)
        self.baseLabel = QtGui.QLabel('folder replace : ')
        self.baseLine = QtGui.QLineEdit()
        self.baseButton = QtGui.QPushButton('rePath')
        self.baseButton.clicked.connect(self.selectBaseReplace)
        self.baseCopyButton = QtGui.QPushButton('copy')
        self.baseCopyButton.clicked.connect(self.makeIn)
        
        downLayout.addWidget(self.refreshButton)
        downLayout.addWidget(self.searchLabel)
        downLayout.addWidget(self.orgLine)
        downLayout.addWidget(self.replaceLabel)
        downLayout.addWidget(self.replaceLine)
        downLayout.addWidget(self.runButton)
        downLayout.addWidget(self.baseLabel)
        downLayout.addWidget(self.baseLine)
        downLayout.addWidget(self.baseButton)
        downLayout.addWidget(self.baseCopyButton)

        mainLayout.addWidget(self.view)

        mainLayout.addLayout(downLayout)

        self.setLayout(mainLayout)
        self.setWindowTitle('textureTool')
        self.setWindowFlags(QtCore.Qt.Window)
        self.resize(640,480)

        self.show()

        self.addList()
        
        self.orgList = []
        self.replaceList = []
        
        

    def addList(self):
        
        addObj = addList()
        self.objList = texModel(addObj.addList, addObj.headers, addObj.getListName)
        self.view.setModel(self.objList)
        
        self.view.data = addObj
        
    def selectReplace(self):

        orgStr = str(self.orgLine.text())
        reStr = str(self.replaceLine.text()).replace('\\', '/')
        
        selectList = self.view.selectedIndexes()
        
        intList = [x.row() for x in selectList] 
        
        model = self.view.model()
       
        for x, y in zip(intList, selectList):
            getPath = pm.getAttr(str(model.nodeName[x]) + '.ftn')
            getPath = getPath.replace(orgStr, reStr)
            pm.setAttr(model.nodeName[x] + '.ftn', getPath)
            model.files[y.column()][y.row()] = getPath
            model.dataChanged.emit(y, y)

    def selectBaseReplace(self):

        reStr = str(self.baseLine.text()).replace('\\', '/')
        if reStr[-1] != '/':
            reStr = reStr + '/' 
        
        selectList = self.view.selectedIndexes()
        
        intList = [x.row() for x in selectList] 
        
        model = self.view.model()
       
        for x, y in zip(intList, selectList):
            self.orgList.append(pm.getAttr(str(model.nodeName[x]) + '.ftn'))
            getPath = reStr + os.path.basename(pm.getAttr(str(model.nodeName[x]) + '.ftn'))
            self.replaceList.append(getPath)
            pm.setAttr(model.nodeName[x] + '.ftn', getPath)
            model.files[y.column()][y.row()] = getPath
            model.dataChanged.emit(y, y)

    def refreshList(self):
        
        self.addList()
        self.view.setModel(self.objList)

    def run(self, nodeName, rePath):

        pm.setAttr(nodeName + '.ftn', str(rePath))

    def makeIn(self):

        if os.path.isdir(os.path.dirname(self.replaceList[0])):
            for x in range(len(self.orgList)):
                shutil.copy(self.orgList[x], self.replaceList[x])
        else:
            os.makedirs(os.path.dirname(self.replaceList[0]))
            for x in range(len(self.orgList)):
                if not os.path.isfile(self.replaceList[x]):
                    shutil.copy(self.orgList[x], self.replaceList[x])

class addList():

    def __init__(self):
        
        self.getList = pm.ls(type='file')
        
        self.getListName = [x.name() for x in self.getList]
        self.getListPath = [x.ftn.get() for x in self.getList]
        self.getListIsFile = [os.path.isfile(x) for x in self.getListPath]
        self.getListSize = [str(x.os.get()) for x in self.getList]
        
        self.addList = [self.getListPath] + [self.getListIsFile] + [self.getListSize]
        self.headers = ['file path', 'isFile', 'size']



###

atest = textureTool()
atest.view.resizeRowsToContents()
atest.view.resizeColumnsToContents()

