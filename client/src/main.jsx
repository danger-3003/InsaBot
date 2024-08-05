import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter, Routes, Route } from "react-router-dom";
import App from './App.jsx'
import Login from './components/Authantication/Login.jsx'
import Signup from './components/Authantication/Signup.jsx'
import Home from './components/Home/Home.jsx';
ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<App/>}>
          <Route path="" element={<Login />} />
          {/* <Route path="Signup" element={<Signup />} /> */}
          <Route path="Home" element={<Home/>} />
        </Route>
      </Routes>
    </BrowserRouter>
  </React.StrictMode>,
)
