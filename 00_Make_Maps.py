from urllib.parse import urlsplit, unquote

import datetime
import shutil
import time
import json
import os
import sys
import glob
from pathlib import Path
from typing import Union
import keyboard
import subprocess

# global json_file_name, pbf_folder, merged_folder, merged_o5m_folder

# ------------------------------------------------------------------------------------------
#  _____                         
# | ____|_ __ _ __ ___  _ __ ___ 
# |  _| | '__| '__/ _ \| '__/ __|
# | |___| |  | | | (_) | |  \__ \
# |_____|_|  |_|  \___/|_|  |___/
# ------------------------------------------------------------------------------------------
def error_message(error, msg1):
# ------------------------------------------------------------------------------------------
# Errorsections
# ------------------------------------------------------------------------------------------
    ''' Error Section. Hand over error-level. Program will be quit with Errorcode. '''

    # os.system('cls') 
    print('------------------------------------------------------------')
    if error == 0:      print("  Routine has been called without a Styles Folder!\n  Press key to exit.")
    if error == 1:      print("  Routine has been called without a valid JSON!\n  Press key to exit.")
    if error == 2:      print("  No (GPX) File provided as parameter (drag and drop).\n  Press key to exit.")
    if error == 3:      print("  Wrong Filetype provided as file to convert.\n  Must be *.GPX\n  Press key to exit.")
    if error == 4:      print("  OSMConvert is missing \n  Press key to exit.")
    if error == 5:      print("  Splitter is missing \n  Press key to exit.")
    if error == 6:      print("  MKGmap is missing \n  Press key to exit.")
    if error == 7:      print("  NSIS is missing \n  Press key to exit.")
    if error == 8:      print('  No ' + msg1 + ' found on Geofabrik Server for download.')
    if error == 9:      print('  Problems to convert '+ msg1 + ' from PBF format to O5M format.')
    if error == 10:     print('  Problems to merge the countries in scope into '+ msg1 + ' area in one O5M format file.')
    if error == 11:     print("  WGET is missing \n  Press key to exit.")
    if error == 12:     print("  Sea-latest is missing \n  Press key to exit.")
    if error == 13:     print("  Bounds-latest is missing \n  Press key to exit.")
    if error == 14:     print("  Cities.txt is missing \n  Press key to exit.")
    if error == 15:     print("  Problems splitting files from " + msg1 +" to tiles.\n  Press key to exit.")
    if error == 16:     print("  road_name_config.txt is missing \n  Press key to exit.")
    if error == 17:     print("  copyright.txt is missing \n  Press key to exit.")
    if error == 18:     print("  license_file.txt is missing \n  Press key to exit.")
    if error == 19:     print("  gmt.exe is missing \n  Press key to exit.")
    if error == 20:     print("  7z.exe is missing \n  Press key to exit.")
    if error == 21:     print("  pth to DEM data is missing \n  Press key to exit.")
    print('------------------------------------------------------------')
    keyboard.read_key()
    sys.exit(error)

# ------------------------------------------------------------------------------------------
#   ____            _____     _          _ _    
#  / ___| ___  ___ |  ___|_ _| |__  _ __(_) | __
# | |  _ / _ \/ _ \| |_ / _` | '_ \| '__| | |/ /
# | |_| |  __/ (_) |  _| (_| | |_) | |  | |   < 
#  \____|\___|\___/|_|  \__,_|_.__/|_|  |_|_|\_\
# ------------------------------------------------------------------------------------------
def download_from_geofabrik(WGET_exe, pbf_folder, o5m_path, country_name, merged_path, geo_name):
    '''
    Lade eine Karte von GeoFabrik. 
    Suche ggf. in den Subdirectories von Geofabrik.
    Input: Ländername
    Output: pbf des Landes im pbf Folder
    '''
    # ....................................................
    # Download from GeoFabrik
    # ....................................................
    GeoFabrik_filename = country_name+'.osm.pbf'
    file_path = pbf_folder+"\\"+GeoFabrik_filename
    o5m_mit_path = o5m_path + "\\" + country_name + ".o5m"
    if os.path.isfile(file_path):           # wenn die datei schon besteht, lösche sie weg denn wget numeriert die downloaded files sonst
        # Prüfe ob die Datei bereits gestern oder heute einmal heruntergeladen wurde. Wenn ja, belasse sie        
        modification_time = os.path.getmtime(file_path)             # Get the last modification time of the file
        modification_datetime = datetime.datetime.fromtimestamp(modification_time)  # Convert the modification time to a datetime object
        current_date = datetime.datetime.now().date()               # Get the current date
        yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
        yesterday_date = yesterday.date()
        if (modification_datetime.date() == current_date) | (modification_datetime.date() == yesterday_date) :            # Check if the file was last modified today
            pass
        else:
            print("country file " + file_path +" from GeoFabrik exists, is more then 2 days old and will be deleted")
            print("removing : " + pbf_folder+"\\"+GeoFabrik_filename )
            os.remove(pbf_folder+"\\"+GeoFabrik_filename)
            if os.path.exists(o5m_mit_path):                                # !!! Remove remark after Test
                print("removing : " + o5m_path + "\\" + country_name + ".o5m")
                os.remove(o5m_mit_path)                                     # !!! Remove remark after Test
            # if os.path.exists(merged_path + "\\" + geo_name + ".o5m"):                           # Sollte basierend auf fresh bereits im Main Code erledigt sein 
            #     print("removing : " + merged_path + "\\" + geo_name + ".o5m")
            #     os.remove(merged_path + "\\" + geo_name + ".o5m") 
                           

    if os.path.isfile(file_path):           # wenn die datei schon besteht, dann ist sie von heute oder gestern und ich lade nichts
        print("Skip\tDownload \t" + country_name)
    else:
        print("\tDownload \t" + country_name)
        
        if   country_name == "baden-wuerttemberg-latest":           result= subprocess.run(WGET_exe + " -q -t 8 https://download.geofabrik.de/europe/germany/"+GeoFabrik_filename+ " -P " + pbf_folder)
        elif country_name == "bayern-latest":                       result= subprocess.run(WGET_exe + " -q -t 8 https://download.geofabrik.de/europe/germany/"+GeoFabrik_filename+ " -P " + pbf_folder)
        elif country_name == "hessen-latest":                       result= subprocess.run(WGET_exe + " -q -t 8 https://download.geofabrik.de/europe/germany/"+GeoFabrik_filename+ " -P " + pbf_folder)
        elif country_name == "rheinland-pfalz-latest":              result= subprocess.run(WGET_exe + " -q -t 8 https://download.geofabrik.de/europe/germany/"+GeoFabrik_filename+ " -P " + pbf_folder)
        elif country_name == "schleswig-holstein-latest":              result= subprocess.run(WGET_exe + " -q -t 8 https://download.geofabrik.de/europe/germany/"+GeoFabrik_filename+ " -P " + pbf_folder)
        elif country_name == "mecklenburg-vorpommern-latest":                       result= subprocess.run(WGET_exe + " -q -t 8 https://download.geofabrik.de/europe/germany/"+GeoFabrik_filename+ " -P " + pbf_folder)
        elif country_name == "brandenburg-latest":                       result= subprocess.run(WGET_exe + " -q -t 8 https://download.geofabrik.de/europe/germany/"+GeoFabrik_filename+ " -P " + pbf_folder)
        elif country_name == "hamburg-latest":                       result= subprocess.run(WGET_exe + " -q -t 8 https://download.geofabrik.de/europe/germany/"+GeoFabrik_filename+ " -P " + pbf_folder)
        elif country_name == "sachsen-anhalt-latest":                       result= subprocess.run(WGET_exe + " -q -t 8 https://download.geofabrik.de/europe/germany/"+GeoFabrik_filename+ " -P " + pbf_folder)
        elif country_name == "nordrhein-westfalen-latest":                       result= subprocess.run(WGET_exe + " -q -t 8 https://download.geofabrik.de/europe/germany/"+GeoFabrik_filename+ " -P " + pbf_folder)
        elif country_name == "niedersachsen-latest":                       result= subprocess.run(WGET_exe + " -q -t 8 https://download.geofabrik.de/europe/germany/"+GeoFabrik_filename+ " -P " + pbf_folder)
        elif country_name == "saarland-latest":                       result= subprocess.run(WGET_exe + " -q -t 8 https://download.geofabrik.de/europe/germany/"+GeoFabrik_filename+ " -P " + pbf_folder)
        elif country_name == "sachsen-latest":                       result= subprocess.run(WGET_exe + " -q -t 8 https://download.geofabrik.de/europe/germany/"+GeoFabrik_filename+ " -P " + pbf_folder)
        elif country_name == "thueringen-latest":                       result= subprocess.run(WGET_exe + " -q -t 8 https://download.geofabrik.de/europe/germany/"+GeoFabrik_filename+ " -P " + pbf_folder)
        # elif country_name == "-latest":                       result= subprocess.run(WGET_exe + " -q -t 8 https://download.geofabrik.de/europe/germany/"+GeoFabrik_filename+ " -P " + pbf_folder)
        
        elif country_name == "alsace-latest":                       result= subprocess.run(WGET_exe + " -q -t 8 https://download.geofabrik.de/europe/france/"+GeoFabrik_filename+ " -P " + pbf_folder)
        elif country_name == "franche-comte-latest":                result= subprocess.run(WGET_exe + " -q -t 8 https://download.geofabrik.de/europe/france/"+GeoFabrik_filename+ " -P " + pbf_folder)
        elif country_name == "lorraine-latest":                     result= subprocess.run(WGET_exe + " -q -t 8 https://download.geofabrik.de/europe/france/"+GeoFabrik_filename+ " -P " + pbf_folder)
        elif country_name == "rhone-alpes-latest":                  result= subprocess.run(WGET_exe + " -q -t 8 https://download.geofabrik.de/europe/france/"+GeoFabrik_filename+ " -P " + pbf_folder)
        elif country_name == "provence-alpes-cote-d-azur-latest":   result= subprocess.run(WGET_exe + " -q -t 8 https://download.geofabrik.de/europe/france/"+GeoFabrik_filename+ " -P " + pbf_folder)
        
        elif country_name == "nord-ovest-latest":                   result= subprocess.run(WGET_exe + " -q -t 8 https://download.geofabrik.de/europe/italy/"+GeoFabrik_filename+ " -P " + pbf_folder)
        elif country_name == "nord-est-latest":                     result= subprocess.run(WGET_exe + " -q -t 8 https://download.geofabrik.de/europe/italy/"+GeoFabrik_filename+ " -P " + pbf_folder)
        
        elif country_name == "china-latest":                        result= subprocess.run(WGET_exe + " -q -t 8 https://download.geofabrik.de/asia/"+GeoFabrik_filename+ " -P " + pbf_folder)
        elif country_name == "armenia-latest":                      result= subprocess.run(WGET_exe + " -q -t 8 https://download.geofabrik.de/asia/"+GeoFabrik_filename+ " -P " + pbf_folder)
        elif country_name == "azerbaijan-latest":                   result= subprocess.run(WGET_exe + " -q -t 8 https://download.geofabrik.de/asia/"+GeoFabrik_filename+ " -P " + pbf_folder)
        elif country_name == "iran-latest":                         result= subprocess.run(WGET_exe + " -q -t 8 https://download.geofabrik.de/asia/"+GeoFabrik_filename+ " -P " + pbf_folder)
        elif country_name == "kazakhstan-latest":                   result= subprocess.run(WGET_exe + " -q -t 8 https://download.geofabrik.de/asia/"+GeoFabrik_filename+ " -P " + pbf_folder)
        elif country_name == "kyrgyzstan-latest":                   result= subprocess.run(WGET_exe + " -q -t 8 https://download.geofabrik.de/asia/"+GeoFabrik_filename+ " -P " + pbf_folder)
        elif country_name == "mongolia-latest":                     result= subprocess.run(WGET_exe + " -q -t 8 https://download.geofabrik.de/asia/"+GeoFabrik_filename+ " -P " + pbf_folder)
        elif country_name == "tajikistan-latest":                   result= subprocess.run(WGET_exe + " -q -t 8 https://download.geofabrik.de/asia/"+GeoFabrik_filename+ " -P " + pbf_folder)
        elif country_name == "turkmenistan-latest":                 result= subprocess.run(WGET_exe + " -q -t 8 https://download.geofabrik.de/asia/"+GeoFabrik_filename+ " -P " + pbf_folder)
        elif country_name == "uzbekistan-latest":                   result= subprocess.run(WGET_exe + " -q -t 8 https://download.geofabrik.de/asia/"+GeoFabrik_filename+ " -P " + pbf_folder)
        
        elif country_name == "algeria-latest":                      result= subprocess.run(WGET_exe + " -q -t 8 https://download.geofabrik.de/africa/"+GeoFabrik_filename+ " -P " + pbf_folder)
        elif country_name == "morocco-latest":                      result= subprocess.run(WGET_exe + " -q -t 8 https://download.geofabrik.de/africa/"+GeoFabrik_filename+ " -P " + pbf_folder)
        elif country_name == "tunisia-latest":                      result= subprocess.run(WGET_exe + " -q -t 8 https://download.geofabrik.de/africa/"+GeoFabrik_filename+ " -P " + pbf_folder)
        
        elif country_name == "costa-rica-latest":                   result= subprocess.run(WGET_exe + " -q -t 8 https://download.geofabrik.de/central-america/"+GeoFabrik_filename+ " -P " + pbf_folder)
        
        else:                                                       result= subprocess.run(WGET_exe + " -q -t 8 https://download.geofabrik.de/europe/"+GeoFabrik_filename+ " -P " + pbf_folder)
        
        if os.path.exists(o5m_mit_path):                                # !!! Remove remark after Test
            os.remove(o5m_mit_path)                                     # !!! Remove remark after Test

# ------------------------------------------------------------------------------------------
#        _      __   _               ____            
#  _ __ | |__  / _| | |_ ___     ___| ___| _ __ ___  
# | '_ \| '_ \| |_  | __/ _ \   / _ \___ \| '_ ` _ \ 
# | |_) | |_) |  _| | || (_) | | (_) |__) | | | | | |
# | .__/|_.__/|_|    \__\___/   \___/____/|_| |_| |_|
# |_|     
# ------------------------------------------------------------------------------------------
def convert_pbf_to_o5m(OSMConvert_exe, pbf_path , o5m_path, country_name):
    '''
    One must convert each PBF file into O5m file as in a later step, certain files will be merged into an Geo - O5M. 
    OSMConvert64 doesn't accept to convert more then 1 PBF file into O5M - so a merge is possible with O5M files only.

    Input: 
        pbf_path = Verzeichnis wo die downloads von Geofabrik liegen
        country_name-latest ohne extension
    Output: 
        Ländername im o5m_path: country_name-latest  >>.o5m<<
        rc = 0
    '''
    # ....................................................
    GeoFabrik_filename = country_name+'.osm.pbf'
    if os.path.exists(o5m_path + "\\" + country_name + ".o5m"):                                # !!! Remove remark after Test
        print("Skip build O5M File: \t" + country_name + ".o5m")
    else:
        print("Build O5M File: \t" + pbf_path +"\\"+ GeoFabrik_filename + "\t\t to \t\t" + o5m_path + "\\" + country_name + ".o5m")
        rc = subprocess.run(OSMConvert_exe + " --drop-version "+ pbf_path +"\\"+ GeoFabrik_filename + " -o=" + o5m_path + "\\" + country_name + ".o5m", shell=True)
        if rc.returncode != 0: error_message(9, country_name)

# ------------------------------------------------------------------------------------------
#                                                        _        _             ____                     
#  _ __ ___   ___ _ __ __ _  ___    ___ ___  _   _ _ __ | |_ _ __(_) ___  ___  |___ \    __ _  ___  ___    
# | '_ ` _ \ / _ \ '__/ _` |/ _ \  / __/ _ \| | | | '_ \| __| '__| |/ _ \/ __|   __) |  / _` |/ _ \/ _ \ 
# | | | | | |  __/ | | (_| |  __/ | (_| (_) | |_| | | | | |_| |  | |  __/\__ \  / __/  | (_| |  __/ (_) |
# |_| |_| |_|\___|_|  \__, |\___|  \___\___/ \__,_|_| |_|\__|_|  |_|\___||___/ |_____|  \__, |\___|\___/ 
#                     |___/                                                             |___/    
# ------------------------------------------------------------------------------------------
def merge_countries_2_geo(OSMConvert_exe, o5m_path, countries, merged_path, geo_name):
    '''
    One must convert each PBF file into O5m file before as in this step, certain files will be merged into one Geo - O5M. 
    OSMConvert64 doesn't accept to convert more then 1 PBF file into O5M - so a merge is possible with O5M files only.
    
    Input: 
        o5m_path    =   where the o5m files are place
        countries   =   the full list
        merged_path =   the path where the Geo O5M should be placed to
        geo_name    =   the name of the Geo
    Output: 
        Geo in merged_path in o5m format
        rc = 0
    '''
    # print("Merged Path : " + merged_path + "\\" + geo_name + ".o5m")
    
    countries_4_merge = ""
    for land in countries.split("; "):
        countries_4_merge = countries_4_merge + o5m_path +"\\"+ land + ".o5m "
        # print(OSMConvert_exe + " --drop-version "+ countries_4_merge + " -o=" + merged_path + "\\" + geo_name + ".o5m")
    print("merge all countriess into one: \t\t" + merged_path + "\\" + geo_name + ".o5m")
    rc = subprocess.run(OSMConvert_exe + " --drop-version "+ countries_4_merge + " -o=" + merged_path + "\\" + geo_name + ".o5m" , stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    if rc.returncode != 0: error_message(10, geo_name)


# ------------------------------------------------------------------------------------------
#  ____        _ _ _     _____ _ _      
# / ___| _ __ | (_) |_  |  ___(_) | ___ 
# \___ \| '_ \| | | __| | |_  | | |/ _ \
#  ___) | |_) | | | |_  |  _| | | |  __/
# |____/| .__/|_|_|\__| |_|   |_|_|\___|
#       |_|                             
# ------------------------------------------------------------------------------------------
def  split_my_files(Splitter_exe, max_nodes, SEA_file, Cities_file, merged_path, MAP_ID, splitfiles_path, geography):
    '''
    There will be a subfolder per Geo in the splitfiles_path. This ensures that the data will be kept for reuse.
    Output: Gesplittete o5m im pbf format im Verzeichnis Splitfiles
            Wichtig im Verzeichnis: template.args und areas.poly
    '''
    # ....................................................
    # Split file
    # ....................................................
    # Create subfolder
    # splitfiles_path = splitfiles_path+"\\"+geography
    if not os.path.exists(splitfiles_path):     
        print("Create new path to Splitfiles:\t" + splitfiles_path)
        os.mkdir(splitfiles_path)
    # Lösche alle alten Files raus
    files = glob.glob(splitfiles_path+"\\*.*")
    for f in files: os.remove(f)
    # split files
    print("Split merged O5M file: \t\t" + merged_path + " --into Splitfiles-- " + splitfiles_path)
    rc = subprocess.run("java -Xmx16384m -jar " + Splitter_exe + " "+ merged_path +"\\" + geography +".o5m --precomp-sea="+SEA_file+" --mapid="+MAP_ID+" --output-dir="+splitfiles_path+" --output=pbf --max-areas=4096 --max-nodes=" + max_nodes + " --wanted-admin-level=8 --description="+geography+" --geonames-file=" + Cities_file , stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    if rc.returncode != 0: error_message(15, geography)


# ------------------------------------------------------------------------------------------
#      _ ____   ___  _   _ 
#     | / ___| / _ \| \ | |
#  _  | \___ \| | | |  \| |
# | |_| |___) | |_| | |\  |
#  \___/|____/ \___/|_| \_|
# ------------------------------------------------------------------------------------------
# def load_json(json_file_name:str) -> dict | list | None:
def load_json(json_file_name:str):
# ------------------------------------------------------------------------------------------
# Load Translation Table 
# 2022 12 01
# ------------------------------------------------------------------------------------------
    ''' If exists: Load JSON file. -> JSON  '''
    try:											
        with open(json_file_name) as f:				
            return json.load(f)						
    except FileNotFoundError:
        error_message(1, "")

# ------------------------------------------------------------------------------------------
#  __  __       _       
# |  \/  | __ _(_)_ __  
# | |\/| |/ _` | | '_ \ 
# | |  | | (_| | | | | |
# |_|  |_|\__,_|_|_| |_|
# ------------------------------------------------------------------------------------------
# Ablauf: 
#       Die JSON wird eingelesen und analysiert. In der JSON sind alle notwendigen Steuerparameter verankert.
#       Basierend auf den JSON daten werden die vorhandenen Daten für die jeweilige Karte zuerst gelöscht oder beibehalten.
#       Die notwendigen  Geodaten werden von Geofabrik heruntergeladen - sofern sie nicht mehr vorhanden sind.

if __name__ == "__main__":
    global json_file_name, pbf_folder, merged_folder

    # ....................................................
    # Erhalte die Übergabeparameter. Erstelle dazu den 
    # default GPX Entry - sofern übergeben.
    # Ansonsten setze Default Pfad auf den Pfad der Exe
    # ....................................................
    os.system('cls') 
    my_name = sys.argv[0]                       # the first argument is the script itself
    my_stem = Path(my_name).stem                # Das ist der DateiName ohne Suffix
    my_path = Path(my_name).parent              # Das ist der Path ohne trailing \
    my_name = Path(my_name).name                # Der komplette Dateiname ohne Path
    json_file_name = my_stem+'.json'
    # ....................................................
    # Lese die JSON ein und hole die Arbeitspfade
    # ....................................................
    my_json = load_json(json_file_name)
    # ....................................................
    # Get all necessary programs and pathes from JSON
    # ....................................................
    WGET_exe            = my_json["WGET_exe"]                           # type: ignore
    OSMConvert_exe      = my_json["OSMConvert_exe"]                     # type: ignore
    gmt_exe             = my_json["gmt_exe"]                            # type: ignore
    z_exe               = my_json["7z_exe"]                             # type: ignore
    Splitter_exe        = my_json["Splitter_exe"]                       # type: ignore
    MkGmap_exe          = my_json["MkGmap_exe"]                         # type: ignore
    NSIS_exe            = my_json["NSIS_exe"]                           # type: ignore
    SEA_file            = my_json["SEA_file"]                           # type: ignore
    BOUNDS_file         = my_json["BOUNDS_file"]                        # type: ignore
    Cities_file         = my_json["Cities_file"]                        # type: ignore
    hgt_path            = my_json["hgt_path"]                           # type: ignore
    road_name_config    = my_json["road_name_config"]                   # type: ignore
    copyright_file      = my_json["copyright_file"]                     # type: ignore
    license_file        = my_json["license_file"]                       # type: ignore
    if not os.path.exists(WGET_exe):            error_message(11,"")
    if not os.path.exists(OSMConvert_exe):      error_message(4,"")
    if not os.path.exists(gmt_exe):             error_message(19,"")
    if not os.path.exists(z_exe):               error_message(20,"")
    if not os.path.exists(Splitter_exe):        error_message(5,"")
    if not os.path.exists(MkGmap_exe):          error_message(6,"")
    if not os.path.exists(NSIS_exe):            error_message(7,"")
    if not os.path.exists(SEA_file):            error_message(12,"")
    if not os.path.exists(BOUNDS_file):         error_message(13,"")
    if not os.path.exists(Cities_file):         error_message(14,"")
    if not os.path.exists(hgt_path):            error_message(21,"")
    if not os.path.exists(road_name_config):    error_message(16,"")
    if not os.path.exists(copyright_file):      error_message(17,"")
    if not os.path.exists(license_file):        error_message(18,"")

    o5m_path = ""
    styles_path         = my_json["styles_path"]                        # type: ignore           
    pbf_path            = my_json["pbf_path"]                           # type: ignore
    o5m_path            = my_json["o5m_path"]                           # type: ignore
    merged_path         = my_json["merged_path"]                        # type: ignore
    splitfiles_path     = my_json["splitfiles_path"]                    # type: ignore
    offroadkarten_path  = my_json["offroadkarten_path"]                 # type: ignore
    strassenkarten_path = my_json["strassenkarten_path"]                # type: ignore
    oruxkarten_path     = my_json["oruxkarten_path"]                    # type: ignore
    # ....................................................
    # Prepare basic folder structure
    # ....................................................
    if not os.path.exists(styles_path):         error_message(0,"")
    if not os.path.exists(pbf_path):            os.mkdir(pbf_path)
    if not os.path.exists(o5m_path):            os.mkdir(o5m_path)
    if not os.path.exists(merged_path):         os.mkdir(merged_path)
    if not os.path.exists(splitfiles_path):     os.mkdir(splitfiles_path)
    if not os.path.exists(strassenkarten_path): os.mkdir(strassenkarten_path)
    if not os.path.exists(offroadkarten_path):  os.mkdir(offroadkarten_path)
    if not os.path.exists(oruxkarten_path):     os.mkdir(oruxkarten_path)

    # ....................................................
    # Arbeite GEO für GEO ab
    # Beispiel: Zuerst Asia-West, dann Asia-Central usw.
    # ....................................................
    for geography in my_json["geo"]:                                    # type: ignore
        fresh = False
        fresh       = my_json["geo"][geography]["fresh"]                # type: ignore
        countries   = my_json["geo"][geography]["countries"]            # type: ignore
        max_nodes   = my_json["geo"][geography]["max_nodes"]            # type: ignore
        
        print('------------------------------------------------------------')
        print("\t Build Maps of "+ geography )
        print('------------------------------------------------------------')
        merged_file_with_path = merged_path + "\\" + geography + ".o5m"
        if fresh:
            # remove the merged files per geography
            if os.path.exists(merged_file_with_path):  
                rc = os.remove(merged_file_with_path)                           # !!! Remove remark after Test
            # ....................................................
            # Arbeite Land für Land in der jeweiligen GEO ab. 
            # Beispiel: Innerhalb der GEO loop nun durch die Länder 
            #           germany-latest, alsace-latest, franche-comte-latest usw.
            # ....................................................
            for land in countries.split("; "):
                all_o5m_files = ""
                # ....................................................
                # Remove existing PBF, O5M Files
                # ....................................................
                land_mit_path = pbf_path + "\\" + land + ".osm.pbf"
                # if os.path.exists(land_mit_path):                               # Wird ebenfalls in der Downloadsektion gemacht!
                    # os.remove(land_mit_path)                                    

                o5m_mit_path = o5m_path + "\\" + land + ".o5m"
                # if os.path.exists(o5m_mit_path):                                # Wird in der Geofabrik gelöscht sofern ein download statt fand
                    # os.remove(o5m_mit_path)                                     # 
                # ....................................................
                # get files from geoFabrik
                # ....................................................
                download_from_geofabrik(WGET_exe, pbf_path, o5m_path, land, merged_path, geography)
                # ....................................................
                #  convert the PBF Files into O5M files to merge them in a next step
                #  Du musst die PBF Files in O5M Files wandeln, da zum Merge der einzelnen 
                # Länder in eine Geo nur O5M Files gehen. OSMconvert kann nur eine PBF aber 
                # viele O5M verarbeiten.
                # ....................................................
                # if not os.path.exists(o5m_mit_path):  
                    # print("Erstelle die \t\t" + o5m_mit_path )                                # !!! Delete after Test 
                convert_pbf_to_o5m(OSMConvert_exe, pbf_path , o5m_path, land)
                # else:
                    # print("Skip die \t" + o5m_mit_path )                                      # !!! Delete after Test 
            
            # ....................................................
            # Merge the O5M files into one Geo O5M file
            # Da das nur einmal gemacht werden muss, geschieht das am Ende 
            # des ersten Durchgangs durch die Länder
            # ....................................................
            print("Merge single Country O5M Files into merged O5M file: \t" + merged_file_with_path)      # !!! Remark after Test 
            if not os.path.exists(merged_file_with_path): merge_countries_2_geo(OSMConvert_exe, o5m_path, countries, merged_path, geography)
            

        for maps in my_json["geo"][geography]["maps"]:                                          
            dem_dists = "standard"                                                               
            make_map    = my_json["geo"][geography]["maps"][maps]["make_map"]                   
            tdbfile     = my_json["geo"][geography]["maps"][maps]["tdbfile"]                    
            gmapsupp    = my_json["geo"][geography]["maps"][maps]["gmapsupp"]                   
            gmapi       = my_json["geo"][geography]["maps"][maps]["gmapi"]                      
            nsis        = my_json["geo"][geography]["maps"][maps]["nsis"]                       
            language    = my_json["geo"][geography]["maps"][maps]["language"]                   
            FAM_ID      = my_json["geo"][geography]["maps"][maps]["FAM_ID"]                     
            MAP_ID      = my_json["geo"][geography]["maps"][maps]["MAP_ID"]                     
            style       = my_json["geo"][geography]["maps"][maps]["style"]                      
            typ_file    = my_json["geo"][geography]["maps"][maps]["typ_file"]                   
            region_name = my_json["geo"][geography]["maps"][maps]["region_name"]                
            areaname    = my_json["geo"][geography]["maps"][maps]["areaname"]                   
            map_name    = my_json["geo"][geography]["maps"][maps]["map_name"]                   
            # housenumbers = my_json["geo"][geography]["maps"][maps]["housenumbers"]            # housenumbers. Enables house number search for OSM input files. If or not compile of housenumbers itself is done by style file.
            dem_dists = my_json["geo"][geography]["maps"][maps]["dem_dists"]                    # 

            output_dir = offroadkarten_path
            if maps == "offroad"        : output_dir = offroadkarten_path
            if maps == "offroad-flat"   : output_dir = offroadkarten_path
            if maps == "street"         : output_dir = strassenkarten_path
            if maps == "orux"           : output_dir = oruxkarten_path
            if maps == "orux-full"      : output_dir = oruxkarten_path
            if maps == "orux-full-flat" : output_dir = oruxkarten_path
            if maps == "orux_street"    : output_dir = oruxkarten_path
            if maps == "rad"            : output_dir = oruxkarten_path
            
            name_tag = "name-tag-list: name:int,int_name,name:en,name,name:de \n"
            if language == "INT": name_tag = "name-tag-list: name:int,int_name,name:en,name,name:de \n"
            if language == "ARA": name_tag = "name-tag-list: name:int,int_name,name:fr,name:en,name \n"
            if language == "FRA": name_tag = "name-tag-list: name,name:fr,name:de,name:it,name:es,name:en \n"
            if language == "GRC": name_tag = "name-tag-list: name:de,name:int,int_name,name:en,name \n"
            if language == "DEU": name_tag = "name-tag-list: name:de,name:int,int_name,name \n"

            if make_map:
                # ....................................................
                # Splitte die o5m Files
                # ....................................................
                # remove the Splitfiles per Geography
                splitfiles_with_path = splitfiles_path + "\\" + geography + "-" + maps
                if os.path.exists(splitfiles_with_path):  
                    if fresh:
                        print("Delete Splitfiles Folder \t" + splitfiles_with_path + "\t from the disk")
                        rc = shutil.rmtree(splitfiles_with_path)                            
                # make Splitfiles
                if os.path.exists(splitfiles_with_path):  
                    pass
                else:                                                                       
                    split_my_files(Splitter_exe, max_nodes, SEA_file, Cities_file, merged_path, MAP_ID, splitfiles_with_path, geography)

                print('............................................................')
                print('Build Map :\t\t\t' + geography + "-" + maps)
                print('............................................................')
                # ....................................................
                # Erstelle die Options
                # ....................................................
                with open('options.txt', 'w', encoding='utf-8') as file:
                    print("Schreibe die Options File")
                    file.write('# ----------------------------------------------------------------------\n')
                    file.write('# Hans Strassguetl & Gravelmaps.de     \n')
                    file.write('# options.txt building map: \t'+geography+"\t"+maps+'  \n')
                    file.write('# ----------------------------------------------------------------------\n')
                    # Schreibe die erste Zeile
                    if gmapi:  file.write("gmapi \n")
                    file.write("output-dir: " + output_dir +" \n")
                    file.write("mapname: " + MAP_ID +" \n")
                    file.write("overview-mapname: " + map_name +" \n")
                    file.write("description: " + map_name +" \n")
                    file.write("country-name: " + map_name +" \n")
                    file.write("region-name: " + region_name +" \n")
                    file.write("style-file: " + styles_path +"\\ \n")
                    file.write("style: " + style +" \n")
                    file.write("family-id: " + FAM_ID +" \n")
                    file.write("family-name: "+ map_name +" \n")
                    file.write("product-id: 1\n")
                    file.write("product-version: 200\n")
                    file.write("series-name:" + map_name +" \n")
                    file.write("area-name: " + areaname +" \n")
                    file.write(name_tag)                                # benötigt kein \n !
                    if gmapsupp: file.write("gmapsupp \n")
                    if nsis: file.write("nsis \n")
                    if tdbfile: file.write("tdbfile \n")
                    file.write("latin1 \n")
                    file.write("index \n")
                    file.write("split-name-index \n")
                    file.write("road-name-config: " + road_name_config +" \n")
                    file.write("bounds: " + BOUNDS_file +" \n")
                    file.write("location-autofill:is_in,nearest \n")
                    # if housenumbers: file.write("housenumbers \n")
                    # housenumbers. Enables house number search for OSM input files. If or not compile of housenumbers itself is done by style file.
                    file.write("housenumbers \n")
                    file.write("remove-ovm-work-files \n")
                    file.write("check-styles \n")
                    file.write("copyright-file: " + copyright_file +" \n")
                    file.write("license-file: " + license_file +" \n")
                    file.write("merge-lines \n")
                    file.write("allow-reverse-merge \n")
                    file.write("improve-overview \n")
                    file.write("# ------- DEM Distancing \t\t\t------- \n")
                    if dem_dists != "none": 
                        file.write("# ------- DEM Distancing for "+ dem_dists + "\t-------\n")
                        file.write("dem: " + hgt_path + "\n")
                    if dem_dists == "standard": 
                        file.write("dem-dists=3312,6624,13248,26496,52992,105984,211968,423936 \n")
                        file.write("overview-dem-dist=88368 \n")
                    if dem_dists == "rad":     
                        file.write("dem-dists:3312,6624,13248,26496,52992,105984,211968 \n")
                        file.write("overview-dem-dist=88368 \n")
                    if dem_dists == "asia":     
                        file.write("dem-dists:13248,26496,52992,105984,211968,423936,650000,900000 \n")
                        file.write("overview-dem-dist=105984 \n")
                    if dem_dists == "africa":     
                        file.write("dem-dists:13248,26496,52992,105984,211968,423936,650000,900000 \n")
                        file.write("overview-dem-dist=105984 \n")
                    file.write("# ------- DEM Distancing ends \t\t-------\n")
                    file.write("max-jobs: 4 \n")
                    file.write("keep-going \n")
                    file.write("route \n")
                    file.write("order-by-decreasing-area \n")
                    file.write("link-pois-to-ways \n")
                    file.write("make-opposite-cycleways \n")
                    file.write("drive-on:detect,right \n")
                    file.write("ignore-turn-restrictions \n")
                    file.write("preserve-element-order: relations, nodes, ways \n")
                    file.write("add-pois-to-areas \n")
                    file.write("add-pois-to-lines \n")
                    file.write("reduce-point-density \n")
                    file.write("reduce-point-density-polygon \n")
                    file.write("min-size-polygon \n")
                    file.write("pois-to-areas-placement: entrance=main, entrance=yes, building=entrance \n")
                    file.write("precomp-sea: " + SEA_file +" \n")
                    file.write("generate-sea:land-tag=natural=background \n")
                    file.write("process-destination \n")
                    file.write("process-exits \n")
                    file.write("draw-priority: 10 \n")
                    file.write("hide-gmapsupp-on-pc \n")
                    file.write("poi-address \n")
                    file.write("show-profiles: 1 \n")
                    if dem_dists != "none": file.write("dem-poly: " + splitfiles_with_path+"\\areas.poly \n")
                    file.write("read-config: "+ splitfiles_with_path +"\\template.args \n")

                    # file.write('# ----------------------------------------------------------------------\n')
                    # file.write("# Following Options are set via JSON:  \n")
                    # file.write('# ----------------------------------------------------------------------\n')

                    # for single_option in options.split("; "):
                    #     if "dem-dists:" in single_option:
                    #         if include_dem: 
                    #             file.write(single_option + "\n")
                    #     else: 
                    #         file.write(single_option + "\n")
                # ....................................................
                #  Die Options ist jetzt geschrieben
                #  Nun starte den Compile
                #  java -Xmx16384m -ea -jar g:\programme\mkgmap\mkgmap.jar  --read-config=options.txt g:\01_Styles\orux.txt
                # ....................................................
                if os.path.isfile(output_dir+"\\"+map_name+".img"): os.remove(output_dir+"\\"+map_name+".img")
                rc = subprocess.run("java -Xmx16384m -ea -jar "+ MkGmap_exe +" --read-config=options.txt "+ styles_path+"\\"+typ_file+".txt")

                # ....................................................
                # rework all typ files 
                # ....................................................
                shutil.copy2(styles_path+"\\grvl_p.typ", output_dir+"\\")
                shutil.copy2(styles_path+"\\grvl_pn.typ", output_dir+"\\")
                shutil.copy2(styles_path+"\\grvl_pB.typ", output_dir+"\\")
                shutil.copy2(styles_path+"\\grvl_pnB.typ", output_dir+"\\")
                shutil.copy2(styles_path+"\\orux.typ", output_dir+"\\")
                rc = subprocess.run(gmt_exe + " -w -y " + FAM_ID + " " + output_dir+"\\grvl_p.typ")
                rc = subprocess.run(gmt_exe + " -w -y " + FAM_ID + " " + output_dir+"\\grvl_pn.typ")
                rc = subprocess.run(gmt_exe + " -w -y " + FAM_ID + " " + output_dir+"\\grvl_pB.typ")
                rc = subprocess.run(gmt_exe + " -w -y " + FAM_ID + " " + output_dir+"\\grvl_pnB.typ")
                rc = subprocess.run(gmt_exe + " -w -y " + FAM_ID + " " + output_dir+"\\orux.typ")

                # ....................................................
                # copy GMAPI to its Garmin folder & pack it
                # 'G:\programme\7z\7z.exe   a -mx7 -spe -sdel G:\10_Offroad_Karte\Asia-Central.gmap.zip G:\10_Offroad_Karte\Asia-Central.gmap'
                # ....................................................
                if os.path.exists(output_dir+"\\"+map_name+".gmap"):
                    result = subprocess.run("xcopy /Q /E /C /I /Y  "+ output_dir+"\\"+map_name+".gmap C:\\ProgramData\\Garmin\\Maps\\"+map_name+".gmap ", shell=True, check=False,  stderr=subprocess.PIPE, text=True)
                    # Pack GMAPI. Delete existing file upfront
                    if os.path.isfile(output_dir+"\\"+map_name+".gmap.zip"):  os.remove(output_dir+"\\"+map_name+".gmap.zip")
                    rc = subprocess.run(z_exe + "  a -mx7 -spe -sdel " + output_dir+"\\"+map_name + ".gmap.zip " + output_dir+"\\"+map_name+".gmap", shell=True, check=False)
                # ....................................................
                # make installer
                # \Programme\nsisbi\makensis.exe G:\10_Offroad_Karte\Central.nsi
                # ....................................................
                if os.path.exists(output_dir+"\\"+map_name + ".nsi"):  
                    print("make installer")
                    rc = subprocess.run(NSIS_exe + " "+ output_dir+"\\"+map_name + ".nsi", shell=True, check=False)
                
                # ....................................................
                # rework gmapsupp
                # ....................................................
                # First delete some files no longer needed
                if os.path.exists(output_dir+"\\"+map_name+".img"):  os.remove(output_dir+"\\"+map_name+".img")
                if os.path.exists(output_dir+"\\"+map_name+".tdb"):  os.remove(output_dir+"\\"+map_name+".tdb")
                if os.path.exists(output_dir+"\\"+map_name+".mdx"):  os.remove(output_dir+"\\"+map_name+".mdx")
                # if os.path.exists(output_dir+"\\"+map_name+".nsi"):  os.remove(output_dir+"\\"+map_name+".nsi")
                if os.path.exists(output_dir+"\\"+map_name+"_license.txt"):  os.remove(output_dir+"\\"+map_name+"_license.txt")
                if os.path.exists(output_dir+"\\"+map_name+"_mdr.img"):  os.remove(output_dir+"\\"+map_name+"_mdr.img")
                if os.path.exists(output_dir+"\\gmapsupp.img"):  
                    result = subprocess.run("xcopy /Q /E /C /I /Y  "+ output_dir+ "\\gmapsupp.img "+output_dir+"\\gmapsupp_backup.img", shell=True, check=False,  stderr=subprocess.PIPE, text=True)                    
                    if maps[:4].lower() != "orux":
                        # G:\Programme\GMAPTool\gmt.exe -w -x G:\10_Offroad_Karte\grvl_p.typ G:\10_Offroad_Karte\gmapsupp.img   
                        rc = subprocess.run(gmt_exe + " -w -x " + output_dir +"\\grvl_p.typ " + output_dir+"\\gmapsupp.img" ,shell=True, check=False )
                        print("gmapsupp.img wurde mit grvl_p.typ Darstellung versehen ")
                    else:
                        # rc = subprocess.run(gmt_exe + " -w -x " + output_dir +"\\orux.typ " + output_dir+"\\gmapsupp.img" ,shell=True, check=False )
                        print("gmapsupp.img nicht mit gmt verändert da eine Orux Karte")

                    if os.path.isfile(output_dir+"\\"+map_name+".img"): os.remove(output_dir+"\\"+map_name+".img")
                    print("Erstelle : " + output_dir+"\\"+map_name+".img")
                    os.rename(output_dir+"\\gmapsupp.img" , output_dir+"\\"+map_name+".img")
                else:
                    print(" gmapsupp.img ist nicht compiled. ")

                # ....................................................
                # Cleanup
                # ....................................................
                # remove the Splitfiles
                # if os.path.exists(splitfiles_with_path): rc = shutil.rmtree(splitfiles_with_path)         #  !!! remove remark for production

                # remove unneccesary files
                files = os.listdir(output_dir)
                for file in files:
                     if file.startswith(FAM_ID) and file.endswith('.img'):
                        file_path = os.path.join(output_dir, file)
                        os.remove(file_path)
                     if file.endswith('.typ'):
                        file_path = os.path.join(output_dir, file)
                        os.remove(file_path)

                if os.path.isfile(output_dir+"\\gmapsupp_backup.img"): rc = os.remove(output_dir+"\\gmapsupp_backup.img")

                # O5M Files
                # Überlege ob du alle o5m Files löschen magst. Brauchen solltest du sie nicht mehr, hauptsache die Merged Files sind noch da. Sie stören aber auch nicht wirklich
                # shutil.rmtree(o5m_path)
                # os.mkdir(o5m_path)
                

    
    print('\n  Fertig!\n  Program closes.\n\n')
    time.sleep(2) # Seconds
exit()   
