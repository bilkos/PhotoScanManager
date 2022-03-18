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
# General modules
import os
import time
import datetime
import locale
import subprocess

# Additional modules
from configparser import ConfigParser
from colorama import init, Fore, Back, Style
import PySimpleGUI as sg

# Zip module, and required dependancies
from zipfile import ZipFile
from os.path import basename

# Initialize colorama module
init(autoreset=True)


```
