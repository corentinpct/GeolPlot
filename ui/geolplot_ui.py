from PyQt5.QtWidgets import QApplication,QMainWindow,QDialog,QMessageBox,QVBoxLayout,QHBoxLayout,QMenu,QWidget
from PyQt5.QtWidgets import QAction,QComboBox,QCheckBox,QPushButton,QLabel,QGroupBox
from PyQt5.QtWidgets import QLineEdit,QFrame
from PyQt5.QtCore import pyqtSignal,Qt
import sys

import ui.geolplot_func as gp
from tools.geolplot_window import Center,MoveDown,MoveUp
from tools.geolplot_window import addScrollArea,setBulletPoints,setHorizontal
from tools.geolplot_dir import make_directories

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('GeolPlot.py')
        self.resize(900,450)
        Center(parent=self)
        self.files = []
        self.imported = False
        self.state = {}
        self.parameters = {}
        self.updates = {}
        self.setMenuBar()
        self.setMainLayout()
        
    def setMenuBar(self):
        menu = self.menuBar()
        self.setFileTab(menu.addMenu('File'))
        self.setDataTab(menu.addMenu('Data'))
        
    def setFileTab(self,menu):
        action,actions = QAction('Import',self),[QAction('Import CSV file(s)',self)]
        # actions = [QAction('Import CSV file(s)',self),QAction('Import FieldMOVE Clino project(s)',self)]
        temp = QMenu('Import',self)
        menu.addAction(action)
        action.setMenu(temp)
        temp.addActions(actions)
        actions[0].triggered.connect(lambda: self._connect('import'))
        #actions[1].triggered.connect()
        
        action,actions = QAction('Add data on current data',self),[QAction('From CSV file(s)',self)]
        #actions = [QAction('From CSV file(s)',self),QAction('From FieldMOVE Clino project(s)',self)]
        temp = QMenu('Add data on current data',self)
        menu.addAction(action)
        action.setMenu(temp)
        temp.addActions(actions)
        actions[0].triggered.connect(lambda: self._connect('import',options='add'))
        #actions[1].triggered.connect()
        
        action,actions = QAction('Save current data as',self),[QAction('CSV file (.csv)',self),QAction('Excel file (.xlsx)',self)]
        temp = QMenu('Save current data as',self)
        menu.addAction(action)
        action.setMenu(temp)
        temp.addActions(actions)
        actions[0].triggered.connect(lambda: self._connect('save',options='csv'))
        actions[1].triggered.connect(lambda: self._connect('save',options='xlsx'))
        
    def setDataTab(self,menu):
        action,actions = QAction('Set name(s) for',self),[QAction('Locality',self),QAction('Unit',self),QAction('Plane type',self)]
        temp = QMenu('Set name(s) for',self)
        menu.addAction(action)
        action.setMenu(temp)
        temp.addActions(actions)
        actions[0].triggered.connect(lambda: self._connect('rename',options='Locality'))
        actions[1].triggered.connect(lambda: self._connect('rename',options='Unit'))
        actions[2].triggered.connect(lambda: self._connect('rename',options='Plane type'))

    def setMainLayout(self):
        widget = QWidget(self)
        self.setCentralWidget(widget)
        if not self.imported :
            QVBoxLayout(widget).addWidget(QLabel('Import CSV file(s) to start GeolPlot.py'),alignment=Qt.AlignCenter)
        else:
            main = QHBoxLayout(widget)
            layout = QVBoxLayout()
            self.setLeftLayout(layout)
            main.addLayout(layout)
            line = QFrame()
            line.setFrameShape(QFrame.VLine)
            line.setFrameShadow(QFrame.Sunken)
            main.addWidget(line)
            layout = QVBoxLayout()
            self.setRightLayout(layout)           
            main.addLayout(layout)
    
    def setLeftLayout(self,layout):
        group = QGroupBox('Current CSV file(s) imported in GeolPlot.py')
        group.setFixedHeight(100)
        frame = QVBoxLayout()
        group.setLayout(frame)
        label = QLabel()
        setBulletPoints(label,self.files)
        addScrollArea(label,frame,parent=self,height=100)
        layout.addWidget(group)
        group = QGroupBox('Parameters from imported CSV file(s)')
        group.setFixedHeight(250)
        frame = QVBoxLayout()
        group.setLayout(frame)
        self.combobox = QComboBox(self)
        self.combobox.addItems(['Locality','Unit','Plane type'])
        self.combobox.currentIndexChanged.connect(self._update)
        self.checkboxes = QVBoxLayout()
        frame.addWidget(self.combobox)
        addScrollArea(self.checkboxes,frame,parent=self)
        layout.addWidget(group)
        
    def setRightLayout(self,layout):
        group = QGroupBox('Output Directory')
        group.setFixedHeight(70)
        self.layout = QHBoxLayout()
        group.setLayout(self.layout)
        button,self.text = QPushButton('Select'),QLineEdit()
        button.clicked.connect(lambda: self._connect('dir'))
        self.layout.addWidget(button)
        self.layout.addWidget(self.text)
        layout.addWidget(group)
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        group = QGroupBox('Stereonet Settings')
        self.settings = QVBoxLayout()
        group.setLayout(self.settings)
        self.settings.addWidget(QLabel('Orientation :'))
        setHorizontal([QCheckBox('Strike/Dip',self),QCheckBox('DipAzimuth/Dip',self)],self.settings)
        self.settings.addWidget(QLabel('Representation :'))
        setHorizontal([QCheckBox('Planes',self),QCheckBox('Poles',self)], self.settings)
        self.settings.addSpacing(5)
        self.settings.addWidget(QLabel('(If both options are checked then an image will be generated per option)'))
        self.settings.addSpacing(5)
        self.settings.addWidget(line)
        self.settings.addWidget(QLabel('Density contouring (only for poles representation) :'))
        combobox = QComboBox(self)
        combobox.addItems(['Kamb','Kamb & Linear Smoothing','Kamb & Exponential Smoothing','Schmidt'])
        setHorizontal([QCheckBox('Plot Density Contouring',self),combobox], self.settings)
        self.settings.addWidget(QCheckBox('Plot both Poles and Density Contouring',self))
        layout.addWidget(group)
        MoveUp(layout)
        button = QPushButton('Generate')
        button.clicked.connect(self._emit)
        MoveDown(button, layout, spacing=10)
    
    def _update(self):
        def get_state(state):
            parameter = self.combobox.currentText()
            if parameter not in self.state:
                self.state[parameter] = {}
            self.state[parameter][self.sender().text()] = True if state == Qt.Checked else False
        state = self.state[self.combobox.currentText()] if self.combobox.currentText() in self.state else {}
        while self.checkboxes.count():
            child = self.checkboxes.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        for name in self.parameters[self.combobox.currentText()]:
            checkbox = QCheckBox(str(name),self)
            checkbox.setChecked(state.get(name,False))
            checkbox.stateChanged.connect(get_state)
            self.checkboxes.addWidget(checkbox)
        self.checkboxes.update()
    
    def _connect(self,task,options=None):
        if task == 'import':
            try:
                self.files,self.parameters,self.imported = gp.select_csv(self.files,parent=self) if options is None else gp.select_csv(self.files,add=True,parent=self)
                self.setMainLayout()
                self._update()
            except TypeError:
                pass
        elif task == 'save':
            informations = {'files':self.files,'updates':self.updates}
            gp.save_csv_as(informations,xlsx=True,parent=self) if options == 'xlsx' else gp.save_csv_as(informations,csv=True,parent=self)
        elif task == 'dir':
            self.directory = gp.select_dir()
            self.text.setText(self.directory)
            self.layout.update()
        elif task == 'rename':
            dialog = SetNamesWindow(options,self.parameters,parent=self)
            dialog.signal.connect(self._receive)
            dialog.exec_()
        
    def _receive(self,signal):
        self.parameters,self.updates = gp.rename_parameters(self.parameters, self.updates, signal)
        self._update()

    def _emit(self):
        self._update()
        if gp.show_messagebox():
            if gp.control_parameters_state(self.state,parent=self) and gp.control_settings_state(gp.get_state(self.settings),parent=self):
                try:
                    make_directories(self.directory, gp.filter_parameters_state(self.state))
                    gp.save_stereonets(self.files, self.state, self.updates,gp.get_state(self.settings),self.directory)
                except AttributeError:
                    QMessageBox.critical(self,'Error : No directory selected','No directory has been selected. Please select the output directory.')
        else:
            pass
        
class SetNamesWindow(QDialog):
    signal = pyqtSignal(dict)
    
    def __init__(self,parameter,parameters,parent=None):
        super().__init__(parent)
        self.setWindowTitle(f'Set name(s) for {parameter}')
        self.resize(300,350)
        Center(parent=self)
        self.parameters = parameters
        self.parameter = parameter
        self.setMainLayout()
        
    def setMainLayout(self):
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel('Enter a new name for the selected name(s) :'))
        line = QLineEdit()
        layout.addWidget(line)
        layout.addWidget(QLabel('Select the name(s) to be modified :'))
        checkboxes = QVBoxLayout()
        for parameter in self.parameters[self.parameter]:
            checkboxes.addWidget(QCheckBox(parameter))
        addScrollArea(checkboxes, layout,parent=self)
        button = QPushButton('Apply modifications')
        button.clicked.connect(lambda: self._emit(checkboxes,line.text().replace(' ','')))
        button.setFixedSize(120,25)
        MoveDown(button,layout,spacing=5)
    
    def _emit(self,checkboxes,name):
        signal = {'name':name,'parameter':self.parameter,'state':gp.get_state(checkboxes)}
        self.signal.emit(signal)
        self.close()
        
def launch():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_()) 
       