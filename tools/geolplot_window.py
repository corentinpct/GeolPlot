from PyQt5.QtWidgets import QHBoxLayout,QVBoxLayout,QDesktopWidget,QLabel,QSizePolicy,QSpacerItem,QScrollArea,QWidget,QGroupBox
from PyQt5.QtCore import Qt

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
    if isinstance(widgets,QVBoxLayout):
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
       
def setBulletPoints(label,points):
    text = '<ul>'
    for point in points:
        text += f'<li>{point}</li>'
    text += '<ul>'
    label.setText(text)
    
def setHorizontal(widgets,layout):
    frame = QHBoxLayout()
    for widget in widgets:
        frame.addWidget(widget)
    layout.addLayout(frame)        
    
    
            
    
    