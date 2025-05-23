# -*- coding: utf-8 -*-
#
# Propriété de jhemmi.eu : usage sous réserve d'accord avec jhemmi.eu
# Terroir Consolidateur pour Python
# 0 parametres trouve le fichier csv des morceaux de terroir par parcelles
# Consolide l'information pour chaque parcelle dans un .csv

### UTs_par_parcelles.csv en entré provient d'une séquence sous QGIS :
### - parcelles_25 provient d'un export Mes Parcelles et d'un filtre sur les "Vigne" sauvé dans Mon_Parcellaire/parcelles
### - une jointure dans Mon Parcellaire (entre ces formes et l'information coopviti [cépage, code cepage, PG, code validation (simplifié en AOP Rouge Rosé & IGP)]
### - puis jointure spatiale avec les orientations [orientatio]. 
### - sauver dans SOLS_TERROIRS/IFV_sols_terroir.gpkg ~vinovalie_25
### - enfin intersection entre UT_Terroir et ce fichier d'affectation vinovalie_25
### - le resultat est sauvé en ./UTs_par_parcelles.csv [creer les champs surface_ut_dans_parcelle et pourcent_ut_dans_parcelle]

### le CSV en sortie  
### contient les informations de Coopviti, l'orientation et de l'étude terroir
### des consolidations des différentes UTs d'une parcelle permette une synthèse et en particulier une RUM_consolidé que l'on apparente à une profondeur probable du sol
### pour retour vers Mes Parcelles le script crée 'Type de sol' & 'Précision du type de sol' (selon table de correspondance de P.Malié (IFV CA Région)
### Pour les parcelles suites A B C qui n'ont pas d'affectation dans Coopviti, on recopie l'affectation, cépage, PG et orientation de la "vigne principale"
# Ce csv peut ensuite être déposé pour jointure dans Mon Parcellaire avec les formes "Vignes" filtrés de Mes Parcelles
# il peut aussi servir à importer des informations de terroir ou coopviti dans Mes Parcelles (envoie à CA)

import os
import sys
from datetime import datetime # , date #, datetime
import csv
import pandas as pd
pd.options.mode.chained_assignment = None

# Unicode / logo / imagettes
U_TERROIR           ="τ"
E_STAT          ="📈"
E_RAISIN        ="🍇"
E_OK            ="✔️"
U_WARNING       =u"\u26A0" #.encode("UTF-8") 
E_WARNING       ="⚠️"
U_INFO          =u"\u2139" #  avec py2 .encode("UTF-8")  # bad avec le rond u"\U0001F6C8" 
U_STOP          =u"\U0001F6AB"
E_STOP          ="🔥" 
E_INTERDIT      ="🛑"
E_PANDA         ="🐼"
# Pour statistique
LE_POURCENTAGE_IGNORE=8

# SEPARATEUR
SEP_U="_"
SEP_T="-"
SEP_P="."
SEP_V=","
SEP_PIPE="|"
SEP_POURCENT="%"
SEP_VIRGULE=SEP_V
SEP_TIRET=SEP_T
SEP_DATE=SEP_T # ou "/" pour Zoho
SEP_POINT_VIRGULE=";"
# Extensions
EXT_csv=".csv"
EXT_json=".json"
EXT_txt=".txt"

# Répertoires
REP_SYN="SYNTHESE"

APPLI_NOM="Terroir-Consolidateur"
APPLI_VERSION="V3.34 Data licence As this"  
# Suivi des versions
# 3.34 Integration à l'extension de Mon Parcellaire (onglet Synchronisation)
# 0.2 Ajout de la vigueur, du drainage et des code teroirs pour "Mes Parcelles"
# 0.1 Création
# Exceptions 
class TC_exception( BaseException):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
# Exemple    
class TC_except_extraction( TC_exception):
    pass


def erreur_assert_TC( NOM_ASSERT, NOM_MODULE, a_text=""):
    aText="Assert Terroir_consolidation {0} en erreur {1}".format( NOM_ASSERT, a_text)
    aText=aText + ". Regardes dans le code {0}".format( NOM_MODULE)
    raise TC_except_extraction( aText)

def initaliser_synthese_csv(a_csv_name):
    """ Ecrit un nouvelle entete et ecrire un nouveau csv """
    SUFFIXE_CONSOLIDE=SEP_U+"CONSOLIDE"
    if os.path.isfile( a_csv_name):
        la_date = datetime.now()
        mon_suffixe = la_date.strftime("%Y_%m_%d_%H_%M_%S")
        os.rename( a_csv_name,  a_csv_name+mon_suffixe)
    mon_csv=open(a_csv_name, "w")
    writer=csv.writer(mon_csv,  delimiter=SEP_POINT_VIRGULE) 
    ENTETE=['nom', 'CODE_UT', 'N_REG_SOL',  'NOMBRE_UT', 'DRAINAGE', 'VIGUEUR',
        'CODE_UT'+ SUFFIXE_CONSOLIDE,  'N_REG_SOL'+SUFFIXE_CONSOLIDE,  
        'RUM'+SUFFIXE_CONSOLIDE, 
        'MIN_N_REG_SOL', 'MAX_N_REG_SOL',  'MIN_RUM', 'MAX_RUM',
        'Affectation_25', 'Superficie', 'Ha', 'Code cépage', 'Viti', 'Affectation_terroir', 'Cause affectation',
        'Type de sol', 'Précision du type de sol'
        ]
    writer.writerow( ENTETE)
    return mon_csv,  writer

def ajoute_un_terroir_mes_parcelles( nom_parcelle, liste_a_ecrire):
    # on ajoute à la liste_a_ecrire le type de sols et la précision du type de sol définis dans Mes Parcelles
    # La correspondance a été faite par Pierre Malié qui a réalisé par ailleurs l'étude terroir de Fronton 2023
    code_ut=liste_a_ecrire[1]
    type_de_sols="Inconnu"
    precision_du_type_de_sol="Inconnu"
    if code_ut in ["U4", "U9","U14", "U19"]:
        type_de_sols="Alluvions caillouteuses"
        precision_du_type_de_sol=type_de_sols + " non calcaires"
    elif code_ut in ["U2", "U3"]:
        type_de_sols="Alluvions sableuses"
        if code_ut == "U2":
            precision_du_type_de_sol=type_de_sols + " non calcaires"
        if code_ut == "U3":
            precision_du_type_de_sol=type_de_sols + " calcaires"
    elif code_ut in ["U6", "U11", "U16"]:
        type_de_sols="Alluvions limoneuses à limono argileuses"            
        precision_du_type_de_sol=type_de_sols + " non calcaires"
    elif code_ut in ["U8", "U13", "U18"]:
        type_de_sols="Alluvions argilo-limoneuses à argileuses"            
        precision_du_type_de_sol=type_de_sols + " non calcaires"
    elif code_ut in ["U5", "U10", "U15"]:
        type_de_sols="Boulbène"            
        precision_du_type_de_sol=type_de_sols + " caillouteuse superficielle"
    elif code_ut in ["U7", "U12", "U17"]:
        type_de_sols="Boulbène"            
        precision_du_type_de_sol=type_de_sols + " profonde"
    elif code_ut in ["U20"]:
        type_de_sols="Sols argileux"            
        precision_du_type_de_sol="Argilo-calcaire moyen"

    return [ type_de_sols, precision_du_type_de_sol]

def ajoute_une_affectation_terroir( nom_parcelle, liste_a_ecrire):
    # on ajoute à la liste_a_ecrire le cepage, affectation_terroir et la cause affectation
    LIMITE_RUM_AOP=130
    LIMITE_RUM_IGP=150
    
    LISTE_AOP_ROUGE=["NG", "SY",  "CF",  "CS", "CO"]
    LISTE_AOP_ROSE=["FE"]
    LISTE_AOP=LISTE_AOP_ROUGE+LISTE_AOP_ROSE
    AFFECTATION="IGP"
    AFFECTATION_COMMENTAIRE="Défaut en IGP"
    
    if nom_parcelle != liste_a_ecrire[0]:
        print("Exception parcelle {0} a une liste en erreur {1}".format ( nom_parcelle,  liste_a_ecrire))
        exit()
    VITI=liste_a_ecrire[0][0:5]
    N_REG_MAJORITAIRE=int( liste_a_ecrire[2])
    NOMBRE_UT=int( liste_a_ecrire[3])
    RUM_CONSOLIDE=int( liste_a_ecrire[12]) # apres orientation

    # Extraire le cepage
    cepage = nom_parcelle[5:7]
    if cepage in LISTE_AOP:     
        # Sauf Sy non attendu en rosé
        if cepage != "SY":
            if RUM_CONSOLIDE > LIMITE_RUM_IGP:
                AFFECTATION="IGP PREMIUM"
                AFFECTATION_COMMENTAIRE="Cépage AOP Rosé et la réserve utile supérieure à {} en IGP".format( LIMITE_RUM_IGP)
            else:
                AFFECTATION="AOP ROSE"
                AFFECTATION_COMMENTAIRE="Cépage AOP Rosé et la réserve utile inférieure à {} en ROSE".format( LIMITE_RUM_IGP)
        if cepage in LISTE_AOP_ROUGE:
            if NOMBRE_UT<3:
                if N_REG_MAJORITAIRE == 1 or N_REG_MAJORITAIRE == 2: 
                    AFFECTATION="AOP ROUGE"
                    AFFECTATION_COMMENTAIRE="Pour graves et caillouteux : ROUGE"
                if (N_REG_MAJORITAIRE == 3 or N_REG_MAJORITAIRE == 4 ) and RUM_CONSOLIDE < LIMITE_RUM_AOP:
                    AFFECTATION="AOP ROUGE"
                    AFFECTATION_COMMENTAIRE="Pour peu profond et réserve utile inférieure à {} : ROUGE".format( LIMITE_RUM_AOP)
            else:
                    AFFECTATION="IGP PREMIUM"
                    AFFECTATION_COMMENTAIRE="Cépages AOP avec {} différents terroirs mélangés".format( NOMBRE_UT)

        
    return [ cepage, VITI, AFFECTATION,  AFFECTATION_COMMENTAIRE]
    
def ajoute_une_consolidation( writer, nom_parcelle, info_terroir): #, la_derniere_liste_a_ecrire):
    # info terroir contient ['pourcent_ut_dans_parcelle',  'CODE_UT', 'N_REG_SOL',  'NOMENCLATU', 'RUM']
    # Numéro de champ        0                             1          2             3              4 
    # 'Drainage', 'Vigueur',   'superficie',  'Code validation', ]
    # 5            6            7              8                 
    SEP_UT_POURCENT=":"
    SEP_UT="__"
    
    drainage=str(info_terroir[0][5])
    vigueur=str(info_terroir[0][6])        
    superficie=info_terroir[0][7]
    ha=superficie/10000
    
    # Simplifier l'affectation
    affectation_complete=str(info_terroir[0][8])    
    if affectation_complete[0:3] == "IGP":
        affectation_coopviti="IGP"
    elif affectation_complete[0:3] == "NON":
        affectation_coopviti="NOP"
    elif affectation_complete[0:3] == "San":
        affectation_coopviti="SIG"
        
    elif affectation_complete[0:3] == "AOP":
        if affectation_complete == "AOP Rosé":
            affectation_coopviti="AOP Rosé"
        else:
            affectation_coopviti="AOP Rouge"
    else:
        affectation_coopviti=None
    #print("Parcelle {} affectation simplifiée {}".format( nom_parcelle, affectation_coopviti ))

    # Consolider en simplifier le nb de REG au minimum (alors que les UTs sont conservés dans la consolidation)
    les_codes_nreg=[]
    les_pourcents_nreg=[]
    if ( len(info_terroir) >1):
        debut_liste_a_ecrire = [ nom_parcelle,  info_terroir[0][1],  str(info_terroir[0][2]),  str( len( info_terroir)), \
                                drainage, vigueur]
        les_codes_nreg.append(  info_terroir[0][2])
        les_pourcents_nreg.append(  info_terroir[0][0])
        le_plus_fort_pourcent = info_terroir[0][0]
        position_plus_fort_pourcent=0
        plus_grande_ut = str(info_terroir[0][1])
        plus_grande_nreg = str(info_terroir[0][2])
        for pos, une_ligne in enumerate( info_terroir):
            if pos == 0:
                continue
            if une_ligne[2] not in les_codes_nreg:
                les_codes_nreg.append( une_ligne[2])
                les_pourcents_nreg.append( une_ligne[0])
                if int(une_ligne[0])>le_plus_fort_pourcent:
                    le_plus_fort_pourcent = int(une_ligne[0])
                    position_plus_fort_pourcent = pos
                    plus_grande_ut = str(une_ligne[1])                    
                    plus_grande_nreg = str(une_ligne[2])
            else:
                l_index=les_codes_nreg.index(  une_ligne[2])
                pourcentage_existant = les_pourcents_nreg[l_index]
                les_pourcents_nreg[l_index] = pourcentage_existant+int(une_ligne[0])
                if pourcentage_existant+int(une_ligne[0])>le_plus_fort_pourcent:
                    le_plus_fort_pourcent = pourcentage_existant+int(une_ligne[0])
                    position_plus_fort_pourcent = pos
                    plus_grande_ut = str(une_ligne[1])
                    plus_grande_nreg = str(une_ligne[2])
                #print("Les codes_NREG {} et les pourcent {}".format( les_codes_nreg, les_pourcents_nreg))
        code_n_reg_long=""
        for pos, nreg in enumerate( les_codes_nreg):
            if pos == 0:
                code_n_reg_long = str( les_codes_nreg[ pos]) + SEP_UT_POURCENT +  str( les_pourcents_nreg[pos])
            else:
                code_n_reg_long =  code_n_reg_long + SEP_UT + str( les_codes_nreg[ pos]) + SEP_UT_POURCENT +  str( les_pourcents_nreg[pos])

        debut_liste_a_ecrire = [ nom_parcelle,  plus_grande_ut,  plus_grande_nreg,  str( len( info_terroir)), drainage, vigueur]
                
        code_ut_long = info_terroir[0][1] + SEP_UT_POURCENT + str( info_terroir[0][0])
        # Ponderation de la sommé des RUM par la surface
        somme_RUM=info_terroir[0][4] *  info_terroir[0][0]
        somme_pourcent_de_surface = info_terroir[0][0]
        max_N_REG_SOL=info_terroir[0][2]
        min_N_REG_SOL=info_terroir[0][2]
        max_rum=info_terroir[0][4]
        min_rum=info_terroir[0][4]
              
        for pos,  une_ligne in enumerate( info_terroir):
            if pos == 0:
                continue
            code_ut_long = code_ut_long + SEP_UT + une_ligne[1] + SEP_UT_POURCENT +  str( une_ligne[0])
            somme_RUM = somme_RUM + une_ligne[4] * une_ligne[0]
            somme_pourcent_de_surface = somme_pourcent_de_surface + une_ligne[0]
            if une_ligne[4] > max_rum:
                max_rum= une_ligne[4] 
            if une_ligne[4] < min_rum:
                min_rum= une_ligne[4] 
            if une_ligne[2] > max_N_REG_SOL:
                max_N_REG_SOL= une_ligne[2] 
            if une_ligne[2] < min_N_REG_SOL:
                min_N_REG_SOL= une_ligne[2] 
            liste_a_ecrire = debut_liste_a_ecrire + \
            [ code_ut_long , code_n_reg_long,  str( int( somme_RUM/somme_pourcent_de_surface)),
                str( min_N_REG_SOL),  str( max_N_REG_SOL),  str( min_rum),  str( max_rum),  
                affectation_coopviti, superficie, ha ]  
    else:   
        liste_a_ecrire = [ nom_parcelle,  info_terroir[0][1],  str( info_terroir[0][2]), "1", drainage, vigueur,
            info_terroir[0][1] + SEP_UT_POURCENT + "100", 
            str(info_terroir[0][2]) + SEP_UT_POURCENT + "100",  info_terroir[0][4],  
            str( info_terroir[0][2]),  str( info_terroir[0][2]), 
            str( info_terroir[0][4]),  str( info_terroir[0][4]), 
            affectation_coopviti, superficie, ha]  

    liste_a_ecrire =  liste_a_ecrire + ajoute_une_affectation_terroir( nom_parcelle, liste_a_ecrire)
    liste_a_ecrire =  liste_a_ecrire + ajoute_un_terroir_mes_parcelles( nom_parcelle, liste_a_ecrire)
    writer.writerow(liste_a_ecrire)
#    if nom_parcelle[-1] in ["A", "B", "C", "D", "E"]:
#        derniere_liste_a_ecrire = la_derniere_liste_a_ecrire
#    else:
#        derniere_liste_a_ecrire =  liste_a_ecrire
#    return derniere_liste_a_ecrire
    return

def dump_df( df, NOM="un_df", lignes=3):
    #my_print("{2} Type de {0} {1}".format (NOM, type(df),  E_PANDA),"Info-entete")
    print("{1} Nom de {0}".format ( df.__class__.__name__,  E_PANDA),"Info-entete")
    #my_print("{0} a pour index {1}".format( NOM, df.index))
    print("{0} a pour shape {1}".format( NOM, df.shape))
    print("{0} {1} a pour colums {2}".format( E_PANDA, NOM, df.columns))
    #Tester le type
    if isinstance( df, pd.DataFrame):
        print("{0} {1} a pour {3} premieres valeurs {2}".format( E_PANDA, NOM, df.head( lignes),  lignes), "Info-pied")
    else:
        min_lignes=min( lignes,  len(df))
        print("{0} a pour {2} premieres valeurs {1}".format( NOM, df[0:min_lignes], min_lignes), "Info-pied")
    return

###my_print("Arguments : ", "Info-entete")
#for arg in sys.argv:
#    print(arg)
#my_print("Fin des {0} arguments :".format( len(sys.argv)), "Info-pied")

# Début de code 
CHEMIN_TC=os.path.dirname( sys.argv[0])
NOM_MODULE=os.path.basename( sys.argv[0])
print("== Version {} du module {}".format( APPLI_VERSION, NOM_MODULE ))

NOM_COURT_TERROIRS_PARCELLES = "UTs_par_parcelles" + EXT_csv
CSV_TERROIRS_PARCELLES = os.path.join( CHEMIN_TC, NOM_COURT_TERROIRS_PARCELLES)
if not os.path.isfile( CSV_TERROIRS_PARCELLES):
    print("KO ~~ Le CSV des Terroirs par parcelles {0} n'existe pas. Créez une jointure des terroirs par vos parcelles et la sauvez en csv dans le répertoire {1}".\
            format( CSV_TERROIRS_PARCELLES, CHEMIN_TC))
    exit()
    
CHEMIN_SYNTHESE = os.path.join( CHEMIN_TC, REP_SYN)   
if not os.path.isdir( CHEMIN_SYNTHESE):
    os.mkdir(CHEMIN_SYNTHESE)
NOM_COURT_SYNTHESE = "Parcelle Coopviti Mes Parcelles Orientation" + SEP_U  + 'SUP'+ SEP_U  + str( LE_POURCENTAGE_IGNORE) + EXT_csv
CSV_SYNTHESE = os.path.join( CHEMIN_SYNTHESE, NOM_COURT_SYNTHESE)
mon_csv_synthese,  writer=initaliser_synthese_csv( CSV_SYNTHESE)

df_T_P =  pd.read_csv( CSV_TERROIRS_PARCELLES,  sep=SEP_POINT_VIRGULE)
#df_T_P =  pd.read_csv( CSV_TERROIRS_PARCELLES,  sep=SEP_VIRGULE)
dump_df( df_T_P, NOM_COURT_TERROIRS_PARCELLES)
print("Les types des colonnes sont : {}".format( df_T_P.dtypes))
available_parcelles=df_T_P['nom'].sort_values().unique()
print("= Info = Nombre de parcelles uniques {}.".format( len( available_parcelles)))
un_seul=plusieurs=sans_terroir=0
max_sous_parcelle=0
#derniere_liste_a_ecrire=[]
for pos, une_parcelle in enumerate(available_parcelles):
    # Trappe pour debug
    #if une_parcelle != "F0001CO24":
    #    continue
    df_une_parcelle=df_T_P[ (df_T_P['nom'] == une_parcelle) & (df_T_P['pourcent_ut_dans_parcelle'] > LE_POURCENTAGE_IGNORE)]
    #df_toutes_UTs_une_parcelle=df_T_P[ df_T_P['nom'] == une_parcelle]
    #df_une_parcelle=df_toutes_UTs_une_parcelle[ df_toutes_UTs_une_parcelle['pourcent_ut_dans_parcelle'] > LE_POURCENTAGE_IGNORE]
    #df[['Column1', 'Column2']].values.tolist()
    info_terroir=df_une_parcelle[['pourcent_ut_dans_parcelle',  'CODE_UT', 'N_REG_SOL',  'NOMENCLATU', 'RUM', 'DRAINAGE', 'VIGUEUR', 'Surface Encepagée',  
                                  'Code validation', 'Cépage', 'Porte Greffe', 'orientatio']].sort_values(ascending=False, by = 'pourcent_ut_dans_parcelle').values.tolist()
    if len(df_une_parcelle) > 1:
        #available_pourcentage_parcelles=df_une_parcelle['pourcent_ut_dans_parcelle'].sort_values(ascending=False)
        plusieurs=plusieurs+1 
        if len(df_une_parcelle) > max_sous_parcelle:
            max_sous_parcelle = len(df_une_parcelle)
###        if plusieurs in [ 100, 800]:
#            print( "Parcelle {} a plusieurs cas de terroirs {} et les pourcentages sont {}".\
#                format( une_parcelle, len(df_une_parcelle),  list(available_pourcentage_parcelles)))
#            print( "Parcelle {} et info terroirs {}".\
#                format( une_parcelle, info_terroir))
    elif len(df_une_parcelle) == 1:
        un_seul=un_seul+1
    else:
        # Cas bizarre
        sans_terroir=sans_terroir+1
        print( "{} Attention TERROIR == Parcelle {} n'a aucune information terroir.".format( U_TERROIR, une_parcelle))
        continue
    # Ecrire dans synthese
#    derniere_liste_a_ecrire=ajoute_une_consolidation( writer, une_parcelle, info_terroir, derniere_liste_a_ecrire)
    ajoute_une_consolidation( writer, une_parcelle, info_terroir)

        
print("== RESUME {} parcelles avec un seul terroir, {} avec plusieurs (min vaut {}%) et {} sans information terroir.".\
    format( un_seul,  plusieurs, max_sous_parcelle, sans_terroir))
print("== Fin la nouvelle Synthèse {} est créée, tu peux faire une jointure avec Mon Parcellaire.".\
                format( CSV_SYNTHESE))
