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
app_version = '0.1.65'
#  </#FV>

# App icon
app_icon = 'appicon.ico'

# Main App Configuration & Info
app_settings_ini = 'settings/app_settings.ini'
app_settings_ini_ftp = 'settings/app_settings-ftp.ini'

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
def settingsReadFtp():
	# Global variables for settings
	global ftp_host_name, ftp_host, ftp_port, ftp_username, ftp_password, ftp_root_path, ftp_use_ssl
	global config
	# Prepare config parser
	config = ConfigParser(allow_no_value=True, comment_prefixes=('#',';'))
	config.optionxform = str

	# Read settings from 'app_settings-ftp.ini' and parse them as variables 
	config.read(app_settings_ini_ftp)

	ftp_host_name = config.get('FTP', 'ftp_host_name')
	ftp_host = config.get('FTP', 'ftp_host')
	ftp_port = config.get('FTP', 'ftp_port')
	ftp_username = config.get('FTP', 'ftp_username')
	ftp_password = config.get('FTP', 'ftp_password')
	ftp_root_path = config.get('FTP', 'ftp_root_path')
	ftp_use_ssl = config.getboolean('FTP', 'ftp_use_ssl')


def updateSettingsFileFtp():
	# update existing value
	config.set('FTP', 'ftp_host_name', str(ftp_host_name))
	config.set('FTP', 'ftp_host', str(ftp_host))
	config.set('FTP', 'ftp_port', str(ftp_port))
	config.set('FTP', 'ftp_username', str(ftp_username))
	config.set('FTP', 'ftp_password', str(ftp_password))
	config.set('FTP', 'ftp_root_path', str(ftp_root_path))
	config.set('FTP', 'ftp_use_ssl', str(ftp_use_ssl))
		
	# save to a file
	with open(app_settings_ini_ftp, 'w') as configfile:
		config.write(configfile)


def editSettingsFtp():
	# Global variables for settings
	global ftp_host_name, ftp_host, ftp_port, ftp_username, ftp_password, ftp_root_path, ftp_use_ssl
	global config
	
	layout_ftp = [
		[sg.Text("FTP Settings", font=app_font_subtitle, text_color='#6eb7ff')],
		[sg.HorizontalSeparator()],
		[sg.Text('Host Name:\t'), sg.Input(default_text=ftp_host_name, background_color='#5a5a5a', border_width=0, s=(35,1), key='FTP_HNAME')],
		[sg.Text('Host:\t\t'), sg.Input(default_text=ftp_host, background_color='#5a5a5a', border_width=0, s=(16,1), key='FTP_HOST')],
		[sg.Text('Port:\t\t'), sg.Input(default_text=ftp_port, background_color='#5a5a5a', border_width=0, s=(8,1), key='FTP_PORT')],
		[sg.Text('Username:\t'), sg.Input(default_text=ftp_username, background_color='#5a5a5a', border_width=0, s=(25,1), key='FTP_US')],
		[sg.Text('Password:\t'), sg.Input(default_text=ftp_password, background_color='#5a5a5a', border_width=0, s=(25,1), key='FTP_PS')],
		[sg.Text('Root path:\t'), sg.Input(default_text=ftp_root_path, background_color='#5a5a5a', border_width=0, s=(35,1), key='FTP_ROOT')],
		[sg.Checkbox('use SSL/TLS', default=ftp_use_ssl, checkbox_color='#2d5ba6', key='FTP_SSL', tooltip='Enable to use SSL/TLS.')],
	]


	layout_main = [
		[sg.Text("PHOTO-SCAN Manager :: FTP Settings", font=app_font_title, text_color=titleColor)],
		[sg.HorizontalSeparator()],
		[sg.vtop([sg.Push(), sg.Col(layout_ftp), sg.Push()])],
		[sg.Button("Save & Close", key='SAVE', focus=True, button_color=(textColWhite,greenBtnColor), border_width=0), sg.Button('Close', key='QUIT', button_color=(textColWhite,orangeBtnColor), border_width=0)]
		# [sg.Button('[C]ontinue', key='CONT', button_color=greenBtnColor), sg.Button('[Q]uit', key='QUIT', button_color=redBtnColor)]
	]
	
	windowSettingsFtp = sg.Window('PhotoScan Manager - FTP Settings', layout_main, use_default_focus=False, font=app_font, no_titlebar=False, icon=app_icon, finalize=True)
	windowSettingsFtp.Element('SAVE').SetFocus()
	windowSettingsFtp.bind('<s>', 'SAVE')
	windowSettingsFtp.bind('<S>', 'SAVE')
	windowSettingsFtp.bind('<c>', 'QUIT')
	windowSettingsFtp.bind('<C>', 'QUIT')
	windowSettingsFtp.bind('<Escape>', 'QUIT')

	# Create an event loop
	while True:
		event, values = windowSettingsFtp.read()
		
		# End program if user closes window or
		# presses the OK button
		if event == "SAVE":
			ftp_host_name = values['FTP_HNAME']
			ftp_host = values['FTP_HOST']
			ftp_port = values['FTP_PORT']
			ftp_username = values['FTP_US']
			ftp_password = values['FTP_PS']
			ftp_root_path = values['FTP_ROOT']
			ftp_use_ssl = values['FTP_SSL']
			
			updateSettingsFileFtp()
			windowSettingsFtp.close()
			quit()
			
		if event == "QUIT" or event == sg.WIN_CLOSED:
			quit()
			
# Start settings editor
settingsReadFtp()
editSettingsFtp()
