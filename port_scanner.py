import os
import sys
import logging
import socket
from scapy.all import *

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
src_port = RandShort()

# Take arguments
try: 
    TARGET_HOST = sys.argv[1]
    SCAN_MODE = sys.argv[2]
except IndexError:
    print("Usage: python port_scanner.py [TARGET IPv4 ADDR] [SCAN MODE]")
    print("Scan mode options: CONNECT, STEALTH, FIN (case-insensitive)")
    sys.exit()

# Check if host is resolvable:
try:
    socket.gethostbyname(TARGET_HOST)
except socket.gaierror:
    print("Cannot resolve hostname provided.")

def connect_scan(host, dst_port):
    tcp_scan_resp = sr1( IP(dst = host) / TCP(sport=src_port, dport=dst_port, flags="S"), verbose=0, timeout=1 )
    if(tcp_scan_resp != None):
        pktflags = (tcp_scan_resp.getlayer(TCP).flags)
        if(pktflags == "SA"): # SYNACK
            rst = sr( IP(dst = host) / TCP(sport=src_port, dport=dst_port, flags="AR"), verbose=0, timeout=1 )
            return "OPEN"

        if(pktflags == "RA"): # RSTACK
            return "CLOSED"
    else:
        return "CLOSED"

def stealth_scan(host, dst_port):
    tcp_scan_resp = sr1( IP(dst = host) / TCP(sport=src_port, dport=dst_port, flags="S"), verbose=0, timeout=1 )
    if(tcp_scan_resp != None): 
        pktflags = (tcp_scan_resp.getlayer(TCP).flags)
        if(pktflags == "SA"): # SYNACK
            rst = sr( IP(dst = host) / TCP(sport=src_port, dport=dst_port, flags="R"), verbose=0, timeout=1 )
            return "OPEN"

        if(pktflags == "RA"): # RSTACK
            return "CLOSED"
    else:
        return "CLOSED"

def fin_scan(host, dst_port):
    tcp_scan_resp = sr1( IP(dst = host) / TCP(sport=src_port, dport=dst_port, flags="F"), verbose=0, timeout=1 )
    if(tcp_scan_resp != None):
        pktflags = (tcp_scan_resp.getlayer(TCP).flags)
        if(pktflags == "RA"): # RSTACK
            return "CLOSED"
    else:
        return "OPEN"

START_TIME = datetime.now()
print("\n* Start port scan at " + str(START_TIME) )
print("* Notable open ports on " + TARGET_HOST + "...")
print("-"*55)
print("| {:^15} | {:^15} | {:^15} |".format("PORT", "STATE","SERVICE"))
print("-"*55)

closed = 0 
for x in range(1, 65535):
    #print("| {:^15} | {:^15} | {:^15} |".format(str(x), fin_scan(TARGET_HOST, x), socket.getservbyport(x)))
    try:
        if(SCAN_MODE.upper() == "CONNECT"): 
            if(connect_scan(TARGET_HOST, x) == "OPEN"): print("| {:^15} | {:^15} | {:^15} |".format(str(x), connect_scan(TARGET_HOST, x), socket.getservbyport(x)))
            else: closed+=1

        elif(SCAN_MODE.upper() == "STEALTH"): 
            if(stealth_scan(TARGET_HOST, x) == "OPEN"): print("| {:^15} | {:^15} | {:^15} |".format(str(x), stealth_scan(TARGET_HOST, x), socket.getservbyport(x)))
            else: closed+=1
        
        elif(SCAN_MODE.upper() == "FIN"): 
            if(fin_scan(TARGET_HOST, x) == "OPEN"): print("| {:^15} | {:^15} | {:^15} |".format(str(x), fin_scan(TARGET_HOST, x), socket.getservbyport(x)))
            else: closed+=1

        else:
            print("| {:^51} |".format("INCORRECT CONNECTION METHOD."))
            print("-"*55)
            sys.exit()
    except OSError:
        pass

print("-"*55)
print("* Elapsed time: " + str(datetime.now() - START_TIME))
print("* Not shown: " + str(closed) + " closed ports. The rest do not have a service associated.")