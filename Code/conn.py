import socket
import struct
import time
import re
from scipy.stats import norm
from scipy.optimize import fsolve
import numpy as np
from flask import Flask
import threading
from flask_cors import CORS, cross_origin

def process_market_data(data):
    packet_length, symbol, sequence_number, timestamp, ltp, ltq, volume, \
        bid_price, bid_qty, ask_price, ask_qty, open_interest, prev_close_price, prev_open_interest = \
        struct.unpack('<i30sqqqqqqqqqqqq', data)
    symbol = symbol.decode('utf-8').rstrip('\x00')
    market_data = {
        'Symbol': symbol,
        'Sequence Number': sequence_number,
        'Timestamp': timestamp,
        'LTP': (ltp / 100),
        'LTQ': ltq,
        'Volume': volume,
        'Bid Price': (bid_price / 100),
        'Bid Quantity': bid_qty,
        'Ask Price': (ask_price / 100),
        'Ask Quantity': ask_qty,
        'Open Interest': open_interest,
        'Previous Close Price': (prev_close_price / 100),
        'Previous Open Interest': prev_open_interest
    }
    index_name, expiry_date, strike_price, option_type = extract_components(
        symbol)
    market_data['indexName'] = index_name
    market_data['expiry_date'] = expiry_date
    market_data['strike_price'] = strike_price
    market_data['option_type'] = option_type
    ttm = unix_converter(timestamp, expiry_date)
    stock_type = market_data.get('StockType', 'Stock')
    market_data['StockType'] = stock_type
    if symbol.endswith('PE'):
        market_data['StockType'] = 'Put'
        market_data['CHNG_IN_OI'] = open_interest - prev_open_interest
        market_data['OI'] = open_interest
        market_data['VOLUME'] = volume
        put_option_price = bid_price
        underlying_price = ltp
        market_data['CHNG'] = ltp-prev_close_price
        market_data['BID_QTY'] = bid_qty
        market_data['BID'] = bid_price
        market_data['ASK'] = ask_price
        market_data['ASK_QTY'] = ask_qty
        market_data['TTM'] = ttm

    elif symbol.endswith('CE'):
        market_data['StockType'] = 'Call'
        market_data['CHNG_IN_OI'] = open_interest - prev_open_interest
        market_data['OI'] = open_interest
        market_data['VOLUME'] = volume
        call_option_price = bid_price
        underlying_price = ltp
        market_data['CHNG'] = ltp-prev_close_price
        market_data['BID_QTY'] = bid_qty
        market_data['BID'] = bid_price
        market_data['ASK'] = ask_price
        market_data['ASK_QTY'] = ask_qty
        market_data['TTM'] = ttm

    return market_data


def unix_converter(unix_timestamp, date_string):
    if date_string == '':
        return 0
    else:
        date_format = "%d%b%y"
        date_unix_timestamp = int(time.mktime(
            time.strptime(date_string, date_format)))
        time_difference = date_unix_timestamp - unix_timestamp // 1000
        days_difference = float(time_difference // (24 * 60 * 60))
        return days_difference


def extract_components(symbol):
    pattern = r'([A-Z]+)(\d{2}[A-Z]{3}\d{2})(\d+)([CP][E]?)'
    match = re.match(pattern, symbol)
    if match:
        index_name = match.group(1)
        expiry_date = match.group(2)
        strike_price = match.group(3)
        option_type = match.group(4)
        return index_name, expiry_date, strike_price, option_type
    else:
        return symbol, '', 0, None


def calculate_implied_volatility(option_price, underlying_price, strike_price, ttm, risk_free_rate, option_type):
    def black_scholes(iv):
        if strike_price != 0:
            d1 = (np.log(underlying_price / strike_price) +
                  (risk_free_rate + 0.5 * iv**2) * ttm) / (iv * np.sqrt(ttm))
            d2 = d1 - iv * np.sqrt(ttm)

            if option_type == 'call':
                return underlying_price * norm.cdf(d1) - strike_price * np.exp(-risk_free_rate * ttm) * norm.cdf(d2)
            elif option_type == 'put':
                return strike_price * np.exp(-risk_free_rate * ttm) * norm.cdf(-d2) - underlying_price * norm.cdf(-d1)
        else:
            pass

    def equations(vars):
        iv, sol = vars
        return [black_scholes(iv) - option_price, iv - sol]

    initial_guess = [0.5, 0.5]
    result = fsolve(equations, initial_guess)

    return result[0]


def appending_and_sorting(index_name, market_data, index_data_1, index_data_2, index_data_3, index_data_4):
    if index_name == 'MAINIDX':
        if index_name not in index_data_1:
            index_data_1[index_name] = []
        index_data_1[index_name].append(market_data)
    elif index_name == 'FINANCIALS':
        if index_name not in index_data_2:
            index_data_2[index_name] = []
        index_data_2[index_name].append(market_data)
    elif index_name == 'ALLBANKS':
        if index_name not in index_data_3:
            index_data_3[index_name] = []
        index_data_3[index_name].append(market_data)
    elif index_name == 'MIDCAPS':
        if index_name not in index_data_4:
            index_data_4[index_name] = []
        index_data_4[index_name].append(market_data)
    if index_name == 'MAINIDX':
        index_data_1[index_name].sort(
            key=lambda x: x['Sequence Number'])
    elif index_name == 'FINANCIALS':
        index_data_2[index_name].sort(
            key=lambda x: x['Sequence Number'])
    elif index_name == 'ALLBANKS':
        index_data_3[index_name].sort(
            key=lambda x: x['Sequence Number'])
    elif index_name == 'MIDCAPS':
        index_data_4[index_name].sort(
            key=lambda x: x['Sequence Number'])


def get_market_data_list():
    index_data_1 = {}
    index_data_2 = {}
    index_data_3 = {}
    index_data_4 = {}
    i = 0
    while i <= 1500:
        data = b''
        while len(data) < PACKET_SIZE:
            packet = sock.recv(PACKET_SIZE - len(data))
            if not packet:
                break
            data += packet
        if not data:
            break
        market_data = process_market_data(data)
        index_name = market_data['indexName']
        appending_and_sorting(
            index_name, market_data, index_data_1, index_data_2, index_data_3, index_data_4)
        i += 1
    count = 0
    for market_data in index_data_1['MAINIDX'][1:]:
        if market_data['StockType'] == 'Call':
            option_price = market_data['LTP']
            spot_price = index_data_1['MAINIDX'][0]['LTP']
            strike_price = float(market_data['strike_price'])
            time_to_maturity = market_data['TTM']
            risk_free_rate = 0.05  # Assuming a fixed risk-free interest rate of 5%
            option_type = 'call'
            implied_volatility = calculate_implied_volatility(
                option_price, spot_price, strike_price, time_to_maturity, risk_free_rate, option_type)
            index_data_1['MAINIDX'][count +
                                    1]['IV'] = implied_volatility

        elif market_data['StockType'] == 'Put':
            option_price = market_data['LTP']
            spot_price = index_data_1['MAINIDX'][0]['LTP']
            strike_price = float(market_data['strike_price'])
            time_to_maturity = market_data['TTM']
            risk_free_rate = 0.05  # Assuming a fixed risk-free interest rate of 5%
            option_type = 'put'
            implied_volatility = calculate_implied_volatility(
                option_price, spot_price, strike_price, time_to_maturity, risk_free_rate, option_type)
            index_data_1['MAINIDX'][count +
                                    1]['IV'] = implied_volatility
        count += 1

    count = 0
    for market_data in index_data_2['FINANCIALS'][1:]:
        if market_data['StockType'] == 'Call':
            option_price = market_data['LTP']
            spot_price = index_data_2['FINANCIALS'][0]['LTP']
            strike_price = float(market_data['strike_price'])
            time_to_maturity = market_data['TTM']
            risk_free_rate = 0.05  # Assuming a fixed risk-free interest rate of 5%
            option_type = 'call'
            implied_volatility = calculate_implied_volatility(
                option_price, spot_price, strike_price, time_to_maturity, risk_free_rate, option_type)
            index_data_2['FINANCIALS'][count +
                                       1]['IV'] = implied_volatility

        elif market_data['StockType'] == 'Put':
            option_price = market_data['LTP']
            spot_price = index_data_2['FINANCIALS'][0]['LTP']
            strike_price = float(market_data['strike_price'])
            time_to_maturity = market_data['TTM']
            risk_free_rate = 0.05
            option_type = 'put'
            implied_volatility = calculate_implied_volatility(
                option_price, spot_price, strike_price, time_to_maturity, risk_free_rate, option_type)
            index_data_2['FINANCIALS'][count +
                                       1]['IV'] = implied_volatility
        count += 1

    count = 0
    for market_data in index_data_3['ALLBANKS'][1:]:
        if market_data['StockType'] == 'Call':
            option_price = market_data['LTP']
            spot_price = index_data_3['ALLBANKS'][0]['LTP']
            strike_price = float(market_data['strike_price'])
            time_to_maturity = market_data['TTM']
            risk_free_rate = 0.05
            option_type = 'call'
            implied_volatility = calculate_implied_volatility(
                option_price, spot_price, strike_price, time_to_maturity, risk_free_rate, option_type)
            index_data_3['ALLBANKS'][count +
                                     1]['IV'] = implied_volatility

        elif market_data['StockType'] == 'Put':
            option_price = market_data['LTP']
            spot_price = index_data_3['ALLBANKS'][0]['LTP']
            strike_price = float(market_data['strike_price'])
            time_to_maturity = market_data['TTM']
            risk_free_rate = 0.05
            option_type = 'put'
            implied_volatility = calculate_implied_volatility(
                option_price, spot_price, strike_price, time_to_maturity, risk_free_rate, option_type)
            index_data_3['ALLBANKS'][count +
                                     1]['IV'] = implied_volatility
        count += 1

    count = 0
    for market_data in index_data_4['MIDCAPS'][1:]:
        if market_data['StockType'] == 'Call':
            option_price = market_data['LTP']
            spot_price = index_data_4['MIDCAPS'][0]['LTP']
            strike_price = float(market_data['strike_price'])
            time_to_maturity = market_data['TTM']
            risk_free_rate = 0.05
            option_type = 'call'
            implied_volatility = calculate_implied_volatility(
                option_price, spot_price, strike_price, time_to_maturity, risk_free_rate, option_type)
            index_data_4['MIDCAPS'][count +
                                    1]['IV'] = implied_volatility

        elif market_data['StockType'] == 'Put':
            option_price = market_data['LTP']
            spot_price = index_data_4['MIDCAPS'][0]['LTP']
            strike_price = float(market_data['strike_price'])
            time_to_maturity = market_data['TTM']
            risk_free_rate = 0.05
            option_type = 'put'
            implied_volatility = calculate_implied_volatility(
                option_price, spot_price, strike_price, time_to_maturity, risk_free_rate, option_type)
            index_data_4['MIDCAPS'][count +
                                    1]['IV'] = implied_volatility
        count += 1

    return [index_data_1, index_data_2, index_data_3, index_data_4]
 

def update_data():
    global market_data
    while True:
        market_data = get_market_data_list()

# Initializing flask app
app = Flask('market_data_api')
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/data')
@cross_origin()
def get_data():
    global market_data
    return {'records': market_data}

HOST = '127.0.0.1'
PORT = 8080
PACKET_SIZE = 130
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST,PORT))
sock.sendall(b'Ready')

t = threading.Thread(None, update_data)
t.start()
app.run(debug=True)