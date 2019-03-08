import pyshark

cap = pyshark.LiveCapture()
for pkt in cap:
        print (pkt)
