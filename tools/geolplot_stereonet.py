import matplotlib.pyplot as plt
import mplstereonet
import numpy as np

def plot_planes(strike_or_dipazimuth,dip,parameters,directory,strike=False,dipazimuth=False):
    fig = plt.figure(figsize=(8,7))
    ax = fig.add_subplot(111,projection='stereonet')
    ax.grid(True)
    ax.plane(strike_or_dipazimuth,dip,color='k',linewidth=0.5)
    replace_labels(ax)
    show_parameters(ax,parameters,strike=strike,dipazimuth=dipazimuth)
    name = get_png_name(parameters,directory,strike=strike,dipazimuth=dipazimuth,representation='planes')
    plt.savefig(name,dpi=300,bbox_inches='tight',pad_inches=0.1,format='png')
    plt.close(fig)
    
def plot_poles(strike_or_dipazimuth,dip,parameters,directory,strike=False,dipazimuth=False):   
    fig = plt.figure(figsize=(8,7))
    ax = fig.add_subplot(111,projection='stereonet')
    ax.grid(True)
    ax.pole(strike_or_dipazimuth,dip,color='k',markersize=4)
    replace_labels(ax)
    show_parameters(ax,parameters,strike=strike,dipazimuth=dipazimuth)
    name = get_png_name(parameters,directory,strike=strike,dipazimuth=dipazimuth,representation='poles')
    plt.savefig(name,dpi=300,bbox_inches='tight',pad_inches=0.1,format='png')
    plt.close(fig)
    
def plot_contouring(strike_or_dipazimuth,dip,parameters,directory,strike=False,dipazimuth=False,method=None,overlay=False):
    fig = plt.figure(figsize=(8,7))
    ax = fig.add_subplot(111,projection='stereonet')
    ax.grid(True)
    colormap = ax.density_contourf(strike_or_dipazimuth,dip,measurement='poles',method=get_method(method),cmap='Reds')
    ax.density_contour(strike_or_dipazimuth,dip,measurement='poles',method=get_method(method),cmap='turbo')
    set_colorbar(ax, colormap)
    if overlay:
        ax.pole(strike_or_dipazimuth,dip,color='k',markersize=4)
    replace_labels(ax)
    show_parameters(ax,parameters,strike=strike,dipazimuth=dipazimuth)
    representation = 'poles' if overlay else None
    name = get_png_name(parameters,directory,strike=strike,dipazimuth=dipazimuth,method=get_method(method),representation=representation)
    plt.savefig(name,dpi=300,bbox_inches='tight',pad_inches=0.1,format='png')
    plt.close(fig)
    
def get_method(method):
    methods = {'Kamb':'kamb','Kamb & Linear Smoothing':'linear_kamb',
               'Kamb & Exponential Smoothing':'exponential_kamb','Schmidt':'schmidt'}
    return methods[method]

def replace_labels(ax):
    ax.set_azimuth_ticks([])
    labels = np.arange(0,360,45)
    labels = np.column_stack((labels,0.5-0.575*np.cos(np.radians(labels+90)),0.5+0.575*np.sin(np.radians(labels+90))))
    for i in range(len(labels)):
        ax.text(labels[i,1],labels[i,2],str(labels[i,0])+'\N{DEGREE SIGN}',transform=ax.transAxes,ha='center',va='center')

def show_parameters(ax,parameters,strike=False,dipazimuth=False):
    text = f"Locality : {parameters['Locality']}\nUnit : {parameters['Unit']}\nPlane type : {parameters['Plane type']}\n"
    if strike:
        text += 'Orientation : Strike/Dip'
    elif dipazimuth:
        text += 'Orientation : Dip Azimuth/Dip'
    text += f"\n{parameters['len']} values"
    ax.text(0,-0.20,text,transform=ax.transAxes,fontsize=10,ha='center',va='center',bbox=dict(facecolor='white',alpha=0.5))
    
def set_colorbar(ax,density_contouring):
    colorbar = plt.colorbar(density_contouring,ax=ax,pad=0.1,orientation='vertical')
    colorbar.ax.set_position([0.85,0.125,0.02,0.7])
    colorbar.ax.text(0.5,1.05,'Density (%)',transform=colorbar.ax.transAxes,va='bottom',ha='center',fontsize=11)
    
def get_png_name(parameters,directory,representation=None,strike=False,dipazimuth=False,method=None):
    name = f"{directory}/{parameters['Plane type'].lower()}_{representation}_" if representation is not None else f"{directory}/{parameters['Plane type'].lower()}_"
    if strike:
        name += 'strike'
    elif dipazimuth:
        name += 'dipazimuth'
    if method is not None and isinstance(method,str):
        name += '_'+method.replace('_','-')
    return name+'.png'
    





