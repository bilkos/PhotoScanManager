# Photogrammetry Scan Manager
# Made by: Boris Bilc

# IMPORT MODULES & GENERAL VARIABLES
import modlib.zip_archive as zip_archive
import os
import time
import datetime
import locale
import subprocess
from configparser import ConfigParser
from colorama import init, Fore, Back, Style
import PySimpleGUI as sg

# Import and initialize colorama module
init(autoreset=True)

# Set default locale for app
locale.setlocale(locale.LC_ALL, 'sl_SI')

# <!#FV>
app_version = '0.1.63'
#  </#FV>

# App icon
app_icon = 'appicon.ico'

# Main App Configuration & Info
app_settings_ini = 'settings/app_settings.ini'

# Import and initialize PySimpleGUI module
sg.theme('DarkGrey14')		# GUI Color Theme (DarkBlue3, SystemDefaultForReal, Python, DarkGrey14)

# Button colors
greenBtnColor = "#4cb000"
blueBtnColor = "#59acff"
orangeBtnColor = "#db8504"
redBtnColor = "#b00000"
titleColor = '#ffc559'
textColWhite = '#ffffff'
textColBlack = '#000000'
listboxBg = '#3282d1'

# Default App Font for GUI
app_font_title = 'Bahnschrift 20 bold'
app_font_subtitle = 'Bahnschrift 14 bold'
app_font_ver = 'Bahnschrift 9 bold'
app_font_menubar = 'Bahnschrift 9'
app_font_statusbar = 'Bahnschrift 8'
app_font = 'Bahnschrift 11'
sg.set_options(font=app_font)


# Global app variables
new_count = 0					# New datasets counter init
process_start = False			# Start process initialize

app_statusbar_text = 'App started...'

# Load settings from files in ./settings folder
def metaOptionsRead():
	selectDataToProcess()
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
		[sg.Listbox(openfile_list, default_values=openfile_list[0], key='meta_worksite', highlight_text_color=textColWhite, highlight_background_color=listboxBg, s=(25, openfile_i), select_mode='LISTBOX_SELECT_MODE_SINGLE', auto_size_text=True)],
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
		[sg.Listbox(openfile_list, default_values=openfile_list[0], key='meta_instrument', highlight_text_color=textColWhite, highlight_background_color=listboxBg, s=(25, openfile_i), select_mode='LISTBOX_SELECT_MODE_SINGLE', auto_size_text=True)],
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
		[sg.Listbox(openfile_list, default_values=openfile_list[0], key='meta_surveyor', highlight_text_color=textColWhite, highlight_background_color=listboxBg, s=(25, openfile_i), select_mode='LISTBOX_SELECT_MODE_SINGLE', auto_size_text=True)],
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
		[sg.Listbox(openfile_list, default_values=openfile_list[0], key="meta_scantype", highlight_text_color=textColWhite, highlight_background_color=listboxBg, s=(25, openfile_i), select_mode='LISTBOX_SELECT_MODE_SINGLE', auto_size_text=True)],
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
		[sg.Listbox(openfile_list, default_values=openfile_list[0], key="meta_scandet", highlight_text_color=textColWhite, highlight_background_color=listboxBg, s=(25, openfile_i), select_mode='LISTBOX_SELECT_MODE_SINGLE', auto_size_text=True)],
	]


	# Get current date/time as 'dnow' variable
	dnow = datetime.datetime.now()
	# Enter station of scanned profile / Date and Time for new export
	layout_station = [
		[sg.Text('Station (00+000.00):')],
		[sg.Input(default_text='00+000.00', s=(15,1), focus=True, key="meta_station", border_width=0)],
	]

	layout_date = [
		[sg.Text('Date & Time:')],
		[sg.CalendarButton('Date Picker', format='%Y-%m-%d', title = "Choose Date", key="meta_datepicker", target='meta_date', button_color=('#ffffff',blueBtnColor), border_width=0)],
		[sg.Input(default_text=dnow.strftime("%Y-%m-%d"), key='meta_date', size=(12,1)), sg.Input(default_text=dnow.strftime("%H:%M"), key='meta_time', size=(6,1))],
	]


	layout_meta = [
		[sg.Text("PhotoScan Manager :: Process Setup", font=app_font_title, text_color=titleColor)],
		[sg.HorizontalSeparator()],
		[sg.Text("DataSet / Point file", font=app_font_subtitle, text_color='#6eb7ff')],
		[sg.HorizontalSeparator()],
		[sg.vtop([sg.Col(layout_fileFolders)])],
		[sg.vtop([sg.Col(layout_filePoints)])],
		[sg.Text("Metadata", font=app_font_subtitle, text_color='#6eb7ff')],
		[sg.HorizontalSeparator()],
		[sg.vtop([sg.Col(layout_work), sg.Col(layout_inst)])],
		[sg.vtop([sg.Col(layout_scantype), sg.Col(layout_surveyor)])],
		[sg.vtop([sg.Col(layout_scandet), sg.Col(layout_date)])],
		[sg.vtop([sg.Col(layout_station)])],
		[sg.Button('Exit', key='QUIT', button_color=(textColWhite,redBtnColor), border_width=0), sg.Button('Back', key='BACK', button_color=(textColWhite,orangeBtnColor), border_width=0), sg.Push(), sg.Button("Process Dataset", key='CONT', focus=True, button_color=(textColWhite,greenBtnColor), border_width=0)]
		# [sg.Button('[C]ontinue', key='CONT', button_color=greenBtnColor), sg.Button('[Q]uit', key='QUIT', button_color=redBtnColor)]
	]
	
	window2 = sg.Window('PhotoScan Manager - Process Setup', layout_meta, use_default_focus=False, font=app_font, finalize=True)
	window2.Element('CONT').SetFocus()
	window2.bind('<c>', 'CONT')
	window2.bind('<C>', 'CONT')
	window2.bind('<b>', 'BACK')
	window2.bind('<B>', 'BACK')
	window2.bind('<x>', 'QUIT')
	window2.bind('<X>', 'QUIT')
	window2.bind('<Escape>', 'BACK')

	while True:
		event, values = window2.read()
		
		# End program if user closes window or
		# presses the OK button
		if event == "CONT":
			replace_chars = "'[]"
			window2.hide()
			
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
			clicked = sg.popup_ok_cancel('ENTERED METADATA:\n',
			'Worksite: ' + meta_worksite,
			'Instrument: ' + meta_instrument,
			'Surveyor: ' + meta_surveyor,
			'Scan type: ' + meta_scantype,
			'Scan detail: ' + meta_scandet,
			'Station: ' + meta_station,
			'Date / Time: ' + meta_date + ' / ' + meta_time,
			title='Confirm metadata options', button_color=('#ffffff','#226ab3'))

			if clicked == 'OK':
				process_start = True
				window2.close()
				break
			if clicked == 'Cancel':
				window2.un_hide()
			if clicked == None:
				appStartupMenu(False)


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


# Select dataset to process
def selectDataToProcess():
	global layout_fileFolders, layout_filePoints
	print("Scanning for new data in: " + path_scandata)
	scanFolders(path_scandata)
	print(Fore.CYAN + "\nFound: " + str(new_count) + " folders with new data-sets...\n")

	# Read datasets folder names and locations from file new_dataset_folders.txt
	file_folders = open("settings/new_dataset_folders.txt", "r")
	file_folders_list = file_folders.readlines()
	file_folders_i = 0
	# Count options in opened file
	for x in file_folders_list:
		file_folders_list[file_folders_i] = file_folders_list[file_folders_i].strip().replace(path_scandata, '')
		file_folders_i = file_folders_i + 1
	file_folders.close()
	# Prepare Layout (Folders)
	layout_fileFolders = [
		[sg.Text('Dataset folders:')],
		# Create List object with options
		[sg.OptionMenu(file_folders_list, default_value=file_folders_list[0], key='LIST_FOLDERS', s=(50, file_folders_i), auto_size_text=True)],
	]
	
	# Read datasets point file names and locations from file new_dataset_points.txt
	file_points = open("settings/new_dataset_points.txt", "r")
	file_points_list = file_points.readlines()
	file_points_i = 0
	# Count options in opened file
	for x in file_points_list:
		file_points_list[file_points_i] = file_points_list[file_points_i].strip().replace(path_scandata, '')
		file_points_i = file_points_i + 1
	file_points.close()
	# Prepare Layout (Folders)
	layout_filePoints = [
		[sg.Text('Dataset points:')],
		# Create List object with options
		[sg.OptionMenu(file_points_list, default_value=file_points_list[0], key='LIST_PFILES', s=(50, file_points_i), auto_size_text=True)],
	]
	
	print('')


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


filedb_datasets = open("settings/new_dataset_folders.txt", "w")
filedb_datasets.write("")
filedb_pointfiles = open("settings/new_dataset_points.txt", "w")
filedb_pointfiles.write("")


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
	# print(Fore.BLUE + Style.BRIGHT + " App Version: " + str(app_version) + " - Build: " + str(app_build))
	time.sleep(0.1)
	# Load main app settings
	print(Fore.GREEN + "Loading Settings File: " + app_settings_ini)
	time.sleep(0.2)
	settingsRead()
	print(Fore.GREEN + "Loading Settings... Done.\n")
	
	menu_def = [['&File', ['&Exit::menuexit']],
            ['&Configuration', ['&General Settings', '&FTP Settings'], ],
            ['&Help', ['&Documentation', '---', '&About...'], ]
			]

	layout = [
		[sg.MenuBar(menu_def, pad=0, font=app_font_menubar)],
		[sg.Text("PhotoScan Manager", font=app_font_title, text_color=titleColor)],
		# [sg.Text("Version: " + str(app_version) + " - build: " + str(app_build), font=app_font_ver, text_color='#9b9b9b')],
		[sg.HorizontalSeparator()],
		[sg.Text("START MENU", font=app_font_subtitle)],
		[sg.Text("Continue: Start report manager process...")],
		[sg.Text("Settings: Edit app settings configuration.")],
		[sg.Text("Exit: Close application.")],
		[sg.Button("Continue", focus=True, key='RUN', button_color=(textColWhite,greenBtnColor), border_width=0, pad=10), sg.Button("Settings", key='SET', disabled=False, button_color=(textColWhite,blueBtnColor), border_width=0, pad=10), sg.VerticalSeparator(), sg.Button("Exit", key='QUIT', button_color=(textColWhite,redBtnColor), border_width=0, pad=10)],
		[sg.StatusBar(text=app_statusbar_text, relief='flat', font=app_font_statusbar, background_color='#333333', pad=((0,0),(10,0)), justification='left')],
		]

	# Create the window
	window1 = sg.Window("PhotoScan Manager", layout, element_justification='c', font=app_font, margins=(0,0), icon=app_icon, finalize=True)
	window1.Element('RUN').SetFocus()
	window1.bind('<c>', 'RUN')
	window1.bind('<C>', 'RUN')
	window1.bind('<s>', 'SET')
	window1.bind('<S>', 'SET')
	window1.bind('<x>', 'QUIT')
	window1.bind('<X>', 'QUIT')
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
		if event == "SET":
			process_start = True
			window1.close()
			subprocess.call('edit_settings.pyw', shell=True)
			appStartupMenu(False)
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
