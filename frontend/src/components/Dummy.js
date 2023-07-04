import React from 'react';

const Dummy = () => {

  const generateData = () => {
    const data = [];
    const strikePrices = Array.from(Array(601), (_, i) => 17000 + i * 50);
  
    strikePrices.forEach((strikePrice) => {
      const callOption = {
        strikePrice,
        optionType: 'Call',
        OI: Math.floor(Math.random() * 100000),
        CHNG_IN_OI: Math.floor(Math.random() * 100),
        VOLUME: Math.floor(Math.random() * 1000),
        IV: Math.random().toFixed(2),
        LTP: Math.floor(Math.random() * 1000),
        CHNG: Math.floor(Math.random() * 10),
        BID_QTY: Math.floor(Math.random() * 100),
        BID: Math.floor(Math.random() * 1000),
        ASK: Math.floor(Math.random() * 1000),
        ASK_QTY: Math.floor(Math.random() * 100),
      };
  
      const putOption = {
        strikePrice,
        optionType: 'Put',
        OI: Math.floor(Math.random() * 100000),
        CHNG_IN_OI: Math.floor(Math.random() * 100),
        VOLUME: Math.floor(Math.random() * 1000),
        IV: Math.random().toFixed(2),
        LTP: Math.floor(Math.random() * 1000),
        CHNG: Math.floor(Math.random() * 10),
        BID_QTY: Math.floor(Math.random() * 100),
        BID: Math.floor(Math.random() * 1000),
        ASK: Math.floor(Math.random() * 1000),
        ASK_QTY: Math.floor(Math.random() * 100),
      };
  
      data.push(callOption, putOption);
    });
  
    return data;
  };
  // Generate fake option chain data
  const generateOptionChainData = () => {
    const symbols = ['AAPL', 'GOOGL', 'MSFT']; // Add more symbols as needed
    const strikePrices = [150, 155, 160, 165, 170, 175, 180, 185, 190, 195];

    const optionChainData = [];

    for (let symbol of symbols) {
      for (let strikePrice of strikePrices) {
        const expirationDate = '2023-07-21';

        // Generate fake call option data
        const callOption = {
          symbol,
          expirationDate,
          strikePrice,
          optionType: 'call',
          data: `Call Option Data (${symbol}, ${expirationDate}, ${strikePrice})`,
        };
        optionChainData.push(callOption);

        // Generate fake put option data
        const putOption = {
          symbol,
          expirationDate,
          strikePrice,
          optionType: 'put',
          data: `Put Option Data (${symbol}, ${expirationDate}, ${strikePrice})`,
        };
        optionChainData.push(putOption);
      }
    }

    return optionChainData;
  };

  const optionChainData = generateData();

  // Group option chain data by symbol and strike price
  // const groupedOptionChainData = {};
  // optionChainData.forEach(option => {
  //   const key = `${option.symbol}_${option.strikePrice}`;
  //   if (!groupedOptionChainData[key]) {
  //     groupedOptionChainData[key] = {
  //       symbol: option.symbol,
  //       strikePrice: option.strikePrice,
  //       expirationDate: option.expirationDate,
  //       callOptions: [],
  //       putOptions: [],
  //     };
  //   }

  //   if (option.optionType === 'call') {
  //     groupedOptionChainData[key].callOptions.push(option);
  //   } else if (option.optionType === 'put') {
  //     groupedOptionChainData[key].putOptions.push(option);
  //   }
  // });

  // const uniqueOptionChainData = Object.values(groupedOptionChainData);

  return (
    <div className="table-container">
      <table className="w-full border-collapse border">
        <thead className="sticky top-0 bg-gray-200">
          <tr>
            <th className="border p-2">OI</th>
            <th className="border p-2">CHNG IN OI</th>
            <th className="border p-2">VOLUME</th>
            <th className="border p-2">IV</th>
            <th className="border p-2">LTP</th>
            <th className="border p-2">CHNG</th>
            <th className="border p-2">BID QTY</th>
            <th className="border p-2">BID</th>
            <th className="border p-2">ASK</th>
            <th className="border p-2">ASK QTY</th>
            <th className="border p-2">
              <div className="flex items-center justify-center">
                <span>Strike Price</span>
              </div>
            </th>
            <th className="border p-2">OI</th>
            <th className="border p-2">CHNG IN OI</th>
            <th className="border p-2">VOLUME</th>
            <th className="border p-2">IV</th>
            <th className="border p-2">LTP</th>
            <th className="border p-2">CHNG</th>
            <th className="border p-2">BID QTY</th>
            <th className="border p-2">BID</th>
            <th className="border p-2">ASK</th>
            <th className="border p-2">ASK QTY</th>
          </tr>
        </thead>
        <tbody>
          {optionChainData.map((option, index) => (
            <tr key={index}>
              {/* Render call option data */}
              {option.optionType === 'Call' && (
                <>
                  <td className="border p-2">{option.OI}</td>
                  <td className="border p-2">{option.CHNG_IN_OI}</td>
                  <td className="border p-2">{option.VOLUME}</td>
                  <td className="border p-2">{option.IV}</td>
                  <td className="border p-2">{option.LTP}</td>
                  <td className="border p-2">{option.CHNG}</td>
                  <td className="border p-2">{option.BID_QTY}</td>
                  <td className="border p-2">{option.BID}</td>
                  <td className="border p-2">{option.ASK}</td>
                  <td className="border p-2">{option.ASK_QTY}</td>
                </>
              )}
              <td className="border p-2">{option.strikePrice}</td>
              {/* Render put option data */}
              {option.optionType === 'Put' && (
                <>
                  <td className="border p-2">{option.OI}</td>
                  <td className="border p-2">{option.CHNG_IN_OI}</td>
                  <td className="border p-2">{option.VOLUME}</td>
                  <td className="border p-2">{option.IV}</td>
                  <td className="border p-2">{option.LTP}</td>
                  <td className="border p-2">{option.CHNG}</td>
                  <td className="border p-2">{option.BID_QTY}</td>
                  <td className="border p-2">{option.BID}</td>
                  <td className="border p-2">{option.ASK}</td>
                  <td className="border p-2">{option.ASK_QTY}</td>
                </>
              )}
              <td className="border p-2">{option.optionType}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Dummy;

