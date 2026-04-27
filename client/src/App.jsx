import { useState } from 'react'
import './App.css'
import Navbar from './Navbar'
import Search from './Search'
import RecommendationCard from './RecommendationCard'
import ImportBar from './Importbar'

function App() {
  
  const [query, setQuery] = useState('')
  const [rec, setRec] = useState([])
  const [selectedFile, setSelectedFile] = useState(null)
  const [historyUploaded, setHistory] = useState(false)

  
  async function handleSearch(query){
    const response = await fetch("http://localhost:8000/recommendation", {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ query: query })
    })
    const data = await response.json()
    setRec(data.Recommendations)
  }

  async function handleImport(selectedFile){
    const formData = new FormData()
    formData.append('file', selectedFile)
    const response = await fetch("http://localhost:8000/import",{
      method: 'POST',
      body: formData
    })
    const data = await response.json
    setHistory(true)
    handleSearch()
  }

  return (
    <>
    <Navbar></Navbar>
    <ImportBar onImport={handleImport}></ImportBar>
    {historyUploaded && <p>Music History Successfully Uploaded!</p>}
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
