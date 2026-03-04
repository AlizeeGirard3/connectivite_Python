import os
from qgis.core import QgsProject

# Dossier où enregistrer les styles
dossier_styles = "/Users/Aliz/Desktop/QGIS/_Connectivite_PhD/Mergin/styles"
if not os.path.exists(dossier_styles):
    os.makedirs(dossier_styles)

# Nom exact de ta couche spécifique
couche_specifique = "Ecotone.restauration.zone.pt"

counter = 0
for layer in QgsProject.instance().mapLayers().values():
    source = layer.source()
    nom_couche = layer.name()
    
    # CONDITION : 
    # 1. Soit elle contient "PRO_" ET c'est un .shp
    # 2. Soit c'est exactement le nom de ta couche spécifique
    if ("PRO_" in nom_couche and source.lower().endswith(".shp")) or (nom_couche == couche_specifique):
        
        # On enregistre le style avec le nom exact de la couche
        chemin_qml = os.path.join(dossier_styles, f"{nom_couche}.qml")
        layer.saveNamedStyle(chemin_qml)
        print(f"Style exporté pour : {nom_couche}")
        counter += 1

print(f"Exportation terminée : {counter} styles générés dans {dossier_styles}")
