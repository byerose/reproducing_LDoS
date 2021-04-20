#!/bin/bash

# Goes through every directory in the current directory, 
# collects the throughput from the iperf_out.txt file,
# outputs them to files organized by queue size. 
# Directories should be of format:
# data-q[size]-p[period]-i[iteration]
rm -r "output"
mkdir "output"
for d in */ ; do
	{ # try
		if [ ! -f "$d/iperf_out.txt" ]; then
			:
#    		echo "Ignoring dir $d"
		else 
			q=$(sed -E 's/data-q([0-9]+).*/\1/g' <<< "$d")
			p=$(sed -E 's/data-q([0-9]+)-p([0-9]*\.[0-9]+).*/\2/g' <<< "$d")
	    	throughput=$(python calculate_throughput.py --file "$d/iperf_out.txt")
	    	echo "$p $throughput" >> "output/outq$q.txt"
	    fi
	}  || { # catch
    	echo "Error in directory $d"
	}
done
