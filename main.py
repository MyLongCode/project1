import sys
import os
import PyQt5
import matplotlib.animation as animation
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QEvent, QPropertyAnimation, QCoreApplication, Qt, QPoint, QAbstractAnimation, QPointF
from PyQt5.QtChart import QChart, QChartView, QLineSeries
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtWidgets import *
from PySide2 import *
from ui_interface import *
import numpy as np
from random import randint


class Chart(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.setGeometry(10,10,600,400)


        series = QLineSeries()
        my_list = [(73 + np.random.rand()) for i in range(100)]
        for i in range(100):
            series.append(i,my_list[i - 1])



        chart = QChart()
        chart.addSeries(series)
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setTitle("Рандомный график")
        chart.setTheme(QChart.ChartThemeDark)

        chartview = QChartView(chart)

        vbox = QVBoxLayout()
        vbox.addWidget(chartview)
        self.setLayout(vbox)


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.mode = 0 #окно в обычном состоянии
        self.__press_pos = QPoint() #движение окна
        self.chartOn = 0





        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setWindowIcon(QtGui.QIcon("icons/логотип.svg"))

        self.ui.close.clicked.connect(QCoreApplication.instance().quit) #закрыть
        self.ui.expand.clicked.connect(self.expandWindow)
        self.ui.turn.clicked.connect(self.turnWindow)
        self.ui.menuTurn.clicked.connect(self.turnMenu)
        self.ui.username.clicked.connect(self.profileWidget)
        self.ui.dvsoft.clicked.connect(self.mainWidget)
        self.ui.pushButton_5.clicked.connect(self.course)

        self.show()


    def course(self):
        self.ui.label_6.hide()
        self.ui.label_5.hide()
        self.chart = Chart(self.ui.main)
        self.chart.show()
        self.chartOn = 1


    def mainWidget(self):
        self.ui.label_6.show()
        self.ui.label_5.show()
        if self.chartOn == 1:
            self.chart.close()
            self.chartOn = 0

    def profileWidget(self):
        if self.ui.label_6:
            self.ui.label_6.hide()
            self.ui.label_5.hide()


    def turnMenu(self): #выпадающее меню
        width = self.ui.leftMenu.width()
        if width == 200:
            newWidth = 0
            self.ui.menuTurn.setIcon(QtGui.QIcon("icons/под-меню.svg"))
            self.ui.leftMenu.setMinimumSize(QtCore.QSize(0, 0))
            self.ui.leftMenu.setMaximumSize(QtCore.QSize(0, 16777215))
        else:
            newWidth = 200
            self.ui.menuTurn.setIcon(QtGui.QIcon("icons/свернуть бар.svg"))

        self.animation = QPropertyAnimation(self.ui.leftMenu, b"maximumWidth")
        self.animation.setDuration(250)
        self.animation.setStartValue(width)
        self.animation.setEndValue(newWidth)
        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animation.start()



    def expandWindow(self): #cвернуть развернуть
        if self.mode == 0:
            self.showMaximized()
            self.mode = 1
        else:
            self.showNormal()
            self.mode = 0
    def turnWindow(self): #свернуть окно
        self.showMinimized()

    def mousePressEvent(self, event): #движение окна
        if event.button() == Qt.LeftButton and self.mode == 0:
            self.__press_pos = event.pos()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.mode == 0:
            self.__press_pos = QPoint()

    def mouseMoveEvent(self, event):
        if not self.__press_pos.isNull() and self.mode == 0:
            self.move(self.pos() + (event.pos() - self.__press_pos))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())