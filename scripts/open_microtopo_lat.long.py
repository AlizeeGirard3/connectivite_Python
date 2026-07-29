from qgis.core import QgsProject, QgsVectorLayer

# 1. Définir le chemin absolu du fichier CSV (Utilisez des slashes "/")
chemin_csv = "/Users/Aliz/Desktop/QGIS/_Connectivite_PhD/Mergin/_Connectitite_PhD_Mergin_26nov24/_microtopo_lat.long.csv"

# 2. Configurer les paramètres d'importation (URI)
# Remplacer xField et yField par les noms exacts de vos colonnes de coordonnées
# Remplacer EPSG:4326 par le code de votre système de projection (ex: EPSG:2154 pour Lambert 93)
uri = f"file:///{chemin_csv}?delimiter=;&xField=long&yField=lat&crs=EPSG:4326"

# 3. Créer la couche vectorielle
nom_couche = "_microtopo_lat.long"
couche = QgsVectorLayer(uri, nom_couche, "delimitedtext")

# 4. Vérifier si la couche est valide et l'ajouter au projet QGIS
if couche.isValid():
    QgsProject.instance().addMapLayer(couche)
    print("Couche CSV chargée avec succès !")
    
    # 5. Définir le chemin absolu du style QML et l'appliquer
    # Utilisation du chemin complet de votre session utilisateur Mac
    chemin_style = "/Users/Aliz/Desktop/QGIS/_MODÈLES/MODÈLE_microtopo.qml"
    
    # Charger le style sur la couche
    couche.loadNamedStyle(chemin_style)
    
    # Rafraîchir l'affichage et la légende dans QGIS
    couche.triggerRepaint()
    if iface:
        iface.layerTreeView().refreshLayerSymbology(couche.id())
    print("Style de microtopographie appliqué avec succès !")
    
else:
    print("Erreur : Impossible de charger la couche. Vérifiez le chemin ou les paramètres.")