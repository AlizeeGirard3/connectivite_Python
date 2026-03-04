# ## 4 mars 2026
# ## recouper les lits d'écoul pot (MRNF, 2025) au sud de la rivière Etchemin
## version finale

import processing
from qgis.core import (QgsVectorLayer, QgsProject, QgsFeatureRequest,
                       QgsCoordinateTransform, QgsCoordinateReferenceSystem)

# --- 1. CONFIGURATION DES CHEMINS ---
path_source = r"/Users/Aliz/Desktop/QGIS/DONNÉES QUÉBEC/Diffusion2/Imagerie/Produits_derives_LiDAR/Hydrographie/Lits_ecoulements_potentiels/3-Donnees/UDH_02AE/Hydro_LiDAR_02AE.gdb|layername=Ecoulements_02AE"
path_masque = r"/Users/Aliz/Desktop/QGIS/_Connectivite_PhD/Mergin/_ChapitreIII/_ChapitreIII/STH_masque_lit_ecoul_pot_02AE.shp"
path_sortie = r"/Users/Aliz/Desktop/QGIS/_Connectivite_PhD/Mergin/_ChapitreIII/_ChapitreIII/Hydro_LiDAR_02AE_decoupe.shp"

# --- 2. CHARGEMENT ET ADAPTATION AU ZOOM (CRS SAFE) ---
canvas = iface.mapCanvas()
source_layer = QgsVectorLayer(path_source, "Source_Complete", "ogr")

if not source_layer.isValid():
    print("Erreur : Impossible de charger la source LiDAR.")
else:
    # GESTION DU CRS : On transforme l'emprise du zoom vers le CRS du LiDAR
    # Cela évite l'erreur "Aucune entité trouvée" due au décalage mètres/degrés
    transform = QgsCoordinateTransform(canvas.mapSettings().destinationCrs(),
                                       source_layer.crs(),
                                       QgsProject.instance())
    extent_corrige = transform.transformBoundingBox(canvas.extent())

    # Extraction des entités visibles uniquement
    request = QgsFeatureRequest().setFilterRect(extent_corrige)
    input_layer = source_layer.materialize(request)

    if input_layer.featureCount() == 0:
        print("Erreur : Aucune entité trouvée. Vérifiez que vous voyez le LiDAR à l'écran.")
    else:
        print(f"Traitement de {input_layer.featureCount()} entités...")

        # --- 3. EXÉCUTION DE LA DIFFÉRENCE ---
        parametres = {
            'INPUT': input_layer,
            'OVERLAY': path_masque,
            'OUTPUT': path_sortie # Sauvegarde physique sur le disque
        }

        # On lance l'algorithme
        processing.run("native:difference", parametres)

        # --- 4. CHARGEMENT ET NETTOYAGE ---
        res_layer = QgsVectorLayer(path_sortie, "Hydro_LiDAR_02AE_decoupe", "ogr")
        if res_layer.isValid():
            QgsProject.instance().addMapLayer(res_layer)
            # Optionnel : Supprimer la source lourde pour alléger QGIS
            # QgsProject.instance().removeMapLayer(source_layer.id())
            print(f"Succès ! Fichier sauvegardé : {path_sortie}")
        else:
            print("Erreur lors du chargement du fichier de sortie.")
