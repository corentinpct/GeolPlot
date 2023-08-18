import pandas as pd
import numpy as np

def get_df(files,filtered=True):
    df = pd.DataFrame()
    for file in files:
        columns = pd.read_csv(file,nrows=0).columns.str.lower().str.replace(' ','')
        columns = columns.tolist()
        if columns == ['localityid','localityname','dataid','x','y','latitude','longitude','zone',
                      'altitude','horiz_precision','vert_precision','planetype','dip','dipazimuth',
                      'strike','declination','unitid','timedate','notes'] :
            dataframe = pd.read_csv(file,header=0)
            dataframe.columns = dataframe.columns.str.lower().str.replace(' ','')
            dataframe = dataframe.applymap(lambda x: x.replace(' ','') if isinstance(x,str) else x)
            dataframe = dataframe.loc[:,['localityname','planetype','dip','dipazimuth','strike','unitid']] if filtered else dataframe
            df = pd.concat([dataframe,df])
    df.reset_index(drop=True)
    return df

def get_parameters(df):
    if isinstance(df,pd.DataFrame) and not df.empty:
        parameters = {'Locality': df['localityname'].unique().tolist(),
                      'Unit': df['unitid'].unique().tolist(),
                      'Plane type': df['planetype'].unique().tolist()}
    else:
        parameters = None
    return parameters

def get_nparray(df,locality,unit,planetype):
    query = f'localityname == "{locality}" & unitid == "{unit}" & planetype == "{planetype}"'
    dip,dipazimuth,strike = df.query(query)['dip'],df.query(query)['dipazimuth'],df.query(query)['strike']
    if not dip.empty and not dipazimuth.empty and not strike.empty :
        dip,dipazimuth,strike = dip.to_numpy(),dipazimuth.to_numpy(),strike.to_numpy()
    else:
        dip,dipazimuth,strike = None,None,None
    return {'strike':strike,'dipazimuth':dipazimuth,'dip':dip}
    
                   
def update_df(df,updates):
    columns = {'Locality':'localityname','Unit':'unitid','Plane type':'planetype'}
    if updates:
        for parameter,parameters in updates.items():
            for modified,expired in parameters.items():
                for name in expired:
                    df.loc[df[columns[parameter]] == name, columns[parameter]] = modified
    else:
        pass
    return df
            
def save_df_as(informations,file,csv=False,xlsx=False):
    df = get_df(informations['files'],filtered=False)
    df = update_df(df,informations['updates'])
    if csv:
        df.to_csv(file,index=False)
    elif xlsx:
        df.to_excel(file,index=False)
            
        