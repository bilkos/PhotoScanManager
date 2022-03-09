# Photogrammetry Point Report Generator
# Made by: Boris Bilc
# Version: 0.1 (alpha)

import modlib.zip_archive as zip_archive
import time
import datetime
from configparser import ConfigParser
from colorama import init, Fore, Back, Style
#init(autoreset=True)
init(autoreset=True)


# Application start greeting
print(Back.BLUE + Fore.YELLOW + Style.BRIGHT + "┌───────────────────────────────────────────────────────┐")
print(Back.BLUE + Fore.YELLOW + Style.BRIGHT + "│         Photogrammetry Point Report Generator         │")
print(Back.BLUE + Fore.YELLOW + Style.BRIGHT + "└───────────────────────────────────────────────────────┘")
time.sleep(1)

# Read settings configuration from 'app_settings.ini'
def configSettingsRead():
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

	print(Fore.GREEN + "SETTINGS: METADATA")
	print(Fore.GREEN + "==================")
	print(Fore.GREEN + "Enable Metadata: " + Fore.CYAN + Style.BRIGHT + str(metadata_export))
	print(Fore.GREEN + "Create external file: " + Fore.CYAN + Style.BRIGHT + str(metadata_external))
	print(Fore.GREEN + "Use fixed values: " + Fore.CYAN + Style.BRIGHT + str(metadata_fixed) + "\n")
	if metadata_fixed == True:
		print(Fore.GREEN + "\t" + "METADATA FIXED VALUES")
		print(Fore.GREEN + "\t" + "=====================")
		print(Fore.GREEN + "\t" + "Worksite: " + Fore.CYAN + Style.BRIGHT + str(fixed_worksite))
		print(Fore.GREEN + "\t" + "Scan Type: " + Fore.CYAN + Style.BRIGHT + str(fixed_scan_type))
		print(Fore.GREEN + "\t" + "Scan Detail: " + Fore.CYAN + Style.BRIGHT + str(fixed_scan_detail))
		print(Fore.GREEN + "\t" + "Instrument: " + Fore.CYAN + Style.BRIGHT + str(fixed_instrument))
		print(Fore.GREEN + "\t" + "Surveyor: " + Fore.CYAN + Style.BRIGHT + str(fixed_surveyor) + "\n")
	time.sleep(0.2)
	print(Fore.GREEN + "SETTINGS: LOGS")
	print(Fore.GREEN + "==============")
	print(Fore.GREEN + "Enable Logfile: " + Fore.CYAN + Style.BRIGHT + str(logfile))
	print(Fore.GREEN + "Processed DB: " + Fore.CYAN + Style.BRIGHT + str(processed_db) + "\n")
	time.sleep(0.2)
	print(Fore.GREEN + "SETTINGS: FTP UPLOAD")
	print(Fore.GREEN + "====================")
	print(Fore.GREEN + "Enable FTP upload: " + Fore.CYAN + Style.BRIGHT + str(ftp_upload))
	print(Fore.GREEN + "Auto upload: " + Fore.CYAN + Style.BRIGHT + str(auto_upload) + "\n")
	time.sleep(0.2)
	print(Fore.GREEN + "SETTINGS: BACKUP")
	print(Fore.GREEN + "================")
	print(Fore.GREEN + "Enable Backup: " + Fore.CYAN + Style.BRIGHT + str(backup))
	print(Fore.GREEN + "Backup Cleanup: " + Fore.CYAN + Style.BRIGHT + str(backup_cleanup) + "\n")

	# update existing value
	#config.set('section_a', 'string_val', 'world')

	# add a new section and some values

	#config.add_section('section_b')
	#config.set('section_b', 'meal_val', 'spam')
	#config.set('section_b', 'not_found_val', '404')

	# save to a file
	#with open('test_update.ini', 'w') as configfile:
	#	config.write(configfile)


# Load settings from files in ./settings folder
def metaOptionsRead():
	global meta_worksite, meta_station, meta_datetime, meta_serialnr, meta_surveyor
	
	print(Fore.GREEN + "\nWorksite data:")
	f_worksite = open("settings/worksite.txt", "r")
	for x in f_worksite:
		print(Fore.CYAN + Style.BRIGHT + x.strip())
	f_worksite.close()
	time.sleep(0.2)

	print(Fore.GREEN + "\nInstrument data:")
	f_instrument = open("settings/instrument.txt", "r")
	for x in f_instrument:
		print(Fore.CYAN + Style.BRIGHT + x.strip())
	f_instrument.close()
	time.sleep(0.2)
	
	print(Fore.GREEN + "\nSurveyor data:")
	f_worksite = open("settings/surveyor.txt", "r")
	for x in f_worksite:
		print(Fore.CYAN + Style.BRIGHT + x.strip())
	f_worksite.close()
	time.sleep(0.2)

	print(Fore.GREEN + "\nScan type data:")
	f_worksite = open("settings/scan_type.txt", "r")
	for x in f_worksite:
		print(Fore.CYAN + Style.BRIGHT + x.strip())
	f_worksite.close()
	time.sleep(0.2)

	print(Fore.GREEN + "\nScan detail data:")
	f_worksite = open("settings/scan_detail.txt", "r")
	for x in f_worksite:
		print(Fore.CYAN + Style.BRIGHT + x.strip())
	f_worksite.close()
	time.sleep(0.2)

	print(Style.RESET_ALL)


# Settings configuration
def settingsRead():
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

	print(Fore.GREEN + "SETTINGS: METADATA")
	print(Fore.GREEN + "==================")
	print(Fore.GREEN + "Enable Metadata: " + Fore.CYAN + Style.BRIGHT + str(metadata_export))
	print(Fore.GREEN + "Create external file: " + Fore.CYAN + Style.BRIGHT + str(metadata_external))
	print(Fore.GREEN + "Use fixed values: " + Fore.CYAN + Style.BRIGHT + str(metadata_fixed) + "\n")
	if metadata_fixed == True:
		print(Fore.GREEN + "\t" + "METADATA FIXED VALUES")
		print(Fore.GREEN + "\t" + "=====================")
		print(Fore.GREEN + "\t" + "Worksite: " + Fore.CYAN + Style.BRIGHT + str(fixed_worksite))
		print(Fore.GREEN + "\t" + "Scan Type: " + Fore.CYAN + Style.BRIGHT + str(fixed_scan_type))
		print(Fore.GREEN + "\t" + "Scan Detail: " + Fore.CYAN + Style.BRIGHT + str(fixed_scan_detail))
		print(Fore.GREEN + "\t" + "Instrument: " + Fore.CYAN + Style.BRIGHT + str(fixed_instrument))
		print(Fore.GREEN + "\t" + "Surveyor: " + Fore.CYAN + Style.BRIGHT + str(fixed_surveyor) + "\n")
	time.sleep(0.2)
	print(Fore.GREEN + "SETTINGS: LOGS")
	print(Fore.GREEN + "==============")
	print(Fore.GREEN + "Enable Logfile: " + Fore.CYAN + Style.BRIGHT + str(logfile))
	print(Fore.GREEN + "Processed DB: " + Fore.CYAN + Style.BRIGHT + str(processed_db) + "\n")
	time.sleep(0.2)
	print(Fore.GREEN + "SETTINGS: FTP UPLOAD")
	print(Fore.GREEN + "====================")
	print(Fore.GREEN + "Enable FTP upload: " + Fore.CYAN + Style.BRIGHT + str(ftp_upload))
	print(Fore.GREEN + "Auto upload: " + Fore.CYAN + Style.BRIGHT + str(auto_upload) + "\n")
	time.sleep(0.2)
	print(Fore.GREEN + "SETTINGS: BACKUP")
	print(Fore.GREEN + "================")
	print(Fore.GREEN + "Enable Backup: " + Fore.CYAN + Style.BRIGHT + str(backup))
	print(Fore.GREEN + "Backup Cleanup: " + Fore.CYAN + Style.BRIGHT + str(backup_cleanup) + "\n")

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
def dataRead():
	print("\n" + Fore.YELLOW + "Looking for new scan data in ../ScanDataNew/")


def pointFormat():
	global point_id, point_e, point_n, point_h, point_out
	point_id = "1"
	point_e = "406589.455"
	point_n = "45888.741"
	point_h = "22.259"
	out_id = datetime_out + "_" + point_id
	point_out = (f'{point_id:<20}' + f'{point_e:<20}' + f'{point_n:<20}' + f'{point_h:<20}')
	print(point_out)


# Enter Date and Time for new export
def metaUserDatetime():
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
def metaExport():
	# Template for Metadata output
	'''
	Datum in čas: 27.02.2022. 04:20
	Delovišče: T8 Koper
	Podatki: Izkop kalote na stacionaži 25+740.8
	Stacionaža: 25+999.0
	Instrument: TS16 1" (123456)
	Ime in priimek: Toje Posnel
	'''
	print("Metadata values")
	print(datetime_out)

def packageCreate(source_folder, package_file):
	zip_archive.zipFilesInDir(source_folder, package_file)

# App startup
def appStartup():
	print(Fore.GREEN + "\nLoading Settings...\n")
	time.sleep(0.5)
	settingsRead()
	time.sleep(0.5)
	metaOptionsRead()
	time.sleep(0.5)

	print(Fore.YELLOW + "Continue (" + Style.BRIGHT + "Enter" + Style.DIM + ") / Settings (" + Style.BRIGHT + "S" + Style.DIM + ") / Quit (" + Style.BRIGHT + "Q" + Style.DIM + ")")
	app_start = input()
	if app_start == "s" or app_start == "S":
		print(Fore.MAGENTA + Style.BRIGHT + "Settings Configuration...")
	elif app_start == "q" or app_start == "Q":
		print(Fore.RED + Style.BRIGHT + "\nStopping app...\nGood bye!\n\n")
		quit()
	else:
		print(Fore.GREEN + Style.BRIGHT + "Start...")
		dataRead()
		metaUserDatetime()
		metaExport()
		pointFormat()


appStartup()
