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

from qgis.core import ( Qgis, QgsMessageLog )
# La suite des import est en fin de ce module

# TRACES Selon le mode test ou prod
MonParcellaire_PROD="TERMINAL" # HE ou TEST
MonParcellaire_TIMESTAMP="NO"
if MonParcellaire_PROD in [ "TEST",  "HE"]: #, "HE", "FR"]:
    MonParcellaire_TRACE="YES"
elif MonParcellaire_PROD=="TERMINAL":
    MonParcellaire_TRACE="TERMINAL"
else:
    MonParcellaire_TRACE="NO"
#MonParcellaire_EPSG="2154" # faire un dict ou L93
# Nom des flags accompagnant les messages
APPLI_NOM="MonParcellaire"
APPLI_VERSION="V2.0"  
APPLI_NOM_VERSION=APPLI_NOM + " (" +  APPLI_VERSION + ")"
# Suivi des versions dans metadata.txt

# EPSG pour pyProj ou QGIS
ID_SOURCE_CRS      =4326
SUFFIXE_SOURCE_CRS ="_WGS84"
ID_DESTINATION_CRS =2154
SUFFIXE_DESTINATION_CRS ="_L93"

MonParcellaire_LOG=APPLI_NOM
T_INF="Information"
T_ERR="Erreur"
T_OK ="Succes"
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
E_PANDAS        ="🐼"
U_LIGNE         ="│"
U_BRISE         ="〰️"
U_LIGNE_TOURNANTE =u"\u21BA"
U_CISEAUX       ="✂️"
E_FLEUR         ="🌼"
E_RANG_EN_COURS ="⬆️"
E_REGROUPEMENT  ="🔃"
E_RANG_MODELE   ="📍"
E_RANG_NEW      ="⭐"
E_CENTIPEDE     ="🐜"
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
EXT_qgz=".qgz"
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
#DRIVER_GEOJSON="GeoJSON" # Ecrire un geojson depuis geopanda
EXT_pos=".pos"
PREFIXE_pos="solution1_"

# NOM du GPKG et de ses tables 
MonParcellaire_GPKG=APPLI_NOM + EXT_gpkg
MesFondsDePlan_GPKG="MesFondsDePlan" + EXT_gpkg
MesIAE_GPKG="MesIAE" + EXT_gpkg
GPKG_LAYERNAME = SEP_PIPE + "layername="
# Noms tables gpkg
MonParcellaire_ROU="routes"
MonParcellaire_PAR="parcelles"
MonParcellaireNomAttribut='nom'
# Autres noms
MonParcellaire_JOI="jointure" # EN join between
MonParcellaire_PROJET=APPLI_NOM+EXT_qgz
# REPERTOIRE SAUVEGARDE et MODELE
MonParcellaire_SAV=APPLI_NOM+"_SAUVEGARDE" # Repertoire
# NOMAGES FIXES
LISTE_FREQUENCE_SAUVEGARDE=[ "Chaque démarrage", "Par jour",  "Par semaine",  "Par mois"]

NOM_TAMPON_EXTERIEUR              = MonParcellaire_PAR + "_INT_1__" + "_EXT_3"
NOM_TAMPON_INTERIEUR              = MonParcellaire_PAR + "_INT_1"
PREFIXE_NOM_POINT_CENTIPEDE       = "PointsCentipede"
#NOM_POINT_CENTIPEDE               = PREFIXE_NOM_POINT_CENTIPEDE + EXT_geojson
SUFFIXE_Q1                        = "_Q1"
SUFFIXE_Q2                        = "_Q2"
SUFFIXE_Q2_PLUS                   = "_Q2_PLUS"
#SUFFIXE_WGS                       = "_WGS"
SUFFIXE_L93                       = "_L93"
SUFFIXE_INT                       = "_INT"
SUFFIXE_EXT                       = "_EXT"
SUFFIXE_LARGES                    = "_LARGES"

SUFFIXE_FINS                      = "_FINS"
SUFFIXE_INTER                     = "_INTER_RANG"
SUFFIXE_RANG                      = "_SUR_RANG"
SUFFIXE_RUE                       = "_RUE"
NOM_ALLER                         = "ALLER"
NOM_RETOUR                        = "RETOUR"
NOM_LIGNE_COMPLETE_INT="Troncon"   + "_"
NOM_LIGNE_BRISE_INT="TronconBrise" + "_"
NOM_POLYGONE_BRISE_INT="RailBrise" + "_"
NOM_POINT_BRISE_INT="PointBrisee"  + "_"

# Répertoire et nommage traces CENTIPEDE
REPERTOIRE_CENTIPEDE_BRUT           ="CENTIPEDE_BRUT"           # solution.pos
REPERTOIRE_CENTIPEDE_TRAITEMENT     ="CENTIPEDE_TRAITEMENT"     # resultat    
REPERTOIRE_CENTIPEDE_W              =REPERTOIRE_CENTIPEDE_TRAITEMENT + "_ENCOURS"     # resultat
# pour tous les répertoires suivant un QML doit exister pour loadThemAll
REPERTOIRE_CENTIPEDE_PARCELLES      ="PARCELLES"                # multipoly brise   
REPERTOIRE_CENTIPEDE_POLYGONES      ="RAILS"                    # polygone brisé
REPERTOIRE_CENTIPEDE_RANGS          ="RANGS"                    # Polygone consolidé
REPERTOIRE_CENTIPEDE_INTER_RANGS    ="INTER_RANGS"  # ? Rails   # Polygone consolidé
# construit => REPERTOIRE_CENTIPEDE_RANGS_LARGES       =REPERTOIRE_CENTIPEDE_RANGS       + SUFFIXE_LARGES   
REPERTOIRE_CENTIPEDE_LIGNES         ="TRONCONS"                 # ligne brisee cohérente
REPERTOIRE_CENTIPEDE_POINTS         ="POINTS"                   # point brise cohérent 


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
VerificationReferentielMonParcellaire="Avez-vous paramétré le chemin vers le référentiel Mon Parcellaire ? \n\
    Vérifiez dans l'onglet {0} si le chemin vers le référentiel est correct. \n\
    Avez-vous déposer une jointure d'extension {1} dans ce référentiel ? \n\
    Son encodage est de l'UTF-8 ? \n\
    La jointure a-t-elle un délimiteur".format( E_OK, EXTENSIONS_CONNUES,  tuple( DELIMITEURS_CONNUS))
Maintenance="Contactez la maintenance jhemmi.eu"
Support="Si besoin, contactez pour du support jhemmi.eu"
Maintenance_GPKG="{0}, en fournissant votre GPKG de référence ~MonParcellaire/MonParcellaire.gpkg.".format(Maintenance)
VerificationVersionQGIS="Votre version de QGIS n'inclut pas ce module"
VerificationVersionQGISWin="Sous Windows, utilisez QGIS 3.10.x ou 3.12.y qui contiennent ce module."
Pas_verif_mais_maintenance=Maintenance_GPKG + \
    "En cas d'urgence, vous pouvez sortir de QGIS, sauver le GPKG ~MonParcellaire/MonParcellaire.gpkg pour l'envoyer à jhemmi.eu, \
    sinon recréer votre référentiel GPKG à partir de la dernière sauvegarde présente dans ~MonParcellaire/MonParcellaire_SAUVEGARDE "

# REPERTOIRE
def erreurRepertoire( CHEMIN_REP, correction=VerificationReferentielMonParcellaire):
    aText="Nom de répertoire {0} n'existe pas".format( CHEMIN_REP)
    raise MonParcellairePasRepertoire( "{0} || CORRECTION : {1}".format(aText, correction))
# FICHIER    
def erreurGPKG( CHEMIN_REP, NOM_GPKG, correction=VerificationReferentielMonParcellaire):
    aText="Pas de GPKG à traiter - nom de gpkg {0} - répertoire recherché {1})".format(NOM_GPKG, CHEMIN_REP)
    raise MonParcellairePasRepertoire( "{0} || CORRECTION : {1} si il est correct contacter jhemmi.eu".format(aText, correction))
def erreurJointuresExtensions( LISTE_EXTENSIONS=EXTENSIONS_CONNUES, correction=VerificationReferentielMonParcellaire):
    aText="Aucun jointure avec aucune des extensions {}".format( LISTE_EXTENSIONS)
    raise MonParcellaireErreurData( "{0} || CORRECTION : {1}".format(aText, correction))
def erreurJointureDelimeteurs( NOM_JOINTURE, LISTE_DELIMITEURS=DELIMITEURS_CONNUS, correction=VerificationReferentielMonParcellaire):
    aText="La jointure {0} n'a aucun des délimiteurs connus {1}. ".format(NOM_JOINTURE, LISTE_DELIMITEURS)
    aText=aText+"Supprimez ou créez de nouveau cette jointure".format(NOM_JOINTURE)
    monPrint( "{0} || AUTRES CORRECTIONS : \n{1} parmi {2} ?".format(aText, correction,  LISTE_DELIMITEURS),  T_ERR)
    return
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

def erreurTraitement( NOM_ALGO, correction=Pas_verif_mais_maintenance):
    aText="L'algorithme {0} n'a pas pu s'exécuter correctement. Vérifier le message d'erreur dans le journal des messages (onglet Traitement)".\
        format(NOM_ALGO)
    raise MonParcellaireErreurMethodo( "{0} || CORRECTION : {1}".format(aText, correction + " en fournissant votre GPKG et le nom de l'algo problématique"))
def erreur_traitement( NOM_ALGO, correction=Pas_verif_mais_maintenance):
    erreurTraitement( NOM_ALGO, correction)
def incoherenceTraceCentipedeVignoble( nomPos):    
    aText="Cette trace Centipede {} ne concerne pas votre parcellaire. Les traces sont-elles issues votre vignoble? ".format( nomPos)
    raise MonParcellaireErreurData( "{} || Vérifiez que vous avez bien déposer la trace sont dans votre répertoire".format(aText) + \
          " MON_PARCELLAIRE/CENTIPEDE_BRUT. Avez-vous créer vos parcelles dans le GPKG MonParcellaire en précisant la couche parcelles." + \
          " Si vous rejouer un traitement, il faut renommer dans MON_PARCELLAIRE/CENTIPEDE_BRUT le fichier .pos_TRAITE_xxx en .pos." + \
          " {}".format( Support))
def erreurImportVersion( module, correction=VerificationVersionQGIS):
    if MACHINE != 'Linux':
        correction=correction+'\n'+VerificationVersionQGISWin
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
def erreurCoherenceDF( parcelle, ligne, correction=Maintenance):
    aText="Dataframe pour la ligne {0} de la parcelle {1} n'est pas cohérente".format(ligne, parcelle)
    raise MonParcellaireErreurMethodo( "{0} || {1}".format(aText, correction))

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
        mon_prefixe = PREFIX = "== "
        if MonParcellaire_TRACE == "TERMINAL":
            la_date = datetime.now()
            mon_prefixe = la_date.strftime("%H:%M:%S") + SEP_PIPE + " " + PREFIX
            print( mon_prefixe + chaine)

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

def creerRepertoireOptionTemporaire( repertoireCible, temporaire=False):
    if not os.path.isdir( repertoireCible):
        os.mkdir(repertoireCible)
    if temporaire:
        repertoireCibleTmp=os.path.join( repertoireCible, "TMP")
        if not os.path.isdir( repertoireCibleTmp):
            os.mkdir(repertoireCibleTmp)
        return repertoireCibleTmp
    return None

def creerRepertoireEtQML( repertoireCible, temporaire=False):
    repertoireTemporaire = creerRepertoireOptionTemporaire(repertoireCible, temporaire)
    creerQML(repertoireCible)
    return repertoireTemporaire
    
def creerQML( repertoireCible):
    baseQML=os.path.join( os.path.dirname(__file__), EXT_qml[1:])
    nomQML = os.path.basename( repertoireCible)
    sourceQML=os.path.join( baseQML, nomQML + EXT_qml)
    cibleQML=os.path.join( repertoireCible, nomQML + EXT_qml)
    if not os.path.isfile( cibleQML):
        shutil.copy( sourceQML, cibleQML)
    return

def nommageVecteur( Repertoire, nomVecteur, Extension=EXT_geojson, doitExister="Oui"):
        """ Calcule le nom du vecteur et vérifie si le chemin au vecteur existe
        Rend le nom """
        # Assert
        if not os.path.isdir( Repertoire):
            erreurRepertoire( Repertoire)
        chemin_complet = os.path.join( Repertoire, nomVecteur + Extension)
        if  doitExister == "Oui" and not os.path.isfile( chemin_complet):
            erreurVecteur( Repertoire,  nomVecteur + Extension)
        return chemin_complet
    
def nommagesGPKG( Repertoire, nomTable, nomGPKG=MonParcellaire_GPKG, presenceAttendu=False):
    """ Calcule le nom de table et vérifie si le chemin au GPKG existe
    Rend le nom du gpkg, un libelle et le nom pour ouvrir avec QGIS API"""
    # Assert
    if not os.path.isdir( Repertoire):
        erreurRepertoire( Repertoire)
    CHEMIN_GPKG = os.path.join( Repertoire, nomGPKG)
    if not os.path.isfile( CHEMIN_GPKG):
        if presenceAttendu:
            erreurGPKG( nomGPKG,  CHEMIN_GPKG)
        return None, None, None
    #print( "nommageGPKG", CHEMIN_GPKG, "layer='{}'".format(nomTable), CHEMIN_GPKG + GPKG_LAYERNAME + nomTable)
    return CHEMIN_GPKG, "layer='{}'".format(nomTable), CHEMIN_GPKG + GPKG_LAYERNAME + nomTable
    
# Import communs

import platform
MACHINE = platform.system()

try:
    from shapely.geometry.polygon import Polygon
    from shapely.geometry import Point, LineString, MultiLineString
    if MonParcellaire_TRACE=="YES": 
        dir( Point)
        dir( LineString)
        dir( Polygon)
        dir( MultiLineString)
except:
    erreurImport("shapely")
try:
    import pandas as pd
    VERSION_PANDAS=pd.__version__
    print("Version pandas : {0}. Option sans warning".format( VERSION_PANDAS))
    pd.set_option('mode.chained_assignment',None)
    from pandas.io.json import json_normalize
    if MonParcellaire_TRACE=="YES": dir(json_normalize)

except:
    VERSION_PANDAS=None
    erreurImportVersion("pandas")        
try:
    import json
    if MonParcellaire_TRACE=="YES": dir( json)
except:
    erreurImport("json")
try:
    #import geopandas as gpd
    from geopandas import datasets, GeoDataFrame, read_file,  __version__ as gpdVersion    
    from geopandas.tools import sjoin
    if MonParcellaire_TRACE=="YES": 
        print("Version geopandas : {0} ".format( gpdVersion))
        dir( datasets)
        dir(GeoDataFrame)
        dir(read_file)
        dir(sjoin)
except:
    VERSION_GEOPANDAS=None
    if MonParcellaire_TRACE=="YES": print("geopandas non disponible (pour information, mais sans conséquence)")
try:
    import chardet
    if MonParcellaire_TRACE=="YES": print("Version chardet : {0} ".format( chardet.__version__))
except:
    erreurImport("chardet")


import os
if MonParcellaire_TRACE=="YES": dir( os)
import glob
if MonParcellaire_TRACE=="YES": dir( glob)
from datetime import datetime #, timedelta
if MonParcellaire_TRACE=="YES": dir( datetime)
from numpy import sqrt
if MonParcellaire_TRACE=="YES": dir( sqrt)
try:
    import shutil
    if MonParcellaire_TRACE=="YES": dir( shutil)
except:
    erreurImport("shutil")

from pyproj import Proj, transform , __version__ as v_pyproj
if MonParcellaire_TRACE=="TERMINAL": print("Version pyproj {} et transformateur {}".format( v_pyproj, transform))
PYPROJ_SOURCE_CRS      = Proj(init='epsg:4326') #+str(ID_SOURCE_CRS))
PYPROJ_DESTINATION_CRS = Proj(init='epsg:2154') #+str(ID_DESTINATION_CRS))

## N'est plus utile mais contient une creation de multipolygone

##from statistics import mean, pstdev

##def creerPolygonesBrises( dfPointBrut, nomRepertoireCentipede):
##    """
##    Ex PASSE 2 : Passer en revu tous les points par parcelle pour creer des polygones brises et un multipolygone brise par parcelle
##    Les point sont filtré par hrms pour garder les 75% les plus petits
##    """
##    distanceArea = preparerCalculDistance( str(ID_SOURCE_CRS))
##    lesParcelles=dfPointBrut['nom'].sort_values().unique()
##    monPrint( "PASSE 2 -- en cours pour {} parcelle(s) dans répertoire {}".format( len( lesParcelles), nomRepertoireCentipede), T_INF)
##    nombreMultiPolygones = 0
##    nombreTousLesRangs = 0
##    for parcelle in lesParcelles:
##        monPrint( "{} Parcelle {}".format( E_PANDAS,  parcelle))
##        repertoireParcelle = os.path.join( nomRepertoireCentipede, parcelle)
##        monPrint( "Répertoire {}".format( repertoireParcelle))
##        if not os.path.isdir( repertoireParcelle):
##            print("Etrange création de répertoire {}".format(repertoireParcelle),  T_WAR)
##            os.mkdir(repertoireParcelle)    
##        _, listePointsBrisees = chercherPointBrises( repertoireParcelle)
##        if listePointsBrisees == None:
##            continue
##        if len( listePointsBrisees) <= 2:
##            monPrint("Trop peu {} de troncons retrouvés : pas de polygone brisé à extraire pour la parcelle {}. \
##                Avez-vous déposé les données Centipède correspondantes à la parcelle dans ce répertoire ? ".format( len( listePointsBrisees), parcelle ))
##            continue
##
##        repertoirePolygone = os.path.join( os.path.dirname( os.path.dirname( listePointsBrisees[0])), REPERTOIRE_CENTIPEDE_POLYGONES)
##        if not os.path.isdir( repertoirePolygone):
##            creerRepertoireEtQML( repertoirePolygone, baseQML)
##        multiPolygoneGeometrie, multiPolygoneGeometrieAugmente, tousLesHrms, tousLesAzimuths = [], [], [], []
##        nombreTroncons = 0
##        for uneSeriePoints in listePointsBrisees:
##            dfPointBrise = geoJSON2pd( uneSeriePoints)                
##            # Numero de ligne (dans le nom) pour creer le nom du polygone et conserver IdLigne dans Polygone
##            IDSuiteBrisee = chercherIdToncon( uneSeriePoints)
##            nomPolygoneBriseeInterieure = os.path.join( repertoirePolygone, NOM_POLYGONE_BRISE_INT + str(IDSuiteBrisee) + EXT_geojson)
##            # Mémoriser métriques et stat pour renseigner chaque ligne
##            dfMetrique = pd.DataFrame( list(zip(dfPointBrise['distance'], dfPointBrise['azimuthDegre'], dfPointBrise['hrms'])),\
##                columns = ['distance','azimuthDegre', 'hrms'])
##            aStat = dfMetrique.describe()
##            largeurPolygone = aStat.hrms['max']
##            largeurAugmentee = max( [ largeurPolygone, LARGUEUR_AUGMENTEE])
##            # Filtre sur les plus petits hrms
##            dfPointFiltre = dfPointBrise[ ( dfPointBrise[ 'hrms'] <= aStat.hrms['75%'] )] # et &   ou |
##            if len( dfPointFiltre) > LIMITE_MIN_POINT_LIGNE:
##                nombreTroncons = nombreTroncons + 1
##                dateCaptures = chercherDateCapture(dfPointFiltre)
##                monPrint( "{} Polygone brisé {} de largeur {:.4f} contient {} points sur {} pour la parcelle {} capturés {}".\
##                    format( E_CLAP, IDSuiteBrisee, largeurPolygone, len( dfPointFiltre),  len( dfPointBrise), parcelle, dateCaptures))
##                polygoneGeometrie, polygoneGeometrieAugmente, lesFids, lesHrms, lesAzimuths = [], [], [], [], [] 
##                for pointDF in dfPointFiltre.itertuples():
##        #            if IDSuiteBrisee == str(51):
##        #                print("Aller : {} long {} et azimuth R {} et degre {}".format( pointDF.fid, pointDF.longitude, pointDF.azimuthRadian, pointDF.azimuthDegre))
##                    pointCourantWGS, pointCourantL93 = df2QgsPoint( pointDF)
##                    parcelleCourante = pointDF.nom
##                    lesAzimuths.append( pointDF.azimuthDegre)
##                    lesFids.append( pointDF.fid)
##                    lesHrms.append( pointDF.hrms)
##                    pointProjete = distanceArea.computeSpheroidProject( pointCourantWGS, largeurPolygone, pointDF.azimuthRadian + ( pi/2))   # thanks https://stackoverflow.com/questions/55615374/qgsdistancearea-computespheroidproject-return-0-0
##                    pointAumente = distanceArea.computeSpheroidProject( pointCourantWGS, largeurAugmentee, pointDF.azimuthRadian + ( pi/2))
##                    # Stocker pour polygone
##                    polygoneGeometrie.append( [pointProjete.x(), pointProjete.y()])
##                    polygoneGeometrieAugmente.append( [pointAumente.x(), pointAumente.y()])
##                # Inverser le sens df[::-1]  et -PI/2
##                for pointDF in dfPointFiltre[::-1].itertuples():
##                    pointCourantWGS, pointCourantL93 = df2QgsPoint( pointDF)
##                                                                      # Coordonnées en degre
##                    pointProjete = distanceArea.computeSpheroidProject( pointCourantWGS, largeurPolygone, pointDF.azimuthRadian - ( pi/2)) 
##                    pointAumente = distanceArea.computeSpheroidProject( pointCourantWGS, largeurAugmentee, pointDF.azimuthRadian - ( pi/2))
##                    # Stocker pour polygone
##        #            if IDSuiteBrisee == str(51):
##        #                print("Retour : {} est projeté {}".format( pointDF.fid, pointProjete))
##                    polygoneGeometrie.append( [pointProjete.x(), pointProjete.y()])
##                    polygoneGeometrieAugmente.append( [pointAumente.x(), pointAumente.y()])
##
##                # Fermer le polygone  
##                polygoneGeometrie.append( polygoneGeometrie[0])
##                dfPolygoneBrise = pd.DataFrame( [[ IDSuiteBrisee, min( lesFids), max( lesFids), mean( lesHrms), max( lesHrms), mean(lesAzimuths)-90, \
##                                mean(lesAzimuths),  pstdev(lesAzimuths), parcelleCourante, casTracking + "_INITIAL",  nomCaster, largeurAugmentee]],\
##                                        columns = ['IdPolygone', 'MIN_fid', 'MAX_fid', 'hrms', 'MAX_hrms', 'orientation', \
##                                'azimuthDegre', 'STD_azimuthDegre', 'nom', 'capture',  'caster', 'MAX_ecart'])
##                df2GeoJSON( dfPolygoneBrise, nomPolygoneBriseeInterieure, [ [ polygoneGeometrie]], 'MultiPolygon')
##                multiPolygoneGeometrie.append( polygoneGeometrie)
##                multiPolygoneGeometrieAugmente.append( polygoneGeometrieAugmente)
##                nombreTousLesRangs=nombreTousLesRangs+nombreTroncons
##                for h in lesHrms:
##                    tousLesHrms.append( h)
##                for a in lesAzimuths:
##                    if a>0:
##                        tousLesAzimuths.append( a)
##                    else:
##                        # Pour l'autre sens d'avancement
##                        tousLesAzimuths.append( a + 180)
##         #listeDatesCapture]],\
##        dfMultiPolygoneBrise = pd.DataFrame( [[ nombreTroncons, mean( tousLesHrms), max( tousLesHrms),\
##                                mean(tousLesAzimuths)-90, mean(tousLesAzimuths), pstdev(tousLesAzimuths), \
##                               parcelleCourante, casTracking + "_INITIAL",  nomCaster, largeurAugmentee]],\
##                                    columns = [ 'nombreRangs', 'hrms', 'MAX_hrms', \
##                                                'orientation', 'azimuthDegre', 'STD_azimuthDegre', \
##                                                'nom', 'capture',  'caster', 'MAX_ecartement']) #, 'DATE_capture'])
##        nomMultiPolygoneBrise = os.path.join( repertoirePolygone, NOM_POLYGONE_BRISE_INT + parcelleCourante + EXT_geojson)
##        df2GeoJSON( dfMultiPolygoneBrise, nomMultiPolygoneBrise, [ multiPolygoneGeometrie], 'MultiPolygon')
##        _, _, _, _, _, _, _, nomMultiPolygoneAugmente = incrementerNommages( None, casTracking, nomRepertoireCentipede,  parcelle)
##        df2GeoJSON( dfMultiPolygoneBrise, nomMultiPolygoneAugmente, [ multiPolygoneGeometrieAugmente], 'MultiPolygon')
##        nombreMultiPolygones = nombreMultiPolygones + 1
##        
##        monPrint( "Fin extraction des polygones brisées pour la parcelle {}".format( parcelle))
##        
##    monPrint( "{} PASSE 2 : Fin extraction des {} rangs brisés".format( E_CLAP, nombreTousLesRangs),  T_OK)
##    return nombreTousLesRangs, nombreMultiPolygones
