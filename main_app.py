# Photogrammetry Point Report Generator
# Made by: Boris Bilc
# Version: 0.0.1 (alpha)

import modlib.zip_archive as zip_archive
import os
import time
import datetime
from configparser import ConfigParser
from colorama import init, Fore, Back, Style
#init(autoreset=True)
init(autoreset=True)

version = '0.2.1'
new_count = 0

# Load settings from files in ./settings folder
def metaOptionsRead():
	global meta_worksite, meta_instrument, meta_station, meta_datetime, meta_surveyor, meta_scantype, meta_scandet

	os.system('cls||clear')
	
	# Choose worksite of scan
	print(Fore.GREEN + "Worksite:")
	openfile = open("settings/worksite.txt", "r")
	openfile_list = openfile.readlines()
	openfile_i = 0
	for x_fw in openfile_list:
		print(Fore.CYAN + "[" + str(openfile_i) + "] " + Style.BRIGHT + str(x_fw).strip())
		openfile_i = openfile_i + 1
	user_input = int(input("Choose option >>> "))
	if user_input >= 0 and user_input <= openfile_i:
			meta_worksite = str(openfile_list[user_input]).strip()
			print(meta_worksite + " <- OK")
	openfile.close()
	
	# Choose instrument used
	print(Fore.GREEN + "Instrument:")
	openfile = open("settings/instrument.txt", "r")
	openfile_list = openfile.readlines()
	openfile_i = 0
	for x_fw in openfile_list:
		print(Fore.CYAN + "[" + str(openfile_i) + "] " + Style.BRIGHT + str(x_fw).strip())
		openfile_i = openfile_i + 1
	user_input = int(input("Choose option >>> "))
	if user_input >= 0 and user_input <= openfile_i:
			meta_instrument = str(openfile_list[user_input]).strip()
			print(meta_instrument + " <- OK")
	openfile.close()
	
	# Choose surveyor name
	print(Fore.GREEN + "Surveyor:")
	openfile = open("settings/surveyor.txt", "r")
	openfile_list = openfile.readlines()
	openfile_i = 0
	for x_fw in openfile_list:
		print(Fore.CYAN + "[" + str(openfile_i) + "] " + Style.BRIGHT + str(x_fw).strip())
		openfile_i = openfile_i + 1
	user_input = int(input("Choose option >>> "))
	if user_input >= 0 and user_input <= openfile_i:
			meta_surveyor = str(openfile_list[user_input]).strip()
			print(meta_surveyor + " <- OK")
	openfile.close()
	
	# Choose type of scan
	print(Fore.GREEN + "Scan type:")
	openfile = open("settings/scan_type.txt", "r")
	openfile_list = openfile.readlines()
	openfile_i = 0
	for x_fw in openfile_list:
		print(Fore.CYAN + "[" + str(openfile_i) + "] " + Style.BRIGHT + str(x_fw).strip())
		openfile_i = openfile_i + 1
	user_input = int(input("Choose option >>> "))
	if user_input >= 0 and user_input <= openfile_i:
			meta_scantype = str(openfile_list[user_input]).strip()
			print(meta_scantype + " <- OK")
	openfile.close()
	
	# Choose type of scan detail
	print(Fore.GREEN + "Scan detail:")
	openfile = open("settings/scan_detail.txt", "r")
	openfile_list = openfile.readlines()
	openfile_i = 0
	for x_fw in openfile_list:
		print(Fore.CYAN + "[" + str(openfile_i) + "] " + Style.BRIGHT + str(x_fw).strip())
		openfile_i = openfile_i + 1
	user_input = int(input("Choose option >>> "))
	if user_input >= 0 and user_input <= openfile_i:
			meta_scandet = str(openfile_list[user_input]).strip()
			print(meta_scandet + " <- OK")
	openfile.close()
	
	# Enter station of scanned profile
	print(Fore.GREEN + "Station of scanned profile:")
	meta_station = input("Enter scan station (XX+XXX.XX) >>> ")
	print(str(meta_station) + " <- OK")

	# Enter Date and Time for new export
	dnow = datetime.datetime.now()
	print("\n" + Fore.YELLOW + "Enter Date of scan (Format= YYYY-MM-DD) >>> ")
	date_in = input(dnow.strftime("%Y-%m-%d"))
	if date_in == "":
		date_in = dnow.strftime("%Y-%m-%d")
	print(Fore.YELLOW + "Enter Time of scan (Format= HH:MM) >>> ")
	time_in = input(dnow.strftime("%H:%M"))
	if time_in == "":
		time_in = dnow.strftime("%H:%M")
	meta_datetime = date_in + " / " + time_in
	time.sleep(0.5)

	print(Style.RESET_ALL)
	os.system('cls||clear')
	
	print(Fore.GREEN + "Worksite: " + meta_worksite)
	print(Fore.GREEN + "Scan type: " + meta_scantype)
	print(Fore.GREEN + "Scan detail: " + meta_scandet)
	print(Fore.GREEN + "Station: " + meta_station)
	print(Fore.GREEN + "Instrument: " + meta_instrument)
	print(Fore.GREEN + "Surveyor: " + meta_surveyor)
	print(Fore.GREEN + "Date / Time: " + meta_datetime)
	


# Read active settings 
def settingsRead():
	# Global variables for settings
	global path_scandata, path_packages, path_backup
	global metadata_export, metadata_external, metadata_fixed
	global fixed_worksite, fixed_scan_type, fixed_scan_detail, fixed_instrument, fixed_surveyor
	global logfile, processed_db
	global ftp_upload, auto_upload
	global backup, backup_cleanup

	# Prepare config parser
	config = ConfigParser()

	# Read settings from 'app_settings.ini' and parse them as variables 
	config.read('settings/app_settings.ini')

	path_scandata = config.get('FOLDERS', 'path_scandata')
	path_packages = config.get('FOLDERS', 'path_packages')
	path_backup = config.get('FOLDERS', 'path_backup')
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

	# Print current settings at app startup
	print(Fore.GREEN + "SETTINGS: FOLDERS")
	print(Fore.GREEN + "==================")
	print(Fore.GREEN + "Enable Metadata: " + Fore.CYAN + Style.BRIGHT + str(path_scandata))
	print(Fore.GREEN + "Create external file: " + Fore.CYAN + Style.BRIGHT + str(path_packages))
	print(Fore.GREEN + "Use fixed values: " + Fore.CYAN + Style.BRIGHT + str(path_backup) + "\n")
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
	time.sleep(0.1)
	print(Fore.GREEN + "SETTINGS: LOGS")
	print(Fore.GREEN + "==============")
	print(Fore.GREEN + "Enable Logfile: " + Fore.CYAN + Style.BRIGHT + str(logfile))
	print(Fore.GREEN + "Processed DB: " + Fore.CYAN + Style.BRIGHT + str(processed_db) + "\n")
	time.sleep(0.1)
	print(Fore.GREEN + "SETTINGS: FTP UPLOAD")
	print(Fore.GREEN + "====================")
	print(Fore.GREEN + "Enable FTP upload: " + Fore.CYAN + Style.BRIGHT + str(ftp_upload))
	print(Fore.GREEN + "Auto upload: " + Fore.CYAN + Style.BRIGHT + str(auto_upload) + "\n")
	time.sleep(0.1)
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


filedb_datasets = open("settings/new_dataset_folders.txt", "w")
filedb_datasets.write("")
filedb_pointfiles = open("settings/new_dataset_points.txt", "w")
filedb_pointfiles.write("")


# Get folder names for processing
def scanFolders(rootdir):
	global new_count
	global filedb_datasets, filedb_pointfiles
	filedb_datasets = open("settings/new_dataset_folders.txt", "a")
	filedb_pointfiles = open("settings/new_dataset_points.txt", "a")

	for file in os.listdir(rootdir):
		d = os.path.join(rootdir, file)
		
		if os.path.isdir(d):
			if d.endswith("photos"):
				#d = d.replace("\\", "/")
				#print(Fore.CYAN + d)
				scanFolders(d)
			else:
				d = d.replace("\\", "/")
				print(Fore.GREEN + d)
				scanFolders(d)
				new_count = new_count + 1
				filedb_datasets.write(d + "\n")
				filedb_datasets.close()
		elif os.path.isfile(d) and file.endswith(".txt") and file.find("point") == 0:
			d = d.replace("\\", "/")
			print(Fore.YELLOW + d)
			filedb_pointfiles.write(d + "\n")
			filedb_pointfiles.close()



def pointFormat():
	global point_id, point_e, point_n, point_h, point_out
	point_id = "1"
	point_e = "406589.455"
	point_n = "45888.741"
	point_h = "22.259"
	point_out = (f'{point_id:<20}' + f'{point_e:<20}' + f'{point_n:<20}' + f'{point_h:<20}')
	print(point_out)


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


def packDataset(source_folder, package_file):
	zip_archive.zipFilesInDir(source_folder, package_file)

# Process new data-sets
def processNewData():
	metaExport()
	pointFormat()
	#packDataset()


def appStartup():
	# Application start greeting
	print(Back.BLUE + Fore.YELLOW + Style.BRIGHT + "┌───────────────────────────────────────────────────────┐")
	print(Back.BLUE + Fore.YELLOW + Style.BRIGHT + "│                                                       │")
	print(Back.BLUE + Fore.YELLOW + Style.BRIGHT + "│          Photogrammetry Point Report Manager          │")
	print(Back.BLUE + Fore.YELLOW + Style.BRIGHT + "│          -----------------------------------          │")
	print(Back.BLUE + Fore.YELLOW + Style.BRIGHT + "│           Made by Boris Bilc / CELU, d.o.o.           │")
	print(Back.BLUE + Fore.YELLOW + Style.BRIGHT + "│                                                       │")
	print(Back.BLUE + Fore.YELLOW + Style.BRIGHT + "└───────────────────────────────────────────────────────┘")
	print(Fore.BLUE + Style.BRIGHT + " App Version: " + version + "\n")
	time.sleep(0.25)

	print(Fore.YELLOW + "┌────────────────────┐")
	print(Fore.YELLOW + "│ .:: START MENU ::. │")
	print(Fore.YELLOW + "│--------------------│")
	print(Fore.YELLOW + "│ ("+ Style.BRIGHT + "Enter" + Fore.YELLOW + Style.DIM + ") Continue   │")
	print(Fore.YELLOW + "│ ("+ Style.BRIGHT + "S" + Fore.YELLOW + Style.DIM + ") Settings       │")
	print(Fore.YELLOW + "│ ("+ Style.BRIGHT + "Q" + Fore.YELLOW + Style.DIM + ") Quit           │")
	print(Fore.YELLOW + "└────────────────────┘\n")
	
	app_start = input(">>> ")
	
	if app_start == "s" or app_start == "S":
		print(Fore.MAGENTA + Style.BRIGHT + "Settings Configuration...")
	elif app_start == "q" or app_start == "Q":
		print(Fore.RED + Style.BRIGHT + "\n\nExiting app...\n\nGood bye!\n")
		quit()
	else:
		print(Fore.GREEN + "Starting process...")
		print(Fore.GREEN + "\nLoading Settings...\n")
		time.sleep(0.1)
		settingsRead()
		time.sleep(0.1)
		if metadata_fixed == False:
			metaOptionsRead()
			time.sleep(0.1)
		print("\nScanning for new data in: " + path_scandata + "\n")
		scanFolders(path_scandata)
		print(Fore.GREEN + "\nFound: " + str(new_count) + " folders with new data-sets...\n")
		print("Process finished.")

		processNewData()


appStartup()
