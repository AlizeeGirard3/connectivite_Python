#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
#                        GET MNT MIN MAX and update style
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# Description -------------------------------------------------------------
##########################################################################-
# Fait par : Alizée Girard (forte implication de Google IA, j'apprends le Python)
# Affiliation :   ULaval
# Date création initiale : 2025-03-10
# Date mise à jour : 
# - 2026-08-07: fournir un "chemin" (Path) où chercher plutôt qu'à la racine du projet QGIS automatiquement; 
# pour ce faire, choisir les lignes à rouler (ne fonctionne pas si le script est roulé en entier)
# Pourquoi : Obtenir en un clin d'oeil les plages d'étendue d'altitude à partir du MNT
# de MRNF (2026), tirées de Données Québec
# LEXIQUE : 
# - style (en) : symbologie (fr) 
##########################################################################-

# ============================================================================= /
# Initialisation ----
# ============================================================================= /
from qgis.core import (QgsProject, QgsRasterBandStats, QgsRasterShader, 
                       QgsColorRampShader, QgsSingleBandPseudoColorRenderer, QgsStyle)

# ============================================================================= /
# Exécution ----
# ============================================================================= /
# --- 1. INITIALISATION DU STYLE ---
style = QgsStyle.defaultStyle()
base_ramp = style.colorRamp('Spectral')
base_ramp.invert() 

layers_to_style = [] # liste vide nommée layers_to_style


# CHOIX (2.i ou 2.ii) ---------------------------------------------


# --- 2.i ACCÈS AU DOSSIER SPÉCIFIQUE ---
# COMMENT/UNCOMMENT HERE (next line) ---------------------------------------------
# DOSSIER_MNT = Path("/Users/Aliz/Desktop/QGIS/DONNÉES QUÉBEC/Diffusion2/Imagerie/Produits_derives_LiDAR/22C/22C07SO")
# 
# 
# if DOSSIER_MNT.exists():
#     for chemin_fichier in DOSSIER_MNT.glob("*.tif"):
#         nom_fichier = chemin_fichier.stem
#         # On vérifie si le nom contient MNT (ou MTN)
#         if "MNT" in nom_fichier.upper() or "MTN" in nom_fichier.upper():
#             
#             # Récupère la couche si elle est déjà ouverte dans QGIS, sinon la charge
#             couches_existantes = QgsProject.instance().mapLayersByName(nom_fichier)
#             if couches_existantes:
#                 layer = couches_existantes[0]
#             else:
#                 layer = QgsRasterLayer(str(chemin_fichier), nom_fichier)
#                 if layer.isValid():
#                     QgsProject.instance().addMapLayer(layer)
#                 else:
#                     continue
#                     
#             layers_to_style.append(layer)
# COMMENT/UNCOMMENT HERE (previous line) ---------------------------------------------

            
# OU ---------------------------------------------

# --- 2.ii ACCÈS À LA HIÉRARCHIE DES DOSSIERS ---
# COMMENT/UNCOMMENT HERE (next line) ---------------------------------------------
# root = QgsProject.instance().layerTreeRoot()
# 
# def find_group_insensitive(parent, name):
#     """Cherche un groupe sans tenir compte de la casse"""
#     for child in parent.children():
#         if child.nodeType() == QgsLayerTreeNode.NodeGroup and child.name().upper() == name.upper():
#             return child
#     return None
# 
# # On descend la hiérarchie : LiDAR -> SITE.UID -> MNT
# lidar_grp = find_group_insensitive(root, "LiDAR")
# sth_grp = find_group_insensitive(lidar_grp, "PRO") if lidar_grp else None
# mnt_grp = find_group_insensitive(sth_grp, "MNT") if sth_grp else None
# 
# if mnt_grp:
#     for child in mnt_grp.children():
#         layer = child.layer()
#         # On vérifie si c'est un Raster et si le nom contient MNT (ou MTN)
#         if layer and layer.type() == QgsMapLayer.RasterLayer:
#             if "MNT" in layer.name().upper() or "MTN" in layer.name().upper():
#                 layers_to_style.append(layer)
# COMMENT/UNCOMMENT HERE (previous line) ---------------------------------------------



# POURSUIVRE CODE COMMUN ---------------------------------------------



# --- 3. CALCUL ET APPLICATION ---
if not layers_to_style:
    print("Erreur : Aucune couche raster 'MNT' trouvée dans LiDAR/PRO/MNT.")
else:
    # Calcul du Min/Max Global
    global_min = float('inf') # float() convertit l'élément (texte, entier...) en nombre à virgule
    global_max = float('-inf')
    
    print(f"Calcul des stats pour {len(layers_to_style)} couches...")
    for layer in layers_to_style:
        stats = layer.dataProvider().bandStatistics(1, QgsRasterBandStats.All, layer.extent())
        if stats.minimumValue < global_min: global_min = stats.minimumValue
        if stats.maximumValue > global_max: global_max = stats.maximumValue

    # Création des items de couleur (1m par saut)
    nb_classes = int(global_max - global_min) + 1
    color_items = []
    for i in range(nb_classes):
        val = global_min + i
        ratio = (val - global_min) / (global_max - global_min) if global_max > global_min else 0
        color = base_ramp.color(ratio)
        color_items.append(QgsColorRampShader.ColorRampItem(val, color, f"{int(val)} m"))

    # Application du style
    for layer in layers_to_style:
        shader_fcn = QgsColorRampShader()
        shader_fcn.setColorRampType(QgsColorRampShader.Interpolated)
        shader_fcn.setColorRampItemList(color_items)
        
        raster_shader = QgsRasterShader()
        raster_shader.setRasterShaderFunction(shader_fcn)
        
        renderer = QgsSingleBandPseudoColorRenderer(layer.dataProvider(), 1, raster_shader)
        renderer.setClassificationMin(global_min)
        renderer.setClassificationMax(global_max)
        
        layer.setRenderer(renderer)
        layer.setOpacity(0.8) # Règle la transparence à 80%
        layer.triggerRepaint()

    iface.layerTreeView().refreshLayerSymbology('')
    print(f"Terminé ! Global Min: {global_min:.2f}, Global Max: {global_max:.2f}")
    
