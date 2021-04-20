# Average data points and get rid of error messages
# and plot
# Makes 2 plots in the graphs/ directory
# One plot uses the average throughput, and the other uses the min throughpu

import glob   
import os
import plot_normalized_throughput
import re
import shutil
from helper import *

def clean_data(args):
	path = 'output/*' 
	graphDir = "graphs" 
	outDir = "cleanOutput"
	files = glob.glob(path)  

	for file in files:    
	    dict = {} 
	    f = open(file, 'r')  
	    lines = f.readlines()   
	    for line in lines:
	    	splitLine = line.split()
	    	key = splitLine[0]
	    	val = splitLine[1]
	    	if "error" in val:
	    		continue

	    	if dict.has_key(key):
	    		dict[key].append(val)
	    	else:
	    		dict[key] = [val]
	    f.close() 

	    queueSize = re.search('[0-9]+', file).group(0)
	    outfileName = outDir + "/" + args.cong + "_" + queueSize + ".txt"
	    minOutfileName = outDir + "/" + args.cong + "_min" + queueSize + ".txt" 
	    # Right now, plots min and avg on 2 separate graphs
	    # To plot on the same graph, set minOutfileName to outfileName
	    # and then remove the rest of the code pertaining to minOutfile
	    outfile = open(outfileName, 'w')
	    minOutfile = open(minOutfileName, 'w')
	    baseline_avg = 1.0
	    baseline_min = 1.0
	    for key in dict:
	    	# Average the values and output to the file
	    	val = dict[key]
	    	if key != '0.0':
	    		outfile.write(key)
	    		outfile.write(" ")
	    		minOutfile.write(key)
	    		minOutfile.write(" ")

	    	val_floats = [float(x) for x in val]
	    	minVal = min(val_floats)

	    	avg = sum(val_floats)/len(val_floats)
	    	if key != '0.0':
	    		outfile.write(str(avg))
	    		outfile.write("\n")
	    		minOutfile.write(str(minVal))
	    		minOutfile.write("\n")
	    	else:
	    		baseline_avg = avg
	    		baseline_min = minVal
	    	
	    outfile.close()
	    minOutfile.close()

	    # Find the queue size
	    # TODO: remove code below (about queueing) later for final submission?
	    # That is, we would have decided on a queue size then
	    # so we wouldn't need to create separate plots by queue size
	    plot_normalized_throughput.plot(outfileName, baseline_avg, graphDir + "/" + args.cong + "_" + queueSize)
	    plot_normalized_throughput.plot(minOutfileName, baseline_min, graphDir + "/" + args.cong + "_min" + queueSize)

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('--cong',
	                    help="TCP variant",
	                    default="reno") # Will show the plot

	args = parser.parse_args()
	clean_data(args)
