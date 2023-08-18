from PyQt5.QtWidgets import QFileDialog,QMessageBox,QHBoxLayout,QVBoxLayout,QCheckBox,QComboBox

from tools import geolplot_csv as gp_csv
from tools import geolplot_dir as gp_dir
from tools import geolplot_stereonet as gp_stereo

def select_csv(files,add=False,parent=None):
    dialog = QFileDialog()
    dialog.setWindowTitle('Import FieldMOVE Clino CSV file(s)')
    dialog.setFileMode(QFileDialog.ExistingFiles)
    dialog.setNameFilter('CSV Files (*.csv)')
    if dialog.exec() == QFileDialog.Accepted:
        if not add :
            files = dialog.selectedFiles()
        else:
            files.extend(dialog.selectedFiles())
        parameters = gp_csv.get_parameters(gp_csv.get_df(files))
        if parameters is not None:
            imported = True
            return files,parameters,imported
        else:
            QMessageBox.critical(parent,'Error : Imported file(s) cannot be read','Data in imported file(s) do not represent geological planes. Please select one or more CSV files from a FieldMOVE Clino project containing plane data.')

def select_dir():
    dialog = QFileDialog()
    dialog.setWindowTitle('Select the directory in which the stereographic representations will be generated.')
    dialog.setFileMode(QFileDialog.Directory)
    if dialog.exec() == QFileDialog.Accepted:
        return dialog.selectedFiles()[0]
           
def save_csv_as(informations,csv=False,xlsx=False,parent=None):
    if csv :
        file,_ = QFileDialog.getSaveFileName(parent, 'Save as CSV file (.csv)', '', 'CSV Files (*.csv)')
    elif xlsx :
        file,_ = QFileDialog.getSaveFileName(parent, 'Save as Excel file (.xlsx)', '', 'Excel Files (*.xlsx)')
    if file:
        try:
            gp_csv.save_df_as(informations,file,csv=csv,xlsx=xlsx)
            gp_dir.open_directory(file)
        except Exception as exception:
            QMessageBox.critical(parent,'Error : Dataframe cannot be saved',f'Error while saving the dataframe : {exception}')
            
def rename_parameters(parameters,updates,signal):
    updates = {'Locality':{},'Unit':{},'Plane type':{}} if len(updates) == 0 else updates
    updates[signal['parameter']][signal['name']] = []
    for parameter, state in signal['state'].items():
        if parameter in parameters[signal['parameter']] and state:
            parameters[signal['parameter']].remove(parameter)
            updates[signal['parameter']][signal['name']].append(parameter)
    if not signal['name'] in parameters[signal['parameter']]:
        parameters[signal['parameter']].append(signal['name'])
    return parameters,updates

def get_state(layout):
    state = {}  
    for i in range(layout.count()):
        item = layout.itemAt(i).widget()
        if isinstance(item, QCheckBox):
            state[item.text()] = item.isChecked()
        elif item is None:
            item = layout.itemAt(i).layout()
            if item is not None and isinstance(item,(QHBoxLayout,QVBoxLayout)):
                for j in range(item.count()):
                    widget = item.itemAt(j).widget()
                    if isinstance(widget,QCheckBox):
                        state[widget.text()] = widget.isChecked()
                    elif isinstance(widget,QComboBox):
                        state['Plot Density Contouring'] = [state['Plot Density Contouring'],widget.currentText()]
    return state

def filter_parameters_state(state):
    for parameter,parameters in state.items():
        state[parameter] = {key: checked for key,checked in parameters.items() if checked}
    return state

def control_parameters_state(state,parent=None):
    requirements = {}
    for parameter,parameters in state.items():
        requirements[parameter] = True
        if not any(parameters.values()) :
            requirements[parameter] = any(parameters.values())
    if len(requirements) != len(['Locality','Unit','Plane type']) or not all(requirements.values()):
        parameters = ['Locality','Unit','Plane type']
        for parameter in requirements:
            if parameter in parameters:
                parameters.remove(parameter)
        if not len(parameters) != 0:
            parameters = [parameter for parameter,status in requirements.items() if status is False]
        parameters = parameters = ', '.join(parameters)
        QMessageBox.critical(parent,f'Error : No parameter selected for {parameters}',f'No parameter have been selected for {parameters}, please select at least one parameter for {parameters}.')
    else:
        return True
           
def control_settings_state(state,parent=None):
    requirements = []
    for setting,checked in state.items():
        if setting == 'Strike/Dip' or setting == 'DipAzimuth/Dip':
            requirements.append(state[setting])
    if not all(requirements) and not any(requirements):
        QMessageBox.critical(parent,'Error : No orientation selected','No orientation has been selected, please select at least one orientation (Strike/Dip or DipAzimuth/Dip).')
    else:
        return True
    
def show_messagebox():
    dialog = QMessageBox()
    dialog.setIcon(QMessageBox.Information)
    dialog.setWindowTitle('Initiate stereonet generation')
    dialog.setText('Generation may require some time to complete depending on the amount of data being imported. Please wait until output directory opens.\n\nPress OK to start stereonet generation.')
    reply = dialog.exec_()
    if reply == QMessageBox.Ok:
        return True
    elif reply == QMessageBox.Cancel:
        return False
    
def save_stereonets(files,state,updates,settings,directory):
    df = gp_csv.update_df(gp_csv.get_df(files), updates)
    state = filter_parameters_state(state)
    for locality in state['Locality'].keys():
        for unit in state['Unit'].keys():
            for planetype in state['Plane type'].keys():
                data = gp_csv.get_nparray(df,locality,unit,planetype)
                parameters = {'Locality':locality,'Unit':unit,'Plane type':planetype}
                subdirectory = gp_dir.get_directory(directory, locality, unit)
                if data['dip'] is not None:
                    parameters['len'] = len(data['dip'])
                    if settings['Planes']:
                        if settings['Strike/Dip']:
                            gp_stereo.plot_planes(data['strike'],data['dip'],parameters,subdirectory,strike=True)
                        if settings['DipAzimuth/Dip']:
                            gp_stereo.plot_planes(data['dipazimuth'],data['dip'],parameters,subdirectory,dipazimuth=True)   
                    if settings['Plot Density Contouring'][0]:
                        if settings['Poles'] and not settings['Plot both Poles and Density Contouring']:
                            if settings['Strike/Dip']:
                                gp_stereo.plot_contouring(data['strike'],data['dip'],parameters,subdirectory,strike=True,method=settings['Plot Density Contouring'][1])
                                gp_stereo.plot_poles(data['strike'],data['dip'],parameters,subdirectory,strike=True)
                            if settings['DipAzimuth/Dip']:
                                gp_stereo.plot_contouring(data['dipazimuth'],data['dip'],parameters,subdirectory,dipazimuth=True,method=settings['Plot Density Contouring'][1])
                                gp_stereo.plot_poles(data['dipazimuth'],data['dip'],parameters,subdirectory,dipazimuth=True)
                        elif not settings['Poles']:
                            if settings['Strike/Dip']:
                                gp_stereo.plot_contouring(data['strike'],data['dip'],parameters,subdirectory,strike=True,method=settings['Plot Density Contouring'][1])
                            if settings['DipAzimuth/Dip']:
                                gp_stereo.plot_contouring(data['dipazimuth'],data['dip'],parameters,subdirectory,dipazimuth=True,method=settings['Plot Density Contouring'][1])
                        elif settings['Poles'] and settings['Plot both Poles and Density Contouring']:
                            if settings['Strike/Dip']:
                                gp_stereo.plot_contouring(data['strike'],data['dip'],parameters,subdirectory,strike=True,method=settings['Plot Density Contouring'][1],overlay=True)
                            if settings['DipAzimuth/Dip']:
                                gp_stereo.plot_contouring(data['dipazimuth'],data['dip'],parameters,subdirectory,dipazimuth=True,method=settings['Plot Density Contouring'][1],overlay=True)
                    elif settings['Poles']:
                        if settings['Strike/Dip']:
                            gp_stereo.plot_poles(data['strike'],data['dip'],parameters,subdirectory,strike=True)
                        if settings['DipAzimuth/Dip']:
                            gp_stereo.plot_poles(data['dipazimuth'],data['dip'],parameters,subdirectory,dipazimuth=True)
                else:
                    pass
    gp_dir.delete_directories(directory)
    gp_dir.open_directory(directory)
                
                
                
        
    


    