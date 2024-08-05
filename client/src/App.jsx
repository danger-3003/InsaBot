import React from 'react'
import './App.css'
import { Outlet } from 'react-router-dom'
function App() {
  return (
    <div className='justify-center flex items-center w-full'>
      <Outlet/>
    </div>
  )
}

export default App
