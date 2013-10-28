import sys
from PySide import QtGui, QtCore

class listWindow(QtGui.QWidget):
    def __init__(self):
        super(listWindow, self).__init__()

        mainLayout = QtGui.QVBoxLayout()
        self.listWg = QtGui.QListWidget()
        button = QtGui.QPushButton('alpha')

        button.clicked.connect(self.run)

        self.listWg.addItems(['append', 'bend', 'cycle', 'system', 'code', 'mac', 'python'])
        self.listWg.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)

        mainLayout.addWidget(self.listWg)
        mainLayout.addWidget(button)

        self.setLayout(mainLayout)
        self.setWindowTitle('List Window')
        self.setGeometry(300, 300, 200, 500)
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

