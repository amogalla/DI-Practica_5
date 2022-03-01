# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'design.ui'
##
## Created by: Qt User Interface Compiler version 6.2.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QFormLayout, QGroupBox,
    QHeaderView, QLabel, QLineEdit, QMainWindow,
    QMenu, QMenuBar, QSizePolicy, QStatusBar,
    QTableView, QToolBar, QVBoxLayout, QWidget)
from PySide6.QtWidgets import QGraphicsOpacityEffect, QHBoxLayout, QMainWindow, QVBoxLayout, QWidget
from PySide6 import QtCore, QtWidgets

import resources_rc
from smilerating import SmileRating

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.actionInsertar = QAction(MainWindow)
        self.actionInsertar.setObjectName(u"actionInsertar")
        icon = QIcon()
        icon.addFile(u":/icons/database--plus.png", QSize(), QIcon.Normal, QIcon.Off)
        self.actionInsertar.setIcon(icon)
        self.actionModificar = QAction(MainWindow)
        self.actionModificar.setObjectName(u"actionModificar")
        icon1 = QIcon()
        icon1.addFile(u":/icons/database--arrow.png", QSize(), QIcon.Normal, QIcon.Off)
        self.actionModificar.setIcon(icon1)
        self.actionEliminar = QAction(MainWindow)
        self.actionEliminar.setObjectName(u"actionEliminar")
        icon2 = QIcon()
        icon2.addFile(u":/icons/database--minus.png", QSize(), QIcon.Normal, QIcon.Off)
        self.actionEliminar.setIcon(icon2)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.formLayout = QFormLayout(self.groupBox)
        self.formLayout.setObjectName(u"formLayout")

        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")
        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.lineEdit_ID = QLineEdit(self.groupBox)
        self.lineEdit_ID.setObjectName(u"lineEdit_ID")
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.lineEdit_ID)

        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")
        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_2)
        
        self.lineEdit_nombre = QLineEdit(self.groupBox)
        self.lineEdit_nombre.setObjectName(u"lineEdit_nombre")
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.lineEdit_nombre)

        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")
        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_3)
                
        self.lineEdit_apellidos = QLineEdit(self.groupBox)
        self.lineEdit_apellidos.setObjectName(u"lineEdit_apellidos")
        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.lineEdit_apellidos)

        self.label_4 = QLabel(self.groupBox)
        self.label_4.setObjectName(u"label_4")
        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_4)

        self.comboBox_curso = QComboBox(self.groupBox)
        self.comboBox_curso.setObjectName(u"comboBox_curso")
        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.comboBox_curso)

        self.label_5 = QLabel(self.groupBox)
        self.label_5.setObjectName(u"label_5")
        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.label_5)

        self.lineEdit_suspensos1 = QLineEdit(self.groupBox)
        self.lineEdit_suspensos1.setObjectName(u"lineEdit_suspensos1")
        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.lineEdit_suspensos1)

        self.label_6 = QLabel(self.groupBox)
        self.label_6.setObjectName(u"label_6")
        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.label_6)

        self.lineEdit_suspensos2 = QLineEdit(self.groupBox)
        self.lineEdit_suspensos2.setObjectName(u"lineEdit_suspensos2")
        self.formLayout.setWidget(5, QFormLayout.FieldRole, self.lineEdit_suspensos2)

        self.label_7 = QLabel(self.groupBox)
        self.label_7.setObjectName(u"label_7")
        self.formLayout.setWidget(6, QFormLayout.LabelRole, self.label_7)

        self.lineEdit_suspensos3 = QLineEdit(self.groupBox)
        self.lineEdit_suspensos3.setObjectName(u"lineEdit_suspensos3")
        self.formLayout.setWidget(6, QFormLayout.FieldRole, self.lineEdit_suspensos3)

        self.label_8 = QLabel(self.groupBox)
        self.label_8.setObjectName(u"label_8")
        self.formLayout.setWidget(7, QFormLayout.LabelRole, self.label_8)

        self.lineEdit_itinerario = QLineEdit(self.groupBox)
        self.lineEdit_itinerario.setObjectName(u"lineEdit_itinerario")
        self.formLayout.setWidget(7, QFormLayout.FieldRole, self.lineEdit_itinerario)

        self.label_9 = QLabel(self.groupBox)
        self.label_9.setObjectName(u"label_9")
        self.formLayout.setWidget(8, QFormLayout.LabelRole, self.label_9)

        self.lineEdit_optativa = QLineEdit(self.groupBox)
        self.lineEdit_optativa.setObjectName(u"lineEdit_optativa")
        self.formLayout.setWidget(8, QFormLayout.FieldRole, self.lineEdit_optativa)

        self.label_10 = QLabel(self.groupBox)
        self.label_10.setObjectName(u"label_10")
        self.formLayout.setWidget(9, QFormLayout.LabelRole, self.label_10)

        self.lineEdit_repetidor = QLineEdit(self.groupBox)
        self.lineEdit_repetidor.setObjectName(u"lineEdit_repetidor")
        self.formLayout.setWidget(9, QFormLayout.FieldRole, self.lineEdit_repetidor)

        self.verticalLayout_2.addWidget(self.groupBox)

        self.tabla = QTableView(self.centralwidget)
        self.tabla.setObjectName(u"tabla")

        self.verticalLayout_2.addWidget(self.tabla)

        self.boton = QtWidgets.QPushButton(self.centralwidget) # Creamos el widget Boton
        self.boton.setText("Generar acta de evaluación")
        self.verticalLayout_2.addWidget(self.boton)
        self.botonGrafica = QtWidgets.QPushButton(self.centralwidget) # Creamos el widget Boton
        self.botonGrafica.setText("Gráfica de alumnos matriculados en cada itinerario")
        self.verticalLayout_2.addWidget(self.botonGrafica)

        #COMPONENTE AÑADIDO (@author: Pedro G. Morales)
        self.smileRating = SmileRating("¡Gracias!")
        self.verticalLayout_2.addWidget(self.smileRating)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 24))
        self.menuRegistro = QMenu(self.menubar)
        self.menuRegistro.setObjectName(u"menuRegistro")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QToolBar(MainWindow)
        self.toolBar.setObjectName(u"toolBar")
        MainWindow.addToolBar(Qt.TopToolBarArea, self.toolBar)

        self.menubar.addAction(self.menuRegistro.menuAction())
        self.menuRegistro.addAction(self.actionInsertar)
        self.menuRegistro.addAction(self.actionModificar)
        self.menuRegistro.addAction(self.actionEliminar)
        self.toolBar.addAction(self.actionInsertar)
        self.toolBar.addAction(self.actionModificar)
        self.toolBar.addAction(self.actionEliminar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionInsertar.setText(QCoreApplication.translate("MainWindow", u"Insertar", None))
#if QT_CONFIG(shortcut)
        self.actionInsertar.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+I", None))
#endif // QT_CONFIG(shortcut)
        self.actionModificar.setText(QCoreApplication.translate("MainWindow", u"Modificar", None))
#if QT_CONFIG(shortcut)
        self.actionModificar.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+M", None))
#endif // QT_CONFIG(shortcut)
        self.actionEliminar.setText(QCoreApplication.translate("MainWindow", u"Eliminar", None))
#if QT_CONFIG(shortcut)
        self.actionEliminar.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+D", None))
#endif // QT_CONFIG(shortcut)
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Datos del alumno", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"ID", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Nombre", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Apellidos", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Curso", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Suspensos 1", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Suspensos 2", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Suspensos 3", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Itinerario", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Optativa", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Repetidor", None))
        self.menuRegistro.setTitle(QCoreApplication.translate("MainWindow", u"Registro", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
    # retranslateUi

