import { useState } from 'react'
import './App.css'
import Navbar from './Navbar'
import RecommendationCard from './RecommendationCard'
import Discovery from './Discovery'

function App() {
  
  const [rec, setRec] = useState([])
  const [historyUploaded, setHistory] = useState(false)

  async function handleSubmit(selectedFile, query, aiAgent) {
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
      body: JSON.stringify({query: query, aiAgent: aiAgent})
    })
    const dataQuery = await responseQuery.json()
    setRec(dataQuery.Recommendations)
  }

  return (
    <>
    <div className='min-h-screen bg-linear-to-r from-zinc-800 to-zinc-600'>
    <Navbar></Navbar>
    <div className='max-w-4xl mx-auto px-4 md:px-6 py-8'>
    <Discovery onSubmit ={handleSubmit}></Discovery>
    {historyUploaded && <p className='px-4 py-2 flex justify-center items-center mb-2 gap-3 '>
      Music History Successfully Uploaded!
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="green" className="size-8">
        <path fillRule="evenodd" d="M2.25 12c0-5.385 4.365-9.75 9.75-9.75s9.75 4.365 9.75 9.75-4.365 9.75-9.75 9.75S2.25 17.385 2.25 12Zm13.36-1.814a.75.75 0 1 0-1.22-.872l-3.236 4.53L9.53 12.22a.75.75 0 0 0-1.06 1.06l2.25 2.25a.75.75 0 0 0 1.14-.094l3.75-5.25Z" clipRule="evenodd" />
      </svg>
      </p>}
    <div className='grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4'>
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
  </div>
  </div>
    </>
  )
}

export default App
