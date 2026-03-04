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
# if not os.path.exists(dossier_styles):
#     os.makedirs(dossier_styles)

prefixes = ["STH", "PRO"]
couche_specifique = [] #"Ecotone.restauration.zone.pt"

counter = 0 # compter le nombre de couches visées au fil du script

# ============================================================================= /
# Exécution ----
# ============================================================================= /
for layer in QgsProject.instance().mapLayers().values():
    nom_couche = layer.name()
    
    # 0 correspond aux couches vectorielles (SHP, GPKG, etc.)
    # Cela remplace la ligne qui causait l'erreur
    est_vecteur = (layer.type() == 0)
    
    if not est_vecteur:
        continue # On passe à la couche suivante si ce n'est pas du vecteur

    a_exporter = False
    
    # 1. Test des préfixes (STH, PRO)
    if any(f"{p}_" in nom_couche for p in prefixes):
        a_exporter = True
        
    # 2. Test de la liste spécifique
    if not a_exporter and nom_couche in couches_specifiques:
        a_exporter = True

    # 3. EXPORTATION
    if a_exporter:
        chemin_qml = os.path.join(dossier_styles, f"{nom_couche}.qml")
        layer.saveNamedStyle(chemin_qml)
        print(f"Style exporté : {nom_couche}")
        counter += 1

print(f"Terminé : {counter} styles générés.")
    
