#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
#                        GET MNT MIN MAX and update style
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# Description -------------------------------------------------------------
##########################################################################-
# Fait par : Alizée Girard
# Affiliation :   ULaval
# Date création initiale : 2025-03-10
# Date mise à jour : 
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
# # 1. Accéder au projet et au style par défaut de QGIS
# project = QgsProject.instance()
# style = QgsStyle.defaultStyle()
# # Vous pouvez changer 'Spectral' par 'Viridis', 'Magma', 'Terrain', etc.
# base_ramp = style.colorRamp('Spectral') 
# base_ramp.invert() # Optionnel : Inverser pour avoir le rouge en haute altitude
# 
# count = 0
# 
# # 2. Boucle sur toutes les couches du projet
# for layer in project.mapLayers().values():
#   # On vérifie si c'est un Raster ET si "MNT" est dans le nom
#     if layer.type() == QgsMapLayer.RasterLayer and "MNT" in layer.name().upper():
#         provider = layer.dataProvider() # Sans le dataProvider(), QGIS saurait qu'une couche existe dans la légende, 
#         # mais il ne pourrait pas "voir" ce qu'il y a dedans.
#         band = 1
#         
#         # 1. Stats
#         stats = provider.bandStatistics(1, QgsRasterBandStats.All, layer.extent())
#         v_min, v_max = stats.minimumValue, stats.maximumValue
#         nb_classes = int(v_max - v_min) + 1
#         
#              # 2. Créer la liste des items de couleur manuellement (Plus robuste)
#         color_items = []
#         for i in range(nb_classes):
#             val = v_min + i
#             # Calcul du ratio (0.0 à 1.0) pour la couleur
#             ratio = (val - v_min) / (v_max - v_min) if v_max > v_min else 0
#             color = base_ramp.color(ratio)
#             color_items.append(QgsColorRampShader.ColorRampItem(val, color, f"{int(val)} m"))
#             
#             # On utilise la méthode la plus stable pour la rampe
#             shader_fcn = QgsColorRampShader()
#             shader_fcn.setColorRampType(QgsColorRampShader.Interpolated)
#             shader_fcn.setColorRampItemList(color_items) # <--- On injecte la liste directement
#             raster_shader = QgsRasterShader()
#             raster_shader.setRasterShaderFunction(shader_fcn)
#             # 3. Renderer
#             renderer = QgsSingleBandPseudoColorRenderer(provider, 1, raster_shader)
#             layer.setRenderer(renderer)
#             layer.triggerRepaint()
#             
#             count += 1
#             print(f"Mise à jour : {layer.name()} | Min: {v_min:.2f} | Max: {v_max:.2f}")
#         
#         # 4. Rafraîchir la légende
#         iface.layerTreeView().refreshLayerSymbology('')
#         print(f"Terminé : {count} couches MNT mises à jour.")



from qgis.core import (QgsProject, QgsRasterBandStats, QgsRasterShader, 
                       QgsColorRampShader, QgsSingleBandPseudoColorRenderer, 
                       QgsStyle, QgsColorRamp)

# --- 1. INITIALISATION DU STYLE ---
style = QgsStyle.defaultStyle()
base_ramp = style.colorRamp('Spectral')
base_ramp.invert() 

# --- 2. ACCÈS À LA HIÉRARCHIE DES DOSSIERS ---
root = QgsProject.instance().layerTreeRoot()

def find_group_insensitive(parent, name):
    """Cherche un groupe sans tenir compte de la casse"""
    for child in parent.children():
        if child.nodeType() == QgsLayerTreeNode.NodeGroup and child.name().upper() == name.upper():
            return child
    return None

# On descend la hiérarchie : LiDAR -> STH -> MNT
lidar_grp = find_group_insensitive(root, "LiDAR")
sth_grp = find_group_insensitive(lidar_grp, "PRO") if lidar_grp else None
mnt_grp = find_group_insensitive(sth_grp, "MNT") if sth_grp else None

layers_to_style = []

if mnt_grp:
    for child in mnt_grp.children():
        layer = child.layer()
        # On vérifie si c'est un Raster et si le nom contient MNT (ou MTN)
        if layer and layer.type() == QgsMapLayer.RasterLayer:
            if "MNT" in layer.name().upper() or "MTN" in layer.name().upper():
                layers_to_style.append(layer)

# --- 3. CALCUL ET APPLICATION ---
if not layers_to_style:
    print("Erreur : Aucune couche raster 'MNT' trouvée dans LiDAR/PRO/MNT.")
else:
    # Calcul du Min/Max Global
    global_min = float('inf')
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
        layer.setOpacity(0.8) # Règle la transparence à 50%
        layer.triggerRepaint()

    iface.layerTreeView().refreshLayerSymbology('')
    print(f"Terminé ! Global Min: {global_min:.2f}, Global Max: {global_max:.2f}")
    
