import { useState } from 'react'
import './App.css'
import Navbar from './Navbar'
import Search from './Search'
import RecommendationCard from './RecommendationCard'

function App() {
  
  const [query, setQuery] = useState('')
  const [rec, setRecc] = useState([])

  
  async function handleSearch(query){
    const response = await fetch("http://localhost:8000/recommendation", {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ query: query })
    })
    const data = await response.json()
    setRecc(data.Recommendations)
  }

  return (
    <>
    <Navbar></Navbar>
    <Search onSearch={handleSearch}></Search>
    {rec.map((recs, index) => (
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
