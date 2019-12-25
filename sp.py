from PyQt5 import QtWidgets, uic
from spwin import Ui_MainWindow
import scanner_portov
import sys
from threading import Thread
from time import sleep,time
import re
class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.scan)
        self.ui.lineEdit.setToolTip("Напишите диапазон IP формата:\n192.168.110.0-255")
        self.ui.lineEdit_2.setToolTip("Напишите диапазон портов формата:\ntcp : 1-1000")
        self.ui.lineEdit.setText("192.168.100.1-20")
        self.ui.lineEdit_2.setText("tcp : 1-1000")
        self.ui.tableWidget.setColumnCount(2)
    def scan(self):
        scanner_portov.timeout_S = self.ui.spinBox.value()
        scanner_portov.timeout_A = self.ui.spinBox_2.value()
        scanner_portov.timeout_F = self.ui.spinBox_3.value()
        scanner_portov.mesto_2 = self.ui.spinBox_4.value()
        if self.ui.checkBox.isChecked() == True:
            scanner_portov.code[0] = True
        else:
            scanner_portov.code[0] = False
        if self.ui.checkBox_2.isChecked() == True:
            scanner_portov.code[1] = True
        else:
            scanner_portov.code[1] = False
        if self.ui.checkBox_3.isChecked() == True:
            scanner_portov.code[2] = True
        else:
            scanner_portov.code[2] = False
        print(scanner_portov.code)
        a = self.ui.lineEdit.text()
        a1 = self.ui.lineEdit_2.text()
        b = a.split(".")
        a1 = a1.split()
        a1 = a1[2].split("-")
        scanner_portov.port_range = (int(a1[0]),int(a1[1]))
        a=b[0]+"."+b[1]+"."+b[2]+"."
        scanner_portov.ipaddr=[a + str(i) for i in range(int(b[3].split("-")[0]),int(b[3].split("-")[1]))]
        max = len(range(int(b[3].split("-")[0]),int(b[3].split("-")[1]))) + len(range(int(b[3].split("-")[0]),int(b[3].split("-")[1]))) * 1000
        min = 0
        progb = pb()
        progb.start()
        scanner_portov.start()
        marker=0
        self.ui.tableWidget.setRowCount(len(scanner_portov.d))
        self.ui.tableWidget.setColumnCount(2)
        self.column=["IP","Открытые порты"]
        self.ui.tableWidget.setHorizontalHeaderLabels(self.column)
        for i in scanner_portov.d:
            self.ui.tableWidget.setItem(marker,0,QtWidgets.QTableWidgetItem(i))
            self.ui.tableWidget.setItem(marker,1,QtWidgets.QTableWidgetItem(str(scanner_portov.d[i])[1:-1].replace("'","")))
            marker+=1
        marker=0
app = QtWidgets.QApplication([])
application = mywindow()
class pb(Thread):
    def __init__(self):
        Thread.__init__(self)
    def run(self):
        global application
        application.ui.progressBar.setMinimum(scanner_portov.min)
        while True:
            application.ui.progressBar.setMaximum(scanner_portov.max)
            application.ui.progressBar.setValue(scanner_portov.value)
            print("not yet:" + str(scanner_portov.value) + " " + str(scanner_portov.max) + "\n")
            sleep(1)
            if scanner_portov.max == scanner_portov.value:
                application.ui.progressBar.setMaximum(scanner_portov.max)
                application.ui.progressBar.setValue(scanner_portov.value)
                break
application.show()
sys.exit(app.exec())