import { useState } from "react";

function ImportBar({onImport}){

const [selectedFile, setSelectedFile] = useState(null)

return(
<div>
    <label htmlFor="upload">Upload:</label>
    <input id="upload" type="file" 
    onChange={(e)=> setSelectedFile(e.target.files[0])}
    />
    <button type="button" onClick={() => onImport(selectedFile)}>Upload</button>
</div>
)
}

export default ImportBar