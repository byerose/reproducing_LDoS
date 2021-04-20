import re
from helper import *

parser = argparse.ArgumentParser()
parser.add_argument('--file', '-f',
					help="throughput file to calculate",
					required=True)

args = parser.parse_args()

def calculate_throughput(fname):
	lines = open(fname).readlines()
	if len(lines) == 0:
		print "error: Empty file, check what's going on"
		return
	last_line = lines[len(lines) - 1]
	if ' 0.0' not in last_line:
		print "error: Could not find line in throughput file with aggregate throughput"
		return
	
	m = re.search('(?<=Bytes)[0-9\.\ ]+', last_line)

	if m is None:
		print 'error: Last line does not match the regex'
		return
	else:
		if 'Mbits' in last_line:
			print float(m.group(0))
		elif 'Kbits' in last_line:
			print float(m.group(0)) / 1024
		elif 'bits' in last_line:
			print float(m.group(0)) / 1024 / 1024
		else:
			print "error: could not parse throughput"

if __name__ == "__main__":
	calculate_throughput(args.file)
