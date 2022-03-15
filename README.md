# Photo Scan Manager :: About

Disclaimer!!! - __App is not operational as it's still in development__

Application for managing scan data, with FTP uploading functionality.

- Language: __Python 3__\
- Python version: __3.10.2__
- Made by: __Boris B__

---

## Python 3 - required modules

```python
import os
import time
import datetime
from configparser import ConfigParser

# Import and initialize colorama module
from colorama import init, Fore, Back, Style
init(autoreset=True)

# Import and initialize PySimpleGUI module
import PySimpleGUI as sg

# Import zip module, and required dependancies
from zipfile import ZipFile
from os.path import basename

```
