#!/usr/bin/env python
 
import socket,sys
from impacket import ImpactDecoder, ImpactPacket
 
src = sys.argv[1]
dst = sys.argv[2]
 
#Create a new IP packet and set its source and destination addresses
 
ip = ImpactPacket.IP()
ip.set_ip_src(src)
ip.set_ip_dst(dst)
 
#Create a new ICMP packet
 
icmp = ImpactPacket.ICMP()
icmp.set_icmp_type(icmp.ICMP_ECHO)
 
#inlude a small payload inside the ICMP packet
#and have the ip packet contain the ICMP packet
icmp.contains(ImpactPacket.Data("a"*100))
ip.contains(icmp)
 
s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
 
#give the ICMP packet some ID
icmp.set_icmp_id(1)
#calculate checksum
icmp.set_icmp_cksum(0)
icmp.auto_checksum = 0
s.sendto(ip.get_packet(), (dst, 0))

#Please note you need to run the program as follows, and also you need to be a root user to do so
# ./ipspoof.py 192.168.2.1 127.0.0.1

