# Photogrammetry Scan Manager
# Made by: Boris Bilc

# IMPORT MODULES & GENERAL VARIABLES
from email.mime import image
import modlib.zip_archive as zip_archive
import base64
import locale
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
sg.theme('DarkGrey14')		# GUI Color Theme (SystemDefaultForReal, Python, DarkGrey14)

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
app_font = 'Bahnschrift 11'
font_btn_browse = 'Bahnschrift 9'
font_btn_browse2 = 'Bahnschrift 10'
sg.set_options(font=app_font)

# Image for browse folders
img_browseFolders = "settings/SearchesFolder.png"
imgb64_browse = b''

# Convert images
with open(img_browseFolders, "rb") as image2string:
    imgb64_browse = base64.b64encode(image2string.read())
# print(imgb64_browse)


# Read active settings 
def settingsRead():
	# Global variables for settings
	global path_scandata, path_packages, path_backup
	global metadata_export, metadata_external, metadata_fixed
	global fixed_worksite, fixed_scan_type, fixed_scan_detail, fixed_instrument, fixed_surveyor
	global logfile, processed_db
	global ftp_upload, auto_upload
	global backup, backup_cleanup
	global config
	# Prepare config parser
	config = ConfigParser(allow_no_value=True, comment_prefixes=('#',';'))
	config.optionxform = str

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



def updateSettingsFile():
	# update existing value
	#config.set('FOLDERS', '# Valid path templates are:\n# - Relative to app root (recommended) = ScanData/\n# - Absolute path to folder = X:/my-data/ScanData\n# Folder separator can be either "/" or "\".\n# App will automatically change it to the correct separator before processing.\n', None)
	#config.update('FOLDERS', '# Folder where new unprocessed data is located')
	config.set('FOLDERS', 'path_scandata', str(path_scandata))
	config.set('FOLDERS', 'path_packages', str(path_packages))
	config.set('FOLDERS', 'path_backup', str(path_backup))
	config.set('METADATA', 'metadata_export', str(metadata_export))
	config.set('METADATA', 'metadata_external', str(metadata_external))
	config.set('METADATA', 'metadata_fixed', str(metadata_fixed))
	config.set('LOGS', 'logfile', str(logfile))
	config.set('LOGS', 'processed_db', str(processed_db))
	config.set('UPLOAD', 'ftp_upload', str(ftp_upload))
	config.set('UPLOAD', 'auto_upload', str(auto_upload))
	config.set('BACKUP', 'backup', str(backup))
	config.set('BACKUP', 'backup_cleanup', str(backup_cleanup))
	config.set('METADATA', 'fixed_worksite', str(fixed_worksite))
	config.set('METADATA', 'fixed_scan_type', str(fixed_scan_type))
	config.set('METADATA', 'fixed_scan_detail', str(fixed_scan_detail))
	config.set('METADATA', 'fixed_instrument', str(fixed_instrument))
	config.set('METADATA', 'fixed_surveyor', str(fixed_surveyor))
	

	# add a new section and some values

	#config.add_section('section_b')
	#config.set('section_b', 'meal_val', 'spam')
	#config.set('section_b', 'not_found_val', '404')

	# save to a file
	with open(app_settings_ini, 'w') as configfile:
		config.write(configfile)


def editSettings():
	# Global variables for settings
	global path_scandata, path_packages, path_backup
	global metadata_export, metadata_external, metadata_fixed
	global fixed_worksite, fixed_scan_type, fixed_scan_detail, fixed_instrument, fixed_surveyor
	global logfile, processed_db
	global ftp_upload, auto_upload
	global backup, backup_cleanup
	global config
	
	btn1 = sg.FolderBrowse(target='PATH_DATA', key='BF1', font=font_btn_browse, button_color=blueBtnColor, visible=False)
	btn2 = sg.FolderBrowse(target='PATH_PROC', key='BF2', font=font_btn_browse, button_color=blueBtnColor, visible=False)
	btn3 = sg.FolderBrowse(target='PATH_BACKUP', key='BF3', font=font_btn_browse, button_color=blueBtnColor, visible=False)

	layout_data = [
		#[sg.Text("Working folders", font=app_font_subtitle, text_color='#ffdc73')],
		#[sg.HorizontalSeparator()],
		[sg.Text('Scan Data:'), sg.Push(),
		sg.Input(default_text=str(path_scandata), key='PATH_DATA', s=(40,1), background_color='#3a3a3a', border_width=0), 
		sg.Image(source=img_browseFolders, subsample=8, enable_events=True, key='BRWSF1', tooltip='Browse folders...'), 
		btn1],
		[sg.Text("^ Location where new data is stored", font=font_btn_browse, pad=(130,0), text_color='#ffdc73')],
		[sg.HorizontalSeparator(color='#ffffff')],
		[sg.Text('Processed Data:'), sg.Push(),
		sg.Input(default_text=str(path_packages), key='PATH_PROC', s=(40,1), background_color='#3a3a3a', border_width=0), 
		sg.Image(source=img_browseFolders, subsample=8, enable_events=True, key='BRWSF2', tooltip='Browse folders...'), 
		btn2],
		[sg.Text("^ Location where processed data is stored", font=font_btn_browse, pad=(130,0), text_color='#ffdc73')],
		[sg.HorizontalSeparator(color='#ffffff')],
		[sg.Text('Backups:'), sg.Push(),
		sg.Input(default_text=str(path_backup), key='PATH_BACKUP', s=(40,1), background_color='#3a3a3a', border_width=0), 
		sg.Image(source=img_browseFolders, subsample=8, enable_events=True, key='BRWSF3', tooltip='Browse folders...'), 
		btn3],
		[sg.Text("^ Location where backups are stored", font=font_btn_browse, pad=(130,0), text_color='#ffdc73')],
		#[sg.HorizontalSeparator(color='#ffffff')],
		]


	layout_meta = [
		[sg.Text("Metadata", font=app_font_subtitle, text_color='#6eb7ff')],
		[sg.HorizontalSeparator()],
		[sg.Checkbox('Metadata export', default=metadata_export, checkbox_color='#2d5ba6', key='META_EXP', tooltip='Export metadata to point file header.')],
		[sg.Checkbox('Write to external file', default=metadata_external, checkbox_color='#2d5ba6', key='META_EXT', tooltip='Write metadata to a separate file. Will not write to header.')],
		]
	

	layout_metafix = [
		[sg.Text("Metadata: Fixed Values", font=app_font_subtitle, text_color='#6eb7ff')],
		[sg.HorizontalSeparator()],
		[sg.Checkbox('Use fixed values', default=metadata_fixed, checkbox_color='#2d5ba6', key='META_FIX', tooltip='Enable to use fixed values, and disable metadata options before processing.')],
		[sg.Text('Worksite:'), sg.Push(), sg.Input(default_text=fixed_worksite, background_color='#3a3a3a', border_width=0, s=(25,1), key='FIX_1')],
		[sg.Text('Scan type:'), sg.Push(), sg.Input(default_text=fixed_scan_type, background_color='#3a3a3a', border_width=0, s=(25,1), key='FIX_2')],
		[sg.Text('Scan detail:'), sg.Push(), sg.Input(default_text=fixed_scan_detail, background_color='#3a3a3a', border_width=0, s=(25,1), key='FIX_3')],
		[sg.Text('Instrument:'), sg.Push(), sg.Input(default_text=fixed_instrument, background_color='#3a3a3a', border_width=0, s=(25,1), key='FIX_4')],
		[sg.Text('Surveyor:'), sg.Push(), sg.Input(default_text=fixed_surveyor, background_color='#3a3a3a', border_width=0, s=(25,1), key='FIX_5')],
	]


	layout_logs = [
		[sg.Text("Logging", font=app_font_subtitle, text_color='#6eb7ff')],
		[sg.HorizontalSeparator()],
		[sg.Checkbox('Log events', default=logfile, checkbox_color='#2d5ba6', key='LOG_FILE')],
		[sg.Checkbox('Log processed files', default=processed_db, checkbox_color='#2d5ba6', key='LOG_PROC')],
	]


	layout_ftp = [
		[sg.Text("FTP Uploading", font=app_font_subtitle, text_color='#6eb7ff')],
		[sg.HorizontalSeparator()],
		[sg.Checkbox('FTP Upload', default=ftp_upload, checkbox_color='#2d5ba6', key='FTP_UPL')],
		[sg.Checkbox('Auto-Upload', default=auto_upload, checkbox_color='#2d5ba6', key='FTP_AUTO')],
	]


	layout_backup = [
		[sg.Text("Backups", font=app_font_subtitle, text_color='#6eb7ff')],
		[sg.HorizontalSeparator()],
		[sg.Checkbox('Backup data', default=backup, checkbox_color='#2d5ba6', key='BACKUP')],
		[sg.Checkbox('Cleanup processed', default=backup_cleanup, checkbox_color='#2d5ba6', key='BCKP_CLN')],
	]


	layout_main = [
		[sg.Text("PHOTO-SCAN Manager :: Settings", font=app_font_title, text_color=titleColor)],
		[sg.HorizontalSeparator()],
		[sg.Push(), sg.Frame('Working folders', layout_data, font=app_font_subtitle, title_color='#6eb7ff'), sg.Push()],
		[sg.vtop([sg.Push(), sg.Col(layout_ftp), sg.Col(layout_logs), sg.Col(layout_backup), sg.Push()])],
		[sg.vtop([sg.Push(), sg.Col(layout_meta), sg.Col(layout_metafix), sg.Push()])],
		[sg.Button("Save & Close", key='SAVE', focus=True, button_color=(textColWhite,greenBtnColor), border_width=0), sg.Button('Close', key='QUIT', button_color=(textColWhite,orangeBtnColor), border_width=0)]
		# [sg.Button('[C]ontinue', key='CONT', button_color=greenBtnColor), sg.Button('[Q]uit', key='QUIT', button_color=redBtnColor)]
	]
	
	windowSettings = sg.Window('PhotoScan Manager - Settings', layout_main, use_default_focus=False, font=app_font, no_titlebar=False, icon=app_icon, finalize=True)
	windowSettings.Element('SAVE').SetFocus()
	windowSettings.bind('<s>', 'SAVE')
	windowSettings.bind('<S>', 'SAVE')
	windowSettings.bind('<c>', 'QUIT')
	windowSettings.bind('<C>', 'QUIT')
	windowSettings.bind('<Escape>', 'QUIT')

	# Create an event loop
	while True:
		event, values = windowSettings.read()
		
		# End program if user closes window or
		# presses the OK button
		if event == "BRWSF1":
			btn1.click()
			
		if event == "BRWSF2":
			btn2.click()
			
		if event == "BRWSF3":
			btn3.click()
			
		if event == "SAVE":
			path_scandata = values['PATH_DATA']
			path_packages = values['PATH_PROC']
			path_backup = values['PATH_BACKUP']
			metadata_export = values['META_EXP']
			metadata_external = values['META_EXT']
			metadata_fixed = values['META_FIX']
			logfile = values['LOG_FILE']
			processed_db = values['LOG_PROC']
			ftp_upload = values['FTP_UPL']
			auto_upload = values['FTP_AUTO']
			backup = values['BACKUP']
			backup_cleanup = values['BCKP_CLN']
			# fixed_worksite = config.get('METADATA', 'fixed_worksite')
			# fixed_scan_type = config.get('METADATA', 'fixed_scan_type')
			# fixed_scan_detail = config.get('METADATA', 'fixed_scan_detail')
			# fixed_instrument = config.get('METADATA', 'fixed_instrument')
			# fixed_surveyor = config.get('METADATA', 'fixed_surveyor')

			updateSettingsFile()
			windowSettings.close()
			quit()
			
		if event == "QUIT" or event == sg.WIN_CLOSED:
			quit()
			
# Start settings editor
settingsRead()
editSettings()
