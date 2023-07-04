import React from 'react';

const OptionChainTable = ({ optionChainData }) => {
  // Filter call and put options
  const callOptions = optionChainData.filter(option => option.optionType === 'call');
  const putOptions = optionChainData.filter(option => option.optionType === 'put');

  return (
    <table>
      <thead>
        <tr>
          <th>Symbol</th>
          <th colSpan="8">Call Options</th>
          <th>Strike Price</th>
          <th colSpan="8">Put Options</th>
        </tr>
        <tr>
          <th></th>
          <tr>
          <th className="py-2 px-4 border-b">OI Change (%)</th>
          <th className="py-2 px-4 border-b">OI-Lakh</th>
          <th className="py-2 px-4 border-b">LTP</th>
          <th className="py-2 px-4 border-b">IV</th>
          <th className="py-2 px-4 border-b">Strike</th>
          <th className="py-2 px-4 border-b">IV</th>
          <th className="py-2 px-4 border-b">LTP</th>
          <th className="py-2 px-4 border-b">OI-Lakh</th>
          <th className="py-2 px-4 border-b">OI Change (%)</th>
        </tr>
          <th></th>
          <tr>
          <th className="py-2 px-4 border-b">OI Change (%)</th>
          <th className="py-2 px-4 border-b">OI-Lakh</th>
          <th className="py-2 px-4 border-b">LTP</th>
          <th className="py-2 px-4 border-b">IV</th>
          <th className="py-2 px-4 border-b">Strike</th>
          <th className="py-2 px-4 border-b">IV</th>
          <th className="py-2 px-4 border-b">LTP</th>
          <th className="py-2 px-4 border-b">OI-Lakh</th>
          <th className="py-2 px-4 border-b">OI Change (%)</th>
        </tr>
          <th></th>
        </tr>
      </thead>
      <tbody>
        {/* Render table rows */}
        {optionChainData.map((option, index) => (
          <tr key={index}>
            <td>{option.symbol}</td>
            {/* Render call option cells */}
            {callOptions.slice(0, 8).map((callOption, i) => (
              <td key={i}>{callOption.data}</td>
            ))}
            <td>{option.strikePrice}</td>
            {/* Render put option cells */}
            {putOptions.slice(0, 8).map((putOption, i) => (
              <td key={i}>{putOption.data}</td>
            ))}
            <td>{option.expirationDate}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default OptionChainTable;
