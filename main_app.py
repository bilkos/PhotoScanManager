# Photogrammetry Point Report Generator
# Made by: Boris Bilc
# Version: 0.1 (alpha)

import zip_archive
import time
import datetime
from configparser import ConfigParser
from colorama import init, Fore, Back, Style
#init(autoreset=True)
init(autoreset=True)


# Application start greeting
print(Back.BLUE + "┌───────────────────────────────────────────────────────┐")
print(Back.BLUE + "│         Photogrammetry Point Report Generator         │")
print(Back.BLUE + "└───────────────────────────────────────────────────────┘" + Style.RESET_ALL)
time.sleep(1)

# Load settings from files in ./settings folder
def loadSettings():
	global meta_worksite, meta_station, meta_datetime, meta_serialnr, meta_surveyor
	
	print(Fore.GREEN + "\nLoading Settings...\n")
	
	time.sleep(1)
	configSettings()
	time.sleep(1)

	print("\nWorksite data:")
	f_worksite = open("settings/worksite.txt", "r")
	for x in f_worksite:
		print(x.strip())
	f_worksite.close()
	time.sleep(0.5)

	print("\nInstrument data:")
	f_instrument = open("settings/instrument.txt", "r")
	for x in f_instrument:
		print(x.strip())
	f_instrument.close()
	time.sleep(0.5)
	
	print("\nSurveyor data:")
	f_worksite = open("settings/surveyor.txt", "r")
	for x in f_worksite:
		print(x.strip())
	f_worksite.close()
	time.sleep(0.5)

	print("\nScan type data:")
	f_worksite = open("settings/scan_type.txt", "r")
	for x in f_worksite:
		print(x.strip())
	f_worksite.close()
	time.sleep(0.5)

	print("\nScan detail data:")
	f_worksite = open("settings/scan_detail.txt", "r")
	for x in f_worksite:
		print(x.strip())
	f_worksite.close()
	time.sleep(0.5)

	print(Style.RESET_ALL)


# Settings configuration
def configSettings():
	global metadata_export, metadata_external, metadata_fixed, logfile, processed_db, ftp_upload, auto_upload, backup, backup_cleanup
	global fixed_worksite, fixed_scan_type, fixed_scan_detail, fixed_instrument, fixed_surveyor, fixed_station
	config = ConfigParser()
	# instantiate
	config = ConfigParser()

	# parse existing file
	config.read('settings/app_settings.ini')

	# read values from a section
	metadata_export = config.getboolean('METADATA', 'metadata_export')
	metadata_external = config.getboolean('METADATA', 'metadata_external')
	metadata_fixed = config.getboolean('METADATA', 'metadata_fixed')
	logfile = config.getboolean('LOGS', 'logfile')
	processed_db = config.getboolean('LOGS', 'processed_db')
	ftp_upload = config.getboolean('UPLOAD', 'ftp_upload')
	auto_upload = config.getboolean('UPLOAD', 'auto_upload')
	backup = config.getboolean('BACKUP', 'backup')
	backup_cleanup = config.getboolean('BACKUP', 'backup_cleanup')
	fixed_worksite = config.get('METADATA', 'fixed_worksite')
	fixed_scan_type = config.get('METADATA', 'fixed_scan_type')
	fixed_scan_detail = config.get('METADATA', 'fixed_scan_detail')
	fixed_instrument = config.get('METADATA', 'fixed_instrument')
	fixed_surveyor = config.get('METADATA', 'fixed_surveyor')

	print("SETTINGS: METADATA")
	print("==================")
	print("Enable Metadata: " + str(metadata_export) + " / As external file: " + str(metadata_external) + " / Use fixed values: " + str(metadata_fixed) + "\n")
	if metadata_fixed == True:
		print("\t" + "METADATA FIXED VALUES")
		print("\t" + "=====================")
		print("\t" + "Worksite: " + str(fixed_worksite))
		print("\t" + "Scan Type: " + str(fixed_scan_type))
		print("\t" + "Scan Detail: " + str(fixed_scan_detail))
		print("\t" + "Instrument: " + str(fixed_instrument))
		print("\t" + "Surveyor: " + str(fixed_surveyor) + "\n")
	time.sleep(0.5)
	print("SETTINGS: LOGS")
	print("==============")
	print("Enable Logfile: " + str(logfile) + " / Processed DB: " + str(processed_db) + "\n")
	time.sleep(0.5)
	print("SETTINGS: FTP UPLOAD")
	print("====================")
	print("Enable FTP upload: " + str(ftp_upload) + " / Auto upload: " + str(auto_upload) + "\n")
	time.sleep(0.5)
	print("SETTINGS: BACKUP")
	print("================")
	print("Enable Backup: " + str(backup) + " / Backup Cleanup: " + str(backup_cleanup) + "\n")
	time.sleep(0.5)

	# update existing value
	#config.set('section_a', 'string_val', 'world')

	# add a new section and some values

	#config.add_section('section_b')
	#config.set('section_b', 'meal_val', 'spam')
	#config.set('section_b', 'not_found_val', '404')

	# save to a file
	#with open('test_update.ini', 'w') as configfile:
	#	config.write(configfile)


# Get folder names for processing
def readData():
	print("\n" + Fore.YELLOW + "Looking for new scan data in ../ScanDataNew/")


def formatPoint():
	global point_id, point_e, point_n, point_h, point_out
	point_id = "1"
	point_e = "406589.455"
	point_n = "45888.741"
	point_h = "22.259"
	out_id = datetime_out + "_" + point_id
	point_out = (f'{point_id:<20}' + f'{point_e:<20}' + f'{point_n:<20}' + f'{point_h:<20}')
	print(point_out)


# Enter Date and Time for new export
def setDateTime():
	global datetime_out
	dnow = datetime.datetime.now()
	print("\n" + Fore.YELLOW + "Date (Format= YYYY-MM-DD) >>>")
	date_in = input(dnow.strftime("%Y-%m-%d"))
	if date_in == "":
		date_in = dnow.strftime("%Y-%m-%d")
	print(Fore.YELLOW + "Time (Format= HH:MM) >>>")
	time_in = input(dnow.strftime("%H:%M"))
	if time_in == "":
		time_in = dnow.strftime("%H:%M")
	datetime_out = date_in + " - " + time_in


# Prepare and Write metadata header
def writeMetaHeader():
	# Template for Metadata output
	# Delovišče: T8 Koper
	# Podatki o izkopu: Izkop kalote na stacionaži 25+740.8
	# Datum in čas slikanja: 27.02.2022. 04:20
	# Serijska št. tahimetra: ------
	# Ime in priimek: Ssss mmmmm
	print("Metadata values")
	print(datetime_out)


loadSettings()
readData()
setDateTime()
writeMetaHeader()
formatPoint()
#zip_archive.zipFilesInDir("ScanDataUnprocessed", "ScanDataPackages/test.zip")