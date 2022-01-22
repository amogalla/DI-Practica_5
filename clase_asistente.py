from PySide6.QtSql import QSqlQuery
from datetime import datetime
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QVBoxLayout, QWizard, QWizardPage, QLineEdit, QHBoxLayout, QLabel, QComboBox, QCheckBox, QSpinBox
from reportlab.pdfgen.canvas import Canvas
from PySide6.QtSql import QSqlDatabase, QSqlQuery
import pyqtgraph as pg
import pyqtgraph.exporters
from pdfrw import PdfReader
from pdfrw.buildxobj import pagexobj
from pdfrw.toreportlab import makerl
from clase_pdf import ListadoPDF

# Realizamos la carga y apertura de la base de datos
db = QSqlDatabase("QSQLITE")
db.setDatabaseName("alumnos.sqlite")

db.open()
class Asistente(QWizard):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Mi aplicación")

        self.setWizardStyle(QWizard.ModernStyle)

        self.setPixmap(QWizard.WatermarkPixmap,QPixmap('Watermark.png'))
        self.setPixmap(QWizard.LogoPixmap,QPixmap('Logo.png'))
        self.setPixmap(QWizard.BannerPixmap,QPixmap('Banner.png'))

        #PÁGINA 1
        page1 = QWizardPage()
        page1.setTitle('Generación Acta I.E.S. Virgen de la Invención')
        page1.setSubTitle('Rellena la siguiente información para generar el acta de evaluación')
        
        self.lineEdit_nombre_tutor = QLineEdit()
        self.label_nombre_tutor = QLabel("Tutor")

        self.lineEdit_nombre_delegado = QLineEdit()
        self.label_nombre_delegado = QLabel("Delegado")

        self.lineEdit_nombre_supervisor = QLineEdit()
        self.label_nombre_supervisor = QLabel("Supervisor")

        vLayout11 = QVBoxLayout(page1)
        hLayout11 = QHBoxLayout(page1)
        hLayout12 = QHBoxLayout(page1)
        hLayout13 = QHBoxLayout(page1)

        hLayout11.addWidget(self.label_nombre_tutor)
        hLayout11.addWidget(self.lineEdit_nombre_tutor)
        vLayout11.addLayout(hLayout11)

        hLayout12.addWidget(self.label_nombre_delegado)
        hLayout12.addWidget(self.lineEdit_nombre_delegado)
        vLayout11.addLayout(hLayout12)

        hLayout13.addWidget(self.label_nombre_supervisor)
        hLayout13.addWidget(self.lineEdit_nombre_supervisor)
        vLayout11.addLayout(hLayout13)

        page1.registerField('nombre_tutor*', self.lineEdit_nombre_tutor,self.lineEdit_nombre_tutor.text(),'textChanged')
        page1.registerField('nombre_delegado*', self.lineEdit_nombre_delegado,self.lineEdit_nombre_delegado.text(),'textChanged')
        page1.registerField('nombre_supervisor*', self.lineEdit_nombre_supervisor,self.lineEdit_nombre_supervisor.text(),'textChanged')
        self.addPage(page1)

        #PÁGINA 2
        page2 = QWizardPage()
        page2.setTitle('Generación Acta I.E.S. Virgen de la Invención')
        page2.setSubTitle('Rellena la siguiente información para generar el acta de evaluación')
        
        self.label_curso = QLabel("Curso")
        self.desplegable_curso = QComboBox()
        self.label_clase = QLabel("Clase")
        self.desplegable_clase = QComboBox()
        query = QSqlQuery("SELECT DISTINCT curso FROM alumnos",db=db)
        # Recorremos el resultado de esa query agregando al comboBox el listado de artistas
        while query.next():
            self.desplegable_clase.addItem(query.value(0))

        self.desplegable_curso.addItem("2021/2022")
        self.desplegable_curso.addItem("2022/2023")
        vLayout2 = QVBoxLayout(page2)
        hLayout2 = QHBoxLayout(page2)
        hLayout3 = QHBoxLayout(page2)

        hLayout2.addWidget(self.label_curso)
        hLayout2.addWidget(self.desplegable_curso)
        vLayout2.addLayout(hLayout2)

        hLayout2.addWidget(self.label_clase)
        hLayout2.addWidget(self.desplegable_clase)
        vLayout2.addLayout(hLayout3)

        page2.registerField('curso', self.desplegable_curso,self.desplegable_curso.currentText())
        page2.registerField('clase', self.desplegable_clase,self.desplegable_clase.currentText())
        self.addPage(page2)


        #PÁGINA 3
        page3 = QWizardPage()
        page3.setTitle('Generación Acta I.E.S. Virgen de la Invención')
        page3.setSubTitle('Rellena la siguiente información para generar el acta de evaluación')
        
        self.label_aprobacion_acta_anterior = QLabel("Aprobacion del acta anterior:")
        self.check_aprobacion_acta_anterior = QCheckBox()

        vLayout31 = QVBoxLayout(page3)
        hLayout31 = QHBoxLayout(page3)

        hLayout31.addWidget(self.label_aprobacion_acta_anterior)
        hLayout31.addWidget(self.check_aprobacion_acta_anterior)
        vLayout31.addLayout(hLayout31)

        page3.registerField('aprobacion', self.check_aprobacion_acta_anterior, "Test")
        self.addPage(page3)



        #PÁGINA 4
        page4 = QWizardPage()
        page4.setTitle('Generación Acta I.E.S. Virgen de la Invención')
        page4.setSubTitle('Rellena la siguiente información para generar el acta de evaluación')
        
        self.label_promocion_extraordinaria = QLabel("Alumnos con promoción extraordinaria:")
        self.spin_promocion_extraordinaria = QSpinBox()

        vLayout41 = QVBoxLayout(page4)
        hLayout41 = QHBoxLayout(page4)

        hLayout41.addWidget(self.label_promocion_extraordinaria)
        hLayout41.addWidget(self.spin_promocion_extraordinaria)
        vLayout41.addLayout(hLayout41)

        page4.registerField('promocion', self.spin_promocion_extraordinaria, self.spin_promocion_extraordinaria.text())
        self.addPage(page4)


        #PÁGINA FINAL
        pageFinal = QWizardPage()
        pageFinal.setTitle('Generación Acta I.E.S. Virgen de la Invención')
        pageFinal.setSubTitle('Información complementaria')
        self.label_itinerario = QLabel("Itinerario")
        self.desplegable_itinerario = QComboBox()
        
        self.label_optativa = QLabel("Asignatura optativa")
        self.desplegable_optativa = QComboBox()
        query = QSqlQuery("SELECT DISTINCT itinerario FROM alumnos",db=db)
        # Recorremos el resultado de esa query agregando al comboBox el listado de artistas
        while query.next():
            self.desplegable_itinerario.addItem(query.value(0))

        query2 = QSqlQuery("SELECT DISTINCT optativa FROM alumnos",db=db)
        # Recorremos el resultado de esa query agregando al comboBox el listado de artistas
        while query2.next():
            self.desplegable_optativa.addItem(query2.value(0))

        vLayout5 = QVBoxLayout(pageFinal)
        hLayout5 = QHBoxLayout(pageFinal)
        hLayout51 = QHBoxLayout(pageFinal)

        hLayout5.addWidget(self.label_itinerario)
        hLayout5.addWidget(self.desplegable_itinerario)
        vLayout5.addLayout(hLayout5)

        hLayout51.addWidget(self.label_optativa)
        hLayout51.addWidget(self.desplegable_optativa)
        vLayout5.addLayout(hLayout51)

        pageFinal.registerField('itinerario', self.desplegable_itinerario,self.desplegable_itinerario.currentText())
        pageFinal.registerField('optativa', self.desplegable_optativa,self.desplegable_optativa.currentText())
        pageFinal.setFinalPage(True)

        next = self.button(QWizard.NextButton)
        #next.clicked.connect(lambda:label.setText(page1.field('miCampo')))

        # Y también podemos recuperar la información cuando se complete el asistente
        finish = self.button(QWizard.FinishButton)
        
        finish.clicked.connect(self.generate)

        self.addPage(pageFinal)

    def button_clicked(self, s):
        self.show()


    def generate(self):
        # Creamos un diccionario con los datos
        if self.check_aprobacion_acta_anterior.isChecked():
            self.aprobado = "Aprobada"
        else:
            self.aprobado = "No aprobada"
        
        self.data = {
            'tutor': self.lineEdit_nombre_tutor.text(),
            'delegado': self.lineEdit_nombre_delegado.text(),
            'supervisor': self.lineEdit_nombre_supervisor.text(),
            'curso': self.desplegable_curso.currentText(),
            'clase': self.desplegable_clase.currentText(),
            'aprobacion_acta_anterior': self.aprobado,
            'promocion_extraordinaria': self.spin_promocion_extraordinaria.text(),
            'itinerario': self.desplegable_itinerario.currentText(),
            'optativa': self.desplegable_optativa.currentText(),
        }
        outfile = "Acta_cumplimentada.pdf"

        template = PdfReader("Acta.pdf", decompress=False).pages[0]
        template_obj = pagexobj(template)

        canvas = Canvas(outfile)

        xobj_name = makerl(canvas, template_obj)
        canvas.doForm(xobj_name)


        query_promocionan = QSqlQuery("SELECT COUNT(*) FROM alumnos WHERE suspensos3 <= 2  AND curso ='" + self.data['clase'] + "'",db=db)
        query_promocionan.next()
        query_total_alumnos = QSqlQuery("SELECT COUNT(*) FROM alumnos WHERE curso ='" + self.data['clase'] + "'",db=db)
        query_total_alumnos.next()

        #Para generar la primera gráfica, almacenamos en tres variables el número de alumnos con más de 2 suspensos en cada evaluación
        query_proyeccion_repetidores_1 = QSqlQuery("SELECT COUNT(*) FROM alumnos WHERE suspensos1 >= 3 AND curso ='" + self.data['clase'] + "'",db=db)
        query_proyeccion_repetidores_1.next()

        query_proyeccion_repetidores_2 = QSqlQuery("SELECT COUNT(*) FROM alumnos WHERE suspensos2 >= 3 AND curso ='" + self.data['clase'] + "'",db=db)
        query_proyeccion_repetidores_2.next()

        query_proyeccion_repetidores_3 = QSqlQuery("SELECT COUNT(*) FROM alumnos WHERE suspensos3 >= 3 AND curso ='" + self.data['clase'] + "'",db=db)
        query_proyeccion_repetidores_3.next()

        #Introducimos la gráfica
        #pg.PlotWidget().setBackground('w')
        pen = pg.mkPen(color=(30, 30, 255))
        plt1 = pg.plot([int(query_proyeccion_repetidores_1.value(0)),int(query_proyeccion_repetidores_2.value(0)), int(query_proyeccion_repetidores_3.value(0))], pen = pen)
        #plt1.hide()
        plt1.setBackground('w')
        exporter = pg.exporters.ImageExporter(plt1.plotItem)
        exporter.parameters()['width'] = 150   # (afecta a la altura de forma proporcional)
        exporter.export('graphic.png')
        plt1.close()
        canvas.drawImage("graphic.png", 233, 426, width=None,height=None,mask=None)

        #Para generar la 2ª gráfica, almacenamos en tres variables el número de alumnos que promocionarían en cada evaluación según el itinerario indicado.
        query_promocion1_itinerario = QSqlQuery("SELECT COUNT(*) FROM alumnos WHERE suspensos1 < 3 AND itinerario ='" + self.data['itinerario'] + "'",db=db)
        query_promocion1_itinerario.next()

        query_promocion2_itinerario = QSqlQuery("SELECT COUNT(*) FROM alumnos WHERE suspensos2 < 3 AND itinerario ='" + self.data['itinerario'] + "'",db=db)
        query_promocion2_itinerario.next()

        query_promocion3_itinerario = QSqlQuery("SELECT COUNT(*) FROM alumnos WHERE suspensos3 < 3 AND itinerario ='" + self.data['itinerario'] + "'",db=db)
        query_promocion3_itinerario.next()

        pen2 = pg.mkPen(color=(30, 30, 255))
        plt2 = pg.plot([int(query_promocion1_itinerario.value(0)),int(query_promocion2_itinerario.value(0)), int(query_promocion3_itinerario.value(0))], pen = pen2)
        plt2.hide()
        plt2.setBackground('w')
        exporter2 = pg.exporters.ImageExporter(plt2.plotItem)
        exporter2.parameters()['width'] = 130   # (afecta a la altura de forma proporcional)
        exporter2.export('graphic2.png')
        #plt2.close()
        canvas.drawImage("graphic2.png", 145, 270, width=None,height=None,mask=None)
        canvas.drawString(181, 252, self.data['itinerario'])



        #Para generar la 3ª gráfica, almacenamos en tres variables el número de alumnos que promocionarían en cada evaluación según la optativa indicada.
        query_promocion1_optativa = QSqlQuery("SELECT COUNT(*) FROM alumnos WHERE suspensos1 < 3 AND optativa ='" + self.data['optativa'] + "'",db=db)
        query_promocion1_optativa.next()

        query_promocion2_optativa = QSqlQuery("SELECT COUNT(*) FROM alumnos WHERE suspensos2 < 3 AND optativa ='" + self.data['optativa'] + "'",db=db)
        query_promocion2_optativa.next()

        query_promocion3_optativa = QSqlQuery("SELECT COUNT(*) FROM alumnos WHERE suspensos3 < 3 AND optativa ='" + self.data['optativa'] + "'",db=db)
        query_promocion3_optativa.next()

        pen3 = pg.mkPen(color=(30, 30, 255))
        plt3 = pg.plot([int(query_promocion1_optativa.value(0)),int(query_promocion2_optativa.value(0)), int(query_promocion3_optativa.value(0))], pen = pen3)
        plt3.hide()
        plt3.setBackground('w')
        exporter3 = pg.exporters.ImageExporter(plt3.plotItem)
        exporter3.parameters()['width'] = 130   # (afecta a la altura de forma proporcional)
        exporter3.export('graphic3.png')
        #plt2.close()
        canvas.drawImage("graphic3.png", 355, 270, width=None,height=None,mask=None)
        canvas.drawString(395, 252, self.data['optativa'])
        
        porcentaje_promocionados = str(round(100 * float(query_promocionan.value(0))/float(query_total_alumnos.value(0))))
        porcentaje_total_promocionados = str(round(100 * (float(query_promocionan.value(0)) + float(self.data['promocion_extraordinaria']))/float(query_total_alumnos.value(0))))
        
        ystart = 670
        canvas.drawString(92, ystart+7, self.data['tutor'])

        # Ponemos la fecha de hoy
        today = datetime.today()
        #canvas.drawString(444, ystart-577, today.strftime('%F'))
        canvas.drawString(150, ystart+29, today.strftime('%F'))

        canvas.drawString(186, ystart-469, str(query_total_alumnos.value(0)))
        canvas.drawString(493, ystart-469, str(query_promocionan.value(0)))
        canvas.drawString(280, ystart+111, self.data['curso'])
        canvas.drawString(379, ystart+29, self.data['clase'])
        canvas.drawString(110, ystart-52, self.data['aprobacion_acta_anterior'])
        canvas.drawString(177, ystart-12, self.data['delegado'])
        canvas.drawString(410, ystart+7, self.data['supervisor'])
        canvas.drawString(205, ystart-510, self.data['promocion_extraordinaria'])
        canvas.drawString(215, ystart-490, porcentaje_promocionados)
        canvas.drawString(383, ystart-531, porcentaje_total_promocionados)

        canvas.save()
        #QMessageBox.information(self, "Finalizado", "Se ha generado el PDF")

        self.informe = ListadoPDF()
        self.informe.show()
