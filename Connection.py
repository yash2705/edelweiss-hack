import socket
import struct
from math import log, sqrt, exp
from scipy.stats import norm
from datetime import datetime, timedelta
from scipy.optimize import brentq


def process_market_data(data):
    # Unpack the market data fields from the received data
    packet_length, symbol, sequence_number, timestamp, ltp, ltq, volume, \
    bid_price, bid_qty, ask_price, ask_qty, open_interest, prev_close_price, prev_open_interest = \
        struct.unpack('<i30sqqqqqqqqqqqq', data)

    # Convert symbol from bytes to string
    symbol = symbol.decode('utf-8').rstrip('\x00')

    ltp = ltp / 100.0
    bid_price = bid_price / 100.0
    ask_price = ask_price / 100.0
    prev_close_price = prev_close_price / 100.0

    market_data = {}
        # 'Symbol': symbol,
        # 'Sequence Number': sequence_number,
        # 'Timestamp': timestamp,
        # 'LTP': (ltp / 100),
        # 'LTQ': ltq,
        # 'Volume': volume,
        # 'Bid Price': (bid_price / 100),
        # 'Bid Quantity': bid_qty,
        # 'Ask Price': (ask_price / 100),
        # 'Ask Quantity': ask_qty,
        # 'Open Interest': open_interest,
        # 'Previous Close Price': (prev_close_price / 100),
        # 'Previous Open Interest': prev_open_interest
    # }

    if symbol.endswith('PE'):
        # Put Option specific calculations
        market_data['StockType'] = 'Put'
        market_data['CHNG_IN_OI'] = open_interest - prev_open_interest
        # Add calculations for OI, VOLUME, IV, LTP, CHNG, BID_QTY, BID, ASK, ASK_QTY
        # Replace the placeholders below with the actual formulas for each calculation
        market_data['OI'] = open_interest
        market_data['VOLUME'] = volume
        put_option_price = bid_price
        underlying_price = ltp
        strike_price = extract_strike_price(symbol)
        market_data['IV'] = calculate_implied_volatility(put_option_price, underlying_price, strike_price, 0.05, 0.5, 'put')
        market_data['CHNG'] = bid_price-prev_close_price
        market_data['BID_QTY'] = bid_qty
        market_data['BID'] = bid_price
        market_data['ASK'] = ask_price
        market_data['ASK_QTY'] = ask_qty
        
    elif symbol.endswith('CE'):
        # Call Option specific calculations
        market_data['StockType'] = 'Call'
        market_data['CHNG_IN_OI'] = open_interest - prev_open_interest
        # Add calculations for OI, VOLUME, IV, LTP, CHNG, BID_QTY, BID, ASK, ASK_QTY
        # Replace the placeholders below with the actual formulas for each calculation
        market_data['OI'] = open_interest
        market_data['VOLUME'] = volume
        call_option_price = bid_price
        underlying_price = ltp
        strike_price = extract_strike_price(symbol)
        market_data['IV'] = calculate_implied_volatility(call_option_price, underlying_price, strike_price, 0.05, 0.5, 'call' )
        market_data['CHNG'] = bid_price-prev_close_price
        market_data['BID_QTY'] = bid_qty
        market_data['BID'] = bid_price
        market_data['ASK'] = ask_price
        market_data['ASK_QTY'] = ask_qty

    return market_data

def extract_strike_price(symbol):
    prefix = symbol[:7]
    expiry_date = symbol[7:15]

    # Remove the "PE" or "CE" suffix from the symbol
    symbol = symbol.rstrip("PE").rstrip("CE")

    # Extract the strike price from the modified symbol
    strike_price = symbol[15:]

    # Check if the extracted strike price is numeric
    if strike_price.isnumeric():
        return int(strike_price)
    else:
        return None



# def calculate_implied_volatility(option_price, underlying_price, strike_price, risk_free_rate=0.05, ttm=1.0):
#     # Implement the Black-Scholes formula to calculate implied volatility
#     # Note: This is a simplified version of the formula for demonstration purposes
#     S = underlying_price
#     K = strike_price
#     r = risk_free_rate
#     T = ttm

#     iv = 0.5  # Initial guess for implied volatility

#     d1 = (log(S / K) + (r + 0.5 * (iv ** 2)) * T) / (iv * sqrt(T))
#     d2 = d1 - iv * sqrt(T)

#     call_price = S * norm.cdf(d1) - K * exp(-r * T) * norm.cdf(d2)
#     put_price = call_price - S + K * exp(-r * T)

#     # Newton-Raphson method to find implied volatility
#     epsilon = 0.001
#     max_iterations = 100
#     count = 0
#     while abs(option_price - put_price) > epsilon and count < max_iterations:
#         d1 = (log(S / K) + (r + 0.5 * (iv ** 2)) * T) / (iv * sqrt(T))
#         vega = S * norm.pdf(d1) * sqrt(T)

#         iv = iv - (put_price - option_price) / vega
#         count += 1

#         put_price = S * norm.cdf(d1) - K * exp(-r * T) * norm.cdf(d2)

#     return iv

def calculate_implied_volatility(option_price, underlying_price, strike_price, risk_free_rate, time_to_expiry, option_type):
    """Calculate implied volatility using the Black-Scholes formula."""
    tolerance = 0.0001
    max_iterations = 100
    volatility = 0.5  # Initial guess for implied volatility

    for _ in range(max_iterations):
        d1 = (log(underlying_price / strike_price) + (risk_free_rate + 0.5 * volatility**2) * time_to_expiry) / (volatility * sqrt(time_to_expiry))
        d2 = d1 - volatility * sqrt(time_to_expiry)

        if option_type == 'call':
            calculated_price = underlying_price * norm.cdf(d1) - strike_price * exp(-risk_free_rate * time_to_expiry) * norm.cdf(d2)
        elif option_type == 'put':
            calculated_price = strike_price * exp(-risk_free_rate * time_to_expiry) * norm.cdf(-d2) - underlying_price * norm.cdf(-d1)

        diff = option_price - calculated_price

        if abs(diff) < tolerance:
            return volatility

        vega = underlying_price * sqrt(time_to_expiry) * norm.pdf(d1)

        if vega == 0:
            return None

        volatility = volatility + diff / vega

    return None

    


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
        market_data = process_market_data(data)
        print(market_data)

except ConnectionRefusedError:
    print("Connection to the server refused.")
except Exception as e:
    print("An error occurred:", e)

finally:
    # Close the socket
    sock.close()
    print("Socket closed.")
