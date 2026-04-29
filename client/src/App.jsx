import { useState } from 'react'
import './App.css'
import Navbar from './Navbar'
import RecommendationCard from './RecommendationCard'
import Discovery from './Discovery'

function App() {
  
  const [rec, setRec] = useState([])
  const [historyUploaded, setHistory] = useState(false)

  async function handleSubmit(selectedFile, query) {
    if(selectedFile){
      const formData = new FormData()
      formData.append('file', selectedFile)
        await fetch("http://localhost:8000/import",{
          method:'POST',
          body: formData
    })
      setHistory(true)
    }
    const responseQuery = await fetch("http://localhost:8000/recommendation",{
      method:'POST',
      headers: {
        'Content-Type' : 'application/json'
      },
      body: JSON.stringify({query: query})
    })
    const dataQuery = await responseQuery.json()
    setRec(dataQuery.Recommendations)
  }

  return (
    <>
    <Navbar></Navbar>
    <div className='max-w-4xl mx-auto px-4 md:px-6 py-8'>
    <Discovery onSubmit ={handleSubmit}></Discovery>
    {historyUploaded && <p>Music History Successfully Uploaded!</p>}
    {rec.map((recs, index) => (
      <RecommendationCard
      key={index}
      artist={recs.artist}
      album={recs.album}
      title={recs.title}
      reason={recs.reason}
    />
  ))}
  </div>
    </>
  )
}

export default App
