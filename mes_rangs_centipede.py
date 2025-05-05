# -*- coding: utf-8 -*-
"""
/***************************************************************************
 mes_rangs_centipede
                                 A QGIS plugin
 Centipede script QGIS & pandas

Fonctions organisées en deux groupes qui peuvent être utilisées par le script ou l'extension
    - Traitements (usant de QGIS Processing) avec l'initialisation pour script-processing
    - Généralistes, Pandas à geojson tampon filtre jointure 

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
#from initialisation_var_exception import *
#from qgis.core import ( QgsProject, QgsCoordinateReferenceSystem, 
#   QgsPointXY, QgsDistanceArea)
#
#def creerPointsLignesBrises( dfPointBrut, quelRendu="Q1", detailsStat=None):
#    """
#    PASSE1 : Passer en revu tous les points par parcelle et trouver les ruptures de temps (2 Secondes) ou de distance (2m) (< écartement rang ou de passage
#    """
#    # Préparer le calcul de distance En GPS (mode LONG/LAT)
#    EPSG="4326"
#    distanceArea = preparerCalculDistance( EPSG)
#    # Passage initial sur les points intérieurs de qualité 1 (< mm)
#    # Organiser les points en lignes probables dans la parcelle
#    IDPointsBruts = min( dfPointBrut.index.values) # Cas début est O
#    monPrint( "Origine des points '{}' pour les parcelles, le nombre de points est {}. Le mini calculé est {}".\
#        format( quelRendu, len( dfPointBrut), IDPointsBruts))
#
#    IDPointsBrises, parcellesBrises, pointsBrises, distancesBrises, azimuthsBrises, maLigneBrisee =[], [], [], [], [], []
#    nouvelleLigne = True
#    IDSuiteBrisee=0
#    for pointDF in dfPointBrut.itertuples():
#        #print( "==> IDPoint {} index tuples{} et tuple complet {}".format( IDPointsBruts, pointDF.Index,  pointDF))
#        if nouvelleLigne:
#            nouvelleLigne = False
#            maLigneBrisee = []
#            IDSuiteBrisee, nomPointBriseeInterieur, nomligneBriseeInterieure,  nomLigneBriseeMetrique,  nomLigneBriseeStat,nomLigneCompleteInterieure = \
#                incrementerLigneEtFichier( IDSuiteBrisee, repertoireDesParcelles, casTracking)
#        pointCourant = QgsPointXY( pointDF.longitude, pointDF.latitude)
#        parcelleCourante = pointDF.nom
#        idCourant = pointDF.Index
#        try:
#            pointSuivantExiste = dfPointBrut.datetime[ idCourant + 1]
#            pointSuivant = QgsPointXY( dfPointBrut.longitude[ idCourant + 1], dfPointBrut.latitude[ idCourant + 1])
#            pointSuivantExiste = True
#        except KeyError:
#            print("Fin de recherche : dernier point OK {} premier KO {}".format( idCourant, idCourant + 1 ))
#            pointSuivantExiste = False
#
#        if pointSuivantExiste:
#            # Calcul des écarts Temps et Distance et aussi Azimuth
#            ecartTemps = dfPointBrut.datetime[ idCourant + 1] - pointDF.datetime
#            ecartTempsCapture = ecartTemps.total_seconds()
#            lAzimuth   = pointCourant.azimuth( pointSuivant)
#            parcelleSuivante = dfPointBrut.nom[ idCourant + 1]
#            if distanceArea != None:
#                laDistance = distanceArea.measureLine( pointCourant, pointSuivant)
#            else:
#                laDistance = 0
#            #monPrint( "Par rapport au suivant, le point {} a une distance de {} m, un azimuth {} et un ecard en seconde {}".\
#            #    format(IDPointsBruts,laDistance, lAzimuth, ecartTempsCapture), T_INF)
#            incrementerPointsBrises( IDPointsBrises,  parcellesBrises,  pointsBrises, distancesBrises, azimuthsBrises, \
#                                     idCourant,       parcelleCourante, pointCourant, laDistance, lAzimuth)
#        else:
#            ecartTempsCapture=0
#            laDistance = 0
#            incrementerPointsBrises( IDPointsBrises,  parcellesBrises,  pointsBrises, distancesBrises, azimuthsBrises, \
#                                     idCourant,       parcelleCourante, pointCourant, 0,               0)
#        # Identifier et tracer les causes de fin de ligneBrisée
#        if pointSuivantExiste == False or ecartTempsCapture > MAX_SECONDES_ENTRE_DEUX_CAPTURES or  \
#            laDistance > MAX_DISTANCES_ENTRE_DEUX_CAPTURES or parcelleSuivante != parcelleCourante:  # TODO: pour une autre passe : mais aussi lAzimuth > 2 ° = 
#############            if ecartTempsCapture > MAX_SECONDES_ENTRE_DEUX_CAPTURES:
#############                monPrint( "{} COUPURE {} ECART temps pour le point {}  est {}> {} secondes".\
#############                    format( U_LIGNE, IDSuiteBrisee, IDPointsBruts, ecartTempsCapture, MAX_SECONDES_ENTRE_DEUX_CAPTURES))
#############            if pointSuivantExiste == False:
#############                monPrint( "{} COUPURE {} TOUS les points {} sont traités".format( U_LIGNE, IDSuiteBrisee, IDPointsBruts))
#############            if laDistance > MAX_DISTANCES_ENTRE_DEUX_CAPTURES:
#############                monPrint( "{} COUPURE {} distance vs dernier point {} est {} > {} mètres".\
#############                    format( U_LIGNE, IDSuiteBrisee, IDPointsBruts, laDistance, MAX_DISTANCES_ENTRE_DEUX_CAPTURES))
#############            if parcelleSuivante != parcelleCourante:
#############                monPrint( "{} COUPURE {} nouvelle parcelle {}".\
#############                    format( U_LIGNE, IDSuiteBrisee, parcelleSuivante))
#                
#            if len( pointsBrises) > MIN_POINT_LIGNE:                        
#                # Ecrire les points brises 
#                debut=IDPointsBrises[0]
#                fin=IDPointsBrises[-1]
#                dfPointBrise=dfPointBrut[ debut:fin]
#                dfPointBrise.reindex( list( range( debut, fin)))
#                print( "{} BRISE {}, Nombre de points brisés {} et nombre Azimuth {} et nombre Distance {}".\
#                    format( U_BRISE, IDSuiteBrisee,  len( pointsBrises), len(azimuthsBrises),  len(distancesBrises)))
#                dfPointBrise['IdPoint'] = list( range( debut, fin))
#                dfPointBrise['Distance']= distancesBrises[:-1]
#                dfPointBrise['Azimuth'] = azimuthsBrises[:-1]
#                dfPointBrise['Parcelle']= parcellesBrises[:-1]
#                dfPos2GeoJSON( dfPointBrise, nomPointBriseeInterieur)
#                nouvelleLigne = True
#
#                # Mémoriser métriques et stat pour chaque ligne
#                dfMetrique = pd.DataFrame( list(zip(dfPointBrise['Distance'], dfPointBrise['Azimuth'], dfPointBrise['hrms'],  dfPointBrise['drms'])),\
#                    columns = ['Distance','Azimuth', 'hrms', 'drms'])
#                if detailsStat != None:
#                    dfMetrique.to_csv( nomLigneBriseeMetrique)
#                aStat = dfMetrique.describe()
#                #if detailsStat != None:
#                aStat.to_csv( nomLigneBriseeStat)                    
#
#                # TODO Assert sur les points dans la même parcelle
#                
#                # Ecrire la ligne brisée
#                distanceBrisee=0
#                for unIDPoint in range( 0, len( pointsBrises) - 2):
#                    #monPrint( "{} LIGNE brisé {} demarre {}".format(U_BRISE, IDSuiteBrisee, unIDPoint))
#                    distanceBrisee=distanceBrisee + distancesBrises[ unIDPoint]
#                    # TODO: TEST ligne brisée ? portant les azimuths en M
#                    # En M et Z  distancesBrises[ unIDPoint ] et azimuthsBrises[ unIDPoint]
#                    maLigneBrisee.append([pointsBrises[ unIDPoint].x(), pointsBrises[ unIDPoint].y()])
#                    maLigneBrisee.append([pointsBrises[ unIDPoint+1].x(), pointsBrises[ unIDPoint+1].y()])
#                dfLigneBrise = pd.DataFrame( [[distanceBrisee, IDSuiteBrisee, aStat.drms['mean'], aStat.hrms['mean'], aStat.hrms['max'], aStat.Azimuth['mean'], aStat.Azimuth['std']  ]],\
#                        columns = ['Distance','IdLigne', 'drms', 'hrms', 'MAX_hrms', 'Azimuth','STD_Azimuth']) #, 'parcelle', 
#                dfPos2GeoJSON( dfLigneBrise, nomligneBriseeInterieure, maLigneBrisee, 'LineString')
#
#                # Et la ligne modelisée (ou amplifiée)
#    #####  gpd              monPointDebut=QgsPointXY(centroideDebut.x, centroideDebut.y)
#    #####                centroideFin=centroidePrecedent[IDPointsBruts-1]
#    #####                monPointFin=QgsPointXY(centroideFin.x, centroideFin.y)
#    #####                maLigne = LineString([(monPointDebut.x(), monPointDebut.y()), (monPointFin.x(), monPointFin.y())])
#    #                pointFin = pointsBrises[-1]
#    #                maLigne = LineString([(pointDebut.x(), pointDebut.y()), (pointFin.x(), pointFin.y())])
#    #                # TODO: Rallonger la ligne 
#    ###                gdfLigne.geometry= [ maLigne ]
#    ###                gdfLigne[ "nom" ]=parcelle+SEP_U+str( IDligne)
#    ###                gdfLigne[ "ID"]=str( IDligne)
#    ###                gdfLigne[ "idid"]=str( IDPointsBruts-1) + " - " + str( IDDebut)
#    ###                # Trace date heure de capture
#    ###                gdfLigne[ "capture"]=str( dateDebut)+ " - " + str(tempsPrecedent)
#    ###                # TODO: length ? vitesse ? et hauteur des points
#    ###                gdfLigne.to_file(nomLigneCompleteInterieure, driver=DRIVER_GEOJSON)
#            else:
#                # Trop peu de point on oublie cette ligne
#                monPrint( "{} PORTION avant {} Trop peu de points < {} sont oubliés".format( U_CISEAUX, IDSuiteBrisee, MIN_POINT_LIGNE))
#            # Nouvelle ligne brisée
#            IDPointsBrises, parcellesBrises, pointsBrises, distancesBrises, azimuthsBrises, maLigneBrisee =[], [], [], [], [], []
#    return
#
#""" TRAITEMENTS """
#def traitementJointureLocalisation(source, jointure, sortie, libelle=""):
#    """ {'INPUT':source, 'JOIN':jointure,
#    'PREDICATE':[0,1,3,5],'JOIN_FIELDS':['nom'],'METHOD':0,'DISCARD_NONMATCHING':True,'PREFIX':'',
#    'OUTPUT':sortie} """
#    algo_name,  algo_simplifie ="qgis:joinattributesbylocation",  "Jointure par localisation ..."
#    # TODO: ? orientatio ou tion
#    result = processing.run(algo_name, 
#        {'INPUT': source, 'JOIN':jointure, 'PREDICATE':[0,1,3,5],'JOIN_FIELDS':['nom',  'orientatio'],'METHOD':0,'DISCARD_NONMATCHING':True,'PREFIX':'', 'OUTPUT': sortie})
#    if result == None:
#        monPrint( "Erreur bloquante durant processing {0}".format( algo_simplifie), T_ERR)
#        erreur_traitement(algo_name)
#    return result
#
#def traitementReprojection(source, sortie, libelle=""):
#    """( 'INPUT':source,
#    'TARGET_CRS':QgsCoordinateReferenceSystem('EPSG:2154'),
#    'OUTPUT':sortie})"""
#    algo_name,  algo_simplifie ="native:reprojectlayer",  "Reprojection ..."
#    result = processing.run(algo_name, 
#        {'INPUT': source, 'TARGET_CRS':QgsCoordinateReferenceSystem('EPSG:2154'), 'OUTPUT': sortie})
#    if result == None:
#        monPrint( "Erreur bloquante durant processing {0}".format( algo_simplifie), T_ERR)
#        erreur_traitement(algo_name)
#    return result
#
#def traitementTampon(source, sortie, distance=-1, libelle=""):
#    """("native:buffer",
#    {'INPUT': XXX/Mon_Tom.gpkg|layername=point_acces',
#    'DISTANCE':-2,'SEGMENTS':5,'END_CAP_STYLE':0,'JOIN_STYLE':0,'MITER_LIMIT':2,'DISSOLVE':False,
#    'OUTPUT':ZZZ/PAP/acces.geojson'})"""
#    algo_name,  algo_simplifie ="native:buffer",  "Tampon ..."
#    result = processing.run(algo_name, 
#        {'INPUT': source, \
#        'DISTANCE':distance,'SEGMENTS':5,'END_CAP_STYLE':0,'JOIN_STYLE':0,\
#        'MITER_LIMIT':2,'DISSOLVE':False, 'OUTPUT': sortie})
#    if result == None:
#        monPrint( "Erreur bloquante durant processing {0}".format( algo_simplifie), T_ERR)
#        erreur_traitement(algo_name)
#    return result
#    
#
#def preparerCalculDistance( monEPSG):
#    """ Selon l'EPSG prépare l'objet QGIS distance area
#    """
#    spheroid = 'inconnu'
#    if ( monEPSG == "2154"):
#        spheroid = "GRS80"
#    elif (monEPSG == "4326"):
#        spheroid = "WGS84"
#    else:
#        # Pas de distance pour cet EPSG
#        monPrint( "EPSG {0} n'est pas prévu dans {} : pas de distance ".format(monEPSG, APPLI_NOM_VERSION), T_WAR)
#        return None
#        
#    laProjectionCRS = QgsCoordinateReferenceSystem.fromEpsgId( int(monEPSG))
#    if not laProjectionCRS.isValid():
#        monPrint( "Pas de distance valide pour cet EPSG : {0}".format(monEPSG), T_WAR)
#        return None
#    distancearea = QgsDistanceArea()
#    distancearea.setSourceCrs( laProjectionCRS, QgsProject.instance().transformContext())            
#    distancearea.setEllipsoid( spheroid)
#    return distancearea
#
#def garderAzimuthCentres( df):
#    """
#    Extraction des azimuth les plus centrés 0,20-0,8
#    """
#    try:
#        low, high = df.Azimuth.quantile([0.20,0.80])
#    except:
#        my_print("As-tu fait tourné Ma_Vignette_Azimuth ?", "Attention")
#        raise    
#    dfCentreAzimuth=df.query('{low}<Azimuth<{high}'.format(low=low,high=high))
#    monPrint("LIGNE_AZIMUTH {} a {} dans les quartiles sup à {} et inf à {} ".\
#        format(a_par.n, len( dfCentreAzimuth), round(low, 2), round(high, 2), "Statistique"))
#    return dfCentreAzimuth
#
#"""
## Entre Pandas à geojson, quels tampons, quels filtres, les jointures spatiales int et ext 
#"""
#def geoJSON2pd( nomGeoJSON, attributs="SEULEMENT"):
#    """ Pandas do not manage : Mixing dicts with non-Series
#    Usage de json_normalize pour trouver attribut ou geometriee
#    Création d'une datetime
#            Type de geometrie Point seulement testée
#    """
#    with open( nomGeoJSON,'r') as f:
#        jsonBrut = json.loads(f.read())
#    dfQ1Brut = json_normalize( jsonBrut, record_path = ['features']) # , meta=['jourHeure', 'longitude',  'latitude',  'nom', 'hrms'], errors='ignore') #, [geometry])
#    dfProperties = json_normalize( dfQ1Brut.properties)
#    #TODO TESTER millisecondes avec pd
#    dfProperties['datetime'] = dfProperties['jourHeure'].apply(lambda x: datetime.strptime(x[0:19],'%Y/%m/%d %H:%M:%S'))   # %-S Second as a decimal number.    %f microseconde attend 000800
#    if attributs == "SEULEMENT":
#        return dfProperties
#    else:
#        # TODO test et récupere le type geometry
#        return dfProperties, "Point", json_normalize( dfQ1Brut.geometry)
#        
#def preparerEnteteGeoJSON( nomGeoJSON, EPSG):
#    """Entete GeoJSON"""
#    if EPSG == 4326:
#        crsGeoJSON={ "type": "name", "properties": { "name": "urn:ogc:def:crs:OGC:1.3:CRS84" } }
#    elif EPSG == 2154:
#       crsGeoJSON = { "type": "name", "properties": { "name": "urn:ogc:def:crs:EPSG::2154" } }
#    else:
#        monPrint("EPSG {} non pris en charge par {}".format( EPSG, APPLI_NOM_VERSION))
#        return None
#        
#    nomCourt = os.path.basename( nomGeoJSON)
#    return {"type": "FeatureCollection", "name":nomCourt,  "crs": crsGeoJSON, "features": []}
#
#def dfPos2GeoJSON( df, nomGeoJSON,  laGeometrie=None,  geometrieType='PointLatLong', EPSG=4326, listeNoire=['geometry', 'datetime', 'précision', 'ns','déviation Est', 'déviation Nord' , 'déviation Z']):
#    """ A kind of geopandas to geojson, since gpd is not always inside QGIS distribution
#        Habiller, traduire df (proche pos Centipede) en GeoJSON
#        On conserve dans les attributs lat long H en WGS84 (la source)
#        TODO la géométrie est stockée dans le crs demandé
#    """
#    conteneurGeoJSON = preparerEnteteGeoJSON( nomGeoJSON, EPSG)
#    lesColonneBrutes = list( df.columns)
#    #monPrint("Les colonnes {}".format( lesColonneBrutes))
#    if geometrieType in ['PointLatLong','Point', 'LineString'] and conteneurGeoJSON != None:
#        """Geométrie reconstruite à partir des longitude et latitude"""
#        for monID, ligneDF in df.iterrows():
#            # TODO: traduire dans crs de WGS en EPSG   #if EPSG != 4326:
#            # Paramétrer liste des attributs
#            dicProperties={}
#            for uneCol in lesColonneBrutes:
#                if uneCol in listeNoire: # Blacklist
#                    # TODO: ? datetime dans un objet
#                    continue
#                dicProperties[ uneCol] = ligneDF[ uneCol]
#            if geometrieType == 'PointLatLong':
#                #formatLigneJSON = {"type": "Feature", "geometry": {"type": "Point", "coordinates": [ligneDF.longitude, ligneDF.latitude]}, \
#                formatLigneJSON = {"type": "Feature", "geometry": {"type": "Point", "coordinates": [ligneDF['longitude'], ligneDF['latitude']]}, \
#                        "properties": dicProperties}
#            if geometrieType == 'LineString':
#                formatLigneJSON = {"type": "Feature", "geometry": {"type": "LineString", "coordinates": laGeometrie}, \
#                        "properties": dicProperties}
#            conteneurGeoJSON['features'].append(formatLigneJSON)
#
#        if os.path.isfile( nomGeoJSON):
#            os.remove( nomGeoJSON)
#        with open(nomGeoJSON, 'w', encoding='utf-8') as fp:
#            json.dump(conteneurGeoJSON, fp, ensure_ascii=False)  #,  indent=2
#    # TODO format de la geometrie POINT POINTZ LINE MULTILINE POLYGON
#    else:
#        monPrint("Géométrie {} non prise en charge par {} : pas de geoJSON {}".format( geometrieType, APPLI_NOM_VERSION, nomGeoJSON))
#    return
#    
#def creerTamponsParcelles( baseGPKG, parcelle, NomRepertoireCentipede):
#    """Creer les tampons intérieur & exterieur des parcelles"""
#    NomTamponExterieur = os.path.join( NomRepertoireCentipede, NOM_TAMPON_EXTERIEUR)
#    NomTamponInterieur = os.path.join( NomRepertoireCentipede, NOM_TAMPON_INTERIEUR)
#    if not os.path.isdir( NomRepertoireCentipede):
#        os.mkdir(NomRepertoireCentipede)
#
#    if not os.path.isfile( NomTamponExterieur):
#        traitementTampon( parcelle, NomTamponExterieur,  3)
#    if not os.path.isfile( NomTamponInterieur):
#        traitementTampon( parcelle, NomTamponInterieur)
#    return NomTamponInterieur, NomTamponExterieur
#    
#def chercherDernierPosCentipede( baseGPKG):
#    # Choisir une trace pos et calculer HRMS
#    nomRepertoirePos = os.path.join( baseGPKG, REPERTOIRE_CENTIPEDE_BRUT)
#    nomPosRecherches = os.path.join( nomRepertoirePos, '*' + EXT_pos)
#    listePosTriee = sorted(glob.glob( nomPosRecherches))
#            #monPrint( "Liste des traces disponible {0}".format(listePosTriee))
#            # TODO: permettre le choix d'une trace .pos (la derniere pour le moment)
#    if len(listePosTriee) < 1:
#        monPrint("Pas de solution.pos à traiter : l'extension MonParcellaire pointe vers {} et {}. \
#            Avez-vous les données Centipède dans ce répertoire ?\n \
#            Avez-vous bien défini le chemin vers le référentiel Mon Parcellaire".format( baseGPKG, REPERTOIRE_CENTIPEDE_BRUT ))
#        # TODO Exception ?
#        return None, None
#    return nomRepertoirePos, listePosTriee[-1]
#    
#def chercherCasTrackingHauteur( settings=None):
#    # TODO: Recuperer casTrackingIndex dans settings
#    casTrackingIndex=1
#    LISTE_CAS_TRACKING=["INTERANG", "INTERANG_AR","SUR_RANG" ]
#    HAUTEUR_CAPTEUR_TRACKING=[2.25, 2.25, 2.50 ]
#    return LISTE_CAS_TRACKING[casTrackingIndex], HAUTEUR_CAPTEUR_TRACKING[casTrackingIndex]
#
#def filtreQualitesCentipede( nomPosChoisi, NomRepertoireCentipede):
#    """ Lire dans pandas, renommer colonnes & calcul HRMS 
#        Filtrer Q1 & Q2 et écriture gesjson
#    """
#    # TODO: Comparer dates : modification pos et date creation des geojson
#    NOM_POINT_CENTIPEDE_Q1       = PREFIXE_NOM_POINT_CENTIPEDE + SUFFIXE_Q1 + EXT_geojson
#    nomQ1_GeoJSON = os.path.join( NomRepertoireCentipede, NOM_POINT_CENTIPEDE_Q1)
#    NOM_POINT_CENTIPEDE_Q2_PLUS  = PREFIXE_NOM_POINT_CENTIPEDE + SUFFIXE_Q2_PLUS + EXT_geojson
#    nomQ2_GeoJSON = os.path.join( NomRepertoireCentipede, NOM_POINT_CENTIPEDE_Q2_PLUS)
#    if os.path.isfile( nomQ2_GeoJSON) and os.path.isfile( nomQ2_GeoJSON):
#        monPrint( "Pas de relecture du POS", T_WAR)
#        return nomQ1_GeoJSON, nomQ2_GeoJSON
#        
#    df = pd.read_csv (nomPosChoisi, skiprows=1, skipinitialspace=True, engine='python', sep=r'\s{1,}')   #  BAD :   sep="\s*[,]\s*"
#    #monPrint( "{} mesures dans brutes".format ( len(df)), T_INF)
#
#    lesDates=df['%'].unique()
#    monPrint( "Dates concernés {}".format( lesDates), T_INF)
#    # On traite df pour les format de dates vers datetime
#    df['jourHeure']=df['%']+ " " + df['UTC']
#    df['datetime'] = df['jourHeure'].apply(lambda x: datetime.strptime(x[0:19],'%Y/%m/%d %H:%M:%S'))   # %-S Second as a decimal number.    %f microseconde attend 000800
#    #  Renomme & copie du strict nécessaire
#    dfRen=df.rename( columns={ 'longitude(deg)':"longitude",  'latitude(deg)':"latitude", 'height(m)':"hauteur", \
#                'sde(m)':"déviation Est", 'sdn(m)':"déviation Nord",  'sdu(m)':"déviation Z",\
#                'Q':"précision"})
#    dfMini=dfRen[[ 'jourHeure','datetime', 'longitude', 'latitude', 'hauteur', 'précision',  'ns',  'déviation Est',  'déviation Nord', 'déviation Z']] # 'nom', 'nom_2', 'geometry']]
#    #TODO horizontal VRMS
#    dfMini[ 'drms']=sqrt( 0.5 * ( dfMini[ 'déviation Est'] ** 2 + dfMini[ 'déviation Nord'] ** 2))
#    dfMini[ 'hrms']=2*dfMini[ 'drms']
#
#    df_Q1=dfMini[(dfMini["précision"] == 1)]
#    df_Q2=dfMini[(dfMini["précision"] <= 2) & (dfMini["hrms"] < 0.3)]
#    monPrint( "{} dans Q1 & {} dans Q2_Plus pour {} brutes".format ( len(df_Q1), len(df_Q2),  len(df) ), T_INF)
#    
#    # Ecrire dans un geojson pour faire les jointures spatiales
#    NOM_POINT_CENTIPEDE_Q1       = PREFIXE_NOM_POINT_CENTIPEDE + SUFFIXE_Q1 + EXT_geojson
#    nomQ1_GeoJSON = os.path.join( NomRepertoireCentipede, NOM_POINT_CENTIPEDE_Q1)
#    if not os.path.isfile( nomQ1_GeoJSON):
#        dfPos2GeoJSON( df_Q1, nomQ1_GeoJSON)
#    if not os.path.isfile( nomQ2_GeoJSON):
#        dfPos2GeoJSON( df_Q2, nomQ2_GeoJSON)
#    return nomQ1_GeoJSON, nomQ2_GeoJSON
#
#def projectionPourJointureSpatiale(nomQ1_GeoJSON, nomQ2_GeoJSON):
#    # Transformer en L93 les points bruts pour faire jointure spatiale des parcelles
#    #TODO: src du projet ou du GPKG ?
#    # Assert tampon intérieur et extérieur existent
#    NomRepertoireCentipede= os.path.dirname(nomQ1_GeoJSON)
#    NOM_POINT_CENTIPEDE_Q1_L93      = PREFIXE_NOM_POINT_CENTIPEDE + SUFFIXE_Q1 + SUFFIXE_L93 + EXT_geojson
#    nomPointsCentipedeQ1L93 = os.path.join( NomRepertoireCentipede, NOM_POINT_CENTIPEDE_Q1_L93)
#    if not os.path.isfile( nomPointsCentipedeQ1L93):
#        try:
#            traitementReprojection( nomQ1_GeoJSON, nomPointsCentipedeQ1L93)
#        except:
#            monPrint( "Vecteur {0} ne convient pas pour changer de projection".format( nomQ1_GeoJSON), T_ERR)
#            erreur_traitement("Reprojection Q1")
#                                   
#    NOM_POINT_CENTIPEDE_Q2_PLUS_L93 = PREFIXE_NOM_POINT_CENTIPEDE + SUFFIXE_Q2_PLUS + SUFFIXE_L93 + EXT_geojson
#    nomPointsCentipedeQ2L93 = os.path.join( NomRepertoireCentipede, NOM_POINT_CENTIPEDE_Q2_PLUS_L93)
#    if not os.path.isfile( nomPointsCentipedeQ2L93):
#        try:
#            traitementReprojection( nomQ2_GeoJSON, nomPointsCentipedeQ2L93)
#        except:
#            monPrint( "Vecteur {0} ne convient pas pour changer de projection".format( nomQ2_GeoJSON), T_ERR)
#            erreur_traitement("Reprojection Q2")
#    # Jointure des exterieurs avec les deux qualités
#    NOM_POINT_CENTIPEDE_Q2_EXT = "POINTS" + SUFFIXE_EXT + SUFFIXE_Q2_PLUS + SUFFIXE_L93 + EXT_geojson
#    nomPointsCentipedeQ2EXT = os.path.join( NomRepertoireCentipede, NOM_POINT_CENTIPEDE_Q2_EXT)
#    if not os.path.isfile( nomPointsCentipedeQ2EXT):
#        try:
#            traitementJointureLocalisation( nomPointsCentipedeQ2L93, NomTamponExterieur, nomPointsCentipedeQ2EXT)
#        except:
#            monPrint( "Vecteur {0} ou parcelle extérieure {1} ne permettent pas la jointure".format( nomPointsCentipedeQ2L93, NomTamponExterieur), T_ERR)
#            erreur_traitement("Jointure par localisation Q2 extérieure")
#            
#    NOM_POINT_CENTIPEDE_Q1_EXT = "POINTS" + SUFFIXE_EXT + SUFFIXE_Q1 + SUFFIXE_L93 + EXT_geojson
#    nomPointsCentipedeQ1EXT = os.path.join( NomRepertoireCentipede, NOM_POINT_CENTIPEDE_Q1_EXT)
#    if not os.path.isfile( nomPointsCentipedeQ1EXT):
#        try:
#            traitementJointureLocalisation( nomPointsCentipedeQ1L93, NomTamponExterieur, nomPointsCentipedeQ1EXT)
#        except:
#            monPrint( "Vecteur {0} ou parcelle extérieure {1} ne permettent pas la jointure".format( nomPointsCentipedeQ2L93, NomTamponExterieur), T_ERR)
#            erreur_traitement("Jointure par localisation Q1 extérieure")
#
#    # Jointure des intérieurs avec la qualité 1 uniquement
#    NOM_POINT_CENTIPEDE_Q1_INT = "POINTS" + SUFFIXE_INT + SUFFIXE_Q1 + SUFFIXE_L93 + EXT_geojson
#    nomPointsCentipedeQ1INT = os.path.join( NomRepertoireCentipede, NOM_POINT_CENTIPEDE_Q1_INT)
#    if not os.path.isfile( nomPointsCentipedeQ1INT):
#        try:
#            traitementJointureLocalisation( nomPointsCentipedeQ1L93, NomTamponInterieur, nomPointsCentipedeQ1INT)
#        except:
#            monPrint( "Vecteur {0} ou parcelle exterieure {1} ne permettent pas la jointure".format( nomPointsCentipedeQ1L93, NomTamponInterieur), T_ERR)
#            erreur_traitement("Jointure par localisation intérieure")
#    return nomPointsCentipedeQ1INT, nomPointsCentipedeQ1EXT,  nomPointsCentipedeQ2EXT
#
#def choisirGeoJSONsInterieurExterieur(nomPointsCentipedeQ1INT, nomPointsCentipedeQ1EXT,  nomPointsCentipedeQ2EXT):
#    # Ouvrir 3 geoJSON pour attributs seulement
#    dfQ1Int = geoJSON2pd( nomPointsCentipedeQ1INT)
#    dfQ1Ext = geoJSON2pd( nomPointsCentipedeQ1EXT)
#    dfQ2Ext = geoJSON2pd( nomPointsCentipedeQ2EXT)
#    if dfQ1Ext.empty:
#        monPrint( "Pas de points centimétriques dans vos parcelles. Les traces concernent-elles votre vignoble? Avez-vous créer vos parcelles dans le GPKG MonParcellaire en précisant la couche parcelles", T_ERR)
#        erreur_traitement("Pas de points centimétriques dans vos parcelles")
#    # Stat sur qualité du POS
#    lesParcelles=dfQ1Ext['nom'].unique()
#    monPrint( "Parcelles concernées {} par cette capture & jointure".format( lesParcelles))
#    
#    totalPoints = len(dfQ2Ext) + len(dfQ1Ext)
#    monPrint( "{} Répartition des précision de captures concernant de vos parcelles : {} % décimétrique et {} % centimétrique".\
#        format ( E_CLAP, round( len(dfQ2Ext)/totalPoints*100, 1),  round( len(dfQ1Ext)/totalPoints*100, 1)), T_INF)
#
#    # Lequel je rend pour le traitement
#    # Filtre parcelle pour test
#    dfRendu=dfQ1Int[ dfQ1Int['Nom'=="F0001CO22"]]
#    monPrint("TRAITEMENT Qualité 1, points intérieurs (la geométrie en L93 et lat/long/h restent en WGS84)",  T_INF)
#    #print( dfRendu.columns)
#    return dfRendu, "Q1 Intérieur"
##    dfRendu=dfQ2Ext
##    monPrint("TRAITEMENT Qualité 2, points Extérieur (la geométrie en L93 et lat/long/h restent en WGS84)",  T_INF)
##    #print( dfRendu.columns)
##    return dfRendu, "Q2 Extérieur"
#    
#def incrementerLigneEtFichier( IDligne, repertoireParcelle, casTracking):
#    """
#        Incremente le compteur de ligne et point brisé
#        Détruit le fichier si il existe déjà
#    """
#    IDligne=IDligne+1
#    nomPointBriseeInterieur = os.path.join( repertoireParcelle, NOM_POINT_BRISE_INT + str(IDligne) + EXT_geojson)
#    if os.path.isfile( nomPointBriseeInterieur):
#        os.remove( nomPointBriseeInterieur)
#    nomligneBriseeInterieure = os.path.join( repertoireParcelle, NOM_LIGNE_BRISE_INT + str(IDligne) + EXT_geojson)
#    if os.path.isfile( nomligneBriseeInterieure):
#        os.remove( nomligneBriseeInterieure)
#    nomLigneBriseeMetrique = os.path.join( repertoireParcelle, NOM_LIGNE_BRISE_INT + str(IDligne) + EXT_csv)
#    if os.path.isfile( nomLigneBriseeMetrique):
#        os.remove( nomLigneBriseeMetrique)
#    nomLigneBriseeStat = os.path.join( repertoireParcelle, NOM_LIGNE_BRISE_INT + str(IDligne) + "_STAT"+ EXT_csv)
#    if os.path.isfile( nomLigneBriseeStat):
#        os.remove( nomLigneBriseeStat)
#    nomLigneCompleteInterieure = os.path.join( repertoireParcelle, casTracking + str(IDligne) + EXT_geojson)
#    if os.path.isfile( nomLigneCompleteInterieure):
#        os.remove( nomLigneCompleteInterieure)
#    return IDligne, nomPointBriseeInterieur, nomligneBriseeInterieure,  nomLigneBriseeMetrique,  nomLigneBriseeStat, nomLigneCompleteInterieure
#    
#def incrementerPointsBrises( IDPointsBrises, parcellesBrises, pointsBrises, distancesBrises, azimuthsBrises, IDPointsBruts, parcelleCourante, pointCourant, laDistance, lAzimuth):
#    """Stocker les points brisés """
#    IDPointsBrises.append( IDPointsBruts)
#    parcellesBrises.append(parcelleCourante)
#    pointsBrises.append( pointCourant)
#    distancesBrises.append( laDistance)    
#    azimuthsBrises.append( lAzimuth)
#    # TODO et la geom ?
#    return
#    
#def df2QgsPoint( long, lat, geometrie=None, mode="LONG-LAT"):
#    """Retrouver coordonnées ou geom dns pandas
#    Transformer en QgsPoint"""
#    #print( "Dans df2QgsPoint {} {}".format( long, lat))
#    if mode == "LONG-LAT":
#        return QgsPointXY( long, lat)
#    elif mode == "GEOMETRY":
#        monPrint( geometrie)
#        return None
#    else:
#        monPrint( "Mode de récupération {} n'est pas prévu dans {}".format(mode, APPLI_NOM_VERSION), T_WAR)
#        return None
#
#
##print( "Je suis le module {}".format("mes_rangs_centipede"))
