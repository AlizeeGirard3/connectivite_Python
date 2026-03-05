#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
#                                 GET MNT MIN MAX
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# Description -------------------------------------------------------------
##########################################################################-
# Fait par : Alizée Girard
# Affiliation :   ULaval
# Date création initiale : 2025-03-10
# Date mise à jour : 
# Pourquoi : Obtenir en un clin d'oeil les plages d'étendue d'altitude à partir du MNT
# de MRNF (2026), tirées de Données Québec
##########################################################################-


# ============================================================================= /
# Initialisation ----
from qgis.core import (QgsProject, QgsRasterBandStats, QgsRasterShader, 
                       QgsColorRampShader, QgsSingleBandPseudoColorRenderer, QgsStyle)
# ============================================================================= /

# 1. Accéder au projet et au style par défaut de QGIS
project = QgsProject.instance()
style = QgsStyle.defaultStyle()
# Vous pouvez changer 'Spectral' par 'Viridis', 'Magma', 'Terrain', etc.
base_ramp = style.colorRamp('Spectral') 
base_ramp.invert() # Optionnel : Inverser pour avoir le rouge en haut

count = 0

# 2. Boucle sur toutes les couches du projet
for layer in project.mapLayers().values():
  # On vérifie si c'est un Raster ET si "MNT" est dans le nom
  if layer.type() == QgsMapLayer.RasterLayer and "MNT" in layer.name():
  provider = layer.dataProvider()
band = 1

# Calcul des statistiques réelles (Min/Max) sur toute l'étendue
stats = provider.bandStatistics(band, QgsRasterBandStats.All, layer.extent())
v_min = stats.minimumValue
v_max = stats.maximumValue

# Configuration du Shader (dégradé)
shader_fcn = QgsColorRampShader()
shader_fcn.setColorRampType(QgsColorRampShader.Interpolated)
shader_fcn.setClassificationMode(QgsColorRampShader.Continuous)

# Générer 5 classes automatiques entre le min et le max
shader_fcn.classifyColorRamp(5, band, layer.extent(), base_ramp)

raster_shader = QgsRasterShader()
raster_shader.setRasterShaderFunction(shader_fcn)

# Création et application du rendu
renderer = QgsSingleBandPseudoColorRenderer(provider, band, raster_shader)
renderer.setClassificationMin(v_min)
renderer.setClassificationMax(v_max)

layer.setRenderer(renderer)
layer.triggerRepaint()

count += 1
print(f"Mise à jour : {layer.name()} | Min: {v_min:.2f} | Max: {v_max:.2f}")

# 3. Rafraîchir la légende
iface.layerTreeView().refreshLayerSymbology('')
print(f"Terminé : {count} couches MNT mises à jour.")
