#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
#                                   Scale-dependant rendering
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# Description -------------------------------------------------------------
##########################################################################-
# Fait par :  GoogleIA, Alizée Girard
# Affiliation :   ULaval
# Date création initiale : 2025-02-11
# Date mise à jour : 
# Pourquoi : 1ier essai -> courbes de niveau ~ échelle
# SOURCES : moi-même
# NOTES : 
# LEXIQUE :
#
##########################################################################-

# ============================================================================= /
# Initialisation ----
# ============================================================================= /
from qgis.core import (QgsRuleBasedRenderer, QgsSymbol, QgsProperty, 
                       QgsPalLayerSettings, QgsVectorLayerSimpleLabeling, 
                       QgsVectorLayer, QgsProject, QgsSymbolLayer)
from PyQt5.QtGui import QColor

# ============================================================================= /
# Exécution ----
# ============================================================================= /
layer = iface.activeLayer() # travaille sur la couche actuellement sélectionnée

# path_qml = "/Users/Aliz/Desktop/QGIS/MODÈLE étiquette.qml"
path_qml = "/Users/Aliz/Desktop/QGIS/MODÈLE_style.hydro.standard.qml"

if not layer:
    print("Sélectionnez une couche !")
else:
    # 1. DÉFINITION DES RÈGLES (Structure)
    # (Label, Filtre SQL, Couleur, Échelle Dézoom, Échelle Zoom)
    # Rappel : 25000 = disparaît au-delà de 1:25000. 0 = visible tout le temps.
    rules_data = [
    ('Maîtresses (10m)', '"ELEVATION" % 10 = 0', 'gold', 0, 0), # Épaisseur gérée par expression
    ('Secondaires (1m)', '"ELEVATION" % 1 = 0 AND "ELEVATION" % 10 != 0', 'lemonchiffon', 25000, 0)
    ]

    # Création du moteur de rendu par règles
    root_rule = QgsRuleBasedRenderer.Rule(None)
    renderer = QgsRuleBasedRenderer(root_rule)
    
    # Expression pour l'épaisseur dynamique (affine au dézoom)
    width_expr = 'clamp(0.2, (10000 / @map_scale) * 0.4, 0.8)'

    for label, expression, color, s_min, s_max in rules_data:
        symbol = QgsSymbol.defaultSymbol(layer.geometryType())
        symbol.setColor(QColor(color))
        
        # Appliquer l'épaisseur dynamique
        symbol.symbolLayer(0).setDataDefinedProperty(
            QgsSymbolLayer.PropertyStrokeWidth, 
            QgsProperty.fromExpression(width_expr)
        )
        
        rule = QgsRuleBasedRenderer.Rule(symbol, label=label, filterExp=expression)
        rule.setMinimumScale(s_min)
        rule.setMaximumScale(s_max)
        renderer.rootRule().appendChild(rule)

    layer.setRenderer(renderer)

    # 2. APPLICATION DU MODÈLE .QML (Pour les étiquettes)
    # On charge le QML temporairement sur une couche "fantôme" pour extraire le style de texte
    temp_layer = QgsVectorLayer("LineString?crs=" + layer.crs().authid(), "temp", "memory")
    temp_layer.loadNamedStyle(path_qml)
    
    if temp_layer.labeling():
        # On récupère les réglages de police/style du QML
        label_settings = temp_layer.labeling().settings()
        # On force nos propres règles de zoom sur ces étiquettes
        label_settings.fieldName = "ELEVATION"
        label_settings.scaleVisibility = True
        label_settings.minimumScale = 10000 # Apparaît seulement sous 1:10 000
        label_settings.maximumScale = 0
        
        layer.setLabeling(QgsVectorLayerSimpleLabeling(label_settings))
        layer.setLabelsEnabled(True)

    # 3. RAFRAÎCHISSEMENT
    layer.triggerRepaint()
    iface.layerTreeView().refreshLayerSymbology(layer.id())
    print("Courbes générées et style d'étiquette appliqué !")


