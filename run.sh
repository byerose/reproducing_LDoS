#!/bin/bash

# Note: Mininet must be run as root.  So invoke this shell script
# using sudo.

time=30
iperf_port=5001

if ls data* >/dev/null 2>&1;then
	rm -r data*
fi

python init_dir.py
# one of  [vegas westwood reno bic cubic bbr] 
tcp=$1
period=$2
for cong in $tcp; do
	for min_rto in 1000; do
		for qsize in 4; do
			for i in 1; do

				echo -e "\e[1;42mRunning without attacker \e[0m \033[32m>_\033[0m"
				sudo mn --clean	#clean and exit mininet		
				dir=data-q$qsize-p0.0-i$i
				python topology.py --dir $dir --t $time --maxq $qsize --min_rto $min_rto --disable_attacker true --cong $cong
				echo -e "\e[1;46mDone! \e[0m \033[32m<_\033[0m"
				
				# Always have a "." in the interburst_period numbers. E.g., use "4.0" not "4"
				for interburst_period in $period; do			
					echo -e "\e[1;42mRunning with attacker \e[0m \033[32m>_\033[0m"
				    sudo mn --clean
				    dir=data-q$qsize-p$interburst_period-i$i
				    python topology.py --dir $dir --t $time --maxq $qsize --burst_period $interburst_period --min_rto $min_rto --cong $cong
					echo -e "\e[1;46mDone! \e[0m \033[32m<_\033[0m"
				done
			done
		done
	done

	./findThroughputs.sh
	python cleanData.py --cong $cong

	echo -e "\e[1;42mShow result \e[0m"
	echo "Period Throughput"
	cat cleanOutput/${cong}_4.txt
	echo -e "\e[1;46mEND \e[0m"

done

