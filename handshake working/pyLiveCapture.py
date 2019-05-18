import pyshark

capture = pyshark.LiveCapture(interface='Wi-Fi')
# capture.sniff(timeout=50)
print(capture)

for pkt in capture:
    print (pkt)
    print("----------------------------")
