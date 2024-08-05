import React from 'react'
import { FaRegUserCircle } from "react-icons/fa";

function Navbar() {
  return (
    <div className=' py-2 px-3 flex bg-opacity-50 justify-between w-full'>
        <h1 className='title font-[Grand Hotel] text-3xl text-white'>Insta</h1>
        <div className=" items-center text-lg flex gap-4 nav_container text-gray-400">
            <div className="user p-2 leading-0  bg-white text-black rounded-full"><FaRegUserCircle/></div>
        </div>
    
    </div>
  )
}

export default Navbar
