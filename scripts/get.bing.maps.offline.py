from qgis.PyQt.QtCore import *


l=range(0,1) 

for i in l:


    x=int(i)


    layer = iface.mapCanvas().currentLayer()
    layer.select(x)


    qgis.utils.iface.actionZoomToSelected().trigger()

    layer.deselect(x)



    nom=str(x)


    qgis.utils.iface.mapCanvas().saveAsImage('/Users/Aliz/Desktop/QGIS/_Connectivite_PhD/Mergin/_Connectivite_PhD_Mergin/'+ nom +'.tiff')
