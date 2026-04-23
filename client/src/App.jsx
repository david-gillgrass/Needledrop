import { useState } from 'react'
import './App.css'
import Navbar from './Navbar'
import Search from './Search'

function App() {
  
  function handleSearch(query){
    console.log(query)
  }

  return (
    <>
    <Navbar></Navbar>
    <Search onSearch={handleSearch}></Search>
    </>
  )
}



export default App
