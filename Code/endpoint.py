import socket
import json
import struct
import re

# DATA SERVER
HOST = '127.0.0.1'  # Update with the server's IP address or hostname
PORT = 8050  # Update with the server's listening port
PACKET_SIZE = 130 

# BACKEND SERVER
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 8888 # Connect to this port to recieve data

def process_market_data(raw_data) -> str:
    """
    Convert recieved raw data into usable JSON-formatted data.
    """

    OPTION_TYPES = {'PE': 'PUT', 'CE': 'CALL', 'XX': 'FUTURES'}
    
    packet_length, trading_symbol, sequence_number, timestamp, ltp, ltq, volume, \
    bid_price, bid_qty, ask_price, ask_qty, open_interest, prev_close_price, prev_open_interest = \
        struct.unpack('<i30sqqqqqqqqqqqq', raw_data)

    # Convert symbol from bytes to string and seperate the data into symbol, expiry, strike price and option type
    symbol, expiry, strike_price, option_type = tuple(filter(''.__ne__, re.split(r'^([A-Z]{1,15})(?:([0-9]{2}[A-Z]{3}[0-9]{2})(?:([0-9.]+)([A-Z]{2}))?)?$', str(trading_symbol.decode('utf-8').rstrip('\x00')))))
    
    option_type = OPTION_TYPES[option_type.upper()]
    
    data = {
        'symbol': symbol,
        'timestamp': timestamp,
        'LTP': (ltp / 100),   # Convert from paise to rupees
        'LTQ': ltq,
        'volume': volume,
        'bid_price': (bid_price / 100),  # Convert from paise to rupees
        'bid_qty': bid_qty,
        'ask_price': (ask_price / 100),  # Convert from paise to rupees
        'ask_qty': ask_qty,
        'oi': open_interest,
        'pcp': (prev_close_price / 100),  # Convert from paise to rupees
        'poi': prev_open_interest,
    }
    return json.dumps(data)

# Create a TCP/IP socket
recv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
send_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

send_sock.bind((SERVER_HOST, SERVER_PORT))
send_sock.listen(1)

try:
    # Connect to the server
    recv_sock.connect((HOST, PORT))
    print("Connected to the server.")

except ConnectionRefusedError:
    print("Connection to the server refused.")
except Exception as e:
    print("An error occurred:", e)

def start_socket_transmission():
    # Send a request to indicate readiness
    re.sendall(b'Ready')

    # Receive and process market data
    while True:
        data = b''  # Initialize an empty buffer
        while len(data) < PACKET_SIZE:
            packet = recv_sock.recv(PACKET_SIZE - len(data))  # Receive remaining bytes to complete the packet
            if not packet:
                break  # Connection closed by the server
            data += packet

        if not data:
            break  # Connection closed by the server
        
        # Process the received market data
        proc_data = process_market_data(data)
        connection, address = send_sock.accept()
        connection.sendall(proc_data)
