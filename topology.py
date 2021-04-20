#!/usr/bin/python

from mininet.cli import CLI
from mininet.topo import Topo
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.net import Mininet
from mininet.log import lg, info
from mininet.util import dumpNodeConnections

from subprocess import Popen, PIPE
from time import sleep, time
from multiprocessing import Process
from argparse import ArgumentParser

from helper import avg, stdev

import sys
import os
import math

parser = ArgumentParser(description="Bufferbloat tests")
parser.add_argument('--bw-server', '-bs',
                    type=float,
                    help="Bandwidth of server link (Mb/s)",
                    default=500)

parser.add_argument('--bw-attacker', '-ba',
                    type=float,
                    help="Bandwidth of attacker (network) link (Mb/s)",
                    default=500)

parser.add_argument('--bw-innocent', '-bi',
                    type=float,
                    help="Bandwidth of innocent (network) link (Mb/s)",
                    default=500)

parser.add_argument('--bw-bottleneck', '-bb',
                    type=float,
                    help="Bandwidth of bottleneck link (Mb/s)",
                    default=1.5)

parser.add_argument('--delay',
                    type=float,
                    help="Link propagation delay (ms)",
                    default=2)

parser.add_argument('--dir', '-d',
                    help="Directory to store outputs",
                    required=True)

parser.add_argument('--time', '-t',
                    help="Duration (sec) to run the experiment",
                    type=float,
                    default=10)

parser.add_argument('--maxq',
                    type=int,
                    help="Max buffer size of network interface in packets",
                    default=100)

parser.add_argument('--burst_period',
                    type=float,
                    help="Interburst period",
                    default=0.5)

parser.add_argument('--burst_duration',
                    type=float,
                    help="Interburst duration",
                    default=0.15)

parser.add_argument('--min_rto',
                    type=float,
                    help="Min RTO (ms)",
                    default=1000)

parser.add_argument('--disable_attacker',
                    type=bool,
                    help="Whether the attacker is disabled",
                    default=False)		

# Linux uses CUBIC-TCP by default that doesn't have the usual sawtooth
# behaviour.  For those who are curious, invoke this script with
# --cong cubic and see what happens...
# sysctl -a | grep cong should list some interesting parameters.
parser.add_argument('--cong',
                    help="Congestion control algorithm to use",
                    default="reno")

# Expt parameters
args = parser.parse_args()

class BBTopo(Topo):

    def build(self, n=2):
        switch0 = self.addSwitch('s0')
        switch1 = self.addSwitch('s1')

        attacker_client = self.addHost('attacker')
        self.addLink(attacker_client, switch0, bw=args.bw_attacker, delay=args.delay)

        innocent_client = self.addHost('innocent')
        self.addLink(innocent_client, switch0, bw=args.bw_innocent, delay=args.delay)

        self.addLink(switch0, switch1, bw=args.bw_bottleneck, max_queue_size=args.maxq, delay=args.delay)

        server = self.addHost('server')
        self.addLink(server, switch1, bw=args.bw_server, delay=args.delay)

        return

def start_iperf(net):
    print "Starting iperf server..."
    # Change the min rto for client and server
    # TODO: do we need to set the minRTO for the server?
    
    rto_min = str(1000)
    server = net.get('server')
    server.popen("iperf -s -w 16m >> %s/iperf_server.txt" % args.dir, shell=True)

    client = net.get('innocent')
    cmd = "ip route change 10.0.0.0/8 dev innocent-eth0  proto kernel  scope link  src %s rto_min 1000" % client.IP()
    client.popen(cmd, shell=True).communicate()
    client.popen("iperf -c %s -t %f -i %f -l %f > %s/iperf_out.txt" % (server.IP(), args.time, 2, 32768, args.dir), shell=True)

def start_attacker(net):
    client = net.get('attacker')
    server = net.get('server')
    print "Burst period: %s" % args.burst_period
    client.popen("python shrew.py %s %f %f %f" % (server.IP(), args.burst_period, args.burst_duration, args.time))

def topology():
    if not os.path.exists(args.dir):
        os.makedirs(args.dir)
    os.system("sysctl -w net.ipv4.tcp_congestion_control=%s" % args.cong)

    # TODO: do we need to disable frto?
    os.system("sysctl net.ipv4.tcp_frto=0")

    topo = BBTopo()
    net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink)
    net.start()
    # This dumps the topology and how nodes are interconnected through
    # links.
    dumpNodeConnections(net.hosts)

    start_iperf(net)
    if not args.disable_attacker:
        print "\033[1;41mStarting attacker!\033[0m"
        start_attacker(net)
    # Sleep for + 5 to give iperf chance to finish up
    sleep(args.time + 5)    
    net.stop()
    # Ensure that all processes you create within Mininet are killed.
    # Sometimes they require manual killing.
    Popen("pgrep -f ping | xargs kill -9", shell=True).wait()
    Popen("pgrep -f iperf | xargs kill -9", shell=True).wait()
    Popen("pgrep -f webserver.py | xargs kill -9", shell=True).wait()

if __name__ == "__main__":
    topology()

