import processing
from qgis.core import QgsProject

# 1. Définir le chemin complet du fichier Shapefile de sortie
nom = "SFSM_cours.d.eau_ordre.3.plus"
chemin_sortie = f"/Users/Aliz/Desktop/QGIS/_Connectivite_PhD/Mergin/_ChapitreVI/_ChapitreVI/{nom}.shp"

# 2. Récupérer la couche active (celle où les entités sont sélectionnées)
couche = iface.activeLayer()

# 3. Exécuter l'algorithme pour exporter uniquement la sélection
parametres = {
    'INPUT': couche,
    'OUTPUT': chemin_sortie
}
processing.run("native:saveselectedfeatures", parametres)

# 4. Charger automatiquement le nouveau Shapefile dans QGIS
iface.addVectorLayer(chemin_sortie, nom, "ogr")