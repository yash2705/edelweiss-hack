import React, {useState, useRef}from 'react';
import HeaderMain from './components/HeaderMain';
import Table from './components/Table';
import Dummy from './components/Dummy';
import TrialTable from './components/TrialTable';



const App = () => {
  return (
    <div className='h-screen'>
    <HeaderMain />
    <div className='h-full justify-center flex'>
      <Table />
    </div>
    {/* <FakeTable /> */}
    {/* <NewTable /> */}
    {/* <Dummy /> */}
    {/* <TrialTable /> */}
    </div>
  )
}

export default App