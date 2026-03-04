#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
#                                   Scale-dependant rendering
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# Description -------------------------------------------------------------
##########################################################################-
# Fait par :  GoogleIA, Alizée Girard
# Affiliation :   ULaval
# Date création initiale : 2025-02-11
# Date mise à jour : 
# Pourquoi : MISE À JOUR UNIQUE DU MODÈLE_style.hydro.standard.qml
#            lits d'écoulement ~ échelle
# SOURCES :
# NOTES : 
# LEXIQUE :
#
##########################################################################-

# ============================================================================= /
# Initialisation ----
# ============================================================================= /
import os
from qgis.core import (QgsRuleBasedRenderer, QgsSymbol, QgsProperty, 
                       QgsVectorLayerSimpleLabeling, QgsVectorLayer, 
                       QgsSymbolLayer, QgsCategorizedSymbolRenderer)


layer = iface.activeLayer()
input_qml = "/Users/Aliz/Desktop/QGIS/MODÈLE_style.hydro.standard.qml"
output_qml = "/Users/Aliz/Desktop/QGIS/MODÈLE_style.hydro.standard_V2_DYNAMIQUE.qml"

# ============================================================================= /
# EXECUTION ----
# ============================================================================= /

if not layer:
    print("Sélectionnez la couche source pour préparer le modèle.")
else:
    # 1. CHARGEMENT DU LOOK INITIAL
    layer.loadNamedStyle(input_qml)
    
    # On récupère le style visuel (couleur, etc.) du QML d'origine
    if isinstance(layer.renderer(), QgsCategorizedSymbolRenderer):
        base_symbol = layer.renderer().categories()[0].symbol().clone()
    else:
        base_symbol = layer.renderer().symbol().clone()

    # 2. CONSTRUCTION DU RENDU PAR RÈGLES (Structure intégrée)
    rules_data = [
        ('Majeur (accum > 10k)', '"accum_m2" >= 10000', 0, 0),        
        ('Moyen (accum > 1k)', '"accum_m2" >= 1000 AND "accum_m2" < 10000', 25000, 0),
        ('Détail (accum < 1k)', '"accum_m2" < 1000', 5000, 0)
    ]

    root_rule = QgsRuleBasedRenderer.Rule(None)
    new_renderer = QgsRuleBasedRenderer(root_rule)
    width_expr = 'clamp(0.2, (10000 / @map_scale) * 0.4, 0.8)'

    for label, expression, s_min, s_max in rules_data:
        symbol = base_symbol.clone()
        for sl in symbol.symbolLayers():
            sl.setDataDefinedProperty(QgsSymbolLayer.PropertyStrokeWidth, QgsProperty.fromExpression(width_expr))
        
        rule = QgsRuleBasedRenderer.Rule(symbol, label=label, filterExp=expression)
        rule.setMinimumScale(s_min)
        rule.setMaximumScale(s_max)
        new_renderer.rootRule().appendChild(rule)

    layer.setRenderer(new_renderer)

    # 3. CONFIGURATION DES ÉTIQUETTES DYNAMIQUES
    if layer.labeling():
        settings = layer.labeling().settings()
        settings.scaleVisibility = True
        settings.minimumScale = 5000 
        layer.setLabeling(QgsVectorLayerSimpleLabeling(settings))

    # 4. SAUVEGARDE DU NOUVEAU MODÈLE
    layer.saveNamedStyle(output_qml)
    print(f"Modèle intelligent sauvegardé ici : {output_qml}")

