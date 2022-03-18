# Photogrammetry Scan Manager
# Made by: Boris Bilc

# IMPORT MODULES & GENERAL VARIABLES
import modlib.zip_archive as zip_archive
import os
import time
import datetime
import locale
from configparser import ConfigParser
from colorama import init, Fore, Back, Style
import PySimpleGUI as sg

# Import and initialize colorama module
init(autoreset=True)

# Set default locale for app
locale.setlocale(locale.LC_ALL, 'sl_SI')

# Import and initialize PySimpleGUI module
sg.theme('SystemDefaultForReal')		# GUI Color Theme (SystemDefaultForReal, Python, DarkGrey14)

# Default App Font for GUI
app_font_title = 'Bahnschrift 20 bold'
app_font_subtitle = 'Bahnschrift 14 bold'
app_font_ver = 'Bahnschrift 9 bold'
app_font = 'Bahnschrift 11'
sg.set_options(font=app_font)

# Main App Configuration & Info
app_version = '0.1'		# App version (build)
app_build = '57'
app_settings_ini = 'settings/app_settings.ini'

# Global app variables
new_count = 0					# New datasets counter init
process_start = False			# Start process initialize

# Button colors
greenBtnColor = "#b3ff00"
blueBtnColor = "#59acff"
orangeBtnColor = "#ffc800"
redBtnColor = "#fa5757"


# Load settings from files in ./settings folder
def metaOptionsRead():
	global meta_worksite, meta_instrument, meta_station, meta_date, meta_time, meta_surveyor, meta_scantype, meta_scandet
	
	# Choose worksite
	openfile = open("settings/worksite.txt", "r")
	openfile_list = openfile.readlines()
	openfile_i = 0
	# Count options in opened file
	for x in openfile_list:
		openfile_list[openfile_i] = openfile_list[openfile_i].strip()
		openfile_i = openfile_i + 1
	openfile.close()
	# Prepare Layout (left column)
	layout_work = [
		[sg.Text('Worksite:')],
		# Create List object with options
		[sg.Listbox(openfile_list, default_values=openfile_list[0], key='meta_worksite', s=(25, openfile_i), select_mode='LISTBOX_SELECT_MODE_SINGLE', auto_size_text=True)],
	]
	
	# Choose instrument
	openfile = open("settings/instrument.txt", "r")
	openfile_list = openfile.readlines()
	openfile_i = 0
	# Count options in opened file
	for x in openfile_list:
		openfile_list[openfile_i] = openfile_list[openfile_i].strip()
		openfile_i = openfile_i + 1
	openfile.close()
	# Prepare Layout (left column)
	layout_inst = [
		[sg.Text('Instrument:')],
		# Create List object with options
		[sg.Listbox(openfile_list, default_values=openfile_list[0], key='meta_instrument', s=(25, openfile_i), select_mode='LISTBOX_SELECT_MODE_SINGLE', auto_size_text=True)],
	]
	
		
	# Choose surveyor name
	openfile = open("settings/surveyor.txt", "r")
	openfile_list = openfile.readlines()
	openfile_i = 0
	# Count options in opened file
	for x in openfile_list:
		openfile_list[openfile_i] = openfile_list[openfile_i].strip()
		openfile_i = openfile_i + 1
	openfile.close()
	# Prepare Layout (left column)
	layout_surveyor = [
		[sg.Text('Surveyor:')],
		# Create List object with options
		[sg.Listbox(openfile_list, default_values=openfile_list[0], key='meta_surveyor', s=(25, openfile_i), select_mode='LISTBOX_SELECT_MODE_SINGLE', auto_size_text=True)],
	]
	
	
	# Choose type of scan
	openfile = open("settings/scan_type.txt", "r")
	openfile_list = openfile.readlines()
	openfile_i = 0
	# Count options in 'scan_type.txt'
	for x in openfile_list:
		openfile_list[openfile_i] = openfile_list[openfile_i].strip()
		openfile_i = openfile_i + 1
	openfile.close()
	# Prepare Layout (left column)
	layout_scantype = [
		[sg.Text('Scan type:')],
		# Create List object with options
		[sg.Listbox(openfile_list, default_values=openfile_list[0], key="meta_scantype", s=(25, openfile_i), select_mode='LISTBOX_SELECT_MODE_SINGLE', auto_size_text=True)],
	]	

	
	# Choose type of scan detail
	openfile = open("settings/scan_detail.txt", "r")
	openfile_list = openfile.readlines()
	openfile_i = 0
	# Count options in 'scan_type.txt'
	for x in openfile_list:
		openfile_list[openfile_i] = openfile_list[openfile_i].strip()
		openfile_i = openfile_i + 1
	openfile.close()
	# Prepare Layout (left column)
	layout_scandet = [
		[sg.Text('Scan detail:')],
		# Create List object with options
		[sg.Listbox(openfile_list, default_values=openfile_list[0], key="meta_scandet", s=(25, openfile_i), select_mode='LISTBOX_SELECT_MODE_SINGLE', auto_size_text=True)],
	]


	# Get current date/time as 'dnow' variable
	dnow = datetime.datetime.now()
	# Enter station of scanned profile / Date and Time for new export
	layout_station = [
		[sg.Text('Station (##+###.#):')],
		[sg.Input(default_text='n/a', s=(15,1), focus=True, key="meta_station")],
	]

	layout_date = [
		[sg.Text('Date & Time:')],
		[sg.Input(default_text=dnow.strftime("%Y-%m-%d"), key='meta_date', size=(12,1)), sg.Input(default_text=dnow.strftime("%H:%M"), key='meta_time', size=(6,1))],
		[sg.CalendarButton('Date Picker', format='%Y-%m-%d', title = "Choose Date", key="meta_datepicker", target='meta_date', button_color=blueBtnColor)],
	]


	layout_meta = [
		[sg.Text("METADATA Options", font=app_font_subtitle)],
		[sg.HorizontalSeparator()],
		[sg.vtop([sg.Col(layout_work), sg.Col(layout_inst)])],
		[sg.vtop([sg.Col(layout_scantype), sg.Col(layout_surveyor)])],
		[sg.vtop([sg.Col(layout_scandet)])],
		[sg.vtop([sg.Col(layout_station), sg.Col(layout_date)])],
		[sg.Save("Continue", key='CONT', focus=True, button_color=greenBtnColor), sg.Cancel('Back', key='BACK', button_color=orangeBtnColor), sg.Quit('Quit', key='QUIT', button_color=redBtnColor)]
		# [sg.Button('[C]ontinue', key='CONT', button_color=greenBtnColor), sg.Button('[Q]uit', key='QUIT', button_color=redBtnColor)]
	]
	
	window2 = sg.Window('Metadata options', layout_meta, use_default_focus=False, font=app_font, finalize=True)
	window2.Element('CONT').SetFocus()
	window2.bind('<c>', 'CONT')
	window2.bind('<c>', 'CONT')
	window2.bind('<b>', 'BACK')
	window2.bind('<b>', 'BACK')
	window2.bind('<q>', 'QUIT')
	window2.bind('<q>', 'QUIT')
	window2.bind('<Escape>', 'BACK')

	while True:
		event, values = window2.read()
		
		# End program if user closes window or
		# presses the OK button
		if event == "CONT":
			replace_chars = "'[]"
			process_start = True
			window2.close()
			
			meta_worksite = str(values['meta_worksite'])
			meta_instrument = str(values['meta_instrument'])
			meta_surveyor = str(values['meta_surveyor'])
			meta_scantype = str(values['meta_scantype'])
			meta_scandet = str(values['meta_scandet'])
			meta_station = str(values['meta_station'])
			meta_date = str(values['meta_date'])
			meta_time = str(values['meta_time'])

			for replace_chars in replace_chars:
				meta_worksite = meta_worksite.replace(replace_chars, '')
				meta_instrument = meta_instrument.replace(replace_chars, '')
				meta_surveyor = meta_surveyor.replace(replace_chars, '')
				meta_scantype = meta_scantype.replace(replace_chars, '')
				meta_scandet = meta_scandet.replace(replace_chars, '')
				meta_station = meta_station.replace(replace_chars, '')
				meta_date = meta_date.replace(replace_chars, '')
				meta_time = meta_time.replace(replace_chars, '')

			
			# Show results in a popup window
			clicked = sg.popup('Confirm selection...',
			'Worksite: ' + meta_worksite,
			'Instrument: ' + meta_instrument,
			'Surveyor: ' + meta_surveyor,
			'Scan type: ' + meta_scantype,
			'Scan detail: ' + meta_scandet,
			'Station: ' + meta_station,
			'Date / Time: ' + meta_date + ' / ' + meta_time,
			title='Confirm metadata options')

			if clicked == 'OK':
				break
			if clicked == None:
				appStartupMenu(False)

			window2.close()

		if event == "BACK":
			window2.close()
			appStartupMenu(False)
		
		if event == "QUIT":
			window2.close()
			quit()

		if event == sg.WIN_CLOSED and process_start == False:
			print(Fore.RED + Style.BRIGHT + "\n\nExiting app...\n\nGood bye!\n")
			quit()

	window2.close()


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
	config.read(app_settings_ini)

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

	'''
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
	'''

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
	print("Process finished.")
	process_start = False
	time.sleep(1)
	appStartupMenu(process_start)


# Start main process
def appStartProcess():
	print(Fore.GREEN + "Waiting for metadata user input...")
	if metadata_fixed == False:
		metaOptionsRead()
		
	print(Fore.GREEN + "Metadata preared.\nStarting process...")
	time.sleep(0.1)
	print("\nScanning for new data in: " + path_scandata + "\n")
	scanFolders(path_scandata)
	print(Fore.GREEN + "\nFound: " + str(new_count) + " folders with new data-sets...\n")
	processNewData()


def appStartupMenu(process_start):
	# Clear terminal screen on startup
	os.system('cls||clear')
	# Application start greeting
	print(Back.BLUE + Fore.YELLOW + Style.BRIGHT + "┌──────────────────────────────────────┐")
	print(Back.BLUE + Fore.YELLOW + Style.BRIGHT + "│                                      │")
	print(Back.BLUE + Fore.YELLOW + Style.BRIGHT + "│          PHOTO-SCAN Manager          │")
	print(Back.BLUE + Fore.YELLOW + Style.BRIGHT + "│    -------------------------------   │")
	print(Back.BLUE + Fore.YELLOW + Style.BRIGHT + "│   Made by Boris Bilc / CELU, d.o.o.  │")
	print(Back.BLUE + Fore.YELLOW + Style.BRIGHT + "│                                      │")
	print(Back.BLUE + Fore.YELLOW + Style.BRIGHT + "└──────────────────────────────────────┘")
	print(Fore.BLUE + Style.BRIGHT + " App Version: " + str(app_version) + " - Build: " + str(app_build))
	time.sleep(0.1)
	# Load main app settings
	print(Fore.GREEN + "Loading Settings File: " + app_settings_ini)
	time.sleep(0.2)
	settingsRead()
	print(Fore.GREEN + "Loading Settings... Done.\n")
	

	layout = [
		[sg.Text("PHOTO-SCAN Manager", font=app_font_title, text_color=blueBtnColor)],
		[sg.Text("Version: " + str(app_version) + " - build: " + str(app_build), font=app_font_ver, text_color='#9b9b9b')],
		[sg.HorizontalSeparator()],
		[sg.Text("START MENU", font=app_font_subtitle)],
		[sg.Text("Continue: Start report manager process...")],
		[sg.Text("Settings: Edit app settings configuration.")],
		[sg.Text("Quit: Close application.")],
		[sg.Button("Continue", focus=True, key='RUN', button_color=greenBtnColor), sg.Button("Settings", key='SET', disabled=True, button_color=blueBtnColor), sg.VerticalSeparator(), sg.Button("Quit", key='QUIT', button_color=redBtnColor)],
		]

	# Create the window
	window1 = sg.Window("PHOTO-SCAN Manager", layout, element_justification='c', font=app_font, finalize=True)
	window1.Element('RUN').SetFocus()
	window1.bind('<c>', 'RUN')
	window1.bind('<C>', 'RUN')
	window1.bind('<s>', 'SET')
	window1.bind('<S>', 'SET')
	window1.bind('<q>', 'QUIT')
	window1.bind('<Q>', 'QUIT')
	window1.bind('<Escape>', 'QUIT')

	# Create an event loop
	while True:
		event, values = window1.read()
		
		# End program if user closes window or
		# presses the OK button
		if event == "RUN":
			process_start = True
			window1.close()
			appStartProcess()
		if event == "SETTINGS":
			process_start = True
			window1.close()
			appStartProcess()
		if event == "QUIT":
			print(Fore.RED + Style.BRIGHT + "\n\nExiting app...\n\nGood bye!\n")
			process_start = False
			break
		if event == sg.WIN_CLOSED and process_start == False:
			print(Fore.RED + Style.BRIGHT + "\n\nExiting app...\n\nGood bye!\n")
			break

	window1.close()		
	quit()

# Start App by opening Start Menu
appStartupMenu(process_start)
