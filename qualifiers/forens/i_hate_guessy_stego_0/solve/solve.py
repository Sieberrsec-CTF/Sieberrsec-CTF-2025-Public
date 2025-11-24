from scapy.all import rdpcap, DNS

pcap = "/absolute/path/to/i_hate_guessy_stego_0.pcapng" # REPLACE WITH ACTUAL PATH

pkts = rdpcap(pcap)

ids = [] # prevent duplicates

for pkt in pkts:
    if pkt.haslayer(DNS) and pkt.getlayer(DNS).qr == 0: # DNS queries have their first flag bit set to 0
        dns = pkt.getlayer(DNS)
        qname = dns.qd.qname.decode().rstrip('.')
        if "dnslog.cn" in qname and dns.id not in ids:
            ids.append(dns.id)
            lsubdomain = qname.split('.')[0]
            print(chr(int(lsubdomain, 16)), end="")