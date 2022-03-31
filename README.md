# .: Photo Scan Manager :.

Application for managing scan data, with FTP uploading functionality.

## About

Disclaimer!!! - __App is not operational as it's still in development__

- Language: __Python 3__
- Python version: __3.10.2__
- GUI: __PySimpleGUI__
- Made by: __Boris B__

---

## Python 3 - required modules

```python
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
```
