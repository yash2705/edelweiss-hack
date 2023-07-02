import React, {useState, useRef}from 'react';
import HeaderMain from './components/HeaderMain';
import Table from './components/Table';



const App = () => {
  return (
    <div className='h-screen'>
    <HeaderMain />
    <div className='h-full justify-center flex'>
      <Table />
    </div>
    </div>
  )
}

export default App