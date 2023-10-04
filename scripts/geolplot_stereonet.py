import matplotlib.pyplot as plt
import mplstereonet
import numpy as np

class Stereonets:
    def __init__(self,locality,unit,planetype,directory):
        self.locality = locality
        self.unit = unit
        self.planetype = planetype
        self.directory = directory
    
    def _replace(self,ax):
        ax.set_azimuth_ticks([])
        labels = np.arange(0,360,45)
        labels = np.column_stack((labels,0.5-0.575*np.cos(np.radians(labels+90)),0.5+0.575*np.sin(np.radians(labels+90))))
        for i in range(len(labels)):
            ax.text(labels[i,1],labels[i,2],str(labels[i,0])+'\N{DEGREE SIGN}',transform=ax.transAxes,ha='center',va='center')
    
    def _show(self,ax,strike=False,dipazimuth=False,method=None):
        text = f"Locality : {self.locality}\nUnit : {self.unit}\nPlane type : {self.planetype}\n"
        text += 'Orientation : Strike/Dip' if strike else 'Orientation : Dip Azimuth/Dip'
        if method is not None :
            text +=f"\nDensity gradient : {method}"
        text += f"\n{self.len} values"
        ax.text(0,-0.20,text,transform=ax.transAxes,fontsize=10,ha='center',va='center',bbox=dict(facecolor='white',alpha=0.5))
    
    def _name(self,dtype=None,strike=False,dipazimuth=False,method=None):
        path = f'{self.directory}/{self.locality}/{self.unit}'
        if dtype is not None:
            name = f'{path}/{self.planetype.lower()}_{dtype}_'
        else:
            name = f'{path}/{self.planetype.lower()}_'
        if method is not None:
            name += method.replace('_','-')+'_'
        if strike:
            name += 'strike'
        if dipazimuth:
            name += 'dipazimuth'
        return name+'.png'
        
    def planes(self,data,dip,strike=False,dipazimuth=False):
        self.len = len(dip)
        fig = plt.figure(figsize=(8,7))
        ax = fig.add_subplot(111,projection='stereonet')
        ax.grid(True)
        ax.plane(data,dip,color='k',linewidth=0.5)
        self._replace(ax)
        self._show(ax,strike=strike,dipazimuth=dipazimuth)
        name = self._name(dtype='planes',strike=strike,dipazimuth=dipazimuth)
        plt.savefig(name,dpi=300,bbox_inches='tight',pad_inches=0.1,format='png')
        plt.close(fig)

    def poles(self,data,dip,strike=False,dipazimuth=False):
        self.len = len(dip)
        fig = plt.figure(figsize=(8,7))
        ax = fig.add_subplot(111,projection='stereonet')
        ax.grid(True)
        ax.pole(data,dip,color='k',markersize=4)
        self._replace(ax)
        self._show(ax,strike=strike,dipazimuth=dipazimuth)
        name = self._name(dtype='poles',strike=strike,dipazimuth=dipazimuth)
        plt.savefig(name,dpi=300,bbox_inches='tight',pad_inches=0.1,format='png')
        plt.close(fig)

    def densitycontour(self,data,dip,strike=False,dipazimuth=False,method=None,overlay=False):
        def setcolorbar(ax,colormap):
            colorbar = plt.colorbar(colormap,ax=ax,pad=0.1,orientation='vertical')
            colorbar.ax.set_position([0.85,0.125,0.02,0.7])
            colorbar.ax.text(0.5,1.05,'Density (%)',transform=colorbar.ax.transAxes,va='bottom',ha='center',fontsize=11)
        self.len= len(dip)  
        fig = plt.figure(figsize=(8,7))
        ax = fig.add_subplot(111,projection='stereonet')
        ax.grid(True)
        colormap = ax.density_contourf(data,dip,measurement='poles',method=method,cmap='Reds')
        ax.density_contour(data,dip,measurement='poles',method=method,cmap='turbo')
        setcolorbar(ax,colormap)
        if overlay:
            ax.pole(data,dip,color='k',markersize=4)
        self._replace(ax)
        self._show(ax,strike=strike,dipazimuth=dipazimuth,method=method)
        if overlay:
            name = self._name(dtype='poles',strike=strike,dipazimuth=dipazimuth,method=method)
        else:
            name = self._name(strike=strike,dipazimuth=dipazimuth,method=method)
        plt.savefig(name,dpi=300,bbox_inches='tight',pad_inches=0.1,format='png')
        plt.close(fig)




