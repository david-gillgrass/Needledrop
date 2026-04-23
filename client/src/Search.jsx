import { useState } from "react"

function Search({onSearch}){
    
    const [query, setQuery] = useState('')

    return (

        <div>
            <label htmlFor="search">Search: </label>
        <input 
        type="text"
        value={query}
        onChange={(e)=> setQuery(e.target.value)}
        />
            <button type="button" onClick={() => onSearch(query)}>Search</button>
        </div>
    )

}

export default Search