from PyQt5.QtWidgets import QFileDialog,QMessageBox,QHBoxLayout,QVBoxLayout,QCheckBox,QComboBox
import pandas as pd
import numpy as np
import os

from scripts import geolplot_stereonet as gpstereo

def selectdir():
    dialog = QFileDialog()
    dialog.setWindowTitle('Select the directory in which the stereographic representations will be generated.')
    dialog.setFileMode(QFileDialog.Directory)
    if dialog.exec() == QFileDialog.Accepted:
        return dialog.selectedFiles()[0]

def selectcsv(files,insert=False,parent=None):
    dialog = QFileDialog()
    dialog.setWindowTitle('Import FieldMOVE Clino CSV file(s)')
    dialog.setFileMode(QFileDialog.ExistingFiles)
    dialog.setNameFilter('CSV Files (*.csv)')
    if dialog.exec() == QFileDialog.Accepted:
        files = {} if not insert else files
        for file in dialog.selectedFiles():
            if controlfiles(file,csv=True):
                files[file]=True
        if not files :
            QMessageBox.critical(parent,'Error : Imported file(s) cannot be read','Data from imported file(s) do not represent geological planes. Please select one or more CSV files from a FieldMOVE Clino project containing plane data.')
        df = {}
        for file in files.keys():
            df[file] = getdf(file,csv=True)
        return files,df

def selectxlsx(files,insert=False,parent=None):
    dialog = QFileDialog()
    dialog.setWindowTitle('Import FieldMOVE Clino Excel file(s)')
    dialog.setFileMode(QFileDialog.ExistingFiles)
    dialog.setNameFilter('Excel Files (*.xlsx)')
    if dialog.exec() == QFileDialog.Accepted:
        files = {} if not insert else files
        for file in dialog.selectedFiles():
            if controlfiles(file,xlsx=True):
                files[file]=True
        if not files :
            QMessageBox.critical(parent,'Error : Imported file(s) cannot be read','Data from imported file(s) do not represent geological planes. Please select one or more Excel files containing plane data.')
        df = {}
        for file in files.keys():
            df[file] = getdf(file,xlsx=True)
        return files,df
    
def controlfiles(file,csv=False,xlsx=False):
    standard = ['localityid',
                'localityname',
                'dataid',
                'x',
                'y',
                'latitude',
                'longitude',
                'zone',
                'altitude',
                'horiz_precision',
                'vert_precision',
                'planetype',
                'dip',
                'dipazimuth',
                'strike',
                'declination',
                'unitid',
                'timedate',
                'notes']
    if csv:
        df = pd.read_csv(file,nrows=5)
    elif xlsx:
        df = pd.read_excel(file,nrows=5)
    columns = df.columns.str.lower().str.replace(' ','')
    columns = columns.tolist()
    if 'rockunit' in columns:
        columns = columns.replace('rockunit','unitid')
    return columns == standard and not df.empty

def getdf(file,csv=False,xlsx=False):
    if csv:
        df = pd.read_csv(file,header=0)
    elif xlsx:
        df = pd.read_excel(file,header=0)
    df.columns = df.columns.str.lower().str.replace(' ','')
    df.columns = df.columns.str.replace('rockunit','unitid') if 'rockunit' in df.columns.tolist() else df.columns
    df = df.loc[:,['localityname','planetype','unitid']]
    df = df.applymap(lambda x: x.replace(' ','') if isinstance(x,str) else x)
    return df

def getallparameters(dataframes):
    def list_to_dict(names):
        parameters = {}
        for name in names:
            parameters[name] = [False,True]
        return parameters
    df = pd.DataFrame()
    for file in dataframes.keys():
        df = pd.concat([dataframes[file],df])
    locality = df['localityname'].unique().tolist()
    locality = list_to_dict(sorted(locality))
    unit = df['unitid'].unique().tolist()
    unit = list_to_dict(sorted(unit))
    planetype = df['planetype'].unique().tolist()
    planetype = list_to_dict(sorted(planetype))
    return locality,unit,planetype

def harmonizedf(files,dataframes,filtered=False):
    df = pd.DataFrame()
    locality = []
    unit = []
    planetype = []
    if isinstance(files,dict):
        files = list(files.keys())
    for file in files:
        if file.endswith('.csv'):
            child = pd.read_csv(file,header=0)
        elif file.endswith('.xlsx'):
            child = pd.read_excel(file,header=0)
        child.columns = child.columns.str.lower().str.replace(' ','')
        child.columns = child.columns.str.replace('rockunit','unitid') if 'rockunit' in child.columns.tolist() else child.columns
        child = child.applymap(lambda x: x.replace(' ','') if isinstance(x,str) else x)
        df = pd.concat([df,child])
        locality.extend(dataframes[file]['localityname'].tolist())
        unit.extend(dataframes[file]['unitid'].tolist())
        planetype.extend(dataframes[file]['planetype'].tolist())
    df['localityname'] = locality
    df['unitid'] = unit
    df['planetype'] = planetype
    if filtered :
        df = df.loc[:,['localityname','planetype','dip','dipazimuth','strike','unitid']]
    return df

def savedf(files,csv=False,xlsx=False,parent=None):
    if csv :
        filename,_ = QFileDialog.getSaveFileName(parent, 'Save as CSV file (.csv)', '', 'CSV Files (*.csv)')
    elif xlsx :
        filename,_ = QFileDialog.getSaveFileName(parent, 'Save as Excel file (.xlsx)', '', 'Excel Files (*.xlsx)')
    if filename :
        try:
            df = harmonizedf(files,files)
            if csv :
                df.to_csv(filename,index=False)
            elif xlsx :
                df.to_excel(filename,index=False)
        except Exception as exception:
            QMessageBox.critical(parent,'Error : Dataframe cannot be saved',f'Error while saving the dataframe : {exception}')

def rename(signal,states,dataframes,column=None):
    name = list(signal.keys())[0]
    states[name] = [any(states[key][0] for key in list(signal.values())[0]),any(states[key][1] for key in list(signal.values())[0])]
    states = {key:state for key,state in states.items() if key not in list(signal.values())[0]}
    for file,df in dataframes.items():
        for names in signal[name]:
            df.loc[df[column] == names,column] = name
    return states,dataframes

def getsettings(layout):
    states = {'strike':False,
             'dipazimuth':False,
             'planes':False,
             'poles':False,
             'density':False,
             'method':None,
             'both':False}
    translations = {'Strike/Dip':'strike',
                    'DipAzimuth/Dip':'dipazimuth',
                    'Planes':'planes',
                    'Poles':'poles',
                    'Plot Density Contouring':'density',
                    'Kamb':'kamb',
                    'Kamb & Linear Smoothing':'linear_kamb',
                    'Kamb & Exponential Smoothing':'exponential_kamb',
                    'Schmidt':'schmidt',
                    'Plot both Poles and Density Contouring':'both'}
    for i in range(layout.count()):
        item = layout.itemAt(i).widget()
        if isinstance(item, QCheckBox):
            states[translations[item.text()]] = item.isChecked()
        elif item is None:
            item = layout.itemAt(i).layout()
            if item is not None and isinstance(item,(QHBoxLayout,QVBoxLayout)):
                for j in range(item.count()):
                    child = item.itemAt(j).widget()
                    if isinstance(child, QCheckBox):
                        states[translations[child.text()]] = child.isChecked()
                    elif isinstance(child, QComboBox):
                        states['method'] = translations[child.currentText()]   
    return states

def controlparameters(locality,unit,planetype,files,parent=None):
    if not any(files.values()):
        return False
    if not any(locality[state][0] for state in locality):
        QMessageBox.critical(parent,'Error : No Locality selected','No Locality have been selected, please select at least one parameter for Locality.')
        return False
    if not any(unit[state][0] for state in unit):
        QMessageBox.critical(parent,'Error : No Unit selected','No Unit have been selected, please select at least one parameter for Unit.')
        return False
    if not any(planetype[state][0] for state in planetype):
        QMessageBox.critical(parent,'Error : No Plane type selected','No Plane type have been selected, please select at least one parameter for Plane type.')
        return False
    return True        

def controlsettings(layout,directory,parent=None):
    states = getsettings(layout)
    if not any(states[item] for item in ['strike','dipazimuth']):
        QMessageBox.critical(parent,'Error : No orientation selected','No orientation has been selected, please select Strike/Dip and/or DipAzimuth/Dip.')
        return False
    if not any(states[item] for item in ['planes','poles','density']):
        QMessageBox.critical(parent,'Error : No representation selected','No representation have been selected, please select Planes and/or Poles and/or Density Contouring.')
        return False
    if not directory :
        QMessageBox.critical(parent,'Error : No directory selected','No directory has been selected. Please select the output directory.')
        return False
    return True

def messagebox():
    dialog = QMessageBox()
    dialog.setIcon(QMessageBox.Information)
    dialog.setWindowTitle('Initiate stereonet generation')
    dialog.setText('Generation may require some time to complete depending on the amount of data being imported. Please wait until output directory opens.\n\nPress OK to start stereonet generation.')
    reply = dialog.exec_()
    if reply == QMessageBox.Ok:
        return True
    elif reply == QMessageBox.Cancel:
        return False
    
def savestereonet(locality,unit,planetype,files,dataframes,settings,directory):   
    df = harmonizedf(files,dataframes,filtered=True)
    combinations = np.array([])
    for localityid in locality:
        unitid = df.query(f'localityname=="{localityid}"')['unitid'].unique().tolist()
        unitid = [item for item in unitid if item in unit]
        if unitid:
            for unitid in unitid:
                planetypeid = df.query(f'localityname == "{localityid}" & unitid == "{unitid}"')['planetype'].unique().tolist()
                planetypeid = [item for item in planetypeid if item in planetype]
                if planetypeid:
                    for planetypeid in planetypeid:
                        if combinations.size == 0:
                            combinations = np.array([localityid,unitid,planetypeid])
                        else:
                            combinations = np.vstack((combinations,np.array([localityid,unitid,planetypeid])))
    if len(combinations.shape) == 1:
        combinations = np.array([combinations])
    for combination in combinations:
        if not os.path.exists(f'{directory}/{combination[0]}/{combination[1]}'):
            os.makedirs(f'{directory}/{combination[0]}/{combination[1]}')    
    data = {}
    for i,combination in enumerate(combinations):
        dip = df.query(f'localityname =="{combination[0]}" & unitid =="{combination[1]}" & planetype == "{combination[2]}"')['dip']
        dip = dip.to_numpy()
        data[i] = {'dip':dip}
        if settings['strike'] :
            strike = df.query(f'localityname =="{combination[0]}" & unitid =="{combination[1]}" & planetype == "{combination[2]}"')['strike']
            strike = strike.to_numpy()
            data[i]['strike'] = strike
        if settings['dipazimuth'] :
            dipazimuth = df.query(f'localityname =="{combination[0]}" & unitid =="{combination[1]}" & planetype == "{combination[2]}"')['dipazimuth']
            dipazimuth = dipazimuth.to_numpy()
            data[i]['dipazimuth'] = dipazimuth
    if settings['planes'] and (settings['strike'] and settings['dipazimuth']):
        for i,combination in enumerate(combinations):
            locality = combination[0]
            unit = combination[1]
            planetype = combination[2]
            stereonets = gpstereo.Stereonets(locality, unit, planetype, directory)
            stereonets.planes(data[i]['dipazimuth'],data[i]['dip'],dipazimuth=True)
            stereonets.planes(data[i]['strike'],data[i]['dip'],strike=True)   
    if settings['planes'] and not (settings['strike'] and settings['dipazimuth']):
        if settings['strike']:
            for i,combination in enumerate(combinations):
                locality = combination[0]
                unit = combination[1]
                planetype = combination[2]
                stereonets = gpstereo.Stereonets(locality, unit, planetype, directory)
                stereonets.planes(data[i]['strike'],data[i]['dip'],strike=True)       
        if settings['dipazimuth']:
            for i,combination in enumerate(combinations):
                locality = combination[0]
                unit = combination[1]
                planetype = combination[2]
                stereonets = gpstereo.Stereonets(locality, unit, planetype, directory)
                stereonets.planes(data[i]['dipazimuth'],data[i]['dip'],dipazimuth=True)        
    if settings['poles'] and (settings['strike'] and settings['dipazimuth']):
        for i,combination in enumerate(combinations):
            locality = combination[0]
            unit = combination[1]
            planetype = combination[2]
            stereonets = gpstereo.Stereonets(locality, unit, planetype, directory)
            stereonets.poles(data[i]['dipazimuth'],data[i]['dip'],dipazimuth=True)
            stereonets.poles(data[i]['strike'],data[i]['dip'],strike=True)     
    if settings['poles'] and not (settings['strike'] and settings['dipazimuth']):
        if settings['strike']:
            for i,combination in enumerate(combinations):
                locality = combination[0]
                unit = combination[1]
                planetype = combination[2]
                stereonets = gpstereo.Stereonets(locality, unit, planetype, directory)
                stereonets.poles(data[i]['strike'],data[i]['dip'],strike=True)        
        if settings['dipazimuth']:
            for i,combination in enumerate(combinations):
                locality = combination[0]
                unit = combination[1]
                planetype = combination[2]
                stereonets = gpstereo.Stereonets(locality, unit, planetype, directory)
                stereonets.poles(data[i]['dipazimuth'],data[i]['dip'],dipazimuth=True)    
    if settings['density'] and (settings['strike'] and settings['dipazimuth']):
        for i,combination in enumerate(combinations):
            locality = combination[0]
            unit = combination[1]
            planetype = combination[2]
            stereonets = gpstereo.Stereonets(locality, unit, planetype, directory)
            stereonets.densitycontour(data[i]['dipazimuth'],data[i]['dip'],dipazimuth=True,method=settings['method'],overlay=settings['both'])
            stereonets.densitycontour(data[i]['strike'],data[i]['dip'],strike=True,method=settings['method'],overlay=settings['both'])
    if settings['density'] and not (settings['strike'] and settings['dipazimuth']):
        if settings['strike']:
            for i,combination in enumerate(combinations):
                locality = combination[0]
                unit = combination[1]
                planetype = combination[2]
                stereonets = gpstereo.Stereonets(locality, unit, planetype, directory)
                stereonets.densitycontour(data[i]['strike'],data[i]['dip'],strike=True,method=settings['method'],overlay=settings['both'])
        if settings['dipazimuth']:
            for i,combination in enumerate(combinations):
                locality = combination[0]
                unit = combination[1]
                planetype = combination[2]
                stereonets = gpstereo.Stereonets(locality, unit, planetype, directory)
                stereonets.densitycontour(data[i]['dipazimuth'],data[i]['dip'],dipazimuth=True,method=settings['method'],overlay=settings['both'])
    os.system(f'explorer "{os.path.abspath(directory)}"') if os.name == 'nt' else os.system(f'xdg-open "{os.path.abspath(directory)}"')
                
                
                
        
    


    