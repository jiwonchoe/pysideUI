
import sys, glob
from PySide import QtGui, QtCore


class texModel(QtCore.QAbstractTableModel):
    def __init__(self, files = [[]], headers = [], parent=None):

        super(texModel, self).__init__(parent)

        self.files = files
        self.headers = headers

    def headerData(self, section, orientation, role):

        if role == QtCore.Qt.DisplayRole:

            if orientation == QtCore.Qt.Horizontal:
                if section < len(self.headers):
                    return self.headers[section]
                else:
                    return 'name'
            else:
                return 'mayaFile %02d' % (section+1)

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
            text = str(value)

            if type(text) ==  str:
                self.files[col][row] = text
                self.dataChanged.emit(index, index)
                return True

        return False



class testView(QtGui.QWidget):
    def __init__(self, parent=None):

        super(testView, self).__init__(parent)

        mainLayout = QtGui.QHBoxLayout()

        self.view = QtGui.QTableView()

        mainLayout.addWidget(self.view)

        self.setLayout(mainLayout)
        self.setWindowTitle('Test table')

        self.show()

def main():
    app = QtGui.QApplication(sys.argv)
    windows = testView()
    headers = ['typeA', 'typeB']
    inList = glob.glob('d:\\*.mb')
    inList2 = glob.glob('d:\\*.mb')
    inList = [inList] + [inList2]
    model = texModel(inList, headers)
    windows.view.setModel(model)

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
