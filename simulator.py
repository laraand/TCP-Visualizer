#Anthony Zerka
#Capstone Project - Part 1

# import pyshark
import socket
import textwrap
import ctypes

# cap = pyshark.LiveCapture(output_file = "pyshark.pcap")
# cap.sniff(timeout=20)




#https://www.youtube.com/watch?v=dM9grWOdTBI



ctypes.windll.shell32.IsUserAnAdmin()

#Unpack ethernet frame (AA:BB:CC:DD:EE:FF)
def ethernet_frame(data):
	dest_mac, src_mac, proto = struct.unpack('! 6s 6s H', data[:14])
	return get_mac_addr(dest_mac), get_mac_addr(src_mac), socket.htons(proto), data[14:]

#Return properly formatted MAC address
def get_mac_addr(bytes_addr):
	bytes_addr = map('{:02x}'.format, bytes_addr)
	mac_addr = ':'.join(bytes_addr).upper()
	return mac_addr


def main():
	connection = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)

	while True:
		raw_data, addr = connection.recvfrom(65536)
		dest_mac, src_mac, eth_proto, data = ethernet_frame(raw_data)
		print('\nEthernet Frame : ')
		print('Destination : {}, Source : {}, Protocol : {}'.format(dest_mac,src_mac,eth_proto))



#start program at main()
if __name__ == "__main__":
    main()