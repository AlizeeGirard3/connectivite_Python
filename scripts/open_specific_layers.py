import glob
import os
from qgis.core import QgsProject
from qgis.utils import iface

# --- CONFIGURATION ---
dossier_couches = "/Users/Aliz/Desktop/QGIS/_Connectivite_PhD/Mergin/_Connectitite_PhD_Mergin_26nov24"
dossier_styles = "/Users/Aliz/Desktop/QGIS/_Connectivite_PhD/Mergin/styles"
nom_groupe = "nepasmodifier_couchesConnectivite"

# 1. Liste des exceptions (fichiers PRO_ à NE PAS charger)
exceptions = ["PRO_point (conflicted copy, AGirard v90).shp", "PRO_repérage_zones_experimentales.shp"]

# 2. Liste de couches spécifiques (hors pattern PRO_)
couches_specifiques = ["Ecotone.restauration.zone.pt.shp"]
# ---------------------
root = QgsProject.instance().layerTreeRoot()
projet = QgsProject.instance()

# Nettoyage du groupe
groupe = root.findGroup(nom_groupe)
if groupe:
    for node in groupe.findLayers():
        projet.removeMapLayer(node.layerId())
else:
    groupe = root.addGroup(nom_groupe)

# --- RECHERCHE DES FICHIERS ---
# On prend les PRO_*.shp
tous_les_pro = glob.glob(os.path.join(dossier_couches, "*PRO_*.shp"))

# On filtre les exceptions
fichiers_a_charger = [f for f in tous_les_pro if os.path.basename(f) not in exceptions]

# On ajoute les couches spécifiques (si elles existent)
for spec in couches_specifiques:
    chemin_spec = os.path.join(dossier_couches, spec)
    if os.path.exists(chemin_spec):
        fichiers_a_charger.append(chemin_spec)

# --- CHARGEMENT ET STYLE ---
for chemin in fichiers_a_charger:
    nom_base = os.path.splitext(os.path.basename(chemin))[0]
    
    couche = iface.addVectorLayer(chemin, nom_base, "ogr")
    
    if couche and couche.isValid():
        # Application du style correspondant
        chemin_style = os.path.join(dossier_styles, f"{nom_base}.qml")
        if os.path.exists(chemin_style):
            couche.loadNamedStyle(chemin_style)
            couche.triggerRepaint()
        
        # Rangement dans le groupe
        noeud = root.findLayer(couche.id())
        if noeud:
            copie_noeud = noeud.clone()
            groupe.addChildNode(copie_noeud)
            root.removeChildNode(noeud)

print(f"Import terminé. {len(fichiers_a_charger)} couches traitées.")