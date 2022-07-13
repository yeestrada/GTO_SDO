import matplotlib.pyplot as plt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import numpy as np
import os

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import functions as u
from translation import tr as _, lang

class Ui_MainWindow(QMainWindow):
    significance_level = 0.05
    difference_umbral = 0.01
    save_folder = None
    column = -1
    test = _[lang]['average']
    criteria = 'aic'
    files, logs = [], []
    use_gto = False
    GTO_data = {'pop_size': 30, 'max_iter': 100, 'lower_bound': -100, 'upper_bound': 100, 'variables_no': 10}

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(858, 599)
        MainWindow.setWindowIcon(QIcon("C:/SDO/img/app.png"))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget_2 = QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setGeometry(QRect(0, 0, 831, 551))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_3 = QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_3.setContentsMargins(10, 10, 10, 0)
        self.verticalLayout_3.setSpacing(5)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tableView = QTableView(self.verticalLayoutWidget_2)
        self.tableView.setMinimumSize(QSize(0, 0))
        self.tableView.setObjectName("tableView")
        self.horizontalLayout.addWidget(self.tableView)
        spacerItem = QSpacerItem(10, 20, QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        self.pushButton_3 = QPushButton(self.verticalLayoutWidget_2)
        self.pushButton_3.setIcon(self.style().standardIcon( getattr(QStyle, 'SP_FileDialogInfoView')))
        self.pushButton_3.setMaximumSize(QSize(20, 16777215))
        self.pushButton_3.setLayoutDirection(Qt.RightToLeft)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout_2.addWidget(self.pushButton_3)

        self.pushButton_4 = QPushButton(self.verticalLayoutWidget_2)
        self.pushButton_4.setIcon(self.style().standardIcon(getattr(QStyle, 'SP_FileDialogListView')))
        self.pushButton_4.setMaximumSize(QSize(20, 16777215))
        self.pushButton_4.setLayoutDirection(Qt.RightToLeft)
        self.pushButton_4.setObjectName("pushButton_4")
        self.horizontalLayout_2.addWidget(self.pushButton_4)

        spacerItem1 = QSpacerItem(150, 20, QSizePolicy.Maximum, QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)

        self.pushButton_2 = QPushButton(self.verticalLayoutWidget_2)
        self.pushButton_2.setMaximumSize(QSize(20, 16777215))
        self.pushButton_2.setLayoutDirection(Qt.RightToLeft)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setIcon(self.style().standardIcon(getattr(QStyle, 'SP_FileLinkIcon')))
        self.horizontalLayout_2.addWidget(self.pushButton_2)


        self.pushButton = QPushButton(self.verticalLayoutWidget_2)
        self.pushButton.setMaximumSize(QSize(20, 16777215))
        self.pushButton.setLayoutDirection(Qt.RightToLeft)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setIcon(self.style().standardIcon(getattr(QStyle, 'SP_DialogDiscardButton')))
        self.horizontalLayout_2.addWidget(self.pushButton)

        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.listView = QListView(self.verticalLayoutWidget_2)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listView.sizePolicy().hasHeightForWidth())
        self.listView.setSizePolicy(sizePolicy)
        self.listView.setMaximumSize(QSize(200, 16777215))
        self.listView.setObjectName("listView")
        self.verticalLayout_2.addWidget(self.listView)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.listView_2 = QListView(self.verticalLayoutWidget_2)
        self.listView_2.setMaximumSize(QSize(16777215, 180))
        self.listView_2.setObjectName("listView_2")
        self.verticalLayout_3.addWidget(self.listView_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setGeometry(QRect(0, 0, 858, 21))
        self.menubar.setObjectName("menubar")
        self.menuInicio = QMenu(self.menubar)
        self.menuInicio.setObjectName("menuInicio")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionConfigurar = QAction(MainWindow)
        self.actionConfigurar.setObjectName("actionConfigurar")
        self.actionConfigurar.setIcon(self.style().standardIcon(
            getattr(QStyle, 'SP_TitleBarNormalButton')))
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionAbout.setIcon(self.style().standardIcon(
            getattr(QStyle, 'SP_MessageBoxQuestion')))
        self.actionSalir = QAction(MainWindow)
        self.actionSalir.setObjectName("actionSalir")
        self.actionSalir.setIcon(self.style().standardIcon(getattr(QStyle, 'SP_DialogOkButton')))

        self.actionAdicionar_Fichero = QAction(MainWindow)
        self.actionAdicionar_Fichero.setIcon(self.style().standardIcon(
            getattr(QStyle, 'SP_FileLinkIcon')))
        self.actionAdicionar_Fichero.setObjectName("actionAdicionar_Fichero")

        self.actionGenerar_datos = QAction(MainWindow)
        self.actionGenerar_datos.setIcon(self.style().standardIcon(
            getattr(QStyle, 'SP_DialogApplyButton')))
        self.actionGenerar_datos.setObjectName("actionGenerar_datos")
        self.menuInicio.addAction(self.actionAdicionar_Fichero)
        self.menuInicio.addAction(self.actionGenerar_datos)
        self.menuInicio.addAction(self.actionConfigurar)
        self.menuInicio.addAction(self.actionAbout)
        self.menuInicio.addAction(self.actionSalir)
        self.menubar.addAction(self.menuInicio.menuAction())

        self.centralwidget.setLayout(self.verticalLayout_3)
        MainWindow.showMaximized()
        self.actionAbout.triggered.connect(self.functionAbout)
        self.actionSalir.triggered.connect(self.functionSalir)
        self.actionConfigurar.triggered.connect(self.functionConfigurar)
        self.actionAdicionar_Fichero.triggered.connect(self.functionAdicionar)
        self.pushButton_2.clicked.connect(self.functionAdicionar)
        self.pushButton_3.clicked.connect(self.functionDetails)
        self.pushButton_4.clicked.connect(self.functionCompare)
        self.pushButton.clicked.connect(self.functionEliminar)
        self.actionGenerar_datos.triggered.connect(self.functionGenerarDatos)
        self.listView.clicked.connect(self.onClickedRow)

        self.pushButton.setDisabled(True)
        self.pushButton_3.setDisabled(True)
        self.pushButton_4.setDisabled(True)

        self.tableView.verticalHeader().hide()
        self.tableView.horizontalHeader().hide()
        self.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.listView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.listView_2.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.filesModel = QStringListModel(self)
        self.logModel = QStringListModel(self)
        self.dataModel = QStandardItemModel(0, 0, self)

        # Right-click menu
        self.listView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.listView.customContextMenuRequested.connect(self.myListWidgetContext)

        self.lbl = QLabel(self)
        self.movie = QMovie("C:/SDO/img/loader.gif")
        self.lbl.setMovie(self.movie)
        self.verticalLayout_3.addWidget(self.lbl)
        self.movie.start()
        self.lbl.hide()

        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

    def myListWidgetContext(self, position):
        popMenu = QMenu()
        add_action = QAction(_[lang]['add_files'], self)
        add_action.setIcon(self.style().standardIcon(getattr(QStyle, 'SP_FileLinkIcon')))
        popMenu.addAction(add_action)
        if self.listView.selectionModel() is not None and \
                len(self.listView.selectionModel().selectedRows()) > 0:
            info_action = QAction(_[lang]['details'], self)
            info_action.setIcon(self.style().standardIcon(getattr(QStyle, 'SP_FileDialogInfoView')))
            popMenu.addAction(info_action)
            info_action.triggered.connect(self.functionDetails)

            graphic = QAction(_[lang]['see_graph'], self)
            graphic.setIcon(self.style().standardIcon(getattr(QStyle, 'SP_FileDialogListView')))
            popMenu.addAction(graphic)
            graphic.triggered.connect(self.show_Grafica)

        add_action.triggered.connect(self.functionCargar)
        popMenu.exec_(self.listView.mapToGlobal(position))

    def show_Grafica(self, lbl):
        name = self.listView.selectionModel().selectedRows()[0].data()

        fdata = u.load_data(name)
        col_data, t, round = u.rows_to_columns(fdata['all'])
        data = np.array(col_data[0]).astype(np.float)
        self.lbl.show()
        plt.connect('draw_event', self.handleDialogShown)

        i, col, colors = 1, 0, ["red", "green", "blue", "yellow", "pink", "black", "orange",
                                "purple", "beige", "brown", "gray", "cyan", "magenta"]
        for points in col_data:
            plt.scatter(range(len(points)),
                        points,
                        color=colors[col],
                        label="Columna {0}".format(i))
            col = col + 1 if col < len(colors) - 1 else 0
            i += 1
        plt.gca().axes.yaxis.set_ticklabels([])
        plt.legend()
        plt.show()

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_[lang]['app_name'])
        self.pushButton_3.setToolTip(_[lang]['details'])
        self.pushButton_4.setToolTip(_[lang]['compare'])
        self.menuInicio.setTitle(_[lang]['menu'])
        self.actionConfigurar.setText(_[lang]['configure'])
        self.actionAbout.setText(_[lang]['about'])
        self.actionSalir.setText(_[lang]['exit'])

        self.pushButton.setToolTip(_[lang]['delete_file'])
        self.pushButton_2.setToolTip(_[lang]['add_files'])

        self.actionAdicionar_Fichero.setText(_[lang]['add_files'])
        self.actionGenerar_datos.setText(_[lang]['generate_data'])

    def functionAbout(self):
        msg = QMessageBox()
        msg.setWindowTitle(_[lang]['about'])
        msg.setWindowIcon(QIcon("img/app.png"))
        msg.setIcon(QMessageBox.Information)
        msg.setText(_[lang]['about_text'])
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def functionCompare(self):
        model = self.listView.model()
        self.lbl.show()
        data = self.GTO_data if self.use_gto else None
        for i in range(model.rowCount()):
            fdata = u.load_data(model.index(i).data())
            fixed_data, data_type, round_to = u.rows_to_columns(fdata[fdata['min']])

            AGT_data = u.generateData(fixed_data, data_type, fdata, self.difference_umbral, self.test, self.criteria,data)
            SDO_data = u.generateData(fixed_data, data_type, fdata, self.difference_umbral, self.test, self.criteria)

        self.lbl.hide()
        name = self.listView.selectionModel().selectedRows()[0].data()
        dialog = CompareDialog(name, AGT_data, SDO_data, self.test, self.criteria)
        dialog.start_draw()
        result = dialog.exec_()
        return result == QDialog.Accepted

    def functionGenerarDatos(self):
        model = self.listView.model()
        if model is None:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText(_[lang]['no_file_aviable_text'])
            msg.setWindowTitle(_[lang]['information'])
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            return

        if self.save_folder is None:
            dialog = QFileDialog(self)
            dialog.setFileMode(QFileDialog.DirectoryOnly)
            if dialog.exec_() == QDialog.Accepted:
                self.save_folder = dialog.selectedFiles()[0]
            else:
                return

        self.lbl.show()
        data = self.GTO_data if self.use_gto else None
        for i in range(model.rowCount()):
            fdata = u.load_data(model.index(i).data())
            fixed_data, data_type, round_to = u.rows_to_columns(fdata[fdata['min']])

            AGT_data = u.generateData(fixed_data, data_type, fdata, self.difference_umbral, self.test, self.criteria, data)
            name = '/SDO_AGT_' if self.use_gto else '/SDO_'
            result = u.save_data(
                self.save_folder + name + os.path.basename(model.index(i).data()),
                AGT_data,
                data_type,
                round_to,
                fdata['all'],
                fdata['min_col'],
                self.use_gto)

        text = _[lang]['data_stored_correctly'] if result else _[lang][
            'error_storing_the_data']
        self.lbl.hide()
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(text)
        msg.setWindowTitle(_[lang]['information'])
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def functionSalir(self):
        quit()

    def functionCargar(self):
        self.openFileNameDialog()

    def handleDialogShown(self, x):
        self.lbl.hide()

    def functionDetails(self):
        self.lbl.show()
        name = self.listView.selectionModel().selectedRows()[0].data()
        DetailDialog.getDetail(name, self.lbl, self.test, self.criteria)

    def functionConfigurar(self):
        self.difference_umbral, self.significance_level, self.save_folder, self.column, self.test, self.criteria, ok, self.use_gto = ConfigDialog.getConfig(
            self.significance_level, self.difference_umbral, self.save_folder, self.column,
            self.test, self.criteria, self.use_gto)

    def functionAdicionar(self):
        self.openFileNameDialog()

    def functionEliminar(self):
        name = self.listView.selectionModel().selectedRows()[0].data()
        self.files.remove(name)
        self.filesModel.setStringList(self.files)
        self.listView.setModel(self.filesModel)
        if len(self.files) == 0:
            self.loadData()
            self.pushButton.setDisabled(True)
            self.pushButton_3.setDisabled(True)
            self.pushButton_4.setDisabled(True)
        else:
            self.listView.setCurrentIndex(self.listView.model().index(len(self.files) - 1, 0))
            self.loadData(self.files[len(self.files) - 1])
        self.functionLog(_[lang]['file_deleted'].format(name))

    def functionLog(self, text):
        self.logs.append(text)
        self.logModel.setStringList(self.logs)
        self.listView_2.setModel(self.logModel)

    def onClickedRow(self, index=None):
        self.loadData(self.files[index.row()])
        self.listView.setToolTip(self.files[index.row()])
        self.pushButton.setDisabled(False)
        self.pushButton_3.setDisabled(False)
        self.pushButton_4.setDisabled(False)
        self.functionLog(_[lang]['file_selected'].format(self.files[index.row()]))

    def loadData(self, fileName=None):
        self.dataModel.clear()
        if fileName is not None:
            fdata = u.load_data(fileName, self.column)
            for row in fdata['all']:
                items = []
                for it in row:
                    items.append(QStandardItem(it))
                self.dataModel.appendRow(items)
            self.tableView.setModel(self.dataModel)

    def openFileNameDialog(self):
        txt_msg = ""
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileNames = QFileDialog.getOpenFileNames(self, _[lang]['add_files'], "",
                                                 _[lang]['comma_separated_files'],
                                                 options=options)[0]
        if len(fileNames) > 0:
            for j in fileNames:
                if j not in self.files:
                    self.files.append(j)
                    self.functionLog(_[lang]['files_added'].format(j))
                else:
                    txt_msg += " - {0}\n".format(j)
        else:
            return

        if txt_msg != "":
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText(_[lang]['files_has_been_created'] + txt_msg)
            msg.setWindowTitle(_[lang]['information'])
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()

        self.filesModel.setStringList(self.files)
        self.listView.setModel(self.filesModel)
        self.listView.setCurrentIndex(self.listView.model().index(len(self.files) - 1, 0))
        self.loadData(self.files[len(self.files) - 1])
        self.listView.setToolTip(self.files[-1])
        self.pushButton.setDisabled(False)
        self.pushButton_3.setDisabled(False)
        self.pushButton_4.setDisabled(False)

class ConfigDialog(QDialog):
    def __init__(self, significance_level, threshold, save_f=None, col=-1, test=_[lang]['average'], criteria='aic',
                 parent=None, activeGTO=False):
        super(ConfigDialog, self).__init__(parent)
        self.setWindowTitle(_[lang]['configure'])
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)
        self.setFixedWidth(350)

        layout = QVBoxLayout(self)

        self.umbral_label = QLabel(self)
        self.umbral_label.setObjectName("label")
        self.umbral_label.setText(_[lang]['threshold'])

        self.umbral = QDoubleSpinBox(self)
        self.umbral.setValue(threshold)

        # ==============Prueba a usar============================
        hboxt = QHBoxLayout()
        groupboxt = QGroupBox(_[lang]['test_to_use'], checkable=False)
        groupboxt.setLayout(hboxt)

        self.ad = QRadioButton("Ad")
        if test == 'ad': self.ad.setChecked(True)
        self.ad.setToolTip("Anderson-Darling")
        self.ks = QRadioButton("Ks")
        if test == 'ks': self.ks.setChecked(True)
        self.ks.setToolTip("Kolmogorov-Smirnov")
        self.cvm = QRadioButton("Cvm")
        if test == 'cvm': self.cvm.setChecked(True)
        self.cvm.setToolTip("Cramer-von-Mises")
        self.average = QRadioButton(_[lang]['average'])
        if test == _[lang]['average']: self.average.setChecked(True)
        self.average.setToolTip(_[lang]['average'])

        hboxt.addWidget(self.ad, alignment=Qt.AlignTop)
        hboxt.addWidget(self.ks, alignment=Qt.AlignTop)
        hboxt.addWidget(self.cvm, alignment=Qt.AlignTop)
        hboxt.addWidget(self.average, alignment=Qt.AlignTop)

        # ==============Criterio de selección =======================
        hboxc = QHBoxLayout()
        groupboxc = QGroupBox(_[lang]['selection_criteria'], checkable=False)
        groupboxc.setLayout(hboxc)

        self.aic = QRadioButton("aic")
        if criteria == 'aic': self.aic.setChecked(True)
        self.aic.setToolTip(_[lang]['akaike_criteria'])
        self.bic = QRadioButton("bic")
        if criteria == 'bic': self.bic.setChecked(True)
        self.bic.setToolTip(_[lang]['bayesian_criteria'])

        hboxc.addWidget(self.aic, alignment=Qt.AlignTop)
        hboxc.addWidget(self.bic, alignment=Qt.AlignTop)

        self.sl_label = QLabel(self)
        self.sl_label.setObjectName("label1")
        self.sl_label.setText(_[lang]['significance_level'])

        self.s_level = QDoubleSpinBox(self)
        self.s_level.setValue(significance_level)

        self.column_label = QLabel(self)
        self.column_label.setObjectName("label2")
        self.column_label.setText(_[lang]['column'])

        self.column = QSpinBox(self)
        self.column.setMaximum(10)
        self.column.setMinimum(-1)
        self.column.setValue(col)

        self.savef_label = QLabel(self)
        self.savef_label.setObjectName("label2")
        self.savef_label.setText(_[lang]['store_results_in'])

        self.holayout = QHBoxLayout(self)
        self.savef = QLineEdit(self)
        self.savef.setText(save_f)
        self.savef.setReadOnly(True)

        self.pButton = QPushButton(self)
        self.pButton.setText('...')
        self.pButton.setFixedWidth(20)
        self.pButton.clicked.connect(self.functionSaveFolder)

        self.holayout.addWidget(self.savef)
        self.holayout.addWidget(self.pButton)

        # ==============usar GTO =======================
        self.checkGTO = QCheckBox(_[lang]['use_gto'], self)
        self.checkGTO.setChecked(activeGTO)

        layout.addWidget(groupboxt)
        layout.addWidget(groupboxc)
        layout.addWidget(self.umbral_label)
        layout.addWidget(self.umbral)
        layout.addWidget(self.sl_label)
        layout.addWidget(self.s_level)
        layout.addWidget(self.column_label)
        layout.addWidget(self.column)
        layout.addWidget(self.savef_label)
        layout.addLayout(self.holayout)
        layout.addWidget(self.checkGTO)

        # OK and Cancel buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def getPrueba(self):
        if self.cvm.isChecked(): return 'cvm'
        if self.ks.isChecked(): return 'ks'
        if self.ad.isChecked(): return 'ad'
        return _[lang]['average']

    def getCriterio(self):
        if self.bic.isChecked(): return 'bic'
        return 'aic'

    def functionSaveFolder(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.DirectoryOnly)
        if dialog.exec_() == QDialog.Accepted:
            self.savef.setText(dialog.selectedFiles()[0])
            self.savef.setToolTip(dialog.selectedFiles()[0])

    def um(self):
        return self.umbral.value()

    def sl(self):
        return self.s_level.value()

    def sf(self):
        return self.savef.text()

    def col(self):
        return self.column.value()

    def GTO(self):
        return self.checkGTO.isChecked()

    @staticmethod
    def getConfig(significance_level, umbral, savef, col, prueba, criterio, activeGTO, parent=None):
        dialog = ConfigDialog(significance_level, umbral, savef, col, prueba, criterio, parent, activeGTO)
        result = dialog.exec_()
        um = dialog.um()
        sl = dialog.sl()
        sf = dialog.sf()
        col = dialog.col()
        test = dialog.getPrueba()
        crit = dialog.getCriterio()
        gto = dialog.GTO()
        return um, sl, sf, col, test, crit, result == QDialog.Accepted, gto

class DetailDialog(QDialog):
    dialogShown = pyqtSignal()
    file = None
    difference_umbral = None
    test = None
    criteria = None

    def __init__(self, file=None, lbl=None, parent=None, test='all', criteria='aic',
                 difference_umbral=0.01):
        super(DetailDialog, self).__init__(parent)
        self.file = file
        self.lbl_dialog = lbl
        self.difference_umbral = difference_umbral
        self.test = test
        self.criteria = criteria

        self.setWindowTitle(_[lang]['file_details'].format(os.path.basename(file)))
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)
        self.resize(800, 450)

        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QLabel(self)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.tableView = QTableView(self)
        self.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableView.setMaximumSize(QSize(16777215, 80))
        self.tableView.setObjectName("tableView")
        self.verticalLayout.addWidget(self.tableView)

        self.hlayout = QHBoxLayout(self)

        self.vlayout_details = QVBoxLayout(self)
        self.label_2 = QLabel(self)
        self.label_2.setObjectName("label_2")
        self.vlayout_details.addWidget(self.label_2)

        # self.verticalLayout.addWidget(self.label_2)
        self.listView = QListView(self)
        self.listView.setObjectName("listView")
        self.listView.setFixedWidth(400)
        # self.verticalLayout.addWidget(self.listView)
        self.vlayout_details.addWidget(self.listView)

        self.hlayout.addLayout(self.vlayout_details)

        self.vlayout_plot = QVBoxLayout(self)
        label_3 = QLabel(self)
        label_3.setObjectName("label_3")
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.vlayout_plot.addWidget(self.toolbar)
        self.vlayout_plot.addWidget(self.canvas)

        self.hlayout.addLayout(self.vlayout_plot)
        self.verticalLayout.addLayout(self.hlayout)

        self.tableView.verticalHeader().hide()

        self.label.setText(_[lang]['column_distribution_by_column'])
        self.label_2.setText(_[lang]['details'])

        self.dialogShown.connect(self.handleDialogShown)

        self.tableView.clicked.connect(self.on_click)

        # OK and Cancel buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok,
            Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        self.verticalLayout.addWidget(buttons)
        self.setLayout(self.verticalLayout)

    def start_draw(self):
        fdata = u.load_data(self.file)
        col_data, t, round = u.rows_to_columns(fdata['all'])

        i, col, colors = 1, 0, ["red", "green", "blue", "yellow", "pink", "black", "orange",
                                "purple", "beige", "brown", "gray", "cyan", "magenta"]

        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.clear()

        for points in col_data:
            ax.scatter(range(len(points)),
                       points,
                       color=colors[col],
                       label="Columna {0}".format(i + 1))
            col = col + 1 if col < len(colors) - 1 else 0
            i += 1

        self.figure.gca().axes.yaxis.set_ticklabels([])
        self.figure.legend().remove()
        self.canvas.draw()

    def on_click(self, item):
        fdata = u.load_data(self.file)

        col_data, t, round = u.rows_to_columns(fdata[fdata['min']])
        data = np.array(col_data[0]).astype(np.float)

        i, col, colors = 1, 0, ["red", "green", "blue", "yellow", "pink", "black", "orange",
                                "purple", "beige", "brown", "gray", "cyan", "magenta"]

        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.clear()
        col = item.column() if item.column() < len(colors) - 1 else item.column() - len(colors)
        ax.scatter(range(len(col_data[item.column()])),
                   col_data[item.column()],
                   color=colors[col],
                   label="Columna {0}".format(item.column() + 1))
        self.figure.gca().axes.yaxis.set_ticklabels([])
        self.figure.legend(loc='upper left')
        self.canvas.draw()

    def handleDialogShown(self):
        self.process(self.file)
        self.lbl_dialog.hide()

    def showEvent(self, event):
        super(QDialog, self).showEvent(event)
        self.dialogShown.emit()

    def process(self, filename):
        fdata = u.load_data(filename)
        fixed_data, data_type, round = u.rows_to_columns(fdata[fdata['min']])
        selected_distribution = u.getDistributionInfo(fixed_data, data_type, self.difference_umbral,
                                                      self.test, self.criteria)

        distributionModel = QStandardItemModel(0, 0, self)
        listModel = QStringListModel(self)

        items = [QStandardItem(e['dist'][0]) for e in selected_distribution]
        distributionModel.appendRow(items)
        self.tableView.setModel(distributionModel)
        self.listView.setModel(listModel)

        listed = [
            _[lang]['file'].format(filename),
            _[lang]['total_registry'].format(len(fdata['a']) + len(fdata['b'])),
            _[lang]['total_columns'].format(len(fdata['a'][0])),
            _[lang]['test'].format(self.test),
            _[lang]['selection_criteria1'].format(self.criteria),
            _[lang]['majority_class_contains'].format(len(fdata[fdata['max']])),
            _[lang]['minority_class_contains'].format(len(fdata[fdata['min']])),
            '---------------' + _[lang]['details'] + '---------------',
        ]
        i = 1
        for v in selected_distribution:
            if "ad" in v:
                text = '{0} {1}, Anderson-Darling: {2}, Kolmogorov-Smirnov: {3}, Cramer-von-Mises: {4}'.format(
                    _[lang]['column'], i, np.round(v['ad'], 4), np.round(v['ks'], 4), np.round(v['cvm'], 4))
            else:
                text = '{0} {1}, {2}'.format(_[lang]['column'], i, v['dist'][0])
            listed.append(text)
            i += 1

        listModel.setStringList(listed)

    @staticmethod
    def getDetail(file, lbl, test, criteria, parent=None):
        dialog = DetailDialog(file, lbl, parent, test, criteria)
        dialog.start_draw()
        result = dialog.exec_()
        return result == QDialog.Accepted

class CompareDialog(QDialog):
    dialogShown = pyqtSignal()
    SDO_data = []
    AGT_data = []
    file = None
    difference_umbral = None
    test = None
    criteria = None

    def __init__(self, file, _AGT_data, _SDO_data, _test='all', _criteria='aic', _difference_umbral=0.01, parent=None):
        super(CompareDialog, self).__init__(parent)
        self.SDO_data = _SDO_data
        self.AGT_data = _AGT_data
        self.file = file
        self.difference_umbral = _difference_umbral
        self.criteria = _criteria
        self.test = _test

        self.setWindowTitle(_[lang]['compare'] + ' ' + os.path.basename(file))
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)
        self.resize(800, 450)

        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QLabel(self)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.tableView = QTableView(self)
        self.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableView.setMaximumSize(QSize(16777215, 80))
        self.tableView.setObjectName("tableView")
        self.verticalLayout.addWidget(self.tableView)

        self.hlayout = QHBoxLayout(self)
        # AGT table
        self.vlayout_plot_AGT = QVBoxLayout(self)
        self.figure_AGT = Figure()
        self.canvas_AGT = FigureCanvas(self.figure_AGT)
        self.toolbar_AGT = NavigationToolbar(self.canvas_AGT, self)
        self.vlayout_plot_AGT.addWidget(self.toolbar_AGT)
        self.vlayout_plot_AGT.addWidget(self.canvas_AGT)
        self.hlayout.addLayout(self.vlayout_plot_AGT)

        # SDO table
        self.vlayout_plot_SDO = QVBoxLayout(self)
        self.figure_SDO = Figure()
        self.canvas_SDO = FigureCanvas(self.figure_SDO)
        self.toolbar_SDO = NavigationToolbar(self.canvas_SDO, self)
        self.vlayout_plot_SDO.addWidget(self.toolbar_SDO)
        self.vlayout_plot_SDO.addWidget(self.canvas_SDO)

        self.hlayout.addLayout(self.vlayout_plot_SDO)
        self.verticalLayout.addLayout(self.hlayout)

        self.tableView.verticalHeader().hide()

        self.label.setText(_[lang]['column_distribution_by_column'])

        self.dialogShown.connect(self.handleDialogShown)

        self.tableView.clicked.connect(self.on_click)

        # OK and Cancel buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok,
            Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        self.verticalLayout.addWidget(buttons)
        self.setLayout(self.verticalLayout)

    def start_draw(self):
        # fdata = u.load_data(self.file)
        # col_data, t, round = u.rows_to_columns(fdata['all'])

        i, col, colors = 1, 0, ["red", "green", "blue", "yellow", "pink", "black", "orange",
                                "purple", "beige", "brown", "gray", "cyan", "magenta"]
        # Llenado de AGT
        self.figure_AGT.clear()
        ax = self.figure_AGT.add_subplot(111)
        ax.clear()
        for points in self.AGT_data:
            ax.scatter(range(len(points)),
                       points,
                       color=colors[col],
                       label="Columna {0}".format(i + 1))
            col = col + 1 if col < len(colors) - 1 else 0
            i += 1

        self.figure_AGT.gca().axes.yaxis.set_ticklabels([])
        self.figure_AGT.legend().remove()
        self.canvas_AGT.draw()

        # Llenado de SDO
        col = 0
        self.figure_SDO.clear()
        bx = self.figure_SDO.add_subplot(111)
        bx.clear()

        for points in self.SDO_data:
            bx.scatter(range(len(points)),
                       points,
                       color=colors[col],
                       label="Columna {0}".format(i + 1))
            col = col + 1 if col < len(colors) - 1 else 0
            i += 1

        self.figure_SDO.gca().axes.yaxis.set_ticklabels([])
        self.figure_SDO.legend().remove()
        self.canvas_SDO.draw()

    def on_click(self, item):
        #fdata = u.load_data(self.file)

        #col_data, t, round = u.rows_to_columns(fdata[fdata['min']])
        #data = np.array(col_data[0]).astype(np.float)

        i, col, colors = 1, 0, ["red", "green", "blue", "yellow", "pink", "black", "orange",
                                "purple", "beige", "brown", "gray", "cyan", "magenta"]
        col = item.column() if item.column() < len(colors) - 1 else item.column() - len(colors)

        # Llenado de AGT
        self.figure_AGT.clear()
        ax = self.figure_AGT.add_subplot(111)
        ax.clear()
        ax.scatter(range(len(self.AGT_data[item.column()])),
                   self.AGT_data[item.column()],
                   color=colors[col],
                   label="SDO+AGT")

        self.figure_AGT.gca().axes.yaxis.set_ticklabels([])
        self.figure_AGT.legend(loc='upper left')
        self.canvas_AGT.draw()

        # Llenado de SDO
        self.figure_SDO.clear()
        bx = self.figure_SDO.add_subplot(111)
        bx.clear()

        bx.scatter(range(len(self.SDO_data[item.column()])),
                   self.SDO_data[item.column()],
                   color=colors[col],
                   label="SDO")

        self.figure_SDO.gca().axes.yaxis.set_ticklabels([])
        self.figure_SDO.legend(loc='upper left')
        self.canvas_SDO.draw()



        # self.figure.clear()
        # ax = self.figure.add_subplot(111)
        # ax.clear()
        # col = item.column() if item.column() < len(colors) - 1 else item.column() - len(colors)
        # ax.scatter(range(len(col_data[item.column()])),
        #            col_data[item.column()],
        #            color=colors[col],
        #            label="Columna {0}".format(item.column() + 1))
        # self.figure_SDO.gca().axes.yaxis.set_ticklabels([])
        # self.figure_SDO.legend(loc='upper left')
        # self.canvas_SDO.draw()

    def handleDialogShown(self):
        self.process(self.file)
        # self.lbl_dialog.hide()

    def showEvent(self, event):
        super(QDialog, self).showEvent(event)
        self.dialogShown.emit()

    def process(self, filename):
        fdata = u.load_data(filename)
        fixed_data, data_type, round = u.rows_to_columns(fdata[fdata['min']])
        selected_distribution = u.getDistributionInfo(fixed_data, data_type, self.difference_umbral,
                                                      self.test, self.criteria)

        distributionModel = QStandardItemModel(0, 0, self)

        items = [QStandardItem(e['dist'][0]) for e in selected_distribution]
        distributionModel.appendRow(items)
        self.tableView.setModel(distributionModel)

    @staticmethod
    def getDetail(file, lbl, test, criteria, parent=None):
        dialog = DetailDialog(file, lbl, parent, test, criteria)
        dialog.start_draw()
        result = dialog.exec_()
        return result == QDialog.Accepted

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
