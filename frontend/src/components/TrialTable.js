import React from 'react';

const TrialTable = () => {
  const generateOptionChainData = () => {
    const data = [];
    const strikePrices = Array.from(Array(40), (_, i) => 18000 + i * 50);

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

      data.push({ callOption, putOption });
    });

    return data;
  };

  const optionChainData = generateOptionChainData();

  return (
    <div className="table-container">
      <table className="w-full border-collapse border">
        <thead>
          <tr className="bg-gray-200 sticky top-0">
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
            <th className="border p-2">Strike Price</th>
            <th className="border p-2">ASK QTY</th>
            <th className="border p-2">ASK</th>
            <th className="border p-2">BID</th>
            <th className="border p-2">BID QTY</th>
            <th className="border p-2">CHNG</th>
            <th className="border p-2">LTP</th>
            <th className="border p-2">IV</th>
            <th className="border p-2">VOLUME</th>
            <th className="border p-2">CHNG IN OI</th>
            <th className="border p-2">OI</th>
          </tr>
        </thead>
        <tbody>
          {/* Render table rows */}
          {optionChainData.map((option, index) => (
            <tr key={index} className={`bg-white ${option.callOption.strikePrice === 19500 ? 'bg-blue-300' : ''}`}>
              <td className={`border p-2 text-center ${option.callOption.strikePrice < 19500 ? 'bg-yellow-100' : ''}`}>{option.callOption.OI}</td>
              <td className={`border p-2 text-center ${option.callOption.strikePrice < 19500 ? 'bg-yellow-100' : ''}`}>{option.callOption.CHNG_IN_OI}</td>
              <td className={`border p-2 text-center ${option.callOption.strikePrice < 19500 ? 'bg-yellow-100' : ''}`}>{option.callOption.VOLUME}</td>
              <td className={`border p-2 text-center ${option.callOption.strikePrice < 19500 ? 'bg-yellow-100' : ''}`}>{option.callOption.IV}</td>
              <td className={`border p-2 text-center ${option.callOption.strikePrice < 19500 ? 'bg-yellow-100' : ''}`}>{option.callOption.LTP}</td>
              <td className={`border p-2 text-center ${option.callOption.strikePrice < 19500 ? 'bg-yellow-100' : ''}`}>{option.callOption.CHNG}</td>
              <td className={`border p-2 text-center ${option.callOption.strikePrice < 19500 ? 'bg-yellow-100' : ''}`}>{option.callOption.BID_QTY}</td>
              <td className={`border p-2 text-center ${option.callOption.strikePrice < 19500 ? 'bg-yellow-100' : ''}`}>{option.callOption.BID}</td>
              <td className={`border p-2 text-center ${option.callOption.strikePrice < 19500 ? 'bg-yellow-100' : ''}`}>{option.callOption.ASK}</td>
              <td className={`border p-2 text-center ${option.callOption.strikePrice < 19500 ? 'bg-yellow-100' : ''}`}>{option.callOption.ASK_QTY}</td>
              <td className="border p-2 text-center underline cursor-pointer font-medium text-purple-800 hover:text-purple-500">{option.callOption.strikePrice}</td>
              <td className={`border p-2 text-center ${option.putOption.strikePrice > 19500 ? 'bg-yellow-100' : ''}`}>{option.putOption.ASK_QTY}</td>
              <td className={`border p-2 text-center ${option.putOption.strikePrice > 19500 ? 'bg-yellow-100' : ''}`}>{option.putOption.ASK}</td>
              <td className={`border p-2 text-center ${option.putOption.strikePrice > 19500 ? 'bg-yellow-100' : ''}`}>{option.putOption.BID}</td>
              <td className={`border p-2 text-center ${option.putOption.strikePrice > 19500 ? 'bg-yellow-100' : ''}`}>{option.putOption.BID_QTY}</td>
              <td className={`border p-2 text-center ${option.putOption.strikePrice > 19500 ? 'bg-yellow-100' : ''}`}>{option.putOption.CHNG}</td>
              <td className={`border p-2 text-center ${option.putOption.strikePrice > 19500 ? 'bg-yellow-100' : ''}`}>{option.putOption.LTP}</td>
              <td className={`border p-2 text-center ${option.putOption.strikePrice > 19500 ? 'bg-yellow-100' : ''}`}>{option.putOption.IV}</td>
              <td className={`border p-2 text-center ${option.putOption.strikePrice > 19500 ? 'bg-yellow-100' : ''}`}>{option.putOption.VOLUME}</td>
              <td className={`border p-2 text-center ${option.putOption.strikePrice > 19500 ? 'bg-yellow-100' : ''}`}>{option.putOption.CHNG_IN_OI}</td>
              <td className={`border p-2 text-center ${option.putOption.strikePrice > 19500 ? 'bg-yellow-100' : ''}`}>{option.putOption.OI}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default TrialTable;
