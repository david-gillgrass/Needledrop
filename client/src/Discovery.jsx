import { useState } from "react";

function Discovery({onSubmit}){

    const [query, setQuery] = useState('')
    const [selectedFile, setSelectedFile] = useState(null)

    return(
    <div className="DiscoveryBar">
        <label htmlFor="upload">Upload: </label>
        <input type="file" id="upload" 
        onChange={(e)=> setSelectedFile(e.target.files[0])}
        />
        
        <label htmlFor="search">Additional Queries: </label>
        <input type="text" id="search" 
        value={query}
        onChange={(f)=> setQuery(f.target.value)}
        />
        
        <button type="button"
        onClick={()=> onSubmit(selectedFile,query)}
        >Submit</button>
    </div>
)
}

export default Discovery