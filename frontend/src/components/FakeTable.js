import React from 'react';

const generateFakeData = () => {
    const data = [];
  
    for (let i = 1; i <= 20; i++) {
      const obj = {
        attribute1: `Value ${i} Attribute 1`,
        attribute2: `Value ${i} Attribute 2`,
        attribute3: `Value ${i} Attribute 3`,
        attribute4: `Value ${i} Attribute 4`,
        attribute5: `Value ${i} Attribute 5`,
        attribute6: `Value ${i} Attribute 6`,
        attribute7: `Value ${i} Attribute 7`,
        attribute8: `Value ${i} Attribute 8`,
        attribute9: `value ${i} Attribute 9`
      };
  
      data.push(obj);
    }
  
    return data;
  };

const FakeTable = () => {
    const data = generateFakeData();
  return (
    <table className="min-w-full bg-white border border-gray-200 ">
      <thead className='sticky top-0 bg-white'>
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
      </thead>
      <tbody>
        {data.map((item) => (
          <tr key={item.id}>
            <td className="py-2 px-4 border-b border-r">{item.attribute1}</td>
            <td className="py-2 px-4 border-b border-r">{item.attribute2}</td>
            <td className="py-2 px-4 border-b border-r">{item.attribute3}</td>
            <td className="py-2 px-4 border-b border-r">{item.attribute4}</td>
            <td className="py-2 px-4 border-b border-r">{item.attribute5}</td>
            <td className="py-2 px-4 border-b border-r">{item.attribute6}</td>
            <td className="py-2 px-4 border-b border-r">{item.attribute7}</td>
            <td className="py-2 px-4 border-b border-r">{item.attribute8}</td>
            <td className="py-2 px-4 border-b border-r">{item.attribute9}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default FakeTable;
