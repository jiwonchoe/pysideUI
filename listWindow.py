import sys
from PySide import QtGui, QtCore

class listWindow(QtGui.QWidget):
    def __init__(self):
        super(listWindow, self).__init__()

        mainLayout = QtGui.QVBoxLayout()
        buttonVLayout = QtGui.QVBoxLayout()
        buttonLayout01 = QtGui.QHBoxLayout()
        buttonLayout02 = QtGui.QHBoxLayout()
        buttonLayout03 = QtGui.QHBoxLayout()

        # layout main add
        self.listWg = QtGui.QListWidget()
        self.outPathLineEditer = QtGui.QLineEdit('d:/attr.mel')

        # layout 1 add
        runButton = QtGui.QPushButton('select Check')
        lineEditer = QtGui.QLineEdit()
        filterButton = QtGui.QPushButton('filter')

        # layout 2 add
        exportButton = QtGui.QPushButton('all OutputFile')
        selectExportButton = QtGui.QPushButton('select OutputFile')

        # layout 3 add

        self.radioButton01 = QtGui.QRadioButton('translate', self)
        self.radioButton02 = QtGui.QRadioButton('rotate', self)
        self.radioButton03 = QtGui.QRadioButton('scale', self)
        self.radioButton04 = QtGui.QRadioButton('visibility', self)

        self.radioButton01.setAutoExclusive(0)
        self.radioButton02.setAutoExclusive(0)
        self.radioButton03.setAutoExclusive(0)
        self.radioButton04.setAutoExclusive(0)
        self.radioButton01.setChecked(1)
        self.radioButton02.setChecked(1)
        self.radioButton03.setChecked(1)
        self.radioButton04.setChecked(1)

        # connect
        
        exportButton.clicked.connect(self.run)

        self.listWg.addItems(['append', 'bend', 'cycle', 'system', 'code', 'mac', 'python'])
        self.listWg.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)

        buttonLayout01.addWidget(runButton)
        buttonLayout01.addWidget(lineEditer)
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
        self.setWindowTitle('List Window')

        self.setGeometry(300, 300, 200, 500)

        styleFile = open('w:/BBM/Assets/Rig/Set/Rigging/set/darkorange.stylesheet', 'r')
        self.setStyleData = styleFile.read()
        styleFile.close()
        self.setStyleSheet(self.setStyleData)

        self.show()
    def run(self):
        getList = self.listWg.selectedItems()
        for x in getList:
            print x.text()

def main():
    app = QtGui.QApplication(sys.argv)
    win = listWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
