# GeolPlot
A simple Python GUI to process and represent data from FieldMOVE Clino projects.

------------------------------------------------------------------------

`GeolPlot` allows users to __import CSV _planes_ files__ from [FieldMOVE Clino](https://www.petex.com/products/move-suite/digital-field-mapping/) projects, to __harmonize__ the imported data and to generate __multiple stereographic representations__ based on user-defined parameters and settings.

`GeolPlot` is based on open-source tools [openstereo_addon](https://github.com/corentinpct/openstereo_addon), [OpenStereo](https://openstereo.readthedocs.io/en/latest/) and [mplstereonet](https://github.com/joferkington/mplstereonet) but (for now) only provides reading and representation of data from FieldMOVE Clino files, unlike other available tools.

## Table of contents
- [Installation](#installation)
- [Requirements](#requirements)
- [User Guide](#user-guide)
    - [Import CSV file(s) from FieldMOVE Clino project(s)](#import-csv-files-from-fieldmove-clino-projects)
    - [Add data on current data from CSV file(s)](#add-data-on-current-data-from-csv-files)
    - [Rename specific parameters from imported CSV file(s)](#rename-specific-parameters-from-imported-csv-files)
    - [Save current data as a XLSX or CSV file](#save-current-data-as-a-xlsx-or-csv-file)
    - [Generate stereographic representations from imported data](#generate-stereographic-representations-from-imported-data)
        - [Stereonets generation process](#stereonets-generation-process)
        - [Examples of generated stereographic representations](#examples-of-generated-stereographic-representations)
- [Roadmap](#roadmap)
    
## Installation
Firstly, make sure to __download the latest version__ published of the `GeolPlot` repository locally.
__Run the script__ `geolplot.py` with a Python IDE or use the following command in a shell :
```bash
python -m geolplot.py
```
`GeolPlot` should then start.

If you encounter an __error related to the required packages__ when starting the application, please refer to the following section. 
However, if the error is not related to the required packages, feel free to report the issue in the ['Issues' section](https://github.com/corentinpct/GeolPlot/issues) of the `GeolPlot` repository.

## Requirements
`GeolPlot` relies on several __Python packages__ that ensure the proper functioning of the graphical interface, data reading and processing, and stereographic representations. The complete list of packages present in `GeolPlot` and their versions is provided below: 
- _[Python](https://www.python.org/) : 3.10.12_
- _[PyQt5](https://riverbankcomputing.com/software/pyqt/intro) : 5.15.7_
- _[Matplotlib](https://matplotlib.org/stable/) : 3.6.2_
- _[mplstereonet](https://github.com/joferkington/mplstereonet) : 0.7_
- _[NumPy](https://numpy.org/doc/stable/) : 1.25.2_
- _[Pandas](https://pandas.pydata.org/) : 2.0.3_

You can __install the required packages__ by executing the following command :
```bash
pip install \
    PyQt5 \
    numpy \
    pandas \
    matplotlib \
```
Please note that `mplstereonet` might present __deprecation warnings__. We recommend __installing the package locally__ following the [mplstereonet](https://github.com/joferkington/mplstereonet#install) installation.

## User guide
This section aims to provide a __basic and comprehensive overview__ of `GeolPlot`. Each feature present in the program is associated with examples from synthetic data sets. All resources associated with this guide are provided in the _[examples]()_ section of the repository.

### Import CSV file(s) from FieldMOVE Clino project(s)
Once `GeolPlot` is launched, the user will be prompted to import data from __one or multiple CSV files__ to start the application. Currently, the program can __only process files associated with geological plans__ (it does not support lineations).

__In the `File` tab, select `Import` then `Import CSV file(s)`__. 

![Import CSV file(s)](https://github.com/corentinpct/GeolPlot/assets/133667270/73b7d978-686f-494b-8836-f311838e8203)

A dialog window will open, __allowing you to choose one or more CSV files from FieldMOVE Clino projects__. __No modifications should be made to the files exported from the mobile application__, as they must strictly adhere to the initial format of the CSV file generated by FieldMOVE Clino.

Once the file(s) are imported, the `GeolPlot` main window will appear as follows. In the __upper-left part of the window__, the __currently imported files__ will be listed. In the __lower-left part__, the user __can navigate through the parameters__ (_Locality_, _Unit_ and _Plane type_ from the FieldMOVE Clino project exported) and __select the data they wish to represent__ later.

_We have selected sample1.csv for this first step._

![Import CSV file(s)](https://github.com/corentinpct/GeolPlot/assets/133667270/152a9993-f9d4-4288-9d93-1a17594d9fde)

### Add data on current data from CSV file(s)
`GeolPlot` allows, at any point before generation, to __import additional CSV files__ without needing to import the previously imported files again. 

__In the `File` tab, select `Add data on current data` then `From CSV file(s)`__ to open the CSV file selection dialog window.

![Add data from CSV file(s)](https://github.com/corentinpct/GeolPlot/assets/133667270/fa2c7475-4b4c-4005-b6ac-25996614ade2)

Once the additional CSV file(s) imported, the upper-left part of the window and the content of the lower-left window will be updated.

_We have selected sample2.csv as an additional CSV file for this step._

![Add data from CSV file(s)](https://github.com/corentinpct/GeolPlot/assets/133667270/9d487764-d014-4e8e-af61-a9e03ffe3bdd)

### Rename specific parameters from imported CSV file(s)
In the case of __group work__, it is possible that each parameter (_Locality_, _Unit_ and _Plane type_) has been defined heterogeneously across FieldMOVE Clino projects. Therefore, the program offers an option __to harmonize the names identified__ in the imported CSV files. 

__In the `Data` tab, select `Set name(s) for` then select select the parameter you want to change__.

_In this case, UnitA and StrataA represent the same geological unit (see the lower-left part of the window). Similarly for the pair UnitB and StrataB and the pair UnitC and StrataC._

![Rename specific parameters](https://github.com/corentinpct/GeolPlot/assets/133667270/9cb0f9e0-720c-4cb6-893c-85da54503734)

This will open the following dialog window (spaces will be removed from the name entered in this window to reduce errors related to stereonet generation).

_Here, we rename StrataA to Unit A to harmonize the data between the two imported files_

![Rename specific parameters](https://github.com/corentinpct/GeolPlot/assets/133667270/773c3ad6-898d-423b-a683-c3920f589bf6)

_After repeating this process for the remaining data, we obtain the following geological units._

![Rename specific parameters](https://github.com/corentinpct/GeolPlot/assets/133667270/dab043cf-5c5c-4ac5-abb2-eda3f3f1c3a2)

### Save current data as a XLSX or CSV file
`GeolPlot` allows the user to save imported data as `.xslx` or `.csv`. This feature allows obtaining a __more readable file format__ than the one proposed by FieldMOVE Clino, as well as __concatenating data from multiple imported CSV files in a single file__. Saving the data __also applies the modifications made in `GeolPlot`__ to the original data and produces a __single harmonized file__.

__In the `File` tab, select `Save current data as` then select the desired extension__ to open a dialog window. 

![Save data as XLSX or CSV](https://github.com/corentinpct/GeolPlot/assets/133667270/8e8645bd-b7af-4693-b7ed-e01d7263d703)

_Here, we have saved the data in the file `mergedsamples.xlsx` findable in [examples](http://github.com/corentinpct/GeolPlot/blob/main/examples)._

### Generate stereographic representations from imported data
`GeolPlot` allows the user to customize the stereographic representations they want. These options are mainly facilitated by the mplstereonet package (for any information regarding stereographic representation, consider visiting the [mplstereonet Github repository](https://github.com/joferkington/mplstereonet)). 

Here, the user should define __at least a locality, a unit, a plane type, an orientation and an output directory__ to initiate stereographic representation. The __available methods for plotting density contouring__ are the methods provided in the __mplstereonet package__

_In this case, we have selected all parameters from imported CSV files and each representation settings to generate all stereographic representations from this synthetic data set._

![Generate stereonets from data](https://github.com/corentinpct/GeolPlot/assets/133667270/490dcbfb-2d43-460b-bf5b-136fe7f88144)

As soon as the user wants to initiate the generation, they just need to __click on `Generate` at the bottom right__.

#### Stereonets generation process
1) `GeolPlot` __creates directories for each selected _Locality___ in the output directory selected __and then subdirectories for each selected _Unit___.
2) `GeolPlot` __generates and saves stereonets__ based on the _Plane type(s)_ and the representation settings selected. Stereonets are saved under the following name :
```
{Plane type}_{Poles, Planes or empty (if density contouring is plotted without poles)}_{Strike or Dip Azimuth}_{Method (if density contouring is plotted)}.png
```
4) `GeolPlot` __removes empty directories__ where no stereonet could be generated.
5) `GeolPlot` __opens the output directory__ when the process is over.

_Based on our synthetic data set and the parameters and settings selected, `GeolPlot` will produce the following result :_
```
├── examples (our output directory)
    ├── Locality1
        ├── UnitA
            ├── bedding_dipazimuth_linear-kamb.png
            ├── bedding_planes_dipazimuth.png
            ├── bedding_planes_strike.png
            ├── bedding_poles_dipazimuth.png
            ├── bedding_poles_strike.png
            ├── bedding_strike_linear-kamb.png
            ├── overturnedbedding_dipazimuth_linear-kamb.png
            ├── overturnedbedding_planes_dipazimuth.png
            ├── overturnedbedding_planes_strike.png
            ├── overturnedbedding_poles_dipazimuth.png
            ├── overturnedbedding_poles_strike.png
            └── overturnedbedding_strike_linear-kamb.png
        └── UnitD
            └── 12 stereonets 
    ├── Locality2
        └── UnitB
            └── 24 stereonets
    ├── Locality3
        └── UnitB
            └── 18 stereonets
    ├── Locality4
        └── UnitB
            └── 12 stereonets
    ├── Locality5
        └── UnitB
            └── 6 stereonets
    ├── Locality6
        └── UnitB
            └── 24 stereonets
    ├── Locality7
        └── UnitB
            └── 24 stereonets
    ├── Locality8
        └── UnitC
            └── 24 stereonets
    └── Locality9
        └── UnitA
            └── 12 stereonets
```
_`GeolPlot` produced a total of __174 stereographic representations__ with an __average execution time__ of __1 min 30 sec__ (this time is only applicable for this dataset but provides an idea of the overall duration of the process)._

Once the output directory is open, the user can now navigate through the created directories and open the generated stereonets. 
#### Examples of generated stereographic representations
Below, several examples of generated stereonets from the synthetic data set will be presented.

![cleavage_planes_strike](https://github.com/corentinpct/GeolPlot/assets/133667270/d22b11ec-676f-4ba3-8b2e-1161f23fd7af)

_A stereonet of __Locality 2, Unit B, Cleaveage in Strike/Dip__ represented as __planes__._

![cleavage_poles_strike](https://github.com/corentinpct/GeolPlot/assets/133667270/3b47da62-346a-4c22-a7ac-5b5fb5814b41)

_A stereonet of the same data that the previous stereonet but represented as __poles__._

![joint_dipazimuth_linear-kamb](https://github.com/corentinpct/GeolPlot/assets/133667270/8c2bfad8-7cda-4c33-b306-ae2e8ded01db)

_A stereonet of __Locality 5, Unit B, Joint in Dip Azimuth/Dip__ with a __density contouring & Kamb linear smoothing__._

![joint_poles_dipazimuth_linear-kamb](https://github.com/corentinpct/GeolPlot/assets/133667270/96437c2f-a407-45fe-a846-6667836ed731)

_A stereonet of __Locality 2, Unit B, Joint in Dip Azimuth/Dip__ represented as __poles__ and with a __density contouring & Kamb linear smoothing__._

## Roadmap
While `GeolPlot` offers some advantages in processing and representing data from FieldMOVE Clino projects, it also has several areas that require further improvement. This section is dedicated to possible enhancements for the program. Feel free to communicate any changes you would like to see in the program in the ['Issues' section](https://github.com/corentinpct/GeolPlot/issues).

List of features to develop :
- [ ] Import, process and represent data from `line.csv` from FieldMOVE Clino project(s).
- [ ] Improve data import by recognizing `plane.csv` and `line.csv` files within a FieldMOVE Clino project (_'Import'->'From a FieldMOVE Clino project' for example_).
- [ ] Build a `.exe` to improve the program's portability.
- [ ] Allow the user to customize stereographic representations further using a dedicated window (as offered by [OpenStereo](https://openstereo.readthedocs.io/en/latest/)).
- [ ] Make the parameters selection more interactive by providing filtering systems based on previously selected parameters (_If 'Locality 1' is selected then only the units in this locality will be displayed in the `Unit` tab for example_).
