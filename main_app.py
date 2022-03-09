# Photogrammetry Point Report Generator
# Made by: Boris Bilc
# Version: 0.1 (alpha)

import zip_archive
import datetime
from configparser import ConfigParser
from colorama import init, Fore, Back, Style
init(autoreset=True)



# Application start greeting
print(Back.BLUE + "┌───────────────────────────────────────────────────────┐")
print(Back.BLUE + "│         Photogrammetry Point Report Generator         │")
print(Back.BLUE + "└───────────────────────────────────────────────────────┘")


# Load settings from files in ./settings folder
def loadSettings():
	global meta_worksite, meta_station, meta_datetime, meta_serialnr, meta_surveyor
	print("Loading Settings...")
	
	print("\nWorksite data:")
	f_worksite = open("settings/worksite.txt", "r")
	for x in f_worksite:
		print(x.strip())
	f_worksite.close()

	print("\nInstrument data:")
	f_instrument = open("settings/instrument.txt", "r")
	for x in f_instrument:
		print(x.strip())
	f_instrument.close()
	
	print("\nSurveyor data:")
	f_worksite = open("settings/surveyor.txt", "r")
	for x in f_worksite:
		print(x.strip())
	f_worksite.close()

	print("\nScan type data:")
	f_worksite = open("settings/scan_type.txt", "r")
	for x in f_worksite:
		print(x.strip())
	f_worksite.close()

	print("\nScan detail data:")
	f_worksite = open("settings/scan_detail.txt", "r")
	for x in f_worksite:
		print(x.strip())
	f_worksite.close()


# Settings configuration
def configSettings():
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
	print("\n" + Fore.YELLOW + "Looking for new scan data in ../ScanData/")


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
zip_archive.zipFilesInDir("ScanDataUnprocessed", "ScanDataPackages/test.zip")