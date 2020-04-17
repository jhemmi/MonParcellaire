# -*- coding: utf-8 -*-
# 
"""/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
#import os
# import sys
from qgis.core import (
  Qgis, QgsMessageLog,  #QgsVectorLayer
)
#import glob
#import subprocess

# TRACES Selon le mode test ou prod
MonParcellaire_PROD="TEST" # HE ou TEST
MonParcellaire_TIMESTAMP="NO"
if MonParcellaire_PROD in [ "TEST",  "HE"]: #, "HE", "FR"]:
    MonParcellaire_TRACE="YES"
else:
    MonParcellaire_TRACE="NO"
    
MonParcellaire_EPSG="32631" # faire un dict ou L93
# Nom des flags accompagnant les messages
APPLI_NOM="MonParcellaire"
APPLI_VERSION="V1.2.5"  
# Suivi des versions dans metadata.txt

MonParcellaire_LOG=APPLI_NOM
T_INF="Information"
T_ERR="Erreur"
T_OK="Succes"
T_WAR="Attention"
T_BAR="BAR"
T_LOG="LOG"

# Unicode
U_TOM           ="𝝉"
E_ZIP           ="🗜️"
E_REP           ="📂"
E_TARGET        ="🎯"
E_TRAJET        ="🛣️"
E_OK            ="✔️"
U_WARNING       =u"\u26A0" #.encode("UTF-8") 
E_WARNING       ="⚠️"
U_INFO          =u"\u2139"  
U_STOP          =u"\U0001F6AB"
E_STOP          ="🔥" 
E_INTERDIT      ="🛑"
E_CLAP          ="🎬"
E_PANDA         ="🐼"
E_PETALE        ="🥀"
E_FLEUR         ="🌼"

# SEPARATEUR
SEP_U="_"
SEP_T="-"
SEP_P="."
SEP_V=","
SEP_PIPE="|"
SEP_VIRGULE=SEP_V
SEP_BLANC=" " 
SEP_COTE="'"  # Attention dans nom parcelles 
SEP_TIRET=SEP_T
SEP_DATE=SEP_T # ou "/" pour Zoho
SEP_TILDE="~"
SEP_CONFIG=SEP_PIPE+SEP_PIPE+SEP_TILDE+SEP_PIPE+SEP_PIPE
# Extensions
EXT_gpkg=".gpkg"
EXT_zip=".zip"
EXT_csv=".csv"
EXT_txt=".txt"
EXT_tsv=".tsv"
DELIMITEURS_CONNUS=[';', ",", "\t"]
EXTENSIONS_CONNUES=[EXT_txt, EXT_csv, EXT_tsv]
EXT_json=".json"
EXT_qml=".qml"
EXT_xml=".xml"
EXT_geojson=".geojson"

# NOM du GPKG et de ses tables 
MonParcellaire_GPKG=APPLI_NOM + EXT_gpkg
MesFondsDePlan_GPKG="MesFondsDePlan" + EXT_gpkg
GPKG_LAYERNAME = SEP_PIPE + "layername="
# Noms tables gpkg
MonParcellaire_ROU="routes"
MonParcellaire_PAR="parcelles"
MonParcellaireNomAttribut='nom'
# Autres noms
MonParcellaire_JOI="jointure"
MonParcellaire_PROJET=APPLI_NOM+".qgz"
# REPERTOIRE SAUVEGARDE et MODELE
MonParcellaire_SAV=APPLI_NOM+"_SAUVEGARDE" # Repertoire

# NOMAGES FIXES
LISTE_FREQUENCE_SAUVEGARDE=[ "Chaque démarrage", "Par jour",  "Par semaine",  "Par mois"]

# Exceptions
class MonParcellaireException( BaseException):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
# Exemple    

class MonParcellaireErreurData( MonParcellaireException):
    pass
class MonParcellairePasRepertoire( MonParcellaireException):
    pass
class MonParcellaireErreurMethodo( MonParcellaireException):
    pass

# Texte des messages
NOM_APPS_VENDANGE="CoopViti"
NOM_SIG_VENDANGE="QGIS Projet Référentiel Mon Tom"
VerificationReferentielMonParcellaire="Avez-vous paramétré le chemin vers le référentiel Mon Parcellaire ? \
    Vérifiez dans l'onglet paramètre de l'extension Mon Parcellaire si le chemin est correct"
Maintenance="Contacter la maintenance jhemmi.eu"
Maintenance_GPKG="{0}, en fournissant votre GPKG de référence ~MonParcellaire/MonParcellaire.gpkg.".format(Maintenance)
VerificationVersionQGIS="Votre version de QGIS n'inclut pas ce module. Sous Windows, utilisez \
    QGIS 3.10.0 ou 3.12.0 qui contiennent ce module."
Pas_verif_mais_maintenance=Maintenance_GPKG + \
    "En cas d'urgence, vous pouvez sortir de QGIS, sauver le GPKG ~MonParcellaire/MonParcellaire.gpkg pour l'envoyer à jhemmi.eu, \
        recréer votre référentiel GPKG à partir de la dernière sauvegarde présente dans ~MonParcellaire/MonParcellaire_SAUVEGARDE "

# REPERTOIRE
def erreurRepertoire( CHEMIN_REP, correction=VerificationReferentielMonParcellaire):
    aText="Nom de répertoire {0} n'existe pas".format( CHEMIN_REP)
    raise MonParcellairePasRepertoire( "{0} || CORRECTION : {1}".format(aText, correction))
# FICHIER    
def erreurGPKG( CHEMIN_REP, NOM_GPKG, correction=VerificationReferentielMonParcellaire):
    aText="Pas de GPKG à traiter - nom de gpkg {0} - répertoire recherché {1})".format(NOM_GPKG, CHEMIN_REP)
    raise MonParcellairePasRepertoire( "{0} || CORRECTION : {1} si il est correct contacter jhemmi.eu".format(aText, correction))
def erreurJointures( CHEMIN_REP,  NOM_JOINTURE, LISTE_EXTENSIONS, correction=VerificationReferentielMonParcellaire):
    aText="Pas de jointure {0} avec une des extensions {1}".format(NOM_JOINTURE, LISTE_EXTENSIONS)
    raise MonParcellaireErreurData( "{0} || CORRECTION : {1}".format(aText, correction))
def erreurVecteur( CHEMIN_REP,  NOM_VECTEUR, correction=VerificationReferentielMonParcellaire):
    aText="Pas de vecteur {0} dans le répertoire recherché {1}".format(NOM_VECTEUR, CHEMIN_REP)
    raise MonParcellairePasRepertoire( "{0} || CORRECTION : {1} si il est correct contacter jhemmi.eu".format(aText, correction))
#def erreur_ecrire_vecteur( aText, correction=Maintenance):
#    raise MonParcellaireErreurData( "{0} || CORRECTION : {1}".format(aText, correction))

#Traitement/Processing
#def erreur_alg_traitement( NOM_ALGO, NOM_LIB, correction=Maintenance):
#    aText="L'algorithme {0} n'est pas disponible. Vérifier que Traitement est bien activé puis vérifier dans le paramétrage de Traitement que le fournisseur {1}".format(NOM_ALGO, NOM_LIB) + \
#        " est bien activé"
#    raise MonParcellaireErreurMethodo( "{0} || CORRECTION : {1}".format(aText, correction + " en précisant les noms du fournisseur et de l'algo problématiques"))
#def erreur_traitement( NOM_ALGO, correction=Pas_verif_mais_maintenance):
#    aText="L'algorithme {0} n'a pas pu s'exécuter correctement. Vérifier le message d'erreur dans le journal des messages (onglet Traitement)".\
#        format(NOM_ALGO)
#    raise MonParcellaireErreurMethodo( "{0} || CORRECTION : {1}".format(aText, correction + " en fournissant votre GPKG et le nom de l'algo problématique"))
def erreurImportPandas( module, correction=VerificationVersionQGIS):
    aText="Le module {0} n'est pas présent ou actif dans QGIS.".format(module)
    monPrint( "{0} || CORRECTION : {1}".format(aText, correction))
    return
def erreurImport( module, correction=Maintenance):
    aText="Le module {0} n'est pas présent ou actif dans QGIS. Reprendre le document d'installation".format(module)
    raise MonParcellaireErreurMethodo( "{0} || Si vous restez sans solution : {1}".format(aText, correction))
#def erreur_fermer_projet_QGIS( libelle_traitement, correction="Fermez le projet sans quitter QGIS3 qui reste nécessaire pour activer ce traitement"):
#    aText="Le traitement de {0} préfére qu'aucun projet QGIS ({1}) ne soit ouvert.".format( libelle_traitement,  "nom_projet")
#    MonConseil = "{0} || CORRECTION : {1}".format(aText, correction)
#    raise MonParcellaireErreurMethodo( MonConseil)

def monPrint( aText, level = "Sans_niveau", vers_ou = T_LOG, dialog=None, PREFIX="MonParcellaire"):
    """ Mon print part vers LOG, il decore selon le level (prefixe, emoi et mis en correspondance avec gravité) 
        entete et pied pour encadrement
        en Option il peut aller vers BAR (log aussi) ou sortie STANDARD"""

    if MonParcellaire_TRACE == "NO" and level == "Sans_niveau":
        return # Pas de trace et petit level
    chaine = ""
    gravite=Qgis.Info
    if level == "Sans_niveau":
        # Quand pas de niveau, on ne fait pas de retour ligne par defaut
        chaine = "{0}".format( aText)
    elif level == T_INF:
        chaine = "{0} {1}: {2}".format( PREFIX, U_INFO, aText)
        gravite=Qgis.Info
    elif level == T_WAR:
        chaine = "{0} {1}: {2}".format( PREFIX, E_WARNING, aText)
        gravite=Qgis.Warning
    elif level == T_ERR:   
        chaine = "{0} {1}: {2}".format( PREFIX, E_INTERDIT, aText)
        gravite=Qgis.Critical
    elif level == T_OK:   
        chaine = "{0} {1}: {2}".format( PREFIX, E_OK, aText)
        gravite=Qgis.Success
    else:
        chaine=""
        
    # Communication
    if chaine !="":
        if vers_ou == T_LOG:
            QgsMessageLog.logMessage( chaine, MonParcellaire_LOG, gravite)
        elif vers_ou == T_BAR:
            if dialog != None:
                dialog.bar.pushMessage( chaine, gravite, 15)
            else:
                QgsMessageLog.logMessage( "Inconsistance : impossible de trouver le dialogue pour accéder la barre", MonParcellaire_LOG, Qgis.Warning)
                QgsMessageLog.logMessage( chaine, MonParcellaire_LOG, gravite)
        else:
            print( chaine)
            
