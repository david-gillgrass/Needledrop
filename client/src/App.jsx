import { useState } from 'react'
import './App.css'
import Navbar from './Navbar'
import Search from './Search'
import RecommendationCard from './RecommendationCard'

function App() {
  
  const [query, setQuery] = useState('')
  const [rec, setRecc] = useState([])
  const fakeRecs = [
    { artist: "Radiohead", album: "OK Computer", title: "Karma Police", reason: "You like alternative rock" },
    { artist: "Guns N' Roses", album: "Appetite for Destruction", title: "Welcome to the Jungle", reason: "It Rocks!" },
    { artist: "Van Halen", album: "1984", title: "Jump", reason: "High energy classic rock" },
]
  
  function handleSearch(query){
    setQuery(query)
  }

  return (
    <>
    <Navbar></Navbar>
    <Search onSearch={handleSearch}></Search>
    {fakeRecs.map((recs, index) => (
      <RecommendationCard
      key={index}
      artist={recs.artist}
      album={recs.album}
      title={recs.title}
      reason={recs.reason}
    />
  ))}
    </>
  )
}



export default App
