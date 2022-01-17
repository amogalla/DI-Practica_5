import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QAbstractItemView
from PySide6.QtSql import QSqlDatabase, QSqlQuery, QSqlRelation, QSqlRelationalTableModel
from PySide6.QtCore import Qt
from design import Ui_MainWindow
from datetime import datetime
import sys
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWizard, QWizardPage, QLineEdit, QHBoxLayout, QLabel
from PySide6.QtWidgets import QMessageBox, QPushButton, QLineEdit, QApplication, QComboBox, QCheckBox, QSpinBox
from reportlab.pdfgen.canvas import Canvas
from PySide6.QtSql import QSqlDatabase, QSqlQuery, QSqlRelation, QSqlRelationalTableModel

from pdfrw import PdfReader
from pdfrw.buildxobj import pagexobj
from pdfrw.toreportlab import makerl
# Realizamos la carga y apertura de la base de datos
db = QSqlDatabase("QSQLITE")
db.setDatabaseName("alumnos3.sqlite")

db.open()

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        
        # Cargamos la UI
        self.setupUi(self)
        self.boton.clicked.connect(self.button_clicked)
        # Deshabilitamos la edición del cuadro de texto del ID
        self.lineEdit_ID.setEnabled(False)

        # Creamos una query para obtener todos los artistas de la tabla Artist
        query = QSqlQuery("SELECT DISTINCT curso FROM alumnos",db=db)
        # Recorremos el resultado de esa query agregando al comboBox el listado de artistas
        while query.next():
            self.comboBox_curso.addItem(query.value(0))

        # Creamos un modelo relacional de SQL
        self.modelo = QSqlRelationalTableModel(db=db)
        # Establecemos Album como tabla del modelo
        self.modelo.setTable("alumnos")
        # Establecemos la relación entre el ID de los artistas y su nombre, para que se muestre este último
        #self.modelo.setRelation(2, QSqlRelation("nombre", "apellidos", "curso"))
        # Hacemos el select del modelo
        self.modelo.select()
        # Renombramos las cabeceras de la tabla
        self.modelo.setHeaderData(1, Qt.Horizontal, "Nombre")
        self.modelo.setHeaderData(2, Qt.Horizontal, "Apellidos")
        self.modelo.setHeaderData(3, Qt.Horizontal, "Curso")

        # Establecemos el modelo en el tableView
        self.tabla.setModel(self.modelo)
        # Ajustamos el tamaño de las columnas al contenido
        self.tabla.resizeColumnsToContents()

        # Deshabilitamos la edición directa de la tabla
        self.tabla.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # Establecemos que se seleccionen filas completas en lugar de celdas individuales
        self.tabla.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tabla.setSelectionBehavior(QAbstractItemView.SelectRows)

        # Creamos la señal: Cuando cambie la seleccion, ejecuta self.seleccion
        self.tabla.selectionModel().selectionChanged.connect(self.seleccion)
        # Creamos la señal: Cuando se ejecute la acción Modificar, ejecuta self.modificar
        self.actionModificar.triggered.connect(self.modificar)
        # Creamos la señal: Cuando se ejecute la acción Insertar, ejecuta self.nueva
        self.actionInsertar.triggered.connect(self.nueva)
        # Creamos la señal: Cuando se ejecute la acción Eliminar, ejecuta self.borrar
        self.actionEliminar.triggered.connect(self.borrar)

        # Ponemos la fila inicial a un valor que indica que no está seleccionada ninguna fila
        self.fila = -1

        self.asistente = Asistente()

    def button_clicked(self, s):
        self.asistente.show()

    def seleccion(self, seleccion):
        # Recuerda que indexes almacena los índices de la selección
        if seleccion.indexes():
            # Nos quedamos con la fila del primer índice (solo se puede seleccionar una fila)
            self.fila = seleccion.indexes()[0].row()
            # Obtenemos los valores id, titulo y artista del modelo en esa fila
            id = self.modelo.index(self.fila, 0).data()
            nombre = self.modelo.index(self.fila, 1).data()
            apellidos = self.modelo.index(self.fila, 2).data()
            curso = self.modelo.index(self.fila, 3).data()
            suspensos1 = self.modelo.index(self.fila, 4).data()
            suspensos2 = self.modelo.index(self.fila, 5).data()
            suspensos3 = self.modelo.index(self.fila, 6).data()
            itineario = self.modelo.index(self.fila, 7).data()
            optativa = self.modelo.index(self.fila, 8).data()
            repetidor = self.modelo.index(self.fila, 9).data()
            # Modificamos los campos del formulario para establecer esos valores
            self.lineEdit_ID.setText(str(id))
            self.lineEdit_nombre.setText(nombre)
            indice = self.comboBox_curso.findText(curso)
            self.comboBox_curso.setCurrentIndex(indice)
            self.lineEdit_apellidos.setText(apellidos)
            self.lineEdit_suspensos1.setText(str(suspensos1))
            self.lineEdit_suspensos2.setText(str(suspensos2))
            self.lineEdit_suspensos3.setText(str(suspensos3))
            self.lineEdit_itinerario.setText(itineario)
            self.lineEdit_optativa.setText(optativa)
            self.lineEdit_repetidor.setText(str(repetidor))
        else:
            # Si no hay selección,  ponemos la fila inicial a un valor que indica que no está seleccionada ninguna fila
            self.fila = -1

    def modificar(self):
        # Si es una fila válida la seleccionada
        if self.fila >= 0:
            # Obtenemos los valores de los campos del formulario
            id = self.lineEdit_ID.text()
            nombre = self.lineEdit_nombre.text()
            apellidos = self.lineEdit_apellidos.text()
            curso = self.comboBox_curso.currentText()
            suspensos1 = self.lineEdit_suspensos1.text()
            suspensos2 = self.lineEdit_suspensos2.text()
            suspensos3 = self.lineEdit_suspensos3.text()
            itinerario = self.lineEdit_itinerario.text()
            optativa = self.lineEdit_optativa.text()
            repetidor = self.lineEdit_repetidor.text()
            #query = QSqlQuery("SELECT id FROM alumnos WHERE curso='"+curso+"'",db=db)
            #while query.next():
            #    indice=query.value(0)
            # Actualizamos los campos en el modelo
            self.modelo.setData(self.modelo.index(self.fila, 0), id)
            self.modelo.setData(self.modelo.index(self.fila, 1), nombre)
            self.modelo.setData(self.modelo.index(self.fila, 2), apellidos)
            self.modelo.setData(self.modelo.index(self.fila, 3), curso)
            self.modelo.setData(self.modelo.index(self.fila, 4), suspensos1)
            self.modelo.setData(self.modelo.index(self.fila, 5), suspensos2)
            self.modelo.setData(self.modelo.index(self.fila, 6), suspensos3)
            self.modelo.setData(self.modelo.index(self.fila, 7), itinerario)
            self.modelo.setData(self.modelo.index(self.fila, 8), optativa)
            self.modelo.setData(self.modelo.index(self.fila, 9), repetidor)
            # Ejecutamos los cambios en el modelo
            self.modelo.submit()

    def nueva(self):
        # Guardamos en la variable nuevaFila el número de filas del modelo
        nuevaFila = self.modelo.rowCount()
        # Insertamos una nueva fila en el modelo en la posición de ese valor
        self.modelo.insertRow(nuevaFila)
        # Seleccionamos la fila nueva
        self.tabla.selectRow(nuevaFila)
        query = QSqlQuery("SELECT id FROM alumnos",db=db)
        while query.next():
            indice=query.value(0)
        # Ponemos en blanco el texto del título en el formulario
        self.lineEdit_nombre.setText("")
        self.lineEdit_apellidos.setText("")
        self.lineEdit_suspensos1.setText("")
        self.lineEdit_suspensos2.setText("")
        self.lineEdit_suspensos3.setText("")
        self.lineEdit_itinerario.setText("")
        self.lineEdit_optativa.setText("")
        self.lineEdit_repetidor.setText("")
        self.lineEdit_ID.setText(str(indice + 1))
        # Ponemos el comboBox de artistas al primero de la lista
        self.comboBox_curso.setCurrentIndex(0)
        # Establecemos en blanco los valores (título y artista) de esa nueva fila
        self.modelo.setData(self.modelo.index(nuevaFila, 1), "")
        self.modelo.setData(self.modelo.index(nuevaFila, 2), "")
        self.modelo.setData(self.modelo.index(nuevaFila, 3), "3º ESO")
        self.modelo.setData(self.modelo.index(nuevaFila, 4), "")
        self.modelo.setData(self.modelo.index(nuevaFila, 5), "")
        self.modelo.setData(self.modelo.index(nuevaFila, 6), "")
        self.modelo.setData(self.modelo.index(nuevaFila, 7), "")
        self.modelo.setData(self.modelo.index(nuevaFila, 8), "")
        self.modelo.setData(self.modelo.index(nuevaFila, 9), "")
        # Ejecutamos los cambios en el modelo
        self.modelo.submit()

    def borrar(self):
        # Si es una fila válida la seleccionada
        if self.fila >= 0:
            # Borramos la fila en el modelo
            self.modelo.removeRow(self.fila)
            # Actualizamos la tabla
            self.modelo.select()
            # Y ponemos la fila actual a -1
            self.fila = -1
            # Reseteamos los valores en los campos del formulario
            self.lineEdit_ID.setText("")
            self.lineEdit_nombre.setText("")
            self.lineEdit_apellidos.setText("")
            self.comboBox_curso.setCurrentIndex(0)
            self.lineEdit_suspensos1.setText("")
            self.lineEdit_suspensos2.setText("")
            self.lineEdit_suspensos3.setText("")
            self.lineEdit_itinerario.setText("")
            self.lineEdit_optativa.setText("")
            self.lineEdit_repetidor.setText("")

class Asistente(QWizard):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Mi aplicación")

        #self.button = QPushButton("Presióname para un Wizard")
        #self.button.clicked.connect(self.button_clicked)
        #self.setCentralWidget(self.button)
        
        #self.wizard = QWizard()

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
        pageFinal.setSubTitle('Confirmación de generación de acta')
        label = QLabel()
        hLayout2 = QHBoxLayout(pageFinal)
        hLayout2.addWidget(label)
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
            
        }
        outfile = "Acta_cumplimentada.pdf"

        template = PdfReader("Acta.pdf", decompress=False).pages[0]
        template_obj = pagexobj(template)

        canvas = Canvas(outfile)

        xobj_name = makerl(canvas, template_obj)
        canvas.doForm(xobj_name)


        query_promocionan = QSqlQuery("SELECT COUNT(*) FROM alumnos WHERE suspensos3 <= 2",db=db)
        query_promocionan.next()
        query_total_alumnos = QSqlQuery("SELECT COUNT(*) FROM alumnos",db=db)
        query_total_alumnos.next()

        porcentaje_promocionados = str(round(100 * float(query_promocionan.value(0))/float(query_total_alumnos.value(0))))
        ystart = 670
        canvas.drawString(92, ystart+7, self.data['tutor'])

        # Ponemos la fecha de hoy
        today = datetime.today()
        canvas.drawString(444, ystart-577, today.strftime('%F'))
        canvas.drawString(150, ystart+30, today.strftime('%F'))

        canvas.drawString(280, ystart+111, self.data['curso'])
        canvas.drawString(379, ystart+30, self.data['clase'])
        canvas.drawString(110, ystart-52, self.data['aprobacion_acta_anterior'])
        canvas.drawString(177, ystart-12, self.data['delegado'])
        canvas.drawString(410, ystart+7, self.data['supervisor'])
        canvas.drawString(412, ystart-490, self.data['promocion_extraordinaria'])
        canvas.drawString(440, ystart-470, porcentaje_promocionados)

        canvas.save()
        QMessageBox.information(self, "Finalizado", "Se ha generado el PDF")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
