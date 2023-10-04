from PyQt5.QtWidgets import QApplication,QMainWindow,QDialog,QVBoxLayout,QHBoxLayout,QMenu,QWidget
from PyQt5.QtWidgets import QAction,QComboBox,QCheckBox,QPushButton,QLabel,QGroupBox
from PyQt5.QtWidgets import QLineEdit,QFrame
from PyQt5.QtWidgets import QDesktopWidget,QSizePolicy,QSpacerItem,QScrollArea
from PyQt5.QtCore import pyqtSignal,Qt
import sys

from scripts import geolplot_func as gp

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('GeolPlot.py')
        self.resize(1200,550)
        Center(parent=self)
        self.files = {}
        self.df = {}
        self.locality = {}
        self.unit = {}
        self.planetype = {}  
        self.setMenuBar() 
        self.setMainLayout()
        
    def setMenuBar(self):
        menu = self.menuBar()
        self.setFileTab(menu.addMenu('File'))
        self.setDataTab(menu.addMenu('Data'))
        
    def setFileTab(self,menu):
        action = QAction('Import',self)
        actions = [QAction('Import CSV file(s) (.csv)',self),QAction('Import Excel file(s) (.xlsx)',self)]
        child = QMenu('Import',self)
        menu.addAction(action)
        action.setMenu(child)
        child.addActions(actions)
        actions[0].triggered.connect(lambda: self._import(dtype='csv',insert=False))
        actions[1].triggered.connect(lambda: self._import(dtype='xlsx',insert=False))

        action = QAction('Add data on current data',self)
        actions = [QAction('From CSV file(s) (.csv)',self),QAction('From Excel file(s) (.xlsx)',self)]
        child = QMenu('Add data on current data',self)
        menu.addAction(action)
        action.setMenu(child)
        child.addActions(actions)
        actions[0].triggered.connect(lambda: self._import(dtype='csv',insert=True))
        actions[1].triggered.connect(lambda: self._import(dtype='xlsx',insert=True))
        
        action = QAction('Save current data as',self)
        actions = [QAction('CSV file (.csv)',self),QAction('Excel file (.xlsx)',self)]
        child = QMenu('Save current data as',self)
        menu.addAction(action)
        action.setMenu(child)
        child.addActions(actions)
        actions[0].triggered.connect(lambda: self._save(csv=True))
        actions[1].triggered.connect(lambda: self._save(xlsx=True))
        
    def setDataTab(self,menu):
        action,actions = QAction('Set name(s) for',self),[QAction('Locality',self),QAction('Unit',self),QAction('Plane type',self)]
        child = QMenu('Set name(s) for',self)
        menu.addAction(action)
        action.setMenu(child)
        child.addActions(actions)
        actions[0].triggered.connect(lambda: self._rename(self.locality,title='Locality'))
        actions[1].triggered.connect(lambda: self._rename(self.unit,title='Unit'))
        actions[2].triggered.connect(lambda: self._rename(self.planetype,title='Plane type'))

    def setMainLayout(self):
        widget = QWidget(self)
        self.setCentralWidget(widget)
        if not self.files :
            QVBoxLayout(widget).addWidget(QLabel('Import CSV or Excel file(s) to start GeolPlot.py'),alignment=Qt.AlignCenter)
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
        group.setFixedHeight(150)
        self._files = QVBoxLayout()
        group.setLayout(self._files)
        layout.addWidget(group)
        group = QGroupBox('Parameters from imported CSV file(s)')
        frame= QVBoxLayout()
        group.setLayout(frame)
        child = QHBoxLayout()
        for label in ['Locality','Unit','Plane type']:
            child.addWidget(QLabel(label))
        frame.addLayout(child)
        child = QHBoxLayout()
        self._locality = QVBoxLayout()
        self._unit = QVBoxLayout()
        self._planetype = QVBoxLayout()
        for parameter in [self._locality,self._unit,self._planetype]:
            addScrollArea(parameter,child,parent=self)
        frame.addLayout(child)
        layout.addWidget(group)
        
    def setRightLayout(self,layout):
        group = QGroupBox('Output Directory')
        group.setFixedHeight(70)
        self.layout = QHBoxLayout()
        group.setLayout(self.layout)
        button,self.text = QPushButton('Select'),QLineEdit()
        button.clicked.connect(self._directory)
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
        def _update(state):
            self.files[self.sender().text()] = True if state == Qt.Checked else False
            self.__update()
        while self._files.count():
            file = self._files.takeAt(0)
            if file.widget():
                file.widget().deleteLater()
        for file,state in self.files.items():
            checkbox = QCheckBox(file,self)
            checkbox.setChecked(state)
            checkbox.stateChanged.connect(_update)
            self._files.addWidget(checkbox)
        self._files.update()
        
    def __update(self):
        def _filter():
            def _in(selected,states):
                for state in states.keys():
                    states[state][1] = False if not state in selected else True
            files = {file: self.df[file] for file in self.files if self.files[file]}
            if files :
                locality, unit, planetype = gp.getallparameters(files)
                _in(locality,self.locality)
                _in(unit,self.unit)
                _in(planetype,self.planetype)
            else:
                for states in [self.locality,self.unit,self.planetype]:
                    for boolean in states.values():
                        boolean[1] = False
        def _delete(layout):
            while layout.count():
                child = layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()
        def _update(state,states,checkbox):
            states[checkbox.text()][0] = True if state == Qt.Checked else False
        def _get(states,layout):
            for name in states.keys():
                checkbox = QCheckBox(name,self)
                checkbox.setChecked(states[name][0])
                if not states[name][1]:
                    checkbox.setCheckable(states[name][1])
                    checkbox.setStyleSheet('color:gray;')
                else :
                    checkbox.setStyleSheet('color:black;')
                checkbox.stateChanged.connect(lambda state,checkbox=checkbox:_update(state,states,checkbox))
                layout.addWidget(checkbox)
            layout.update()
        _filter()    
        _delete(self._locality)
        _get(self.locality,self._locality)
        _delete(self._unit)
        _get(self.unit,self._unit)
        _delete(self._planetype)
        _get(self.planetype,self._planetype)

    def _import(self,dtype,insert=False):
        if dtype == 'csv':
            try:
                self.files,self.df = gp.selectcsv(self.files,insert=insert,parent=self)
            except TypeError:
                pass
        elif dtype == 'xlsx':
            try:
                self.files,self.df = gp.selectxlsx(self.files,insert=insert,parent=self)
            except TypeError:
                pass
        self.locality,self.unit,self.planetype = gp.getallparameters(self.df)
        self.setMainLayout()
        self._update()
        self.__update()
        
    def _save(self,csv=False,xlsx=False):
        files = {file: self.df[file] for file in self.files if self.files[file]}
        if files :
            gp.savedf(files,csv=csv,xlsx=xlsx)
            
    def _rename(self,names,title):
        dialog = SetNamesWindow(names,title,parent=self)
        dialog.signal.connect(self._receive)
        dialog.exec_()
    
    def _receive(self,signal):
        if all(locality in self.locality for locality in list(signal.values())[0]):
            self.locality,self.df = gp.rename(signal,self.locality,self.df,column='localityname')
        elif all(unit in self.unit for unit in list(signal.values())[0]):
            self.unit,self.df = gp.rename(signal,self.unit,self.df,column='unitid')
        elif all(planetype in self.planetype for planetype in list(signal.values())[0]):
            self.planetype,self.df = gp.rename(signal,self.planetype,self.df,column='planetype')
        self.__update()  
    
    def _directory(self):
        self.directory = gp.selectdir()
        self.text.setText(self.directory)
        self.layout.update()

    def _emit(self):
        self._update()
        self.__update()
        if gp.controlparameters(self.locality,self.unit,self.planetype,self.files,parent=self):
            if gp.controlsettings(self.settings,self.text.text(),parent=self):
                if gp.messagebox():
                    files = [file for file in self.files if self.files[file]]
                    locality = [locality for locality in self.locality if self.locality[locality][0] and self.locality[locality][1]]
                    unit = [unit for unit in self.unit if self.unit[unit][0] and self.unit[unit][1]]
                    planetype = [planetype for planetype in self.planetype if self.planetype[planetype][0] and self.planetype[planetype][1]]
                    gp.savestereonet(locality,unit,planetype,files,self.df,gp.getsettings(self.settings),self.directory)
                    
                        
class SetNamesWindow(QDialog):
    signal = pyqtSignal(dict)
    
    def __init__(self,names,title,parent=None):
        super().__init__(parent)
        self.setWindowTitle(f'Set name(s) for {title}')
        self.resize(300,350)
        Center(parent=self)
        self.names = names
        self.setMainLayout()
        
    def setMainLayout(self):
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel('Enter a new name for the selected name(s) :'))
        line = QLineEdit()
        layout.addWidget(line)
        layout.addWidget(QLabel('Select the name(s) to be modified :'))
        self.frame = QVBoxLayout()
        for name in self.names.keys() :
            self.frame.addWidget(QCheckBox(name))
        addScrollArea(self.frame, layout,parent=self)
        button = QPushButton('Apply modifications')
        button.setFixedSize(120,25)
        MoveDown(button,layout,spacing=5)
        button.clicked.connect(lambda: self._emit(line.text().replace(' ','')))
        
    def _emit(self,name):
        signal = {name:[]}
        for i in range(self.frame.count()):
            item = self.frame.itemAt(i).widget()
            if item.isChecked():
                signal[name].append(item.text())
        self.signal.emit(signal)
        self.close()
        
def launch():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
    
def Center(parent=None):
    x = (QDesktopWidget().availableGeometry().width() - parent.frameGeometry().width())//2
    y = (QDesktopWidget().availableGeometry().height()- parent.frameGeometry().height())//2
    parent.move(x,y)
    
def MoveUp(layout):
    layout.addStretch(1)
    for i in range(layout.count()):
        if layout.itemAt(i).widget() and isinstance(layout.itemAt(i).widget(), QLabel):
            layout.itemAt(i).widget().setMinimumHeight(30)
            
def MoveDown(widgets,layout,spacing):
    layout.addSpacing(spacing)
    frame = QHBoxLayout()
    frame.addItem(QSpacerItem(0,0,QSizePolicy.Expanding,QSizePolicy.Fixed))
    if not isinstance(widgets,list):
        frame.addWidget(widgets)
    else:
        for widget in widgets:
            frame.addWidget(widget)
    layout.addLayout(frame)
    
def addScrollArea(widgets,layout,parent=None,height=None,width=None):
    frame = QScrollArea(parent)
    if isinstance(widgets,QVBoxLayout) or isinstance(widgets,QHBoxLayout):
        widget = QWidget(frame)
        widget.setLayout(widgets)
        frame.setWidget(widget)
    else:
        frame.setWidget(widgets)
    if height is not None :
        frame.setMaximumHeight(height)
    if width is not None:
        frame.setMaximumWidth(width)
    frame.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
    frame.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    frame.setWidgetResizable(True)
    layout.addWidget(frame)
       
def setHorizontal(widgets,layout):
    frame = QHBoxLayout()
    for widget in widgets:
        frame.addWidget(widget)
    layout.addLayout(frame)   
    