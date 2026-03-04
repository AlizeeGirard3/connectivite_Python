#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
#                 Import automatisé de couches et symbologie dans QGIS
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# Description -------------------------------------------------------------
##########################################################################-
# Fait par : Google IA,  Alizée Girard
# Affiliation :   ULaval
# Date création initiale : 2025-03-10
# Date mise à jour : 
# Pourquoi : Import automatisé de couches et symbologie dans QGIS (pour affichage 
# seulement, modifications écrasées silencieusement), toutes les couches d'un site dans projet parallèle
# Structure :
# —— connectivite
#         |—— archive
#         |—— data
#                     |—— raw
#                     |—— processed
#         |—— output
#                     |—— data
#                     |—— figures
#         |—— scripts
# SOURCES : GoogleIA (pour apprendre le Python)
# NOTES : 
# LEXIQUE :
#
##########################################################################-


 ################ VERSION STH ################-
# ============================================================================= /
# Initialisation ----
# ============================================================================= /
import glob
import os
from qgis.core import QgsProject # chargement de sous-fonctions du "package" qgis.core;
# QgsProject : "cerveau" du projet, évite de charger des miliers d'autres fonctions inutiles
from qgis.utils import iface # idem, mais iface sert à permet de "piloter" le logiciel comme avec une souris

# ============================================================================= /
# CONFIGURATION ----
# ============================================================================= /
dossier_couches = "/Users/Aliz/Desktop/QGIS/_Connectivite_PhD/Mergin/_Connectitite_PhD_Mergin_26nov24"
dossier_styles = "/Users/Aliz/Desktop/QGIS/_Connectivite_PhD/Mergin/styles"
nom_groupe = "nepasmodifier_couchesConnectivite"

# # 1. Liste des exceptions (fichiers à NE PAS charger)
# exceptions = ["PRO_point (conflicted copy, AGirard v90).shp", "PRO_repérage_zones_experimentales.shp"]
# 
# # 2. Liste de couches spécifiques (hors pattern PRO_)
couches_specifiques = ["Ecotone.restauration.zone.pt.shp"]

# # 3. Liste des fichiers à rechercher ~ [site.UID]_*.shp
prefixes = ["STH", "PRO"] # ajouter ici si autres
tous_les_fichiers = []
# 2. Boucle pour chercher chaque préfixe
for p in prefixes:
    # On crée le pattern dynamique, ex: "*STH_*.shp" puis "*PRO_*.shp"
    pattern = os.path.join(dossier_couches, f"*{p}_*.shp") # f-string (f"*{p}_*.shp"): le f devant les guillemets 
    # permet d'insérer directement la variable {p} dans la chaîne de texte. C'est très lisible et pratique pour
    # construire des noms de fichiers dynamiquement.
    
    # On ajoute les résultats à notre liste globale
    tous_les_fichiers.extend(glob.glob(pattern)) # suffixe .extend dit d'ajouter "platement" les sites à 
    # l'opposé de faire des listes de listes avec append par exemple
# ici tous les fichiers vont être nommés l'un à la suite de l'autre ainsi : 
# > tous_les_fichiers
# [1] ['/Users/Aliz/Desktop/QGIS/_Connectivite_PhD/Mergin/_Connectitite_PhD_Mergin_26nov24/STH_puits.shp', ...]

print(f"{len(tous_les_fichiers)} fichiers trouvés avec les préfixes {prefixes}")
# ancienne version : recherche d'un seul SITE.UID à la fois 
# # On prend les [site.UID]_*.shp
# tous_les_fichiers = glob.glob(os.path.join(dossier_couches, "*STH_*.shp"))

# ============================================================================= /
# Import et écrasement silencieux des couches du même nom déjà chargées ----
# ============================================================================= /
root = QgsProject.instance().layerTreeRoot()
projet = QgsProject.instance()

# Nettoyage du groupe
groupe = root.findGroup(nom_groupe)
if groupe:
    for node in groupe.findLayers():
        projet.removeMapLayer(node.layerId())
else:
    groupe = root.addGroup(nom_groupe)

fichiers_a_charger = [f for f in tous_les_fichiers if os.path.basename(f) not in exceptions]
# tous les fichiers sauf les exceptions

# On ajoute les couches spécifiques (si elles existent)
for spec in couches_specifiques:
    chemin_spec = os.path.join(dossier_couches, spec)
    if os.path.exists(chemin_spec):
        fichiers_a_charger.append(chemin_spec)

# --- CHARGEMENT, STYLE ET MISE À JOUR SÉLECTIVE AVEC SÉCURITÉ ---
for chemin in fichiers_a_charger:
    nom_base = os.path.splitext(os.path.basename(chemin))[0]
    
    # 1. VÉRIFICATION : Existe-t-il déjà une couche avec ce nom ?
    couches_existantes = QgsProject.instance().mapLayersByName(nom_base)
    
    layer_a_ignorer = False
    for couche_ancienne in couches_existantes:
        # SÉCURITÉ : Vérifier si la couche a été modifiée mais pas enregistrée
        if couche_ancienne.isModified():
            print(f"ATTENTION : {nom_base} est en cours d'édition. Mise à jour annulée pour cette couche.")
            layer_a_ignorer = True
            break # On sort de la vérification pour cette couche
        else:
            # Si pas de modifs, on peut supprimer l'ancienne version
            QgsProject.instance().removeMapLayer(couche_ancienne.id())

    # 2. CHARGEMENT (seulement si la sécurité n'a pas été déclenchée)
    if not layer_a_ignorer:
        couche = iface.addVectorLayer(chemin, nom_base, "ogr")
        
        if couche and couche.isValid():
            # 3. STYLE
            chemin_style = os.path.join(dossier_styles, f"{nom_base}.qml")
            if os.path.exists(chemin_style):
                couche.loadNamedStyle(chemin_style)
                couche.triggerRepaint()
            
            # 4. RANGEMENT DANS LE GROUPE
            noeud = root.findLayer(couche.id())
            if noeud:
                copie_noeud = noeud.clone()
                groupe.addChildNode(copie_noeud)
                root.removeChildNode(noeud)

print(f"Import terminé. {len(fichiers_a_charger)} couches traitées.")

 ################ VERSION PRO ################-
# import glob
# import os
# from qgis.core import QgsProject
# from qgis.utils import iface
# 
# # --- CONFIGURATION ---
# dossier_couches = "/Users/Aliz/Desktop/QGIS/_Connectivite_PhD/Mergin/_Connectitite_PhD_Mergin_26nov24"
# dossier_styles = "/Users/Aliz/Desktop/QGIS/_Connectivite_PhD/Mergin/styles"
# nom_groupe = "nepasmodifier_couchesConnectivite"
# 
# # 1. Liste des exceptions (fichiers PRO_ à NE PAS charger)
# exceptions = ["PRO_point (conflicted copy, AGirard v90).shp", "PRO_repérage_zones_experimentales.shp"]
# 
# # 2. Liste de couches spécifiques (hors pattern PRO_)
# couches_specifiques = ["Ecotone.restauration.zone.pt.shp"]
# # ---------------------
# root = QgsProject.instance().layerTreeRoot()
# projet = QgsProject.instance()
# 
# # Nettoyage du groupe
# groupe = root.findGroup(nom_groupe)
# if groupe:
#     for node in groupe.findLayers():
#         projet.removeMapLayer(node.layerId())
# else:
#     groupe = root.addGroup(nom_groupe)
# 
# # --- RECHERCHE DES FICHIERS ---
# On prend les [site.UID]_*.shp
# tous_les_fichiers = glob.glob(os.path.join(dossier_couches, "*PRO_*.shp"))
# 
# # On filtre les exceptions
# fichiers_a_charger = [f for f in tous_les_fichiers if os.path.basename(f) not in exceptions]
# 
# # On ajoute les couches spécifiques (si elles existent)
# for spec in couches_specifiques:
#     chemin_spec = os.path.join(dossier_couches, spec)
#     if os.path.exists(chemin_spec):
#         fichiers_a_charger.append(chemin_spec)
# 
# # --- CHARGEMENT ET STYLE ---
# for chemin in fichiers_a_charger:
#     nom_base = os.path.splitext(os.path.basename(chemin))[0]
#     
#     couche = iface.addVectorLayer(chemin, nom_base, "ogr")
#     
#     # test modification apparait dans QGIS ?
#     if couche and couche.isValid():
#         # Application du style correspondant
#         chemin_style = os.path.join(dossier_styles, f"{nom_base}.qml")
#         if os.path.exists(chemin_style):
#             couche.loadNamedStyle(chemin_style)
#             couche.triggerRepaint()
#         
#         # Rangement dans le groupe
#         noeud = root.findLayer(couche.id())
#         if noeud:
#             copie_noeud = noeud.clone()
#             groupe.addChildNode(copie_noeud)
#             root.removeChildNode(noeud)
# 
# print(f"Import terminé. {len(fichiers_a_charger)} couches traitées.")
