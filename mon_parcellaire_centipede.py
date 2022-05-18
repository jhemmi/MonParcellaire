# -*- coding: utf-8 -*-
"""
/***************************************************************************
 mon_parcellaire_centipede
                                 A QGIS plugin
 Centipede script QGIS & pandas
 Traiter les Centipede pos pour identifier des rangs
    Filtrer la qualité 
    Jointure les traces Centipede pos par le parcellaire
    Déterminer les alignements pour créer des rangs ou interrangs

                             -------------------
        begin                : 2021-02-12
        git sha              : $Format:%H$
        copyright            : (C) 2021 by jhemmi.eu
        email                : jean@jhemmi.eu
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from initialisation_var_exception import *
from qgis.core import ( QgsSettings, QgsApplication, QgsProject, QgsCoordinateReferenceSystem, \
    QgsPointXY, QgsDistanceArea) # BAD pour standalone mode QgsCoordinateTransform)
from math import pi
from sys import path  # dans Init processing QGIS

"""Valeur des limites pour couper, ignorer points ou lignes"""
LIMITE_MAX_SECONDES_ENTRE_DEUX_CAPTURES  = 3    # passage en tournières
LIMITE_MAX_DISTANCES_ENTRE_DEUX_CAPTURES = 1.8 # 8 St hubert # vigne 1.8  # changement de troncon, si inférieur à interang

LIMITE_MIN_DISTANCES_ENTRE_DEUX_CAPTURES = 0.03 # éviter les arrets qui polluent les azimuth instantanée
LIMITE_MIN_POINT_LIGNE                   = 10   # éviter les petits alignements 
LIMITE_MIN_LONGUEUR_LIGNE                = 10   # 8 avant 2 mai 21 : éviter les petits alignements bis
ELARGISSEMENT_RANG                       = 0.5  # Prospection de point   
ALLONGE_RANG                             = 500 # 1 km en tout
ALLONGE_RANG_FINS                        = 250
#LIMITE_MAX_STD_AIMUTH_LIGNES=5                 # n'est pas (plus) utilisé
FILTRE_Q2=ELARGISSEMENT_RANG/2 # Q2_PLUS contient seulement les points précis à 25 cm
ALLER_RETOUR_DETAILLE=True
QUALITE_ALIGNEMENT = [ "Non aligné", "Incertain", "Probable", "Fort probable", "Convergent",  "Finalisé"]
LIGNES_TRACEES=["0001", "0010", "0020"]
#####SOURCE_CRS = QgsCoordinateReferenceSystem.fromEpsgId( 4326)
#####DESTINATION_CRS = QgsCoordinateReferenceSystem.fromEpsgId( 2154)
#####TRANSFORMATEUR = QgsCoordinateTransform(SOURCE_CRS, DESTINATION_CRS, QgsProject.instance())  # Pas en standalone car il manque le projet

def chercherIdToncon( uneSeriePoints):
    # Retrouver le nom de troncon
    nomLigne = os.path.basename( uneSeriePoints)
    debutNomLigne=nomLigne.split(".")[0]
    IDSuiteBrisee=debutNomLigne.split("_")[1]
    return str( IDSuiteBrisee).zfill(4)

def chercherLongueDistanceSilver( nomSilver, nomSilverExtent, epsg=ID_SOURCE_CRS):
    """ créer Extent du silver et calcule longueur """
    distanceArea = preparerCalculDistance( str(epsg))  # WGS84
    traitementExtraireExtent( nomSilver, nomSilverExtent)
    dfExtent = geoJSON2pd( nomSilverExtent)
    # Approximation mais dans le cas silver, pas d'épaisseur
    pointMin, _ = coordonnees2Point( dfExtent['MINY'].values.tolist()[0], dfExtent['MINX'].values.tolist()[0])
    pointMax, _ = coordonnees2Point( dfExtent['MAXY'].values.tolist()[0], dfExtent['MAXX'].values.tolist()[0])
    distance = distanceArea.measureLine( pointMin, pointMax)
#    longueur = dfExtent['HEIGHT'].values.tolist()[0]
#    largueur = dfExtent['WIDTH'].values.tolist()[0]
#    monPrint( "longueur {} et largeur {} Extent et distance {}".format( longueur,  largueur,  distance))
    return distance
                
def dfPoints2Alignement( IDLigne, dfPoint, pointDebut=None, pointFin=None, epaisseur=None, longueur=0, alignementIdeal=None):
    """ df vers un alignement, ie polygone (les points de base sont optionels, pointDebut et pointFin peuvent les imposser)
        épaisseur permet de forcer elargissement (si non le polygone a une largeur de 2 HRMS Max) et longueur permet d'allonger le polygone
        quand alignementIdeal est renseigné avec un chemin pour tracer le detail des calculs, la méthode du demi polygone identifie le points de base qui donne le meilleur alignement)
        retour des métriques de l'alignement et de sa geométrie (aux deux formats shapely et liste pour json.dump - TODO Vx: Geom)
    """
    nombrePointAScruter=len( dfPoint)
    dfMetriqueAvant = pd.DataFrame( list(zip( dfPoint['distance'], dfPoint['fid'], dfPoint['azimuthRadian'], dfPoint['hrms'],  dfPoint['jourHeure'])),\
    columns = ['distance', 'fid', 'azimuthRadian', 'hrms', 'jourHeure'])
    statistiqueAvantFiltre = dfMetriqueAvant.describe()
    if epaisseur == None:
        epaisseur = statistiqueAvantFiltre.hrms['max']
    # Filtrer 0,75 des hrms pour ne garder comme base de polygone que des point "précis"
    dfPointFiltre = dfPoint[ ( dfPoint[ 'hrms'] <= statistiqueAvantFiltre.hrms['75%'] )] # et &   ou |
    dfMetriqueFiltre = pd.DataFrame( list(zip( dfPointFiltre['distance'], dfPointFiltre['fid'], dfPointFiltre['azimuthRadian'], dfPointFiltre['hrms'],  dfPointFiltre['jourHeure'])),\
    columns = ['distance', 'fid', 'azimuthRadian', 'hrms', 'jourHeure'])
    statistiqueApresFiltre = dfMetriqueFiltre.describe() #percentiles=[.1, .9])

    # Rechercher les meilleurs points de base : ceux qui permettent à un demi polygone de croiser 50% des points    
    if alignementIdeal != None:
        # Chercher les premiers-derniers vers un meilleur alignement
        fidPremiers, fidDerniers = [], []
        for pointDF in dfPoint.itertuples():
            if pointDF.fid < statistiqueApresFiltre.fid[ '25%']:
                fidPremiers.append( pointDF.fid)
            if pointDF.fid > statistiqueApresFiltre.fid[ '75%']:
                if not pointDF.fid in fidPremiers:
                    fidDerniers.append( pointDF.fid)
        #monPrint("Ligne {} Fid premiers {} Fid derniers {}".format( IDLigne, fidPremiers, fidDerniers ))
        # Comparer les différents demiPolygones 
        maxComparaison = min( len(fidPremiers),  len(fidDerniers))
        syntheseDemiDroiTes=[]
        for position, idPremierFID in enumerate( fidPremiers[:maxComparaison]):
            # TODO V1.6: Boucler toutes les paires et non pas par intervales égaux
            idDernierFID = fidDerniers[ position]
            idDeuxFidS=str(idPremierFID) + '-'+ str( idDernierFID)
            metriqueProspect, _, polygoneProspect = dfDeuxPoints2DemiPolygone( dfPoint, statistiqueAvantFiltre, idPremierFID, idDernierFID , IDLigne, epaisseur)
            # Rallonge pour recherche de points
            _, polygonePossible, polygoneProspectRallonge = dfDeuxPoints2DemiPolygone( dfPoint, statistiqueAvantFiltre, idPremierFID, idDernierFID , IDLigne, \
                epaisseur, longueur)
            #monPrint( "Métriques {} et polygone {} ".format( metriqueProspect,  polygoneProspect))
            # Vérifier nombre de points dedans et dehors
            pointsDedans=0
            for pointDF in dfPoint.itertuples():
                pointGPS, _ = df2ShapelyPoint( pointDF)
                if polygonePossible.contains( pointGPS):
                    pointsDedans = pointsDedans +1   
            pourcentageDedans = int( pointsDedans*100/nombrePointAScruter)
            distanceCinquante=50
            if pointsDedans > 0:
                if pourcentageDedans > 50:
                    distanceCinquante = pourcentageDedans - 50
                else:
                    distanceCinquante = 50 - pourcentageDedans
            syntheseDemiDroiTes.append( {"IDs" : idDeuxFidS, "Premier": idPremierFID, "Dernier": idDernierFID, \
                "nombreDedans": pointsDedans,  "pourcentageDedans": pourcentageDedans, "ratio50Distance" :distanceCinquante})
            # TODO: test pour allonge plutôt ?
            if MonParcellaire_TRACE == "TERMINAL":
                dfProspect = pd.DataFrame( [[ idDeuxFidS, idPremierFID, idDernierFID, IDLigne, metriqueProspect[ "épaisseur"], metriqueProspect[ "MAX_hrms"], \
                    metriqueProspect[ "distance"], metriqueProspect[ "azimuthD"], metriqueProspect[ "orientation"], \
                    metriqueProspect[ "vitesse"], metriqueProspect[ "sens"], pointsDedans, pourcentageDedans, distanceCinquante ]],\
                    columns = ['IdProspect', 'fidPremier', 'fidDernier', 'IdRang', 'largeur', 'MAX_hrms', 'distance', 'azimuthDegre', 'orientation', \
                                   'vitesse',  'sensAvancement', 'nombreDedans', 'pourcentageDedans', 'distanceCinquante' ])
                cheminPourDetailler=alignementIdeal # indicateur sert à passer le répertoire
                nomCourtRepertoire=  os.path.basename( os.path.dirname( cheminPourDetailler))
                nomProspectTemp = os.path.join( cheminPourDetailler, nomCourtRepertoire + '_' + str(IDLigne) + "_PROSPECT_" +  idDeuxFidS + '_' + str( distanceCinquante) + EXT_geojson)
                df2GeoJSON( dfProspect, nomProspectTemp, polygoneProspect, 'Polygon')
                nomProspectAllonge = os.path.join( cheminPourDetailler, nomCourtRepertoire + '_' + str(IDLigne) + "_PROSPECT_RALLONGE_" + idDeuxFidS + '_' + str( distanceCinquante) + EXT_geojson)
                df2GeoJSON( dfProspect, nomProspectAllonge, polygoneProspectRallonge, 'Polygon')
        # Chercher la meilleure synthèse
        laMeilleureSynthese=50
        idMeilleureSynthese = -1
        #monPrint("Les {} syntheses ".format( len(syntheseDemiDroiTes)))
        for idSynthese, uneSynthese in enumerate( syntheseDemiDroiTes):
            if uneSynthese[ 'ratio50Distance'] < laMeilleureSynthese:
                laMeilleureSynthese = uneSynthese[ 'ratio50Distance']
                idMeilleureSynthese = idSynthese
        # Assert sur idMeilleureSynthese >0
        if idMeilleureSynthese < 0:
            monPrint("Ligne {} aucun meilleur alignement identifié {}".format( IDLigne, idMeilleureSynthese), T_WAR)
            return dfPoints2Alignement( IDLigne, dfPoint, None, None, epaisseur, longueur)
        syntheseDemiDroiTes[ idMeilleureSynthese][ "ratio50Qualité"] = QUALITE_ALIGNEMENT[2]   
        if syntheseDemiDroiTes[ idMeilleureSynthese][ "ratio50Distance"] > 30:
            syntheseDemiDroiTes[ idMeilleureSynthese]["ratio50Qualité"] = QUALITE_ALIGNEMENT[1]  # Incertain   
        if syntheseDemiDroiTes[ idMeilleureSynthese][ "ratio50Distance"] <10:
            syntheseDemiDroiTes[ idMeilleureSynthese]["ratio50Qualité"] = QUALITE_ALIGNEMENT[3]  # Fort Probable   
        if syntheseDemiDroiTes[ idMeilleureSynthese][ "ratio50Distance"] < 5:
            syntheseDemiDroiTes[ idMeilleureSynthese]["ratio50Qualité"] = QUALITE_ALIGNEMENT[4]  # Convergent   
        if IDLigne in LIGNES_TRACEES:
            monPrint( "{} Meilleure alignement numéro {} vaut {}".format( U_LIGNE, idMeilleureSynthese,  syntheseDemiDroiTes[ idMeilleureSynthese]))    
        # Rendre le meilleur, ie celui qui la meilleure répartition de points dedans vs dehors
        return dfDeuxPoints2PolygoneModele( dfPoint, statistiqueAvantFiltre, syntheseDemiDroiTes[ idMeilleureSynthese][ "Premier"], syntheseDemiDroiTes[ idMeilleureSynthese][ "Dernier"] , \
            IDLigne, epaisseur, longueur, syntheseDemiDroiTes[ idMeilleureSynthese])        
    elif pointDebut == None or pointFin == None:
        # Cas 2 points extérieurs comme base du polygone
        return dfDeuxPoints2PolygoneModele( dfPoint, statistiqueAvantFiltre, statistiqueApresFiltre.fid['min'], statistiqueApresFiltre.fid['max'], \
            IDLigne, epaisseur, longueur)
    else:
        # Cas 2 points sont connus (cas de polygone fin)
        return dfDeuxPoints2PolygoneModele( dfPoint, statistiqueAvantFiltre, pointDebut, pointFin, \
            IDLigne, epaisseur, longueur)

def dfDeuxPoints2Metrique( dfPoint, dfStat, minFid, maxFid, IDLigne, epaisseur, distanceAreaL):
    """Création des métriques"""
    dateDebut = None
    dateFin = None
    for pointDF in dfPoint.itertuples():
        if pointDF.fid == dfStat.fid ['min']:
            premierPointDF, premierPointDFL93 = df2QgsPoint( pointDF)
        if pointDF.fid == dfStat.fid ['max']:
            dernierPointDF, dernierPointDFL93 = df2QgsPoint( pointDF)
        if pointDF.fid == minFid:
            premierPoint, premierPointL93 = df2QgsPoint( pointDF)
            dateDebut = pointDF.jourHeure      
        if pointDF.fid == maxFid:
            dernierPoint, dernierPointL93 = df2QgsPoint( pointDF)
            dateFin = pointDF.jourHeure
    metriqueLigne={}
    # Distance, vitesse et azimuths entre premier et dernier
    distanceDFL = distanceAreaL.measureLine( premierPointDFL93, dernierPointDFL93)
    distanceL = distanceAreaL.measureLine( premierPointL93, dernierPointL93)
    metriqueLigne[ "couvertureDistance"] = int(distanceL*100/distanceDFL)
    metriqueLigne[ "couvertureQualité"] = QUALITE_ALIGNEMENT[2]   
    if metriqueLigne[ "couvertureDistance"] < 35:
        metriqueLigne["couvertureQualité"] = QUALITE_ALIGNEMENT[1]  # Incertain   
    if metriqueLigne[ "couvertureDistance"] > 70:
        metriqueLigne["couvertureQualité"] = QUALITE_ALIGNEMENT[3]  # Fort Probable   
#    if IDLigne in LIGNES_TRACEES:
#        monPrint("Pourcentage couverture {} qualité {}: Distance DF {} distance couverte {}".\
#            format( metriqueLigne[ "couvertureDistance"], metriqueLigne["couvertureQualité"], distanceDFL, distanceL ))
    aziRL = distanceAreaL.bearing( premierPointL93, dernierPointL93)
#    distanceAreaW = preparerCalculDistance( str( ID_SOURCE_CRS))  
#    distanceW = distanceAreaW.measureLine( premierPoint, dernierPoint)
#    aziRW = distanceAreaW.bearing( premierPoint, dernierPoint)
#    monPrint("Ligne {} Delta L93 - WGS des mesures distance  {} et azimuth {} radian".\
#        format( IDLigne, (distanceL -distanceW), (aziRL - aziRW)))
    metriqueLigne[ "distance"] = distanceL 
    metriqueLigne[ "azimuthR"] = aziRL     
    metriqueLigne[ "vitesse"] = None
    metriqueLigne[ "durée"] = None
    if dateDebut != None and dateFin != None:
        metriqueLigne[ "durée"] = chercherEcartTemps( dateDebut, dateFin)
        metriqueLigne[ "vitesse"] =   metriqueLigne[ "distance"] / metriqueLigne[ "durée"] * 3.6  #m/s en km/h
    metriqueLigne[ "azimuthD"]    = ( metriqueLigne[ "azimuthR"] * 180 / pi) % 360
    metriqueLigne[ "sens"]="INCONNU"
    if metriqueLigne[ "azimuthD"] <= 180:
        metriqueLigne[ "sens"] = NOM_ALLER
    else:
        metriqueLigne[ "sens"] = NOM_RETOUR
        
    metriqueLigne[ "orientation"] = ( metriqueLigne[ "azimuthD"] - 90) % 180
    metriqueLigne[ "épaisseur"] = epaisseur
    metriqueLigne[ "MAX_hrms"] = dfStat.hrms[ "max"]  #statistiqueAvantFiltre.hrms['max']
    metriqueLigne[ "fidPremier"] = minFid
    metriqueLigne[ "fidDernier"] = maxFid
    return metriqueLigne, premierPoint, dernierPoint

def dfDeuxPoints2DemiPolygone( dfPoint, dfStat, minFid, maxFid, IDLigne, epaisseur, rallonge=None):
    """Création d'un demi polygone et de ses métriques qui ne tiennent pas compte de la rallonge"""
    distanceAreaL = preparerCalculDistance( str( ID_DESTINATION_CRS))  # L93 ? param epsg=ID_DESTINATION_CRS
    metriqueLigne, premierPoint, dernierPoint = dfDeuxPoints2Metrique( dfPoint, dfStat, minFid, maxFid, IDLigne, epaisseur, distanceAreaL)
    # Dessiner DEMI _POLYGONE
    if rallonge == None:
        pointA = premierPoint
        pointD = dernierPoint
    else:  # rallonger
        pointA = distanceAreaL.computeSpheroidProject( premierPoint, rallonge, metriqueLigne[ "azimuthR"] - pi)
        pointD = distanceAreaL.computeSpheroidProject( dernierPoint, rallonge, metriqueLigne[ "azimuthR"])
    pointB = distanceAreaL.computeSpheroidProject( pointA, epaisseur, metriqueLigne[ "azimuthR"] + ( pi/2))   # thanks https://stackoverflow.com/questions/55615374/qgsdistancearea-computespheroidproject-return-0-0
    pointC = distanceAreaL.computeSpheroidProject( pointD, epaisseur, metriqueLigne[ "azimuthR"] + ( pi/2))
        
    return metriqueLigne, \
        Polygon([(pointA.x(), pointA.y()), (pointB.x(), pointB.y()), (pointC.x(), pointC.y()), (pointD.x(), pointD.y()), (pointA.x(), pointA.y())]), \
               [[[pointA.x(), pointA.y()], [pointB.x(), pointB.y()], [pointC.x(), pointC.y()], [pointD.x(), pointD.y()], [pointA.x(), pointA.y()]]]

def dfDeuxPoints2PolygoneModele( dfPoint, dfStat, minFid, maxFid, IDLigne, epaisseur, rallonge=None, synthese=None):
    """Création d'un polygone et de ses métriques qui ne tiennent pas compte de la rallonge"""
    distanceAreaL = preparerCalculDistance( str( ID_DESTINATION_CRS))  # L93 
    metriqueLigne, premierPoint, dernierPoint = dfDeuxPoints2Metrique( dfPoint, dfStat, minFid, maxFid, IDLigne, epaisseur, distanceAreaL)
    #print("Synthese {}".format( synthese))
    if synthese != None:
        metriqueLigne[ "ratio50Distance"] = synthese[ "ratio50Distance"]
        metriqueLigne[ "ratio50Qualité"]  = synthese[ "ratio50Qualité"]   
    else:  # Non aligné
        metriqueLigne[ "ratio50Distance"] = 99
        metriqueLigne[ "ratio50Qualité"]  = QUALITE_ALIGNEMENT[0]   
    
    if IDLigne in LIGNES_TRACEES:
        monPrint( "Ligne {} a pour métriques : {}".format( IDLigne, metriqueLigne))
    
    # Dessiner POLYGONE ENTIER
#    if metriqueLigne[ "azimuthR"] <= pi: # premier est en bas
    if metriqueLigne[ "sens"] == NOM_ALLER:
        if rallonge == None:
            pointA = premierPoint
            pointD = dernierPoint
        else:
            pointA = distanceAreaL.computeSpheroidProject( premierPoint, rallonge     , metriqueLigne[ "azimuthR"] -pi)
            pointD = distanceAreaL.computeSpheroidProject( dernierPoint, rallonge     , metriqueLigne[ "azimuthR"]) 
    else:
        if rallonge == None:
            pointA = dernierPoint
            pointD = premierPoint
        else:
            pointA = distanceAreaL.computeSpheroidProject( dernierPoint, rallonge     , metriqueLigne[ "azimuthR"] -pi)
            pointD = distanceAreaL.computeSpheroidProject( premierPoint, rallonge     , metriqueLigne[ "azimuthR"]) 
    # on tourne sens horaire
    pointB = distanceAreaL.computeSpheroidProject(         pointA,       epaisseur     , metriqueLigne[ "azimuthR"] + ( pi/2)) 
    pointC = distanceAreaL.computeSpheroidProject(         pointD,       epaisseur     , metriqueLigne[ "azimuthR"] + ( pi/2)) 
    pointE = distanceAreaL.computeSpheroidProject(         pointD,       epaisseur     , metriqueLigne[ "azimuthR"] - ( pi/2)) 
    pointF = distanceAreaL.computeSpheroidProject(         pointA,       epaisseur     , metriqueLigne[ "azimuthR"] - ( pi/2)) 
    return metriqueLigne, \
        Polygon([(pointA.x(), pointA.y()), (pointB.x(), pointB.y()), (pointC.x(), pointC.y()), (pointD.x(), pointD.y()), \
                    (pointE.x(), pointE.y()), (pointF.x(), pointF.y()), (pointA.x(), pointA.y())]), \
               [[[pointA.x(), pointA.y()], [pointB.x(), pointB.y()], [pointC.x(), pointC.y()], [pointD.x(), pointD.y()], \
                    [pointE.x(), pointE.y()], [pointF.x(), pointF.y()], [pointA.x(), pointA.y()]]]

def t2_CreerRailPassage( dfPointBrut, nomRepertoireCentipede, repertoireDesParcelles, cheminCompletTable, rangOuInter=REPERTOIRE_CENTIPEDE_POLYGONES):
    """
    PASSE2 : recoller les troncons de points dans un polygone représentant le rang/interang/rail (simplification, elargissement, clip) 
    Créer un rail élargi et étroit, pour identifier le rang durant un passage 
    """
    lesParcelles=dfPointBrut['nom'].sort_values().unique()
    monPrint( "PASSE 2 -- en cours pour {} parcelle(s) dans répertoire {}".format( len( lesParcelles), nomRepertoireCentipede), T_INF)
    
    # Preambule Exploser le parcellaire dans un gpkg par parcellaire
    repertoireParcelleGPKG = os.path.join( os.path.join( nomRepertoireCentipede, REPERTOIRE_CENTIPEDE_PARCELLES),  "GPKG")
    creerRepertoireOptionTemporaire( repertoireParcelleGPKG)
    dictParcellesGeoJSON  = traitementExploserParcelles( cheminCompletTable, repertoireParcelleGPKG, lesParcelles)
    
    nombreTousLesRangs = 0
    for parcelle in lesParcelles:
        monPrint( "{} Parcelle {} est dans geoJSON : {}".format( E_PANDAS,  parcelle, dictParcellesGeoJSON[ parcelle]))
        repertoireParcelle = os.path.join( nomRepertoireCentipede, parcelle)
        creerRepertoireOptionTemporaire( repertoireParcelle)
        repertoireTaitementOK = os.path.join( repertoireParcelle,  "TRAITE_PASSE_2")
        if os.path.isdir( repertoireTaitementOK):
            monPrint( "Pas de traitement de la parcelle {} : déjà joué".format( parcelle))
            continue
        _, listePointsBrisees = chercherPointBrises( repertoireParcelle)
        if listePointsBrisees == None:
            continue
# Commenter ces 4 lignes pour voiture St hubert
        if len( listePointsBrisees) <= 2:
            monPrint("Trop peu {} de troncons retrouvés : pas de rang à extraire pour la parcelle {}. \
                Avez-vous déposé les données Centipède correspondantes à la parcelle dans ce répertoire ? ".format( len( listePointsBrisees), parcelle ))
            continue
        _, listeTronconsBrisees = chercherLignesBrisees( repertoireParcelle)
        numeroRang = 1
        # Creer un polygone de base avec la premiere serie de point
        IDTronconBase = chercherIdToncon( listePointsBrisees[0])
        IDTronconFinal = chercherIdToncon( listePointsBrisees[-1])
        dfPointBase = geoJSON2pd( listePointsBrisees[0])
        courtRepertoireFin, repertoireFin, repertoireFinTemporaire, \
        courtRepertoireLarge, repertoireLarge, repertoireLargeTemporaire, repertoireLargeAller,  repertoireLargeRetour = \
            creerRepertoiresFinLarge( os.path.dirname( os.path.dirname(  listePointsBrisees[0])), rangOuInter, ALLER_RETOUR_DETAILLE)
        metriqueTroncon, rangPossible, _ = dfPoints2Alignement( numeroRang, dfPointBase, None, None, ELARGISSEMENT_RANG, ALLONGE_RANG)
        distanceDesTroncons=metriqueTroncon[ "distance"]
        rangTermine = False
        for idSerie, uneSeriePoints in enumerate( listePointsBrisees[1:]):
            IDSuivant = chercherIdToncon( uneSeriePoints)
##            monPrint( "{}  Rang {} en cours de {} points issus du/des troncon(s) {}. Troncon prospecté {}".\
##              format( E_RANG_EN_COURS, numeroRang, len( dfPointBase), IDTronconBase, IDSuivant))
            dfPointsSuivants = geoJSON2pd( uneSeriePoints)
            for unPointSuivant in dfPointsSuivants.itertuples():
                pointSuivantGPS, _ = df2ShapelyPoint( unPointSuivant)
                # COLLAGE Chercher à ralonger le rangPossible si il contient un des points du troncon suivant
                if rangPossible.contains( pointSuivantGPS):
                     # Addition de ce df de point dès qu'un point est dans le troncon en cours
                    dfPointBase   = pd.concat( [dfPointBase, dfPointsSuivants],  sort=False)
                    IDTronconBase = IDTronconBase + '-' + IDSuivant
                    # Calculer le nouveau rang possible
                    metriqueDesTroncons, rangPossible, _ = dfPoints2Alignement( numeroRang, dfPointBase, None, None, ELARGISSEMENT_RANG, ALLONGE_RANG)
                    distanceDesTroncons = metriqueDesTroncons[ "distance"]
                    monPrint( "{} Regroupement des troncons {} soit {} points coallescents couvrant une distance {}".\
                            format( E_REGROUPEMENT, IDTronconBase, len(dfPointBase), int(distanceDesTroncons)))
                    rangTermine = False
                    break # on continue avec la serie de points suivante sans terminer le rang
                else:
                    rangTermine = True
            
            if rangTermine or IDSuivant == IDTronconFinal:    # pour le dernier       
                IDRangRempliZero=str( numeroRang).zfill(4)
                # CHOIX MEILLEUR POINTS Rang est entierement identifié, le suivant permettra de creer un nouveau rang
                # Rang large se calle sur meilleurs points de base                                                             # 0.5 metre
                metriqueLigne, rangElargi, rangElargiGeoJSON = dfPoints2Alignement( IDRangRempliZero, dfPointBase, None, None, ELARGISSEMENT_RANG, \
                    ALLONGE_RANG, repertoireLargeTemporaire)
                # Passer les meilleurs points de demi droite du rang large
                # TODO V1.6: tester demi droite sur rang fins
                _, _, rangHrmsNonAllonge = dfPoints2Alignement( IDRangRempliZero, dfPointBase,  \
                    metriqueLigne[ "fidPremier"],  metriqueLigne[ "fidDernier"], None)
                metriqueSilver, rangHrms, rangHrmsGeoJSON = dfPoints2Alignement( IDRangRempliZero, dfPointBase,  \
                    metriqueLigne[ "fidPremier"],  metriqueLigne[ "fidDernier"], None, ALLONGE_RANG_FINS)
                nomRangSilverTempNonAllonge = os.path.join( repertoireFinTemporaire, courtRepertoireFin + "_COURT_" + IDRangRempliZero + '_' + parcelle + EXT_geojson)
                nomRangSilverTemp = os.path.join( repertoireFinTemporaire, courtRepertoireFin + "_A_DECOUPER_" + IDRangRempliZero + '_' + parcelle + EXT_geojson)
                #nomRangSilverExtent = os.path.join( repertoireFinTemporaire, courtRepertoireFin+ "_ETENDUE_" + IDRangRempliZero + '_' + parcelle + EXT_geojson)
                nomRangSilver = os.path.join( repertoireFin, courtRepertoireFin + '_' + IDRangRempliZero + '_' + parcelle + EXT_geojson)
                dfRang = pd.DataFrame( [[ IDRangRempliZero, IDTronconBase, metriqueSilver[ "épaisseur"], metriqueSilver[ "MAX_hrms"], \
                        parcelle, metriqueSilver[ "distance"], metriqueSilver[ "azimuthD"], metriqueSilver[ "orientation"], metriqueSilver[ "vitesse"],  metriqueSilver[ "sens"]]],\
                    columns = ['IdRang', 'IdTroncon', 'largeur', 'MAX_hrms', 'nom', 'distance', 'azimuthDegre', 'orientation', 'vitesse',  'sensAvancement']) 
                df2GeoJSON( dfRang,   nomRangSilverTempNonAllonge, rangHrmsNonAllonge, 'Polygon')
                df2GeoJSON( dfRang,   nomRangSilverTemp, rangHrmsGeoJSON, 'Polygon')
                traitementCouperRang( nomRangSilverTemp, dictParcellesGeoJSON[ parcelle], nomRangSilver)
                # Longueur du polygone 
                # TODO distance du rang final distanceApresDecoupe = chercherLongueDistanceSilver( nomRangSilver, nomRangSilverExtent)
                monPrint("{0} Création du rang {1} qualité {4} contient troncon(s) {2} couvre la distance à {3} %".\
                    format( E_RANG_MODELE, IDRangRempliZero, IDTronconBase, metriqueLigne["couvertureDistance"], metriqueLigne["couvertureQualité"]))

                # Différencier le nommage & repertoire pour permettre thematique auto
                if ALLER_RETOUR_DETAILLE:
                    allerRetour = metriqueLigne[ "sens"]
                    # Ajout d'ALLER/RETOUR mais aussi du troncon 
                    finNomRang = IDRangRempliZero + '_T' + IDTronconBase +  '_' + allerRetour + '_' + parcelle + EXT_geojson
                    nomRangTemp = os.path.join( repertoireLargeTemporaire, courtRepertoireLarge + "_A_DECOUPER_" + finNomRang)
                    if allerRetour == NOM_ALLER:
                        nomRangLarge = os.path.join( repertoireLargeAller, courtRepertoireLarge + '_' + finNomRang)
                    else:
                        nomRangLarge = os.path.join( repertoireLargeRetour, courtRepertoireLarge + '_' + finNomRang)
                else:
                    finNomRang = IDRangRempliZero + '_' + parcelle + EXT_geojson
                    nomRangTemp = os.path.join( repertoireLargeTemporaire, courtRepertoireLarge + "_A_DECOUPER_" + finNomRang)
                    nomRangLarge = os.path.join( repertoireLarge, courtRepertoireLarge + '_' + finNomRang)
                dfRang = pd.DataFrame( [[ IDRangRempliZero, IDTronconBase, metriqueLigne[ "épaisseur"], metriqueLigne[ "MAX_hrms"], \
                    parcelle, metriqueLigne[ "distance"], metriqueLigne[ "azimuthD"], metriqueLigne[ "orientation"], metriqueLigne[ "vitesse"], \
                        metriqueLigne[ "sens"], metriqueLigne[ "couvertureQualité"], metriqueLigne["couvertureDistance"], \
                        metriqueLigne["ratio50Distance"], metriqueLigne["ratio50Qualité"]]],\
                    columns = ['IdRang', 'IdTroncon', 'largeur', 'MAX_hrms', 'nom', 'distance', 'azimuthDegre', 'orientation', \
                                   'vitesse',  'sensAvancement',  'couvertureQualité', 'couvertureDistance', 'ratio50Distance', 'ratio50Qualité'])
                df2GeoJSON( dfRang,   nomRangTemp, rangElargiGeoJSON, 'Polygon')
                # Decoupage 
                traitementCouperRang( nomRangTemp, dictParcellesGeoJSON[ parcelle], nomRangLarge)
                if IDSuivant != IDTronconFinal:
                    numeroRang = numeroRang + 1
                    monPrint("{} Nouveau rang numéro {} pour le troncon {} et la parcelle {} :".format( E_RANG_NEW, numeroRang,  IDSuivant,  parcelle))
                    IDTronconBase=IDSuivant
                    dfPointBase = geoJSON2pd( uneSeriePoints)
                    metriqueTroncon, rangPossible, _ = dfPoints2Alignement( numeroRang, dfPointBase, None, None, ELARGISSEMENT_RANG, ALLONGE_RANG)
                    distanceDesTroncons=metriqueTroncon[ "distance"]
                rangTermine = False
        nombreTousLesRangs = nombreTousLesRangs + numeroRang
        creerRepertoireOptionTemporaire( repertoireTaitementOK)
    monPrint( "{} PASSE 2 : Fin extraction des {} rangs Modele".format( E_CLAP, nombreTousLesRangs),  T_OK)
    return nombreTousLesRangs
                  
def t1_NettoyerBruitPourCreerPointsLignesBrises( dfPointBrut, nomRepertoireCentipede, quelRendu, detailsStat=None):
    """
    PASSE1 : Passer en revu tous les points par parcelle et trouver les ruptures de temps (2 Secondes) ou de distance (2m) (< écartement rang ou de passage
    Nettoyage du bruit pour Troncon brisé valide
    """
    # Préparer le calcul de distance En GPS (mode LONG/LAT)
    distanceArea = preparerCalculDistance( str(ID_DESTINATION_CRS))
    # Passage initial sur les points intérieurs
    # Organiser les points en lignes probables dans la parcelle
    listeFidsPossibles = dfPointBrut.fid.values
    listeParcelle =   dfPointBrut.nom.values
    if len (listeFidsPossibles) <= 0:
        raise erreurCoherenceDF( listeParcelle[0], "?")
    minFIDPointsBruts = min( listeFidsPossibles) # Cas début est O
    maxFIDPointsBruts = max( listeFidsPossibles)
    monPrint( "Origine des points '{}' pour les parcelles, le nombre de points est {}. Le mini calculé est {}, les max est {}".\
        format( quelRendu, len( dfPointBrut), minFIDPointsBruts,  maxFIDPointsBruts))
    listeFidPointsBrises, listePointsBrises, listeDistancesBrisees, listeAzimuthsBrisesDegre, listeAzimuthsBrisesRadian, maLigneBrisee =[],  [], [], [], [], []
    nouvelleLigne = True
    IDSuiteBrisee=0
    IDPoint=0
    nombrePointsConserves=0
    for pointDF in dfPointBrut.itertuples():
        pointCourantWGS, pointCourantL93 = df2QgsPoint( pointDF)
        parcelleCourante = pointDF.nom
        fidCourant = pointDF.fid
        IDPoint=IDPoint+1
####        if IDPoint > 350:
####            break
####        else:
####            print( "Parcelle {}, fid {},id {}".format( parcelleCourante, fidCourant, IDPoint))
        #Assertion fid 
        if not fidCourant in listeFidsPossibles:
            print("Attention, pas dans LISTE : FID {} dont la position du point est {}".format( fidCourant, IDPoint))
            raise erreurCoherenceDF( parcelleCourante, IDSuiteBrisee)
        if nouvelleLigne:
            nouvelleLigne = False
            maLigneBrisee = []
            IDSuiteBrisee, nomPointBriseeInterieur, nomPointBriseMetrique,  nomPointBriseStat, \
                nomligneBriseeInterieure,  nomLigneBriseeMetrique,  nomLigneBriseeStat, nomPolygoneBrise = \
                incrementerNommages( IDSuiteBrisee, casTracking, nomRepertoireCentipede, parcelleCourante )
        try:
            pointSuivantFID = dfPointBrut[ ( dfPointBrut['fid'] == fidCourant + 1)]
            pointSuivantWGS, pointSuivantL93 = coordonnees2Point( pointSuivantFID.longitude.values[0], pointSuivantFID.latitude.values[0])
            pointSuivantExiste = True
        except IndexError:
            #print("Fin de recherche : dernier point OK {} fid {} premier KO {}".format( IDPoint, fidCourant, fidCourant + 1 ))
            pointSuivantExiste = False

        if pointSuivantExiste:
            # Calcul des écarts Temps et Distance et aussi Azimuth
            ecartTempsCapture = chercherEcartTemps( pointDF.jourHeure, pointSuivantFID.jourHeure.values[0])
            #BAD TEST lAzimuth   = pointCourantL93.azimuth( pointSuivantL93)
            parcelleSuivante = pointSuivantFID.nom.values[0]
            if distanceArea != None:
                laDistance = distanceArea.measureLine( pointCourantL93, pointSuivantL93)
                if laDistance < LIMITE_MIN_DISTANCES_ENTRE_DEUX_CAPTURES:
                    # On garde le point du redemarrage
#                    print("{} ARRET PROBABLE détecté par une distance entre points insuffisante {} < {} m : point ignoré {}".\
#                        format( E_INTERDIT, laDistance, LIMITE_MIN_DISTANCES_ENTRE_DEUX_CAPTURES, fidCourant))
                    continue
                lAzimuthRadian = distanceArea.bearing( pointCourantL93, pointSuivantL93)
                lAzimuthDegre = ( lAzimuthRadian * 180 / pi) % 360

            else:
                laDistance = 0
                lAzimuthRadian, lAzimuthDegre = None, None
        else:
            ecartTempsCapture=0
            laDistance = 0
            lAzimuthRadian, lAzimuthDegre = None, None
            parcelleSuivante = ""
        incrementerListePointsBrises( listeFidPointsBrises,  listePointsBrises, listeDistancesBrisees, listeAzimuthsBrisesDegre, listeAzimuthsBrisesRadian,   \
                                      fidCourant,            pointCourantWGS,   laDistance,            lAzimuthDegre,            lAzimuthRadian)
        # Identifier et tracer les causes de fin de ligneBrisée
        causeCoupureTroncon=""
        if pointSuivantExiste == False or ecartTempsCapture > LIMITE_MAX_SECONDES_ENTRE_DEUX_CAPTURES or  \
            laDistance > LIMITE_MAX_DISTANCES_ENTRE_DEUX_CAPTURES or parcelleSuivante != parcelleCourante:  # TODO pour une autre passe : mais aussi lAzimuthDegre > 2 ° = 
            if ecartTempsCapture > LIMITE_MAX_SECONDES_ENTRE_DEUX_CAPTURES:
                causeCoupureTroncon = causeCoupureTroncon  + " _ " + "TEMPS TROP LONG"
#                monPrint( "{} COUPURE {} ECART temps pour le point {}  est {}> {} secondes".\
#                    format( U_LIGNE, IDSuiteBrisee, fidCourant, ecartTempsCapture, LIMITE_MAX_SECONDES_ENTRE_DEUX_CAPTURES))
            if pointSuivantExiste == False:
                causeCoupureTroncon = causeCoupureTroncon + " _ " + "DERNIER POINT"
#                monPrint( "{} COUPURE {} TOUS les {} points sans coupure avant {} sont traités".format( U_LIGNE, IDSuiteBrisee, len( listeFidPointsBrises)-1, fidCourant))
            if laDistance > LIMITE_MAX_DISTANCES_ENTRE_DEUX_CAPTURES:
                causeCoupureTroncon = causeCoupureTroncon + " _ " + "POINT TROP ELOIGNE"
#                monPrint( "{} COUPURE {} distance vs dernier point {} est {} > {} mètres".\
#                    format( U_LIGNE, IDSuiteBrisee, fidCourant, laDistance, LIMITE_MAX_DISTANCES_ENTRE_DEUX_CAPTURES))
            if parcelleSuivante != parcelleCourante:
                causeCoupureTroncon = causeCoupureTroncon + " _ " + "FIN PARCELLE"
#                monPrint( "{} COUPURE {} vers une nouvelle parcelle {}".\
#                    format( U_LIGNE, IDSuiteBrisee, parcelleSuivante))
###            if causeCoupureTroncon[0:3] == " _ ":
###                causeCoupureTroncon = causeCoupureTroncon[3:]
###            if causeCoupureTroncon != "DERNIER POINT _ FIN PARCELLE":
###                monPrint( "{} COUPURE {} dans parcelle {} causes {}: Listes des {} points oubliés {} - {}".\
###                    format( U_LIGNE, IDSuiteBrisee, parcelleCourante, causeCoupureTroncon, len( listeFidPointsBrises), listeFidPointsBrises[0], listeFidPointsBrises[len( listeFidPointsBrises)-1]))                
            if len( listePointsBrises) > LIMITE_MIN_POINT_LIGNE:
                # Ecrire les points brisés 
                dfPointBrise= pd.DataFrame()
                #print( dfPointBrise.shape)
                                            # -1 car le dernier n'a pas tous les attributs
                for unFid in listeFidPointsBrises[:-1]:
                    dfPointBrise = dfPointBrise.append( dfPointBrut[( dfPointBrut['fid'] == unFid)])
                if len( dfPointBrise) == len( listeFidPointsBrises) -1:
                    dfPointBrise['distance']= listeDistancesBrisees[:-1]
                    dfPointBrise['azimuthDegre'] =  listeAzimuthsBrisesDegre[:-1]
                    dfPointBrise['azimuthRadian'] = listeAzimuthsBrisesRadian[:-1]
                else:
                    print( "{} BRISE PROBLEMATIQUE {}, Nombre ID {}, taille df {}, Nombre de points brisés {} et nombre Azimuth {} et nombre Distance {}".\
                        format( U_BRISE, IDSuiteBrisee, len( listeFidPointsBrises), len( dfPointBrise),  len( listePointsBrises), \
                        len( listeAzimuthsBrisesDegre), len( listeDistancesBrisees)))
                    raise erreurCoherenceDF( parcelleCourante, IDSuiteBrisee)
#####   Ecriture les points après le filtre             df2GeoJSON( dfPointBrise, nomPointBriseeInterieur)
                nouvelleLigne = True

                # Mémoriser métriques point pour filtrer lignes
                dfMetriquePoint = pd.DataFrame( list(zip(dfPointBrise['fid'], dfPointBrise['distance'], dfPointBrise['azimuthDegre'], dfPointBrise['hrms'])),\
                    columns = ['fid', 'distance','azimuthDegre', 'hrms'])
                if detailsStat != None:
                    dfMetriquePoint.to_csv( nomPointBriseMetrique)
                uneStatistique = dfMetriquePoint.describe(percentiles=[.1, .9])
                #if detailsStat != None:
                uneStatistique.to_csv( nomPointBriseStat)                    
                # Supression des azimuths extremes pour centrer
                dfPointFiltre = dfPointBrise[ ( dfPointBrise[ 'azimuthDegre'] < uneStatistique.azimuthDegre['90%'] ) & \
                                              ( dfPointBrise[ 'azimuthDegre'] > uneStatistique.azimuthDegre['10%'] )] # et &   ou |
                
                # Mémoriser métriques et stat pour renseigner chaque ligne
                dfMetriqueLigne = pd.DataFrame( list(zip(dfPointFiltre['fid'], dfPointFiltre['distance'], dfPointFiltre['azimuthDegre'], dfPointFiltre['hrms'])),\
                    columns = ['fid', 'distance','azimuthDegre', 'hrms' ])
                if detailsStat != None:
                    dfMetriqueLigne.to_csv( nomLigneBriseeMetrique)
                aStatLigne = dfMetriqueLigne.describe()
                #if detailsStat != None:
                aStatLigne.to_csv( nomLigneBriseeStat)                    
                
                # Ecrire la ligne brisée
                distanceBrisee=0
                listePointL93PourLigne, listePointGPSPourLigne = [], []
                for pointFiltre in dfPointFiltre.itertuples():
                    pointCourantGPS, pointCourantL93 = df2QgsPoint( pointFiltre)
                    listePointL93PourLigne.append( pointCourantL93)
                    listePointGPSPourLigne.append( pointCourantGPS)
                for unIdPoint in range( 0, len( listePointL93PourLigne) - 2):
                    #monPrint( "Point {} pour TRONCON brisé".format( unIdPoint, listePointPourLigne[ unIdPoint]))
                    pointCourant = listePointL93PourLigne[ unIdPoint]
                    pointSuivant = listePointL93PourLigne[ unIdPoint + 1]
                    distanceBrisee=distanceBrisee +  distanceArea.measureLine( pointCourant, pointSuivant)
                    # ?? En M et Z  listeDistancesBrisees[ unIDPoint ] et listeAzimuthsBrisesDegre[ unIDPoint]
                    pointCourant = listePointGPSPourLigne[ unIdPoint]
                    pointSuivant = listePointGPSPourLigne[ unIdPoint + 1]
                    maLigneBrisee.append([ pointCourant.x(), pointCourant.y()])
                    maLigneBrisee.append([ pointSuivant.x(), pointSuivant.y()])
                if distanceBrisee > LIMITE_MIN_LONGUEUR_LIGNE:
####  Supprime trop de ligne : and aStatLigne.azimuthDegre['std'] < LIMITE_MAX_STD_AIMUTH_LIGNES: 
                    nombrePointsConserves = nombrePointsConserves + len( maLigneBrisee)
                    dfLigneBrise = pd.DataFrame( [[distanceBrisee, IDSuiteBrisee, aStatLigne.fid['min'], aStatLigne.fid['max'],  \
                        aStatLigne.hrms['mean'], aStatLigne.hrms['max'], \
                        aStatLigne.azimuthDegre['mean'], aStatLigne.azimuthDegre['std'], (aStatLigne.azimuthDegre['mean'] - 90) % 180 ]],\
                          columns = ['distance','IdLigne', 'MIN_fid', 'MAX_fid', 'hrms', 'MAX_hrms', 'azimuthDegre','STD_azimuthDegre', 'orientation']) #, 'parcelle', 
                    df2GeoJSON( dfLigneBrise, nomligneBriseeInterieure, maLigneBrisee, 'LineString')
                    # On garde aussi les points filtrés
                    df2GeoJSON( dfPointFiltre, nomPointBriseeInterieur)
                else:
                    monPrint( "{} TRONCON {} TROP COURT <= {} aux oubliettes".format( U_CISEAUX, IDSuiteBrisee, LIMITE_MIN_LONGUEUR_LIGNE))
####                elif aStat.azimuthDegre['std'] >= LIMITE_MAX_STD_AIMUTH_LIGNES: 
####                    monPrint( "{} TRONCON {} TROP TOURNANT <= {}° est oubliée. Vérifiez le contour de la parcelle {}".\
####                        format( U_LIGNE_TOURNANTE, IDSuiteBrisee, LIMITE_MAX_STD_AIMUTH_LIGNES, parcelleCourante))
            else:
                # Trop peu de point on oublie cette ligne
                monPrint( "{} PORTION avant {} Trop peu de points < {} aux oubliettes".format( U_CISEAUX, IDSuiteBrisee, LIMITE_MIN_POINT_LIGNE))
            # Nouvelle ligne brisée
            nouvelleLigne = True
            listeFidPointsBrises, listePointsBrises, listeDistancesBrisees, listeAzimuthsBrisesDegre, listeAzimuthsBrisesRadian, maLigneBrisee =[], [], [], [], [], []
    monPrint( "{} PASSE 1 : Fin extraction des {} points bruts et création de {} troncons brisés soit {} points concervés {}".\
        format( E_CLAP, len( dfPointBrut), IDSuiteBrisee, nombrePointsConserves,  nombrePointsConserves/len( dfPointBrut)*100),  T_OK)
    return IDSuiteBrisee

# QGIS Processing
import warnings
from functools import wraps

def ignore_warnings(f):
    @wraps(f)   # see https://www.geeksforgeeks.org/python-functools-wraps-function/
    def inner(*args, **kwargs):
        with warnings.catch_warnings(record=True): # as w:
            warnings.simplefilter("ignore")
            response = f(*args, **kwargs)
        return response
    return inner
    
# Thanks to https://gis.stackexchange.com/questions/311957/importing-qgis3-processing-tools-in-standalone-script & https://spatialparalysis.xyz/
@ignore_warnings # Ignored because we want the output of this script to be a single value, and "import processing" is noisy
def initialisationProcessing():
    if MACHINE == 'Linux':
        CHEMIN_LIB_QGIS="/usr/lib/qgis" #" no /usr/bin  /usr/bin/qgis
        CHEMIN_PLUGIN_QGIS="/usr/share/qgis/python/plugins"
    else:
        print( "Quels chemins pour Qgis ?")
        exit(1)
    qgsApp = QgsApplication([], False)
    qgsApp.initQgis()
    path.append(CHEMIN_LIB_QGIS)
    path.append(CHEMIN_PLUGIN_QGIS)
    try:
        import processing
        from qgis.analysis import QgsNativeAlgorithms
        from processing.core.Processing import Processing
    except:
        erreurImport("Processing")    
    try:
        Processing.initialize()
        qgsApp.processingRegistry().addProvider(QgsNativeAlgorithms())
        #monPrint( "Après AddProvider {0}".format( len( QgsApplication.processingRegistry().providers())))
    except:
        erreurImport("Processing initialize")    
    return( qgsApp,  processing)
      
def traitementExploserParcelles( gpkgMP, repertoireSortie, listeParcelles, libelle=""):
    """ Creer un gpkg par parcelle puis un geojson du au "nombre d'ouvertures spatialite (GPKG) limité à 64
    {'INPUT':'XXX/MonParcellaire.gpkg|layername=parcelles', 'FIELD':'nom',
    'OUTPUT':'YYYY/PARCELLES'} """ 
    algo_name,  algo_simplifie ="qgis:splitvectorlayer",  "Decouper les parcelles ..."
    result = processing.run(algo_name, 
        {'INPUT':gpkgMP, 'FIELD':MonParcellaireNomAttribut,'OUTPUT':repertoireSortie})
    if result == None:
        monPrint( "Erreur bloquante durant processing {0}".format( algo_simplifie), T_ERR)
        erreur_traitement( "Pas de découpage GPKG")

    # Creation d'un geoJSON : bye pass du nombre d'ouvertures spatialite (GPKG) limité à 64 
    repertoireJSON = os.path.dirname( repertoireSortie)
    listetoutesParcellesGPKG = result[ 'OUTPUT_LAYERS']
    dictParcellesGeoJSON = {}
    for parcelle in listeParcelles:
        nomGeoJSON = os.path.join( repertoireJSON, parcelle + EXT_geojson)
        #monPrint("Parcelle {} transformé en geoJSON {}".format( parcelle,  nomGeoJSON))
        # Retrouver gpkg de la parcelle
        parcelleGPKG = parcelle + EXT_gpkg
        listeParcelleGPKG = [s for s in listetoutesParcellesGPKG if parcelleGPKG in s]
        # Assert
        if len( listeParcelleGPKG) != 1:
            monPrint( "Parcelle {} est plusieurs GPKG ? {}".format( parcelle, listeParcelleGPKG), T_ERR)
            monPrint( "Erreur bloquante durant processing {0}".format( "Retrouve GPKG"), T_ERR)
            erreur_traitement( "Retrouve GPKG")
        result = traitementReprojection( listeParcelleGPKG[0], nomGeoJSON)
        if result == None:
            monPrint( "Erreur bloquante durant processing {0}".format( "Création du geoJSON" + nomGeoJSON), T_ERR)
            erreur_traitement( "Création du geoJSON {}".format(nomGeoJSON))
        dictParcellesGeoJSON[ parcelle] = nomGeoJSON
    return dictParcellesGeoJSON

def traitementExtraireExtent( source, sortie, libelle=""):
    """ {'INPUT':source, 'OUTPUT':sortie}) """
    algo_name,  algo_simplifie ="qgis:polygonfromlayerextent",  "Extraire extent"
    result = processing.run(algo_name, 
        {'INPUT':source,'OUTPUT':sortie})
    if result == None:
        monPrint( "Erreur bloquante durant processing {0}".format( algo_simplifie), T_ERR)
        erreur_traitement(algo_name)
    return result
    
#def traitementExtraireSommets( source, sortie, libelle=""):
#    """ {'INPUT':source, 'OUTPUT':sortie}) """
#    algo_name,  algo_simplifie ="native:extractvertices",  "Extraire sommets"
#    result = processing.run(algo_name, 
#        {'INPUT':source,'OUTPUT':sortie})
#    if result == None:
#        monPrint( "Erreur bloquante durant processing {0}".format( algo_simplifie), T_ERR)
#        erreur_traitement(algo_name)
#    return result

def traitementCouperRang( source, parcelle, sortie, libelle=""):
    """ {'INPUT':source,'OVERLAY':parcelle,'OUTPUT':sortie}) """
    algo_name,  algo_simplifie ="native:clip",  "Découper rang par parcelle ..."
    result = processing.run(algo_name, 
        {'INPUT':source,'OVERLAY':parcelle,'OUTPUT':sortie})
    if result == None:
        monPrint( "Erreur bloquante durant processing {0}".format( algo_simplifie), T_ERR)
        erreur_traitement(algo_name)
    return result

def traitementJointureLocalisation(source, jointure, sortie, libelle=""):
    """ {'INPUT':source, 'JOIN':jointure,
    'PREDICATE':[0,1,3,5],'JOIN_FIELDS':['nom'],'METHOD':0,'DISCARD_NONMATCHING':True,'PREFIX':'',
    'OUTPUT':sortie} """
    algo_name,  algo_simplifie ="qgis:joinattributesbylocation",  "Jointure par localisation ..."
    # TODO ? orientatio ou tion 'JOIN_FIELDS':['nom' ,  'orientatio'],
    result = processing.run(algo_name, 
        {'INPUT': source, 'JOIN':jointure, 'PREDICATE':[0,1,3,5],'JOIN_FIELDS':['nom'],
            'METHOD':0,'DISCARD_NONMATCHING':True,'PREFIX':'', 'OUTPUT': sortie})
    if result == None:
        monPrint( "Erreur bloquante durant processing {0}".format( algo_simplifie), T_ERR)
        erreur_traitement(algo_name)
    return result

def traitementReprojection( source, sortie, EPSG=ID_DESTINATION_CRS, libelle=""):
    """( 'INPUT':source,
    'TARGET_CRS':QgsCoordinateReferenceSystem('EPSG:2154'),
    'OUTPUT':sortie})"""
    algo_name,  algo_simplifie ="native:reprojectlayer",  "Reprojection ..."
    EPSG_long="EPSG:"+str(EPSG)
    result = processing.run(algo_name, 
        {'INPUT': source, 'TARGET_CRS':QgsCoordinateReferenceSystem(EPSG_long), 'OUTPUT': sortie})
    if result == None:
        monPrint( "Erreur bloquante durant processing {0}".format( algo_simplifie), T_ERR)
        erreur_traitement(algo_name)
    return result

def traitementPolygone2LignePuisTampon( source, sortieLigne, sortie, distance=4, libelle=""):
    """("polygonstolines",
    {'INPUT':source,
    'OUTPUT':sortieLigne puis traitementTampon de +4
    dans sortie tampon})"""
    algo_name,  algo_simplifie ="qgis:polygonstolines",  "Polygone vers lignes ..."
    result = processing.run(algo_name, 
        {'INPUT': source, 'OUTPUT': sortieLigne})
    if result == None:
        monPrint( "Erreur bloquante durant processing {0}".format( algo_simplifie), T_ERR)
        erreur_traitement(algo_name)
    resultatLigne=traitementTampon( sortieLigne, sortie, distance)
    return resultatLigne

def traitementTampon( source, sortie, distance=-1, libelle=""):
    """("native:buffer",
    {'INPUT': XXX/Mon_Tom.gpkg|layername=point_acces',
    'DISTANCE':-2,'SEGMENTS':5,'END_CAP_STYLE':0,'JOIN_STYLE':0,'MITER_LIMIT':2,'DISSOLVE':False,
    'OUTPUT':ZZZ/PAP/acces.geojson'})"""
    algo_name,  algo_simplifie ="native:buffer",  "Tampon ..."
    result = processing.run(algo_name, 
        {'INPUT': source, \
        'DISTANCE':distance,'SEGMENTS':5,'END_CAP_STYLE':0,'JOIN_STYLE':0,\
        'MITER_LIMIT':2,'DISSOLVE':False, 'OUTPUT': sortie})
    if result == None:
        monPrint( "Erreur bloquante durant processing {0}".format( algo_simplifie), T_ERR)
        erreur_traitement(algo_name)
    return result
      


def preparerCalculDistance( monEPSG):
    """ Selon l'EPSG prépare l'objet QGIS distance area
    """
    spheroid = 'inconnu'
    if ( monEPSG == "2154"):
        spheroid = "GRS80"
    elif (monEPSG == "4326"):
        spheroid = "WGS84"
    else:
        # Pas de distance pour cet EPSG
        monPrint( "EPSG {0} n'est pas prévu dans {} : ni distance ni azimuth".format(monEPSG, APPLI_NOM_VERSION), T_WAR)
        return None
        
    laProjectionCRS = QgsCoordinateReferenceSystem.fromEpsgId( int(monEPSG))
    if not laProjectionCRS.isValid():
        monPrint( "Pas de distance valide pour cet EPSG : {0}".format(monEPSG), T_WAR)
        return None
    distancearea = QgsDistanceArea()
    distancearea.setSourceCrs( laProjectionCRS, QgsProject.instance().transformContext())            
    distancearea.setEllipsoid( spheroid)
    return distancearea
    
def chercherEcartTemps(avantSTR, apresSTR):
    """Passe en datetime pour ecart de temps"""
#    print("apres {} de type {} et avant {}".format(apresSTR,  type(apresSTR),  avantSTR))
    apres = datetime.strptime( apresSTR[0:19],'%Y/%m/%d %H:%M:%S')   # %-S Second as a decimal number.    %f microseconde attend 000800
    avant = datetime.strptime( avantSTR[0:19],'%Y/%m/%d %H:%M:%S')  # %-S Second as a decimal number.    %f microseconde attend 000800
    #avantMicro = dt1.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]+'Z'    
    return (apres - avant).total_seconds()

"""
# Entre Pandas à geojson, quels tampons, quels filtres, les jointures spatiales int et ext 
"""
def geoJSON2pd( nomGeoJSON, attributs="SEULEMENT", nomCourtChoisi="à controler dans votre journal d'exécution "):
    """ Pandas do not manage : Mixing dicts with non-Series
    Usage de json_normalize pour trouver attribut ou geometriee
            Type de geometrie Point seulement testée
    """
    with open( nomGeoJSON,'r') as f:
        jsonBrut = json.loads(f.read())
    dfQ1Brut = pd.DataFrame()
    try:
        dfQ1Brut = json_normalize( jsonBrut, record_path = ['features']) # , meta=['jourHeure', 'longitude',  'latitude',  'nom', 'hrms'], errors='ignore') #, [geometry])
        dfProperties = json_normalize( dfQ1Brut.properties)
        #monPrint( dfProperties.head())
    except AttributeError:
        raise incoherenceTraceCentipedeVignoble( nomCourtChoisi)
    if attributs == "SEULEMENT":
        return dfProperties
    else:
        # TODO Vx test et récupere le type geometry
        return dfProperties, "Point", json_normalize( dfQ1Brut.geometry)
        
def preparerEnteteGeoJSON( nomGeoJSON, EPSG):
    """Entete GeoJSON"""
    if EPSG == 4326:
        crsGeoJSON={ "type": "name", "properties": { "name": "urn:ogc:def:crs:OGC:1.3:CRS84" } }
    elif EPSG == 2154:
       crsGeoJSON = { "type": "name", "properties": { "name": "urn:ogc:def:crs:EPSG::2154" } }
    else:
        monPrint("EPSG {} non pris en charge par {}".format( EPSG, APPLI_NOM_VERSION))
        return None
        
    nomCourt = os.path.basename( nomGeoJSON)
    return {"type": "FeatureCollection", "name":nomCourt,  "crs": crsGeoJSON, "features": []}

def df2GeoJSON( df, nomGeoJSON,  laGeometrie=None,  geometrieType='PointLatLong', EPSG=4326, \
    listeNoire=['geometry', 'précision', 'ns','déviation Est', 'déviation Nord' , 'déviation Z']):
    """ A kind of geopandas to geojson, since gpd is not always inside QGIS distribution
        Habiller, traduire df (proche pos Centipede) en GeoJSON
        On conserve dans les attributs lat long H en WGS84 (la source)
        TODO Vx la géométrie est stockée dans le crs demandé
    """
    conteneurGeoJSON = preparerEnteteGeoJSON( nomGeoJSON, EPSG)
    lesColonneBrutes = list( df.columns)
    #monPrint("Les colonnes {}".format( lesColonneBrutes))
    if geometrieType in ['PointLatLong','Point', 'LineString', 'Polygon', 'MultiPolygon'] and conteneurGeoJSON != None:
        """Geométrie reconstruite à partir des longitudes et latitudes"""
        for monID, ligneDF in df.iterrows():
            # Paramétrer liste des attributs
            dicProperties={}
            for uneCol in lesColonneBrutes:
                if monID == 1 and uneCol == 'jourHeure':
                    monPrint("Format jourHeure {}".format( ligneDF[ uneCol]))
                if uneCol in listeNoire: # Blacklist
                    continue
                dicProperties[ uneCol] = ligneDF[ uneCol]
                if monID == 1 and uneCol == 'jourHeure':
                    monPrint("Format properties jourHeure {}".format( dicProperties[ uneCol]))
            if geometrieType == 'PointLatLong':
                formatLigneJSON = {"type": "Feature", "geometry": {"type": "Point", "coordinates": [ligneDF['longitude'], ligneDF['latitude']]}, \
                        "properties": dicProperties}
            elif geometrieType == 'LineString':
                formatLigneJSON = {"type": "Feature", "geometry": {"type": "LineString", "coordinates": laGeometrie}, \
                        "properties": dicProperties}
            elif geometrieType == 'Polygon':
                formatLigneJSON = {"type": "Feature", "geometry": {"type": "Polygon", "coordinates": laGeometrie}, \
                        "properties": dicProperties}
            elif geometrieType == 'MultiPolygon':
                formatLigneJSON = {"type": "Feature", "geometry": {"type": "MultiPolygon", "coordinates": laGeometrie}, \
                        "properties": dicProperties}
            conteneurGeoJSON['features'].append(formatLigneJSON)
    # TODO format de la geometrie POINT POINTZ MULTILINE
        if os.path.isfile( nomGeoJSON):
            os.remove( nomGeoJSON)
        with open(nomGeoJSON, 'w', encoding='utf-8') as fp:
            json.dump(conteneurGeoJSON, fp, ensure_ascii=False)  #,  indent=2
    else:
        monPrint("Géométrie {} non prise en charge par {} : pas de geoJSON {}".format( geometrieType, APPLI_NOM_VERSION, nomGeoJSON))
    return

def creerRepertoiresFinLarge( repertoireBase, rangOuInter, ALLER_RETOUR_DETAILLE=True):
    courtRepertoireFin = rangOuInter + SUFFIXE_FINS
    repertoireFin = os.path.join( repertoireBase, courtRepertoireFin)
    repertoireFinTemporaire = creerRepertoireOptionTemporaire( repertoireFin, True)
    creerQML( repertoireFin)
    courtRepertoireLarge = rangOuInter + SUFFIXE_LARGES
    repertoireLarge = os.path.join( repertoireBase, courtRepertoireLarge)
    repertoireLargeTemporaire = creerRepertoireOptionTemporaire( repertoireLarge, True)
    creerQML( repertoireLarge)
    if ALLER_RETOUR_DETAILLE:
        repertoireLargeAller = os.path.join( repertoireLarge, NOM_ALLER)
        creerRepertoireOptionTemporaire( repertoireLargeAller)
        creerQML( repertoireLargeAller)
        repertoireLargeRetour = os.path.join( repertoireLarge, NOM_RETOUR)
        creerRepertoireOptionTemporaire( repertoireLargeRetour)
        creerQML( repertoireLargeRetour)        
    return courtRepertoireFin, repertoireFin, repertoireFinTemporaire, courtRepertoireLarge, repertoireLarge, repertoireLargeTemporaire, repertoireLargeAller, repertoireLargeRetour

    
def creerTamponsOuCopieParcelles( parcelle, nomRepertoireCentipede, petitNomInterieur, petitNomExterieur, CALCUL_TAMPON="OK"):
    """Creer les tampons intérieur & exterieur des parcelles"""
    NomTamponLigneInterieure = os.path.join( nomRepertoireCentipede, petitNomInterieur + "_LIGNE" + EXT_geojson)
    NomTamponExterieur = os.path.join( nomRepertoireCentipede, petitNomExterieur + EXT_geojson)
    NomTamponInterieur = os.path.join( nomRepertoireCentipede, petitNomInterieur + EXT_geojson)
    creerRepertoireOptionTemporaire( nomRepertoireCentipede)

    if CALCUL_TAMPON == "OK":
        if not os.path.isfile( NomTamponInterieur):
            traitementTampon( parcelle, NomTamponInterieur) # poly -1            
        if not os.path.isfile( NomTamponExterieur):
            traitementPolygone2LignePuisTampon(NomTamponInterieur, NomTamponLigneInterieure, NomTamponExterieur) # ring -1 et + 3 soit 4
    else:
        # Copie sans tampon pour Cas de RUE par exemple
        if not os.path.isfile( NomTamponInterieur):
            traitementReprojection( parcelle, NomTamponInterieur, ID_DESTINATION_CRS)
        if not os.path.isfile( NomTamponExterieur):
            traitementReprojection( parcelle, NomTamponExterieur, ID_DESTINATION_CRS)
    return NomTamponInterieur, NomTamponExterieur
    
def chercherDernierPosCentipede( baseGPKG):
    # Choisir une trace pos et calculer HRMS
    nomRepertoirePos = os.path.join( baseGPKG, REPERTOIRE_CENTIPEDE_BRUT)
    nomPosRecherches = os.path.join( nomRepertoirePos, '*' + EXT_pos)
    listePosTriee = sorted(glob.glob( nomPosRecherches))
            #monPrint( "Liste des traces disponible {0}".format( listePosTriee))
            # TODO VxUI: permettre le choix d'une trace .pos (la derniere pour le moment)
    if len( listePosTriee) < 1:
        monPrint("Pas de solution.pos à traiter : l'extension MonParcellaire pointe vers {} et {}. \
            Avez-vous les données Centipède dans ce répertoire ?\n \
            Avez-vous bien défini le chemin vers le référentiel Mon Parcellaire".format( baseGPKG, REPERTOIRE_CENTIPEDE_BRUT ))
        return None, None, None
    nomCourt=os.path.basename( listePosTriee[-1])
    nomIdPos=nomCourt[ 10:24]
    return nomIdPos, nomCourt, listePosTriee[-1]

def chercherLignesBrisees( repertoireParcelle):
    repertoireLignes = os.path.join( repertoireParcelle, REPERTOIRE_CENTIPEDE_LIGNES)
    nomsRecherches = os.path.join( repertoireLignes, NOM_LIGNE_BRISE_INT + '*' + EXT_geojson)
    listeTriee = sorted(glob.glob( nomsRecherches))
    if len( listeTriee) < 1:
        monPrint("Pas de troncon brisé à traiter dans {}. \
            Avez-vous préparer des données Centipède dans ce répertoire ? ".format( repertoireParcelle ))
        return None, None
    return None, listeTriee

def chercherPointBrises( repertoireParcelle):
    repertoirePoints = os.path.join( repertoireParcelle, REPERTOIRE_CENTIPEDE_POINTS)
    nomsRecherches = os.path.join( repertoirePoints, NOM_POINT_BRISE_INT + '*' + EXT_geojson)
    listeTriee = sorted(glob.glob( nomsRecherches))
    if len( listeTriee) < 1:
        monPrint("Pas de point brisé à traiter dans {}. \
            Avez-vous préparer des données Centipède dans ce répertoire ? ".format( repertoireParcelle ))
        return None, None
    return None, listeTriee
    
#def chercherPolygonesBrises( repertoireParcelle):
#    repertoirePoints = os.path.join( repertoireParcelle, REPERTOIRE_CENTIPEDE_POLYGONES)
#    nomsRecherches = os.path.join( repertoirePoints, NOM_POLYGONE_BRISE_INT + '*' + EXT_geojson)
#    listeTriee = sorted(glob.glob( nomsRecherches))
#    if len( listeTriee) < 1:
#        monPrint("Pas de rang brisé à traiter dans {}. \
#            Avez-vous préparer des données Centipède dans ce répertoire ? ".format( repertoireParcelle ))
#        return None, None
#    return None, listeTriee

def chercherCasTrackingHauteur( casTrackingIndex, settings=None):
    # TODO VxUI: Recuperer casTrackingIndex dans settings
    LISTE_CASTER=[ "BATIV", "STLYS", "STLYS", "RAB01"]
    LISTE_CAS_TRACKING=[ SUFFIXE_INTER, SUFFIXE_INTER + "_AR", SUFFIXE_RANG, SUFFIXE_RUE]
    LISTE_REPERTOIRE=[ REPERTOIRE_CENTIPEDE_INTER_RANGS, REPERTOIRE_CENTIPEDE_INTER_RANGS, REPERTOIRE_CENTIPEDE_RANGS, REPERTOIRE_CENTIPEDE_POLYGONES]
    HAUTEUR_CAPTEUR=[ 2.25, 2.25, 2.50,  1.13 ]
    return LISTE_CAS_TRACKING[ casTrackingIndex], LISTE_REPERTOIRE[ casTrackingIndex], LISTE_CASTER[ casTrackingIndex], HAUTEUR_CAPTEUR[ casTrackingIndex]

def chercherDateCapture(df):
    listeDatesCaptures = df['jourDate'].unique()
    nombreDates=len( listeDatesCaptures)
    if nombreDates > 0:
        if nombreDates == 1:
            dateCaptures=listeDatesCaptures[0]
        else:
            dateCaptures="Entre le " + listeDatesCaptures[0][:5] + " et le " + listeDatesCaptures[-1] 
    else:
        dateCaptures="Inconnue"
    return dateCaptures
    
def filtreQualitesCentipede( nomPosChoisi, nomRepertoireCentipede):
    """ Lire dans pandas, renommer colonnes & calcul HRMS 
        Filtrer Q1 & Q2 et écriture geojson
    """
    # TODO Vx: Comparer dates : modification pos et date creation des geojson
    NOM_POINT_CENTIPEDE_Q1       = PREFIXE_NOM_POINT_CENTIPEDE + SUFFIXE_Q1 + EXT_geojson
    nomQ1_GeoJSON = os.path.join( nomRepertoireCentipede, NOM_POINT_CENTIPEDE_Q1)
    NOM_POINT_CENTIPEDE_Q2_PLUS  = PREFIXE_NOM_POINT_CENTIPEDE + SUFFIXE_Q2_PLUS + EXT_geojson
    nomQ2_GeoJSON = os.path.join( nomRepertoireCentipede, NOM_POINT_CENTIPEDE_Q2_PLUS)
    if os.path.isfile( nomQ2_GeoJSON) and os.path.isfile( nomQ2_GeoJSON):
        monPrint( "Pas de relecture du POS", T_WAR)
        return ["Inconnue"], nomQ1_GeoJSON, nomQ2_GeoJSON
        
    df = pd.read_csv (nomPosChoisi, skiprows=1, skipinitialspace=True, engine='python', sep=r'\s{1,}')   #  BAD :   sep="\s*[,]\s*"
    #monPrint( "{} mesures dans brutes".format ( len( df)), T_INF)
    lesDates=df['%'].unique()
    monPrint( "Dates concernés {}".format( lesDates), T_INF)
    # On traite df pour les formats de dates 
    df['jourDate']=df['%']
    df['jourHeure']=df['%']+ " " + df['UTC']
    #  Renomme & copie du strict nécessaire
    dfRen=df.rename( columns={ 'longitude(deg)':"longitude",  'latitude(deg)':"latitude", 'height(m)':"hauteur", \
                'sde(m)':"déviation Est", 'sdn(m)':"déviation Nord",  'sdu(m)':"déviation Z",\
                'Q':"précision"})
    dfMini=dfRen[[ 'jourDate', 'jourHeure', 'longitude', 'latitude', 'hauteur', 'précision',  'ns',  'déviation Est',  'déviation Nord', 'déviation Z']] # 'nom', 'nom_2', 'geometry']]
    #TODO V1.7: horizontal VRMS
    dfMini[ 'drms']=sqrt( 0.5 * ( dfMini[ 'déviation Est'] ** 2 + dfMini[ 'déviation Nord'] ** 2))
    dfMini[ 'hrms']=2*dfMini[ 'drms']

    df_Q1=dfMini[(dfMini["précision"] == 1)]
    fidINDEX = list( range( 0, len( df_Q1)))
    df_Q1['fid'] =fidINDEX
    # Q2 acception jusqu'à 30 cm de précision
    df_Q2=dfMini[(dfMini["précision"] <= 2) & (dfMini["hrms"] < FILTRE_Q2)]
    fidINDEX = list( range( 0, len( df_Q2)))
    df_Q2['fid'] =fidINDEX
    #monPrint( "{} dans Q1 & {} dans Q2_Plus pour {} brutes".format ( len( df_Q1), len( df_Q2),  len( df) ), T_INF)
    
    # Ecrire dans un geojson pour faire les jointures spatiales
    NOM_POINT_CENTIPEDE_Q1       = PREFIXE_NOM_POINT_CENTIPEDE + SUFFIXE_Q1 + EXT_geojson
    nomQ1_GeoJSON = os.path.join( nomRepertoireCentipede, NOM_POINT_CENTIPEDE_Q1)
    if not os.path.isfile( nomQ1_GeoJSON):
        df2GeoJSON( df_Q1, nomQ1_GeoJSON)
    if not os.path.isfile( nomQ2_GeoJSON):
        df2GeoJSON( df_Q2, nomQ2_GeoJSON)
    return lesDates, nomQ1_GeoJSON, nomQ2_GeoJSON

#def GPDjointureSpatialePointsBruts( NomTamponInterieur_WGS, NomTamponExterieur_WGS, nomQ1_GeoJSON, nomQ2_GeoJSON):
#    """ gpd sjoin """
#    print("GPD Jointure")
#    dfTamponInterieur = read_file( NomTamponInterieur_WGS)
#    dfQ1 = read_file( nomQ1_GeoJSON)
#    dfQ2 = read_file( nomQ2_GeoJSON)
#    #dfTamponExterieur = read_file( NomTamponExterieur_WGS)
#    # Recheche dfQ1int
#    dfQ1Int=sjoin( dfQ1, dfTamponInterieur, how='left') #, op=’intersect’)
#    dfQ2Int=sjoin( dfQ2, dfTamponInterieur, how='left') #, op=’intersect’)
#    monPrint( "Type Q1Int {} ".format( type(dfQ1Int)))
#    monPrint( "Taille de Q1Int {} ".format( len(dfQ1Int)))
#    return dfQ1Int, dfQ2Int, None

def QGISjointureSpatialePointsBruts( NomTamponInterieur_WGS, NomTamponExterieur_WGS, nomQ1_GeoJSON, nomQ2_GeoJSON):
    # jointure spatiale des points bruts par les parcelles
    nomRepertoireCentipede= os.path.dirname( nomQ1_GeoJSON)
    # Jointure des exterieurs avec les deux qualités
    NOM_POINT_CENTIPEDE_Q2_EXT = "POINTS" + SUFFIXE_EXT + SUFFIXE_Q2_PLUS + EXT_geojson
    nomPointsCentipedeQ2EXT = os.path.join( nomRepertoireCentipede, NOM_POINT_CENTIPEDE_Q2_EXT)
    if not os.path.isfile( nomPointsCentipedeQ2EXT):
        traitementJointureLocalisation( nomQ2_GeoJSON, NomTamponExterieur_WGS, nomPointsCentipedeQ2EXT)
    NOM_POINT_CENTIPEDE_Q2_INT = "POINTS" + SUFFIXE_INT + SUFFIXE_Q2_PLUS + EXT_geojson
    nomPointsCentipedeQ2INT = os.path.join( nomRepertoireCentipede, NOM_POINT_CENTIPEDE_Q2_INT)
    if not os.path.isfile( nomPointsCentipedeQ2INT):
        traitementJointureLocalisation( nomQ2_GeoJSON, NomTamponInterieur_WGS, nomPointsCentipedeQ2INT)
    # Jointure des intérieurs avec la qualité 1 uniquement
    NOM_POINT_CENTIPEDE_Q1_INT = "POINTS" + SUFFIXE_INT + SUFFIXE_Q1 + EXT_geojson
    nomPointsCentipedeQ1INT = os.path.join( nomRepertoireCentipede, NOM_POINT_CENTIPEDE_Q1_INT)
    if not os.path.isfile( nomPointsCentipedeQ1INT):
        traitementJointureLocalisation( nomQ1_GeoJSON, NomTamponInterieur_WGS, nomPointsCentipedeQ1INT)
    return nomPointsCentipedeQ1INT, nomPointsCentipedeQ2INT,  nomPointsCentipedeQ2EXT

def PARCELLESchoisirGeoJSONsInterieur( dfQ1Int, dfQ2Int, nomCourtChoisi, casTracking):
    """ Rendre un seul df pour quel parcelles de test"""
    dfRendu=dfQ2Int[ (dfQ2Int['nom']=="F0001CO21") | (dfQ2Int['nom']=="F0001CF52")] #SY13")]
    label=SUFFIXE_Q2[1:] + casTracking
    monPrint("TRAITEMENT {}, points intérieurs (la geométrie en L93 et lat/long/h restent en WGS84)".format( label),  T_WAR)
    return dfRendu, label, dfRendu['jourDate'].unique()

def choisirGeoJSONsInterieur( dfQ1Int, dfQ2Int, nomCourtChoisi, casTracking):
    """ Choisir la qualité selon la proportion de Q1, rend aussi les dates coorspondante à ce choix"""
    if dfQ2Int.empty:
        monPrint( "Pas de points Centipede dans vos parcelles. Les traces concernent-elles votre vignoble? Avez-vous créer vos parcelles dans le GPKG MonParcellaire en précisant la couche parcelles", T_ERR)
        erreur_traitement("Pas de points Centipede dans vos parcelles")
    # Stat sur qualité du POS
    lesParcelles=dfQ2Int['nom'].unique()
    monPrint( "Cette capture concerne {} parcelles : {}".format( len( lesParcelles), lesParcelles))
    totalPoints = len( dfQ2Int)
    Q1Points    = len( dfQ1Int)
    Q2Points    = totalPoints - Q1Points
    monPrint( "Répartition des précision de {} captures concernant de vos parcelles : {} % décimétrique et {} % centimétrique".\
        format ( totalPoints, round( Q2Points/totalPoints*100, 1),  round( Q1Points/totalPoints*100, 1)), T_INF)
    #  Rend Q1 si plus de 90 %
    if Q1Points/totalPoints*100 > 90:
        label=SUFFIXE_Q1[1:] + casTracking
        monPrint("TRAITEMENT {}, points intérieurs (la geométrie en L93 et lat/long/h restent en WGS84)".format( label), T_WAR)
        return dfQ1Int, label, dfQ1Int['jourDate'].unique()
    else:
        label=SUFFIXE_Q2[1:] + casTracking
        monPrint("TRAITEMENT {}, points Extérieur (la geométrie en L93 et lat/long/h restent en WGS84)".format( label), T_WAR)
        return dfQ2Int, label, dfQ2Int['jourDate'].unique()
    
def incrementerNommages( IDligne, casTracking, cheminParcelle, parcelle=None):
    """
        Incremente le compteur de ligne et point brisé
        Détruit le fichier si il existe déjà
    """
    repertoireParcelle = cheminParcelle
    creerRepertoireOptionTemporaire( cheminParcelle)
    if IDligne != None and parcelle != None:
        repertoireDeLaParcelle = os.path.join( cheminParcelle, parcelle)
        creerRepertoireOptionTemporaire( repertoireDeLaParcelle)
        repertoireParcelle=repertoireDeLaParcelle
        IDligne=IDligne+1
    
    if IDligne != None:
        repertoirePoint = os.path.join( repertoireParcelle, REPERTOIRE_CENTIPEDE_POINTS)
        IDLigneRempliZero=str(IDligne).zfill(4)
        repertoirePointTemporaire = creerRepertoireEtQML(  repertoirePoint, True)
        nomPointBriseeInterieur = os.path.join( repertoirePoint, NOM_POINT_BRISE_INT + IDLigneRempliZero + EXT_geojson)
        if os.path.isfile( nomPointBriseeInterieur):
            os.remove( nomPointBriseeInterieur)
        nomPointBriseMetrique = os.path.join( repertoirePointTemporaire, "METRIQUES_" +NOM_POINT_BRISE_INT +IDLigneRempliZero + EXT_csv)
        if os.path.isfile( nomPointBriseMetrique):
            os.remove( nomPointBriseMetrique)
        nomPointBriseeStat = os.path.join( repertoirePointTemporaire, "STATISTIQUES_"+ NOM_POINT_BRISE_INT + IDLigneRempliZero +  EXT_csv)
        if os.path.isfile( nomPointBriseeStat):
            os.remove( nomPointBriseeStat)
            
        repertoireLigne = os.path.join( repertoireParcelle, REPERTOIRE_CENTIPEDE_LIGNES)
        repertoireLigneTemporaire = creerRepertoireEtQML( repertoireLigne, True)
        nomligneBriseeInterieure = os.path.join( repertoireLigne, NOM_LIGNE_BRISE_INT + IDLigneRempliZero + EXT_geojson)
        if os.path.isfile( nomligneBriseeInterieure):
            os.remove( nomligneBriseeInterieure)
        nomLigneBriseeMetrique = os.path.join( repertoireLigneTemporaire, "METRIQUES_" +NOM_LIGNE_BRISE_INT + IDLigneRempliZero + EXT_csv)
        if os.path.isfile( nomLigneBriseeMetrique):
            os.remove( nomLigneBriseeMetrique)
        nomLigneBriseeStat = os.path.join( repertoireLigneTemporaire, "STATISTIQUES_"+ NOM_LIGNE_BRISE_INT + IDLigneRempliZero +  EXT_csv)
        if os.path.isfile( nomLigneBriseeStat):
            os.remove( nomLigneBriseeStat)
        return IDligne, nomPointBriseeInterieur, nomPointBriseMetrique, nomPointBriseeStat, \
                    nomligneBriseeInterieure,  nomLigneBriseeMetrique,  nomLigneBriseeStat, _
    else:
        # Dans chemin PARCELLE
        repertoireMultiPolygones = os.path.join( cheminParcelle, REPERTOIRE_CENTIPEDE_PARCELLES)
        if not os.path.isdir( repertoireMultiPolygones):
            creerRepertoireEtQML( repertoireMultiPolygones)
        nomPolygoneBrise = os.path.join( repertoireMultiPolygones, parcelle + "_" + casTracking + EXT_geojson)
        if os.path.isfile( nomPolygoneBrise):
            os.remove( nomPolygoneBrise)
        return _, _, _, _, _,  _,  _, nomPolygoneBrise
    
def incrementerListePointsBrises( listeFidPointsBrises, listePointsBrises, listeDistancesBrisees, listeAzimuthsBrisesDegre, listeAzimuthsBrisesRadian,  \
                                   IDPointsBruts,       pointCourant,      laDistance,            lAzimuthDegre,            lAzimuthRadian):
    """Stocker les points brisés ,fid & distance azimuth vers le prochain """
    listeFidPointsBrises.append( IDPointsBruts)
    listePointsBrises.append( pointCourant)
    listeDistancesBrisees.append( laDistance)    
    listeAzimuthsBrisesDegre.append( lAzimuthDegre)
    listeAzimuthsBrisesRadian.append( lAzimuthRadian)
    return
 
def df2ShapelyPoint( ligneDf, geometrie=None, mode="SHAPELY-LONG-LAT"):
    if mode == "SHAPELY-LONG-LAT":
        return coordonnees2Point( ligneDf.longitude, ligneDf.latitude,  None, mode)
    elif mode == "SHAPELY-LONG-LAT-HAUT":
        return coordonnees2Point( ligneDf.longitude, ligneDf.latitude, ligneDf.hauteur)
    else:
        monPrint( "Ce mode {} de récupération coordonnées n'est pas prévu dans {}".format( mode, APPLI_NOM_VERSION), T_WAR)
        return None
 
def df2QgsPoint( ligneDf, geometrie=None, mode="LONG-LAT"):
    if mode == "LONG-LAT":
        return coordonnees2Point( ligneDf.longitude, ligneDf.latitude)
    elif mode == "LONG-LAT-HAUT":
        return coordonnees2Point( ligneDf.longitude, ligneDf.latitude, ligneDf.hauteur)
    else:
        monPrint( "Ce mode {} de récupération coordonnées n'est pas prévu dans {}".format( mode, APPLI_NOM_VERSION), T_WAR)
        return None
        
def coordonnees2Point( long, lat, hauteur=None, mode="LONG-LAT", geometrie=None):
    """Tranforme coordonnées ou geom en QGSPoint ou shapely Point ...
       Usage de pyProj transform avec les variables globales PYPROJ_SOURCE_CRS et PYPROJ_DESTINATION_CRS
       Mode LONG-LAT transforme en QgsPointXY
       Mode LONG-LAT-HAUT transforme en QgsPointXYZ"""
    #print( "Dans coordonnees2Point mode {} : {} {}".format( mode, long, lat))
    if mode == "LONG-LAT" or mode == "SHAPELY-LONG-LAT":
        longDestination, latDestination = transform( PYPROJ_SOURCE_CRS, PYPROJ_DESTINATION_CRS, long, lat)
    if mode == "LONG-LAT":
        return QgsPointXY( long, lat),  QgsPointXY( longDestination, latDestination)
    elif mode == "SHAPELY-LONG-LAT":
        return Point( long, lat), Point( longDestination, latDestination)
    elif mode == "LONG-LAT-HAUT":
        # TODO V1.7: Calculer le Z = hauteur - 47 - hauteur du capteur
        longDestination, latDestination, hauteurDestination = transform( PYPROJ_SOURCE_CRS, PYPROJ_DESTINATION_CRS, long, lat, hauteur)
        return QgsPointXYZ( long, lat, hauteur),  QgsPointXYZ( longDestination, latDestination, hauteurDestination)
    else:
        monPrint( "Ce mode {} de récupération coordonnées n'est pas prévu dans {}".format( mode, APPLI_NOM_VERSION), T_WAR)
        return None

# Début script
monPrint( "Traitement des traces centipedes ... {} module {}".format( APPLI_NOM_VERSION,  __name__), T_OK)
qgsApp, processing =initialisationProcessing()

reglages = QgsSettings( APPLI_NOM)
baseGPKG = reglages.value( "MonParcellaire/repertoireGPKG", os.path.join( os.path.dirname(__file__), "data"))
nomVignoble = os.path.basename( baseGPKG)
#baseGPKG = "C:\SIG\MON_PARCELLAIRE_F0001" ou "C:\SIG\MP_F0001"

CHEMIN_GPKG, _, cheminCompletTable = nommagesGPKG( baseGPKG, MonParcellaire_PAR, MonParcellaire_GPKG, True)  
nomRepertoireCentipede = os.path.join( baseGPKG, REPERTOIRE_CENTIPEDE_W)
creerRepertoireOptionTemporaire( nomRepertoireCentipede)
repertoireDesParcelles = os.path.join( nomRepertoireCentipede, REPERTOIRE_CENTIPEDE_PARCELLES)
creerRepertoireEtQML( repertoireDesParcelles)
# Creer les tampon puis passer le referentiel en WGS84 pour travailler les points en projection native
if nomVignoble == "ST_HUBERT":
    NomTamponInterieur, NomTamponExterieur = creerTamponsOuCopieParcelles( cheminCompletTable, nomRepertoireCentipede, NOM_TAMPON_INTERIEUR, NOM_TAMPON_EXTERIEUR, "PAS_TAMPON")
else:
    NomTamponInterieur, NomTamponExterieur = creerTamponsOuCopieParcelles( cheminCompletTable, nomRepertoireCentipede, NOM_TAMPON_INTERIEUR, NOM_TAMPON_EXTERIEUR)

NomTamponInterieur_WGS = os.path.join( os.path.dirname( NomTamponInterieur), NOM_TAMPON_INTERIEUR + SUFFIXE_SOURCE_CRS + EXT_geojson)
NomTamponExterieur_WGS = os.path.join( os.path.dirname( NomTamponExterieur), NOM_TAMPON_EXTERIEUR + SUFFIXE_SOURCE_CRS + EXT_geojson)
if not os.path.isfile( NomTamponInterieur_WGS):
    traitementReprojection( NomTamponInterieur, NomTamponInterieur_WGS, ID_SOURCE_CRS)
if not os.path.isfile( NomTamponExterieur_WGS):
    traitementReprojection( NomTamponExterieur, NomTamponExterieur_WGS, ID_SOURCE_CRS)

nomIdPos, nomCourtChoisi, nomSolutionPosChoisie = chercherDernierPosCentipede(baseGPKG)     
monPrint( "Trace {0} est choisie : nom complet . Si vous voulez un autre traitement, renommer vos fichier bruts *.pos dans {1}".format( nomIdPos, nomSolutionPosChoisie))

# TODO Vx.UI dans un dictionnaire ou une regle de nommage des solution
casTracking, rangOuInterRang, nomCaster, hauteurCapteur = SUFFIXE_RANG, REPERTOIRE_CENTIPEDE_RANGS, "Inconnu", 0
if nomVignoble == "DEVT_PRECISION_CENTIPEDE":
    casTracking, rangOuInterRang,  nomCaster, hauteurCapteur= chercherCasTrackingHauteur( 0)
if nomVignoble == "ST_HUBERT":
    casTracking, rangOuInterRang,  nomCaster, hauteurCapteur= chercherCasTrackingHauteur( 3)
if nomVignoble == "MON_PARCELLAIRE_F0001" or  nomVignoble == "MON_PARCELLAIRE_F0001_IGN":
    if nomIdPos in ["20210205091248", "rgo_2021062306"]:
        casTracking, rangOuInterRang,  nomCaster, hauteurCapteur= chercherCasTrackingHauteur( 1)
    else:
        casTracking, rangOuInterRang,  nomCaster, hauteurCapteur= chercherCasTrackingHauteur( 2)
monPrint( "Vignoble {}. Cas tracking {} nom rang ou inter {} et caster {} hauteur capteur {}".format( nomVignoble, casTracking, rangOuInterRang, nomCaster, hauteurCapteur ))
# TODO : attraper les cas non prévu dans chercherCasTrackingHauteur

repertoireCochantFiltre = os.path.join( nomRepertoireCentipede, "TRAITE_FILTRE_QUALITE")
#if not os.path.isdir( repertoireCochantFiltre):
_, nomQ1_GeoJSON, nomQ2_GeoJSON = filtreQualitesCentipede( nomSolutionPosChoisie, nomRepertoireCentipede)
monPrint("Filtrage des données capturées",  T_OK)
#if MACHINE != "Linux":
nomPointsCentipedeQ1INT, nomPointsCentipedeQ2INT, nomPointsCentipedeQ2EXT =\
        QGISjointureSpatialePointsBruts( NomTamponInterieur_WGS, NomTamponExterieur_WGS, nomQ1_GeoJSON, nomQ2_GeoJSON)
#else:
#    dfQ1Int, dfQ2Int, _ = GPDjointureSpatialePointsBruts( NomTamponInterieur_WGS, NomTamponExterieur_WGS, nomQ1_GeoJSON, nomQ2_GeoJSON)
monPrint("Jointure spatiale (extraction) des points dans vos parcelles",  T_OK)

#if MACHINE != "Linux":
# Ouvrir les geoJSON Intérieur (les Ext serait necessaires pour l'identification de rupture)
dfQ1Int = geoJSON2pd( nomPointsCentipedeQ1INT, "SEULEMENT", nomCourtChoisi)
dfQ2Int = geoJSON2pd( nomPointsCentipedeQ2INT)
dfPointBrut, quelRendu, listeDatesCaptures = choisirGeoJSONsInterieur( dfQ1Int, dfQ2Int, nomCourtChoisi, casTracking)
monPrint("Choix de la qualité des {} points {} pour une trace {} réalisée les {} ".format( len(dfPointBrut), quelRendu[ 0:2], casTracking, listeDatesCaptures),  T_OK)
if len( dfPointBrut) > 2:
    creerRepertoireOptionTemporaire( repertoireCochantFiltre)
###i=0
###for pointDF in dfPointBrut.itertuples():
###    i=i+1
###    if i >10:
###        break
###    monPrint( "Point brut apres jointure {}".format( pointDF.jourHeure))
                                                                      
# PASSE 1 : Passer en revue tous les points par parcelle et trouver les ruptures de temps (2 Secondes) ou de distance (2m) (< écartement rang ou de passage
repertoireCochantPasse1 = os.path.join( nomRepertoireCentipede, "TRAITE_PASSE_1")
if not os.path.isdir( repertoireCochantPasse1):
    nombreLignesBrisees = t1_NettoyerBruitPourCreerPointsLignesBrises( dfPointBrut, nomRepertoireCentipede, quelRendu)
    if nombreLignesBrisees > 2:
        creerRepertoireOptionTemporaire( repertoireCochantPasse1)
else:
    monPrint( "{} Pas extraction des Points & Lignes brisées".format( T_WAR))
    
# PASSE 2 : Regrouper points des troncons et définir un rang modèle
repertoireCochantPasse2 = os.path.join( nomRepertoireCentipede, "TRAITE_PASSE_2")
if not os.path.isdir( repertoireCochantPasse2):
    nombreTousLesRangs = t2_CreerRailPassage( dfPointBrut, nomRepertoireCentipede, repertoireDesParcelles, cheminCompletTable, rangOuInterRang)
    if nombreTousLesRangs > 10:
        creerRepertoireOptionTemporaire( repertoireCochantPasse2)
    else:
        print("Nombre de rangs {}".format( nombreTousLesRangs))
else:
    monPrint( "{} Pas extraction des Polygones Rangs".format( T_WAR))

# Renommer le .pos & repertoireCible
if os.path.isdir( repertoireCochantPasse1) and os.path.isdir( repertoireCochantPasse2): ### and os.path.isdir( repertoireCochantPasse3):
    os.rename( nomSolutionPosChoisie, nomSolutionPosChoisie + "_TRAITE_PASSE_1_2")
    os.rename( nomRepertoireCentipede, os.path.join( baseGPKG, REPERTOIRE_CENTIPEDE_TRAITEMENT + "_" + quelRendu ))
#Fin QGIS
qgsApp.exitQgis()
monPrint( "{} Fin du traitement de la trace Centipede {}. Merci à Centipede {}".format( E_TRAJET, nomCourtChoisi,  E_CENTIPEDE))
