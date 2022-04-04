import webbrowser

from PyQt5 import QtCore, QtGui, QtWidgets
from searcher import *

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(450, 700)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.additem_pushButton = QtWidgets.QPushButton(self.centralwidget, clicked= lambda: self.search())
        self.additem_pushButton.setGeometry(QtCore.QRect(10, 50, 430, 30))
        self.additem_pushButton.setObjectName("additem_pushButton")
        self.additem_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.additem_lineEdit.setGeometry(QtCore.QRect(10, 10, 430, 30))
        self.additem_lineEdit.setObjectName("additem_lineEdit")
        self.mylist_listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.mylist_listWidget.setGeometry(QtCore.QRect(10, 90, 430, 600))
        self.mylist_listWidget.setObjectName("mylist_listWidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.mylist_listWidget.itemClicked.connect(self.сlicked)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    # Add Item To List
    def search(self):
        self.mylist_listWidget.clear()
        request = self.additem_lineEdit.text()
        result_docs = searcher.search(request)
        result_links = searcher.get_links(result_docs)
        for link in result_links:
            self.mylist_listWidget.addItem(link)
        self.additem_lineEdit.setText("")

    def delete_it(self):
        clicked = self.mylist_listWidget.currentRow()
        self.mylist_listWidget.takeItem(clicked)

    def clear_it(self):
        self.mylist_listWidget.clear()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Habr search"))
        self.additem_pushButton.setText(_translate("MainWindow", "Search"))

    def сlicked(self, item):
        webbrowser.open(item.text(), new=0, autoraise=True)


if __name__ == "__main__":
    searcher = Searcher()
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

