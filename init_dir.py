import glob 
import os
import shutil

path = 'output/*' 
graphDir = "graphs" 
outDir = "cleanOutput"

files = glob.glob(path)  

# Remove existing graphs/ and output/ directory
if os.path.exists(graphDir):
	shutil.rmtree(graphDir)
os.mkdir(graphDir)
if os.path.exists(outDir):
	shutil.rmtree(outDir)
os.mkdir(outDir) 