from helper import *
import plot_defaults

from matplotlib.ticker import MaxNLocator
from pylab import figure

def plot(file, baseline, out):
	m.rc('figure', figsize=(16, 6))
	fig = figure()
	ax = fig.add_subplot(111)

	lines = open(file).readlines()
	x = [float(line.split(' ')[0]) for line in lines]
	y = [float(line.split(' ')[1]) / baseline for line in lines]

	ax.plot(x,y, linestyle="", marker='x')
	ax.set_ylabel("Throughput")
	ax.set_xlabel("DoS Interburst Period")
	ax.set_ylim(ymin=0)
	ax.set_ylim(ymax=1.0)
	ax.set_xlim(xmin=0)


	if out:
	    plt.savefig(out)
	else:
	    plt.show()

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('--file', '-f',
	                    help="Normalized throughput file to graph",
	                    required=True)

	parser.add_argument('--baseline',
	                    help="Baseline throughput without an attacker",
	                    type=float,
	                    default=1.0)

	parser.add_argument('--out', '-o',
	                    help="Output png file for the plot.",
	                    default=None) # Will show the plot

	args = parser.parse_args()
	plot(args.file, args.baseline, args.out)
