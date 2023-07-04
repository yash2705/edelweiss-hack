import React, { useEffect, useState } from 'react';
import axios from 'axios';

function Table() {
  const [data, setData] = useState([]);

  useEffect(()=>{
    const getData = async () =>{
      const d = await axios.get('http://127.0.0.1:5000/data')
      console.log(d.data.records[0].MAINIDX)
      setData(d.data.records[0].MAINIDX)
    }

    getData()
  },[])
  // useEffect(() => {
  //   const socket = new WebSocket('ws://localhost:8765');
  //   socket.onmessage = async (event) => {
  //     const receivedData = await JSON.parse(event.data);
  //     console.log(receivedData.strike_price, receivedData.option_type, receivedData.symbol)
  //   };
    
  //   return () => {
  //     socket.close();
  //   };
  // }, []);

  return (
    <table>
    <thead className='w-full justify-around'>
      <tr>
        <th className="border p-2">STRIKE PRICE</th>
        <th className="border p-2">OPTION TYPE</th>
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
      {data.map((d,i)=>{
        return (
        <tr key={i} className=''>
          <td className={`border p-2 text-center ${d.option_type === 'CE' && d.strike_price < 19500 ? 'bg-yellow-100' : ''}  ${d.option_type === 'PE' && d.strike_price > 19500 ? 'bg-yellow-100' : ''} ${d.strike_price === "19500" ? 'bg-blue-300' : ''}`}>{d.strike_price}</td>
          <td className={`border p-2 text-center ${d.option_type === 'CE' && d.strike_price < 19500 ? 'bg-yellow-100' : ''}  ${d.option_type === 'PE' && d.strike_price > 19500 ? 'bg-yellow-100' : ''} ${d.strike_price === "19500" ? 'bg-blue-300' : ''}`}>{d.option_type}</td>
          <td className={`border p-2 text-center ${d.option_type === 'CE' && d.strike_price < 19500 ? 'bg-yellow-100' : ''}  ${d.option_type === 'PE' && d.strike_price > 19500 ? 'bg-yellow-100' : ''} ${d.strike_price === "19500" ? 'bg-blue-300' : ''}`}>{d.OI}</td>
          <td className={`border p-2 text-center ${d.option_type === 'CE' && d.strike_price < 19500 ? 'bg-yellow-100' : ''}  ${d.option_type === 'PE' && d.strike_price > 19500 ? 'bg-yellow-100' : ''} ${d.strike_price === "19500" ? 'bg-blue-300' : ''}`}>{d.CHNG_IN_OI}</td>
          <td className={`border p-2 text-center ${d.option_type === 'CE' && d.strike_price < 19500 ? 'bg-yellow-100' : ''}  ${d.option_type === 'PE' && d.strike_price > 19500 ? 'bg-yellow-100' : ''} ${d.strike_price === "19500" ? 'bg-blue-300' : ''}`}>{d.VOLUME}</td>
          <td className={`border p-2 text-center ${d.option_type === 'CE' && d.strike_price < 19500 ? 'bg-yellow-100' : ''}  ${d.option_type === 'PE' && d.strike_price > 19500 ? 'bg-yellow-100' : ''} ${d.strike_price === "19500" ? 'bg-blue-300' : ''}`}>{d.IV < 0 && (d.IV * -1).toFixed(2) ||d.IV > 0 && d.IV.toFixed(2) || '-'}</td>
          <td className={`border p-2 text-center ${d.option_type === 'CE' && d.strike_price < 19500 ? 'bg-yellow-100' : ''}  ${d.option_type === 'PE' && d.strike_price > 19500 ? 'bg-yellow-100' : ''} ${d.strike_price === "19500" ? 'bg-blue-300' : ''}`}>{d.LTP}</td>
          <td className={`border p-2 text-center ${d.option_type === 'CE' && d.strike_price < 19500 ? 'bg-yellow-100' : ''}  ${d.option_type === 'PE' && d.strike_price > 19500 ? 'bg-yellow-100' : ''} ${d.strike_price === "19500" ? 'bg-blue-300' : ''}`}>{d.CHNG}</td>
          <td className={`border p-2 text-center ${d.option_type === 'CE' && d.strike_price < 19500 ? 'bg-yellow-100' : ''}  ${d.option_type === 'PE' && d.strike_price > 19500 ? 'bg-yellow-100' : ''} ${d.strike_price === "19500" ? 'bg-blue-300' : ''}`}>{d.BID_QTY}</td>
          <td className={`border p-2 text-center ${d.option_type === 'CE' && d.strike_price < 19500 ? 'bg-yellow-100' : ''}  ${d.option_type === 'PE' && d.strike_price > 19500 ? 'bg-yellow-100' : ''} ${d.strike_price === "19500" ? 'bg-blue-300' : ''}`}>{d.BID}</td>
          <td className={`border p-2 text-center ${d.option_type === 'CE' && d.strike_price < 19500 ? 'bg-yellow-100' : ''}  ${d.option_type === 'PE' && d.strike_price > 19500 ? 'bg-yellow-100' : ''} ${d.strike_price === "19500" ? 'bg-blue-300' : ''}`}>{d.ASK}</td>
          <td className={`border p-2 text-center ${d.option_type === 'CE' && d.strike_price < 19500 ? 'bg-yellow-100' : ''}  ${d.option_type === 'PE' && d.strike_price > 19500 ? 'bg-yellow-100' : ''} ${d.strike_price === "19500" ? 'bg-blue-300' : ''}`}>{d.ASK_QTY}</td>
        </tr> 
      )})}
    </tbody>
    </table>
  );
}

export default Table;