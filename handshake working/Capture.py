import pyshark
#tshark_path=None # for later use

print(pyshark.tshark.tshark.get_tshark_interfaces())

#cap = pyshark.LiveCapture()
cap = pyshark.FileCapture('test.pcap', only_summaries = True)
for pkt in cap:
        print (pkt)
