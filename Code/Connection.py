import socket
import struct

def process_market_data(data):
    # Unpack the market data fields from the received data
    packet_length, symbol, sequence_number, timestamp, ltp, ltq, volume, \
    bid_price, bid_qty, ask_price, ask_qty, open_interest, prev_close_price, prev_open_interest = \
        struct.unpack('!i30sqqqqqqqqqqqq', data)

    # Convert symbol from bytes to string
    symbol = symbol.decode('utf-8').rstrip('\x00')

    # Process and display the market data as per your requirements
    print('Packet Length:', packet_length)
    print('Symbol:', symbol)
    print('Sequence Number:', sequence_number)
    print('Timestamp:', timestamp)
    print('LTP:', ltp / 100)  # Convert from paise to rupees
    print('LTQ:', ltq)
    print('Volume:', volume)
    print('Bid Price:', bid_price / 100)  # Convert from paise to rupees
    print('Bid Quantity:', bid_qty)
    print('Ask Price:', ask_price / 100)  # Convert from paise to rupees
    print('Ask Quantity:', ask_qty)
    print('Open Interest:', open_interest)
    print('Previous Close Price:', prev_close_price / 100)  # Convert from paise to rupees
    print('Previous Open Interest:', prev_open_interest)
    print('')

HOST = '127.0.0.1'  # Update with the server's IP address or hostname
PORT = 12345  # Update with the server's listening port
PACKET_SIZE = 130 

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to the server
    sock.connect((HOST, PORT))
    print("Connected to the server.")

    # Send a request to indicate readiness
    sock.sendall(b'Ready')

    # Receive and process market data
    while True:
        data = b''  # Initialize an empty buffer
        while len(data) < PACKET_SIZE:
            packet = sock.recv(PACKET_SIZE - len(data))  # Receive remaining bytes to complete the packet
            if not packet:
                break  # Connection closed by the server
            data += packet

        if not data:
            break  # Connection closed by the server
        # Process the received market data
        process_market_data(data)

except ConnectionRefusedError:
    print("Connection to the server refused.")
except Exception as e:
    print("An error occurred:", e)

finally:
    # Close the socket
    sock.close()
    print("Socket closed.")


