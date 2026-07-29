# SCRIPT DYSFONCTIONNEL À RÉPARER (TYPE DE DONNÉES DES COLONNES)

from qgis.core import QgsField
from qgis.PyQt.QtCore import QVariant

# 1. Sélectionner la couche active dans QGIS
layer = iface.activeLayer()

# 2. Définir les nouvelles colonnes avec leur nom et leur type de données
# Types communs : QVariant.Int (Entier), QVariant.Double (Décimal),
# QVariant.String (Texte)
new_fields = [
    QgsField("lat", QVariant.String),
    QgsField("long", QVariant.String),
    QgsField("site.uid", QVariant.String),
    QgsField("well.uid", QVariant.String),
    QgsField("trmnt.uid", QVariant.String),
    QgsField("probe.uid", QVariant.String),
    QgsField("Note", QVariant.String)
]

# 3. Ajouter les colonnes via le dataProvider
if layer.dataProvider().capabilities() & layer.dataProvider().AddAttributes:
    # Ajouter la liste des champs d'un coup
    layer.dataProvider().addAttributes(new_fields)

    # Étape obligatoire pour rafraîchir la table d'attributs dans l'interface
    layer.updateFields()
    print("Colonnes créées avec succès !")
else:
    print("Cette couche ne permet pas l'ajout d'attributs.")
