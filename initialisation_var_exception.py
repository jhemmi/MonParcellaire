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
  Qgis,  QgsVectorLayer, QgsMessageLog,  
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
MonParcellaire_LOG="MonParcellaire"
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
DELIMITEUR_CONNUS=[',', ";", "\t"]
EXT_json=".json"
EXT_txt=".txt"
EXT_qml=".qml"
#EXT_tsv=".txt"
EXT_geojson=".geojson"

# NOM du GPKG et de ses tables 
MonParcellaire_GPKG="MonParcellaire" + EXT_gpkg
MesFondsDePlan_GPKG="MesFondsDePlan" + EXT_gpkg
GPKG_LAYERNAME = SEP_PIPE + "layername="
# Noms tables gpkg
MonParcellaire_ROU="routes"
MonParcellaire_PAR="parcelles"
MonParcellaireNomAttribut='nom'
MonParcellaireListeAttribut=['nom','tu tu','cépage', 'cadastre', "toto"]
# Autres noms
MonParcellaire_JOI="jointure"
MonParcellaire_PROJET="projet_MonParcellaire.qgs"
# REPERTOIRE SAUVEGARDE et MODELE
MonParcellaire_SAV="MonParcellaire_SAUVEGARDE" # Repertoire
#MonParcellaire_MOD="MonParcellaire_MODELE" # Repertoire des modele gpkg, projet, QML

# Attributs clé des tables
if MonParcellaire_PROD == "FR":
    ATTR_NOM_PARCELLE='name' 
    ATTR_LISTE_PARCELLE='Vignes'
    ATTR_DIRECTION='direction'
   # Préciser
else:
    #ATTR_MonParcellaire_PARCELLE='CODE_VIGNE'  # HE
    ATTR_NOM_PARCELLE='CODE_VIGNE' 
    ATTR_LISTE_PARCELLE='Vignes' 
    ATTR_DIRECTION=None
ATTR_FID='fid'

# NOMAGES FIXES
LISTE_FREQUENCE_SAUVEGARDE=[ "Chaque démarrage", "Par jour",  "Par semaine",  "Par mois"]
# Attention pas de séparateur "_" dans la liste ci dessous
#PREMIER_PREFIXES_SOLO="SOLO"
#LISTE_PREFIXES=[ "SOLO | DUO | TRIO | QUATUOR | QUINTET" , "A | B | C | D | E","Camille | Léo | Pauline | Mickael", \
#    "BERLINGO | KANGOO | C4 | MERCEDES", "NORD | SUD | EST | OUEST", \
#    "Yvette | Léa | Magda | Jean", "Pivoine | Violette | Rose | Agapanthe"]
APPLI_NOM="MonParcellaire"
APPLI_VERSION="V0.0.1"  
# Suivi des versions

# Exceptions
class MonParcellaireException( BaseException):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
# Exemple    
class MonParcellaireErreurVecteur( MonParcellaireException):
    pass
class MonParcellaireErreurData( MonParcellaireException):
    pass
class MonParcellaireErreurSaisie( MonParcellaireException):
    pass
class MonParcellairePasRepertoire( MonParcellaireException):
    pass
class MonParcellaireErreurTraitement( MonParcellaireException):
    pass
class MonParcellaireErreurMethodo( MonParcellaireException):
    pass

# Texte des messages
Verif_mon_parcellaire="Avez-vous activer la préparation de Mon Parcellaire ? Vérifiez dans l'onglet paramètre de l'extension Mon Parcellaire si le chemin est correct"
NOM_APPS_VENDANGE="CoopViti"
Verif_apps_vendanges="Ce fichier ~MonParcellaire/jointure.csv a été crée par votre application {0}.".format( NOM_APPS_VENDANGE)
Verif_apps_repertoire = Verif_apps_vendanges + " Vérifier si il se trouve dans le bon répertoire ?"
NOM_SIG_VENDANGE="QGIS Projet Référentiel Mon Tom"
Verif_sig_vendanges="sous {0}, vous pouvez rajouter la(es) parcelle(s) manquante(s) dans le référentiel GPKG parcelles".format( NOM_SIG_VENDANGE)
Verif_vecteur_destination="Vérifier les propriétes du vecteur dans le GPKG MonParcellaire"
Maintenance="Contacter la maintenance jhemmi.eu"
Maintenance_GPKG="{0}, en fournissant votre GPKG de référence ~MonParcellaire/MonParcellaire.gpkg.".format(Maintenance)
Maintenance_STYLE="{0}, en fournissant une liste répertoire ~MonParcellaire/MonParcellaire_STYLES_SELECTION.".format(Maintenance)
Pas_verif_mais_maintenance=Maintenance_GPKG + \
    "En cas d'urgence, vous pouvez sortir de QGIS, sauver le GPKG ~MonParcellaire/MonParcellaire.gpkg pour l'envoyer à jhemmi.eu, \
        recréer votre référentiel GPKG à partir de la dernière sauvegarde présente dans ~MonParcellaire/MonParcellaire_SAUVEGARDE "
Yourself="Modifiez votre saisie et relancer le découpage"
# REPERTOIRE
def erreur_repertoire( CHEMIN_REP, correction=Verif_mon_parcellaire):
    aText="Nom de répertoire {0} n'existe pas".format( CHEMIN_REP)
    raise MonParcellairePasRepertoire( "{0} || CORRECTION : {1}".format(aText, correction))
# FICHIER    
def erreur_gpkg( CHEMIN_REP,  NOM_GPKG, correction=Verif_mon_parcellaire):
    aText="Pas de GPKG à traiter - nom de gpkg {0} - répertoire recherché {1})".format(NOM_GPKG, CHEMIN_REP)
    raise MonParcellairePasRepertoire( "{0} || CORRECTION : {1} si il est correct contacter jhemmi.eu".format(aText, correction))
def erreur_jointures( CHEMIN_REP,  NOM_JOINTURE, correction=Pas_verif_mais_maintenance):
    aText="Pas de parcelles en correspondance à point d'accés - nom jointure finale {0}".format(NOM_JOINTURE)
    raise MonParcellaireErreurData( "{0} || CORRECTION : {1}".format(aText, correction))
def erreur_vecteur( CHEMIN_REP,  NOM_VECTEUR, correction=Verif_mon_parcellaire):
    aText="Pas de vecteur à traiter - nom du vecteur {0} - répertoire recherché {1}".format(NOM_VECTEUR, CHEMIN_REP)
    raise MonParcellairePasRepertoire( "{0} || CORRECTION : {1} si il est correct contacter jhemmi.eu".format(aText, correction))
def erreur_ecrire_vecteur( aText, correction=Maintenance):
    raise MonParcellaireErreurData( "{0} || CORRECTION : {1}".format(aText, correction))

def erreur_style( CHEMIN_REP,  NOM_STYLE, correction=Maintenance_STYLE):
    aText="Pas de style pour la couche {0} - répertoire recherché {1}".format(NOM_STYLE, CHEMIN_REP)
    raise MonParcellairePasRepertoire( "{0} || CORRECTION : {1}".format(aText, correction))
# TSV
def erreur_table( CHEMIN_REP,  fichier, correction=Verif_apps_repertoire):
    aText="La table {0} n'existe pas dans ce répertoire {1}".format( fichier, CHEMIN_REP, NOM_APPS_VENDANGE)
    raise MonParcellaireErreurData( "{0} || CORRECTION : {1}".format(aText, correction))
#Traitement/Processing
def erreur_alg_traitement( NOM_ALGO, NOM_LIB, correction=Maintenance):
    aText="L'algorithme {0} n'est pas disponible. Vérifier que Traitement est bien activé puis vérifier dans le paramétrage de Traitement que le fournisseur {1}".format(NOM_ALGO, NOM_LIB) + \
        " est bien activé"
    raise MonParcellaireErreurMethodo( "{0} || CORRECTION : {1}".format(aText, correction + " en précisant les noms du fournisseur et de l'algo problématiques"))
def erreur_traitement( NOM_ALGO, correction=Pas_verif_mais_maintenance):
    aText="L'algorithme {0} n'a pas pu s'exécuter correctement. Vérifier le message d'erreur dans le journal des messages (onglet Traitement)".\
        format(NOM_ALGO)
    raise MonParcellaireErreurMethodo( "{0} || CORRECTION : {1}".format(aText, correction + " en fournissant votre GPKG et le nom de l'algo problématique"))
def erreur_import( module, correction=Pas_verif_mais_maintenance):
    aText="L'import de {0} n'est pas disponible.".format(module)
    raise MonParcellaireErreurMethodo( "{0} || CORRECTION : {1}".format(aText, correction))
def erreur_fermer_projet_QGIS( libelle_traitement, correction="Fermez le projet sans quitter QGIS3 qui reste nécessaire pour activer ce traitement"):
    aText="Le traitement de {0} préfére qu'aucun projet QGIS ({1}) ne soit ouvert.".format( libelle_traitement,  "nom_projet")
    MonConseil = "{0} || CORRECTION : {1}".format(aText, correction)
    raise MonParcellaireErreurMethodo( MonConseil)

def my_print( aText, level = "Sans_niveau", vers_ou = T_LOG, dialog=None, PREFIX="MonParcellaire"):
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
            


def ouvre_vecteur( Repertoire, Nom_vecteur, Libelle, mon_dialogue=None, Extension=EXT_geojson):
    """ Ouvre le vecteur, vérifie sa validité
    Rend le vecteur et son nom
    """
    # Retrouve nom
    chemin_complet = nommage_vecteur( Repertoire, Nom_vecteur, Extension)
    vecteur = QgsVectorLayer( chemin_complet, Nom_vecteur, "ogr") 
    if not vecteur.isValid():
        aText="Vecteur {0} non valide ...".format(Libelle)
        if mon_dialogue != None:
            my_print( aText, T_ERR, T_BAR, mon_dialogue)
        else: # vers LOG
            my_print( aText, T_ERR)
        erreur_vecteur( Repertoire,  Nom_vecteur)
    return vecteur, chemin_complet
        
    
def ouvre_gpkg( Repertoire, Nom_vecteur, Libelle, Nom_gpkg=MonParcellaire_GPKG, mon_dialogue=None):
    """ Ouvre le vecteur dans son gpkg, vérifie sa validité
    Rend le vecteur QGIS et son nom
    """
    # Retrouve nom du vecteur dans gpkg
    _, _, chemin_complet = nommages_gpkg( Repertoire, Nom_vecteur, Nom_gpkg)
    #my_print( "Chemin du vecteur GPKG".format( chemin_complet),  T_INF)
    vecteur = QgsVectorLayer( chemin_complet, Nom_vecteur, "ogr")  
    if not vecteur.isValid():
        aText="Vecteur {0} non valide ...".format(Libelle)
        if mon_dialogue != None:
            my_print( aText, T_ERR, T_BAR, mon_dialogue)
        else: # vers LOG
            my_print( aText, T_ERR)
        erreur_gpkg( Repertoire,  Nom_vecteur)
    return vecteur, chemin_complet

