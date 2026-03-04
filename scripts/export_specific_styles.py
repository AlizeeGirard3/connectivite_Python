#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
#                 Export automatisé de symbologies de couches QGIS
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# Description -------------------------------------------------------------
##########################################################################-
# Fait par : Google IA,  Alizée Girard
# Affiliation :   ULaval
# Date création initiale : 2025-03-10
# Date mise à jour : 
# Pourquoi : mettre à jour et référer à cette symbologie automatiquement à l'import de 
# couches dans d'autres projets #
##########################################################################-


 ################ VERSION STH ################-
# ============================================================================= /
# Initialisation ----
# ============================================================================= /
import os
from qgis.core import QgsProject

# ============================================================================= /
# Configuration ----
# ============================================================================= /
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
    # 1. Soit elle contient "STH_" ET c'est un .shp
    # 2. Soit c'est exactement le nom de ta couche spécifique
    if ("STH_" in nom_couche and source.lower().endswith(".shp")) or (nom_couche == couche_specifique):
        
        # On enregistre le style avec le nom exact de la couche
        chemin_qml = os.path.join(dossier_styles, f"{nom_couche}.qml")
        layer.saveNamedStyle(chemin_qml)
        print(f"Style exporté pour : {nom_couche}")
        counter += 1

print(f"Exportation terminée : {counter} styles générés dans {dossier_styles}")


#  ################ VERSION PRO ################-
# import os
# from qgis.core import QgsProject
# 
# # Dossier où enregistrer les styles
# dossier_styles = "/Users/Aliz/Desktop/QGIS/_Connectivite_PhD/Mergin/styles"
# if not os.path.exists(dossier_styles):
#     os.makedirs(dossier_styles)
# 
# # Nom exact de ta couche spécifique
# couche_specifique = "Ecotone.restauration.zone.pt"
# 
# counter = 0
# for layer in QgsProject.instance().mapLayers().values():
#     source = layer.source()
#     nom_couche = layer.name()
#     
#     # CONDITION : 
#     # 1. Soit elle contient "PRO_" ET c'est un .shp
#     # 2. Soit c'est exactement le nom de ta couche spécifique
#     if ("PRO_" in nom_couche and source.lower().endswith(".shp")) or (nom_couche == couche_specifique):
#         
#         # On enregistre le style avec le nom exact de la couche
#         chemin_qml = os.path.join(dossier_styles, f"{nom_couche}.qml")
#         layer.saveNamedStyle(chemin_qml)
#         print(f"Style exporté pour : {nom_couche}")
#         counter += 1
# 
# print(f"Exportation terminée : {counter} styles générés dans {dossier_styles}")
