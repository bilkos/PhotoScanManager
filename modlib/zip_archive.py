# Photogrammetry Point Report Generator
# Module: ZIP archiving

from zipfile import ZipFile
import os
from os.path import basename

# Zip the files from given directory that matches the filter
def zipFilesInDir(dirName, zipFileName):
	# create a ZipFile object
	with ZipFile(zipFileName, 'w') as zipObj:
		# Iterate over all the files in directory
		for folderName, subfolders, filenames in os.walk(dirName):
			for filename in filenames:
				# create complete filepath of file in directory
				filePath = os.path.join(folderName, filename)
				# Add file to zip
				zipObj.write(filePath, basename(filePath))