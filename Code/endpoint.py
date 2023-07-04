import socket
import asyncio
import json
import struct
import re
import websockets

# DATA SERVER
HOST = '127.0.0.1'  
PORT = 8040  
PACKET_SIZE = 130

async def process_market_data(raw_data):
    """
    Convert received raw data into usable JSON-formatted data.
    """

    packet_length, trading_symbol, sequence_number, timestamp, ltp, ltq, volume, \
    bid_price, bid_qty, ask_price, ask_qty, open_interest, prev_close_price, prev_open_interest = \
        struct.unpack('<i30sqqqqqqqqqqqq', raw_data)

   
    x = list(filter(''.__ne__, re.split(r'^([A-Z]{1,15})(?:([0-9]{2}[A-Z]{3}[0-9]{2})(?:([0-9.]+)([A-Z]{2}))?)?$',
                             str(trading_symbol.decode('utf-8').rstrip('\x00')))))
    x += ['-'] * (4 - (len(x)))
    symbol, expiry, strike_price, option_type = tuple(x)

    data = {
        'symbol': symbol,
        'timestamp': timestamp,
        'expiry': expiry,
        'strike_price': strike_price,
        'option_type': option_type,
        'LTP': (ltp / 100), 
        'LTQ': ltq,
        'volume': volume,
        'bid_price': (bid_price / 100), 
        'bid_qty': bid_qty,
        'ask_price': (ask_price / 100),  
        'ask_qty': ask_qty,
        'oi': open_interest,
        'pcp': (prev_close_price / 100),
        'poi': prev_open_interest,
    }
    return json.dumps(data)

async def send_market_data(websocket, path):
    recv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        
        recv_sock.connect((HOST, PORT))
        print("Connected to the server.")

        recv_sock.sendall(b'Ready')

        while True:
            data = b''  
            while len(data) < PACKET_SIZE:
                packet = recv_sock.recv(PACKET_SIZE - len(data)) 
                if not packet:
                    break  
                data += packet

            if not data:
                break  

            
            proc_data = await process_market_data(data)

           
            await websocket.send(proc_data)

    except ConnectionRefusedError:
        print("Connection to the server refused.")
    except Exception as e:
        print("An error occurred:", e)

    recv_sock.close()

start_server = websockets.serve(send_market_data, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()