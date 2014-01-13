"""
-----------------------------------------------------------------------------------------------------------------------------------------------------
Written by jiwon choe
Copyright : jiwon choe
E-mail : jiwonkun@gmail.com
Version : ?
-----------------------------------------------------------------------------------------------------------------------------------------------------
"""

from PyQt4 import QtGui, QtCore
import maya.OpenMayaUI as OpenMayaUI  
import sip
import pymel.core as pm
import glob, subprocess, os

def getPyQtMayaWindow():  
    accessMainWindow = OpenMayaUI.MQtUtil.mainWindow()
    return sip.wrapinstance(long(accessMainWindow), QtCore.QObject)  

class bgCheckTool(QtGui.QWidget):
    def __init__(self, parent=getPyQtMayaWindow()):

        super(bgCheckTool, self).__init__(parent)
        
        # set
        self.iniFile = 'W:/BBM/Assets/Rig/Set/rigging/set/toolini/bgCheckTool.ini'
        
        if os.path.isfile(self.iniFile):
            self.outPath = open(self.iniFile,'r').read()
        else:
            self.outPath = 'X:/BBM/Post/Episode/Ep015/maMel/untitled.mel'
        #
        self.fileList = []
        
        # layout
        mainLayout = QtGui.QVBoxLayout()
        buttonVLayout = QtGui.QVBoxLayout()
        buttonLayout00 = QtGui.QHBoxLayout()
        buttonLayout01 = QtGui.QHBoxLayout()
        buttonLayout02 = QtGui.QHBoxLayout()
        buttonLayout03 = QtGui.QHBoxLayout()
        buttonLayout04 = QtGui.QHBoxLayout()
        Layout04 = QtGui.QHBoxLayout()
        logLayout = QtGui.QVBoxLayout()
        fileLayout = QtGui.QVBoxLayout()
        fileInAddLayout = QtGui.QVBoxLayout()
        fileInLayout = QtGui.QHBoxLayout()
        

        # layout main add
        self.listWg = QtGui.QListWidget()
        
        # layout 0 add
        outPathLabel = QtGui.QLabel('OutPath')
        self.outPathLineEditer = QtGui.QLineEdit(self.outPath)
        sceneSetButton = QtGui.QPushButton('sceneSet')
        sceneSetSaveButton = QtGui.QPushButton('save')

        # layout 1 add
        runButton = QtGui.QPushButton('select Check')

        self.lineEditer = QtGui.QLineEdit('insert Text')
        filterButton = QtGui.QPushButton('filter')

        # layout 2 add
        exportButton = QtGui.QPushButton('export all save')
        selectExportButton = QtGui.QPushButton('export select save')
        animExportButton = QtGui.QPushButton('export anim save')

        # layout 3 add

        self.progress = QtGui.QProgressBar()
        
        # layout 4 add
        
        sortButton = QtGui.QPushButton('Sort')
        connectButton = QtGui.QPushButton('connectAttr >>> setAttr')
        removeButton = QtGui.QPushButton('Remove Item')
        
        # layout 5 add
        
        self.logLabel = QtGui.QTextBrowser()
        self.listFilewg = QtGui.QListWidget()
        
        #
        
        loadButton = QtGui.QPushButton('file load')
        importMelButton = QtGui.QPushButton('import mel')
        importMaButton = QtGui.QPushButton('import ma')
        openFolderButton = QtGui.QPushButton('open folder')
        aboutFolderButton = QtGui.QPushButton('about')
        
        textLabel = QtGui.QLabel('<font color=yellow>6c61737420757064617465</font>')
        

        outPathLabel.setBuddy(self.outPathLineEditer)
        self.logLabel.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred))
        self.listFilewg.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred))

        
        self.progress.setTextVisible(0)

        ###### button connect ######
        runButton.clicked.connect(self.additem)
        filterButton.clicked.connect(self.filterItem)
        exportButton.clicked.connect(self.allOutFile)
        selectExportButton.clicked.connect(self.selectOutFile)
        sortButton.clicked.connect(self.sortRun)
        connectButton.clicked.connect(self.convert)
        removeButton.clicked.connect(self.selectRemoveItem)
        animExportButton.clicked.connect(self.animOut)
        sceneSetButton.clicked.connect(self.fileName)
        
        sceneSetSaveButton.clicked.connect(self.setSaveFile)
        
        loadButton.clicked.connect(self.addFile)
        importMelButton.clicked.connect(self.importMel)
        importMaButton.clicked.connect(self.importMa)
        aboutFolderButton.clicked.connect(self.aboutMessage)
        openFolderButton.clicked.connect(self.openFolder)
        
        # listWg set
        self.listWg.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.listWg.setSortingEnabled(True)
        


        # layout addWidget
        
        buttonLayout00.addWidget(outPathLabel)
        buttonLayout00.addWidget(self.outPathLineEditer)
        buttonLayout00.addWidget(sceneSetButton)
        buttonLayout00.addWidget(sceneSetSaveButton)

        buttonLayout01.addWidget(runButton)
        buttonLayout04.addWidget(self.lineEditer)
        buttonLayout04.addWidget(filterButton)

        buttonLayout02.addWidget(exportButton)
        buttonLayout02.addWidget(selectExportButton)
        buttonLayout02.addWidget(animExportButton)


        buttonLayout03.addWidget(self.progress)

        buttonLayout04.addWidget(sortButton)
        buttonLayout04.addWidget(removeButton)
        buttonLayout04.addWidget(connectButton)
        
        
        logLayout.addWidget(self.logLabel)
        fileLayout.addWidget(self.listFilewg)
        
        fileInAddLayout.addWidget(loadButton)
        fileInAddLayout.addWidget(importMaButton)
        fileInAddLayout.addWidget(importMelButton)
        fileInAddLayout.addWidget(openFolderButton)
        fileInAddLayout.addWidget(aboutFolderButton)
        fileInAddLayout.addWidget(textLabel)
        
        mainLayout.addWidget(self.listWg)
        

        buttonVLayout.addLayout(buttonLayout01)
        buttonVLayout.addLayout(buttonLayout04)
        
        
        buttonVLayout.addLayout(buttonLayout02)
        
        buttonVLayout.addLayout(buttonLayout00)
        
        fileInLayout.addLayout(fileLayout)
        fileInLayout.addLayout(fileInAddLayout)
        
        
        Layout04.addLayout(logLayout)
        Layout04.addLayout(fileInLayout)

        mainLayout.addLayout(buttonVLayout)
        mainLayout.addLayout(Layout04)
        mainLayout.addLayout(buttonLayout03)
        
        # style
        #styleFile = open('w:/BBM/Assets/Rig/Set/Rigging/set/darkorange.stylesheet', 'r')
        #self.setStyleData = styleFile.read()
        #styleFile.close()
        #self.setStyleSheet(self.setStyleData)        
        
        self.setLayout(mainLayout)
        self.setWindowTitle('getReferenceEdits Tool')

        self.setGeometry(300, 300, 200, 500)
        self.resize(400, 1000)
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
        self.logLabel.setText('---selected=mel.file---')

    def allOutFile(self):
        outList = self.allOut()
        outPath = str(self.outPathLineEditer.text())
        with open(outPath,'w') as outFile:
            for x in outList:
                outFile.write(x + ';\n')
            outFile.close()
        self.logLabel.setText('---all=mel.file---')
    
    def additem(self):
        
        selectNode = self.nodeFilter(pm.selected())
        
        referenceAttrList = []
        
        for k in selectNode:
            if type(k) == str:
                print k
                break
            else:
                referenceAttrList = referenceAttrList + k.referenceFile().getReferenceEdits()

        referenceAttrListFilter = []
        self.progress.setRange(1, len(referenceAttrList))
        
        self.i = 1
        
        for x in referenceAttrList:
            self.i += 1
            self.progress.setValue(self.i)
            if x[0:7] == 'setAttr':
                if pm.objectType(x.split(' ')[1].split('.')[0]) == 'transform':
                    referenceAttrListFilter.append(x)
            elif x[0:7] == 'connect':
                if pm.objectType(x.split('"')[3].split('.')[0]) == 'transform':
                    referenceAttrListFilter.append(x)
 
        referenceAttrListFilter = self.filterOutStringlist(referenceAttrListFilter, '-k 0 ')
    
        if self.listWg.count() >= 0:
            self.listWg.clear()
            self.listWg.addItems(referenceAttrListFilter)   
    
    def nodeFilter(self, getList):
        
        returnList = []
        
        if len(getList) > 1 :

            nodeList = []
            for x in getList:
                nodeList.append(x.referenceFile().refNode.name())
            newList = list(set(nodeList))
            
            for i in newList:
                returnList.append(pm.PyNode(i))
            return returnList
        else:
            if not len(getList) == 0:
                return getList
            else:
                return ['Not Select']


    def addFile(self):

        path = os.path.dirname(str(self.outPathLineEditer.text()))
        self.fileList = glob.glob(path + '/*.mel')
        
        baseName = []
        
        for x in self.fileList:
            baseName.append(os.path.basename(x).split('.')[0])
        
        if self.listFilewg.count() >= 0:
            self.listFilewg.clear()
            self.listFilewg.addItems(baseName)

    def filterOutStringlist(self, inputList, filterString):

        returnList =[]
        
        for x in inputList:
            if x.find(filterString) == -1:
                returnList.append(x)
        
        return returnList        


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

    def sortRun(self):
        self.listWg.sortItems(QtCore.Qt.DescendingOrder)

    def convert(self):
        font = QtGui.QFont()
        font.setBold(1)
        font.setPixelSize(12)
        
        connectItem = []
        getList = []
        inputText = '--- convert log ---\n'
        
        for x in xrange(self.listWg.count()):
            getList.append(self.listWg.item(x))
        for y in getList:
            if not str(y.text()).find('connectAttr') == -1:
                connectItem.append(y)
        for z in connectItem:
            z.setFont(font)
            nodeName = str(z.text()).split('"')[1].split('.')[0]
            inNodeName = str(z.text()).split('"')[3]
            node = pm.PyNode(nodeName)
            if not str(node.nodeType()).find('animCurve') == -1:
                attr = str(node.output.get())
                inText = 'setAttr ' + inNodeName + ' ' + attr + ';'
                z.setText(inText)
                inputText += 'covert --- ' + inNodeName + '\n'
            elif not str(node.nodeType()).find('animBlendNode') == -1:
                z.setText('//' + z.text())
                inputText += ('animLayer --- ' + inNodeName + '\n')
            else:
                z.setText('//' + z.text())
                inputText += (inNodeName + '\n')

        self.logLabel.setText(inputText)
        
    def selectRemoveItem(self):
        
        getList = self.listWg.selectedItems()
        
        getNumber = None
        rmItem = None
        
        for x in getList:
            getNumber = self.listWg.indexFromItem(x).row()
            rmItem = self.listWg.takeItem(getNumber)
            self.listWg.removeItemWidget(rmItem)
 
    def animOut(self):
        font = QtGui.QFont()
        font.setBold(1)
        font.setPixelSize(12)
        connectItem = []
        getList = []
        inputText = '--- anim OutputFile log ---\n'
        getAnimNode = []
        
        for x in xrange(self.listWg.count()):
            getList.append(self.listWg.item(x))
        for y in getList:
            if not str(y.text()).find('connectAttr') == -1:
                connectItem.append(y)
        for z in connectItem:
            z.setFont(font)
            nodeName = str(z.text()).split('"')[1].split('.')[0]
            inNodeName = str(z.text()).split('"')[3]
            node = pm.PyNode(nodeName)
            if not str(node.nodeType()).find('animCurve') == -1:
                inText ='connectAttr "' + 'copy_' + z.text().split('"')[1].split(':')[-1] + '" "' + str(z.text()).split('"')[3] + '"'
                z.setText(inText)
                getAnimNode.append(node)
                inputText += 'animCurve --- ' + node.name() + '\n'
            elif not str(node.nodeType()).find('animBlendNode') == -1:
                z.setText('//' + z.text())
                inputText += (inNodeName + '\n')
            else:
                z.setText('//' + z.text())
                inputText += (inNodeName + '\n')
        
        outNodeList = self.copyAnimCurve(getAnimNode)
        self.allOutFile()
        
        ###
        
        pm.select(cl=1)
        pm.select(outNodeList, r=1)
        outPath = str(self.outPathLineEditer.text()).replace('.mel','.ma')
        out = pm.exportSelected(outPath, typ='mayaAscii')
        pm.select(cl=1)
        inputText += out + '\n'
        
        ###
        
        self.logLabel.setText(inputText)
        #print inputText        

    def copyAnimCurve(self, getList):
        outList = []
        for x in getList:
            outList.append(pm.duplicate(x,n='copy_'+x.name().split(':')[-1])[0])
        return outList

    def fileName(self):
        fileName = pm.sceneName().basename().split('.')[0]
        rePath = str(self.outPathLineEditer.text()).replace('\\','/')
        self.outPathLineEditer.setText(rePath)

        if fileName == u'':
            newName = os.path.dirname(rePath) + '/untitled.mel'
        else:
            newName = os.path.dirname(rePath) + '/' + fileName + '.mel'
            if str(self.outPathLineEditer.text()).find('.') == -1:
                newName = str(self.outPathLineEditer.text()) + '/' + fileName + '.mel'

        self.outPathLineEditer.setText(newName)


    
    def importMel(self):

        selectItem = self.listFilewg.selectedItems()[0]
        path = os.path.dirname(str(self.outPathLineEditer.text()))
        melfile = path + '/' + selectItem.text() + '.mel'
        if os.path.isfile(melfile):
            out = pm.mel.source(melfile)
            inputText = 'import mel file\n' + out
            self.logLabel.setText(inputText)
        else:
            inputText = 'import mel file\nmel file ??????'
            self.logLabel.setText(inputText)

    def importMa(self):

        selectItem = self.listFilewg.selectedItems()[0]
        path = os.path.dirname(str(self.outPathLineEditer.text()))
        mafile = path + '/' + selectItem.text() + '.ma'
        if os.path.isfile(mafile):
            pm.importFile(str(mafile))
            inputText = 'import ma file\n' + mafile
            self.logLabel.setText(inputText)
        else:
            inputText = 'import ma file\nma file ??????'
            self.logLabel.setText(inputText)
    
    def aboutMessage(self):
        
        message = QtGui.QMessageBox()
        message.setWindowTitle('About')
        message.setInformativeText('PyQt4 version(4.8.3)\nWritten by jiwon choe')
        message.exec_()

    def openFolder(self):
        
        path = os.path.dirname(str(self.outPathLineEditer.text()))
        subprocess.Popen(r'explorer.exe %s' % path.replace('/','\\'))


    def setSaveFile(self):
        outPath = str(self.outPathLineEditer.text())
        with open(self.iniFile,'w') as outFile:
                outFile.write(outPath)
        outFile.close()

### test run ###
#testz = bgCheckTool()
#testz.show()

        
