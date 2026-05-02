import { useState } from "react";

function Discovery({onSubmit}){

    const [query, setQuery] = useState('')
    const [selectedFile, setSelectedFile] = useState(null)
    const [aiAgent, setAgent] = useState('claude')

    return(
    <div className="bg-zinc-800 border border-amber-400 rounded-xl p-4 mb-2 flex flex-col md:flex-row items-center gap-3">
        <label htmlFor="upload" className="bg-zinc-700 hover:bg-zinc-600 text-sm px-4 py-2 rounded-lg cursor-pointer transition-colors whitespace-nowrap gap-2 flex flex-row">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="size-6">
                <path fillRule="evenodd" d="M11.47 2.47a.75.75 0 0 1 1.06 0l4.5 4.5a.75.75 0 0 1-1.06 1.06l-3.22-3.22V16.5a.75.75 0 0 1-1.5 0V4.81L8.03 8.03a.75.75 0 0 1-1.06-1.06l4.5-4.5ZM3 15.75a.75.75 0 0 1 .75.75v2.25a1.5 1.5 0 0 0 1.5 1.5h13.5a1.5 1.5 0 0 0 1.5-1.5V16.5a.75.75 0 0 1 1.5 0v2.25a3 3 0 0 1-3 3H5.25a3 3 0 0 1-3-3V16.5a.75.75 0 0 1 .75-.75Z" clipRule="evenodd" />
            </svg> Upload Scrobbler 
            </label>
        <input type="file" id="upload" className="hidden"
        onChange={(e)=> setSelectedFile(e.target.files[0])}
        />
        
        <label htmlFor="search"></label>
        <input type="text" id="search" 
        value={query}
        onChange={(f)=> setQuery(f.target.value)}
        placeholder="Additional queries: Uptempo happy day etc..."
        className="flex-1 bg-zinc-700 placeholder-zinc-300 px-4 py-2 rounded-lg border border-zinc-400 focus:outline-none focus:border-amber-400 w-full"
        autoComplete="off"
        />

        <label htmlFor="aiAgent">AI Agent:</label>
        <select id="aiAgent" className="bg-zinc-700" onChange={(g) => setAgent(g.target.value)}>
            <option value="claude">Claude</option>
            <option value="groq">Groq</option>
        </select>
        
        <button type="button"
        className="bg-amber-400 hover:bg-amber-300 rounded-xl px-4 py-2 text-zinc-700 cursor-pointer transition-colors whitespace-nowrap w-full md:w-auto"
        onClick={()=> onSubmit(selectedFile,query,aiAgent)}
        >Submit</button>
    </div>
)
}

export default Discovery