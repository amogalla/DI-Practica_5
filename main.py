import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QAbstractItemView
from PySide6.QtSql import QSqlDatabase, QSqlQuery, QSqlRelationalTableModel
from design import Ui_MainWindow
from PySide6.QtWidgets import QApplication, QMainWindow
import pyqtgraph as pg
from clase_asistente import Asistente
import pyqtgraph.exporters

from pdfrw import PdfReader
from pdfrw.buildxobj import pagexobj
from pdfrw.toreportlab import makerl
# Realizamos la carga y apertura de la base de datos


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.db = QSqlDatabase("QSQLITE")
        self.db.setDatabaseName("alumnos.sqlite")

        self.db.open()
        # Cargamos la UI
        self.setupUi(self)
        self.boton.clicked.connect(self.button_clicked)
        self.botonGrafica.clicked.connect(self.mostrar_grafica)
        
        # Deshabilitamos la edición del cuadro de texto del ID
        self.lineEdit_ID.setEnabled(False)

        # Creamos una query para obtener todos los artistas de la tabla Artist
        query = QSqlQuery("SELECT DISTINCT curso FROM alumnos",db=self.db)
        # Recorremos el resultado de esa query agregando al comboBox el listado de artistas
        while query.next():
            self.comboBox_curso.addItem(query.value(0))

        # Creamos un modelo relacional de SQL
        self.modelo = QSqlRelationalTableModel(db=self.db)
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

    #def prueba(self):
       # return 3

    def button_clicked(self, s):
        self.asistente.show()
    
    def mostrar_grafica(self, s):
        #Para generar la primera gráfica, almacenamos en tres variables el número de alumnos con más de 2 suspensos en cada evaluación
        query_matriculados_ciencias = QSqlQuery("SELECT COUNT(*) FROM alumnos WHERE itinerario ='Ciencias'",db=self.db)
        query_matriculados_ciencias.next()

        query_matriculados_sociales = QSqlQuery("SELECT COUNT(*) FROM alumnos WHERE itinerario ='Sociales'",db=self.db)
        query_matriculados_sociales.next()

        query_matriculados_humanidades = QSqlQuery("SELECT COUNT(*) FROM alumnos WHERE itinerario ='Humanidades'",db=self.db)
        query_matriculados_humanidades.next()

        #Introducimos la gráfica
        #self.graphWidget = pg.PlotWidget()
        #self.setCentralWidget(self.graphWidget)

        #self.graphWidget.setBackground('w')
        pen = pg.mkPen(color=(30, 30, 255))
        grafica = pg.plot([int(query_matriculados_ciencias.value(0)),int(query_matriculados_sociales.value(0)), int(query_matriculados_humanidades.value(0))], pen = pen)
        grafica.setBackground('w')


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

            #print(self.fila)
            print(self.tabla.selectionModel().selectedIndexes()[0].row())
            #print(seleccion)
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

    def num_alumnos(self):
        query = QSqlQuery("SELECT id FROM alumnos",db=self.db)
        while query.next():
            indice=query.value(0)
        return indice

    def nueva(self):
        # Guardamos en la variable nuevaFila el número de filas del modelo
        nuevaFila = self.modelo.rowCount()
        # Insertamos una nueva fila en el modelo en la posición de ese valor
        self.modelo.insertRow(nuevaFila)
        # Seleccionamos la fila nueva
        self.tabla.selectRow(nuevaFila)
        self.numero_alumnos = self.num_alumnos()
        # Ponemos en blanco los textos
        self.lineEdit_nombre.setText("")
        self.lineEdit_apellidos.setText("")
        self.lineEdit_suspensos1.setText("")
        self.lineEdit_suspensos2.setText("")
        self.lineEdit_suspensos3.setText("")
        self.lineEdit_itinerario.setText("")
        self.lineEdit_optativa.setText("")
        self.lineEdit_repetidor.setText("")
        self.lineEdit_ID.setText(str(self.numero_alumnos + 1))
        self.comboBox_curso.setCurrentIndex(0)
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    
    window.show()
    sys.exit(app.exec())
